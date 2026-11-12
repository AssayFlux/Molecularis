package org.molecularis.app.ai.plugins

import android.app.ActivityManager
import android.content.Context
import android.os.Build

/** Device snapshot for preflight checks; free RAM is volatile and is not a load guarantee. */
object AndroidAiRuntimeEnvironment {
    fun current(context: Context): AiRuntimeEnvironment {
        val manager = context.applicationContext.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        val memory = ActivityManager.MemoryInfo().also(manager::getMemoryInfo)
        return AiRuntimeEnvironment(
            androidApi = Build.VERSION.SDK_INT,
            availableMemoryBytes = memory.availMem,
            maximumArtifactBytes = 15_000_000_000L
        )
    }

    fun check(context: Context, manifest: AiModelManifest): ModelCompatibility =
        AiModelCompatibility.check(manifest, current(context))
}
