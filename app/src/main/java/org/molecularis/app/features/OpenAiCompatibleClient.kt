package org.molecularis.app.features

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL

data class RemoteChatMessage(val role: String, val content: String)

/**
 * OpenAI-compatible Chat Completions client. It sends only the messages explicitly
 * supplied by the caller; it never reads local chat history or attachments itself.
 */
class OpenAiCompatibleClient(
    baseUrl: String,
    private val apiKey: String,
    private val modelId: String,
    private val connectTimeoutMs: Int = 15_000,
    private val readTimeoutMs: Int = 60_000
) {
    private val endpoint: String

    init {
        val uri = URI(baseUrl.trim().trimEnd('/'))
        require(uri.scheme.equals("https", true) && !uri.host.isNullOrBlank()) {
            "Online AI endpoint must be a valid HTTPS URL."
        }
        require(uri.userInfo == null && uri.query == null && uri.fragment == null) {
            "Endpoint URL cannot contain credentials, query parameters or fragments."
        }
        require(apiKey.length >= 8) { "Enter the API key supplied by your provider." }
        require(modelId.isNotBlank() && modelId.length <= 160) { "Enter a valid model ID." }
        val path = uri.path.trimEnd('/')
        val completionPath = if (path.endsWith("/v1")) "$path/chat/completions" else "$path/v1/chat/completions"
        endpoint = URI(uri.scheme, null, uri.host, uri.port, completionPath, null, null).toASCIIString()
    }

    suspend fun complete(messages: List<RemoteChatMessage>, maxTokens: Int = 1024): String =
        withContext(Dispatchers.IO) {
            require(messages.isNotEmpty()) { "At least one message is required." }
            require(messages.size <= 32) { "A maximum of 32 messages can be sent per request." }
            require(messages.all { it.role in setOf("system", "user", "assistant") && it.content.isNotBlank() }) {
                "Messages must have a supported role and non-empty content."
            }
            require(maxTokens in 1..4096) { "maxTokens must be between 1 and 4096." }
            val body = JSONObject()
                .put("model", modelId)
                .put("messages", JSONArray().apply {
                    messages.forEach { put(JSONObject().put("role", it.role).put("content", it.content)) }
                })
                .put("max_tokens", maxTokens)
                .put("stream", false)
                .toString()
                .toByteArray(Charsets.UTF_8)
            val connection = URL(endpoint).openConnection() as HttpURLConnection
            try {
                connection.requestMethod = "POST"
                connection.instanceFollowRedirects = false
                connection.connectTimeout = connectTimeoutMs
                connection.readTimeout = readTimeoutMs
                connection.setRequestProperty("Authorization", "Bearer $apiKey")
                connection.setRequestProperty("Accept", "application/json")
                connection.setRequestProperty("Content-Type", "application/json")
                connection.doOutput = true
                connection.setFixedLengthStreamingMode(body.size)
                connection.outputStream.use { it.write(body) }
                val status = connection.responseCode
                val stream = if (status in 200..299) connection.inputStream else connection.errorStream
                val response = stream?.bufferedReader(Charsets.UTF_8)?.use { reader ->
                    val output = StringBuilder()
                    val buffer = CharArray(4096)
                    var total = 0
                    while (true) {
                        val count = reader.read(buffer)
                        if (count < 0) break
                        total += count
                        if (total > MAX_RESPONSE_CHARS) throw IOException("Online AI response exceeded the 1 MiB limit.")
                        output.append(buffer, 0, count)
                    }
                    output.toString()
                }.orEmpty()
                if (status !in 200..299) {
                    val detail = runCatching { JSONObject(response).optString("error").takeIf { it.isNotBlank() } }.getOrNull()
                    throw IOException("Online AI HTTP $status: " + (detail ?: response.take(240)))
                }
                val json = JSONObject(response)
                val choices = json.getJSONArray("choices")
                require(choices.length() > 0) { "Provider returned no completion choices." }
                choices.getJSONObject(0).getJSONObject("message").getString("content").trim()
                    .also { require(it.isNotBlank()) { "Provider returned an empty completion." } }
            } finally {
                connection.disconnect()
            }
        }

    companion object {
        private const val MAX_RESPONSE_CHARS = 1_048_576
    }
}
