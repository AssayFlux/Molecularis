package org.molecularis.app.ui

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.UploadFile
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.molecularis.app.data.AppDatabase
import org.molecularis.app.data.BookEntity
import java.io.File
import java.util.UUID


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BookLibraryScreen(database: AppDatabase) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val books by database.bookDao().books().collectAsState(initial = emptyList())
    var query by remember { mutableStateOf("") }
    var importing by remember { mutableStateOf(false) }
    var status by remember { mutableStateOf("") }
    var selectedBook by remember { mutableStateOf<BookEntity?>(null) }
    var results by remember { mutableStateOf(emptyList<BookPassageEntity>()) }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null && !importing) {
            scope.launch {
                importing = true
                status = "Reading and indexing the selected PDF on this device…"
                var localFile: File? = null
                var importedChars = 0
                val id = UUID.randomUUID().toString()
                try {
                    val name = context.contentResolver.query(uri, arrayOf(android.provider.OpenableColumns.DISPLAY_NAME), null, null, null)?.use { cursor ->
                        if (cursor.moveToFirst()) cursor.getString(0) else null
                    } ?: "Biochemistry textbook.pdf"
                    require(name.endsWith(".pdf", true)) { "Please select a PDF textbook." }
                    val bookDir = File(context.filesDir, "books").apply { mkdirs() }
                    val safeName = name.replace(Regex("[^A-Za-z0-9._-]"), "_").take(100)
                    localFile = File(bookDir, "$id-$safeName")
                    withContext(Dispatchers.IO) {
                        context.contentResolver.openInputStream(uri)?.use { input ->
                            localFile!!.outputStream().buffered().use { output -> input.copyTo(output) }
                        } ?: error("Could not open the selected PDF.")
                    }
                    val book = BookEntity(
                        id = id,
                        title = name.removeSuffix(".pdf").removeSuffix(".PDF"),
                        originalFileName = name,
                        localPath = localFile!!.absolutePath,
                        sourceUri = uri.toString(),
                        pageCount = 0,
                        extractedChars = 0
                    )
                    database.bookDao().addBook(book)
                    status = "Added ${book.title} to Library. The original PDF is preserved unchanged. Open Knowledge Pool when you are ready to extract, analyse and organize its content."

                } catch (error: CancellationException) {
                    withContext(NonCancellable) {
                        runCatching { database.bookDao().deleteBook(id) }
                        localFile?.delete()
                    }
                    throw error
                } catch (error: Throwable) {
                    withContext(NonCancellable) {
                        runCatching { database.bookDao().deleteBook(id) }
                        localFile?.delete()
                    }
                    status = "Import failed: " + (error.message ?: error.javaClass.simpleName)
                } finally {
                    importing = false
                }
            }
        }
    }

    LaunchedEffect(query, selectedBook?.id) {
        val clean = query.trim()
        results = if (clean.length < 2) emptyList()
        else selectedBook?.let { database.bookDao().searchInBook(it.id, clean) }
            ?: database.bookDao().searchAll(clean)
    }

    Column(Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("Textbook library", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text("Library is your source shelf. Add original books here first; extraction, quality analysis and topic organization happen separately in Knowledge Pool.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Button(onClick = { picker.launch(arrayOf("application/pdf")) }, enabled = !importing, modifier = Modifier.fillMaxWidth()) {
            Icon(Icons.Default.UploadFile, contentDescription = null)
            Spacer(Modifier.width(8.dp))
            Text(if (importing) "Saving PDF…" else "Add original PDF")
        }
        if (importing) LinearProgressIndicator(Modifier.fillMaxWidth())
        if (status.isNotBlank()) Text(status, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            modifier = Modifier.fillMaxWidth(),
            label = { Text("Search extracted Library text") },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
            singleLine = true
        )
        if (selectedBook != null) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                TextButton(onClick = { selectedBook = null; query = "" }) { Text("All books") }
                Text(selectedBook!!.title, fontWeight = FontWeight.SemiBold, maxLines = 1)
            }
        }
        val showingResults = query.trim().length >= 2
        if (showingResults) {
            Text(results.size.toString() + " matching passages", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(results, key = { it.id }) { passage ->
                    Card(Modifier.fillMaxWidth()) {
                        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                            Text("Page " + passage.pageNumber, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary)
                            Text(passage.text, style = MaterialTheme.typography.bodyMedium)
                        }
                    }
                }
            }
        } else if (selectedBook != null) {
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(selectedBook!!.title, fontWeight = FontWeight.SemiBold)
                    Text("This is the preserved source document. Open Knowledge Pool to extract text, detect metadata and propose chapter/topic structure.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        } else if (books.isEmpty()) {
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.fillMaxWidth().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Icon(Icons.Default.MenuBook, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(36.dp))
                    Text("Your library is empty", fontWeight = FontWeight.SemiBold)
                    Text("Import a PDF to start building your private biochemistry knowledge base.", style = MaterialTheme.typography.bodySmall)
                }
            }
        } else {
            LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(books, key = { it.id }) { book ->
                    Card(Modifier.fillMaxWidth().clickable { selectedBook = book; query = "" }) {
                        Row(Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.MenuBook, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(28.dp))
                            Spacer(Modifier.width(12.dp))
                            Column(Modifier.weight(1f)) {
                                Text(book.title, fontWeight = FontWeight.SemiBold)
                                Text(if (book.pageCount == 0) "Original PDF stored · not yet processed" else book.pageCount.toString() + " pages · " + book.extractedChars + " extracted characters", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            IconButton(onClick = {
                                scope.launch {
                                    database.knowledgePoolDao().deleteForBook(book.id)
                                    database.bookDao().deleteBook(book.id)
                                    withContext(Dispatchers.IO) { File(book.localPath).delete() }
                                    status = "Removed " + book.title + " from this device."
                                }
                            }) { Icon(Icons.Default.Delete, contentDescription = "Delete textbook") }
                        }
                    }
                }
            }
        }
    }
}

private fun splitChunks(text: String, maxChars: Int = 1100): List<String> {
    val normalized = text.replace(Regex("\\s+"), " ").trim()
    if (normalized.isBlank()) return emptyList()
    val chunks = mutableListOf<String>()
    var start = 0
    while (start < normalized.length) {
        var end = (start + maxChars).coerceAtMost(normalized.length)
        if (end < normalized.length) {
            val boundary = normalized.lastIndexOf(' ', end)
            if (boundary > start + maxChars / 2) end = boundary
        }
        chunks += normalized.substring(start, end).trim()
        if (end == normalized.length) break
        start = end
    }
    return chunks
}
