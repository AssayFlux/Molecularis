package org.molecularis.app.ai
enum class Capability { CHAT, CODE, VISION, AUDIO_TRANSCRIPTION, EMBEDDING, IMAGE_GENERATION }
data class ModelDescriptor(val id: String, val name: String, val runtimeId: String, val capabilities: Set<Capability>, val installed: Boolean, val ramEstimateMb: Int? = null, val localPath: String? = null)
data class InferenceRequest(val prompt: String, val conversationId: Long, val maxTokens: Int = 512)
data class ModelResult(val modelId: String, val text: String, val elapsedMs: Long)
interface LocalModelProvider {
 val providerId: String
 suspend fun isAvailable(model: ModelDescriptor): Boolean
 suspend fun generate(model: ModelDescriptor, request: InferenceRequest): ModelResult
 suspend fun unload(modelId: String)
}
// Production providers must wrap real runtimes such as llama.cpp or LiteRT-LM. No fake provider is shipped.
