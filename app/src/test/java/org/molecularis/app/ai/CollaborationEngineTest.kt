package org.molecularis.app.ai

import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class CollaborationEngineTest {
    private class FakeProvider(
        var available: Boolean = true,
        var availabilityFailure: Exception? = null
    ) : LocalModelProvider {
        override val providerId = "fake"
        val generated = mutableListOf<String>()
        val unloaded = mutableListOf<String>()
        override suspend fun isAvailable(model: ModelDescriptor): Boolean {
            availabilityFailure?.let { throw it }
            return available
        }
        override suspend fun generate(model: ModelDescriptor, request: InferenceRequest): ModelResult {
            generated += model.name
            return ModelResult(model.name, "answer from " + model.name, 12L)
        }
        override suspend fun unload(modelId: String) { unloaded += modelId }
    }

    private fun catalog(provider: FakeProvider): ModelCatalog = ModelCatalog().apply {
        register(ModelDescriptor("one", "One", provider.providerId, setOf(Capability.CHAT), true, localPath = "/models/one"))
        register(ModelDescriptor("two", "Two", provider.providerId, setOf(Capability.CHAT), true, localPath = "/models/two"))
    }

    @Test fun requiresTwoDistinctInstalledModels() = runBlocking {
        val provider = FakeProvider()
        val catalog = ModelCatalog()
        catalog.register(ModelDescriptor("one", "One", provider.providerId, setOf(Capability.CHAT), true, localPath = "/models/one"))
        val result = CollaborationEngine(listOf(provider), catalog).execute(
            InferenceRequest("Explain offline AI", 1L), setOf(Capability.CHAT), provider
        )
        assertTrue(result is CollaborationResult.Unavailable)
        assertTrue(provider.generated.isEmpty())
    }

    @Test fun runsTwoModelsAndThenCoordinator() = runBlocking {
        val provider = FakeProvider()
        val catalog = catalog(provider)
        val progress = mutableListOf<String>()
        val result = CollaborationEngine(listOf(provider), catalog).execute(
            InferenceRequest("Compare these approaches", 2L), setOf(Capability.CHAT), provider
        ) { progress += it }

        assertTrue(result is CollaborationResult.Success)
        result as CollaborationResult.Success
        assertEquals(2, result.participants.size)
        assertEquals(listOf("One", "Two", "One"), provider.generated)
        assertEquals(3, progress.size)
        assertEquals("answer from One", result.finalAnswer)
        assertEquals(listOf("one", "two"), provider.unloaded)
    }

    @Test fun duplicatePathsDoNotCountAsTwoModels() = runBlocking {
        val provider = FakeProvider()
        val catalog = ModelCatalog()
        catalog.register(ModelDescriptor("one", "One", provider.providerId, setOf(Capability.CHAT), true, localPath = "/models/shared"))
        catalog.register(ModelDescriptor("two", "Duplicate copy", provider.providerId, setOf(Capability.CHAT), true, localPath = "/models/shared"))
        val result = CollaborationEngine(listOf(provider), catalog).execute(
            InferenceRequest("Check", 3L), setOf(Capability.CHAT), provider
        )
        assertTrue(result is CollaborationResult.Unavailable)
    }

    @Test fun availabilityFailureReturnsUnavailableInsteadOfEscaping() = runBlocking {
        val provider = FakeProvider(availabilityFailure = IllegalStateException("runtime probe failed"))
        val result = CollaborationEngine(listOf(provider), catalog(provider)).execute(
            InferenceRequest("Check", 4L), setOf(Capability.CHAT), provider
        )
        assertTrue(result is CollaborationResult.Unavailable)
        assertTrue(provider.generated.isEmpty())
    }

    @Test fun unavailableCoordinatorDoesNotClaimSuccess() = runBlocking {
        val provider = FakeProvider()
        val unavailableCoordinator = FakeProvider(available = false)
        val coordinatorModel = ModelDescriptor(
            "coordinator", "Coordinator", unavailableCoordinator.providerId,
            setOf(Capability.CHAT), true, localPath = "/models/coordinator"
        )
        val models = catalog(provider).apply { register(coordinatorModel) }
        val result = CollaborationEngine(listOf(provider, unavailableCoordinator), models).execute(
            InferenceRequest("Check", 5L), setOf(Capability.CHAT), unavailableCoordinator
        )
        assertTrue(result is CollaborationResult.Unavailable)
        assertEquals(listOf("One", "Two"), provider.generated)
        assertTrue(unavailableCoordinator.generated.isEmpty())
    }

    @Test fun cancellationDuringAvailabilityCheckIsPropagated() = runBlocking {
        val provider = FakeProvider(availabilityFailure = CancellationException("cancelled"))
        val result = runCatching {
            CollaborationEngine(listOf(provider), catalog(provider)).execute(
                InferenceRequest("Check", 6L), setOf(Capability.CHAT), provider
            )
        }.exceptionOrNull()
        assertTrue(result is CancellationException)
    }
}
