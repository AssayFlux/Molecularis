package org.assayflux.molecularis

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject

@Composable
internal fun PublicDatabaseCard(
    onStructureFetched: (PublicScientificRecord) -> Unit,
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val client = remember { PublicDatabaseClient() }
    val store = remember(context) { PublicRecordStore(context) }
    var query by rememberSaveable { mutableStateOf("") }
    var hits by remember { mutableStateOf(emptyList<PublicDatabaseHit>()) }
    var busy by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf("Search public reference records. Network access occurs only when you choose an action.") }
    var analysisPreview by remember { mutableStateOf<String?>(null) }
    var savedRecords by remember { mutableStateOf(store.recent()) }
    var confirmClearAll by rememberSaveable { mutableStateOf(false) }

    DisposableEffect(store) { onDispose { store.close() } }

    fun search(database: String) {
        busy = true
        analysisPreview = null
        scope.launch {
            val result = runCatching {
                withContext(Dispatchers.IO) {
                    when (database) {
                        "gene" -> client.searchNcbiGene(query)
                        "nuccore", "protein" -> client.searchNcbiSequence(database, query)
                        "uniprot" -> client.searchUniProt(query)
                        else -> error("Unsupported public database")
                    }
                }
            }
            hits = result.getOrDefault(emptyList())
            message = result.fold(
                { "${database.uppercase()}: ${it.size} results" },
                { "${database.uppercase()} search failed: ${it.message ?: "request error"}" },
            )
            busy = false
        }
    }

    fun searchGeneLinks(hit: PublicDatabaseHit, database: String) {
        busy = true
        scope.launch {
            val result = runCatching {
                withContext(Dispatchers.IO) {
                    client.searchNcbiGeneLinkedSequences(hit.accession, database)
                }
            }
            hits = result.getOrDefault(emptyList())
            message = result.fold(
                { "${hit.title}: ${it.size} linked ${if (database == "nuccore") "nucleotide" else "protein"} records" },
                { "NCBI Gene link lookup failed: ${it.message ?: "request error"}" },
            )
            busy = false
        }
    }

    fun fetchSequence(hit: PublicDatabaseHit) {
        busy = true
        analysisPreview = null
        scope.launch {
            val result = runCatching {
                withContext(Dispatchers.IO) {
                    val fetched = when {
                        hit.source == "UniProtKB" -> client.fetchUniProtFasta(hit.accession)
                        hit.database in setOf("nuccore", "protein") ->
                            client.fetchNcbiFasta(hit.database!!, hit.accession)
                        else -> error("This search result does not expose a sequence accession")
                    }
                    val saved = store.save(fetched)
                    val analysis = runCatching {
                        if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
                        Python.getInstance().getModule("molecularis_probe")
                            .callAttr("analyze_fasta", fetched.content).toString().also { json ->
                                require(JSONObject(json).optInt("record_count", 0) > 0) {
                                    "Retrieved FASTA did not produce a valid sequence analysis"
                                }
                                store.saveAnalysis(saved.id, json)
                            }
                    }
                    Pair(saved, analysis)
                }
            }
            result.fold(
                { (saved, analysis) ->
                    savedRecords = withContext(Dispatchers.IO) { store.recent() }
                    analysisPreview = analysis.getOrNull()
                        ?: "Record safely saved. The current FASTA QC engine could not process it: ${analysis.exceptionOrNull()?.message ?: "unsupported record or size limit"}"
                    message = if (analysis.isSuccess) {
                        "Retrieved, checksum-verified and encrypted locally · ${saved.source} ${saved.accession}. FASTA QC completed on-device."
                    } else {
                        "Reference sequence saved locally · ${saved.source} ${saved.accession}. QC was not completed; see the limitation below."
                    }
                },
                { error -> message = "Sequence retrieval or storage failed: ${error.message ?: error.javaClass.simpleName}" },
            )
            busy = false
        }
    }

    fun fetchStructure() {
        busy = true
        scope.launch {
            val result = runCatching {
                withContext(Dispatchers.IO) {
                    val fetched = client.fetchRcsbMmcif(query)
                    val saved = store.save(fetched)
                    Pair(fetched, saved)
                }
            }
            result.fold(
                { (fetched, saved) ->
                    savedRecords = withContext(Dispatchers.IO) { store.recent() }
                    onStructureFetched(fetched)
                    message = "RCSB structure retrieved and encrypted locally · ${saved.accession}. Opening the existing Molecularis structure parser and viewer."
                },
                { error -> message = "Structure retrieval failed: ${error.message ?: error.javaClass.simpleName}" },
            )
            busy = false
        }
    }

    Card(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("Public scientific databases", style = MaterialTheme.typography.titleMedium)
            Text(
                "Search and retrieve reference sequences and structures directly inside Molecularis. Retrieved source records are checksum-verified and encrypted in app-private storage.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                "Search public names and accessions only. Do not enter patient/sample identifiers or raw sequences.",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("Gene, protein, accession or PDB ID") },
                singleLine = true,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                OutlinedButton(enabled = !busy && query.trim().length >= 2, modifier = Modifier.weight(1f), onClick = { search("gene") }) { Text("NCBI genes") }
                OutlinedButton(enabled = !busy && query.trim().length >= 2, modifier = Modifier.weight(1f), onClick = { search("nuccore") }) { Text("Nucleotide") }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                OutlinedButton(enabled = !busy && query.trim().length >= 2, modifier = Modifier.weight(1f), onClick = { search("protein") }) { Text("NCBI protein") }
                OutlinedButton(enabled = !busy && query.trim().length >= 2, modifier = Modifier.weight(1f), onClick = { search("uniprot") }) { Text("UniProtKB") }
            }
            Button(
                enabled = !busy && query.trim().matches(Regex("[0-9][A-Za-z0-9]{3}")),
                modifier = Modifier.fillMaxWidth(),
                onClick = { fetchStructure() },
            ) { Text("Retrieve RCSB PDB structure") }

            if (busy) CircularProgressIndicator()
            Text(message, style = MaterialTheme.typography.bodySmall)
            hits.take(8).forEach { hit ->
                Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                    Text(hit.title, style = MaterialTheme.typography.bodyMedium)
                    Text(
                        listOfNotNull(hit.source, hit.accession, hit.organism).joinToString(" · "),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    hit.description?.let {
                        Text(it, style = MaterialTheme.typography.bodySmall, maxLines = 2, overflow = TextOverflow.Ellipsis)
                    }
                    if (hit.source == "NCBI Gene") {
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            TextButton(enabled = !busy, onClick = { searchGeneLinks(hit, "nuccore") }) { Text("Find nucleotide") }
                            TextButton(enabled = !busy, onClick = { searchGeneLinks(hit, "protein") }) { Text("Find protein") }
                        }
                    }
                    if (hit.source == "UniProtKB" || hit.database in setOf("nuccore", "protein")) {
                        TextButton(enabled = !busy, onClick = { fetchSequence(hit) }) { Text("Retrieve and analyse sequence") }
                    }
                }
            }
            analysisPreview?.let { json ->
                Text("On-device FASTA QC", style = MaterialTheme.typography.titleSmall)
                Text(
                    json.take(3000),
                    modifier = Modifier.fillMaxWidth().heightIn(max = 220.dp).verticalScroll(rememberScrollState()),
                    style = MaterialTheme.typography.bodySmall,
                )
            }
            if (savedRecords.isNotEmpty()) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Saved public records", style = MaterialTheme.typography.titleSmall)
                    TextButton(enabled = !busy, onClick = { confirmClearAll = true }) { Text("Clear all") }
                }
                savedRecords.forEach { saved ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                            Text("${saved.source} · ${saved.accession}", style = MaterialTheme.typography.bodySmall)
                            Text(
                                "${saved.format} · ${saved.byteCount} bytes · SHA-256 ${saved.sha256.take(12)}…",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                        if (saved.format.equals("mmCIF", ignoreCase = true)) {
                            TextButton(
                                enabled = !busy,
                                onClick = {
                                    scope.launch {
                                        val opened = runCatching {
                                            withContext(Dispatchers.IO) { store.loadRecord(saved.id) }
                                        }
                                        opened.fold(
                                            { loaded ->
                                                if (loaded != null) {
                                                    onStructureFetched(loaded)
                                                    message = "Saved RCSB structure reopened from encrypted local storage."
                                                } else {
                                                    message = "Saved structure is no longer available."
                                                }
                                            },
                                            { error ->
                                                message = "Saved structure could not be authenticated: ${error.message ?: "local storage error"}"
                                            },
                                        )
                                    }
                                },
                            ) { Text("Open") }
                        }
                        if (saved.format.equals("FASTA", ignoreCase = true)) {
                            TextButton(
                                enabled = !busy,
                                onClick = {
                                    busy = true
                                    scope.launch {
                                        val analysis = runCatching {
                                            withContext(Dispatchers.IO) {
                                                val loaded = store.loadRecord(saved.id)
                                                    ?: error("Saved FASTA record is unavailable")
                                                if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
                                                Python.getInstance().getModule("molecularis_probe")
                                                    .callAttr("analyze_fasta", loaded.content).toString()
                                                    .also { json ->
                                                        require(JSONObject(json).optInt("record_count", 0) > 0)
                                                        store.saveAnalysis(saved.id, json)
                                                    }
                                            }
                                        }
                                        analysisPreview = analysis.getOrNull()
                                        message = analysis.fold(
                                            { "Saved sequence reopened, re-analysed locally and result updated." },
                                            { "Saved sequence could not be re-analysed: ${it.message ?: it.javaClass.simpleName}" },
                                        )
                                        savedRecords = withContext(Dispatchers.IO) { store.recent() }
                                        busy = false
                                    }
                                },
                            ) { Text("Reanalyse") }
                        }
                        TextButton(
                            enabled = !busy,
                            onClick = {
                                scope.launch {
                                    val deleted = withContext(Dispatchers.IO) { store.delete(saved.id) }
                                    savedRecords = withContext(Dispatchers.IO) { store.recent() }
                                    message = if (deleted) "Saved record deleted from this device." else "Saved record could not be deleted."
                                }
                            },
                        ) { Text("Delete") }
                    }
                }
            }
            Text(
                "Only public search terms and accessions are sent to providers. Imported patient data is never uploaded. Local cache is user-deletable.",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
    if (confirmClearAll) {
        AlertDialog(
            onDismissRequest = { confirmClearAll = false },
            title = { Text("Clear saved public records?") },
            text = { Text("This deletes locally cached public reference payloads and their saved analysis metadata. It does not affect imported research jobs.") },
            confirmButton = {
                TextButton(onClick = {
                    confirmClearAll = false
                    scope.launch {
                        val deleted = withContext(Dispatchers.IO) { store.deleteAll() }
                        savedRecords = withContext(Dispatchers.IO) { store.recent() }
                        message = "Deleted $deleted saved public reference records."
                    }
                }) { Text("Clear all") }
            },
            dismissButton = { TextButton(onClick = { confirmClearAll = false }) { Text("Cancel") } },
        )
    }
}
