package org.assayflux.molecularis

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject

/** Android dispatch boundary for S3 structure-site and S8 genetic-code research tools. */
internal object S3S8Runner {
    const val MAX_STRUCTURE_BYTES = 16 * 1024 * 1024
    const val MAX_FASTA_CHARS = 1_000_000

    private fun python(context: Context): Python {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        return Python.getInstance()
    }

    fun analyzeLigandSite(
        context: Context,
        sourceText: String,
        sourceFormat: String,
        ligandChain: String,
        ligandResidueNumber: Int,
        ligandResidueName: String,
        cutoffAngstrom: Double,
    ): JSONObject {
        require(sourceText.toByteArray(Charsets.UTF_8).size <= MAX_STRUCTURE_BYTES) {
            "Structure input exceeds the 16 MiB limit."
        }
        require(sourceFormat == "pdb" || sourceFormat == "mmcif") {
            "Select a PDB or mmCIF structure."
        }
        require(ligandChain.isNotBlank()) { "Enter the ligand chain identifier." }
        require(ligandResidueName.isNotBlank()) { "Enter the ligand residue name." }
        require(cutoffAngstrom.isFinite() && cutoffAngstrom > 0.0) {
            "Contact cutoff must be finite and positive."
        }
        val json = python(context).getModule("kinetics_probe")
            .callAttr(
                "analyze_ligand_site",
                sourceText,
                sourceFormat,
                ligandChain,
                ligandResidueNumber,
                ligandResidueName,
                cutoffAngstrom,
            ).toString()
        return JSONObject(json)
    }

    fun analyzeApoPockets(
        context: Context,
        sourceText: String,
        sourceFormat: String,
    ): JSONObject {
        require(sourceText.toByteArray(Charsets.UTF_8).size <= MAX_STRUCTURE_BYTES) {
            "Structure input exceeds the 16 MiB limit."
        }
        require(sourceFormat == "pdb" || sourceFormat == "mmcif") {
            "Select a PDB or mmCIF structure."
        }
        val json = python(context).getModule("kinetics_probe")
            .callAttr("analyze_apo_pockets", sourceText, sourceFormat).toString()
        return JSONObject(json)
    }

    fun inferGeneticCode(
        context: Context,
        fastaText: String,
        completeCds: Boolean,
    ): JSONObject {
        require(fastaText.isNotBlank()) { "Enter coding-sequence FASTA records." }
        require(fastaText.length <= MAX_FASTA_CHARS) {
            "FASTA input exceeds the 1,000,000-character limit."
        }
        val json = python(context).getModule("kinetics_probe")
            .callAttr("infer_genetic_code_from_fasta", fastaText, completeCds).toString()
        return JSONObject(json)
    }
}
