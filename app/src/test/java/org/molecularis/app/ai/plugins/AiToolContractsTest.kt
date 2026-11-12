package org.molecularis.app.ai.plugins

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class AiToolContractsTest {
    private val manifest = AiModelManifest(
        id = "demo-chat",
        displayName = "Demo chat",
        artifactFormat = ModelArtifactFormat.GGUF,
        runtimeId = "llama.cpp",
        tasks = setOf(AiTask.CHAT, AiTask.CODE),
        executionMode = ExecutionMode.ON_DEVICE,
        artifactBytes = 1024L,
        sha256 = "a".repeat(64),
        estimatedPeakRamBytes = 512L
    )

    @Test fun acceptsModelWithinArtifactAndRamLimits() {
        assertEquals(
            ModelCompatibility.Compatible,
            AiModelCompatibility.check(manifest, AiRuntimeEnvironment(35, 1024L))
        )
    }

    @Test fun rejectsArtifactAboveFifteenGb() {
        val oversized = manifest.copy(artifactBytes = 15L * 1024L * 1024L * 1024L + 1L)
        val result = AiModelCompatibility.check(oversized, AiRuntimeEnvironment(35, Long.MAX_VALUE))
        assertTrue(result is ModelCompatibility.Rejected)
        assertTrue((result as ModelCompatibility.Rejected).reasons.any { it.contains("15 GB") })
    }

    @Test fun rejectsModelWhoseEstimatedPeakRamIsTooHigh() {
        val result = AiModelCompatibility.check(manifest, AiRuntimeEnvironment(35, 256L))
        assertTrue(result is ModelCompatibility.Rejected)
        assertTrue((result as ModelCompatibility.Rejected).reasons.any { it.contains("RAM") })
    }

    @Test fun registryRequiresFormatAndAllDeclaredTasks() {
        val adapter = object : AiRuntimeAdapter {
            override val runtimeId = "llama.cpp"
            override val supportedFormats = setOf(ModelArtifactFormat.GGUF)
            override val supportedTasks = setOf(AiTask.CHAT, AiTask.CODE)
            override suspend fun load(manifest: AiModelManifest, artifact: java.io.File) = Unit
            override suspend fun infer(request: AiInferenceRequest) = AiInferenceResult(text = "ok")
            override suspend fun unload() = Unit
        }
        val registry = AiRuntimeRegistry(listOf(adapter))
        assertTrue(registry.find(manifest) === adapter)
        assertFalse(registry.find(manifest.copy(artifactFormat = ModelArtifactFormat.ONNX)) === adapter)
        assertEquals(setOf("llama.cpp"), registry.runtimeIds())
    }
}
