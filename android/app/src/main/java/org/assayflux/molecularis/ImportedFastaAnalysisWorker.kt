package org.assayflux.molecularis

import android.content.Context
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject

/** Authenticated, bounded, on-device FASTA QC for an already imported research job. */
class ImportedFastaAnalysisWorker(context: Context, parameters: WorkerParameters) : Worker(context, parameters) {
    override fun doWork(): Result {
        val jobId = inputData.getString(KEY_JOB_ID) ?: return Result.failure()
        if (!jobId.matches(Regex("[A-Za-z0-9_-]{1,80}"))) return Result.failure()
        val store = ResearchStore(applicationContext)
        return try {
            val name = store.storedInputName(jobId) ?: error("Research job does not exist")
            val committedBytes = store.storedInputByteCount(jobId)
                ?: error("Only completed, hash-verified imports can be analysed")
            require(committedBytes in 1..MAX_INPUT_BYTES) {
                "FASTA import exceeds the 1,000,000-byte analysis limit"
            }
            val normalizedName = name.lowercase().removeSuffix(".gz")
            require(normalizedName.substringAfterLast('.') in setOf("fa", "fasta", "fna")) {
                "This worker accepts FASTA files only; FASTQ requires an explicit Phred offset."
            }
            val result = store.withStoredInput(jobId) { file ->
                require(file.isFile && file.length() in 1..MAX_INPUT_BYTES) {
                    "FASTA import exceeds the 1,000,000-byte analysis limit"
                }
                val text = SequenceFileSupport.readText(file, name.lowercase().endsWith(".gz"), MAX_INPUT_BYTES, MAX_INPUT_CHARS)
                if (!Python.isStarted()) Python.start(AndroidPlatform(applicationContext))
                val json = Python.getInstance().getModule("kinetics_probe")
                    .callAttr("analyze_fasta", text).toString()
                require(json.length <= MAX_RESULT_CHARS) {
                    "FASTA QC result exceeds the 2,000,000-character storage limit"
                }
                val parsed = JSONObject(json)
                check(parsed.getInt("record_count") > 0) { "FASTA contains no records" }
                check(parsed.getJSONArray("records").length() > 0) { "FASTA QC result contains no records" }
                json
            } ?: error("Imported encrypted input is unavailable")
            store.saveAnalysisResult(
                id = jobId,
                toolId = "sequence.fasta.qc",
                toolVersion = "1",
                parametersJson = """{"input":"authenticated-decrypted-import","compression":"auto-by-gzip-extension","max_expanded_bytes":1000000,"gc_denominator":"all sequence symbols"}""",
                resultJson = result,
            )
            Result.success()
        } catch (error: Exception) {
            runCatching {
                store.updateJobMessage(
                    jobId,
                    "FASTA QC failed: ${error.message ?: error.javaClass.simpleName}",
                )
            }
            Result.failure()
        } finally {
            store.close()
        }
    }

    companion object {
        const val KEY_JOB_ID = "job_id"
        private const val MAX_INPUT_BYTES = 1_000_000L
        private const val MAX_INPUT_CHARS = 1_000_000
        private const val MAX_RESULT_CHARS = 2_000_000
    }
}
