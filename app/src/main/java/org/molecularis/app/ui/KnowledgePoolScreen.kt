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
import java.security.MessageDigest

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
    var titleDraft by remember { mutableStateOf("") }
    var authorDraft by remember { mutableStateOf("") }
    var publisherDraft by remember { mutableStateOf("") }
    var editionDraft by remember { mutableStateOf("") }
    var subjectDraft by remember { mutableStateOf("") }

    LaunchedEffect(selected?.id) {
        topics = selected?.let { database.knowledgePoolDao().topics(it.id) }.orEmpty()
        titleDraft = selected?.detectedTitle.orEmpty()
        authorDraft = selected?.author.orEmpty()
        publisherDraft = selected?.publisher.orEmpty()
        editionDraft = selected?.edition.orEmpty()
        subjectDraft = selected?.subject.orEmpty()
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
            var pagesWithText = 0
            var emptyPages = 0
            var shortTextPages = 0
            var duplicatePages = 0
            val pageFingerprints = mutableSetOf<String>()
            val candidates = linkedMapOf<String, Pair<String, Pair<Int, Pair<Float, String>>>>()
            val reader = OfflineDocumentReader(context)
            val stagingBookId = "__stage__${UUID.randomUUID()}"
            var stageCreated = false
            try {
                require(File(book.localPath).isFile) { "The original PDF is missing from local storage." }
                database.bookDao().addBook(book.copy(id = stagingBookId))
                stageCreated = true
                val summary = try {
                    reader.readPdfPages(Uri.fromFile(File(book.localPath)), maxPdfPages = 5_000) { page, total, text ->
                        chars += text.length
                        require(chars <= KNOWLEDGE_MAX_CHARS) { "The 25 million character processing safety limit was reached." }
                        if (text.isBlank()) {
                            emptyPages++
                        } else {
                            pagesWithText++
                            if (text.trim().length < 50) shortTextPages++
                            if (page <= 18) pageSamples += page to text.take(4_000)
                            val normalizedPage = text.lowercase().replace(Regex("\\s+"), " ").trim()
                            val fingerprint = MessageDigest.getInstance("SHA-256")
                                .digest(normalizedPage.toByteArray(Charsets.UTF_8))
                                .joinToString("") { byte -> "%02x".format(byte) }
                            if (!pageFingerprints.add(fingerprint)) duplicatePages++
                        }
                        val chunks = knowledgeChunks(text)
                        chunks.forEachIndexed { index, chunk ->
                            pending += BookPassageEntity(UUID.randomUUID().toString(), stagingBookId, index, page, chunk)
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
                val opening = pageSamples.sortedBy { it.first }.joinToString(System.lineSeparator()) { it.second }
                val detectedTitle = opening.lineSequence().map { it.trim() }.firstOrNull { it.length in 5..140 && !it.contains("copyright", true) } ?: book.title
                val author = Regex("(?im)^(?:by|author[s]?:)\\s*(.{3,100})$").find(opening)?.groupValues?.get(1)?.trim().orEmpty()
                val publisher = Regex("(?im)^.{0,30}(?:publishers?|press)\\s*$").find(opening)?.value?.trim().orEmpty()
                val edition = Regex("(?i)(\\d{1,2}(?:st|nd|rd|th)\\s+edition|edition\\s*[:#]?\\s*\\d{1,2})").find(opening)?.value.orEmpty()
                val subject = if (("$detectedTitle $opening").contains("biochem", true)) "Biochemistry" else "Needs subject review"
                val chapters = candidates.values.sortedBy { it.second.first }.take(120)
                val outline = chapters.joinToString(System.lineSeparator()) { it.second.first.toString() + ". " + it.first + " [confidence " + "%.2f".format(java.util.Locale.US, it.second.second.first) + "]" }
                val pageCoverage = if (summary.pageCount > 0) pagesWithText.toDouble() / summary.pageCount else 0.0
                val duplicateRatio = if (pagesWithText > 0) duplicatePages.toDouble() / pagesWithText else 0.0
                val score = (
                    (if (passageCount > 0) 20 else 0) +
                    (pageCoverage * 25).toInt() +
                    ((1.0 - duplicateRatio.coerceIn(0.0, 1.0)) * 15).toInt() +
                    (if (chapters.isNotEmpty()) 15 else 0) +
                    (if (author.isNotBlank()) 8 else 0) +
                    (if (publisher.isNotBlank()) 5 else 0) +
                    (if (edition.isNotBlank()) 5 else 0) +
                    (if (summary.extractedChars.toDouble() / summary.pageCount.coerceAtLeast(1) >= 300.0) 7 else 0)
                ).coerceIn(0, 100)
                // Swap staged passages only after the complete PDF has been read and validated.
                // Failed or cancelled re-analysis leaves the previous reviewed content intact.
                database.bookDao().replacePassagesFromStage(book.id, stagingBookId)
                stageCreated = false
                database.bookDao().updateBookStats(book.id, summary.pageCount, summary.extractedChars)
                val knowledgeId = database.knowledgePoolDao().forBook(book.id)?.id ?: UUID.randomUUID().toString()
                database.knowledgePoolDao().saveBook(
                    KnowledgeBookEntity(
                        id = knowledgeId, bookId = book.id, detectedTitle = detectedTitle,
                        author = author, publisher = publisher, edition = edition, subject = subject,
                        summary = "Extraction audit: $pagesWithText/${summary.pageCount} pages contained OCR text; $emptyPages pages were empty; $shortTextPages pages had fewer than 50 characters; $duplicatePages pages repeated identical OCR text. Indexed $passageCount source-linked passages and detected ${chapters.size} possible headings. Readiness is heuristic, not a scientific accuracy score. Inspect flagged pages in the original PDF before approval.",
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
                    if (stageCreated) runCatching { database.bookDao().deleteBook(stagingBookId) }
                }
                throw cancelled
            } catch (error: Exception) {
                if (stageCreated) withContext(NonCancellable) {
                    runCatching { database.bookDao().deleteBook(stagingBookId) }
                }
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
                    Text("Extracted book details · edit before approval", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                    OutlinedTextField(titleDraft, { titleDraft = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Book title") }, singleLine = true)
                    OutlinedTextField(authorDraft, { authorDraft = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Author") }, singleLine = true)
                    OutlinedTextField(publisherDraft, { publisherDraft = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Publisher") }, singleLine = true)
                    OutlinedTextField(editionDraft, { editionDraft = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Edition") }, singleLine = true)
                    OutlinedTextField(subjectDraft, { subjectDraft = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Subject / discipline") }, singleLine = true)
                    OutlinedButton(onClick = {
                        scope.launch {
                            database.knowledgePoolDao().updateMetadata(selected!!.id, titleDraft.trim(), authorDraft.trim(), publisherDraft.trim(), editionDraft.trim(), subjectDraft.trim())
                            selected = selected!!.copy(detectedTitle = titleDraft.trim(), author = authorDraft.trim(), publisher = publisherDraft.trim(), edition = editionDraft.trim(), subject = subjectDraft.trim(), reviewState = "needs_review")
                            status = "Book metadata saved. Review and approve the source when it is accurate."
                        }
                    }, modifier = Modifier.fillMaxWidth(), enabled = titleDraft.isNotBlank()) { Text("Save book details") }
                    Text("Extraction readiness: " + selected!!.qualityScore + "/100 · " + selected!!.reviewState.replace('_', ' '), style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                    Text(selected!!.summary, style = MaterialTheme.typography.bodySmall)
                    Button(
                        onClick = {
                            scope.launch {
                                database.knowledgePoolDao().setReviewState(selected!!.id, "approved")
                                selected = selected!!.copy(reviewState = "approved")
                                status = "Source marked as professor-reviewed. Individual topic approvals remain visible below."
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = selected!!.reviewState != "approved"
                    ) { Text(if (selected!!.reviewState == "approved") "Source reviewed" else "Mark source as reviewed") }
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
                                scope.launch {
                                    database.knowledgePoolDao().setTopicApproved(topic.id, checked)
                                    topics = database.knowledgePoolDao().topics(selected!!.id)
                                    if (topics.isNotEmpty() && topics.all { it.approved }) {
                                        database.knowledgePoolDao().setReviewState(selected!!.id, "approved")
                                        selected = selected!!.copy(reviewState = "approved")
                                    } else if (selected!!.reviewState == "approved") {
                                        database.knowledgePoolDao().setReviewState(selected!!.id, "needs_review")
                                        selected = selected!!.copy(reviewState = "needs_review")
                                    }
                                }
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
                                Button(onClick = { processBook(book) }, enabled = processingId == null && analysed == null) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = null)
                                    Spacer(Modifier.width(5.dp))
                                    Text(if (analysed == null) "Extract & analyse" else "Already analysed")
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
