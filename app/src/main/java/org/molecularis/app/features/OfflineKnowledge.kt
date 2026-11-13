package org.molecularis.app.features

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.pdf.PdfRenderer
import android.net.Uri
import android.os.ParcelFileDescriptor
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.util.Locale
import kotlin.math.min

/** Offline OCR and text extraction. PDF pages are rasterized locally and passed to on-device ML Kit OCR. */
class OfflineDocumentReader(private val context: Context) {
    private val recognizer by lazy { TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS) }

    suspend fun read(uri: Uri, mimeType: String?, maxPdfPages: Int = 40, displayName: String? = null): String = withContext(Dispatchers.IO) {
        val name = (displayName ?: uri.lastPathSegment).orEmpty().lowercase(Locale.ROOT)
        val isImage = mimeType?.startsWith("image/") == true || listOf(".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif").any(name::endsWith)
        val extracted = when {
            mimeType == "application/pdf" || name.endsWith(".pdf") -> readPdf(uri, maxPdfPages)
            isImage -> readImage(uri)
            name.endsWith(".docx") || mimeType == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" -> readDocx(uri)
            mimeType?.startsWith("text/") == true || listOf(".txt", ".md", ".csv", ".json", ".xml", ".log").any(name::endsWith) -> readText(uri)
            else -> error("Unsupported attachment type. Choose PDF, image, DOCX, or a text file.")
        }
        if (!isImage) require(extracted.isNotBlank()) { "No readable text was found in this document." }
        extracted
    }

    private suspend fun readImage(uri: Uri): String {
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        context.contentResolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, bounds) }
        require(bounds.outWidth > 0 && bounds.outHeight > 0) { "Cannot decode the selected image" }
        var sample = 1
        while (bounds.outWidth / sample > 2048 || bounds.outHeight / sample > 2048) sample *= 2
        val bitmap = context.contentResolver.openInputStream(uri)?.use {
            BitmapFactory.decodeStream(it, null, BitmapFactory.Options().apply { inSampleSize = sample })
        } ?: error("Cannot decode the selected image")
        return try { recognizer.process(InputImage.fromBitmap(bitmap, 0)).await().text }
        finally { bitmap.recycle() }
    }

    /**
     * OCR a large PDF one page at a time so the caller can persist bounded batches instead of
     * holding an entire 5,000-page textbook and all of its chunks in memory.
     */
    suspend fun readPdfPages(
        uri: Uri,
        maxPdfPages: Int,
        startPage: Int = 1,
        onPage: suspend (pageNumber: Int, totalPages: Int, text: String) -> Unit
    ): PdfExtractionSummary = withContext(Dispatchers.IO) {
        require(maxPdfPages in 1..5_000) { "PDF import limit must be between 1 and 5,000 pages." }
        val pfd = context.contentResolver.openFileDescriptor(uri, "r") ?: error("Cannot open PDF")
        pfd.use { descriptor ->
            PdfRenderer(descriptor).use { pdf ->
                require(pdf.pageCount <= maxPdfPages) {
                    "PDF has ${pdf.pageCount} pages; limit is $maxPdfPages pages per import."
                }
                require(startPage in 1..(pdf.pageCount + 1)) { "Resume page is outside this PDF." }
                var extractedChars = 0
                for (index in (startPage - 1) until pdf.pageCount) {
                    val pageText = pdf.openPage(index).use { page ->
                        val scale = min(2.0, 1800.0 / maxOf(page.width, page.height)).toFloat()
                        val bitmap = Bitmap.createBitmap(
                            (page.width * scale).toInt().coerceAtLeast(1),
                            (page.height * scale).toInt().coerceAtLeast(1),
                            Bitmap.Config.ARGB_8888
                        )
                        try {
                            page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                            recognizer.process(InputImage.fromBitmap(bitmap, 0)).await().text
                        } finally {
                            bitmap.recycle()
                        }
                    }
                    extractedChars += pageText.length
                    onPage(index + 1, pdf.pageCount, pageText)
                }
                PdfExtractionSummary(pdf.pageCount, extractedChars)
            }
        }
    }

    private suspend fun readPdf(uri: Uri, maxPages: Int): String {
        val pfd = context.contentResolver.openFileDescriptor(uri, "r") ?: error("Cannot open PDF")
        return pfd.use { descriptor ->
            PdfRenderer(descriptor).use { pdf ->
                require(pdf.pageCount <= maxPages) { "PDF has ${pdf.pageCount} pages; limit is $maxPages pages per import." }
                buildString {
                    for (index in 0 until pdf.pageCount) {
                        pdf.openPage(index).use { page ->
                            val scale = min(2.0, 1800.0 / maxOf(page.width, page.height)).toFloat()
                            val bitmap = Bitmap.createBitmap((page.width * scale).toInt().coerceAtLeast(1), (page.height * scale).toInt().coerceAtLeast(1), Bitmap.Config.ARGB_8888)
                            try {
                                page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                                val text = recognizer.process(InputImage.fromBitmap(bitmap, 0)).await().text
                                if (text.isNotBlank()) append("\n\n[Page ${index + 1}]\n").append(text)
                            } finally { bitmap.recycle() }
                        }
                    }
                }
            }
        }
    }

    private fun readText(uri: Uri): String = context.contentResolver.openInputStream(uri)?.use { input ->
        BufferedReader(InputStreamReader(input, Charsets.UTF_8)).use { it.readBounded(2_000_000) }
    } ?: error("Cannot open document")

    private fun readDocx(uri: Uri): String {
        val input = context.contentResolver.openInputStream(uri) ?: error("Cannot open DOCX")
        return input.use { stream ->
            java.util.zip.ZipInputStream(stream).use { zip ->
                var entry = zip.nextEntry
                while (entry != null && entry.name != "word/document.xml") entry = zip.nextEntry
                require(entry != null) { "DOCX document.xml is missing" }
                val xml = zip.bufferedReader(Charsets.UTF_8).use { it.readBounded(2_000_000) }
                val factory = javax.xml.parsers.DocumentBuilderFactory.newInstance().apply {
                    setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
                    setFeature("http://xml.org/sax/features/external-general-entities", false)
                    setFeature("http://xml.org/sax/features/external-parameter-entities", false)
                    runCatching { setAttribute("http://javax.xml.XMLConstants/property/accessExternalDTD", "") }
                    runCatching { setAttribute("http://javax.xml.XMLConstants/property/accessExternalSchema", "") }
                }
                val document = factory.newDocumentBuilder().parse(org.xml.sax.InputSource(java.io.StringReader(xml)))
                val nodes = document.getElementsByTagName("w:t")
                (0 until nodes.length).joinToString(" ") { nodes.item(it).textContent }
            }
        }
    }

    fun close() { recognizer.close() }
}

