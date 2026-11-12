package org.molecularis.app.features
import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL
import java.net.URI
import javax.net.ssl.HttpsURLConnection

/** Fetches a bounded signed catalog. The trusted public key is build-time configuration. */
class ModelCatalogClient(context: Context, private val catalogUrl: String, private val trustedPublicKeyBase64: String) {
    suspend fun fetch(): VerifiedModelCatalog = withContext(Dispatchers.IO) {
        val catalogUri = URI(catalogUrl)
        require(
            catalogUri.scheme.equals("https", true) &&
                !catalogUri.host.isNullOrBlank() &&
                catalogUri.userInfo == null &&
                catalogUri.fragment == null
        ) { "Catalog URL must be a valid HTTPS URL without credentials or fragments." }
        require(trustedPublicKeyBase64.isNotBlank()) { "No trusted catalog publisher key is configured in this build." }
        var current = catalogUri.toURL()
        var redirects = 0
        while (true) {
            currentCoroutineContext().ensureActive()
            val connection = current.openConnection() as? HttpsURLConnection ?: error("Catalog connections must use HTTPS.")
            try {
                connection.connectTimeout = 15_000; connection.readTimeout = 20_000
                connection.instanceFollowRedirects = false; connection.setRequestProperty("Accept", "application/json"); connection.connect()
                if (connection.responseCode in 300..399) {
                    require(redirects++ < 2) { "Too many catalog redirects." }
                    val next = URL(current, connection.getHeaderField("Location") ?: error("Missing redirect location"))
                    val nextUri = URI(next.toString())
                    require(
                        nextUri.scheme.equals("https", true) &&
                            !nextUri.host.isNullOrBlank() &&
                            nextUri.userInfo == null &&
                            nextUri.fragment == null
                    ) { "Catalog redirects must remain valid HTTPS URLs without credentials or fragments." }
                    current = next
                    continue
                }
                require(connection.responseCode == HttpURLConnection.HTTP_OK) { "Catalog request failed: HTTP ${connection.responseCode}" }
                val bytes = connection.inputStream.use { input ->
                    val output = java.io.ByteArrayOutputStream(); val buffer = ByteArray(8192); var total = 0
                    while (true) {
                        currentCoroutineContext().ensureActive()
                        val count = input.read(buffer)
                        if (count < 0) break
                        total += count
                        require(total <= 2 * 1024 * 1024) { "Catalog exceeds 2 MiB." }
                        output.write(buffer, 0, count)
                    }
                    output.toByteArray()
                }
                return@withContext ModelCatalogParser.parseSigned(bytes, Ed25519CatalogVerifier(trustedPublicKeyBase64))
            } finally { connection.disconnect() }
        }
        error("Unreachable catalog state")
    }
}
