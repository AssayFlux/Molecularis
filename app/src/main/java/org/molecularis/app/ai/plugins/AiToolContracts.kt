package org.molecularis.app.ai.plugins

import java.io.File

/**
 * Stable extension contract for adding AI engines without coupling the app UI to a
 * particular model format. Runtime implementations are shipped as trusted app code
 * (or separately signed Android feature modules), never loaded from a model file.
 */
enum class AiTask {
    CHAT, CODE, VISION, IMAGE_GENERATION, AUDIO_TRANSCRIPTION,
    SPEECH_SYNTHESIS, EMBEDDINGS, RERANKING, CLASSIFICATION
}

enum class ModelArtifactFormat {
    LITERT_LM, GGUF, ONNX, TFLITE, SAFETENSORS, DIFFUSION_BUNDLE,
    WHISPER_MODEL, SHERPA_ONNX, OPENAI_COMPATIBLE_ENDPOINT, OTHER
}

enum class ExecutionMode { ON_DEVICE, REMOTE }

data class AiModelManifest(
    val id: String,
    val displayName: String,
    val artifactFormat: ModelArtifactFormat,
    val runtimeId: String,
    val tasks: Set<AiTask>,
    val executionMode: ExecutionMode,
    val artifactBytes: Long,
    val sha256: String? = null,
    val minimumAndroidApi: Int = 26,
    /** Estimated peak process memory, including weights, KV cache and runtime. */
    val estimatedPeakRamBytes: Long? = null,
    val contextLength: Int? = null,
    val quantization: String? = null,
    val license: String? = null,
    val source: String? = null
)

data class AiRuntimeEnvironment(
    val androidApi: Int,
    val availableMemoryBytes: Long,
    val maximumArtifactBytes: Long = 15_000_000_000L
)

sealed class ModelCompatibility {
    data object Compatible : ModelCompatibility()
    data class Rejected(val reasons: List<String>) : ModelCompatibility()
}

object AiModelCompatibility {
    fun check(manifest: AiModelManifest, environment: AiRuntimeEnvironment): ModelCompatibility {
        val reasons = mutableListOf<String>()
        if (manifest.id.isBlank()) reasons += "Model ID is missing."
        if (manifest.displayName.isBlank()) reasons += "Model name is missing."
        if (manifest.runtimeId.isBlank()) reasons += "No runtime adapter is declared."
        if (manifest.tasks.isEmpty()) reasons += "No supported AI task is declared."
        if (manifest.artifactBytes <= 0L) reasons += "Artifact size is invalid."
        if (manifest.artifactBytes > environment.maximumArtifactBytes) {
            reasons += "Artifact exceeds the configured 15 GB integration limit."
        }
        if (manifest.minimumAndroidApi > environment.androidApi) {
            reasons += "Requires Android API ${manifest.minimumAndroidApi}."
        }
        if (manifest.executionMode == ExecutionMode.ON_DEVICE) {
            val peak = manifest.estimatedPeakRamBytes
            if (peak == null || peak <= 0L) {
                reasons += "Peak RAM estimate is required for on-device safety checks."
            } else if (peak > environment.availableMemoryBytes) {
                reasons += "Estimated peak RAM exceeds currently available memory."
            }
        }
        manifest.sha256?.let {
            if (!it.matches(Regex("(?i)^[a-f0-9]{64}$"))) reasons += "SHA-256 must contain exactly 64 hexadecimal characters."
        }
        return if (reasons.isEmpty()) ModelCompatibility.Compatible else ModelCompatibility.Rejected(reasons)
    }

    fun verifyArtifact(file: File, expectedSha256: String?): Boolean {
        if (!file.isFile || !file.canRead()) return false
        if (expectedSha256.isNullOrBlank()) return true
        val digest = java.security.MessageDigest.getInstance("SHA-256")
        file.inputStream().buffered().use { input ->
            val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
            while (true) {
                val count = input.read(buffer)
                if (count < 0) break
                digest.update(buffer, 0, count)
            }
        }
        val actual = digest.digest().joinToString("") { "%02x".format(it) }
        return actual.equals(expectedSha256, ignoreCase = true)
    }
}

data class AiInferenceRequest(
    val task: AiTask,
    val prompt: String? = null,
    val inputFile: File? = null,
    val options: Map<String, String> = emptyMap()
)

data class AiInferenceResult(
    val text: String? = null,
    val outputFiles: List<File> = emptyList(),
    val metadata: Map<String, String> = emptyMap(),
    val embedding: FloatArray? = null
)

/** Implement this interface for each concrete engine (LiteRT-LM, llama.cpp, ONNX, diffusion, etc.). */
interface AiRuntimeAdapter {
    val runtimeId: String
    val supportedFormats: Set<ModelArtifactFormat>
    val supportedTasks: Set<AiTask>

    suspend fun load(manifest: AiModelManifest, artifact: File)
    suspend fun infer(request: AiInferenceRequest): AiInferenceResult
    suspend fun unload()
}


/** In-memory registry for trusted adapters packaged with Astronaut. */
class AiRuntimeRegistry(adapters: Collection<AiRuntimeAdapter> = emptyList()) {
    private val byId = linkedMapOf<String, AiRuntimeAdapter>()

    init {
        adapters.forEach(::register)
    }

    fun register(adapter: AiRuntimeAdapter) {
        require(adapter.runtimeId.isNotBlank()) { "Runtime ID cannot be blank." }
        require(adapter.supportedFormats.isNotEmpty()) { "Runtime must declare supported formats." }
        require(adapter.supportedTasks.isNotEmpty()) { "Runtime must declare supported tasks." }
        require(!byId.containsKey(adapter.runtimeId)) { "Runtime already registered: ${adapter.runtimeId}" }
        byId[adapter.runtimeId] = adapter
    }

    fun find(manifest: AiModelManifest): AiRuntimeAdapter? {
        val adapter = byId[manifest.runtimeId] ?: return null
        if (manifest.artifactFormat !in adapter.supportedFormats) return null
        if (!adapter.supportedTasks.containsAll(manifest.tasks)) return null
        return adapter
    }

    fun runtimeIds(): Set<String> = byId.keys.toSet()
}
