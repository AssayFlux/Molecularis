package org.molecularis.app.features

import android.app.Application
import android.content.Context
import android.os.Build
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/** Opt-in, on-device crash metadata. It never records exception messages, chat text, files or network data. */
object CrashDiagnostics {
    private const val PREFS = "molecularis_diagnostics"
    private const val ENABLED = "enabled"

    fun isEnabled(context: Context): Boolean =
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getBoolean(ENABLED, false)

    fun setEnabled(context: Context, enabled: Boolean) {
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putBoolean(ENABLED, enabled).apply()
    }

    fun install(application: Application) {
        val previous = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, error ->
            if (isEnabled(application)) runCatching {
                val directory = File(application.filesDir, "diagnostics").apply { mkdirs() }
                val stamp = SimpleDateFormat("yyyyMMdd-HHmmss", Locale.US).format(Date())
                val file = File(directory, "crash-$stamp.txt")
                file.bufferedWriter().use { out ->
                    out.appendLine("Molecularis local crash diagnostic")
                    out.appendLine("time=$stamp")
                    out.appendLine("thread=${thread.name.take(80)}")
                    out.appendLine("device=${Build.MANUFACTURER.take(60)} ${Build.MODEL.take(80)}")
                    out.appendLine("android_sdk=${Build.VERSION.SDK_INT}")
                    out.appendLine("exception_type=${error.javaClass.name.take(200)}")
                    out.appendLine("stack_frames:")
                    error.stackTrace.take(80).forEach { frame ->
                        out.appendLine("  ${frame.className.take(200)}.${frame.methodName.take(120)}(${frame.fileName?.take(120)}:${frame.lineNumber})")
                    }
                }
                directory.listFiles()?.filter { it.name.startsWith("crash-") }?.sortedByDescending { it.lastModified() }?.drop(3)?.forEach(File::delete)
            }
            previous?.uncaughtException(thread, error)
        }
    }

    fun export(context: Context): String {
        val directory = File(context.filesDir, "diagnostics")
        val logs = directory.listFiles()?.filter { it.name.startsWith("crash-") }?.sortedByDescending { it.lastModified() }.orEmpty()
        return if (logs.isEmpty()) "No crash diagnostics are stored on this device." else logs.joinToString("\n\n") { it.readText().take(32_000) }
    }

    fun hasLogs(context: Context): Boolean =
        File(context.filesDir, "diagnostics").listFiles()?.any { it.name.startsWith("crash-") } == true
}
