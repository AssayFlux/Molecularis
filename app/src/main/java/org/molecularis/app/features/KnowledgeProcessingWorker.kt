package org.molecularis.app.features

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.net.Uri
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.room.withTransaction
import androidx.work.CoroutineWorker
import androidx.work.ForegroundInfo
import androidx.work.WorkerParameters
import androidx.work.workDataOf
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.ensureActive
import org.molecularis.app.R
import org.molecularis.app.data.*
import java.io.File
import java.util.UUID

class KnowledgeProcessingWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {
    override suspend fun getForegroundInfo(): ForegroundInfo {
        val manager = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= 26) manager.createNotificationChannel(
            NotificationChannel(CHANNEL, "Knowledge processing", NotificationManager.IMPORTANCE_LOW)
        )
        val notification = NotificationCompat.Builder(applicationContext, CHANNEL)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle("Molecularis is preparing a textbook")
            .setContentText("Extracting pages and indexing references")
            .setOngoing(true).setOnlyAlertOnce(true).build()
        return if (Build.VERSION.SDK_INT >= 29)
            ForegroundInfo(NOTIFICATION_ID, notification, android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC)
        else ForegroundInfo(NOTIFICATION_ID, notification)
    }

    override suspend fun doWork(): Result {
        val id = inputData.getString(KEY_BOOK_ID) ?: return Result.failure()
        val db = DatabaseProvider.get(applicationContext)
        val book = db.bookDao().book(id) ?: return Result.failure()
        val source = File(book.localPath)
        if (!source.isFile) return Result.failure(workDataOf("error" to "Original PDF is missing"))
        val stageId = "__stage__" + UUID.randomUUID()
        var staged = false
        val reader = OfflineDocumentReader(applicationContext)
        try {
            setForeground(getForegroundInfo())
            db.bookDao().addBook(book.copy(id = stageId))
            staged = true
            var chars = 0
            var passages = 0
            val pending = mutableListOf<BookPassageEntity>()
            val candidates = linkedMapOf<String, Pair<Int, Pair<Float, String>>>()
            val summary = reader.readPdfPages(Uri.fromFile(source), 5_000) { page, total, text ->
                currentCoroutineContext().ensureActive()
                chars += text.length
                require(chars <= MAX_CHARS) { "The 25 million character safety limit was reached." }
                chunks(text).forEachIndexed { index, chunk ->
                    pending += BookPassageEntity(UUID.randomUUID().toString(), stageId, index, page, chunk)
                    if (pending.size >= 250) {
                        db.bookDao().addPassages(pending.toList())
                        passages += pending.size
                        pending.clear()
                    }
                }
                headings(text).forEach { (name, confidence, evidence) ->
                    val key = name.lowercase().replace(Regex("\\s+"), " ").trim()
                    if (key.length >= 4 && key !in candidates) candidates[key] = page to (confidence to evidence)
                }
                setProgress(workDataOf("page" to page, "total" to total, "passages" to passages))
            }
            if (pending.isNotEmpty()) {
                db.bookDao().addPassages(pending.toList())
                passages += pending.size
                pending.clear()
            }
            require(summary.extractedChars > 0) { "No readable text was extracted." }
            val knowledgeId = db.knowledgePoolDao().forBook(id)?.id ?: UUID.randomUUID().toString()
            val topics = candidates.entries.sortedBy { it.value.first }.take(120).map { (name, info) ->
                KnowledgeTopicEntity(UUID.randomUUID().toString(), knowledgeId, name, info.first, info.second.first, info.second.second)
            }
            val quality = ((if (passages > 0) 35 else 0) + if (topics.isNotEmpty()) 15 else 0 +
                (if (summary.extractedChars / summary.pageCount.coerceAtLeast(1) >= 300) 50 else 0)).coerceIn(0, 100)
            val metadata = KnowledgeBookEntity(
                id = knowledgeId, bookId = id, detectedTitle = book.title, author = "", publisher = "",
                edition = "", subject = "Needs subject review",
                summary = "Offline OCR extracted " + summary.extractedChars + " characters from " + summary.pageCount +
                    " pages and indexed " + passages + " page-linked passages. Readiness is heuristic, not a scientific accuracy score.",
                chapterOutline = topics.joinToString("\n") { it.startPage.toString() + ". " + it.name },
                extractedPageCount = summary.pageCount, extractedChars = summary.extractedChars,
                passageCount = passages, topicCount = topics.size, qualityScore = quality, reviewState = "needs_review"
            )
            db.withTransaction {
                db.bookDao().replacePassagesFromStage(id, stageId)
                db.bookDao().updateBookStats(id, summary.pageCount, summary.extractedChars)
                db.knowledgePoolDao().saveBook(metadata)
                db.knowledgePoolDao().clearTopics(knowledgeId)
                db.knowledgePoolDao().saveTopics(topics)
            }
            staged = false
            return Result.success(workDataOf("bookId" to id, "passages" to passages))
        } catch (cancelled: kotlinx.coroutines.CancellationException) {
            throw cancelled
        } catch (error: Exception) {
            return Result.failure(workDataOf("error" to (error.message ?: error.javaClass.simpleName)))
        } finally {
            reader.close()
            if (staged) runCatching { db.bookDao().deleteBook(stageId) }
        }
    }

    companion object {
        const val KEY_BOOK_ID = "book_id"
        private const val CHANNEL = "molecularis_knowledge"
        private const val NOTIFICATION_ID = 4107
        private const val MAX_CHARS = 25_000_000
    }
}

private fun chunks(text: String): List<String> {
    val normalized = text.replace(Regex("\\s+"), " ").trim()
    if (normalized.isBlank()) return emptyList()
    val result = mutableListOf<String>()
    var start = 0
    while (start < normalized.length) {
        val end = (start + 1_100).coerceAtMost(normalized.length)
        result += normalized.substring(start, end).trim()
        if (end == normalized.length) break
        start = end
    }
    return result
}

private fun headings(text: String): List<Triple<String, Float, String>> {
    val result = mutableListOf<Triple<String, Float, String>>()
    text.lineSequence().map { it.trim().replace(Regex("\\s+"), " ") }
        .filter { it.length in 5..110 }.forEach { line ->
            val match = Regex("(?i)^(chapter|unit|part)\\s+[0-9ivx]+\\b[:.\\- ]*(.{2,90})$").find(line)
            if (match != null) result += Triple(match.groupValues[2].trim().ifBlank { line }, 0.88f, line)
        }
    return result
}
