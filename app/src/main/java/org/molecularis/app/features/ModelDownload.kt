package org.molecularis.app.features

import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Environment
import java.io.File
import java.security.MessageDigest

data class ModelDownloadSpec(
    val id: String,
    val displayName: String,
    val url: String,
    val expectedSha256: String,
    val licenseUrl: String,
    val licenseAccepted: Boolean
)

/** Uses Android DownloadManager; callers must obtain explicit license acceptance before enqueueing. */
class ModelDownloadManager(private val context: Context) {
    private val manager = context.getSystemService(DownloadManager::class.java)

    fun enqueue(spec: ModelDownloadSpec): Long {
        require(spec.licenseAccepted) { "Accept and review the model license before downloading." }
        require(spec.url.startsWith("https://")) { "Only HTTPS model downloads are permitted." }
        require(spec.expectedSha256.matches(Regex("[a-fA-F0-9]{64}"))) { "A valid SHA-256 checksum is required." }
        require(spec.licenseUrl.startsWith("https://")) { "A valid HTTPS license URL is required." }
        val safe = spec.displayName.replace(Regex("[^A-Za-z0-9._-]"), "_")
        val request = DownloadManager.Request(Uri.parse(spec.url))
            .setTitle(spec.displayName)
            .setDescription("Downloading model · verify checksum before import")
            .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
            .setAllowedOverMetered(true)
            .setAllowedOverRoaming(false)
            .setDestinationInExternalFilesDir(context, Environment.DIRECTORY_DOWNLOADS, "astronaut-${spec.id}-$safe")
        return manager.enqueue(request)
    }

    fun completedFile(downloadId: Long): File? {
        val query = DownloadManager.Query().setFilterById(downloadId)
        manager.query(query)?.use { cursor ->
            if (!cursor.moveToFirst() || cursor.getInt(cursor.getColumnIndexOrThrow(DownloadManager.COLUMN_STATUS)) != DownloadManager.STATUS_SUCCESSFUL) return null
            val uri = Uri.parse(cursor.getString(cursor.getColumnIndexOrThrow(DownloadManager.COLUMN_LOCAL_URI)))
            return if (uri.scheme == "file") File(uri.path!!) else null
        }
        return null
    }

    fun verifySha256(file: File, expected: String): Boolean {
        require(expected.matches(Regex("[a-fA-F0-9]{64}")))
        val digest = MessageDigest.getInstance("SHA-256")
        file.inputStream().buffered().use { input ->
            val buffer = ByteArray(1024 * 1024)
            while (true) { val count = input.read(buffer); if (count < 0) break; digest.update(buffer, 0, count) }
        }
        return digest.digest().joinToString("") { "%02x".format(it) }.equals(expected, ignoreCase = true)
    }
}
