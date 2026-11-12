package org.molecularis.app.features

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import android.os.StatFs
import org.json.JSONObject
import java.io.File
import java.security.MessageDigest
import java.nio.file.Files
import java.nio.file.StandardCopyOption

data class ModelCompatibility(
    val compatible: Boolean,
    val reasons: List<String>,
    val deviceRamMb: Long,
    val availableStorageBytes: Long,
    val runtimeAvailable: Boolean
)

class ModelCompatibilityChecker(context: Context) {
    private val appContext = context.applicationContext

    fun check(model: ModelCatalogEntry): ModelCompatibility {
        val reasons = mutableListOf<String>()
        val activityManager = appContext.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        val memory = ActivityManager.MemoryInfo().also(activityManager::getMemoryInfo)
        val totalRamMb = memory.totalMem / (1024L * 1024L)
        val storage = StatFs(appContext.filesDir.absolutePath)
        val availableStorage = storage.availableBytes
        if (Build.VERSION.SDK_INT < model.minSdk) reasons += "Requires Android API ${model.minSdk}; this device is API ${Build.VERSION.SDK_INT}."
        if (totalRamMb < model.minRamMb) reasons += "Requires at least ${model.minRamMb} MiB RAM; device reports ${totalRamMb} MiB."
        if (availableStorage < (model.sizeBytes * 2L) + MIN_INSTALL_HEADROOM_BYTES) {
            reasons += "Insufficient private storage for download, installation and temporary files."
        }
        val runtimeAvailable = when (model.format to model.runtime) {
            "litertlm" to "litertlm" -> true
            "onnx" to "onnx-runtime-embeddings" -> model.capabilities == setOf(ModelCapability.EMBEDDING)
            else -> false
        }
        return ModelCompatibility(reasons.isEmpty(), reasons, totalRamMb, availableStorage, runtimeAvailable)
    }

    companion object {
        private const val MIN_INSTALL_HEADROOM_BYTES = 256L * 1024L * 1024L
    }
}

data class InstalledModelVersion(
    val modelId: String,
    val version: String,
    val file: File,
    val sha256: String,
    val sizeBytes: Long,
    val installedAt: Long,
    val active: Boolean
)

/**
 * Keeps immutable version directories and an atomic active-version pointer.
 * A new version never overwrites the active file; rollback only changes the pointer.
 */
class ModelInstallStore(context: Context) {
    private val root = File(context.applicationContext.filesDir, "model-registry").apply { mkdirs() }

    @Synchronized
    fun install(
        entry: ModelCatalogEntry,
        verifiedSource: File,
        ensureActive: () -> Unit = {}
    ): InstalledModelVersion {
        ensureActive()
        require(verifiedSource.isFile && verifiedSource.canRead()) { "Verified model source is missing or unreadable." }
        require(entry.id.matches(Regex("^[a-z0-9][a-z0-9._-]{1,79}$"))) { "Invalid model ID." }
        require(entry.version.matches(Regex("^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$"))) { "Invalid model version." }
        require(entry.fileName.matches(Regex("^[A-Za-z0-9._-]{1,120}$")) && entry.fileName.contains('.')) { "Invalid model filename." }
        require(entry.sha256.matches(Regex("^[A-Fa-f0-9]{64}$"))) { "Invalid model checksum." }
        require(verifiedSource.length() == entry.sizeBytes) { "Downloaded model size does not match the signed catalog." }
        val modelRoot = File(root, entry.id).apply { mkdirs() }
        val versionDir = File(modelRoot, entry.version)
        val target = File(versionDir, entry.fileName)
        if (versionDir.exists()) {
            val existingMetadata = File(versionDir, "install.json")
            require(existingMetadata.isFile && target.isFile) {
                "This model version already exists but is incomplete; remove the damaged version before reinstalling."
            }
            val record = JSONObject(existingMetadata.readText())
            require(record.optString("sha256").equals(entry.sha256, true) && sha256(target, ensureActive).equals(entry.sha256, true)) {
                "Model version ${entry.version} is immutable and already contains different bytes."
            }
            activate(entry, target, modelRoot)
            return InstalledModelVersion(entry.id, entry.version, target, entry.sha256.lowercase(), target.length(), record.optLong("installed_at"), true)
        }
        val staging = File(modelRoot, ".${entry.version}.installing")
        if (staging.exists()) staging.deleteRecursively()
        check(staging.mkdirs()) { "Could not create model staging directory." }
        try {
            val stagedFile = File(staging, entry.fileName)
            verifiedSource.inputStream().buffered().use { input ->
                stagedFile.outputStream().buffered().use { output ->
                    val buffer = ByteArray(64 * 1024)
                    while (true) {
                        ensureActive()
                        val count = input.read(buffer)
                        if (count < 0) break
                        output.write(buffer, 0, count)
                    }
                }
            }
            ensureActive()
            val actual = sha256(stagedFile, ensureActive)
            ensureActive()
            require(actual.equals(entry.sha256, true)) { "Model checksum mismatch during installation." }
            require(stagedFile.length() == entry.sizeBytes) { "Model size changed during installation." }
            val metadata = JSONObject()
                .put("model_id", entry.id).put("name", entry.name).put("publisher", entry.publisher)
                .put("version", entry.version).put("file_name", entry.fileName)
                .put("format", entry.format).put("runtime", entry.runtime)
                .put("capabilities", org.json.JSONArray(entry.capabilities.map { it.name.lowercase() }))
                .put("sha256", actual).put("size_bytes", stagedFile.length())
                .put("license", entry.license).put("license_url", entry.licenseUrl)
                .put("installed_at", System.currentTimeMillis())
            File(staging, "install.json").writeText(metadata.toString(2))
            ensureActive()
            check(staging.renameTo(versionDir)) { "Could not atomically publish the installed model version." }
            val installedFile = File(versionDir, entry.fileName)
            activate(entry, installedFile, modelRoot)
            return InstalledModelVersion(entry.id, entry.version, installedFile, actual, installedFile.length(), System.currentTimeMillis(), true)
        } catch (error: Throwable) {
            staging.deleteRecursively()
            throw error
        }
    }

