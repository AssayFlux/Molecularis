package org.molecularis.app.ui

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.UploadFile
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.molecularis.app.data.AppDatabase
import org.molecularis.app.data.BookEntity
import org.molecularis.app.data.BookPassageEntity
import org.molecularis.app.features.OfflineDocumentReader
import java.io.File
import java.util.UUID

private data class ImportedPage(val number: Int, val text: String)

@Composable
fun LibraryScreen(database: AppDatabase) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val books by database.bookDao().books().collectAsState(initial = emptyList())
    var importing by remember { mutableStateOf(false) }
    var status by remember { mutableStateOf("Your textbooks stay on this device.") }
    var query by remember { mutableStateOf("") }
    var matches by remember { mutableStateOf(emptyList<BookPassageEntity>()) }
    var searching by remember { mutableStateOf(false) }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri: Uri? ->
        if (uri != null && !importing) scope.launch {
            importing = true
            status = "Copying and extracting the selected document…"
            var copiedFile: File? = null
            try {
                runCatching { context.contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION) }
                val name = withContext(Dispatchers.IO) {
                    context.contentResolver.query(uri, arrayOf(android.provider.OpenableColumns.DISPLAY_NAME), null, null, null)
                        ?.use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }
                } ?: uri.lastPathSegment?.substringAfterLast('/') ?: "textbook"
                val safeName = name.replace(Regex("[^A-Za-z0-9._ -]"), "_").take(100).ifBlank { "textbook" }
                val id = UUID.randomUUID().toString()
                val directory = File(context.filesDir, "books").apply { mkdirs() }
                copiedFile = File(directory, id + "-" + safeName)
                withContext(Dispatchers.IO) {
                    context.contentResolver.openInputStream(uri)?.use { input ->
                        copiedFile!!.outputStream().use { output -> input.copyTo(output) }
                    } ?: error("Android could not open the selected file.")
                }
                val mime = context.contentResolver.getType(uri)
                val reader = OfflineDocumentReader(context)
                val extracted = try {
                    reader.read(uri, mime ?: if (safeName.endsWith(".pdf", true)) "application/pdf" else "text/plain", maxPdfPages = 250, displayName = safeName)
                } finally { reader.close() }
                val pages = splitIntoPages(extracted)
                require(pages.any { it.text.isNotBlank() }) { "No readable text was extracted." }
                val title = safeName.substringBeforeLast('.').ifBlank { safeName }
                database.bookDao().addBook(BookEntity(id, title, safeName, copiedFile!!.absolutePath, uri.toString(), pages.size, extracted.length))
                val passages = pages.flatMap { page ->
                    splitPassages(page.text).mapIndexed { chunkIndex, passage ->
                        BookPassageEntity(id + "-" + page.number + "-" + chunkIndex, id, chunkIndex, page.number, passage)
                    }
                }
                database.bookDao().addPassages(passages)
                status = "Imported " + title + " · " + pages.size + " pages · " + passages.size + " searchable passages."
            } catch (error: Throwable) {
                copiedFile?.delete()
                status = "Import failed: " + (error.message ?: error.javaClass.simpleName)
            } finally { importing = false }
        }
    }

    Column(Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.72f))) {
            Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("MOLECULARIS KNOWLEDGE LIBRARY", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Text("Your books. Your local knowledge base.", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text("Import PDFs and text files. Molecularis extracts page-aware passages for offline search and lesson preparation.")
            }
        }
        Button(onClick = { picker.launch(arrayOf("application/pdf", "text/plain", "text/markdown")) }, enabled = !importing, modifier = Modifier.fillMaxWidth()) {
            Icon(Icons.Default.UploadFile, contentDescription = null)
            Spacer(Modifier.width(8.dp))
            Text(if (importing) "Importing…" else "Import a textbook or notes")
        }
        Text(status, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text("Library · " + books.size + " books", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        if (books.isEmpty()) Text("No books yet. Add your first textbook when ready.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        else LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(books, key = { it.id }) { book ->
                Card {
                    Row(Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Icon(Icons.Default.MenuBook, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Column(Modifier.weight(1f)) {
                            Text(book.title, fontWeight = FontWeight.SemiBold)
                            Text(book.pageCount.toString() + " pages · " + book.extractedChars + " extracted characters", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        IconButton(onClick = {
                            scope.launch {
                                database.bookDao().deleteBook(book.id)
                                File(book.localPath).delete()
                                status = "Removed " + book.title + " from this device."
                            }
                        }) { Icon(Icons.Default.Delete, contentDescription = "Remove textbook") }
                    }
                }
            }
        }
        Divider()
        Text("Search your textbooks", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        OutlinedTextField(query, { query = it }, modifier = Modifier.fillMaxWidth(), singleLine = true, label = { Text("Search a biochemical concept") })
        OutlinedButton(onClick = {
            scope.launch {
                searching = true
                try {
                    matches = if (query.isBlank()) emptyList() else database.bookDao().searchAll(query.trim())
                    status = if (matches.isEmpty()) "No passages matched that phrase." else "Found " + matches.size + " matching passages."
                } finally { searching = false }
            }
        }, enabled = query.isNotBlank() && !searching, modifier = Modifier.fillMaxWidth()) {
            Text(if (searching) "Searching…" else "Search local library")
        }
        if (matches.isNotEmpty()) LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(matches, key = { it.id }) { passage ->
                val title = books.firstOrNull { it.id == passage.bookId }?.title ?: "Textbook"
                Card { Column(Modifier.fillMaxWidth().padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(title + " · page " + passage.pageNumber, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary)
                    Text(passage.text, style = MaterialTheme.typography.bodyMedium)
                } }
            }
        }
    }
}

private fun splitIntoPages(extracted: String): List<ImportedPage> {
    val marker = Regex("(?m)^\\[Page (\\d+)]\\s*")
    val found = marker.findAll(extracted).toList()
    if (found.isEmpty()) return listOf(ImportedPage(1, extracted.trim()))
    return found.mapIndexed { index, match ->
        val end = found.getOrNull(index + 1)?.range?.first ?: extracted.length
        ImportedPage(match.groupValues[1].toIntOrNull() ?: index + 1, extracted.substring(match.range.last + 1, end).trim())
    }.filter { it.text.isNotBlank() }
}

private fun splitPassages(text: String, maxChars: Int = 1800): List<String> {
    val output = mutableListOf<String>()
    var current = StringBuilder()
    text.split(Regex("\\n\\s*\\n")).map { it.trim() }.filter { it.isNotBlank() }.forEach { paragraph ->
        if (current.isNotEmpty() && current.length + paragraph.length + 2 > maxChars) {
            output += current.toString()
            current = StringBuilder()
        }
        if (paragraph.length > maxChars) {
            if (current.isNotEmpty()) { output += current.toString(); current = StringBuilder() }
            paragraph.chunked(maxChars).forEach(output::add)
        } else {
            if (current.isNotEmpty()) current.append("\\n\\n")
            current.append(paragraph)
        }
    }
    if (current.isNotEmpty()) output += current.toString()
    return output
}
