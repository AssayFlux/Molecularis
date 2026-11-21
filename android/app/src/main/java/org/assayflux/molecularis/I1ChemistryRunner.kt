package org.assayflux.molecularis

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject

/** Android-safe graph-only ligand preview; RDKit is deliberately not bundled here. */
internal object I1ChemistryRunner {
    const val MAX_SDF_BYTES = 16 * 1024 * 1024

    private fun python(context: Context): Python {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        return Python.getInstance()
    }

    fun analyzeSdfGraph(context: Context, sourceText: String): JSONObject {
        require(sourceText.toByteArray(Charsets.UTF_8).size <= MAX_SDF_BYTES) {
            "SDF input exceeds the 16 MiB limit."
        }
        val json = python(context).getModule("molecularis_probe")
            .callAttr("analyze_ligand_sdf_graph", sourceText)
            .toString()
        return JSONObject(json)
    }
}