    @Synchronized
    fun rollback(modelId: String): InstalledModelVersion {
        val modelRoot = safeModelRoot(modelId)
        val pointer = readPointer(modelRoot)
        val previous = pointer.optString("previous_version")
        require(previous.isNotBlank()) { "No previous model version is available for rollback." }
        val metadata = File(modelRoot, "$previous/install.json")
        require(metadata.isFile) { "Previous model version is missing." }
        val record = JSONObject(metadata.readText())
        val file = File(modelRoot, previous + "/" + record.getString("file_name"))
        require(file.isFile && sha256(file).equals(record.getString("sha256"), true)) {
            "Previous model version failed integrity verification."
        }
        val current = pointer.optString("active_version")
        writePointer(modelRoot, previous, current)
        return InstalledModelVersion(modelId, previous, file, record.getString("sha256"), file.length(), record.getLong("installed_at"), true)
    }

    fun list(modelId: String): List<InstalledModelVersion> {
        val modelRoot = safeModelRoot(modelId)
        if (!modelRoot.isDirectory) return emptyList()
        val pointer = readPointer(modelRoot)
        val active = pointer.optString("active_version")
        return modelRoot.listFiles()?.filter { it.isDirectory && !it.name.startsWith(".") }?.mapNotNull { dir ->
            runCatching {
                val record = JSONObject(File(dir, "install.json").readText())
                val file = File(dir, record.getString("file_name"))
                if (!file.isFile) return@runCatching null
                InstalledModelVersion(modelId, dir.name, file, record.getString("sha256"), file.length(),
                    record.optLong("installed_at"), dir.name == active)
            }.getOrNull()
        }?.sortedByDescending { it.installedAt }.orEmpty()
    }

    @Synchronized
    fun removeVersion(modelId: String, version: String) {
        val modelRoot = safeModelRoot(modelId)
        require(version.matches(Regex("^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$"))) { "Invalid model version." }
        val pointer = readPointer(modelRoot)
        require(pointer.optString("active_version") != version) { "Load another version or roll back before removing the active version." }
        File(modelRoot, version).deleteRecursively()
    }

    private fun activate(entry: ModelCatalogEntry, file: File, modelRoot: File) {
        val pointer = readPointer(modelRoot)
        val active = pointer.optString("active_version").takeIf { it.isNotBlank() }
        writePointer(modelRoot, entry.version, active?.takeIf { it != entry.version } ?: pointer.optString("previous_version"))
    }

    private fun readPointer(modelRoot: File): JSONObject {
        val file = File(modelRoot, "active.json")
        return if (file.isFile) JSONObject(file.readText()) else JSONObject()
    }

    private fun writePointer(modelRoot: File, active: String, previous: String?) {
        val temp = File(modelRoot, "active.json.tmp")
        temp.writeText(JSONObject().put("active_version", active).put("previous_version", previous ?: "").toString())
        val target = File(modelRoot, "active.json")
        Files.move(temp.toPath(), target.toPath(), StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING)
    }

    private fun safeModelRoot(modelId: String): File {
        require(modelId.matches(Regex("^[a-z0-9][a-z0-9._-]{1,79}$"))) { "Invalid model ID." }
        return File(root, modelId)
    }

    private fun sha256(file: File, ensureActive: () -> Unit = {}): String {
        val digest = MessageDigest.getInstance("SHA-256")
        file.inputStream().buffered().use { input ->
            val buffer = ByteArray(64 * 1024)
            while (true) {
                ensureActive()
                val count = input.read(buffer)
                if (count < 0) break
                digest.update(buffer, 0, count)
            }
        }
        return digest.digest().joinToString("") { "%02x".format(it) }
    }
}
