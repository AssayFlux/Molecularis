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
import java.util.zip.GZIPInputStream

private data class VcfQcDocument(val name: String, val text: String)

private fun readVcfQcDocument(context: Context, uri: Uri): VcfQcDocument {
    val name = context.contentResolver.query(
        uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
    )?.use { cursor ->
        if (cursor.moveToFirst()) cursor.getString(0) else null
    } ?: uri.lastPathSegment ?: "variants.vcf"
    require(name.endsWith(".vcf", ignoreCase = true) || name.endsWith(".vcf.gz", ignoreCase = true)) {
        "Select a .vcf or .vcf.gz file."
    }
    val input = context.contentResolver.openInputStream(uri)
        ?: error("The selected VCF document could not be opened.")
    val decodedInput = if (name.endsWith(".gz", ignoreCase = true)) GZIPInputStream(input) else input
    val bytes = decodedInput.use { stream ->
        val output = ByteArrayOutputStream()
        val buffer = ByteArray(16 * 1024)
        var total = 0
        while (true) {
            val count = stream.read(buffer)
            if (count < 0) break
            total += count
            require(total <= GenomicsVcfQcRunner.MAX_INPUT_BYTES) {
                "Expanded VCF input exceeds the 5 MiB processing limit."
            }
            output.write(buffer, 0, count)
        }
        output.toByteArray()
    }
    val text = Charsets.UTF_8.newDecoder()
        .onMalformedInput(CodingErrorAction.REPORT)
        .onUnmappableCharacter(CodingErrorAction.REPORT)
        .decode(ByteBuffer.wrap(bytes)).toString()
    require(!text.contains('\u0000')) { "VCF input contains a NUL byte." }
    return VcfQcDocument(name, text)
}

/** P1 aggregate-only VCF syntax/QC surface; no sample-level result is exposed. */
@Composable
internal fun GenomicsVcfQcCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var authorizationConfirmed by rememberSaveable { mutableStateOf(false) }
    var selectedUri by remember { mutableStateOf<Uri?>(null) }
    var selectedName by remember { mutableStateOf<String?>(null) }
    var report by remember { mutableStateOf<JSONObject?>(null) }
    var status by remember { mutableStateOf("Choose a VCF dataset covered by your institutional research authorization.") }
    var error by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        selectedUri = uri
        selectedName = uri?.let {
            runCatching {
                context.contentResolver.query(
                    it, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
                )?.use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }
            }.getOrNull()
        }
        authorizationConfirmed = false
        report = null
        error = null
        status = if (uri == null) "No file selected." else "File selected. Confirm the data boundary before running aggregate QC."
    }

    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("VCF aggregate research QC", style = MaterialTheme.typography.titleMedium)
            Text(
                "Bounded local VCF record-structure and aggregate summary. Only aggregate counts are returned; sample identifiers and genotype strings are not displayed or persisted.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(
                onClick = { picker.launch(arrayOf("text/vcf", "text/plain", "*/*")) },
                enabled = !busy,
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Choose VCF / VCF.GZ file") }
            selectedName?.let { Text("File: $it", style = MaterialTheme.typography.labelMedium) }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = authorizationConfirmed, onCheckedChange = {
                    authorizationConfirmed = it
                    report = null
                })
                Text(
                    "I confirm I am authorized under the applicable institutional approval to use this dataset for this research.",
                    style = MaterialTheme.typography.bodySmall,
                )
            }
            Text(
                "This is an operator attestation, not automated verification. Use only data within the approved protocol, with required consent, access controls and data minimisation. Do not use this exploratory QC output for diagnosis or treatment decisions.",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(
                onClick = {
                    val uri = selectedUri ?: return@Button
                    busy = true
                    error = null
                    report = null
                    status = "Checking VCF record structure locally…"
                    scope.launch {
                        val outcome = withContext(Dispatchers.IO) {
                            runCatching {
                                val document = readVcfQcDocument(context, uri)
                                document.name to GenomicsVcfQcRunner.analyze(context, document.text)
                            }
                        }
                        outcome.onSuccess {
                            selectedName = it.first
                            report = it.second
                            status = "Aggregate QC completed in memory. Input text was not saved by this screen."
                        }.onFailure {
                            error = it.message ?: "VCF QC failed."
                            status = "No result was produced."
                        }
                        busy = false
                    }
                },
                enabled = !busy && selectedUri != null && authorizationConfirmed,
                modifier = Modifier.fillMaxWidth(),
            ) { Text(if (busy) "Checking…" else "Run aggregate QC") }
            Text(status, style = MaterialTheme.typography.bodySmall)
            error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
            report?.let { result ->
                HorizontalDivider()
                Text(
                    "${result.optInt("record_count")} variant records · ${result.optInt("contig_count")} contigs · ${result.optInt("sample_count")} sample columns",
                    fontWeight = androidx.compose.ui.text.font.FontWeight.SemiBold,
                )
                Text(
                    "SNV records ${result.optInt("snv_record_count")} · multiallelic ${result.optInt("multiallelic_record_count")} · missing QUAL ${result.optInt("missing_quality_record_count")}",
                    style = MaterialTheme.typography.bodySmall,
                )
                Text("FILTER counts", style = MaterialTheme.typography.labelLarge)
                result.optJSONObject("filter_counts")?.let { counts ->
                    counts.keys().asSequence().sorted().forEach { key ->
                        Text("$key · ${counts.optInt(key)}", style = MaterialTheme.typography.bodySmall)
                    }
                }
                Text("Contig counts", style = MaterialTheme.typography.labelLarge)
                result.optJSONObject("contig_record_counts")?.let { counts ->
                    counts.keys().asSequence().sorted().forEach { key ->
                        Text("$key · ${counts.optInt(key)}", style = MaterialTheme.typography.bodySmall)
                    }
                }
                Text("Input SHA-256 · ${result.optString("source_sha256")}", style = MaterialTheme.typography.labelSmall)
                val limitations = result.optJSONArray("limitations")
                if (limitations != null) {
                    for (index in 0 until limitations.length()) {
                        Text("• ${limitations.optString(index)}", style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}
