package org.molecularis.app.features

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.io.File
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL
import java.net.URLEncoder
import java.security.MessageDigest
import java.util.Locale
import java.util.UUID

data class CommonsImageResult(
    val title: String,
    val thumbnailUrl: String,
    val originalUrl: String,
    val sourcePageUrl: String,
    val licenseName: String,
    val licenseUrl: String,
    val attribution: String
)

data class CachedCommonsImage(
    val imagePath: String,
    val metadataPath: String,
    val sha256: String,
    val title: String,
    val licenseName: String,
    val licenseUrl: String,
    val sourcePageUrl: String,
    val attribution: String
)

/** Searches Wikimedia Commons and keeps the license and attribution fields with every result. */
class CommonsImageSearchClient(
    private val connectTimeoutMs: Int = 12_000,
    private val readTimeoutMs: Int = 20_000
) {
    suspend fun search(query: String, limit: Int = 8): List<CommonsImageResult> = withContext(Dispatchers.IO) {
        val clean = query.trim()
        require(clean.length in 2..120) { "Enter an image-search phrase between 2 and 120 characters." }
        require(limit in 1..20) { "Image search limit must be between 1 and 20." }
        val encoded = URLEncoder.encode("filetype:bitmap $clean", Charsets.UTF_8.name())
        val endpoint = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=$encoded&gsrnamespace=6&gsrlimit=$limit&prop=imageinfo&iiprop=url%7Cextmetadata&iiurlwidth=900&format=json&formatversion=2"
        val connection = URL(endpoint).openConnection() as HttpURLConnection
        try {
            connection.requestMethod = "GET"
            connection.instanceFollowRedirects = false
            connection.connectTimeout = connectTimeoutMs
            connection.readTimeout = readTimeoutMs
            connection.setRequestProperty("Accept", "application/json")
            connection.setRequestProperty("User-Agent", "Molecularis/0.1 (educational biochemistry teaching app)")
            val status = connection.responseCode
            require(status in 200..299) { "Wikimedia Commons search returned HTTP $status." }
            val response = connection.inputStream.use { readBounded(it, MAX_JSON_BYTES).toString(Charsets.UTF_8) }
            parseResponse(response)
        } finally {
            connection.disconnect()
        }
    }

    companion object {
        private const val MAX_JSON_BYTES = 1_500_000

        internal fun parseResponse(jsonText: String): List<CommonsImageResult> {
            val root = JSONObject(jsonText)
            val pages = root.optJSONObject("query")?.optJSONArray("pages") ?: JSONArray()
            return buildList {
                for (index in 0 until pages.length()) {
                    val page = pages.optJSONObject(index) ?: continue
                    val title = page.optString("title").trim()
                    val info = page.optJSONArray("imageinfo")?.optJSONObject(0) ?: continue
                    val thumbnail = info.optString("thumburl")
                    val original = info.optString("url")
                    if (title.isBlank() || !isAllowedImageUrl(thumbnail) || !isAllowedImageUrl(original)) continue
                    val metadata = info.optJSONObject("extmetadata") ?: continue
                    val license = plainText(metadata.optJSONObject("LicenseShortName")?.optString("value").orEmpty())
                    val licenseUrl = metadata.optJSONObject("LicenseUrl")?.optString("value").orEmpty().trim()
                    val artist = plainText(metadata.optJSONObject("Attribution")?.optString("value")
                        ?.takeIf { it.isNotBlank() } ?: metadata.optJSONObject("Artist")?.optString("value").orEmpty())
                    if (license.isBlank() || license.equals("unknown", true) || license.equals("no license", true)) continue
                    val encodedTitle = URLEncoder.encode(title.replace(' ', '_'), Charsets.UTF_8.name()).replace("+", "%20")
                    add(CommonsImageResult(
                        title = title.take(240),
                        thumbnailUrl = thumbnail,
                        originalUrl = original,
                        sourcePageUrl = "https://commons.wikimedia.org/wiki/$encodedTitle",
                        licenseName = license.take(120),
                        licenseUrl = licenseUrl.takeIf { value -> value.isBlank() || runCatching { URI(value).let { it.scheme.equals("https", true) && !it.host.isNullOrBlank() && it.userInfo == null } }.getOrDefault(false) }.orEmpty().take(500),
                        attribution = artist.take(500)
                    ))
                }
            }
        }

        private fun isAllowedImageUrl(value: String): Boolean = runCatching {
            val uri = URI(value)
            uri.scheme.equals("https", true) && uri.host.equals("upload.wikimedia.org", true) &&
                uri.userInfo == null && uri.port in listOf(-1, 443) && uri.query == null && uri.fragment == null
        }.getOrDefault(false)

        private fun plainText(value: String): String = value
            .replace(Regex("<[^>]*>"), " ")
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&quot;", "\"")
            .replace("&#39;", "'")
            .replace(Regex("\\s+"), " ")
            .trim()

        internal fun readBounded(input: java.io.InputStream, maximumBytes: Int): ByteArray {
            val output = ByteArrayOutputStream()
            val buffer = ByteArray(16 * 1024)
            var total = 0
            while (true) {
                val count = input.read(buffer)
                if (count < 0) break
                total += count
                require(total <= maximumBytes) { "Image or search response exceeded its size limit." }
                output.write(buffer, 0, count)
            }
            return output.toByteArray()
        }
    }
}

