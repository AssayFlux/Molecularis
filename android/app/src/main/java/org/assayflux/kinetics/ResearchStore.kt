package org.assayflux.molecularis

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.io.File
import java.util.UUID
import org.json.JSONObject

data class ResearchJob(
    val id: String,
    val inputName: String,
    val state: String,
    val sha256: String?,
    val message: String?,
    val provenanceToolId: String? = null,
    val provenanceToolVersion: String? = null,
    val provenanceParametersJson: String? = null,
    val provenanceCreatedAt: Long? = null,
    val analysisToolId: String? = null,
    val analysisToolVersion: String? = null,
    val analysisParametersJson: String? = null,
    val analysisCreatedAt: Long? = null,
    val analysisResultJson: String? = null,
)

data class RecoverableImport(val id: String, val uri: String)


class ResearchStore(context: Context) :
    SQLiteOpenHelper(context, "kinetics-research.db", null, DATABASE_VERSION) {

    private val appContext = context.applicationContext

    init {
        cleanupStalePlaintextCache()
    }

    /**
     * Recover plaintext analysis temporaries left by abrupt process death.
     * Only this app's uniquely-prefixed cache files older than 24 hours are eligible.
     */
    private fun cleanupStalePlaintextCache() {
        val cutoff = System.currentTimeMillis() - PLAINTEXT_CACHE_MAX_AGE_MS
        appContext.cacheDir.listFiles()
            ?.filter { file ->
                file.isFile && file.name.startsWith(PLAINTEXT_CACHE_PREFIX) &&
                    file.lastModified() > 0L && file.lastModified() < cutoff
            }
            ?.forEach { it.delete() }
    }

    override fun onConfigure(db: SQLiteDatabase) {
        super.onConfigure(db)
        db.setForeignKeyConstraintsEnabled(true)
    }

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """CREATE TABLE jobs (
                id TEXT PRIMARY KEY NOT NULL, input_name TEXT NOT NULL, input_uri TEXT NOT NULL,
                state TEXT NOT NULL, sha256 TEXT, byte_count INTEGER, message TEXT,
                storage_path TEXT, exported_at INTEGER, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        db.execSQL(
            """CREATE TABLE provenance (
                job_id TEXT PRIMARY KEY NOT NULL REFERENCES jobs(id), tool_id TEXT NOT NULL,
                tool_version TEXT NOT NULL, input_sha256 TEXT NOT NULL,
                parameters_json TEXT NOT NULL, created_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        db.execSQL("CREATE INDEX jobs_created_at_idx ON jobs(created_at DESC)")
        db.execSQL("CREATE INDEX provenance_created_at_idx ON provenance(created_at DESC)")
        db.execSQL("""CREATE TABLE analysis_results (job_id TEXT PRIMARY KEY NOT NULL REFERENCES jobs(id) ON DELETE CASCADE, tool_id TEXT NOT NULL, tool_version TEXT NOT NULL, input_sha256 TEXT NOT NULL, parameters_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at INTEGER NOT NULL)""")
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        if (oldVersion < 2) {
            db.execSQL("ALTER TABLE jobs ADD COLUMN storage_path TEXT")
        }
        if (oldVersion < 3) {
            db.execSQL("ALTER TABLE jobs ADD COLUMN exported_at INTEGER")
            db.execSQL("CREATE INDEX IF NOT EXISTS provenance_created_at_idx ON provenance(created_at DESC)")
        }
        if (oldVersion < 4) {
            db.execSQL("""CREATE TABLE analysis_results (job_id TEXT PRIMARY KEY NOT NULL REFERENCES jobs(id) ON DELETE CASCADE, tool_id TEXT NOT NULL, tool_version TEXT NOT NULL, input_sha256 TEXT NOT NULL, parameters_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at INTEGER NOT NULL)""")
        }
    }

    fun createJob(id: String, name: String, uri: String) {
        val now = System.currentTimeMillis()
        val values = ContentValues().apply {
            put("id", id)
            put("input_name", name)
            put("input_uri", uri)
            put("state", "queued")
            put("created_at", now)
            put("updated_at", now)
        }
        writableDatabase.insertOrThrow("jobs", null, values)
    }

    fun updateJob(
        id: String, state: String, hash: String? = null,
        bytes: Long? = null, message: String? = null,
    ) {
        val values = ContentValues().apply {
            put("state", state)
            put("updated_at", System.currentTimeMillis())
            if (hash != null) put("sha256", hash)
            if (bytes != null) put("byte_count", bytes)
            if (message != null) put("message", message)
        }
        writableDatabase.update("jobs", values, "id=?", arrayOf(id))
    }

    /** Atomically claim or recover a running import; a cancelled job cannot be resurrected by a late worker. */
    fun startImport(id: String): Boolean {
        val values = ContentValues().apply {
            put("state", "running")
            put("updated_at", System.currentTimeMillis())
        }
        return writableDatabase.update(
            "jobs", values, "id=? AND state IN ('queued','running')", arrayOf(id),
        ) == 1
    }

    /** Queue only an explicitly resumable failed/cancelled import before scheduling its worker. */
    fun queueImportForResume(id: String): Boolean {
        val values = ContentValues().apply {
            put("state", "queued")
            put("message", "Resume queued")
            put("updated_at", System.currentTimeMillis())
        }
        return writableDatabase.update(
            "jobs", values, "id=? AND state IN ('cancelled','failed')", arrayOf(id),
        ) == 1
    }

    /** Cancellation wins atomically against import finalization; completed jobs are never downgraded. */
    fun cancelActiveImport(id: String): Boolean {
        val db = writableDatabase
        db.beginTransaction()
        try {
            val values = ContentValues().apply {
                put("state", "cancelled")
                put("message", "Cancellation requested. Any encrypted partial input is retained and may be resumed.")
                put("updated_at", System.currentTimeMillis())
            }
            val changed = db.update(
                "jobs", values, "id=? AND state IN ('queued','running')", arrayOf(id),
            ) == 1
            if (changed) {
                db.delete("analysis_results", "job_id=?", arrayOf(id))
                db.setTransactionSuccessful()
            }
            return changed
        } finally {
            db.endTransaction()
        }
    }

    fun isJobCancelled(id: String): Boolean = readableDatabase.rawQuery(
        "SELECT state FROM jobs WHERE id=?", arrayOf(id),
    ).use { cursor -> cursor.moveToFirst() && cursor.getString(0) == "cancelled" }

    /** Resolve only canonical finalized KDAT files inside the dedicated no-backup directory. */
    private fun resolveEncryptedInput(path: String): File {
        val root = File(appContext.noBackupFilesDir, "research-inputs").canonicalFile
        val candidate = File(path).canonicalFile
        require(candidate.parentFile == root && candidate.extension == "kdat") {
            "Encrypted input path is outside the dedicated app-private storage directory"
        }
        return candidate
    }

    /** Atomically records encrypted storage location, successful state and provenance. */
    fun completeImport(id: String, hash: String, bytes: Long, encryptedPath: String) {
        val verifiedPath = resolveEncryptedInput(encryptedPath)
        require(verifiedPath.isFile && verifiedPath.length() > LocalCrypto.HEADER_BYTES) {
            "Final encrypted input file is missing or empty"
        }
        val db = writableDatabase
        db.beginTransaction()
        try {
            val currentState = db.rawQuery(
                "SELECT state FROM jobs WHERE id=?", arrayOf(id),
            ).use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }
            check(currentState == "running") {
                "Import cannot be finalized after cancellation or outside the running state"
            }
            val values = ContentValues().apply {
                put("state", "succeeded")
                put("sha256", hash)
                put("byte_count", bytes)
                put("storage_path", encryptedPath)
                put("message", "Imported, encrypted at rest and SHA-256 recorded")
                put("updated_at", System.currentTimeMillis())
            }
            check(db.update("jobs", values, "id=?", arrayOf(id)) == 1) {
                "Import job disappeared before finalization"
            }
            val provenance = ContentValues().apply {
                put("job_id", id)
                put("tool_id", "file-import-encrypt-sha256")
                put("tool_version", "3")
                put("input_sha256", hash)
                put("parameters_json", """{"encryption":"AES-256-GCM","format":"chunked-v2","aad":"job-id+chunk-index","storage":"app-private-no-backup"}""")
                put("created_at", System.currentTimeMillis())
            }
            db.insertWithOnConflict(
                "provenance", null, provenance, SQLiteDatabase.CONFLICT_REPLACE,
            )
            db.setTransactionSuccessful()
        } finally {
            db.endTransaction()
        }
    }

    /** Persist an analysis result with the exact imported-input digest and explicit method parameters. */
    fun saveAnalysisResult(id: String, toolId: String, toolVersion: String, parametersJson: String, resultJson: String) {
        require(toolId.isNotBlank() && toolVersion.isNotBlank()) { "Analysis tool identity is required" }
        require(resultJson.isNotBlank() && resultJson.length <= MAX_ANALYSIS_RESULT_CHARS) {
            "Analysis result is empty or exceeds the storage limit"
        }
        val db = writableDatabase
        db.beginTransaction()
        try {
            val inputHash = db.rawQuery("SELECT sha256,state FROM jobs WHERE id=?", arrayOf(id)).use { cursor ->
                check(cursor.moveToFirst() && cursor.getString(1) == "succeeded" && !cursor.isNull(0)) {
                    "Only a completed, hash-verified import can be analysed"
                }
                cursor.getString(0).also { hash ->
                    require(hash.matches(Regex("[a-f0-9]{64}"))) { "Imported input SHA-256 is invalid" }
                }
            }
            val values = ContentValues().apply {
                put("job_id", id); put("tool_id", toolId); put("tool_version", toolVersion)
                put("input_sha256", inputHash); put("parameters_json", parametersJson)
                put("result_json", resultJson); put("created_at", System.currentTimeMillis())
            }
            db.insertWithOnConflict("analysis_results", null, values, SQLiteDatabase.CONFLICT_REPLACE)
            db.setTransactionSuccessful()
        } finally { db.endTransaction() }
    }

    fun analysisResultJson(id: String): String? = readableDatabase.rawQuery(
        "SELECT result_json FROM analysis_results WHERE job_id=?", arrayOf(id),
    ).use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }

    /** Portable analysis record, bound to the exact import digest; excludes source URI and paths. */
    fun analysisExportJson(id: String): String? = readableDatabase.rawQuery(
        """SELECT a.tool_id,a.tool_version,a.input_sha256,a.parameters_json,a.result_json,a.created_at
           FROM analysis_results a JOIN jobs j ON j.id=a.job_id
           WHERE a.job_id=? AND j.state='succeeded' AND j.sha256=a.input_sha256""".trimIndent(),
        arrayOf(id),
    ).use { cursor ->
        if (!cursor.moveToFirst()) null else {
            val parameters = runCatching { JSONObject(cursor.getString(3)) }
                .getOrElse { JSONObject().put("raw_parameters", cursor.getString(3)) }
            JSONObject()
                .put("schema", "org.assayflux.molecularis.analysis-result")
                .put("schema_version", 1)
                .put("record_type", "research_analysis")
                .put("tool_id", cursor.getString(0))
                .put("tool_version", cursor.getString(1))
                .put("input_sha256", cursor.getString(2))
                .put("parameters", parameters)
                .put("result", JSONObject(cursor.getString(4)))
                .put("created_at_epoch_ms", cursor.getLong(5))
                .put("scope_note", "Research-use QC only. No diagnosis, clinical interpretation or independent biological validation is implied.")
                .toString(2)
        }
    }

    fun storedInputName(id: String): String? = readableDatabase.rawQuery(
        "SELECT input_name FROM jobs WHERE id=?", arrayOf(id),
    ).use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }

    /** Read only the committed import size before any analysis plaintext is materialized. */
    fun storedInputByteCount(id: String): Long? = readableDatabase.rawQuery(
        "SELECT byte_count FROM jobs WHERE id=? AND state='succeeded' AND storage_path IS NOT NULL",
        arrayOf(id),
    ).use { cursor -> if (cursor.moveToFirst() && !cursor.isNull(0)) cursor.getLong(0) else null }

    fun storedInputPath(id: String): String? {
        readableDatabase.rawQuery(
            "SELECT storage_path FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            return if (cursor.moveToFirst() && !cursor.isNull(0)) cursor.getString(0) else null
        }
    }

    /** Materialize an authenticated temporary plaintext copy for a caller-controlled analysis/export. */
    fun materializeStoredInput(id: String, destination: File): Boolean {
        val safeRoot = appContext.cacheDir.canonicalFile.toPath()
        val safeDestination = destination.canonicalFile.toPath()
        require(safeDestination.startsWith(safeRoot) && safeDestination != safeRoot) {
            "Decrypted research inputs may only be materialized inside the app-private cache"
        }
        val stored = readableDatabase.rawQuery(
            "SELECT storage_path,sha256 FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst() || cursor.isNull(0) || cursor.isNull(1)) null
            else Pair(cursor.getString(0), cursor.getString(1))
        } ?: return false
        LocalCrypto.decryptChunkedFile(
            resolveEncryptedInput(stored.first), destination, "kinetics-import:$id", stored.second,
        )
        return true
    }

    /** Stream an authenticated, hash-verified input to a caller-selected SAF output stream. */
    fun exportStoredInput(id: String, destination: java.io.OutputStream): Boolean {
        val stored = readableDatabase.rawQuery(
            "SELECT storage_path,sha256 FROM jobs WHERE id=? AND state='succeeded'",
            arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst() || cursor.isNull(0) || cursor.isNull(1)) null
            else Pair(cursor.getString(0), cursor.getString(1))
        } ?: return false
        LocalCrypto.decryptChunkedFileToStream(
            resolveEncryptedInput(stored.first), destination, "kinetics-import:$id", stored.second,
        )
        val exported = ContentValues().apply {
            put("exported_at", System.currentTimeMillis())
            put("updated_at", System.currentTimeMillis())
        }
        check(writableDatabase.update("jobs", exported, "id=?", arrayOf(id)) == 1) {
            "Exported job metadata disappeared"
        }
        return true
    }

    /** Run a local analysis callback and always remove its plaintext cache file. */
    fun <T> withStoredInput(id: String, action: (File) -> T): T? {
        val temporary = File(appContext.cacheDir, "kinetics-analysis-" + UUID.randomUUID() + ".tmp")
        return withPrivateTemporaryFile(
            file = temporary,
            materialize = { destination -> materializeStoredInput(id, destination) },
            action = action,
        )
    }

    /** Update an explanatory message without changing the durable job state. */
    fun updateJobMessage(id: String, message: String) {
        val values = ContentValues().apply {
            put("message", message)
            put("updated_at", System.currentTimeMillis())
        }
        check(writableDatabase.update("jobs", values, "id=?", arrayOf(id)) == 1) {
            "Research job does not exist"
        }
    }

    fun updateProgress(id: String, bytes: Long) {
        val values = ContentValues().apply {
            put("byte_count", bytes)
            put("updated_at", System.currentTimeMillis())
        }
        writableDatabase.update("jobs", values, "id=?", arrayOf(id))
    }

    fun progress(id: String): Long {
        readableDatabase.rawQuery(
            "SELECT byte_count FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            return if (cursor.moveToFirst() && !cursor.isNull(0)) cursor.getLong(0) else 0L
        }
    }

    fun inputUri(id: String): String? {
        readableDatabase.rawQuery(
            "SELECT input_uri FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            return if (cursor.moveToFirst()) cursor.getString(0) else null
        }
    }

    /**
     * Preserve encrypted records when the Keystore alias is missing. Never create a replacement
     * key or delete ciphertext automatically: the original data is unrecoverable without its key.
     * Returns the number of completed jobs moved to the explicit recovery-required state.
     */
    fun markKeyLossRecoveryRequired(): Int {
        val db = writableDatabase
        db.beginTransaction()
        try {
            val completedValues = ContentValues().apply {
                put("state", "recovery_required")
                put("message", "Encryption key is missing. Completed ciphertext is preserved; do not overwrite this record. Restore the original Android Keystore backup/device state if available, otherwise export is unavailable.")
                put("updated_at", System.currentTimeMillis())
            }
            var changed = db.update(
                "jobs", completedValues,
                "state='succeeded' AND storage_path IS NOT NULL", null,
            )

            // Encrypted partials also depend on the lost key. Mark only jobs whose
            // authenticated staging file actually exists; never delete or reset it.
            val stagingRoot = File(appContext.noBackupFilesDir, "research-imports").canonicalFile
            stagingRoot.listFiles()
                ?.filter { it.isFile && it.name.endsWith(".encpart") && it.length() > 0L }
                ?.forEach { partial ->
                    val id = partial.name.removeSuffix(".encpart")
                    if (!id.matches(Regex("[A-Za-z0-9_-]{1,80}"))) return@forEach
                    val partialValues = ContentValues().apply {
                        put("state", "recovery_required")
                        put("message", "Encrypted partial import is preserved, but its Keystore key is missing and it cannot be resumed. Re-import the original source as a new job after confirming the source is still available.")
                        put("updated_at", System.currentTimeMillis())
                    }
                    changed += db.update(
                        "jobs", partialValues,
                        "id=? AND storage_path IS NULL AND state IN ('queued','running','cancelled','failed')",
                        arrayOf(id),
                    )
                }
            db.setTransactionSuccessful()
            return changed
        } finally {
            db.endTransaction()
        }
    }

    /**
     * Report encrypted files without a matching durable job/storage reference.
     * Findings are inventory-only: this method never deletes or modifies ciphertext.
     */
    fun encryptedOrphanInventory(): List<EncryptedOrphanFile> {
        val knownIds = mutableSetOf<String>()
        val referencedPaths = mutableSetOf<String>()
        val jobsWithFinalStorage = mutableSetOf<String>()
        readableDatabase.rawQuery(
            "SELECT id,storage_path FROM jobs", emptyArray(),
        ).use { cursor ->
            while (cursor.moveToNext()) {
                val id = cursor.getString(0)
                knownIds += id
                if (!cursor.isNull(1)) {
                    val path = cursor.getString(1)
                    referencedPaths += runCatching { File(path).canonicalPath }.getOrDefault(path)
                    jobsWithFinalStorage += id
                }
            }
        }
        return EncryptedOrphanScanner.scan(
            finalizedDirectory = File(appContext.noBackupFilesDir, "research-inputs"),
            stagingDirectory = File(appContext.noBackupFilesDir, "research-imports"),
            referencedFinalPaths = referencedPaths,
            knownJobIds = knownIds,
            jobsWithFinalStorage = jobsWithFinalStorage,
        )
    }

    /** Imports left queued/running by process death; unique WorkManager names make re-enqueue idempotent. */
    fun recoverableImports(): List<RecoverableImport> {
        val result = mutableListOf<RecoverableImport>()
        readableDatabase.rawQuery(
            "SELECT id,input_uri FROM jobs WHERE state IN ('queued','running') ORDER BY created_at",
            emptyArray(),
        ).use { cursor ->
            while (cursor.moveToNext()) {
                result += RecoverableImport(cursor.getString(0), cursor.getString(1))
            }
        }
        return result
    }

    /** Delete local encrypted input, partial staging and associated SQLite metadata (not secure erase). */
    fun deleteStoredJob(id: String): Boolean {
        require(id.matches(Regex("[A-Za-z0-9_-]{1,80}"))) { "Invalid research job identifier" }
        val storedPath = readableDatabase.rawQuery(
            "SELECT storage_path FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst()) return false
            if (cursor.isNull(0)) null else cursor.getString(0)
        }
        val encrypted = storedPath?.let(::resolveEncryptedInput)
        val stagingRoot = File(appContext.noBackupFilesDir, "research-imports").canonicalFile
        val partial = File(stagingRoot, "$id.encpart").canonicalFile
        val legacyPlaintext = File(stagingRoot, "$id.part").canonicalFile
        require(partial.parentFile == stagingRoot && legacyPlaintext.parentFile == stagingRoot) {
            "Invalid import staging path"
        }
        if (encrypted != null && encrypted.exists() && !encrypted.delete()) {
            throw IllegalStateException("Encrypted input could not be deleted")
        }
        if (partial.exists() && !partial.delete()) {
            throw IllegalStateException("Encrypted partial input could not be deleted")
        }
        if (legacyPlaintext.exists() && !legacyPlaintext.delete()) {
            throw IllegalStateException("Legacy plaintext partial could not be deleted")
        }
        val db = writableDatabase
        db.beginTransaction()
        try {
            db.delete("analysis_results", "job_id=?", arrayOf(id))
            db.delete("provenance", "job_id=?", arrayOf(id))
            check(db.delete("jobs", "id=?", arrayOf(id)) == 1) {
                "Research job metadata disappeared during deletion"
            }
            db.setTransactionSuccessful()
        } finally {
            db.endTransaction()
        }
        return true
    }


    /**
     * Build a portable, machine-readable import-provenance record.
     * Source URI and encrypted storage path are deliberately excluded from export.
     */
    fun provenanceJson(id: String): String? {
        return readableDatabase.rawQuery(
            """SELECT j.id,j.input_name,j.state,j.sha256,j.byte_count,j.created_at,j.updated_at,
                      p.tool_id,p.tool_version,p.input_sha256,p.parameters_json,p.created_at
               FROM jobs j INNER JOIN provenance p ON p.job_id=j.id
               WHERE j.id=?""".trimIndent(),
            arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst()) {
                null
            } else {
                val rawParameters = cursor.getString(10)
                val parameters = runCatching { JSONObject(rawParameters) }
                    .getOrElse { JSONObject().put("unparsed_parameters_json", rawParameters) }
                val job = JSONObject()
                    .put("id", cursor.getString(0))
                    .put("input_name", cursor.getString(1))
                    .put("state", cursor.getString(2))
                    .put("input_sha256", if (cursor.isNull(3)) JSONObject.NULL else cursor.getString(3))
                    .put("byte_count", if (cursor.isNull(4)) JSONObject.NULL else cursor.getLong(4))
                    .put("created_at_epoch_ms", cursor.getLong(5))
                    .put("updated_at_epoch_ms", cursor.getLong(6))
                val provenance = JSONObject()
                    .put("tool_id", cursor.getString(7))
                    .put("tool_version", cursor.getString(8))
                    .put("input_sha256", cursor.getString(9))
                    .put("parameters", parameters)
                    .put("recorded_at_epoch_ms", cursor.getLong(11))
                JSONObject()
                    .put("schema", "org.assayflux.molecularis.provenance")
                    .put("schema_version", 1)
                    .put("record_type", "import")
                    .put("job", job)
                    .put("provenance", provenance)
                    .put(
                        "scope_note",
                        "Import provenance only. This record does not represent a scientific analysis result.",
                    )
                    .toString(2)
            }
        }
    }

    fun provenanceSummary(id: String): String? {
        val record = readableDatabase.rawQuery(
            """SELECT j.id,j.input_name,j.state,j.sha256,j.byte_count,j.created_at,j.updated_at,
                      p.tool_id,p.tool_version,p.parameters_json,p.created_at
               FROM jobs j INNER JOIN provenance p ON p.job_id=j.id
               WHERE j.id=?""".trimIndent(),
            arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst()) null else ImportProvenanceSummary(
                jobId = cursor.getString(0),
                inputName = cursor.getString(1),
                state = cursor.getString(2),
                inputSha256 = if (cursor.isNull(3)) null else cursor.getString(3),
                byteCount = if (cursor.isNull(4)) null else cursor.getLong(4),
                jobCreatedAtEpochMs = cursor.getLong(5),
                jobUpdatedAtEpochMs = cursor.getLong(6),
                toolId = cursor.getString(7),
                toolVersion = cursor.getString(8),
                parametersJson = cursor.getString(9),
                recordedAtEpochMs = cursor.getLong(10),
            )
        } ?: return null
        return ImportProvenanceSummaryFormatter.render(record)
    }

    fun recentJobs(limit: Int = 30): List<ResearchJob> {
        val result = mutableListOf<ResearchJob>()
        readableDatabase.rawQuery(
            """SELECT j.id,j.input_name,j.state,j.sha256,j.message,
                      p.tool_id,p.tool_version,p.parameters_json,p.created_at,
                      a.tool_id,a.tool_version,a.parameters_json,a.created_at,a.result_json
               FROM jobs j
               LEFT JOIN provenance p ON p.job_id=j.id
               LEFT JOIN analysis_results a ON a.job_id=j.id
               ORDER BY j.created_at DESC LIMIT ?""".trimIndent(),
            arrayOf(limit.coerceIn(1, 100).toString()),
        ).use { cursor ->
            while (cursor.moveToNext()) {
                result += ResearchJob(
                    id = cursor.getString(0),
                    inputName = cursor.getString(1),
                    state = cursor.getString(2),
                    sha256 = if (cursor.isNull(3)) null else cursor.getString(3),
                    message = if (cursor.isNull(4)) null else cursor.getString(4),
                    provenanceToolId = if (cursor.isNull(5)) null else cursor.getString(5),
                    provenanceToolVersion = if (cursor.isNull(6)) null else cursor.getString(6),
                    provenanceParametersJson = if (cursor.isNull(7)) null else cursor.getString(7),
                    provenanceCreatedAt = if (cursor.isNull(8)) null else cursor.getLong(8),
                    analysisToolId = if (cursor.isNull(9)) null else cursor.getString(9),
                    analysisToolVersion = if (cursor.isNull(10)) null else cursor.getString(10),
                    analysisParametersJson = if (cursor.isNull(11)) null else cursor.getString(11),
                    analysisCreatedAt = if (cursor.isNull(12)) null else cursor.getLong(12),
                    analysisResultJson = if (cursor.isNull(13)) null else cursor.getString(13),
                )
            }
        }
        return result
    }

    companion object {
        private const val DATABASE_VERSION = 4
        private const val MAX_ANALYSIS_RESULT_CHARS = 2_000_000
        private const val PLAINTEXT_CACHE_PREFIX = "kinetics-analysis-"
        private const val PLAINTEXT_CACHE_MAX_AGE_MS = 24L * 60L * 60L * 1000L
    }
}
