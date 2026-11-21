package org.assayflux.molecularis

import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

object PythonProbe {
    fun report(context: android.content.Context): String {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context))
        }
        return Python.getInstance()
            .getModule("molecularis_probe")
            .callAttr("runtime_report")
            .toString()
    }
}
