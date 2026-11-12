package org.molecularis.app.features

import org.molecularis.app.data.KnowledgeChunkEntity
import org.molecularis.app.data.KnowledgeDao
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.security.MessageDigest
import kotlin.math.max

/**
 * Persistent, on-device hybrid retrieval. Text and vectors are stored in the encrypted Room DB.
 * The caller owns the embedding provider and should close it when the model is unloaded.
 */
class PersistentHybridRag(
    private val dao: KnowledgeDao,
    private val embedder: LocalEmbeddingProvider,
    private val scopeId: String,
    private val maxChunkChars: Int = 900,
    private val overlapChars: Int = 120
) {
    init {
        require(scopeId.isNotBlank()) { "A conversation or project scope is required." }
        require(maxChunkChars >= 128) { "Chunk size must be at least 128 characters." }
        require(overlapChars in 0 until maxChunkChars) { "Chunk overlap must be smaller than chunk size." }
    }

    suspend fun indexDocument(source: String, text: String): Int {
        require(source.isNotBlank() && text.isNotBlank()) { "A source name and readable text are required." }
        val chunks = splitIntoChunks(text)
        val rows = chunks.mapIndexed { index, chunk ->
            val vector = embedder.embed(chunk.text)
            require(vector.size == embedder.dimensions) { "Embedding model returned an unexpected vector size." }
            KnowledgeChunkEntity(
                id = stableId(embedder.modelId, scopeId, source, index),
                source = source,
                chunkIndex = index,
                pageNumber = chunk.pageNumber,
                text = chunk.text,
                embeddingModelId = embedder.modelId,
                scopeId = scopeId,
                embedding = encode(vector)
            )
        }
        // Build all vectors before replacing the old source so an embedding failure preserves it.
        dao.deleteSource(source, embedder.modelId, scopeId)
        if (rows.isNotEmpty()) dao.upsert(rows)
        return rows.size
    }

    suspend fun removeDocument(source: String) = dao.deleteSource(source, embedder.modelId, scopeId)

    suspend fun indexedChunkCount(): Int = dao.countForModel(embedder.modelId, scopeId)

    suspend fun search(query: String, limit: Int = 5): List<RetrievedChunk> {
        require(limit in 1..50) { "Retrieval limit must be between 1 and 50." }
        if (query.isBlank()) return emptyList()
        val rows = dao.chunksForModel(embedder.modelId, scopeId)
        if (rows.isEmpty()) return emptyList()

        val queryVector = embedder.embed(query)
        require(queryVector.size == embedder.dimensions) { "Query embedding dimension mismatch." }

        val lexicalIndex = LocalRagIndex(maxChunkChars = max(128, maxChunkChars), overlap = 0)
        rows.forEach { lexicalIndex.add(it.id, it.text) }
        val lexicalScores = lexicalIndex.search(query, limit = rows.size.coerceAtMost(100)).associate { it.chunk.source to it.score }
        val maxLexical = lexicalScores.values.maxOrNull()?.takeIf { it > 0.0 } ?: 1.0

        return rows.mapNotNull { row ->
            val vector = decode(row.embedding)
            if (vector.size != embedder.dimensions) return@mapNotNull null
            val cosine = cosineSimilarity(queryVector, vector)
            val semanticScore = ((cosine + 1.0) / 2.0).coerceIn(0.0, 1.0)
            val lexicalScore = (lexicalScores[row.id] ?: 0.0) / maxLexical
            // Do not return arbitrary chunks merely because cosine similarity has a 0.5 baseline.
            if (semanticScore < 0.53 && lexicalScore == 0.0) return@mapNotNull null
            val combined = 0.65 * semanticScore + 0.35 * lexicalScore
            val chunk = KnowledgeChunk(row.source, row.chunkIndex, row.text, row.pageNumber)
            RetrievedChunk(chunk, combined)
        }.sortedByDescending { it.score }.take(limit)
    }

    suspend fun contextFor(query: String, limit: Int = 5): String =
        search(query, limit).joinToString("\n\n") { result ->
            val page = result.chunk.pageNumber?.let { " · page $it" }.orEmpty()
            "[${result.chunk.source}$page · chunk ${result.chunk.index + 1}]\n${result.chunk.text}"
        }

    private data class TextChunk(val text: String, val pageNumber: Int?)

    private fun splitIntoChunks(input: String): List<TextChunk> {
        val normalized = input.replace("\r\n", "\n").replace('\r', '\n')
        val pagePattern = Regex("\\[Page (\\d+)]")
        val chunks = mutableListOf<TextChunk>()
        var currentPage: Int? = null
        val content = StringBuilder()
        fun flushPage() {
            val pageText = content.toString().replace(Regex("\\s+"), " ").trim()
            var start = 0
            while (start < pageText.length) {
                var end = (start + maxChunkChars).coerceAtMost(pageText.length)
                if (end < pageText.length) {
                    val boundary = pageText.lastIndexOf(' ', end)
                    if (boundary > start + maxChunkChars / 2) end = boundary
                }
                val part = pageText.substring(start, end).trim()
                if (part.isNotEmpty()) chunks += TextChunk(part, currentPage)
                if (end >= pageText.length) break
                start = (end - overlapChars).coerceAtLeast(start + 1)
            }
            content.clear()
        }
        normalized.lineSequence().forEach { line ->
            val marker = pagePattern.find(line)
            if (marker != null) {
                flushPage()
                currentPage = marker.groupValues[1].toIntOrNull()
                content.append(line.substring(marker.range.last + 1)).append(' ')
            } else {
                content.append(line).append(' ')
            }
        }
        flushPage()
        return chunks
    }

    private fun encode(vector: FloatArray): ByteArray {
        val buffer = ByteBuffer.allocate(vector.size * Float.SIZE_BYTES).order(ByteOrder.LITTLE_ENDIAN)
        vector.forEach { value ->
            require(value.isFinite()) { "Embedding contains a non-finite value." }
            buffer.putFloat(value)
        }
        return buffer.array()
    }

    private fun decode(bytes: ByteArray): FloatArray {
        require(bytes.size % Float.SIZE_BYTES == 0) { "Stored embedding is corrupt." }
        val buffer = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN)
        return FloatArray(bytes.size / Float.SIZE_BYTES) { buffer.float }
    }

    private fun stableId(modelId: String, scope: String, source: String, index: Int): String {
        val input = "$modelId\u0000$scope\u0000$source\u0000$index".toByteArray(Charsets.UTF_8)
        return MessageDigest.getInstance("SHA-256").digest(input).joinToString("") { "%02x".format(it.toInt() and 0xff) }
    }
}
