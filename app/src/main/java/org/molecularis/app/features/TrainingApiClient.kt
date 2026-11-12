package org.molecularis.app.features

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

data class TrainingJobStatus(
    val id: String,
    val state: String,
    val progress: Float,
    val message: String,
    val artifactUrl: String?
)

/**
 * Explicit opt-in client for the user's own HTTPS training server.
 * API credentials are supplied per call and are never persisted by this client.
 */
class TrainingApiClient(
    baseUrl: String,
    private val apiKey: String
) {
    private val base = baseUrl.trimEnd('/')

    init {
        val parsed = URL(base)
        require(parsed.protocol.equals("https", ignoreCase = true)) {
            "Training server must use HTTPS. Do not send datasets or API keys over plain HTTP."
        }
        require(parsed.host.isNotBlank()) { "Training server URL is invalid." }
        require(apiKey.length >= 16) { "Enter the API key configured on your training server." }
    }

    suspend fun uploadDataset(fileName: String, content: String): String = withContext(Dispatchers.IO) {
        val boundary = "----Astronaut" + System.nanoTime().toString(16)
        val safeName = fileName.substringAfterLast('/').replace(Regex("[^A-Za-z0-9._-]"), "_")
            .ifBlank { "dataset.jsonl" }
        require(safeName.endsWith(".jsonl", ignoreCase = true)) { "Training API accepts JSONL files only." }
        val data = content.toByteArray(Charsets.UTF_8)
        require(data.size <= 20 * 1024 * 1024) { "Dataset exceeds the app's 20 MiB upload limit." }
        val prefix = (
            "--$boundary\r\n" +
                "Content-Disposition: form-data; name=\"file\"; filename=\"$safeName\"\r\n" +
                "Content-Type: application/jsonl\r\n\r\n"
            ).toByteArray(Charsets.UTF_8)
        val suffix = "\r\n--$boundary--\r\n".toByteArray(Charsets.UTF_8)
        val response = request(
            path = "/v1/datasets",
            method = "POST",
            contentType = "multipart/form-data; boundary=$boundary",
            body = prefix + data + suffix
        )
        response.getString("id")
    }

    suspend fun startJob(
        datasetId: String,
        baseModelPath: String,
        method: String,
        epochs: Int
    ): TrainingJobStatus = withContext(Dispatchers.IO) {
        require(method == "lora" || method == "qlora")
        require(epochs in 1..10)
        val body = JSONObject()
            .put("dataset_id", datasetId)
            .put("base_model", baseModelPath)
            .put("method", method)
            .put("epochs", epochs)
        parseJob(request("/v1/training/jobs", "POST", "application/json", body.toString().toByteArray()))
    }

    suspend fun getJob(jobId: String): TrainingJobStatus = withContext(Dispatchers.IO) {
        parseJob(request("/v1/training/jobs/$jobId", "GET"))
    }

    suspend fun cancelJob(jobId: String): TrainingJobStatus = withContext(Dispatchers.IO) {
        parseJob(request("/v1/training/jobs/$jobId/cancel", "POST", "application/json", "{}".toByteArray()))
    }

    private fun parseJob(json: JSONObject) = TrainingJobStatus(
        id = json.getString("id"),
        state = json.getString("state"),
        progress = json.optDouble("progress", 0.0).toFloat().coerceIn(0f, 100f),
        message = json.optString("message", ""),
        artifactUrl = json.optString("artifact_url").takeIf { it.isNotBlank() && it != "null" }
    )

    private fun request(
        path: String,
        method: String,
        contentType: String? = null,
        body: ByteArray? = null
    ): JSONObject {
        val connection = URL(base + path).openConnection() as HttpURLConnection
        try {
            connection.requestMethod = method
            connection.instanceFollowRedirects = false
            connection.connectTimeout = 20_000
            connection.readTimeout = 45_000
            connection.setRequestProperty("Accept", "application/json")
            connection.setRequestProperty("X-API-Key", apiKey)
            if (body != null) {
                connection.doOutput = true
                connection.setRequestProperty("Content-Type", contentType ?: "application/json")
                connection.setFixedLengthStreamingMode(body.size)
                connection.outputStream.use { it.write(body) }
            }
            val status = connection.responseCode
            val stream = if (status in 200..299) connection.inputStream else connection.errorStream
            val responseText = stream?.bufferedReader(Charsets.UTF_8)?.use { it.readText() }.orEmpty()
            if (status !in 200..299) {
                val detail = runCatching { JSONObject(responseText).optString("detail") }.getOrNull()
                throw IOException("Training API HTTP $status: " + (detail?.takeIf { it.isNotBlank() } ?: responseText.take(300)))
            }
            return if (responseText.isBlank()) JSONObject() else JSONObject(responseText)
        } finally {
            connection.disconnect()
        }
    }
}
