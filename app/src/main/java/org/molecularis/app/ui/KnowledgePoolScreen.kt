package org.molecularis.app.ui

import android.net.Uri
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Analytics
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.molecularis.app.data.*
import org.molecularis.app.features.OfflineDocumentReader
import java.io.File
import java.util.UUID

private const val KNOWLEDGE_MAX_CHARS = 25_000_000

@Composable
fun KnowledgePoolScreen(database: AppDatabase) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val library by database.bookDao().books().collectAsState(initial = emptyList())
    val pool by database.knowledgePoolDao().books().collectAsState(initial = emptyList())
    var status by remember { mutableStateOf("Your source books stay unchanged in Library. Process a copy into structured knowledge here.") }
    var processingId by remember { mutableStateOf<String?>(null) }
    var selected by remember { mutableStateOf<KnowledgeBookEntity?>(null) }
    var topics by remember { mutableStateOf(emptyList<KnowledgeTopicEntity>()) }

    LaunchedEffect(selected?.id) {
        topics = selected?.let { database.knowledgePoolDao().topics(it.id) }.orEmpty()
    }

    fun processBook(book: BookEntity) {
        if (processingId != null) return
        processingId = book.id
        status = "Preparing source analysis for ${book.title}…"
        scope.launch {
            var chars = 0
            var passageCount = 0
            var pending = mutableListOf<BookPassageEntity>()
            val pageSamples = mutableListOf<Pair<Int, String>>()
            val candidates = linkedMapOf<String, Pair<Int, Pair<Float, String>>>()
            val reader = OfflineDocumentReader(context)
            try {
                require(File(book.localPath).isFile) { "The original PDF is missing from local storage." }
                database.bookDao().deletePassages(book.id)
                val summary = try {
                    reader.readPdfPages(Uri.fromFile(File(book.localPath)), maxPdfPages = 5_000) { page, total, text ->
                        chars += text.length
                        require(chars <= KNOWLEDGE_MAX_CHARS) { "The 25 million character processing safety limit was reached." }
                        if (page <= 18 && text.isNotBlank()) pageSamples += page to text.take(4_000)
                        val chunks = knowledgeChunks(text)
                        chunks.forEachIndexed { index, chunk ->
                            pending += BookPassageEntity(UUID.randomUUID().toString(), book.id, index, page, chunk)
                            if (pending.size >= 250) {
                                database.bookDao().addPassages(pending)
                                passageCount += pending.size
                                pending = mutableListOf()
                            }
                        }
                        detectChapterHeadings(text).forEach { (heading, confidence, evidence) ->
                            val key = heading.lowercase().replace(Regex("\\s+"), " ").trim()
                            if (key.length >= 4 && key !in candidates) candidates[key] = heading to (page to (confidence to evidence))
                        }
                        if (page % 10 == 0 || page == total) {
                            status = "Analysing page $page of $total · $passageCount passages indexed · ${candidates.size} topic candidates"
                        }
                    }
                } finally {
                    reader.close()
                }
                if (pending.isNotEmpty()) {
                    database.bookDao().addPassages(pending)
                    passageCount += pending.size
                }
                require(summary.extractedChars > 0) { "No readable text was extracted. Check the PDF quality or OCR language." }
                database.bookDao().updateBookStats(book.id, summary.pageCount, summary.extractedChars)

                val opening = pageSamples.sortedBy { it.first }.joinToString("\\n") { it.second }
                val detectedTitle = opening.lineSequence().map { it.trim() }.firstOrNull { it.length in 5..140 && !it.contains("copyright", true) } ?: book.title
                val author = Regex("(?im)^(?:by|author[s]?:)\\s*(.{3,100})$").find(opening)?.groupValues?.get(1)?.trim().orEmpty()
                val publisher = Regex("(?im)^.{0,30}(?:publishers?|press)\\s*$").find(opening)?.value?.trim().orEmpty()
                val edition = Regex("(?i)(\\d{1,2}(?:st|nd|rd|th)\\s+edition|edition\\s*[:#]?\\s*\\d{1,2})").find(opening)?.value.orEmpty()
                val subject = if (("$detectedTitle $opening").contains("biochem", true)) "Biochemistry" else "Needs subject review"
                val chapters = candidates.values.sortedBy { it.second.first }.take(120)
                val outline = chapters.joinToString("\\n") { "${it.second.first}. ${it.first} [confidence ${"%.2f".format(java.util.Locale.US, it.second.second.first)}]" }
                val pagesWithText = pageSamples.size.coerceAtMost(summary.pageCount)
                val pageCoverage = if (summary.pageCount > 0) summary.extractedChars.toDouble() / summary.pageCount else 0.0
                val score = ((if (passageCount > 0) 35 else 0) + (if (chapters.isNotEmpty()) 25 else 0) +
                    (if (author.isNotBlank()) 10 else 0) + (if (edition.isNotBlank()) 5 else 0) +
                    (if (pagesWithText > 0) 15 else 0) + (if (pageCoverage > 500) 10 else 0)).coerceIn(0, 100)
                val knowledgeId = database.knowledgePoolDao().forBook(book.id)?.id ?: UUID.randomUUID().toString()
                database.knowledgePoolDao().saveBook(
                    KnowledgeBookEntity(
                        id = knowledgeId, bookId = book.id, detectedTitle = detectedTitle,
                        author = author, publisher = publisher, edition = edition, subject = subject,
                        summary = "Extracted ${summary.pageCount} pages into $passageCount source-linked passages. ${chapters.size} possible chapter/topic headings were detected. Review metadata and headings before using them as teaching structure.",
                        chapterOutline = outline, extractedPageCount = summary.pageCount,
                        extractedChars = summary.extractedChars, passageCount = passageCount,
                        topicCount = chapters.size, qualityScore = score, reviewState = "needs_review"
                    )
                )
                database.knowledgePoolDao().clearTopics(knowledgeId)
                database.knowledgePoolDao().saveTopics(chapters.map { (name, info) ->
                    KnowledgeTopicEntity(
                        id = UUID.randomUUID().toString(), knowledgeBookId = knowledgeId,
                        name = name, startPage = info.first, confidence = info.second.first,
                        evidence = info.second.second
                    )
                })
                status = "Knowledge preparation complete for ${book.title}. Review extracted metadata and approve topic candidates before generating teaching material."
            } catch (cancelled: CancellationException) {
                withContext(NonCancellable) {
                    runCatching { database.bookDao().deletePassages(book.id) }
                    runCatching { database.knowledgePoolDao().deleteForBook(book.id) }
                }
                throw cancelled
            } catch (error: Exception) {
                status = "Analysis failed for ${book.title}: ${error.message ?: error.javaClass.simpleName}"
            } finally {
                processingId = null
            }
        }
    }

    Column(Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("Knowledge Pool", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text("A reviewed, source-linked knowledge workspace built from your Library. Extraction is not model training: Molecularis analyses and organizes content first, then uses approved material as evidence for teaching.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            KnowledgeMetric("Library", library.size.toString(), Modifier.weight(1f))
            KnowledgeMetric("Analysed", pool.size.toString(), Modifier.weight(1f))
            KnowledgeMetric("Needs review", pool.count { it.reviewState != "approved" }.toString(), Modifier.weight(1f))
        }
        if (status.isNotBlank()) Text(status, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
        if (processingId != null) LinearProgressIndicator(Modifier.fillMaxWidth())
        if (selected != null) {
            TextButton(onClick = { selected = null }) { Text("← All knowledge sources") }
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(selected!!.detectedTitle, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
                    Text(listOf(selected!!.author, selected!!.edition, selected!!.publisher).filter { it.isNotBlank() }.joinToString(" · ").ifBlank { "Bibliographic details need review" }, style = MaterialTheme.typography.bodySmall)
                    Text("Subject: ${selected!!.subject}", style = MaterialTheme.typography.bodySmall)
                    Text("Quality readiness: ${selected!!.qualityScore}/100 · ${selected!!.reviewState.replace('_', ' ')}", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                    Text(selected!!.summary, style = MaterialTheme.typography.bodySmall)
                    Divider()
                    Text("Detected chapter / topic candidates", fontWeight = FontWeight.SemiBold)
                    if (topics.isEmpty()) Text("No reliable headings were detected. Add topics manually in a future review editor.", style = MaterialTheme.typography.bodySmall)
                    topics.forEach { topic ->
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Column(Modifier.weight(1f)) {
                                Text(topic.name, fontWeight = FontWeight.Medium)
                                Text("Page ${topic.startPage} · confidence ${"%.0f".format(topic.confidence * 100)}% · evidence: ${topic.evidence}", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            Checkbox(checked = topic.approved, onCheckedChange = { checked ->
                                scope.launch { database.knowledgePoolDao().setTopicApproved(topic.id, checked); topics = database.knowledgePoolDao().topics(selected!!.id) }
                            })
                        }
                    }
                }
            }
        } else {
            LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                item { Text("READY TO PROCESS", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold) }
                items(library, key = { it.id }) { book ->
                    val analysed = pool.firstOrNull { it.bookId == book.id }
                    Card(Modifier.fillMaxWidth()) {
                        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                Icon(Icons.Default.MenuBook, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                                Column(Modifier.weight(1f)) {
                                    Text(book.title, fontWeight = FontWeight.SemiBold)
                                    Text(if (analysed == null) "Original source · not analysed" else "${analysed.extractedPageCount} pages · ${analysed.passageCount} passages · ${analysed.topicCount} topic candidates", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                            }
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                Button(onClick = { processBook(book) }, enabled = processingId == null) {
                                    Icon(if (analysed == null) Icons.Default.PlayArrow else Icons.Default.Analytics, contentDescription = null)
                                    Spacer(Modifier.width(5.dp))
                                    Text(if (analysed == null) "Extract & analyse" else "Re-analyse")
                                }
                                if (analysed != null) OutlinedButton(onClick = { selected = analysed }) { Text("Review") }
                            }
                        }
                    }
                }
                if (library.isEmpty()) item { Text("Add original books in Library first. They will appear here for knowledge preparation.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                item {
                    Card(Modifier.fillMaxWidth()) {
                        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                            Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                            Text("Quality gates", fontWeight = FontWeight.SemiBold)
                            Text("Preserve book/page provenance · detect metadata conservatively · flag uncertain headings · review topics before teaching · never invent missing references. Model fine-tuning is a separate, opt-in workflow and is not performed by importing a book.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }
}

@Composable private fun KnowledgeMetric(label: String, value: String, modifier: Modifier = Modifier) {
    Card(modifier) { Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) { Text(value, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold); Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant) } }
}

private fun knowledgeChunks(text: String, maxChars: Int = 1_100): List<String> {
    val normalized = text.replace(Regex("\\s+"), " ").trim()
    if (normalized.isBlank()) return emptyList()
    val output = mutableListOf<String>()
    var start = 0
    while (start < normalized.length) {
        var end = (start + maxChars).coerceAtMost(normalized.length)
        if (end < normalized.length) {
            val boundary = normalized.lastIndexOf(' ', end)
            if (boundary > start + maxChars / 2) end = boundary
        }
        output += normalized.substring(start, end).trim()
        if (end >= normalized.length) break
        start = end
    }
    return output
}

private fun detectChapterHeadings(text: String): List<Triple<String, Float, String>> {
    val lines = text.lineSequence().map { it.trim().replace(Regex("\\s+"), " ") }
        .filter { it.length in 5..110 }.toList()
    val results = mutableListOf<Triple<String, Float, String>>()
    lines.forEach { line ->
        val chapter = Regex("(?i)^(chapter|unit|part)\\s+[0-9ivx]+\\b[:.\\- ]*(.{2,90})$").find(line)
        when {
            chapter != null -> {
                val title = chapter.groupValues[3].trim().ifBlank { line }
                results += Triple(title, 0.88f, line.take(180))
            }
            line.length <= 85 && line == line.uppercase() && line.any(Char::isLetter) &&
                line.count(Char::isLetter) >= 5 && !line.contains("COPYRIGHT") -> {
                results += Triple(line.lowercase().split(" ").joinToString(" ") { it.replaceFirstChar(Char::uppercase) }, 0.58f, line.take(180))
            }
        }
    }
    return results
}