private fun BufferedReader.readBounded(maxChars: Int): String {
    val out = StringBuilder()
    val buffer = CharArray(8192)
    while (out.length < maxChars) {
        val count = read(buffer, 0, min(buffer.size, maxChars - out.length))
        if (count < 0) break
        out.append(buffer, 0, count)
    }
    return out.toString()
}

data class PdfExtractionSummary(val pageCount: Int, val extractedChars: Int)

data class KnowledgeChunk(val source: String, val index: Int, val text: String, val pageNumber: Int? = null)
data class RetrievedChunk(val chunk: KnowledgeChunk, val score: Double)

/** Small, deterministic, on-device retrieval index. No embeddings or network calls are implied. */
class LocalRagIndex(private val maxChunkChars: Int = 900, private val overlap: Int = 120) {
    init {
        require(maxChunkChars >= 32) { "Chunk size must be at least 32 characters." }
        require(overlap in 0 until maxChunkChars) { "Overlap must be smaller than chunk size." }
    }
    private val chunks = mutableListOf<KnowledgeChunk>()

    @Synchronized fun add(source: String, text: String) {
        require(source.isNotBlank() && text.isNotBlank())
        val normalized = text.replace(Regex("\\s+"), " ").trim()
        var start = 0
        var index = 0
        while (start < normalized.length) {
            val end = min(start + maxChunkChars, normalized.length)
            chunks += KnowledgeChunk(source, index++, normalized.substring(start, end))
            if (end == normalized.length) break
            start = (end - overlap).coerceAtLeast(start + 1)
        }
    }

