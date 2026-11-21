package org.assayflux.molecularis

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import org.json.JSONObject
import java.io.File
import java.security.MessageDigest
import java.util.UUID

data class SavedPublicRecord(
    val id: String, val source: String, val accession: String, val format: String,
    val sourceUrl: String, val retrievedAt: String, val sha256: String,
    val byteCount: Long, val analysisJson: String?,
)

internal class PublicRecordStore(context: Context) :
    SQLiteOpenHelper(context.applicationContext, "kinetics-public-records.db", null, 1) {
    private val appContext = context.applicationContext

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """CREATE TABLE public_records (
                id TEXT PRIMARY KEY NOT NULL, source TEXT NOT NULL, accession TEXT NOT NULL,
                format TEXT NOT NULL, source_url TEXT NOT NULL, retrieved_at TEXT NOT NULL,
                sha256 TEXT NOT NULL, byte_count INTEGER NOT NULL, encrypted_path TEXT NOT NULL,
                analysis_json TEXT, saved_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        db.execSQL("CREATE INDEX public_records_saved_at_idx ON public_records(saved_at DESC)")
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) = Unit

    fun save(record: PublicScientificRecord): SavedPublicRecord {
        require(record.content.isNotEmpty()) { "Cannot save an empty public record" }
        val bytes = record.content.toByteArray(Charsets.UTF_8)
        require(bytes.size <= MAX_RECORD_BYTES) { "Public record exceeds the 24 MiB storage limit" }
        val actualHash = sha256(bytes)
        require(actualHash.equals(record.sha256, ignoreCase = true)) { "Public record checksum does not match the retrieved content" }
        val id = sha256("${record.source}|${record.accession}|${record.sha256}".toByteArray())
        val directory = File(appContext.noBackupFilesDir, "public-records").canonicalFile
        check(directory.exists() || directory.mkdirs()) { "Private public-record storage is unavailable" }
        val destination = File(directory, "$id.kdat").canonicalFile
        require(destination.parentFile == directory) { "Invalid public-record storage path" }
        val temporary = File(directory, "$id.tmp")
        check(!temporary.exists() || temporary.delete()) { "Stale encrypted temporary could not be removed" }
        try {
            LocalCrypto.ensureChunkedFileHeader(temporary)
            var offset = 0
            var chunkIndex = 0L
            while (offset < bytes.size) {
                val end = minOf(offset + LocalCrypto.CHUNK_BYTES, bytes.size)
                LocalCrypto.appendEncryptedChunk(
                    temporary, bytes.copyOfRange(offset, end),
                    LocalCrypto.associatedData("kinetics-public-record:$id", chunkIndex),
                )
                offset = end
                chunkIndex++
            }
            if (destination.exists()) check(destination.delete()) { "Previous encrypted record could not be replaced" }
            check(temporary.renameTo(destination)) { "Encrypted public record could not be finalized" }
            val values = ContentValues().apply {
                put("id", id); put("source", record.source); put("accession", record.accession)
                put("format", record.format); put("source_url", record.sourceUrl)
                put("retrieved_at", record.retrievedAt); put("sha256", record.sha256.lowercase())
                put("byte_count", bytes.size.toLong()); put("encrypted_path", destination.absolutePath)
                put("saved_at", System.currentTimeMillis())
            }
            writableDatabase.insertWithOnConflict("public_records", null, values, SQLiteDatabase.CONFLICT_REPLACE)
            enforceCacheQuota(protectedId = id)
        } catch (error: Exception) {
            temporary.delete()
            throw error
        }
        return get(id) ?: error("Saved public record metadata could not be read back")
    }

    fun saveAnalysis(id: String, analysisJson: String) {
        require(analysisJson.isNotBlank() && analysisJson.length <= MAX_ANALYSIS_CHARS) {
            "Analysis result is empty or exceeds the storage limit"
        }
        JSONObject(analysisJson)
        val values = ContentValues().apply { put("analysis_json", analysisJson) }
        check(writableDatabase.update("public_records", values, "id=?", arrayOf(id)) == 1) {
            "Saved public record does not exist"
        }
    }

    fun get(id: String): SavedPublicRecord? = readableDatabase.rawQuery(
        """SELECT id,source,accession,format,source_url,retrieved_at,sha256,byte_count,analysis_json
           FROM public_records WHERE id=?""".trimIndent(), arrayOf(id),
    ).use { cursor ->
        if (!cursor.moveToFirst()) null else SavedPublicRecord(
            cursor.getString(0), cursor.getString(1), cursor.getString(2), cursor.getString(3),
            cursor.getString(4), cursor.getString(5), cursor.getString(6), cursor.getLong(7),
            if (cursor.isNull(8)) null else cursor.getString(8),
        )
    }

    fun recent(limit: Int = 20): List<SavedPublicRecord> {
        require(limit in 1..100)
        val ids = readableDatabase.rawQuery(
            "SELECT id FROM public_records ORDER BY saved_at DESC LIMIT ?", arrayOf(limit.toString()),
        ).use { cursor -> buildList { while (cursor.moveToNext()) add(cursor.getString(0)) } }
        return ids.mapNotNull(::get)
    }

    fun totalBytes(): Long = readableDatabase.rawQuery(
        "SELECT COALESCE(SUM(byte_count),0) FROM public_records", null,
    ).use { cursor -> if (cursor.moveToFirst()) cursor.getLong(0) else 0L }

    fun recordCount(): Int = readableDatabase.rawQuery(
        "SELECT COUNT(*) FROM public_records", null,
    ).use { cursor -> if (cursor.moveToFirst()) cursor.getInt(0) else 0 }

    fun deleteAll(): Int {
        val ids = readableDatabase.rawQuery("SELECT id FROM public_records", null).use { cursor ->
            buildList { while (cursor.moveToNext()) add(cursor.getString(0)) }
        }
        return ids.count { delete(it) }
    }

    private fun enforceCacheQuota(protectedId: String) {
        var bytes = totalBytes()
        var count = recordCount()
        if (bytes <= MAX_CACHE_BYTES && count <= MAX_RECORDS) return
        val oldest = readableDatabase.rawQuery(
            "SELECT id FROM public_records WHERE id<>? ORDER BY saved_at ASC", arrayOf(protectedId),
        ).use { cursor -> buildList { while (cursor.moveToNext()) add(cursor.getString(0)) } }
        for (id in oldest) {
            if (bytes <= MAX_CACHE_BYTES && count <= MAX_RECORDS) break
            val record = get(id) ?: continue
            if (delete(id)) { bytes -= record.byteCount; count-- }
        }
        check(bytes <= MAX_CACHE_BYTES && count <= MAX_RECORDS) {
            "Public reference cache quota cannot be met without deleting the newly saved record"
        }
    }
    fun <T> withContent(id: String, action: (File) -> T): T? {
        val saved = get(id) ?: return null
        val directory = File(appContext.noBackupFilesDir, "public-records").canonicalFile
        val encrypted = File(directory, "$id.kdat").canonicalFile
        require(encrypted.parentFile == directory && encrypted.absolutePath == encryptedPath(id)) {
            "Saved public record path failed validation"
        }
        val temporary = File(appContext.cacheDir, "kinetics-public-$id-${UUID.randomUUID()}.tmp")
        try {
            LocalCrypto.decryptChunkedFile(encrypted, temporary, "kinetics-public-record:$id", saved.sha256)
            require(temporary.length() == saved.byteCount) { "Saved public record byte count is inconsistent" }
            return action(temporary)
        } finally {
            temporary.delete()
        }
    }

    fun loadRecord(id: String): PublicScientificRecord? {
        val metadata = get(id) ?: return null
        val content = withContent(id) { file ->
            file.readText(Charsets.UTF_8)
        } ?: return null
        return PublicScientificRecord(
            source = metadata.source,
            accession = metadata.accession,
            format = metadata.format,
            sourceUrl = metadata.sourceUrl,
            retrievedAt = metadata.retrievedAt,
            sha256 = metadata.sha256,
            content = content,
        )
    }

    fun delete(id: String): Boolean {
        val path = encryptedPath(id) ?: return false
        val directory = File(appContext.noBackupFilesDir, "public-records").canonicalFile
        val file = File(path).canonicalFile
        require(file.parentFile == directory && file.extension == "kdat") { "Saved public record path failed validation" }
        val deleted = !file.exists() || file.delete()
        if (deleted) writableDatabase.delete("public_records", "id=?", arrayOf(id))
        return deleted
    }

    private fun encryptedPath(id: String): String? = readableDatabase.rawQuery(
        "SELECT encrypted_path FROM public_records WHERE id=?", arrayOf(id),
    ).use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }

    private fun sha256(bytes: ByteArray): String =
        MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it) }

    companion object {
        private const val MAX_RECORD_BYTES = 24 * 1024 * 1024
        private const val MAX_CACHE_BYTES = 200L * 1024 * 1024
        private const val MAX_RECORDS = 50
        private const val MAX_ANALYSIS_CHARS = 2_000_000
    }
}
