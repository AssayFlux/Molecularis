package org.assayflux.molecularis

import android.os.Bundle
import androidx.fragment.app.FragmentActivity
import androidx.activity.enableEdgeToEdge
import androidx.activity.compose.setContent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkInfo
import androidx.work.WorkManager
import androidx.work.workDataOf
import java.util.UUID
import java.io.File
import java.security.MessageDigest
import androidx.lifecycle.Observer
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : FragmentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { MolecularisResearchHome(this) }
    }
}

@androidx.compose.runtime.Composable
private fun MolecularisResearchHome(activity: FragmentActivity) {
    val preferences = remember {
        activity.getSharedPreferences("molecularis_preferences", android.content.Context.MODE_PRIVATE)
    }
    var themeFamily by remember {
        mutableStateOf(preferences.getString("theme_family", "system") ?: "system")
    }
    var onboardingComplete by remember {
        mutableStateOf(preferences.getBoolean("onboarding_complete", false))
    }
    var biometricEnabled by remember {
        mutableStateOf(preferences.getBoolean("biometric_unlock_enabled", false))
    }
    var biometricUnlocked by remember { mutableStateOf(true) }
    var biometricError by remember { mutableStateOf<String?>(null) }
    DisposableEffect(activity, biometricEnabled, onboardingComplete) {
        var hasBackgrounded = false
        val observer = LifecycleEventObserver { _, event ->
            if (biometricEnabled && onboardingComplete) {
                when (event) {
                    Lifecycle.Event.ON_STOP -> {
                        hasBackgrounded = true
                        biometricUnlocked = false
                        biometricError = null
                    }
                    Lifecycle.Event.ON_START -> if (hasBackgrounded) {
                        hasBackgrounded = false
                        biometricUnlocked = false
                        biometricError = null
                        BiometricUnlock.authenticate(
                            activity,
                            onSuccess = { biometricUnlocked = true; biometricError = null },
                            onError = { biometricError = it },
                        )
                    }
                    else -> Unit
                }
            }
        }
        activity.lifecycle.addObserver(observer)
        onDispose { activity.lifecycle.removeObserver(observer) }
    }
    LaunchedEffect(biometricEnabled, onboardingComplete) {
        if (biometricEnabled && onboardingComplete) {
            biometricUnlocked = false
            biometricError = null
            BiometricUnlock.authenticate(
                activity,
                onSuccess = { biometricUnlocked = true; biometricError = null },
                onError = { biometricError = it },
            )
        } else {
            biometricUnlocked = true
            biometricError = null
        }
    }
    val store = remember { ResearchStore(activity) }
    var jobs by remember { mutableStateOf(store.recentJobs()) }
    var notice by remember { mutableStateOf("Caution: Use only datasets covered by your institutional approval. Research outputs are not clinically validated.") }
    var runtimeReport by remember { mutableStateOf<String?>(null) }
    var deleteTarget by remember { mutableStateOf<ResearchJob?>(null) }
    val scope = rememberCoroutineScope()
    var pendingExportJob by remember { mutableStateOf<String?>(null) }
    var pendingProvenanceExportJob by remember { mutableStateOf<String?>(null) }
    var pendingProvenanceSummaryJob by remember { mutableStateOf<String?>(null) }
    var pendingAnalysisExportJob by remember { mutableStateOf<String?>(null) }
    val exportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/octet-stream"),
    ) { uri ->
        val jobId = pendingExportJob
        pendingExportJob = null
        if (uri != null && jobId != null) {
            scope.launch {
                notice = "Exporting verified research input..."
                notice = withContext(Dispatchers.IO) {
                    val exportResult = runCatching {
                        val output = activity.contentResolver.openOutputStream(uri, "wt")
                            ?: error("Selected export destination could not be opened")
                        output.use { stream ->
                            check(store.exportStoredInput(jobId, stream)) {
                                "No completed encrypted input exists for this job"
                            }
                        }
                    }
                    exportResult.fold(
                        { "Verified research input exported successfully." },
                        { error ->
                            // SAF providers differ in whether they support document deletion.
                            // Remove a failed partial export where possible; never claim cleanup
                            // if the provider refuses or does not implement deletion.
                            val removed = runCatching {
                                android.provider.DocumentsContract.deleteDocument(
                                    activity.contentResolver, uri,
                                )
                            }.getOrDefault(false)
                            val detail = error.message ?: error.javaClass.simpleName
                            if (removed) {
                                "Export failed: $detail. The incomplete destination was removed."
                            } else {
                                "Export failed: $detail. The destination may contain partial data; " +
                                    "delete that document manually before retrying."
                            }
                        },
                    )
                }
            }
        }
    }

    val provenanceExportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/json"),
    ) { uri ->
        val jobId = pendingProvenanceExportJob
        pendingProvenanceExportJob = null
        if (uri != null && jobId != null) {
            scope.launch {
                notice = "Exporting import provenance..."
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        val json = store.provenanceJson(jobId)
                            ?: error("No provenance record exists for this job")
                        val output = activity.contentResolver.openOutputStream(uri, "wt")
                            ?: error("Selected provenance destination could not be opened")
                        output.use { stream ->
                            stream.write(json.toByteArray(Charsets.UTF_8))
                            stream.flush()
                        }
                    }
                }
                notice = result.fold(
                    { "Import provenance JSON exported. The source URI and input contents are not included." },
                    { error ->
                        val removed = runCatching {
                            android.provider.DocumentsContract.deleteDocument(activity.contentResolver, uri)
                        }.getOrDefault(false)
                        val detail = error.message ?: error.javaClass.simpleName
                        if (removed) {
                            "Provenance export failed: $detail. The incomplete destination was removed."
                        } else {
                            "Provenance export failed: $detail. The destination may be partial; delete it manually before retrying."
                        }
                    },
                )
            }
        }
    }

    val analysisExportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/json"),
    ) { uri ->
        val jobId = pendingAnalysisExportJob
        pendingAnalysisExportJob = null
        if (uri != null && jobId != null) {
            scope.launch {
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        val json = store.analysisExportJson(jobId) ?: error("No saved analysis result exists")
                        val output = activity.contentResolver.openOutputStream(uri, "wt")
                            ?: error("Selected analysis destination could not be opened")
                        output.use { stream -> stream.write(json.toByteArray(Charsets.UTF_8)); stream.flush() }
                    }
                }
                notice = result.fold(
                    { "Analysis result and source-hash provenance exported." },
                    { error ->
                        val removed = runCatching {
                            android.provider.DocumentsContract.deleteDocument(activity.contentResolver, uri)
                        }.getOrDefault(false)
                        val detail = error.message ?: error.javaClass.simpleName
                        if (removed) "Analysis export failed: $detail. Incomplete destination removed."
                        else "Analysis export failed: $detail. Destination may be partial; remove it manually."
                    },
                )
            }
        }
    }

    val provenanceSummaryPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("text/plain"),
    ) { uri ->
        val jobId = pendingProvenanceSummaryJob
        pendingProvenanceSummaryJob = null
        if (uri != null && jobId != null) {
            scope.launch {
                notice = "Exporting human-readable provenance summary..."
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        val summary = store.provenanceSummary(jobId)
                            ?: error("No provenance record exists for this job")
                        val output = activity.contentResolver.openOutputStream(uri, "wt")
                            ?: error("Selected summary destination could not be opened")
                        output.use { stream ->
                            stream.write(summary.toByteArray(Charsets.UTF_8))
                            stream.flush()
                        }
                    }
                }
                notice = result.fold(
                    { "Human-readable provenance summary exported. Source URI and input contents are excluded." },
                    { error ->
                        val removed = runCatching {
                            android.provider.DocumentsContract.deleteDocument(activity.contentResolver, uri)
                        }.getOrDefault(false)
                        val detail = error.message ?: error.javaClass.simpleName
                        if (removed) {
                            "Summary export failed: $detail. The incomplete destination was removed."
                        } else {
                            "Summary export failed: $detail. The destination may be partial; delete it manually before retrying."
                        }
                    },
                )
            }
        }
    }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            val persistentReadGrant = runCatching {
                activity.contentResolver.takePersistableUriPermission(
                    uri, android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }.isSuccess
            if (!persistentReadGrant) {
                notice = "This document provider did not grant persistent read access. Choose a file from a provider that supports resumable access."
                return@rememberLauncherForActivityResult
            }
            val id = UUID.randomUUID().toString()
            val name = uri.lastPathSegment ?: "Imported document"
            store.createJob(id, name, uri.toString())
            val request = OneTimeWorkRequestBuilder<ImportWorker>()
                .setInputData(workDataOf(ImportWorker.KEY_JOB_ID to id, ImportWorker.KEY_URI to uri.toString()))
                .addTag("kinetics-import").build()
            WorkManager.getInstance(activity).enqueueUniqueWork(
                "import-$id", ExistingWorkPolicy.KEEP, request)
            notice = "Import queued. The file will be streamed, encrypted at rest and hashed in the background."
            jobs = store.recentJobs()
        }
    }
    DisposableEffect(activity) {
        val manager = WorkManager.getInstance(activity)
        // Detect definite Keystore key loss before exposing encrypted jobs. An unavailable
        // Keystore is treated as unknown, never as proof that the key was deleted.
        if (LocalCrypto.existingKeyStatus() == false) {
            val affected = store.markKeyLossRecoveryRequired()
            if (affected > 0) {
                notice = "$affected encrypted record(s) require key recovery. Ciphertext was preserved."
            }
        }
        // Recover imports interrupted by process death. KEEP prevents duplicate workers
        // when WorkManager already has an unfinished unique job.
        store.recoverableImports().forEach { pending ->
            val uri = android.net.Uri.parse(pending.uri)
            val hasReadGrant = activity.contentResolver.persistedUriPermissions.any {
                it.uri == uri && it.isReadPermission
            }
            if (!hasReadGrant) {
                store.updateJob(
                    pending.id, "failed",
                    message = "Recovery blocked: persistent document read permission was revoked",
                )
            } else {
                val request = OneTimeWorkRequestBuilder<ImportWorker>()
                    .setInputData(workDataOf(
                        ImportWorker.KEY_JOB_ID to pending.id,
                        ImportWorker.KEY_URI to pending.uri,
                    ))
                    .addTag("kinetics-import")
                    .build()
                manager.enqueueUniqueWork(
                    "import-${pending.id}", ExistingWorkPolicy.KEEP, request,
                )
            }
        }
        val workInfos = manager.getWorkInfosByTagLiveData("kinetics-import")
        val analysisInfos = manager.getWorkInfosByTagLiveData("kinetics-analysis")
        val observer = Observer<List<WorkInfo>> { jobs = store.recentJobs() }
        workInfos.observe(activity, observer)
        analysisInfos.observe(activity, observer)
        jobs = store.recentJobs()
        onDispose { workInfos.removeObserver(observer); analysisInfos.removeObserver(observer) }
    }
    if (!onboardingComplete) {
        MolecularisOnboardingScreen(
            themeFamily = themeFamily,
            onComplete = {
                preferences.edit().putBoolean("onboarding_complete", true).apply()
                onboardingComplete = true
            },
        )
    } else if (biometricEnabled && !biometricUnlocked) {
        BiometricLockScreen(
            error = biometricError,
            themeFamily = themeFamily,
            onRetry = {
                biometricError = null
                BiometricUnlock.authenticate(
                    activity,
                    onSuccess = { biometricUnlocked = true; biometricError = null },
                    onError = { biometricError = it },
                )
            },
        )
    } else MolecularisAppShell(
        jobs = jobs,
        notice = notice,
        runtimeReport = runtimeReport,
        onImport = { picker.launch(arrayOf("*/*")) },
        onRefresh = { jobs = store.recentJobs() },
        onRunRuntime = {
            scope.launch {
                runtimeReport = "Running local Python and native runtime probes..."
                runtimeReport = withContext(Dispatchers.IO) {
                    val python = runCatching { PythonProbe.report(activity) }
                        .getOrElse { "FAILED: ${it.message ?: it.javaClass.simpleName}" }
                    val native = runCatching {
                        val probe = NativeProbe()
                        val cpp = probe.cppSumSquares(3.0, 4.0)
                        val rust = probe.rustSumSquares(3.0, 4.0)
                        check(kotlin.math.abs(cpp - 25.0) < 1e-9) { "C++ JNI result mismatch" }
                        check(kotlin.math.abs(rust - 25.0) < 1e-9) { "Rust FFI result mismatch" }
                        val aad = LocalCrypto.associatedData("runtime-probe", 0)
                        val plaintext = "kinetics-keystore-probe".toByteArray()
                        val encrypted = LocalCrypto.encrypt(plaintext, aad)
                        check(LocalCrypto.decrypt(encrypted, aad).contentEquals(plaintext)) {
                            "Android Keystore AES-GCM roundtrip mismatch"
                        }
                        val wrongAadRejected = runCatching {
                            LocalCrypto.decrypt(encrypted, LocalCrypto.associatedData("wrong-job", 0))
                        }.isFailure
                        check(wrongAadRejected) { "AES-GCM did not reject mismatched authenticated metadata" }
                        val cryptoDir = File(activity.cacheDir, "kinetics-crypto-probe").apply { mkdirs() }
                        val encryptedFile = File(cryptoDir, "probe.kdat")
                        val plaintextFile = File(cryptoDir, "probe.txt")
                        try {
                            LocalCrypto.ensureChunkedFileHeader(encryptedFile)
                            LocalCrypto.appendEncryptedChunk(encryptedFile, plaintext, aad)
                            val hash = MessageDigest.getInstance("SHA-256").digest(plaintext)
                                .joinToString("") { "%02x".format(it) }
                            LocalCrypto.decryptChunkedFile(encryptedFile, plaintextFile, "runtime-probe", hash)
                            check(plaintextFile.readBytes().contentEquals(plaintext)) {
                                "Versioned encrypted-file roundtrip mismatch"
                            }
                        } finally {
                            encryptedFile.delete()
                            plaintextFile.delete()
                            cryptoDir.delete()
                        }
                        "C++ JNI: $cpp; Rust FFI: $rust; Keystore AES-GCM + versioned file roundtrip: passed"
                    }.getOrElse { "FAILED: ${it.message ?: it.javaClass.simpleName}" }
                    "Python probe:\n$python\nNative probe: $native"
                }
            }
        },
        onCancel = { job ->
            // Commit the terminal state first. ImportWorker finalization checks this same
            // state inside its database transaction, so a late worker cannot resurrect it.
            if (store.cancelActiveImport(job.id)) {
                WorkManager.getInstance(activity).cancelUniqueWork("import-" + job.id)
                notice = "Import cancelled. Any authenticated encrypted partial input is retained for resume."
            } else {
                notice = "This import is already complete or is no longer active; its state was not changed."
            }
            jobs = store.recentJobs()
        },
        onResume = { job ->
            val savedUri = store.inputUri(job.id)
            if (savedUri != null && store.queueImportForResume(job.id)) {
                val request = OneTimeWorkRequestBuilder<ImportWorker>()
                    .setInputData(workDataOf(ImportWorker.KEY_JOB_ID to job.id, ImportWorker.KEY_URI to savedUri))
                    .addTag("kinetics-import").build()
                WorkManager.getInstance(activity).enqueueUniqueWork(
                    "import-" + job.id, ExistingWorkPolicy.REPLACE, request)
                jobs = store.recentJobs()
            } else {
                notice = "This job is not in a resumable state."
            }
        },
        onDelete = { job -> deleteTarget = job },
        onExport = { job ->
            pendingExportJob = job.id
            exportPicker.launch(job.inputName.substringAfterLast('/').take(120).ifBlank { "kinetics-research-export.bin" })
        },
        onExportProvenance = { job ->
            pendingProvenanceExportJob = job.id
            provenanceExportPicker.launch("kinetics-provenance-${job.id}.json")
        },
        onAnalyzeImported = { job ->
            val request = OneTimeWorkRequestBuilder<ImportedFastaAnalysisWorker>()
                .setInputData(workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to job.id))
                .addTag("kinetics-analysis").build()
            WorkManager.getInstance(activity).enqueueUniqueWork(
                "analysis-${job.id}", ExistingWorkPolicy.KEEP, request,
            )
            notice = "Local FASTA QC queued for ${job.inputName}. The saved result will retain the imported SHA-256 provenance."
        },
        onExportAnalysis = { job ->
            pendingAnalysisExportJob = job.id
            analysisExportPicker.launch("kinetics-analysis-${job.id}.json")
        },
        onExportProvenanceSummary = { job ->
            pendingProvenanceSummaryJob = job.id
            provenanceSummaryPicker.launch("kinetics-provenance-${job.id}.txt")
        },
        onAnalyzeFastq = { job, offset ->
            val request = OneTimeWorkRequestBuilder<ImportedFastqAnalysisWorker>()
                .setInputData(workDataOf(
                    ImportedFastqAnalysisWorker.KEY_JOB_ID to job.id,
                    ImportedFastqAnalysisWorker.KEY_PHRED_OFFSET to offset,
                ))
                .addTag("kinetics-analysis").build()
            WorkManager.getInstance(activity).enqueueUniqueWork(
                "analysis-${job.id}", ExistingWorkPolicy.REPLACE, request,
            )
            notice = "Local FASTQ QC queued with explicit Phred+$offset encoding. The result will retain the imported SHA-256 provenance."
        },
        themeFamily = themeFamily,
        onThemeFamilyChange = { selected ->
            preferences.edit().putString("theme_family", selected).apply()
            themeFamily = selected
        },
        biometricEnabled = biometricEnabled,
        biometricAvailable = BiometricUnlock.canAuthenticate(activity),
        debugBuild = (activity.applicationInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0,
        onBiometricChange = { enabled ->
            if (!enabled || BiometricUnlock.canAuthenticate(activity)) {
                preferences.edit().putBoolean("biometric_unlock_enabled", enabled).apply()
                biometricEnabled = enabled
            } else {
                notice = "Biometric app unlock cannot be enabled: enroll a supported biometric or device credential first."
            }
        },
    )
        deleteTarget?.let { target ->
            AlertDialog(
                onDismissRequest = { deleteTarget = null },
                title = { Text("Delete local research data?") },
                text = {
                    Text(
                        "This removes the encrypted local input, any retained encrypted partial, " +
                            "and job/provenance metadata. It cannot delete copies you previously exported. " +
                            "Flash storage secure erasure is not guaranteed."
                    )
                },
                confirmButton = {
                    TextButton(onClick = {
                        deleteTarget = null
                        WorkManager.getInstance(activity).cancelUniqueWork("import-" + target.id)
                        WorkManager.getInstance(activity).cancelUniqueWork("analysis-" + target.id)
                        scope.launch {
                            val result = withContext(Dispatchers.IO) {
                                runCatching { store.deleteStoredJob(target.id) }
                            }
                            notice = result.fold(
                                { "Local research data deleted." },
                                { "Deletion failed: ${it.message ?: it.javaClass.simpleName}" },
                            )
                            jobs = store.recentJobs()
                        }
                    }) { Text("Delete") }
                },
                dismissButton = {
                    TextButton(onClick = { deleteTarget = null }) { Text("Keep data") }
                },
            )
        }
    }
