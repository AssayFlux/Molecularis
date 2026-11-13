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
import java.security.MessageDigest
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

        val reader = OfflineDocumentReader(applicationContext)
        try {
            setForeground(getForegroundInfo())
            var checkpoint = db.bookDao().processingCheckpoint(id)
            if (checkpoint == null) {
                val stageId = "__stage__" + id
                db.withTransaction {
                    if (db.bookDao().book(stageId) == null) db.bookDao().addBook(book.copy(id = stageId))
                    checkpoint = KnowledgeProcessingCheckpointEntity(id, stageId, 1, 0, 0)
                    db.bookDao().saveProcessingCheckpoint(checkpoint!!)
                }
            }

            val active = checkpoint!!
            val stageId = active.stagingBookId
            var totalChars = active.extractedChars
            var totalPassages = active.passageCount

            val summary = reader.readPdfPages(
                uri = Uri.fromFile(source),
                maxPdfPages = 5_000,
                startPage = active.nextPage
            ) { page, total, text ->
                currentCoroutineContext().ensureActive()
                val updatedChars = totalChars + text.length
                require(updatedChars <= MAX_CHARS) { "The 25 million character safety limit was reached." }
                val pagePassages = chunks(text).mapIndexed { index, chunk ->
                    BookPassageEntity(UUID.randomUUID().toString(), stageId, index, page, chunk)
                }
                val normalizedPage = text.lowercase().replace(Regex("\\s+"), " ").trim()
                val fingerprint = sha256(normalizedPage)
                val duplicatePage = normalizedPage.isNotBlank() && db.bookDao().pageFingerprintCount(stageId, fingerprint) > 0
                val pageAudit = KnowledgePageAuditEntity(
                    stagingBookId = stageId,
                    pageNumber = page,
                    charCount = text.trim().length,
                    fingerprint = fingerprint,
                    qualityFlag = when {
                        normalizedPage.isBlank() -> "empty"
                        duplicatePage -> "duplicate"
                        text.trim().length < 50 -> "short"
                        else -> "ok"
                    }
                )
                val nextCheckpoint = KnowledgeProcessingCheckpointEntity(
                    bookId = id,
                    stagingBookId = stageId,
                    nextPage = page + 1,
                    extractedChars = updatedChars,
                    passageCount = totalPassages + pagePassages.size
                )
                // A page's passages and the next-page cursor commit together. If the process
                // dies before commit, that page is OCRed again; it cannot be silently skipped.
                db.withTransaction {
                    if (pagePassages.isNotEmpty()) db.bookDao().addPassages(pagePassages)
                    db.bookDao().savePageAudit(pageAudit)
                    db.bookDao().saveProcessingCheckpoint(nextCheckpoint)
                }
                totalChars = updatedChars
                totalPassages = nextCheckpoint.passageCount
                setProgress(workDataOf("page" to page, "total" to total, "passages" to totalPassages))
            }

            require(totalChars > 0) { "No readable text was extracted." }
            val knowledgeId = db.knowledgePoolDao().forBook(id)?.id ?: UUID.randomUUID().toString()
            val candidates = linkedMapOf<String, Pair<Int, Pair<Float, String>>>()
            db.bookDao().passages(stageId).forEach { passage ->
                headings(passage.text).forEach { (name, confidence, evidence) ->
                    val key = name.lowercase().replace(Regex("\\s+"), " ").trim()
                    if (key.length >= 4 && key !in candidates) {
                        candidates[key] = passage.pageNumber to (confidence to evidence)
                    }
                }
            }
            val topics = candidates.entries.sortedBy { it.value.first }.take(120).map { (name, info) ->
                KnowledgeTopicEntity(UUID.randomUUID().toString(), knowledgeId, name, info.first, info.second.first, info.second.second)
            }
            val audits = db.bookDao().pageAudits(stageId)
            val pagesWithText = audits.count { it.charCount > 0 }
            val emptyPages = audits.count { it.charCount == 0 }
            val shortTextPages = audits.count { it.charCount in 1..49 }
            val duplicatePages = audits.count { it.qualityFlag == "duplicate" }
            val coverageScore = (pagesWithText * 40 / summary.pageCount.coerceAtLeast(1))
            val duplicatePenalty = (duplicatePages * 2).coerceAtMost(20)
            val quality = (coverageScore + (if (totalPassages > 0) 30 else 0) +
                (if (topics.isNotEmpty()) 10 else 0) - duplicatePenalty).coerceIn(0, 100)
            val metadata = KnowledgeBookEntity(
                id = knowledgeId,
                bookId = id,
                detectedTitle = book.title,
                author = "",
                publisher = "",
                edition = "",
                subject = "Needs subject review",
                summary = "Offline OCR extracted " + totalChars + " characters from " + summary.pageCount +
                    " pages and indexed " + totalPassages + " page-linked passages. Page audit: " +
                    pagesWithText + " with text, " + emptyPages + " empty, " + shortTextPages +
                    " short, " + duplicatePages + " repeated OCR pages. Readiness is heuristic, not a scientific accuracy score.",
                chapterOutline = topics.joinToString("\\n") { it.startPage.toString() + ". " + it.name },
                extractedPageCount = summary.pageCount,
                extractedChars = totalChars,
                passageCount = totalPassages,
                topicCount = topics.size,
                qualityScore = quality,
                reviewState = "needs_review",
                pagesWithText = pagesWithText,
                emptyPages = emptyPages,
                shortTextPages = shortTextPages,
                duplicatePages = duplicatePages
            )
            db.withTransaction {
                db.bookDao().replacePassagesFromStage(id, stageId)
                db.bookDao().deletePageAudits(id)
                db.bookDao().movePageAudits(stageId, id)
                db.bookDao().updateBookStats(id, summary.pageCount, totalChars)
                db.knowledgePoolDao().saveBook(metadata)
                db.knowledgePoolDao().clearTopics(knowledgeId)
                db.knowledgePoolDao().saveTopics(topics)
                db.bookDao().deleteProcessingCheckpoint(id)
            }
            return Result.success(workDataOf("bookId" to id, "passages" to totalPassages))
        } catch (cancelled: kotlinx.coroutines.CancellationException) {
            throw cancelled
        } catch (error: Exception) {
            // Keep the staging passages and last committed page cursor for recovery/retry.
            return if (error is IllegalArgumentException || runAttemptCount >= MAX_RETRIES)
                Result.failure(workDataOf("error" to (error.message ?: error.javaClass.simpleName)))
            else Result.retry()
        } finally {
            reader.close()
        }
    }

    companion object {
        const val KEY_BOOK_ID = "book_id"
        private const val CHANNEL = "molecularis_knowledge"
        private const val NOTIFICATION_ID = 4107
        private const val MAX_CHARS = 25_000_000
        private const val MAX_RETRIES = 3
    }
}

