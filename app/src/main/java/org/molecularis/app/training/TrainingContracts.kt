package org.molecularis.app.training
enum class DatasetFormat { JSONL, JSON, CSV, TXT }
data class DatasetManifest(val name: String, val sourceUri: String, val format: DatasetFormat, val trainCount: Int, val validationCount: Int)
data class FineTuneConfig(val baseModelId: String, val method: String = "LoRA", val epochs: Int = 1, val learningRate: Double = 0.0002, val rank: Int = 8)
data class TrainingJobStatus(val jobId: String, val state: String, val progressPercent: Int?, val message: String?)
interface TrainingExecutor {
 suspend fun validate(dataset: DatasetManifest, config: FineTuneConfig): List<String>
 suspend fun submit(dataset: DatasetManifest, config: FineTuneConfig): String
 suspend fun status(jobId: String): TrainingJobStatus
 suspend fun cancel(jobId: String)
}
// Contract only: actual fine-tuning requires a real trainer and appropriate hardware/backend.