    /**
     * Offline BM25 lexical retrieval. This is stronger than raw term-frequency ranking,
     * but deliberately does not claim semantic/embedding search.
     */
    @Synchronized fun search(query: String, limit: Int = 5): List<RetrievedChunk> {
        require(limit in 1..100) { "Retrieval limit must be between 1 and 100." }
        val terms = tokenize(query).toSet()
        if (terms.isEmpty() || chunks.isEmpty()) return emptyList()

        val tokenized = chunks.map { tokenize(it.text) }
        val averageLength = tokenized.sumOf { it.size }.toDouble() / tokenized.size.coerceAtLeast(1)
        val documentFrequency = terms.associateWith { term ->
            tokenized.count { words -> term in words }
        }
        val k1 = 1.2
        val b = 0.75

        return chunks.mapIndexed { index, chunk ->
            val words = tokenized[index]
            val counts = words.groupingBy { it }.eachCount()
            val lengthNorm = if (averageLength > 0.0) words.size / averageLength else 0.0
            val score = terms.sumOf { term ->
                val frequency = counts[term] ?: 0
                if (frequency == 0) 0.0 else {
                    val df = documentFrequency[term] ?: 0
                    val inverseDocumentFrequency = kotlin.math.ln(
                        1.0 + (chunks.size - df + 0.5) / (df + 0.5)
                    )
                    inverseDocumentFrequency * (frequency * (k1 + 1.0)) /
                        (frequency + k1 * (1.0 - b + b * lengthNorm))
                }
            }
            RetrievedChunk(chunk, score)
        }.filter { it.score > 0.0 }.sortedByDescending { it.score }.take(limit)
    }

    @Synchronized fun contextFor(query: String, limit: Int = 5): String {
        val matches = search(query, limit)
        val selected = if (matches.isNotEmpty()) matches else chunks.take(limit).map { RetrievedChunk(it, 0.0) }
        return selected.joinToString("\n\n") { "[${it.chunk.source} · chunk ${it.chunk.index + 1}]\n${it.chunk.text}" }
    }

    @Synchronized fun clear() = chunks.clear()
    @Synchronized fun size() = chunks.size

    private fun tokenize(value: String) = Regex("[\\p{L}\\p{N}]{2,}").findAll(value.lowercase(Locale.ROOT)).map { it.value }.toList()
}

data class DatasetReport(val validRecords: Int, val invalidLines: List<Int>, val trainRecords: Int, val validationRecords: Int)

/** Validates JSONL examples and produces deterministic train/validation counts; it does not train weights. */
object OfflineDatasetInspector {
    fun inspect(jsonl: String, validationFraction: Double = 0.1): DatasetReport {
        require(validationFraction in 0.05..0.3)
        val invalid = mutableListOf<Int>()
        var valid = 0
        jsonl.lineSequence().forEachIndexed { index, line ->
            if (line.isBlank()) return@forEachIndexed
            try {
                val obj = JSONObject(line)
                val hasText = obj.optString("text").isNotBlank() || obj.optString("prompt").isNotBlank() ||
                    (obj.optJSONArray("messages")?.length() ?: 0) > 0
                require(hasText) { "Expected text, prompt, or messages" }
                valid++
            } catch (_: Exception) { invalid += index + 1 }
        }
        val validation = if (valid > 1) (valid * validationFraction).toInt().coerceAtLeast(1) else 0
        return DatasetReport(valid, invalid, valid - validation, validation)
    }
}
