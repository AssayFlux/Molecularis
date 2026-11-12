package org.molecularis.app.features

import org.json.JSONArray
import org.json.JSONObject
import java.net.URI
import net.i2p.crypto.eddsa.EdDSAEngine
import net.i2p.crypto.eddsa.EdDSAPublicKey
import net.i2p.crypto.eddsa.spec.EdDSANamedCurveTable
import net.i2p.crypto.eddsa.spec.EdDSAPublicKeySpec
import java.security.MessageDigest
import java.util.Base64

enum class ModelCapability { CHAT, CODE, VISION, AUDIO_TRANSCRIPTION, SPEECH_SYNTHESIS, EMBEDDING, RERANKING, CLASSIFICATION, IMAGE_GENERATION }

data class ModelCatalogEntry(
    val id: String,
    val name: String,
    val publisher: String,
    val version: String,
    val description: String,
    val license: String,
    val licenseUrl: String,
    val downloadUrl: String,
    val sha256: String,
    val fileName: String,
    val format: String,
    val runtime: String,
    val minSdk: Int,
    val minRamMb: Int,
    val sizeBytes: Long,
    val capabilities: Set<ModelCapability>,
    val architecture: String,
    val quantization: String
)

data class VerifiedModelCatalog(
    val schemaVersion: Int,
    val generatedAt: String,
    val models: List<ModelCatalogEntry>,
    val payloadSha256: String
)

/** A catalog is trusted only after its exact payload bytes pass a publisher-key signature check. */
fun interface CatalogSignatureVerifier {
    fun verify(payload: ByteArray, signature: ByteArray): Boolean
}

class Ed25519CatalogVerifier(x509PublicKeyBase64: String) : CatalogSignatureVerifier {
    private val publicKey: EdDSAPublicKey

    init {
        val encoded = Base64.getDecoder().decode(x509PublicKeyBase64)
        val prefix = byteArrayOf(0x30, 0x2a, 0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70, 0x03, 0x21, 0x00)
        require(encoded.size == 44 && encoded.copyOfRange(0, prefix.size).contentEquals(prefix)) {
            "Catalog publisher key must be an X.509 Ed25519 public key."
        }
        val rawKey = encoded.copyOfRange(prefix.size, encoded.size)
        val curve = EdDSANamedCurveTable.getByName("Ed25519")
            ?: error("Ed25519 curve implementation is unavailable.")
        publicKey = EdDSAPublicKey(EdDSAPublicKeySpec(rawKey, curve))
    }

    override fun verify(payload: ByteArray, signature: ByteArray): Boolean = runCatching {
        val verifier = EdDSAEngine(MessageDigest.getInstance("SHA-512"))
        verifier.initVerify(publicKey)
        verifier.update(payload)
        verifier.verify(signature)
    }.getOrDefault(false)
}

object ModelCatalogParser {
    private val idPattern = Regex("^[a-z0-9][a-z0-9._-]{1,79}$")
    private val shaPattern = Regex("^[A-Fa-f0-9]{64}$")

    fun parseSigned(envelopeBytes: ByteArray, verifier: CatalogSignatureVerifier): VerifiedModelCatalog {
        require(envelopeBytes.size in 1..(2 * 1024 * 1024)) { "Catalog envelope must be between 1 byte and 2 MiB." }
        val envelope = JSONObject(envelopeBytes.toString(Charsets.UTF_8))
        val payload = Base64.getDecoder().decode(envelope.getString("payload"))
        val signature = Base64.getDecoder().decode(envelope.getString("signature"))
        require(payload.size in 1..(1024 * 1024)) { "Catalog payload exceeds 1 MiB." }
        require(verifier.verify(payload, signature)) { "Catalog signature is invalid. No catalog entries were trusted." }
        return parseVerifiedPayload(payload)
    }

    internal fun parseVerifiedPayload(payload: ByteArray): VerifiedModelCatalog {
        val json = JSONObject(payload.toString(Charsets.UTF_8))
        require(json.getInt("schema_version") == 1) { "Unsupported model catalog schema." }
        val modelsJson = json.getJSONArray("models")
        require(modelsJson.length() <= 500) { "Catalog contains too many models." }
        val models = (0 until modelsJson.length()).map { parseEntry(modelsJson.getJSONObject(it)) }
        require(models.map { it.id }.distinct().size == models.size) { "Catalog contains duplicate model IDs." }
        return VerifiedModelCatalog(
            schemaVersion = 1,
            generatedAt = json.getString("generated_at"),
            models = models,
            payloadSha256 = java.security.MessageDigest.getInstance("SHA-256")
                .digest(payload).joinToString("") { "%02x".format(it) }
        )
    }

