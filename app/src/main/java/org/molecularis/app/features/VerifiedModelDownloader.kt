package org.molecularis.app.features

import android.content.Context
import android.os.StatFs
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.net.URI
import java.security.MessageDigest
import javax.net.ssl.HttpsURLConnection

data class DownloadedModel(val file: File, val sha256: String, val bytes: Long)

/** HTTPS downloader with persistent Range resume. Partial bytes are never exposed to inference. */
class VerifiedModelDownloader(context: Context) {
    private val modelDirectory = File(context.applicationContext.filesDir, "models").apply { mkdirs() }

    suspend fun download(
        sourceUrl: String,
        expectedSha256: String,
        requestedFileName: String,
        onProgress: (downloadedBytes: Long, totalBytes: Long?) -> Unit = { _, _ -> }
    ): DownloadedModel = withContext(Dispatchers.IO) {
        require(expectedSha256.matches(Regex("[A-Fa-f0-9]{64}"))) { "Enter a valid 64-character SHA-256 checksum." }
        val safeName = requestedFileName.substringAfterLast('/').substringAfterLast('\\').replace(Regex("[^A-Za-z0-9._-]"), "_")
        val allowedExtensions = setOf(".litertlm", ".gguf", ".onnx", ".tflite", ".safetensors", ".zip", ".bin", ".ggml")
        require(safeName.isNotBlank() && allowedExtensions.any { safeName.endsWith(it, true) }) {
            "Unsupported model artifact extension. Supported: " + allowedExtensions.joinToString()
        }
        val sourceUri = URI(sourceUrl)
        require(
            sourceUri.scheme.equals("https", true) &&
                !sourceUri.host.isNullOrBlank() &&
                sourceUri.userInfo == null &&
                sourceUri.fragment == null
        ) { "Model downloads require a valid HTTPS URL without embedded credentials or fragments." }
        var currentUrl = sourceUri.toURL()
        val digestKey = expectedSha256.lowercase()
        val partial = File(modelDirectory, ".$digestKey.part")
        val target = File(modelDirectory, digestKey.take(16) + "-" + safeName)
        if (target.isFile && target.length() <= MAX_BYTES && sha256(target).equals(digestKey, true)) return@withContext DownloadedModel(target, digestKey, target.length())
        if (partial.length() > MAX_BYTES) partial.delete()
        var offset = partial.length()
        var redirects = 0
        var restartedAfter416 = false
        var connection: HttpsURLConnection? = null
        try {
            while (true) {
                currentCoroutineContext().ensureActive()
                val candidate = currentUrl.openConnection() as? HttpsURLConnection ?: error("Only HTTPS model download endpoints are allowed.")
                connection = candidate
                candidate.connectTimeout = 20_000
                candidate.readTimeout = 45_000
                candidate.instanceFollowRedirects = false
                candidate.setRequestProperty("User-Agent", "Astronaut-Offline-AI/0.1.0")
                candidate.setRequestProperty("Accept-Encoding", "identity")
                if (offset > 0) candidate.setRequestProperty("Range", "bytes=$offset-")
                candidate.connect()
                val status = candidate.responseCode
                if (status in 300..399) {
                    val location = candidate.getHeaderField("Location") ?: error("Redirect has no destination.")
                    require(redirects++ < 3) { "Too many model download redirects." }
                    val redirected = URL(currentUrl, location)
                    val redirectedUri = URI(redirected.toString())
                    require(
                        redirectedUri.scheme.equals("https", true) &&
                            !redirectedUri.host.isNullOrBlank() &&
                            redirectedUri.userInfo == null &&
                            redirectedUri.fragment == null
                    ) { "Redirects must remain on valid HTTPS URLs without embedded credentials or fragments." }
                    candidate.disconnect(); connection = null; currentUrl = redirected
                    continue
                }
                if (status == 416 && offset > 0 && !restartedAfter416) {
                    candidate.disconnect(); connection = null; partial.delete(); offset = 0; restartedAfter416 = true
                    continue
                }
                val append = if (offset > 0 && status == HttpURLConnection.HTTP_PARTIAL) {
                    val contentRange = candidate.getHeaderField("Content-Range") ?: error("Server omitted Content-Range for resumed download.")
                    require(contentRange.startsWith("bytes $offset-", true)) { "Server resumed at an unexpected byte offset." }
                    true
                } else {
                    require(status == HttpURLConnection.HTTP_OK) { "Download failed with HTTP status $status." }
                    offset = 0
                    false
                }
                val remaining = candidate.contentLengthLong.takeIf { it >= 0 }
                val total = remaining?.let { offset + it }?.takeIf { it > 0 }
                if (total != null) {
                    require(total <= MAX_BYTES) { "Model exceeds the 15 GB download limit." }
                    val requiredSpace = (total - offset).coerceAtLeast(0L) + MIN_FREE_SPACE_BYTES
                    require(StatFs(modelDirectory.absolutePath).availableBytes >= requiredSpace) {
                        "Not enough free storage. Keep at least 512 MiB free beyond the model download."
                    }
                }
                var downloaded = offset
                candidate.inputStream.use { input ->
                    val output = (if (append) FileOutputStream(partial, true) else partial.outputStream()).buffered()
                    output.use { sink ->
                        val buffer = ByteArray(64 * 1024)
                        while (true) {
                            currentCoroutineContext().ensureActive()
                            val count = input.read(buffer)
                            if (count < 0) break
                            downloaded += count
                            require(downloaded <= MAX_BYTES) { "Model exceeds the 15 GB download limit." }
                            sink.write(buffer, 0, count)
                            if (downloaded % PROGRESS_INTERVAL < count) {
                                val progress = downloaded
                                withContext(Dispatchers.Main) { onProgress(progress, total) }
                            }
                        }
                    }
                }
                require(total == null || downloaded == total) { "Download ended early; partial bytes were retained for resume." }
                currentCoroutineContext().ensureActive()
                val actual = sha256(partial)
                currentCoroutineContext().ensureActive()
                if (!actual.equals(digestKey, true)) {
                    partial.delete()
                    error("SHA-256 mismatch. Expected $digestKey but received $actual. Partial bytes were discarded.")
                }
                currentCoroutineContext().ensureActive()
                check(partial.renameTo(target)) { "Could not publish verified model into private storage." }
                withContext(Dispatchers.Main) { onProgress(downloaded, total ?: downloaded) }
                return@withContext DownloadedModel(target, actual, downloaded)
            }
            error("Unreachable download state")
        } finally { connection?.disconnect() }
    }

    private fun sha256(file: File): String {
        val digest = MessageDigest.getInstance("SHA-256")
        file.inputStream().buffered().use { input ->
            val buffer = ByteArray(64 * 1024)
            while (true) { val count = input.read(buffer); if (count < 0) break; digest.update(buffer, 0, count) }
        }
        return digest.digest().joinToString("") { "%02x".format(it) }
    }

    companion object {
        private const val MAX_BYTES = 15_000_000_000L
        private const val MIN_FREE_SPACE_BYTES = 512L * 1024L * 1024L
        private const val PROGRESS_INTERVAL = 512L * 1024L
    }
}
