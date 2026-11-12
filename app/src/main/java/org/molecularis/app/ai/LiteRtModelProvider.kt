package org.molecularis.app.ai

import android.content.Context
import android.os.SystemClock
import java.io.File

/**
 * Real LiteRT-LM provider. It loads one selected model for one request and releases it
 * immediately afterward. Collaboration is intentionally sequential to limit peak RAM.
 */
class LiteRtModelProvider(context: Context) : LocalModelProvider {
    private val appContext = context.applicationContext
    override val providerId: String = "litertlm"

    override suspend fun isAvailable(model: ModelDescriptor): Boolean =
        model.localPath?.let { File(it).isFile && File(it).canRead() } == true

    override suspend fun generate(model: ModelDescriptor, request: InferenceRequest): ModelResult {
        val path = model.localPath ?: error("Model has no local file path")
        require(File(path).isFile) { "Model file is missing: " + model.name }
        val runtime = LiteRtRuntime(appContext)
        val started = SystemClock.elapsedRealtime()
        try {
            runtime.load(path)
            val text = runtime.generate(request.prompt)
            return ModelResult(model.name, text, SystemClock.elapsedRealtime() - started)
        } finally {
            runtime.close()
        }
    }

    // Each generate call owns and closes its runtime, so there is nothing left to unload.
    override suspend fun unload(modelId: String) = Unit
}
