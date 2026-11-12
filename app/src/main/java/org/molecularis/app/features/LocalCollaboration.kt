package org.molecularis.app.features

import kotlinx.coroutines.CancellationException
import org.molecularis.app.ai.Capability
import org.molecularis.app.ai.InferenceRequest
import org.molecularis.app.ai.LocalModelProvider
import org.molecularis.app.ai.ModelCatalog
import org.molecularis.app.ai.ModelResult

data class CollaborationReport(
    val modelOutputs: List<ModelResult>,
    val synthesis: String,
    val failures: List<String>
)

/** Executes only models backed by registered providers; sequential execution limits peak RAM use. */
class LocalCollaborationCoordinator(
    private val providers: List<LocalModelProvider>,
    private val catalog: ModelCatalog
) {
    suspend fun run(request: InferenceRequest, required: Set<Capability>, maxPeers: Int = 2): CollaborationReport {
        require(maxPeers in 2..3) { "Choose two or three peer models." }
        val eligible = catalog.compatible(required).take(maxPeers)
        require(eligible.size >= 2) { "At least two installed models with the required capability are needed." }
        val outputs = mutableListOf<ModelResult>()
        val failures = mutableListOf<String>()
        eligible.forEach { model ->
            val provider = providers.firstOrNull { it.providerId == model.runtimeId }
            if (provider == null) failures += "${model.name}: runtime is not registered"
            else try {
                if (!provider.isAvailable(model)) failures += "${model.name}: model/runtime unavailable"
                else outputs += provider.generate(model, request)
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (error: Exception) {
                failures += "${model.name}: ${error.message ?: error.javaClass.simpleName}"
            } finally {
                runCatching { provider.unload(model.id) }
            }
        }
        require(outputs.size >= 2) { "Collaboration stopped: fewer than two peers completed. ${failures.joinToString()}" }
        return CollaborationReport(outputs, "", failures)
    }
}
