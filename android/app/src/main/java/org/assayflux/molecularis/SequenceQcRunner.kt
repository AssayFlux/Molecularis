package org.assayflux.molecularis

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject

internal data class SequenceQcRecord(
    val identifier: String,
    val length: Int,
    val gcPercent: Double,
    val ambiguousCount: Int,
)

internal data class SequenceQcResult(
    val recordCount: Int,
    val totalBases: Int,
    val records: List<SequenceQcRecord>,
)

internal data class FastqReadQc(val identifier: String, val length: Int,
    val meanPhred: Double, val q20Fraction: Double, val q30Fraction: Double)

internal data class FastqQcResult(val recordCount: Int, val totalBases: Int,
    val phredOffset: Int, val meanPhred: Double, val q20Fraction: Double,
    val q30Fraction: Double, val reads: List<FastqReadQc>)

internal object SequenceQcRunner {
    const val MAX_INPUT_CHARS = 1_000_000

    fun analyzeFastq(context: Context, fastqText: String, phredOffset: Int): FastqQcResult {
        require(fastqText.isNotBlank()) { "Enter FASTQ records before analysis." }
        require(fastqText.length <= MAX_INPUT_CHARS) { "FASTQ input exceeds the 1,000,000-character limit." }
        require(phredOffset == 33 || phredOffset == 64) { "Select Phred+33 or Phred+64 explicitly." }
        if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
        val json = Python.getInstance().getModule("molecularis_probe")
            .callAttr("analyze_fastq", fastqText, phredOffset).toString()
        val root = JSONObject(json)
        val array = root.getJSONArray("reads")
        val reads = (0 until array.length()).map { i ->
            val item = array.getJSONObject(i)
            FastqReadQc(item.getString("identifier"), item.getInt("length"),
                item.getDouble("mean_phred"), item.getDouble("q20_fraction"),
                item.getDouble("q30_fraction"))
        }
        return FastqQcResult(root.getInt("record_count"), root.getInt("total_bases"),
            root.getInt("phred_offset"), root.getDouble("mean_phred"),
            root.getDouble("q20_fraction"), root.getDouble("q30_fraction"), reads)
    }

    fun analyze(context: Context, fastaText: String): SequenceQcResult {
        require(fastaText.isNotBlank()) { "Enter FASTA records before analysis." }
        require(fastaText.length <= MAX_INPUT_CHARS) {
            "FASTA input exceeds the 1,000,000-character limit."
        }
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        val json = Python.getInstance()
            .getModule("molecularis_probe")
            .callAttr("analyze_fasta", fastaText)
            .toString()
        val root = JSONObject(json)
        val recordsJson = root.getJSONArray("records")
        val records = (0 until recordsJson.length()).map { index ->
            val item = recordsJson.getJSONObject(index)
            SequenceQcRecord(
                identifier = item.getString("identifier"),
                length = item.getInt("length"),
                gcPercent = item.getDouble("gc_percent"),
                ambiguousCount = item.getInt("ambiguous_count"),
            )
        }
        return SequenceQcResult(
            recordCount = root.getInt("record_count"),
            totalBases = root.getInt("total_bases"),
            records = records,
        )
    }
}