    private fun parseEntry(json: JSONObject): ModelCatalogEntry {
        val id = json.getString("id")
        require(idPattern.matches(id)) { "Invalid model ID: $id" }
        val name = json.getString("name").trim()
        val publisher = json.getString("publisher").trim()
        val version = json.getString("version")
        require(name.isNotEmpty() && name.length <= 160) { "Model $id has an invalid display name." }
        require(publisher.isNotEmpty() && publisher.length <= 120) { "Model $id has an invalid publisher name." }
        require(version.matches(Regex("^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$"))) {
            "Model $id has an invalid version."
        }

        val sha = json.getString("sha256")
        require(shaPattern.matches(sha)) { "Model $id has an invalid SHA-256 checksum." }
        val download = json.getString("download_url")
        val licenseUrl = json.getString("license_url")
        require(isHttps(download) && isHttps(licenseUrl)) {
            "Model $id must use HTTPS for downloads and license links."
        }

        val fileName = json.getString("file_name")
        require(fileName.matches(Regex("^[A-Za-z0-9._-]{1,120}$")) && fileName.contains('.')) {
            "Model $id must reference a safe filename with an extension."
        }
        val format = json.getString("format").lowercase()
        val runtime = json.getString("runtime").lowercase()
        val allowed = mapOf(
            "litertlm" to ("litertlm" to setOf(".litertlm")),
            "gguf" to ("llama.cpp" to setOf(".gguf")),
            "onnx" to ("onnx-runtime-embeddings" to setOf(".onnx")),
            "tflite" to ("litert" to setOf(".tflite")),
            "diffusion_bundle" to ("mnn-diffusion" to setOf(".zip", ".safetensors")),
            "whisper_model" to ("whisper.cpp" to setOf(".bin", ".ggml", ".gguf")),
            "sherpa_onnx" to ("sherpa-onnx" to setOf(".onnx", ".zip"))
        )
        val spec = allowed[format] ?: error("Unsupported artifact format for $id: $format")
        require(runtime == spec.first) {
            "Format $format requires runtime ${spec.first}, not $runtime."
        }
        require(spec.second.any { fileName.endsWith(it, ignoreCase = true) }) {
            "Filename extension does not match declared format $format."
        }

        val size = json.getLong("size_bytes")
        require(size in 1..15_000_000_000L) { "Model $id exceeds the 15 GB integration limit." }
        val minSdk = json.getInt("min_sdk")
        val minRam = json.getInt("min_ram_mb")
        require(minSdk in 26..100 && minRam in 256..262144) {
            "Invalid device requirements for $id."
        }

        val capabilitiesJson = json.getJSONArray("capabilities")
        require(capabilitiesJson.length() in 1..ModelCapability.entries.size) {
            "Model $id must declare a bounded non-empty capability list."
        }
        val capabilityValues = (0 until capabilitiesJson.length()).map {
            ModelCapability.valueOf(capabilitiesJson.getString(it).uppercase())
        }
        require(capabilityValues.distinct().size == capabilityValues.size) {
            "Model $id contains duplicate capabilities."
        }
        val capabilities = capabilityValues.toSet()

        val architecture = json.getString("architecture").trim()
        val quantization = json.getString("quantization").trim()
        require(architecture.isNotEmpty() && architecture.length <= 80) {
            "Model $id has an invalid architecture."
        }
        require(quantization.isNotEmpty() && quantization.length <= 40) {
            "Model $id has an invalid quantization."
        }

        return ModelCatalogEntry(
            id = id,
            name = name,
            publisher = publisher,
            version = version,
            description = json.optString("description").take(2000),
            license = json.getString("license"),
            licenseUrl = licenseUrl,
            downloadUrl = download,
            sha256 = sha,
            fileName = fileName,
            format = format,
            runtime = runtime,
            minSdk = minSdk,
            minRamMb = minRam,
            sizeBytes = size,
            capabilities = capabilities,
            architecture = architecture,
            quantization = quantization
        )
    }

    private fun isHttps(value: String): Boolean = runCatching {
        val uri = URI(value)
        uri.scheme.equals("https", true) && !uri.host.isNullOrBlank() && uri.userInfo == null
    }.getOrDefault(false)
}