private fun sha256(value: String): String {
    val digest = MessageDigest.getInstance("SHA-256").digest(value.toByteArray(Charsets.UTF_8))
    return digest.joinToString("") { "%02x".format(it) }
}

private fun chunks(text: String): List<String> {
    val normalized = text.replace(Regex("\\s+"), " ").trim()
    if (normalized.isBlank()) return emptyList()
    val result = mutableListOf<String>()
    var start = 0
    while (start < normalized.length) {
        var end = (start + 1_100).coerceAtMost(normalized.length)
        if (end < normalized.length) {
            val boundary = normalized.lastIndexOf(' ', end)
            if (boundary > start + 550) end = boundary
        }
        result += normalized.substring(start, end).trim()
        if (end == normalized.length) break
        start = end
    }
    return result
}

private fun headings(text: String): List<Triple<String, Float, String>> =
    text.lineSequence().map { it.trim().replace(Regex("\\s+"), " ") }
        .filter { it.length in 5..110 }
        .mapNotNull { line ->
            val match = Regex("(?i)^(chapter|unit|part)\\s+[0-9ivx]+\\b[:.\\- ]*(.{2,90})$").find(line)
            match?.let { Triple(it.groupValues[2].trim().ifBlank { line }, 0.88f, line) }
        }.toList()