/** Caches only raster thumbnails from Wikimedia's upload host and writes a license sidecar. */
class CommonsImageCache(context: Context, private val maximumImageBytes: Int = 8 * 1024 * 1024) {
    private val directory = File(context.applicationContext.filesDir, "diagram-images")

    private fun matchesRasterSignature(bytes: ByteArray, mime: String): Boolean = when (mime) {
        "image/jpeg" -> bytes.size >= 3 && bytes[0] == 0xFF.toByte() && bytes[1] == 0xD8.toByte() && bytes[2] == 0xFF.toByte()
        "image/png" -> bytes.size >= 8 && bytes.take(8).map { it.toInt() and 0xFF } == listOf(137, 80, 78, 71, 13, 10, 26, 10)
        "image/webp" -> bytes.size >= 12 && bytes.copyOfRange(0, 4).toString(Charsets.US_ASCII) == "RIFF" && bytes.copyOfRange(8, 12).toString(Charsets.US_ASCII) == "WEBP"
        else -> false
    }
    suspend fun cache(result: CommonsImageResult): CachedCommonsImage = withContext(Dispatchers.IO) {
        require(result.licenseName.isNotBlank()) { "An explicit license is required before caching an image." }
        require(result.sourcePageUrl.startsWith("https://commons.wikimedia.org/wiki/")) { "Image source page is not a Wikimedia Commons page." }
        val uri = URI(result.thumbnailUrl)
        require(uri.scheme.equals("https", true) && uri.host.equals("upload.wikimedia.org", true) && uri.userInfo == null) {
            "Only Wikimedia Commons raster thumbnails can be cached."
        }
        directory.mkdirs()
        val connection = URL(result.thumbnailUrl).openConnection() as HttpURLConnection
        try {
            connection.requestMethod = "GET"
            connection.instanceFollowRedirects = false
            connection.connectTimeout = 12_000
            connection.readTimeout = 25_000
            connection.setRequestProperty("User-Agent", "Molecularis/0.1 (educational biochemistry teaching app)")
            val status = connection.responseCode
            require(status in 200..299) { "Image download returned HTTP $status." }
            val mime = connection.contentType.orEmpty().substringBefore(';').lowercase(Locale.ROOT)
            val extension = when (mime) {
                "image/jpeg" -> "jpg"
                "image/png" -> "png"
                "image/webp" -> "webp"
                else -> error("Only JPEG, PNG and WebP reference images can be cached.")
            }
            val declared = connection.contentLengthLong
            require(declared <= maximumImageBytes || declared < 0) { "Reference image exceeds the 8 MiB cache limit." }
            val bytes = connection.inputStream.use { CommonsImageSearchClient.readBounded(it, maximumImageBytes) }
            require(bytes.isNotEmpty()) { "The image download was empty." }
            require(matchesRasterSignature(bytes, mime)) { "The downloaded file does not match its declared raster image type." }
            val id = UUID.randomUUID().toString()
            val image = File(directory, "$id.$extension")
            val sidecar = File(directory, "$id.json")
            val tempImage = File(directory, "$id.$extension.tmp")
            val tempSidecar = File(directory, "$id.json.tmp")
            try {
                tempImage.writeBytes(bytes)
                val digest = MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it) }
                val metadata = JSONObject()
                    .put("title", result.title)
                    .put("sourcePageUrl", result.sourcePageUrl)
                    .put("licenseName", result.licenseName)
                    .put("licenseUrl", result.licenseUrl)
                    .put("attribution", result.attribution)
                    .put("sha256", digest)
                    .put("cachedAtEpochMs", System.currentTimeMillis())
                tempSidecar.writeText(metadata.toString(), Charsets.UTF_8)
                check(tempImage.renameTo(image)) { "Could not finalize cached image." }
                check(tempSidecar.renameTo(sidecar)) { "Could not save image license metadata." }
                CachedCommonsImage(image.absolutePath, sidecar.absolutePath, digest, result.title, result.licenseName, result.licenseUrl, result.sourcePageUrl, result.attribution)
            } catch (error: Throwable) {
                tempImage.delete(); tempSidecar.delete(); image.delete(); sidecar.delete()
                throw error
            }
        } finally {
            connection.disconnect()
        }
    }
}
