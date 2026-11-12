package org.molecularis.app.ui
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.documentfile.provider.DocumentFile
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.FileNotFoundException

private data class StudioFile(val document: DocumentFile, val relativePath: String)

/** SAF-scoped editor: no broad storage permission, shell execution or implicit file writes. */
@Composable
fun DeveloperStudioScreen(modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val prefs = remember(context) { context.getSharedPreferences("molecularis_developer_studio", 0) }
    var treeUri by remember { mutableStateOf(prefs.getString("tree_uri", null)) }
    var files by remember { mutableStateOf(emptyList<StudioFile>()) }
    var selected by remember { mutableStateOf<StudioFile?>(null) }
    var editorText by remember { mutableStateOf("") }
    var dirty by remember { mutableStateOf(false) }
    var status by remember { mutableStateOf("Choose a project folder. Access is limited to the folder you select.") }
    var busy by remember { mutableStateOf(false) }

    fun refresh(uriText: String?) {
        if (uriText == null) { files = emptyList(); return }
        val root = DocumentFile.fromTreeUri(context, android.net.Uri.parse(uriText))
        if (root == null || !root.canRead()) { status = "Project folder is no longer accessible. Choose it again."; files = emptyList(); return }
        val result = mutableListOf<StudioFile>()
        fun walk(folder: DocumentFile, prefix: String, depth: Int) {
            if (depth > 5 || result.size >= 500) return
            folder.listFiles().sortedBy { it.name?.lowercase().orEmpty() }.forEach { child ->
                val name = child.name ?: return@forEach
                if (name.startsWith(".") || name in setOf("build", ".git", "node_modules")) return@forEach
                val path = if (prefix.isEmpty()) name else "$prefix/$name"
                if (child.isDirectory) walk(child, path, depth + 1) else if (child.isFile) result += StudioFile(child, path)
            }
        }
        walk(root, "", 0)
        files = result
        status = "Showing ${result.size} files · folder-scoped access only"
    }
    val folderPicker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocumentTree()) { uri ->
        if (uri != null) {
            runCatching { context.contentResolver.takePersistableUriPermission(uri, android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION or android.content.Intent.FLAG_GRANT_WRITE_URI_PERMISSION) }
            treeUri = uri.toString(); prefs.edit().putString("tree_uri", treeUri).apply()
            selected = null; editorText = ""; dirty = false; refresh(treeUri)
        }
    }
    LaunchedEffect(treeUri) { if (treeUri != null) refresh(treeUri) }
    Column(modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text("Developer Studio", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.SemiBold)
        Text("Browse and edit text files in a folder you explicitly select. Files remain where they are.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { folderPicker.launch(null) }) { Icon(Icons.Default.FolderOpen, null); Spacer(Modifier.width(6.dp)); Text(if (treeUri == null) "Open project folder" else "Change folder") }
            OutlinedButton(onClick = { refresh(treeUri) }, enabled = treeUri != null && !busy) { Icon(Icons.Default.Refresh, null); Text("Refresh") }
        }
        Text(status, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
        if (treeUri == null) Text("The Studio uses Android's Storage Access Framework. It cannot access arbitrary device paths.")
        else Row(Modifier.weight(1f), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            LazyColumn(Modifier.weight(0.42f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                items(files, key = { it.relativePath }) { item ->
                    TextButton(onClick = {
                        if (dirty) status = "Save your current edits before opening another file."
                        else {
                            selected = item; busy = true
                            scope.launch {
                                try {
                                    val text = withContext(Dispatchers.IO) {
                                        val bytes = context.contentResolver.openInputStream(item.document.uri)?.use { input ->
                                            val out = java.io.ByteArrayOutputStream(); val buffer = ByteArray(8192); var total = 0
                                            while (true) { val n = input.read(buffer); if (n < 0) break; total += n; require(total <= MAX_TEXT_BYTES) { "File exceeds the 2 MiB editor limit." }; out.write(buffer, 0, n) }
                                            out.toByteArray()
                                        } ?: throw FileNotFoundException("Cannot open file")
                                        require(bytes.none { it == 0.toByte() }) { "Binary files cannot be opened in the text editor." }
                                        bytes.toString(Charsets.UTF_8)
                                    }
                                    editorText = text; dirty = false; status = "Opened ${item.relativePath}"
                                } catch (e: Throwable) { status = "Cannot edit file: ${e.message}" } finally { busy = false }
                            }
                        }
                    }, modifier = Modifier.fillMaxWidth()) { Text(item.relativePath, maxLines = 2, style = MaterialTheme.typography.labelSmall) }
                }
            }
            Column(Modifier.weight(0.58f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(selected?.relativePath ?: "Select a text file", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.titleSmall)
                OutlinedTextField(value = editorText, onValueChange = { editorText = it; dirty = true }, modifier = Modifier.weight(1f).fillMaxWidth(),
                    enabled = selected != null && !busy, placeholder = { Text("UTF-8 text editor · max 2 MiB") }, textStyle = MaterialTheme.typography.bodySmall)
                Button(onClick = {
                    val item = selected ?: return@Button; busy = true
                    scope.launch {
                        try {
                            withContext(Dispatchers.IO) {
                                context.contentResolver.openOutputStream(item.document.uri, "wt")?.use { it.write(editorText.toByteArray(Charsets.UTF_8)); it.flush() }
                                    ?: error("Cannot write selected file")
                            }
                            dirty = false; status = "Saved ${item.relativePath}"
                        } catch (e: Throwable) { status = "Save failed: ${e.message}" } finally { busy = false }
                    }
                }, enabled = selected != null && dirty && !busy, modifier = Modifier.fillMaxWidth()) {
                    Icon(Icons.Default.Save, null); Spacer(Modifier.width(6.dp)); Text("Save changes")
                }
            }
        }
        HorizontalDivider()
        Text("Shell execution, Git operations and build orchestration are not enabled in this on-device editor. No project code runs automatically.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
private const val MAX_TEXT_BYTES = 2 * 1024 * 1024
