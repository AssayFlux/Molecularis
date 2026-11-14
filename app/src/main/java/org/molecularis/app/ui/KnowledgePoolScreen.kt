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
import org.molecularis.app.features.KnowledgeProcessingWorker
import org.molecularis.app.features.TopicOrganization
import androidx.work.*
import kotlinx.coroutines.flow.collect
import org.molecularis.app.features.OfflineDocumentReader
import java.io.File
import java.util.UUID
import java.security.MessageDigest

private const val KNOWLEDGE_MAX_CHARS = 25_000_000

@Composable
fun KnowledgePoolScreen(database: AppDatabase, subjectId:String) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val library by database.bookDao().booksForSubject(subjectId).collectAsState(initial = emptyList())
    val pool by database.knowledgePoolDao().booksForSubject(subjectId).collectAsState(initial = emptyList())
    var status by remember { mutableStateOf("Your source books stay unchanged in Library. Process a copy into structured knowledge here.") }
    var processingId by remember { mutableStateOf<String?>(null) }
    var selected by remember { mutableStateOf<KnowledgeBookEntity?>(null) }
    var topics by remember { mutableStateOf(emptyList<KnowledgeTopicEntity>()) }
    var aliases by remember { mutableStateOf(emptyMap<String, List<KnowledgeTopicAliasEntity>>()) }
    var titleDraft by remember { mutableStateOf("") }
    var authorDraft by remember { mutableStateOf("") }
    var publisherDraft by remember { mutableStateOf("") }
    var editionDraft by remember { mutableStateOf("") }
    var subjectDraft by remember { mutableStateOf("") }
    var newTopicName by remember { mutableStateOf("") }
    var newTopicPage by remember { mutableStateOf("1") }

    LaunchedEffect(subjectId) {
        selected = null
        topics = emptyList()
        aliases = emptyMap()
    }

    LaunchedEffect(Unit) {
        // Android may kill the process before the coroutine cleanup handler can run.
        // Reclaim only abandoned staging rows older than seven days.
        database.bookDao().cleanupStaleStagingBooks(System.currentTimeMillis() - 7L * 24 * 60 * 60 * 1000)
    }

    LaunchedEffect(selected?.id) {
        topics = selected?.let { database.knowledgePoolDao().topics(it.id) }.orEmpty()
        aliases = topics.associate { it.id to database.knowledgePoolDao().aliases(it.id) }
        titleDraft = selected?.detectedTitle.orEmpty()
        authorDraft = selected?.author.orEmpty()
        publisherDraft = selected?.publisher.orEmpty()
        editionDraft = selected?.edition.orEmpty()
        subjectDraft = selected?.subject.orEmpty()
    }

    fun processBook(book: BookEntity) {
        if (processingId != null) return
        processingId = book.id
        status = "Queueing durable document analysis for " + book.title + "…"
        val request = OneTimeWorkRequestBuilder<KnowledgeProcessingWorker>()
            .setInputData(workDataOf(KnowledgeProcessingWorker.KEY_BOOK_ID to book.id))
            .addTag("molecularis-knowledge")
            .build()
        WorkManager.getInstance(context).enqueueUniqueWork(
            "knowledge-" + book.id, ExistingWorkPolicy.KEEP, request
        )
        scope.launch {
            WorkManager.getInstance(context)
                .getWorkInfosForUniqueWorkFlow("knowledge-" + book.id)
                .collect { infos ->
                    val info = infos.firstOrNull() ?: return@collect
                    val page = info.progress.getInt("page", 0)
                    val total = info.progress.getInt("total", 0)
                    val passages = info.progress.getInt("passages", 0)
                    status = when (info.state) {
                        WorkInfo.State.ENQUEUED -> "Document analysis is queued for background processing."
                        WorkInfo.State.RUNNING -> if (total > 0) "Analysing page " + page + " of " + total + " · " + passages + " passages indexed" else "Preparing document analysis…"
                        WorkInfo.State.SUCCEEDED -> "Knowledge preparation complete for " + book.title + ". Review metadata and approve topic candidates before teaching."
                        WorkInfo.State.FAILED -> "Analysis failed: " + (info.outputData.getString("error") ?: "unknown error")
                        WorkInfo.State.CANCELLED -> "Analysis cancelled. Previously reviewed passages remain unchanged."
                        WorkInfo.State.BLOCKED -> "Document analysis is waiting for its prerequisites."
                    }
                    if (info.state.isFinished) processingId = null
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
        if (processingId != null) { LinearProgressIndicator(Modifier.fillMaxWidth()); TextButton(onClick = { processingId?.let { WorkManager.getInstance(context).cancelUniqueWork("knowledge-" + it) } }) { Text("Cancel processing") } }
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
                                status = "Source marked as user-reviewed. Individual topic approvals remain visible below."
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = selected!!.reviewState != "approved"
                    ) { Text(if (selected!!.reviewState == "approved") "Source reviewed" else "Mark source as reviewed") }
                    Divider()
                    Text("Detected chapter / topic candidates", fontWeight = FontWeight.SemiBold)
                    OutlinedTextField(newTopicName, { newTopicName = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Add a topic manually") }, singleLine = true)
                    OutlinedTextField(newTopicPage, { newTopicPage = it.filter(Char::isDigit).take(5) }, modifier = Modifier.fillMaxWidth(), label = { Text("Starting page") }, singleLine = true)
                    OutlinedButton(
                        onClick = {
                            scope.launch {
                                val page = newTopicPage.toIntOrNull()?.coerceAtLeast(1) ?: 1
                                database.knowledgePoolDao().addTopic(KnowledgeTopicEntity(
                                    id = UUID.randomUUID().toString(), knowledgeBookId = selected!!.id,
                                    name = newTopicName.trim(), startPage = page, confidence = 0f,
                                    evidence = "Added manually by user", approved = false
                                ))
                                topics = database.knowledgePoolDao().topics(selected!!.id)
                                newTopicName = ""
                                newTopicPage = "1"
                                database.knowledgePoolDao().setReviewState(selected!!.id, "needs_review")
                                selected = selected!!.copy(reviewState = "needs_review")
                                status = "Topic added. Review and approve it before using it as a teaching source."
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = newTopicName.isNotBlank() &&
                            (newTopicPage.toIntOrNull() ?: 0) in 1..(library.firstOrNull { it.id == selected?.bookId }?.pageCount ?: 0)
                    ) { Text("Add topic") }
                    if (topics.isEmpty()) Text("No reliable headings were detected. You can add user-authored topics above.", style = MaterialTheme.typography.bodySmall)
                    topics.forEach { topic ->
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                var editedName by remember(topic.id) { mutableStateOf(topic.name) }
                                var editedPage by remember(topic.id) { mutableStateOf(topic.startPage.toString()) }
                                var showPageEvidence by remember(topic.id) { mutableStateOf(false) }
                                var pageEvidence by remember(topic.id) { mutableStateOf(emptyList<BookPassageEntity>()) }
                                TextButton(onClick = {
                                    scope.launch {
                                        showPageEvidence = !showPageEvidence
                                        if (showPageEvidence) {
                                            val linked = database.knowledgePoolDao().passagesForTopic(topic.id)
                                            pageEvidence = linked.ifEmpty { database.bookDao().passagesAtPage(selected!!.bookId, topic.startPage) }
                                        }
                                    }
                                }) { Text(if (showPageEvidence) "Hide source passages" else "View linked source passages · from page " + topic.startPage) }
                                if (showPageEvidence) {
                                    if (pageEvidence.isEmpty()) Text("No extracted passages are available at this page.", style = MaterialTheme.typography.bodySmall)
                                    pageEvidence.forEachIndexed { index, passage ->
                                        Card(Modifier.fillMaxWidth()) {
                                            Column(Modifier.padding(8.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                                                Text("Book page " + passage.pageNumber + " · passage " + (index + 1), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                                                Text(passage.text, style = MaterialTheme.typography.bodySmall)
                                            }
                                        }
                                    }
                                }
                                OutlinedTextField(editedName, { editedName = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Topic") }, singleLine = true)
                                OutlinedTextField(editedPage, { editedPage = it.filter(Char::isDigit).take(5) }, modifier = Modifier.fillMaxWidth(), label = { Text("Starting page") }, singleLine = true)
                                var aliasDraft by remember(topic.id) { mutableStateOf("") }
                                var parentMenu by remember(topic.id) { mutableStateOf(false) }
                                var mergeMenu by remember(topic.id) { mutableStateOf(false) }
                                var mergeTarget by remember(topic.id) { mutableStateOf(topics.firstOrNull { it.id != topic.id }?.id.orEmpty()) }
                                Text("Parent topic", style = MaterialTheme.typography.labelMedium)
                                Box {
                                    OutlinedButton(onClick = { parentMenu = true }, modifier = Modifier.fillMaxWidth()) {
                                        Text(topics.firstOrNull { it.id == topic.parentTopicId }?.name ?: "Top-level topic")
                                    }
                                    DropdownMenu(expanded = parentMenu, onDismissRequest = { parentMenu = false }) {
                                        DropdownMenuItem(text = { Text("Top-level topic") }, onClick = {
                                            parentMenu = false
                                            scope.launch {
                                                database.knowledgePoolDao().setTopicParent(topic.id, null)
                                                topics = database.knowledgePoolDao().topics(selected!!.id)
                                                database.knowledgePoolDao().setReviewState(selected!!.id, "needs_review")
                                                selected = selected!!.copy(reviewState = "needs_review")
                                            }
                                        })
                                        topics.filter { it.id != topic.id }.forEach { candidate ->
                                            DropdownMenuItem(text = { Text(candidate.name) }, onClick = {
                                                parentMenu = false
                                                scope.launch {
                                                    runCatching { database.knowledgePoolDao().setTopicParent(topic.id, candidate.id) }
                                                        .onSuccess {
                                                            topics = database.knowledgePoolDao().topics(selected!!.id)
                                                            database.knowledgePoolDao().setReviewState(selected!!.id, "needs_review")
                                                            selected = selected!!.copy(reviewState = "needs_review")
                                                            status = "Topic hierarchy updated. Review the topic again before teaching."
                                                        }
                                                        .onFailure { status = it.message ?: "Could not update topic hierarchy." }
                                                }
                                            })
                                        }
                                    }
                                }
                                Text("Aliases", style = MaterialTheme.typography.labelMedium)
                                aliases[topic.id].orEmpty().forEach { alias ->
                                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                        Text(alias.alias, style = MaterialTheme.typography.bodySmall)
                                        TextButton(onClick = {
                                            scope.launch {
                                                database.knowledgePoolDao().deleteAlias(alias.id)
                                                aliases = aliases + (topic.id to database.knowledgePoolDao().aliases(topic.id))
                                            }
                                        }) { Text("Remove") }
                                    }
                                }
                                OutlinedTextField(aliasDraft, { aliasDraft = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Add alternate name") }, singleLine = true)
                                TextButton(onClick = {
                                    scope.launch {
                                        val normalized = TopicOrganization.normalizeName(aliasDraft)
                                        if (normalized.isBlank() || normalized == TopicOrganization.normalizeName(topic.name)) {
                                            status = "Enter a distinct, non-empty alias."
                                        } else {
                                            val result = database.knowledgePoolDao().addAlias(
                                                KnowledgeTopicAliasEntity(UUID.randomUUID().toString(), topic.id, aliasDraft.trim(), normalized)
                                            )
                                            if (result == -1L) status = "That alias already exists for this topic."
                                            else {
                                                aliases = aliases + (topic.id to database.knowledgePoolDao().aliases(topic.id))
                                                aliasDraft = ""
                                                status = "Alias saved."
                                            }
                                        }
                                    }
                                }, enabled = aliasDraft.isNotBlank()) { Text("Add alias") }
                                val possibleDuplicates = topics.filter { it.id != topic.id && TopicOrganization.normalizeName(it.name) == TopicOrganization.normalizeName(topic.name) }
                                if (possibleDuplicates.isNotEmpty() || topics.size > 1) {
                                    Text("Merge duplicate topic into", style = MaterialTheme.typography.labelMedium)
                                    Box {
                                        OutlinedButton(onClick = { mergeMenu = true }, modifier = Modifier.fillMaxWidth()) {
                                            Text(topics.firstOrNull { it.id == mergeTarget }?.name ?: "Choose target topic")
                                        }
                                        DropdownMenu(expanded = mergeMenu, onDismissRequest = { mergeMenu = false }) {
                                            topics.filter { it.id != topic.id }.forEach { candidate ->
                                                DropdownMenuItem(text = { Text(candidate.name) }, onClick = {
                                                    mergeTarget = candidate.id
                                                    mergeMenu = false
                                                })
                                            }
                                        }
                                    }
                                    TextButton(onClick = {
                                        scope.launch {
                                            runCatching { database.knowledgePoolDao().mergeTopic(topic.id, mergeTarget) }
                                                .onSuccess {
                                                    topics = database.knowledgePoolDao().topics(selected!!.id)
                                                    aliases = topics.associate { it.id to database.knowledgePoolDao().aliases(it.id) }
                                                    database.knowledgePoolDao().setReviewState(selected!!.id, "needs_review")
                                                    selected = selected!!.copy(reviewState = "needs_review")
                                                    status = "Topic merged. Verify the surviving topic and its aliases."
                                                }
                                                .onFailure { status = it.message ?: "Could not merge topics." }
                                        }
                                    }, enabled = mergeTarget.isNotBlank() && mergeTarget != topic.id) { Text("Merge this topic into selected") }
                                }
                                Text(
                                    if (topic.evidence == "Added manually by user") "User-created · ${topic.evidence}"
                                    else "Detection confidence ${"%.0f".format(topic.confidence * 100)}% · ${topic.evidence}",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                TextButton(onClick = {
                                    scope.launch {
                                        val page = editedPage.toIntOrNull()?.coerceAtLeast(1) ?: topic.startPage
                                        database.knowledgePoolDao().updateTopicDetails(topic.id, editedName.trim(), page)
                                        topics = database.knowledgePoolDao().topics(selected!!.id)
                                        database.knowledgePoolDao().setReviewState(selected!!.id, "needs_review")
                                        selected = selected!!.copy(reviewState = "needs_review")
                                        status = "Topic updated; its approval was reset for user review."
                                    }
                                }, enabled = editedName.isNotBlank() && editedPage.toIntOrNull() != null) { Text("Save topic") }
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
                                Button(onClick = { processBook(book) }, enabled = processingId == null) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = null)
                                    Spacer(Modifier.width(5.dp))
                                    Text(if (analysed == null) "Extract & analyse" else "Re-analyse safely")
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
