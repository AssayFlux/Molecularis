package org.assayflux.molecularis

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Checkbox
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
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
import java.util.Locale
import java.util.zip.GZIPInputStream

private data class S3StructureDocument(val name: String, val format: String, val text: String)

private fun readS3StructureDocument(context: Context, uri: Uri): S3StructureDocument {
    val name = context.contentResolver.query(
        uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
    )?.use { cursor ->
        if (cursor.moveToFirst()) cursor.getString(0) else null
    } ?: uri.lastPathSegment ?: "structure"
    val lowerName = name.lowercase(Locale.ROOT).removeSuffix(".gz")
    val format = when {
        lowerName.endsWith(".pdb") || lowerName.endsWith(".ent") -> "pdb"
        lowerName.endsWith(".cif") || lowerName.endsWith(".mmcif") -> "mmcif"
        else -> error("Select PDB, ENT, CIF, mmCIF or a .gz-compressed version.")
    }
    val input = context.contentResolver.openInputStream(uri)
        ?: error("The selected structure document could not be opened.")
    val decoded = if (name.endsWith(".gz", ignoreCase = true)) GZIPInputStream(input) else input
    val bytes = decoded.use { stream ->
        val output = ByteArrayOutputStream()
        val buffer = ByteArray(32 * 1024)
        var total = 0
        while (true) {
            val count = stream.read(buffer)
            if (count < 0) break
            total += count
            require(total <= S3S8Runner.MAX_STRUCTURE_BYTES) {
                "Structure file exceeds the 16 MiB import limit."
            }
            output.write(buffer, 0, count)
        }
        output.toByteArray()
    }
    val text = Charsets.UTF_8.newDecoder()
        .onMalformedInput(CodingErrorAction.REPORT)
        .onUnmappableCharacter(CodingErrorAction.REPORT)
        .decode(ByteBuffer.wrap(bytes)).toString()
    require(!text.contains('\u0000')) { "Structure file contains a NUL byte." }
    return S3StructureDocument(name, format, text)
}

