package org.molecularis.app.ai

import kotlinx.coroutines.CancellationException

enum class TaskKind { GENERAL, PROGRAMMING, DOCUMENT, IMAGE, AUDIO, CREATIVE }
data class RoutingDecision(val task: TaskKind, val required: Set<Capability>)
class TaskRouter {
    fun classify(prompt: String): RoutingDecision {
        val p = prompt.lowercase()
        return when {
            listOf("debug", "code", "function", "python", "kotlin", "compile").any(p::contains) ->
                RoutingDecision(TaskKind.PROGRAMMING, setOf(Capability.CODE))
            listOf("photo", "image", "picture").any(p::contains) ->
                RoutingDecision(TaskKind.IMAGE, setOf(Capability.VISION))
            listOf("transcribe", "audio", "speech").any(p::contains) ->
                RoutingDecision(TaskKind.AUDIO, setOf(Capability.AUDIO_TRANSCRIPTION))
            listOf("pdf", "document", "paper").any(p::contains) ->
                RoutingDecision(TaskKind.DOCUMENT, setOf(Capability.CHAT))
            else -> RoutingDecision(TaskKind.GENERAL, setOf(Capability.CHAT))
        }
    }
}

class ModelCatalog {
    private val models = linkedMapOf<String, ModelDescriptor>()
    fun register(model: ModelDescriptor) { models[model.id] = model }
    fun all() = models.values.toList()
    fun compatible(required: Set<Capability>) = all().filter { it.installed && it.capabilities.containsAll(required) }
}

sealed interface CollaborationResult {
    data class Success(val participants: List<ModelResult>, val finalAnswer: String) : CollaborationResult
    data class Unavailable(val reason: String) : CollaborationResult
}

/**
 * Sequential peer review. Each participant receives the same original task; a coordinator
 * then reviews both outputs. Progress is surfaced to the UI and failures are never fabricated.
 */
class CollaborationEngine(
    private val providers: List<LocalModelProvider>,
    private val catalog: ModelCatalog
) {
    suspend fun execute(
        request: InferenceRequest,
        required: Set<Capability>,
        coordinator: LocalModelProvider,
        onProgress: (String) -> Unit = {}
    ): CollaborationResult {
        val candidates = catalog.compatible(required)
            .distinctBy { it.localPath ?: it.id }
            .take(2)
        if (candidates.size < 2) {
            return CollaborationResult.Unavailable("Two distinct installed compatible models are required.")
        }

        val outputs = mutableListOf<ModelResult>()
        for (model in candidates) {
            val provider = providers.firstOrNull { it.providerId == model.runtimeId }
                ?: return CollaborationResult.Unavailable("Required model runtime is not registered.")
            val available = try {
                provider.isAvailable(model)
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (error: Exception) {
                return CollaborationResult.Unavailable(
                    "Could not check model " + model.name + ": " + (error.message ?: error.javaClass.simpleName)
                )
            }
            if (!available) {
                return CollaborationResult.Unavailable("A selected model is unavailable.")
            }
            try {
                onProgress("Independent review: " + model.name)
                outputs += provider.generate(
                    model,
                    request.copy(prompt = "Independently solve this task. State assumptions and uncertainties. Do not assume another model has answered.\n\nTask:\n" + request.prompt)
                )
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (error: Exception) {
                return CollaborationResult.Unavailable("Model " + model.name + " failed: " + (error.message ?: error.javaClass.simpleName))
            } finally {
                try { provider.unload(model.id) } catch (_: Exception) { }
            }
        }

        val coordinatorModel = catalog.all().firstOrNull {
            it.installed && it.runtimeId == coordinator.providerId && Capability.CHAT in it.capabilities
        } ?: return CollaborationResult.Unavailable("No installed coordinator model is available.")
        val coordinatorAvailable = try {
            coordinator.isAvailable(coordinatorModel)
        } catch (cancelled: CancellationException) {
            throw cancelled
        } catch (error: Exception) {
            return CollaborationResult.Unavailable(
                "Could not check coordinator " + coordinatorModel.name + ": " + (error.message ?: error.javaClass.simpleName)
            )
        }
        if (!coordinatorAvailable) {
            return CollaborationResult.Unavailable("The coordinator model is unavailable.")
        }
        val joined = outputs.joinToString("\n\n") { "[" + it.modelId + "]\n" + it.text }
        return try {
            onProgress("Coordinator synthesis: " + coordinatorModel.name)
            val final = coordinator.generate(
                coordinatorModel,
                request.copy(prompt = "Review the independent model answers. Compare correctness, identify disagreements and missing assumptions, then produce one careful final answer.\n\nOriginal task:\n" + request.prompt + "\n\nIndependent answers:\n" + joined)
            )
            CollaborationResult.Success(outputs, final.text)
        } catch (cancelled: CancellationException) {
            throw cancelled
        } catch (error: Exception) {
            CollaborationResult.Unavailable("Coordinator synthesis failed: " + (error.message ?: error.javaClass.simpleName))
        }
    }
}
