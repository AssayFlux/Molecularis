package org.molecularis.app.features

import org.junit.Assert.assertFalse
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.Base64
import java.security.KeyPairGenerator
import java.security.Signature

class ModelCatalogTest {
    private fun modelJson(
        id: String = "astronaut-chat-small",
        sha: String = "a".repeat(64),
        url: String = "https://models.example.org/chat.litertlm"
    ) = """
        {
          "id":"$id","name":"Astronaut Chat Small","publisher":"Example Publisher",
          "version":"1.0.0","description":"Test model","license":"Apache-2.0",
          "license_url":"https://models.example.org/license",
          "download_url":"$url","sha256":"$sha","file_name":"chat-small.litertlm",
          "format":"litertlm","runtime":"litertlm","min_sdk":26,"min_ram_mb":2048,
          "size_bytes":1048576,"capabilities":["chat","code"],
          "architecture":"transformer","quantization":"int4"
        }
    """.trimIndent()

    private fun payload(vararg models: String) = """
        {"schema_version":1,"generated_at":"2026-11-05T00:00:00Z","models":[${models.joinToString(",")}]}
    """.trimIndent().toByteArray()

    @Test fun parsesModelMetadataAndCapabilities() {
        val catalog = ModelCatalogParser.parseVerifiedPayload(payload(modelJson()))
        val model = catalog.models.single()
        assertEquals("astronaut-chat-small", model.id)
        assertEquals(setOf(ModelCapability.CHAT, ModelCapability.CODE), model.capabilities)
        assertEquals(1048576L, model.sizeBytes)
    }


    @Test fun acceptsGgufCatalogEntriesAndArtifactsLargerThanEightGiB() {
        val gguf = modelJson()
            .replace("chat-small.litertlm", "chat-small.gguf")
            .replace("\"format\":\"litertlm\",\"runtime\":\"litertlm\"", "\"format\":\"gguf\",\"runtime\":\"llama.cpp\"")
            .replace("\"size_bytes\":1048576", "\"size_bytes\":9000000000")
        val model = ModelCatalogParser.parseVerifiedPayload(payload(gguf)).models.single()
        assertEquals("gguf", model.format)
        assertEquals("llama.cpp", model.runtime)
        assertEquals(9_000_000_000L, model.sizeBytes)
    }

    @Test fun acceptsOnnxEmbeddingFormatWithMatchingRuntimeId() {
        val onnx = modelJson()
            .replace("chat-small.litertlm", "sentence-embedder.onnx")
            .replace("\"format\":\"litertlm\",\"runtime\":\"litertlm\"", "\"format\":\"onnx\",\"runtime\":\"onnx-runtime-embeddings\"")
            .replace("\"capabilities\":[\"chat\",\"code\"]", "\"capabilities\":[\"embedding\"]")
        val model = ModelCatalogParser.parseVerifiedPayload(payload(onnx)).models.single()
        assertEquals("onnx", model.format)
        assertEquals("onnx-runtime-embeddings", model.runtime)
        assertEquals(setOf(ModelCapability.EMBEDDING), model.capabilities)
    }

    @Test fun rejectsArtifactsAboveFifteenGb() {
        val oversized = modelJson().replace("\"size_bytes\":1048576", "\"size_bytes\":15000000001")
        val error = runCatching { ModelCatalogParser.parseVerifiedPayload(payload(oversized)) }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsNonHttpsDownload() {
        val error = runCatching {
            ModelCatalogParser.parseVerifiedPayload(payload(modelJson(url="http://models.example.org/model.litertlm")))
        }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsInvalidChecksum() {
        val error = runCatching {
            ModelCatalogParser.parseVerifiedPayload(payload(modelJson(sha="not-a-checksum")))
        }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsDuplicateModelIds() {
        val error = runCatching {
            ModelCatalogParser.parseVerifiedPayload(payload(modelJson(), modelJson()))
        }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsFilenameTraversalAndMismatchedExtensions() {
        val traversal = modelJson().replace("chat-small.litertlm", "../chat-small.litertlm")
        val mismatch = modelJson().replace("chat-small.litertlm", "chat-small.gguf")
        assertTrue(runCatching { ModelCatalogParser.parseVerifiedPayload(payload(traversal)) }.exceptionOrNull() is IllegalArgumentException)
        assertTrue(runCatching { ModelCatalogParser.parseVerifiedPayload(payload(mismatch)) }.exceptionOrNull() is IllegalArgumentException)
    }

    @Test fun rejectsRuntimeFormatMismatch() {
        val invalid = modelJson().replace(""""runtime":"litertlm"""", """"runtime":"llama.cpp"""")
        val error = runCatching { ModelCatalogParser.parseVerifiedPayload(payload(invalid)) }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsCredentialBearingDownloadUrls() {
        val invalid = modelJson(url="https://user:password@models.example.org/chat.litertlm")
        val error = runCatching { ModelCatalogParser.parseVerifiedPayload(payload(invalid)) }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test fun rejectsUnknownCapabilitiesAndInvalidDeviceRequirements() {
        val invalidCapability = modelJson().replace(""""chat","code"""", """"telepathy"""")
        val invalidRam = modelJson().replace("2048", "128")
        assertTrue(runCatching { ModelCatalogParser.parseVerifiedPayload(payload(invalidCapability)) }.isFailure)
        assertTrue(runCatching { ModelCatalogParser.parseVerifiedPayload(payload(invalidRam)) }.exceptionOrNull() is IllegalArgumentException)
    }

    @Test fun signedEnvelopeRequiresVerifierApproval() {
        val raw = payload(modelJson())
        val envelope = """{"payload":"${Base64.getEncoder().encodeToString(raw)}","signature":"AQ=="}""".toByteArray()
        val rejected = runCatching {
            ModelCatalogParser.parseSigned(envelope, CatalogSignatureVerifier { _, _ -> false })
        }.exceptionOrNull()
        assertTrue(rejected is IllegalArgumentException)
        val accepted = ModelCatalogParser.parseSigned(envelope, CatalogSignatureVerifier { bytes, signature ->
            bytes.contentEquals(raw) && signature.contentEquals(byteArrayOf(1))
        })
        assertEquals(1, accepted.models.size)
    }
}

class Ed25519CatalogVerifierTest {
    @Test
    fun ed25519VerifierAcceptsAuthenticSignatureAndRejectsTampering() {
        val pair = KeyPairGenerator.getInstance("Ed25519").generateKeyPair()
        val payload = """{"schema_version":1,"models":[]}""".toByteArray()
        val signer = Signature.getInstance("Ed25519")
        signer.initSign(pair.private)
        signer.update(payload)
        val signature = signer.sign()
        val publicKey = Base64.getEncoder().encodeToString(pair.public.encoded)
        val verifier = Ed25519CatalogVerifier(publicKey)
        assertTrue(verifier.verify(payload, signature))
        assertFalse(verifier.verify(payload + byteArrayOf(0), signature))
    }
}
