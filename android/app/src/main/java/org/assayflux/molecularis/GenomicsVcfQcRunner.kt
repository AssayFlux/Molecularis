package org.assayflux.molecularis

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject

/** Aggregate-only VCF QC bridge. Never returns sample identifiers or genotype strings. */
internal object GenomicsVcfQcRunner {
    const val MAX_INPUT_BYTES = 5 * 1024 * 1024

    private fun python(context: Context): Python {
        if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
        return Python.getInstance()
    }

    fun analyze(context: Context, vcfText: String): JSONObject {
        require(vcfText.toByteArray(Charsets.UTF_8).size <= MAX_INPUT_BYTES) {
            "VCF input exceeds the 5 MiB limit."
        }
        return JSONObject(
            python(context).getModule("molecularis_probe")
                .callAttr("summarize_vcf_research_qc", vcfText).toString(),
        )
    }
}
