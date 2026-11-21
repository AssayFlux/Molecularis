package org.assayflux.molecularis

import android.content.Context
import org.json.JSONObject
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.security.MessageDigest
import java.nio.file.Files
import java.nio.file.StandardCopyOption

data class DataPackManifest(
    val id: String,
    val version: String,
    val source: String,
    val license: String,
    val sha256: String,
    val sizeBytes: Long,
)

/** Installs data-only packs after manifest, size and checksum checks; never loads executable content. */
class DataPackManager(context: Context) {
    private val root = File(context.filesDir, "datapacks").apply { mkdirs() }
    private val maximumPackBytes = 256L * 1024L * 1024L

    fun parseManifest(json: String): DataPackManifest {
        val value = JSONObject(json)
        val manifest = DataPackManifest(
            id = value.getString("id"),
            version = value.getString("version"),
            source = value.getString("source"),
            license = value.getString("license"),
            sha256 = value.getString("sha256").lowercase(),
            sizeBytes = value.getLong("size_bytes"),
        )
        require(manifest.id.matches(Regex("[A-Za-z0-9._-]{1,80}")) && manifest.id !in setOf(".", "..")) { "Invalid pack id" }
        require(manifest.version.matches(Regex("[A-Za-z0-9._-]{1,80}")) && manifest.version !in setOf(".", "..")) { "Invalid pack version" }
        require(manifest.source.startsWith("https://"))
        require(manifest.license.isNotBlank()) { "License metadata is mandatory" }
        require(manifest.sha256.matches(Regex("[a-f0-9]{64}"))) { "Invalid SHA-256" }
        require(manifest.sizeBytes in 1..maximumPackBytes) { "Pack size outside permitted range" }
        return manifest
    }

    @Synchronized
    fun install(source: File, manifest: DataPackManifest): File {
        // Revalidate even programmatically-created manifests: callers must not be able
        // to bypass parseManifest and escape the private data-pack directory.
        require(manifest.id.matches(Regex("[A-Za-z0-9._-]{1,80}")) && manifest.id !in setOf(".", "..")) { "Invalid pack id" }
        require(manifest.version.matches(Regex("[A-Za-z0-9._-]{1,80}")) && manifest.version !in setOf(".", "..")) { "Invalid pack version" }
        require(manifest.source.startsWith("https://") && manifest.license.isNotBlank()) {
            "Pack source and license metadata are mandatory"
        }
        require(manifest.sha256.matches(Regex("[a-f0-9]{64}"))) { "Invalid SHA-256" }
        require(manifest.sizeBytes in 1..maximumPackBytes) { "Pack size outside permitted range" }
        require(source.isFile && source.length() == manifest.sizeBytes) { "Pack size mismatch" }

        val destinationDir = File(root, manifest.id).apply { mkdirs() }
        val destination = File(destinationDir, manifest.version + ".data")
        require(!destination.exists()) { "This pack version is already installed" }
        val temporary = File.createTempFile("pack-" + manifest.version + "-", ".tmp", destinationDir)
        val digest = MessageDigest.getInstance("SHA-256")
        var copied = 0L
        try {
            // Hash the exact byte stream being installed to close the hash/copy TOCTOU gap.
            FileInputStream(source).use { input ->
                FileOutputStream(temporary, false).use { output ->
                    val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                    while (true) {
                        val count = input.read(buffer)
                        if (count < 0) break
                        copied += count
                        require(copied <= manifest.sizeBytes && copied <= maximumPackBytes) {
                            "Pack grew beyond its declared size"
                        }
                        digest.update(buffer, 0, count)
                        output.write(buffer, 0, count)
                    }
                    output.fd.sync()
                }
            }
            require(copied == manifest.sizeBytes) { "Pack size changed during installation" }
            val actual = digest.digest().joinToString("") { "%02x".format(it) }
            require(actual == manifest.sha256) { "Pack checksum mismatch" }
            check(!destination.exists()) { "This pack version is already installed" }
            // Same-directory atomic rename: never expose a partially copied installed pack.
            Files.move(
                temporary.toPath(), destination.toPath(), StandardCopyOption.ATOMIC_MOVE,
            )
            return destination
        } catch (error: Exception) {
            temporary.delete()
            throw error
        }
    }
}
