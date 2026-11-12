package org.molecularis.app.features

import ai.onnxruntime.OnnxTensor
import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import java.io.File
import java.nio.LongBuffer
import java.util.Locale
import kotlin.math.sqrt

/**
 * Local sentence embedding provider for MiniLM-style WordPiece ONNX exports.
 *
 * Expected inputs: input_ids and attention_mask (int64), with optional token_type_ids.
 * Expected output: token embeddings [1, sequence, dimensions] or pooled [1, dimensions].
 * The model and vocab are user-supplied local files; this class never downloads or uploads data.
 */
interface LocalEmbeddingProvider : AutoCloseable {
    val modelId: String
    val dimensions: Int
    fun embed(text: String): FloatArray
}

class OnnxWordPieceEmbedder(
    modelFile: File,
    vocabFile: File,
    override val modelId: String,
    private val maxSequenceLength: Int = 128
) : LocalEmbeddingProvider {
    private val environment = OrtEnvironment.getEnvironment()
    private val session: OrtSession
    private val vocabulary: Map<String, Int>
    private val unknownId: Int
    private val clsId: Int
    private val sepId: Int
    private val padId: Int
    override val dimensions: Int

    init {
        require(modelFile.isFile && modelFile.length() > 0L) { "Embedding ONNX model is missing or empty." }
        require(vocabFile.isFile && vocabFile.length() > 0L) { "WordPiece vocab.txt is missing or empty." }
        require(maxSequenceLength in 8..512) { "Sequence length must be between 8 and 512." }
        vocabulary = vocabFile.readLines(Charsets.UTF_8).mapIndexed { index, token -> token.trim() to index }
            .filter { it.first.isNotEmpty() }.toMap()
        unknownId = vocabulary["[UNK]"] ?: error("vocab.txt must contain [UNK].")
        clsId = vocabulary["[CLS]"] ?: error("vocab.txt must contain [CLS].")
        sepId = vocabulary["[SEP]"] ?: error("vocab.txt must contain [SEP].")
        padId = vocabulary["[PAD]"] ?: 0
        val options = OrtSession.SessionOptions()
        session = try { environment.createSession(modelFile.absolutePath, options) }
        finally { options.close() }
        val names = session.inputNames.map { it.lowercase(Locale.ROOT) }.toSet()
        require("input_ids" in names && "attention_mask" in names) {
            "Unsupported embedding model: expected input_ids and attention_mask."
        }
        dimensions = inferDimensions()
    }

    override fun embed(text: String): FloatArray {
        require(text.isNotBlank()) { "Cannot embed blank text." }
        val tokens = tokenize(text).take(maxSequenceLength - 2)
        val ids = LongArray(maxSequenceLength) { padId.toLong() }
        val mask = LongArray(maxSequenceLength)
        ids[0] = clsId.toLong()
        tokens.forEachIndexed { index, id -> ids[index + 1] = id.toLong() }
        ids[tokens.size + 1] = sepId.toLong()
        for (index in 0..tokens.size + 1) mask[index] = 1L

        val tensors = mutableListOf<OnnxTensor>()
        try {
            val inputs = linkedMapOf<String, OnnxTensor>()
            fun tensor(values: LongArray): OnnxTensor =
                OnnxTensor.createTensor(environment, LongBuffer.wrap(values), longArrayOf(1, values.size.toLong()))
                    .also(tensors::add)
            session.inputNames.forEach { name ->
                when (name.lowercase(Locale.ROOT)) {
                    "input_ids" -> inputs[name] = tensor(ids)
                    "attention_mask" -> inputs[name] = tensor(mask)
                    "token_type_ids" -> inputs[name] = tensor(LongArray(maxSequenceLength))
                }
            }
            session.run(inputs).use { result ->
                val output = result[0].value
                val vector = when (output) {
                    is Array<*> -> {
                        val first = output.firstOrNull() ?: error("Embedding model returned an empty tensor.")
                        when (first) {
                            is Array<*> -> {
                                val rows = first.map { it as? FloatArray ?: error("Expected float token embeddings.") }
                                meanPool(rows, mask)
                            }
                            is FloatArray -> first.copyOf()
                            else -> error("Unsupported embedding output tensor.")
                        }
                    }
                    else -> error("Unsupported embedding output tensor.")
                }
                require(vector.size == dimensions) { "Embedding output dimension changed unexpectedly." }
                return normalize(vector)
            }
        } finally {
            tensors.forEach { runCatching { it.close() } }
        }
    }

    private fun inferDimensions(): Int {
        val sampleIds = LongArray(maxSequenceLength) { padId.toLong() }.also {
            it[0] = clsId.toLong(); it[1] = sepId.toLong()
        }
        val mask = LongArray(maxSequenceLength).also { it[0] = 1L; it[1] = 1L }
        val tensors = mutableListOf<OnnxTensor>()
        try {
            val inputs = linkedMapOf<String, OnnxTensor>()
            fun tensor(values: LongArray) = OnnxTensor.createTensor(
                environment, LongBuffer.wrap(values), longArrayOf(1, values.size.toLong())
            ).also(tensors::add)
            session.inputNames.forEach { name ->
                when (name.lowercase(Locale.ROOT)) {
                    "input_ids" -> inputs[name] = tensor(sampleIds)
                    "attention_mask" -> inputs[name] = tensor(mask)
                    "token_type_ids" -> inputs[name] = tensor(LongArray(maxSequenceLength))
                }
            }
            session.run(inputs).use { result ->
                val value = result[0].value as? Array<*> ?: error("Expected rank-2 or rank-3 float output.")
                val first = value.firstOrNull() ?: error("Empty model output.")
                return when (first) {
                    is Array<*> -> (first.firstOrNull() as? FloatArray)?.size
                        ?: error("Unsupported token embedding output.")
                    is FloatArray -> first.size
                    else -> error("Unsupported embedding output.")
                }
            }
        } finally {
            tensors.forEach { runCatching { it.close() } }
        }
    }

    private fun meanPool(rows: List<FloatArray>, mask: LongArray): FloatArray {
        require(rows.isNotEmpty()) { "Embedding model returned no token vectors." }
        val result = FloatArray(rows.first().size)
        var count = 0
        rows.take(mask.size).forEachIndexed { index, row ->
            if (mask[index] == 1L) {
                require(row.size == result.size) { "Inconsistent token embedding dimensions." }
                for (dimension in row.indices) result[dimension] += row[dimension]
                count++
            }
        }
        require(count > 0) { "No unmasked tokens were returned." }
        for (dimension in result.indices) result[dimension] /= count
        return result
    }

    private fun tokenize(text: String): List<Int> {
        val basicTokens = Regex("[\\p{L}\\p{N}]+|[^\\s\\p{L}\\p{N}]")
            .findAll(text.lowercase(Locale.ROOT)).map { it.value }
        val result = mutableListOf<Int>()
        basicTokens.forEach { token ->
            if (token in vocabulary) {
                result += vocabulary.getValue(token)
            } else {
                var start = 0
                val pieces = mutableListOf<Int>()
                var failed = false
                while (start < token.length) {
                    var end = token.length
                    var found: Int? = null
                    while (end > start) {
                        val piece = (if (start == 0) "" else "##") + token.substring(start, end)
                        val id = vocabulary[piece]
                        if (id != null) { found = id; break }
                        end--
                    }
                    if (found == null) { failed = true; break }
                    pieces += found
                    start = end
                }
                if (failed) result += unknownId else result += pieces
            }
        }
        return result
    }

    private fun normalize(vector: FloatArray): FloatArray {
        val norm = sqrt(vector.sumOf { (it * it).toDouble() }).toFloat()
        if (norm <= 1e-12f) return vector
        return FloatArray(vector.size) { vector[it] / norm }
    }

    override fun close() { session.close() }
}

/** Cosine similarity for already-normalized or arbitrary finite vectors. */
fun cosineSimilarity(left: FloatArray, right: FloatArray): Double {
    require(left.isNotEmpty() && left.size == right.size) { "Embedding dimensions must match and be non-empty." }
    var dot = 0.0
    var leftNorm = 0.0
    var rightNorm = 0.0
    for (index in left.indices) {
        val a = left[index].toDouble()
        val b = right[index].toDouble()
        require(a.isFinite() && b.isFinite()) { "Embedding contains a non-finite value." }
        dot += a * b
        leftNorm += a * a
        rightNorm += b * b
    }
    if (leftNorm == 0.0 || rightNorm == 0.0) return 0.0
    return (dot / (sqrt(leftNorm) * sqrt(rightNorm))).coerceIn(-1.0, 1.0)
}
