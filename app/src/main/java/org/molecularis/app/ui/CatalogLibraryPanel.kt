package org.molecularis.app.ui

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Job
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.withContext
import kotlinx.coroutines.launch
import org.molecularis.app.BuildConfig
import org.molecularis.app.features.*
import java.io.File

@Composable
fun CatalogLibraryPanel(onInstalled: (ModelCatalogEntry, File) -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val scope = rememberCoroutineScope()
    var entries by remember { mutableStateOf(emptyList<ModelCatalogEntry>()) }
    var status by remember { mutableStateOf("Signed publisher catalog is not configured in this build.") }
    var loading by remember { mutableStateOf(false) }
    var installing by remember { mutableStateOf<String?>(null) }
    var installJob by remember { mutableStateOf<Job?>(null) }
    var downloadProgress by remember { mutableFloatStateOf(0f) }
    var downloadLabel by remember { mutableStateOf("") }
    var finalizingInstall by remember { mutableStateOf(false) }
    var compatibility by remember { mutableStateOf<Map<String, ModelCompatibility>>(emptyMap()) }
    val configured = BuildConfig.MODEL_CATALOG_URL.isNotBlank() && BuildConfig.MODEL_CATALOG_PUBLIC_KEY.isNotBlank()

    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text("Verified model catalog", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
            Text(
                "Publisher-signed model metadata, HTTPS downloads and SHA-256 verification. A catalog signature authenticates metadata; it does not guarantee that every artifact runtime is installed.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        if (configured) {
            OutlinedButton(
                onClick = {
                    loading = true
                    scope.launch {
                        try {
                            val catalog = ModelCatalogClient(
                                context,
                                BuildConfig.MODEL_CATALOG_URL,
                                BuildConfig.MODEL_CATALOG_PUBLIC_KEY
                            ).fetch()
                            entries = catalog.models
                            val checker = ModelCompatibilityChecker(context)
                            compatibility = entries.associate { it.id to checker.check(it) }
                            status = "Signature verified · ${entries.size} models · payload SHA-256 ${catalog.payloadSha256.take(16)}…"
                        } catch (cancelled: CancellationException) {
                            throw cancelled
                        } catch (error: Exception) {
                            status = "Catalog verification failed: ${error.message ?: error.javaClass.simpleName}"
                            entries = emptyList()
                        } finally {
                            loading = false
                        }
                    }
                },
                enabled = !loading && installing == null,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (loading) CircularProgressIndicator(Modifier.size(18.dp), strokeWidth = 2.dp)
                else Icon(Icons.Default.Verified, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text(if (loading) "Verifying publisher signature…" else "Refresh signed catalog")
            }
        } else {
            ElevatedCard {
                Row(Modifier.padding(14.dp), horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.Top) {
                    Icon(Icons.Default.Key, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text("Publisher setup required", fontWeight = FontWeight.SemiBold)
                        Text(
                            "Configure MOLECULARIS_CATALOG_URL and MOLECULARIS_CATALOG_PUBLIC_KEY as Gradle properties. Keep the Ed25519 private signing key offline or in a protected publisher environment; never place it in the app.",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }

        if (status.isNotBlank()) {
            Text(status, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
        }

        entries.forEach { entry ->
            val check = compatibility[entry.id]
            var licenseAccepted by remember(entry.id, entry.version) { mutableStateOf(false) }
            val installedVersions = remember(entry.id) {
                mutableStateListOf<InstalledModelVersion>().apply {
                    addAll(ModelInstallStore(context).list(entry.id))
                }
            }
            val activeInstalled = installedVersions.firstOrNull { it.active }
            val thisInstalling = installing == entry.id

            ElevatedCard(Modifier.fillMaxWidth()) {
                Column(
                    Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(9.dp)
                ) {
                    Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Surface(
                            color = MaterialTheme.colorScheme.secondaryContainer,
                            shape = MaterialTheme.shapes.medium
                        ) {
                            Icon(
                                if (entry.capabilities.contains(ModelCapability.VISION)) Icons.Default.Visibility
                                else if (entry.capabilities.contains(ModelCapability.CODE)) Icons.Default.Code
                                else Icons.Default.Psychology,
                                contentDescription = null,
                                modifier = Modifier.padding(10.dp).size(22.dp),
                                tint = MaterialTheme.colorScheme.onSecondaryContainer
                            )
                        }
                        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            Text(entry.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                            Text(
                                "${entry.publisher} · v${entry.version}",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        if (activeInstalled != null) {
                            Surface(
                                color = MaterialTheme.colorScheme.primaryContainer,
                                shape = MaterialTheme.shapes.small
                            ) {
                                Row(
                                    Modifier.padding(horizontal = 8.dp, vertical = 5.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                                ) {
                                    Icon(Icons.Default.CheckCircle, contentDescription = null, modifier = Modifier.size(14.dp))
                                    Text("Installed", style = MaterialTheme.typography.labelSmall)
                                }
                            }
                        }
                    }

                    Text(entry.description, style = MaterialTheme.typography.bodyMedium)
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                        listOf(entry.format.uppercase(), entry.quantization, formatCatalogSize(entry.sizeBytes)).forEach { label ->
                            Surface(color = MaterialTheme.colorScheme.surfaceVariant, shape = MaterialTheme.shapes.small) {
                                Text(
                                    label,
                                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 5.dp),
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                    Text(
                        "Architecture: ${entry.architecture} · Minimum Android: ${entry.minSdk} · RAM requirement: ${entry.minRamMb} MiB",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        "Capabilities: ${entry.capabilities.joinToString { it.name.lowercase().replace('_', ' ') }}",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    TextButton(onClick = {
                        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(entry.licenseUrl)))
                    }) {
                        Icon(Icons.Default.Description, contentDescription = null)
                        Spacer(Modifier.width(6.dp))
                        Text("Review ${entry.license} license")
                    }

                    if (check != null && !check.compatible) {
                        check.reasons.forEach { reason ->
                            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.Top) {
                                Icon(Icons.Default.WarningAmber, contentDescription = null, tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(17.dp))
                                Text(reason, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    } else if (check?.runtimeAvailable == true) {
                        Text("Device requirements passed · runtime available", color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelSmall)
                    } else if (check?.compatible == true) {
                        Text("Download compatible · execution runtime is not bundled in this build", color = MaterialTheme.colorScheme.tertiary, style = MaterialTheme.typography.bodySmall)
                    }

                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = licenseAccepted, onCheckedChange = { licenseAccepted = it })
                        Text("I have reviewed and accept this model license", style = MaterialTheme.typography.bodySmall)
                    }

                    if (thisInstalling) {
                        if (finalizingInstall) {
                            LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
                            Text("Verifying and installing the completed download…", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        } else {
                            LinearProgressIndicator(
                                progress = downloadProgress,
                                modifier = Modifier.fillMaxWidth()
                            )
                            Text(downloadLabel, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            OutlinedButton(
                                onClick = {
                                    status = "Download cancelled. Any partial transfer remains private and can be resumed."
                                    installJob?.cancel()
                                },
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Icon(Icons.Default.Close, contentDescription = null)
                                Spacer(Modifier.width(8.dp))
                                Text("Cancel download")
                            }
                        }
                    } else {
                        Button(
                            onClick = {
                                installing = entry.id
                                finalizingInstall = false
                                downloadProgress = 0f
                                downloadLabel = "Preparing secure download…"
                                installJob = scope.launch {
                                    try {
                                        val downloaded = VerifiedModelDownloader(context).download(
                                            entry.downloadUrl,
                                            entry.sha256,
                                            entry.fileName
                                        ) { bytes, total ->
                                            downloadProgress = if (total != null && total > 0L) {
                                                (bytes.toFloat() / total).coerceIn(0f, 1f)
                                            } else 0f
                                            downloadLabel = if (total != null && total > 0L) {
                                                "${formatCatalogSize(bytes)} of ${formatCatalogSize(total)}"
                                            } else {
                                                "${formatCatalogSize(bytes)} downloaded"
                                            }
                                        }
                                        finalizingInstall = true
                                        val store = ModelInstallStore(context)
                                        val callerJob = currentCoroutineContext()[Job]
                                        val installed = withContext(Dispatchers.IO) {
                                            store.install(entry, downloaded.file) {
                                                if (callerJob?.isActive == false) {
                                                    throw CancellationException("Model installation was cancelled.")
                                                }
                                            }
                                        }
                                        val currentVersions = withContext(Dispatchers.IO) { store.list(entry.id) }
                                        installedVersions.clear()
                                        installedVersions.addAll(currentVersions)
                                        onInstalled(entry, installed.file)
                                        status = "Installed ${entry.name} ${entry.version}; SHA-256 verified."
                                    } catch (cancelled: CancellationException) {
                                        throw cancelled
                                    } catch (error: Exception) {
                                        status = "Install failed: ${error.message ?: error.javaClass.simpleName}"
                                    } finally {
                                        installing = null
                                        installJob = null
                                        downloadProgress = 0f
                                        downloadLabel = ""
                                        finalizingInstall = false
                                    }
                                }
                            },
                            enabled = check?.compatible == true && installing == null &&
                                licenseAccepted && activeInstalled?.version != entry.version,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Icon(Icons.Default.Download, contentDescription = null)
                            Spacer(Modifier.width(8.dp))
                            Text(if (activeInstalled != null) "Update model" else "Download and install")
                        }
                    }

                    if (installedVersions.any { !it.active }) {
                        OutlinedButton(
                            onClick = {
                                try {
                                    val rolledBack = ModelInstallStore(context).rollback(entry.id)
                                    installedVersions.clear()
                                    installedVersions.addAll(ModelInstallStore(context).list(entry.id))
                                    onInstalled(entry, rolledBack.file)
                                    status = "Rolled back ${entry.id} to ${rolledBack.version}."
                                } catch (error: Exception) {
                                    status = "Rollback failed: ${error.message ?: error.javaClass.simpleName}"
                                }
                            },
                            enabled = installing == null,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Icon(Icons.Default.History, contentDescription = null)
                            Spacer(Modifier.width(8.dp))
                            Text("Rollback to previous version")
                        }
                    }
                }
            }
        }
    }
}

private fun formatCatalogSize(bytes: Long): String = when {
    bytes >= 1_073_741_824L -> "%.1f GB".format(bytes / 1_073_741_824.0)
    bytes >= 1_048_576L -> "%.0f MB".format(bytes / 1_048_576.0)
    else -> "%.0f KB".format(bytes / 1024.0)
}
