package org.assayflux.molecularis

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.Surface
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.util.zip.GZIPInputStream

private data class I1LigandDocument(val name: String, val text: String)

private fun readI1LigandDocument(context: Context, uri: Uri): I1LigandDocument {
    val name = context.contentResolver.query(
        uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
    )?.use { cursor ->
        if (cursor.moveToFirst()) cursor.getString(0) else null
    } ?: uri.lastPathSegment ?: "ligand"
    val baseName = name.lowercase(java.util.Locale.ROOT).removeSuffix(".gz")
    require(baseName.endsWith(".sdf") || baseName.endsWith(".mol")) {
        "Select an SDF or MOL file, optionally gzip-compressed."
    }
    val input = context.contentResolver.openInputStream(uri)
        ?: error("The selected ligand document could not be opened.")
    val decoded = if (name.endsWith(".gz", ignoreCase = true)) GZIPInputStream(input) else input
    val bytes = decoded.use { stream ->
        val output = ByteArrayOutputStream()
        val buffer = ByteArray(32 * 1024)
        var total = 0
        while (true) {
            val count = stream.read(buffer)
            if (count < 0) break
            total += count
            require(total <= I1ChemistryRunner.MAX_SDF_BYTES) {
                "Ligand file exceeds the 16 MiB import limit."
            }
            output.write(buffer, 0, count)
        }
        output.toByteArray()
    }
    val text = Charsets.UTF_8.newDecoder()
        .onMalformedInput(CodingErrorAction.REPORT)
        .onUnmappableCharacter(CodingErrorAction.REPORT)
        .decode(ByteBuffer.wrap(bytes)).toString()
    require(!text.contains('\u0000')) { "Ligand file contains a NUL byte." }
    return I1LigandDocument(name, text)
}

@Composable
internal fun LigandGraphPreviewCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var document by remember { mutableStateOf<I1LigandDocument?>(null) }
    var result by remember { mutableStateOf<JSONObject?>(null) }
    var status by remember {
        mutableStateOf("Import one local SDF/MOL ligand for bounded graph-only inspection.")
    }
    var error by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var fullScreen by remember { mutableStateOf(false) }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            busy = true
            error = null
            result = null
            status = "Reading ligand file…"
            scope.launch {
                val outcome = withContext(Dispatchers.IO) {
                    runCatching { readI1LigandDocument(context, uri) }
                }
                outcome.onSuccess {
                    document = it
                    status = "Loaded ${it.name}; analysis runs locally."
                }.onFailure {
                    error = it.message ?: "Ligand import failed."
                    status = "Ligand file was not loaded."
                }
                busy = false
            }
        }
    }

    @Composable
    fun Panel(modifier: Modifier) {
    Card(modifier) {
        Column(
            Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text("Ligand chemistry workspace", style = MaterialTheme.typography.titleMedium)
            Button(onClick = { fullScreen = !fullScreen }) { Text(if (fullScreen) "Close full-screen view" else "Open full-screen chemistry") }
            Text(
                "Offline-first SDF/MOL import with explicit-atom formula, graph counts and SHA-256 provenance. This is not RDKit sanitization or a drug-likeness verdict.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(
                onClick = {
                    picker.launch(arrayOf("chemical/x-mdl-sdfile", "chemical/x-mdl-molfile", "*/*"))
                },
                enabled = !busy,
                modifier = Modifier.fillMaxWidth(),
            ) { Text(if (busy) "Working…" else "Choose SDF / MOL / .gz ligand") }
            document?.let { Text("Ligand: ${it.name}", style = MaterialTheme.typography.labelMedium) }
            Button(
                onClick = {
                    val source = document?.text
                    if (source == null) {
                        error = "Choose a ligand file first."
                    } else {
                        busy = true
                        error = null
                        result = null
                        scope.launch {
                            val outcome = withContext(Dispatchers.IO) {
                                runCatching { I1ChemistryRunner.analyzeSdfGraph(context, source) }
                            }
                            outcome.onSuccess {
                                result = it
                                status = "Graph preview complete; limitations are listed below."
                            }.onFailure {
                                error = it.message ?: "Ligand analysis failed."
                                status = "Ligand analysis did not complete."
                            }
                            busy = false
                        }
                    }
                },
                enabled = !busy && document != null,
                modifier = Modifier.fillMaxWidth(),
            ) { Text(if (busy) "Analysing…" else "Analyse ligand graph") }
            Text(status, style = MaterialTheme.typography.bodySmall)
            error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            result?.let { output ->
                val graph = output.optJSONObject("graph")
                Text("Formula (explicit atoms): ${output.optString("formula_explicit_atoms")}")
                Text("Explicit-atom mass sum: ${"%.3f".format(output.optDouble("explicit_atom_mass_sum_da"))} Da")
                Text("Atoms: ${graph?.optInt("atom_count") ?: 0} · Bonds: ${graph?.optInt("bond_count") ?: 0}")
                Text("Connected components: ${graph?.optInt("connected_components") ?: 0} · Cycle rank: ${graph?.optInt("cycle_rank") ?: 0}")
                Text(
                    "SHA-256: ${output.optString("source_sha256")}",
                    style = MaterialTheme.typography.labelSmall,
                )
                val limitations = output.optJSONArray("limitations")
                if (limitations != null) {
                    for (index in 0 until limitations.length()) {
                        Text("• ${limitations.optString(index)}", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }
    }
    }
    if (fullScreen) {
        Dialog(onDismissRequest = { fullScreen = false }, properties = DialogProperties(usePlatformDefaultWidth = false)) {
            Surface(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing), color = MaterialTheme.colorScheme.background) {
                Panel(Modifier.fillMaxSize())
            }
        }
    } else {
        Panel(Modifier.fillMaxWidth())
    }
}