@Composable
internal fun StructureSiteAnalysisCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var sourceText by remember { mutableStateOf<String?>(null) }
    var sourceFormat by remember { mutableStateOf("pdb") }
    var sourceName by remember { mutableStateOf<String?>(null) }
    var message by remember { mutableStateOf("Choose a local PDB or mmCIF file (compressed .gz is supported) to screen structure-site candidates.") }
    var chain by rememberSaveable { mutableStateOf("A") }
    var residueNumber by rememberSaveable { mutableStateOf("") }
    var residueName by rememberSaveable { mutableStateOf("") }
    var cutoff by rememberSaveable { mutableStateOf("5.0") }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    var ligandResult by remember { mutableStateOf<JSONObject?>(null) }
    var apoResult by remember { mutableStateOf<JSONObject?>(null) }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            busy = true
            error = null
            message = "Reading structure file…"
            scope.launch {
                val outcome = withContext(Dispatchers.IO) {
                    runCatching { readS3StructureDocument(context, uri) }
                }
                outcome.onSuccess { document ->
                    sourceText = document.text
                    sourceFormat = document.format
                    sourceName = document.name
                    ligandResult = null
                    apoResult = null
                    message = "Loaded ${document.name} · local analysis only."
                }.onFailure {
                    error = it.message ?: "Structure import failed."
                    message = "Structure file was not loaded."
                }
                busy = false
            }
        }
    }

    Card(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("Structure-site candidates", style = MaterialTheme.typography.titleMedium)
            Text(
                "Run bounded local ligand-proximity or apo concavity screening. Results are geometric candidates, not binding, affinity or function predictions.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(
                onClick = { picker.launch(arrayOf("*/*")) },
                enabled = !busy,
                modifier = Modifier.fillMaxWidth(),
            ) { Text(if (busy) "Working…" else "Choose PDB / mmCIF structure") }
            sourceName?.let { Text("Structure: $it", style = MaterialTheme.typography.labelMedium) }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = chain,
                    onValueChange = { chain = it.take(8) },
                    modifier = Modifier.weight(1f),
                    label = { Text("Ligand chain") },
                    singleLine = true,
                )
                OutlinedTextField(
                    value = residueNumber,
                    onValueChange = { residueNumber = it.filter { ch -> ch.isDigit() || ch == '-' }.take(8) },
                    modifier = Modifier.weight(1f),
                    label = { Text("Residue number") },
                    singleLine = true,
                )
                OutlinedTextField(
                    value = residueName,
                    onValueChange = { residueName = it.uppercase(Locale.ROOT).take(8) },
                    modifier = Modifier.weight(1f),
                    label = { Text("Residue name") },
                    singleLine = true,
                )
            }
            OutlinedTextField(
                value = cutoff,
                onValueChange = { cutoff = it.take(8) },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("Ligand contact cutoff (Å)") },
                singleLine = true,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = {
                        val source = sourceText
                        val residue = residueNumber.toIntOrNull()
                        val distance = cutoff.toDoubleOrNull()
                        if (source == null) {
                            error = "Choose a structure file first."
                        } else if (residue == null || distance == null || chain.isBlank() || residueName.isBlank()) {
                            error = "Enter a valid ligand chain, residue number/name and positive cutoff."
                        } else {
                            busy = true
                            error = null
                            ligandResult = null
                            scope.launch {
                                val outcome = withContext(Dispatchers.IO) {
                                    runCatching {
                                        S3S8Runner.analyzeLigandSite(
                                            context, source, sourceFormat, chain, residue,
                                            residueName, distance,
                                        )
                                    }
                                }
                                outcome.onSuccess { ligandResult = it }
                                    .onFailure { error = it.message ?: "Ligand-site screening failed." }
                                busy = false
                            }
                        }
                    },
                    enabled = !busy && sourceText != null,
                    modifier = Modifier.weight(1f),
                ) { Text("Screen ligand site") }
                Button(
                    onClick = {
                        val source = sourceText
                        if (source == null) {
                            error = "Choose a structure file first."
                        } else {
                            busy = true
                            error = null
                            apoResult = null
                            scope.launch {
                                val outcome = withContext(Dispatchers.IO) {
                                    runCatching { S3S8Runner.analyzeApoPockets(context, source, sourceFormat) }
                                }
                                outcome.onSuccess { apoResult = it }
                                    .onFailure { error = it.message ?: "Apo-pocket screening failed." }
                                busy = false
                            }
                        }
                    },
                    enabled = !busy && sourceText != null,
                    modifier = Modifier.weight(1f),
                ) { Text("Screen apo cavities") }
            }
            Text(message, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
            ligandResult?.let { result ->
                HorizontalDivider()
                Text("Ligand-site result · ${result.optString("status")}", fontWeight = androidx.compose.ui.text.font.FontWeight.SemiBold)
                result.optJSONObject("provenance")?.optString("source_sha256")?.takeIf { it.isNotBlank() }?.let {
                    Text("Input SHA-256 ${it.take(16)}…", style = MaterialTheme.typography.labelSmall)
                }
                Text("${result.optInt("candidate_residue_count")} nearby residue candidates")
                val candidates = result.optJSONArray("residue_candidates")
                if (candidates != null) {
                    for (index in 0 until minOf(candidates.length(), 8)) {
                        val item = candidates.getJSONObject(index)
                        Text(
                            "${item.optString("chain_id")}:${item.optString("residue_name")}${item.optInt("residue_number")} · min ${String.format(Locale.ROOT, "%.2f", item.optDouble("minimum_distance_angstrom"))} Å · ${item.optInt("atom_contact_count")} atom contacts",
                            style = MaterialTheme.typography.bodySmall,
                        )
                    }
                }
                Text("Geometry-only evidence. No affinity, specificity, mechanism or function is inferred.", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            apoResult?.let { result ->
                HorizontalDivider()
                Text("Apo-pocket result · ${result.optString("status")}", fontWeight = androidx.compose.ui.text.font.FontWeight.SemiBold)
                result.optJSONObject("provenance")?.optString("source_sha256")?.takeIf { it.isNotBlank() }?.let {
                    Text("Input SHA-256 ${it.take(16)}…", style = MaterialTheme.typography.labelSmall)
                }
                Text("${result.optInt("pocket_candidate_count")} coarse concavity candidates")
                val candidates = result.optJSONArray("pocket_candidates")
                if (candidates != null) {
                    for (index in 0 until minOf(candidates.length(), 5)) {
                        val item = candidates.getJSONObject(index)
                        val centroid = item.optJSONArray("centroid_angstrom")
                        val center = if (centroid != null && centroid.length() == 3) {
                            (0..2).joinToString(", ") { axis ->
                                String.format(Locale.ROOT, "%.1f", centroid.optDouble(axis))
                            }
                        } else "unknown"
                        Text(
                            "Candidate ${item.optInt("rank")} · ${item.optInt("grid_point_count")} grid points · centroid ($center) Å",
                            style = MaterialTheme.typography.bodySmall,
                        )
                    }
                }
                Text("Coarse probe-grid screen with generic atom radii. Chemical components, solvent, metals and biological assembly are not modelled.", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

private fun readGeneticCodeFasta(context: Context, uri: Uri): Pair<String, String> {
    val name = context.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)
        ?.use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }
        ?: uri.lastPathSegment ?: "sequence.fasta"
    val baseName = name.lowercase(Locale.ROOT).removeSuffix(".gz")
    require(baseName.substringAfterLast('.', "") in setOf("fa", "fasta", "fna", "fas", "txt")) {
        "Choose a FASTA sequence file (.fa, .fasta, .fna or .fas), optionally gzip-compressed."
    }
    val input = context.contentResolver.openInputStream(uri) ?: error("The selected sequence file could not be opened.")
    val decoded = if (name.endsWith(".gz", ignoreCase = true)) GZIPInputStream(input) else input
    val bytes = decoded.use { stream ->
        val output = ByteArrayOutputStream()
        val buffer = ByteArray(16 * 1024)
        var total = 0
        while (true) {
            val count = stream.read(buffer)
            if (count < 0) break
            total += count
            require(total <= S3S8Runner.MAX_FASTA_CHARS * 4) { "Sequence file exceeds the import limit." }
            output.write(buffer, 0, count)
        }
        output.toByteArray()
    }
    val text = Charsets.UTF_8.newDecoder()
        .onMalformedInput(CodingErrorAction.REPORT)
        .onUnmappableCharacter(CodingErrorAction.REPORT)
        .decode(ByteBuffer.wrap(bytes)).toString()
    require(!text.contains('\u0000')) { "Sequence file contains a NUL byte." }
    require(text.length <= S3S8Runner.MAX_FASTA_CHARS) { "Sequence file exceeds the supported character limit." }
    return name to text
}

@Composable
internal fun GeneticCodeInferenceCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var fastaText by rememberSaveable { mutableStateOf("") }
    var selectedSequenceName by rememberSaveable { mutableStateOf<String?>(null) }
    var completeCds by rememberSaveable { mutableStateOf(false) }
    var running by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    var result by remember { mutableStateOf<JSONObject?>(null) }

    val fastaPicker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            running = true
            error = null
            result = null
            scope.launch {
                val loaded = withContext(Dispatchers.IO) { runCatching { readGeneticCodeFasta(context, uri) } }
                loaded.onSuccess { (name, text) -> selectedSequenceName = name; fastaText = text }
                    .onFailure { error = it.message ?: "Could not read the selected FASTA file." }
                running = false
            }
        }
    }

    Card(Modifier.fillMaxWidth()) {
        Column(
            Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("Genetic code finder", style = MaterialTheme.typography.titleMedium)
            Text(
                "Choose a FASTA file or paste DNA sequences. Molecularis handles sequence parsing and genetic-code comparison in the background.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(onClick = { fastaPicker.launch(arrayOf("text/plain", "application/octet-stream", "*/*")) }, enabled = !running, modifier = Modifier.fillMaxWidth()) { Text("Choose DNA sequence file") }
            selectedSequenceName?.let { Text("Loaded: $it", style = MaterialTheme.typography.labelSmall) }
            OutlinedTextField(
                value = fastaText,
                onValueChange = {
                    if (it.length <= S3S8Runner.MAX_FASTA_CHARS) {
                        fastaText = it
                        error = null
                        result = null
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("DNA sequence (FASTA)") },
                minLines = 5,
                maxLines = 10,
                supportingText = { Text("Up to 1,000,000 characters. Multiple sequences supported.") },
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = completeCds, onCheckedChange = {
                    completeCds = it
                    result = null
                })
                Text("Sequences include complete start and stop codons")
            }
            Button(
                onClick = {
                    running = true
                    error = null
                    result = null
                    scope.launch {
                        val outcome = withContext(Dispatchers.IO) {
                            runCatching { S3S8Runner.inferGeneticCode(context, fastaText, completeCds) }
                        }
                        outcome.onSuccess { result = it }
                            .onFailure { error = it.message ?: "Genetic-code screening failed." }
                        running = false
                    }
                },
                enabled = !running && fastaText.isNotBlank(),
                modifier = Modifier.fillMaxWidth(),
            ) { Text(if (running) "Analysing…" else "Find likely genetic code") }
            error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
            result?.let { report ->
                HorizontalDivider()
                Text("Result · ${report.optString("status")}", fontWeight = androidx.compose.ui.text.font.FontWeight.SemiBold)
                report.optJSONObject("provenance")?.optString("source_sha256")?.takeIf { it.isNotBlank() }?.let {
                    Text("Input SHA-256 ${it.take(16)}…", style = MaterialTheme.typography.labelSmall)
                }
                Text("${report.optInt("record_count")} records · ${report.optInt("codon_count")} codons")
                if (!report.isNull("candidate_table_id")) {
                    Text(
                        "Leading candidate: NCBI table ${report.optInt("candidate_table_id")} · margin ${String.format(Locale.ROOT, "%.4f", report.optDouble("candidate_margin"))}",
                        fontWeight = androidx.compose.ui.text.font.FontWeight.SemiBold,
                    )
                } else {
                    Text("No table selected; evidence was insufficient or ambiguous.")
                }
                val ranked = report.optJSONArray("ranked_candidates")
                if (ranked != null) {
                    for (index in 0 until minOf(ranked.length(), 5)) {
                        val item = ranked.getJSONObject(index)
                        Text(
                            "Table ${item.optInt("table_id")} · ${item.optString("table_name")} · penalty ${String.format(Locale.ROOT, "%.4f", item.optDouble("penalty"))} · internal stops ${item.optInt("internal_stop_count")}",
                            style = MaterialTheme.typography.bodySmall,
                        )
                    }
                }
                val warnings = report.optJSONArray("warnings")
                if (warnings != null) {
                    for (index in 0 until warnings.length()) {
                        Text("• ${warnings.optString(index)}", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
            Text(
                "Heuristic candidate ranking only. No taxonomic, codon-usage, homolog or transcript evidence is used; no organism-specific genetic code is assigned or scientifically validated.",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}
