package org.assayflux.molecularis

import android.content.Context
import androidx.compose.foundation.Image
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Menu
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AccountCircle
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.WorkOutline
import androidx.compose.material.icons.filled.Fingerprint
import androidx.compose.runtime.*
import androidx.activity.compose.BackHandler
import androidx.compose.runtime.saveable.rememberSaveable
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import org.assayflux.designsystem.MolecularisTokens
import org.assayflux.designsystem.MolecularisTypography
import org.assayflux.designsystem.MolecularisScientificTextStyle
import org.assayflux.designsystem.MolecularisAppBar
import org.assayflux.designsystem.MolecularisField
import org.assayflux.designsystem.MolecularisListRow
import org.assayflux.designsystem.MolecularisComponentGallery
import org.json.JSONArray
import org.json.JSONObject

internal enum class MolecularisTab(val label: String) {
    Home("Home"), Work("Work"), Settings("Settings")
}

@Composable
private fun MolecularisTabIcon(tab: MolecularisTab) {
    val image = when (tab) {
        MolecularisTab.Home -> Icons.Outlined.Home
        MolecularisTab.Work -> Icons.Outlined.WorkOutline
        MolecularisTab.Settings -> Icons.Outlined.Settings
    }
    Icon(image, contentDescription = null)
}

@Composable
internal fun MolecularisAppShell(
    jobs: List<ResearchJob>, notice: String, runtimeReport: String?,
    onImport: () -> Unit, onRefresh: () -> Unit, onRunRuntime: () -> Unit,
    onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
    onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit,
    onAnalyzeImported: (ResearchJob) -> Unit, onExportAnalysis: (ResearchJob) -> Unit,
    onAnalyzeFastq: (ResearchJob, Int) -> Unit,
    themeFamily: String, onThemeFamilyChange: (String) -> Unit,
    biometricEnabled: Boolean, biometricAvailable: Boolean,
    onBiometricChange: (Boolean) -> Unit,
    debugBuild: Boolean,
) {
    var tab by rememberSaveable { mutableStateOf(MolecularisTab.Home) }
    var showSearch by rememberSaveable { mutableStateOf(false) }
    var searchQuery by rememberSaveable { mutableStateOf("") }
    var workSearchQuery by rememberSaveable { mutableStateOf("") }
    var showComponentGallery by rememberSaveable { mutableStateOf(false) }
    var showProfile by rememberSaveable { mutableStateOf(false) }
    var selectedServiceId by rememberSaveable { mutableStateOf<String?>(null) }
    val context = LocalContext.current
    val capabilities = remember(context) {
        runCatching {
            loadCapabilityCatalogue(context) + CapabilityEntry(
                id = "public.reference_databases",
                name = "Public reference databases",
                status = "implemented",
                implementation = "PublicDatabaseClient.kt",
                evidenceLevel = "none",
                domain = "Public reference databases",
            )
        }.getOrDefault(emptyList())
    }
    BackHandler(enabled = showSearch || showComponentGallery || showProfile || selectedServiceId != null) {
        when {
            showComponentGallery -> showComponentGallery = false
            showSearch -> showSearch = false
            showProfile -> showProfile = false
            else -> selectedServiceId = null
        }
    }
    val resolvedTheme = when (themeFamily) {
        "system" -> if (isSystemInDarkTheme()) "dark" else "light"
        else -> themeFamily
    }
    val palette = if (resolvedTheme == "dark") MolecularisTokens.MolecularisDarkClassic else MolecularisTokens.MolecularisLightClassic
    val decisionColors = if (resolvedTheme == "dark") MolecularisTokens.StatusDark else MolecularisTokens.StatusLight
    val scheme = if (resolvedTheme == "light") {
        lightColorScheme(
            primary = palette.primary, secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface, onSurface = palette.text,
            onBackground = palette.text, surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted, outline = palette.outline, error = decisionColors.error,
        )
    } else {
        darkColorScheme(
            primary = palette.primary, onPrimary = palette.background,
            secondary = palette.secondary, tertiary = palette.tertiary,
            background = palette.background, surface = palette.surface, onSurface = palette.text,
            onBackground = palette.text, surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted, outline = palette.outline, error = decisionColors.error,
        )
    }
    MaterialTheme(colorScheme = scheme, typography = MolecularisTypography) {
      BoxWithConstraints(Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing)) {
        val drawerState = rememberDrawerState(DrawerValue.Closed)
        val drawerScope = rememberCoroutineScope()
        ModalNavigationDrawer(
            drawerState = drawerState,
            gesturesEnabled = true,
            drawerContent = {
                ModalDrawerSheet(
                    modifier = Modifier.fillMaxHeight().widthIn(max = 340.dp),
                    drawerContainerColor = MaterialTheme.colorScheme.surface,
                ) {
                    Column(
                        Modifier.fillMaxWidth().height(160.dp).padding(horizontal = 24.dp, vertical = 20.dp),
                        verticalArrangement = Arrangement.Bottom,
                    ) {
                        Text("KINETICS", style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.SemiBold, letterSpacing = 1.4.sp)
                        Spacer(Modifier.height(6.dp))
                        Text("COMPUTATIONAL RESEARCH", style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                    }
                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    Spacer(Modifier.height(12.dp))
                    MolecularisTab.entries.forEach { item ->
                        NavigationDrawerItem(
                            selected = tab == item && selectedServiceId == null && !showProfile && !showSearch,
                            onClick = {
                                tab = item
                                selectedServiceId = null
                                showProfile = false
                                showSearch = false
                                drawerScope.launch { drawerState.close() }
                            },
                            icon = { MolecularisTabIcon(item) },
                            label = { Text(item.label) },
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp),
                        )
                    }
                    NavigationDrawerItem(
                        selected = showSearch,
                        onClick = {
                            showSearch = true
                            showProfile = false
                            selectedServiceId = null
                            drawerScope.launch { drawerState.close() }
                        },
                        icon = { Icon(Icons.Outlined.Search, contentDescription = null) },
                        label = { Text("Search") },
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp),
                    )
                    Spacer(Modifier.weight(1f))
                    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    Text("RESEARCH MODE", modifier = Modifier.padding(horizontal = 24.dp, vertical = 18.dp),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            },
        ) {
            Scaffold(
                containerColor = MaterialTheme.colorScheme.background,
                topBar = {
                    MolecularisAppBar(
                        title = when {
                            showSearch -> "Search"
                            showComponentGallery -> "Design system"
                            showProfile -> "Profile"
                            selectedServiceId != null -> capabilities.firstOrNull { it.id == selectedServiceId }?.name ?: "Service"
                            tab == MolecularisTab.Home -> ""
                            else -> "KINETICS"
                        },
                        subtitle = when {
                            showSearch -> "Jobs and registered capabilities"
                            showComponentGallery -> "Developer component preview"
                            showProfile -> "Local profile and device security"
                            selectedServiceId != null -> "Scientific service workspace"
                            tab == MolecularisTab.Home -> ""
                            else -> tab.label
                        },
                        navigation = {
                            if (showSearch || showComponentGallery || showProfile || selectedServiceId != null) {
                                IconButton(
                                    onClick = {
                                        when {
                                            showSearch -> showSearch = false
                                            showComponentGallery -> showComponentGallery = false
                                            showProfile -> showProfile = false
                                            else -> selectedServiceId = null
                                        }
                                    },
                                    modifier = Modifier.size(48.dp),
                                ) { Icon(Icons.Outlined.ArrowBack, contentDescription = "Back") }
                            } else {
                                IconButton(
                                    onClick = { drawerScope.launch { drawerState.open() } },
                                    modifier = Modifier.size(48.dp),
                                ) { Icon(Icons.Outlined.Menu, contentDescription = "Open navigation menu") }
                            }
                        },
                        actions = {
                            if (!showSearch && !showComponentGallery && !showProfile && selectedServiceId == null) {
                                ProfileAvatarButton(onClick = { showProfile = true })
                            }
                        },
                    )
                },
            ) { padding ->
                val contentModifier = Modifier.padding(padding)
                when {
                    showComponentGallery -> MolecularisComponentGallery()
                    showProfile -> ProfileScreen(biometricEnabled, biometricAvailable)
                    showSearch -> GlobalSearchScreen(
                        query = searchQuery,
                        onQueryChange = { searchQuery = it },
                        jobs = jobs,
                        onSelectJob = { result ->
                            workSearchQuery = result.title
                            showSearch = false
                            tab = MolecularisTab.Work
                        },
                        onSelectCapability = { result ->
                            val entry = capabilities.firstOrNull { it.id == result.id.removePrefix("capability:") }
                            selectedServiceId = entry?.id
                            showSearch = false
                        },
                        modifier = contentModifier,
                    )
                    selectedServiceId != null -> ServiceDetailScreen(
                        domain = capabilities.firstOrNull { it.id == selectedServiceId }?.domain ?: "Service",
                        capabilities = capabilities.filter { it.id == selectedServiceId },
                        onImport = onImport,
                        modifier = contentModifier,
                    )
                    else -> when (tab) {
                        MolecularisTab.Home -> HomeScreen(
                            jobs, notice, runtimeReport, resolvedTheme, onImport, onRunRuntime,
                            { tab = MolecularisTab.Work }, { selectedServiceId = it },
                            onCancel, onResume, onDelete, onExport, onExportProvenance,
                            onExportProvenanceSummary, onAnalyzeImported, onExportAnalysis,
                            onAnalyzeFastq, contentModifier,
                        )
                        MolecularisTab.Work -> WorkScreen(
                            jobs, workSearchQuery, onImport, onCancel, onResume, onDelete, onExport,
                            onExportProvenance, onExportProvenanceSummary, onAnalyzeImported,
                            onExportAnalysis, onAnalyzeFastq, contentModifier,
                        )
                        MolecularisTab.Settings -> SettingsScreen(
                            runtimeReport, onRunRuntime, onRefresh, themeFamily, onThemeFamilyChange,
                            biometricEnabled, biometricAvailable, onBiometricChange,
                            debugBuild, { showComponentGallery = true }, contentModifier,
                        )
                    }
                }
            }
      }
    }
  }
}

private fun loadLocalProfileBitmap(context: Context, uriText: String): android.graphics.Bitmap? {
    val uri = android.net.Uri.parse(uriText)
    val resolver = context.contentResolver
    val bounds = android.graphics.BitmapFactory.Options().apply { inJustDecodeBounds = true }
    resolver.openInputStream(uri)?.use { android.graphics.BitmapFactory.decodeStream(it, null, bounds) }
    if (bounds.outWidth <= 0 || bounds.outHeight <= 0) return null
    var sample = 1
    while (bounds.outWidth / sample > 512 || bounds.outHeight / sample > 512) sample *= 2
    val options = android.graphics.BitmapFactory.Options().apply {
        inSampleSize = sample
        inPreferredConfig = android.graphics.Bitmap.Config.RGB_565
    }
    return resolver.openInputStream(uri)?.use { android.graphics.BitmapFactory.decodeStream(it, null, options) }
}

@Composable
private fun ProfileAvatarButton(onClick: () -> Unit) {
    val context = LocalContext.current
    val uri = context.getSharedPreferences("molecularis_preferences", Context.MODE_PRIVATE)
        .getString("local_profile_avatar_uri", null)
    val bitmap by produceState<android.graphics.Bitmap?>(null, uri) {
        value = withContext(Dispatchers.IO) {
            uri?.let { raw ->
                runCatching {
                    loadLocalProfileBitmap(context, raw)
                }.getOrNull()
            }
        }
    }
    IconButton(onClick = onClick, modifier = Modifier.size(48.dp)) {
        if (bitmap != null) {
            Image(bitmap = bitmap!!.asImageBitmap(), contentDescription = "Open profile",
                modifier = Modifier.size(36.dp).clip(CircleShape))
        } else {
            Icon(Icons.Outlined.AccountCircle, contentDescription = "Open profile",
                modifier = Modifier.size(36.dp))
        }
    }
}

@Composable
private fun ProfileScreen(biometricEnabled: Boolean, biometricAvailable: Boolean) {
    val context = LocalContext.current
    val preferences = remember(context) {
        context.getSharedPreferences("molecularis_preferences", Context.MODE_PRIVATE)
    }
    var displayName by rememberSaveable {
        mutableStateOf(preferences.getString("local_profile_name", "Researcher") ?: "Researcher")
    }
    var avatarUri by rememberSaveable {
        mutableStateOf(preferences.getString("local_profile_avatar_uri", null))
    }
    val localWorkspaceId = remember {
        preferences.getString("local_workspace_id", null) ?: java.util.UUID.randomUUID().toString().also {
            preferences.edit().putString("local_workspace_id", it).apply()
        }
    }
    val avatarPicker = androidx.activity.compose.rememberLauncherForActivityResult(
        androidx.activity.result.contract.ActivityResultContracts.OpenDocument(),
    ) { uri ->
        if (uri != null) {
            runCatching {
                context.contentResolver.takePersistableUriPermission(
                    uri, android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION,
                )
            }
            avatarUri = uri.toString()
            preferences.edit().putString("local_profile_avatar_uri", avatarUri).apply()
        }
    }
    val avatarBitmap by produceState<android.graphics.Bitmap?>(null, avatarUri) {
        value = withContext(Dispatchers.IO) {
            avatarUri?.let { raw ->
                runCatching {
                    loadLocalProfileBitmap(context, raw)
                }.getOrNull()
            }
        }
    }
    Frame("ACCOUNT", "Local profile", "This profile belongs to this app installation; it is not a remote account.", Modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                Column(Modifier.fillMaxWidth().padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp),
                    horizontalAlignment = Alignment.CenterHorizontally) {
                    if (avatarBitmap != null) {
                        Image(
                            bitmap = avatarBitmap!!.asImageBitmap(),
                            contentDescription = "Selected local profile image",
                            modifier = Modifier.size(88.dp).clip(CircleShape),
                        )
                    } else {
                        Icon(Icons.Outlined.AccountCircle, contentDescription = "Default profile image",
                            modifier = Modifier.size(88.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    OutlinedButton(onClick = { avatarPicker.launch(arrayOf("image/*")) }) {
                        Text(if (avatarUri == null) "Choose profile image" else "Change profile image")
                    }
                    OutlinedTextField(
                        value = displayName,
                        onValueChange = { displayName = it.take(60) },
                        modifier = Modifier.fillMaxWidth(),
                        label = { Text("Display name") },
                        singleLine = true,
                    )
                    Button(
                        onClick = { preferences.edit().putString("local_profile_name", displayName.trim().ifBlank { "Researcher" }).apply() },
                        modifier = Modifier.fillMaxWidth(),
                    ) { Text("Save local profile") }
                    Text("Device-local workspace ID", style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(localWorkspaceId, style = MaterialTheme.typography.bodySmall)
                    Text("This identifier is generated on this device. It is not a user/account ID and is not synced.",
                        style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            SettingGroup("DEVICE SECURITY", "The existing biometric option is a local app lock, not account authentication.") {
                Text(
                    when {
                        biometricEnabled && biometricAvailable -> "Biometric/device credential unlock is enabled on this device."
                        biometricAvailable -> "Biometric/device credential unlock is available but not enabled."
                        else -> "No supported biometric/device credential is currently enrolled."
                    },
                    style = MaterialTheme.typography.bodySmall,
                )
                Text("Manage the local app lock in Settings.", style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            SettingGroup("ONLINE ACCOUNT", "Remote sign-in, password reset, account recovery and cloud sign-out are unavailable because no identity backend is configured.") {
                Text("No remote account credentials are stored by Molecularis. Do not enter institutional or patient-system passwords here.",
                    style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun ServiceDetailScreen(
    domain: String,
    capabilities: List<CapabilityEntry>,
    onImport: () -> Unit,
    modifier: Modifier,
) {
    var publicStructureRecord by remember { mutableStateOf<PublicScientificRecord?>(null) }
    val capability = capabilities.firstOrNull()
    val androidWorkflowAvailable = capability?.id in setOf(
        "public.reference_databases",
        "sequence.fasta",
        "sequence.fastq",
        "sequence.genetic_code_candidate_inference",
        "protein.descriptors",
        "molecular.primer_screen",
        "molecular.crispr_pam",
        "genome.orf_candidate_scan",
        "kinetics.michaelis_menten",
        "phylo.newick",
        "sequence.global_alignment",
        "genome.contig_assembly_qc",
        "structure.sasa",
        "structure.interaction_candidates",
        "microbiome.diversity",
        "omics.logistic_growth",
        "sequence.explicit_genetic_code_translation",
        "kinetics.inhibition_rate",
        "phylo.upgma",
        "omics.normalisation",
        "omics.cross_correlation",
        "phylo.jukes_cantor_nj",
        "genome.gff3_annotation_import",
        "genome.gff3_transcript_cds_reconstruction",
        "protein.fixed_width_motif_scan",
        "protein.hmmscan_domain_evidence",
        "protein.hmmscan_domtblout_evidence",
        "protein.hmmer_domain_candidate_ranking",
        "genome.prokaryotic_orf_candidate_scan",
        "kinetics.bootstrap_intervals",
        "protein.design_brief_validation",
        "structure.geometry_screen_metrics",
        "structure.prediction_envelope_validation",
        "structure.experimental_ca_comparison",
        "phylo.nj_site_bootstrap",
        "structure.exact_sequence_mapping",
        "structure.chain_interface_contacts",
        "structure.alignment_coordinate_mapping",
        "structure.variant_coordinate_mapping",
        "sequence.exact_reference_search",
        "sequence.local_alignment_reference_search",
        "sequence.local_fasta_exact_search",
        "sequence.local_fasta_alignment_search",
        "genes.ncbi_catalogue",
        "genes.catalogue_coverage_report",
        "phylo.newick_export",
        "structure.pdb_geometry",
        "structure.ligand_site_candidates",
        "structure.apo_pocket_candidates",
        "chemistry.sdf_graph",
        "genomics.sam_vcf",
        "sequence.local_reference_pack_loader",
        "sequence.local_blastp",
        "sequence.local_hmmpress",
        "sequence.local_hmmscan",
        "variant.reference_checked_normalization",
        "genomics.variant_normalization",
        "omics.nb2_glm",
        "genomics.bam_core",
        "pgx.star_allele_definitions",
        "chemistry.rdkit_adapter",
        "genomics.htslib_bam_cram",
        "pgx.pharmvar_tsv",
        "structure.viewer_payload",
        "structure.session_export",
        "structure.pinned_local_prediction_process",
        "genome.augustus_local_gene_candidates",
        "genome.prodigal_local_gene_candidates",
        "genome.pinned_local_gff3_annotator",
        "structure.local_prediction_engine_adapter"
    )
    Frame("SCIENTIFIC SERVICE", capability?.name ?: domain, "Service ID: ${capability?.id ?: "not registered"} · $domain", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item {
                OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                    Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                        Text(if (capability?.status == "implemented") "ENGINE SOURCE REGISTERED" else "ENGINE SOURCE NOT IMPLEMENTED",
                            style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                        Text(if (androidWorkflowAvailable) "Android workflow: available" else "Android workflow: not connected",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Text("Source: ${capability?.implementation ?: "not available"}", style = MaterialTheme.typography.bodySmall)
                        Text("A registered Python engine is not automatically runnable in this Android app. No scientific validation is implied.",
                            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
            if (capability?.id == "public.reference_databases" || capability?.id == "genes.ncbi_catalogue") {
                item { PublicDatabaseCard(onStructureFetched = { publicStructureRecord = it }) }
                item { StructureViewerPreview(publicRecord = publicStructureRecord) }
            }
            if (capability?.id == "sequence.fasta") item { FastaQcCard() }
            if (capability?.id == "sequence.fastq") item { FastqQcCard() }
            if (capability?.id == "sequence.genetic_code_candidate_inference") item { GeneticCodeInferenceCard() }
            if (capability?.id == "protein.descriptors") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "protein.descriptors",
                    title = "Protein sequence descriptors",
                    description = "Calculate composition, estimated molecular mass, mean hydropathy and theoretical pI for an unmodified linear peptide.",
                    sample = "MKWVTFISLLFLFSSAYS",
                    actionLabel = "Analyse protein",
                ) }
            }
            if (capability?.id == "molecular.primer_screen") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "molecular.primer_screen",
                    title = "Primer property screen",
                    description = "Bounded Wallace-rule GC/Tm screening for one unambiguous 15–40 nt primer. Not an oligo design or wet-lab validation tool.",
                    sample = "ATGCGTACGTAGCTAGCT",
                    actionLabel = "Screen primer",
                ) }
            }
            if (capability?.id == "genome.orf_candidate_scan") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "genome.orf_candidate_scan",
                    title = "Six-frame ORF candidate scan",
                    description = "Enumerate complete start-to-stop ORFs on both strands using explicit NCBI table 11 and a bounded mobile workload. Not gene annotation.",
                    sample = "ATG" + "GCT".repeat(29) + "TAA",
                    actionLabel = "Scan ORFs",
                ) }
            }
            if (capability?.id == "kinetics.michaelis_menten") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "kinetics.michaelis_menten",
                    title = "Michaelis–Menten rate calculator",
                    description = "Calculate v = Vmax·[S]/(Km+[S]). Enter three comma-separated non-negative values: substrate concentration, Vmax and Km.",
                    sample = "10,100,5",
                    actionLabel = "Calculate rate",
                ) }
            }
            if (capability?.id in setOf("phylo.newick", "phylo.newick_export")) {
                item { BasicResearchCapabilityCard(
                    capabilityId = "phylo.newick",
                    title = "Newick tree parser",
                    description = "Parse a Newick tree and return leaf labels and a normalized serialization. This does not infer a phylogeny from sequence data.",
                    sample = "((A:0.1,B:0.2):0.3,C:0.4);",
                    actionLabel = "Parse tree",
                ) }
            }
            if (capability?.id == "molecular.crispr_pam") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "molecular.crispr_pam",
                    title = "SpCas9 NGG PAM scan",
                    description = "Locate NGG PAM triplets on both strands and report 0-based half-open coordinates. No guide efficacy or editing outcome is predicted.",
                    sample = "AACCGGTTACGGTAGGCTAACCGG",
                    actionLabel = "Scan PAM sites",
                ) }
            }
            if (capability?.id == "sequence.global_alignment") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "sequence.global_alignment",
                    title = "Global pairwise alignment",
                    description = "Needleman–Wunsch alignment. Enter two sequences on separate lines; work is limited to 250,000 dynamic-programming cells.",
                    sample = "ACGTACGT\nACGTCGTT",
                    actionLabel = "Align sequences",
                ) }
            }
            if (capability?.id == "genome.contig_assembly_qc") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "genome.contig_assembly_qc",
                    title = "Contig assembly QC",
                    description = "Summarize FASTA contigs, N50/L50, GC and ambiguity burden. Input is capped at 1 MB and 10,000 records.",
                    sample = ">contig_1\nACGTACGTACGT\n>contig_2\nGGGGCCCC",
                    actionLabel = "Analyse assembly",
                ) }
            }
            if (capability?.id == "structure.sasa") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.sasa",
                    title = "Structure solvent-accessible surface area",
                    description = "Approximate Shrake–Rupley SASA from PDB ATOM records. Requires 1–2,000 supported atoms; geometry only.",
                    sample = "",
                    actionLabel = "Calculate SASA",
                ) }
            }
            if (capability?.id == "structure.interaction_candidates") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.interaction_candidates",
                    title = "Structure interaction candidates",
                    description = "Distance-only candidate screening for hydrogen bonds, salt bridges and disulfides. Not an energetic or binding-affinity calculation.",
                    sample = "",
                    actionLabel = "Screen interactions",
                ) }
            }
            if (capability?.id == "microbiome.diversity") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "microbiome.diversity",
                    title = "Microbiome diversity",
                    description = "Calculate Shannon and Gini–Simpson diversity from comma-separated non-negative abundance counts.",
                    sample = "12,8,5,3,2",
                    actionLabel = "Calculate diversity",
                ) }
            }
            if (capability?.id == "omics.logistic_growth") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "omics.logistic_growth",
                    title = "Logistic growth model",
                    description = "Enter JSON with timepoints, carrying_capacity, growth_rate and initial. Returns deterministic model predictions.",
                    sample = "{\"timepoints\":[0,1,2,3,4],\"carrying_capacity\":100,\"growth_rate\":0.5,\"initial\":5}",
                    actionLabel = "Run growth model",
                ) }
            }
            if (capability?.id == "sequence.explicit_genetic_code_translation") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "sequence.explicit_genetic_code_translation",
                    title = "Explicit genetic-code translation",
                    description = "Translate one coding sequence using a caller-selected NCBI table and reading frame. Input JSON: sequence, table_id, frame, cds.",
                    sample = "{\"sequence\":\"ATGGCTTAA\",\"table_id\":1,\"frame\":0,\"cds\":true}",
                    actionLabel = "Translate sequence",
                ) }
            }
            if (capability?.id == "kinetics.inhibition_rate") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "kinetics.inhibition_rate",
                    title = "Enzyme inhibition rate",
                    description = "Calculate competitive, uncompetitive, noncompetitive or mixed inhibition rate. Supply substrate, inhibitor, Vmax, Km, Ki and mode as JSON.",
                    sample = "{\"substrate\":10,\"inhibitor\":2,\"vmax\":100,\"km\":5,\"ki\":1,\"mode\":\"competitive\"}",
                    actionLabel = "Calculate inhibition rate",
                ) }
            }
            if (capability?.id == "phylo.upgma") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "phylo.upgma",
                    title = "UPGMA tree construction",
                    description = "Build a rooted UPGMA tree from a finite symmetric distance matrix and unique labels. Supply distance_matrix and labels as JSON.",
                    sample = "{\"labels\":[\"A\",\"B\",\"C\"],\"distance_matrix\":[[0,2,4],[2,0,4],[4,4,0]]}",
                    actionLabel = "Build UPGMA tree",
                ) }
            }
            if (capability?.id == "omics.normalisation") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "omics.normalisation",
                    title = "Omics count normalisation",
                    description = "Apply counts-per-million or centred log-ratio transformation to a rectangular feature-by-sample matrix. Input JSON includes method and matrix.",
                    sample = "{\"method\":\"cpm\",\"matrix\":[[10,20],[30,40]]}",
                    actionLabel = "Normalise matrix",
                ) }
            }
            if (capability?.id == "omics.cross_correlation") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "omics.cross_correlation",
                    title = "Cross-omics correlation",
                    description = "Calculate pairwise Pearson correlations between two feature-by-sample matrices with matching sample order. Input JSON includes first and second matrices.",
                    sample = "{\"first\":[[1,2,3],[3,2,1]],\"second\":[[2,4,6]]}",
                    actionLabel = "Correlate features",
                ) }
            }
            if (capability?.id == "phylo.jukes_cantor_nj") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "phylo.jukes_cantor_nj",
                    title = "Jukes–Cantor neighbour joining",
                    description = "Infer a neighbour-joining tree from caller-supplied aligned DNA sequences using pairwise-deletion Jukes–Cantor distances. Input JSON includes named sequences.",
                    sample = "{\"sequences\":{\"A\":\"ACGTACGTACGTACGTACGT\",\"B\":\"ACGTACGTACGTACGTACGA\",\"C\":\"ACGTACGTACGTACGTACGG\"}}",
                    actionLabel = "Build NJ tree",
                ) }
            }
            if (capability?.id == "genome.gff3_annotation_import") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "genome.gff3_annotation_import",
                    title = "GFF3 annotation validation",
                    description = "Validate GFF3 version, feature coordinates, IDs and Parent relationships. No gene function is inferred.",
                    sample = "##gff-version 3\nchr1\tMolecularis\tgene\t1\t100\t.\t+\t.\tID=gene1",
                    actionLabel = "Validate annotation",
                ) }
            }
            if (capability?.id == "genome.gff3_transcript_cds_reconstruction") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "genome.gff3_transcript_cds_reconstruction",
                    title = "GFF3 transcript CDS reconstruction",
                    description = "Reconstruct spliced CDS from validated GFF3 and supplied contigs. Input JSON contains gff3, contigs and optional table_id.",
                    sample = "{\"gff3\":\"##gff-version 3\\nchr1\\tMolecularis\\tgene\\t1\\t9\\t.\\t+\\t.\\tID=g1\\nchr1\\tMolecularis\\tmRNA\\t1\\t9\\t.\\t+\\t.\\tID=t1;Parent=g1\\nchr1\\tMolecularis\\tCDS\\t1\\t9\\t.\\t+\\t0\\tID=c1;Parent=t1\",\"contigs\":{\"chr1\":\"ATGGCTTAA\"},\"table_id\":11}",
                    actionLabel = "Reconstruct CDS",
                ) }
            }
            if (capability?.id == "genes.catalogue_coverage_report") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "genes.catalogue_coverage_report",
                    title = "Gene catalogue snapshot report",
                    description = "Summarize a bounded, source-release-pinned NCBI gene_info TSV snapshot. Reports composition and missing annotations only; it does not claim genome-wide completeness.",
                    sample = "{\"source_release\":\"NCBI Gene 2025-01\",\"gene_info_tsv\":\"9606\\t1\\tA1BG\\t-\\tA1B\\t-\\t19\\t19q13.43\\talpha-1-B glycoprotein\\tprotein-coding\\tA1BG\\talpha-1-B glycoprotein\\tApproved\\t-\\t20250101\\tgene\"}",
                    actionLabel = "Summarize gene snapshot",
                ) }
            }
            if (capability?.id in setOf(
                "sequence.local_reference_pack_loader",
                "sequence.local_blastp",
                "sequence.local_hmmpress",
                "sequence.local_hmmscan",
                "variant.reference_checked_normalization",
                "genes.ncbi_catalogue",
                "genomics.variant_normalization",
                "omics.nb2_glm",
                "genomics.bam_core",
                "pgx.star_allele_definitions",
                "chemistry.rdkit_adapter",
                "genomics.htslib_bam_cram",
                "pgx.pharmvar_tsv",
                "structure.viewer_payload",
                "structure.session_export",
                "structure.pinned_local_prediction_process",
                "genome.augustus_local_gene_candidates",
                "genome.prodigal_local_gene_candidates",
                "genome.pinned_local_gff3_annotator",
                "structure.local_prediction_engine_adapter"
            )) {
                item { BasicResearchCapabilityCard(
                    capabilityId = capability.id ?: "",
                    title = capability.name ?: "Advanced local workflow",
                    description = "Advanced local workflow. Supply JSON input following the workflow schema in docs/track-u/android-capability-integration-matrix.md. Optional engine binaries/libraries must be installed and hash-pinned locally; unavailable dependencies are reported rather than simulated.",
                    sample = when (capability.id) {
                        "sequence.local_reference_pack_loader" -> "{\"fasta\":\">ref1\\nACGT\",\"manifest\":{\"schema_version\":1,\"name\":\"Example DNA pack\",\"version\":\"1\",\"license\":\"CC0-1.0\",\"source\":\"https://example.org/reference.fasta\",\"sequence_type\":\"DNA\",\"format\":\"fasta\",\"content_sha256\":\"17e6a3a608308379a5f171b594fefb7a4733ad12ead687cc668cdc48bb8be4e8\"},\"query\":\"ACGT\"}",
                        "sequence.local_blastp" -> "{\"query_fasta\":\">query\\nMKWVTFISLL\",\"executable_path\":\"/app-private/bin/blastp\",\"executable_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"database_prefix\":\"/app-private/db/protein\",\"database_file_sha256\":{},\"database_id\":\"local-pack\",\"database_version\":\"1\",\"database_license\":\"CC0-1.0\",\"database_source\":\"https://example.org/db\"}",
                        "sequence.local_hmmpress" -> "{\"executable_path\":\"/app-private/bin/hmmpress\",\"executable_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"profile_path\":\"/app-private/profiles/example.hmm\",\"source_hmm_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"profile_name\":\"Example\",\"profile_version\":\"1\",\"profile_license\":\"CC0-1.0\",\"profile_source\":\"https://example.org/profile\"}",
                        "sequence.local_hmmscan" -> "{\"sequences_fasta\":\">query\\nMKWVTFISLL\",\"executable_path\":\"/app-private/bin/hmmscan\",\"executable_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"profile_path\":\"/app-private/profiles/example.hmm\",\"profile_pack\":{\"name\":\"Example\",\"version\":\"1\",\"license\":\"CC0-1.0\",\"source\":\"https://example.org/profile\",\"content_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\"}}",
                        "variant.reference_checked_normalization" -> "{\"reference\":{\"assembly\":\"GRCh-test\",\"accession\":\"NC_TEST.1\",\"release\":\"test\",\"contig\":\"chrT\",\"sequence\":\"ACGTACGT\",\"retrieved_at\":\"2026-11-18T00:00:00Z\"},\"chrom\":\"chrT\",\"position\":2,\"ref\":\"C\",\"alt\":\"T\"}",
                        "genes.ncbi_catalogue" -> "{\"source_release\":\"NCBI Gene example release\",\"gene_info_tsv\":\"9606\\t1\\tA1BG\\t-\\tA1B\\t-\\t19\\t19q13.43\\talpha-1-B glycoprotein\\tprotein-coding\\tA1BG\\talpha-1-B glycoprotein\\tApproved\\t-\\t20250101\\tgene\"}",
                        "genomics.variant_normalization" -> "{\"chrom\":\"chrT\",\"position\":2,\"ref\":\"C\",\"alt\":\"T\",\"reference_sequence\":\"ACGTACGT\"}",
                        "omics.nb2_glm" -> "{\"counts\":[[10,12,20,22],[30,28,31,29]],\"condition\":[0,0,1,1],\"feature_ids\":[\"geneA\",\"geneB\"]}",
                        "genomics.bam_core" -> "{\"bam_base64\":\"\"}",
                        "pgx.star_allele_definitions" -> "{\"definitions_json\":\"{\\\"schema_version\\\":1,\\\"source\\\":{\\\"name\\\":\\\"Synthetic\\\",\\\"release\\\":\\\"1\\\",\\\"url\\\":\\\"https://example.org\\\",\\\"license\\\":\\\"CC0-1.0\\\",\\\"sha256\\\":\\\"0000000000000000000000000000000000000000000000000000000000000000\\\"},\\\"genome_build\\\":\\\"GRCh-test\\\",\\\"definitions\\\":[{\\\"gene\\\":\\\"GENE\\\",\\\"star_allele\\\":\\\"*1\\\",\\\"id\\\":\\\"synthetic-1\\\",\\\"required_variants\\\":[],\\\"excluded_variants\\\":[]}]}\",\"source_release\":\"1\",\"gene_symbol\":\"GENE\",\"genome_build\":\"GRCh-test\",\"observed_variants\":[],\"phase_confirmed\":false,\"call_complete\":false}",
                        "chemistry.rdkit_adapter" -> "{\"smiles\":\"CCO\"}",
                        "genomics.htslib_bam_cram" -> "{\"path\":\"/app-private/data/sample.bam\"}",
                        "pgx.pharmvar_tsv" -> "{\"tsv\":\"Haplotype Identifier\\tGene Symbol\\tdbSNP rsID\\tReference Sequence\\tVariant Start\\tVariant Stop\\tReference Allele\\tVariant Allele\\tVariant Type\\n*1\\tSYN1\\t.\\tNG_SYNTHETIC.1\\t0\\t0\\tREFERENCE\\t.\\treference\\n*2\\tSYN1\\trsSynthetic1\\tNG_SYNTHETIC.1\\t2\\t2\\tA\\tG\\tsnv\\n\",\"source_release\":\"fixture-1\",\"expected_release\":\"fixture-1\",\"source_url\":\"https://example.org/pharmvar.tsv\",\"source_sha256\":\"915e56904e25ea33e3d992920ee17b18eb3f5e7ae03d6048558efcfedc5d4a74\",\"license_id\":\"CC0 synthetic test only\",\"gene_symbol\":\"SYN1\",\"reference_accession\":\"NG_SYNTHETIC.1\",\"observed_variants\":[],\"phase_confirmed\":false,\"call_complete\":false}",
                        "structure.viewer_payload" -> "{\"source_format\":\"pdb\",\"atoms\":[{\"serial\":1,\"name\":\"CA\",\"residue\":\"GLY\",\"chain\":\"A\",\"residue_number\":1,\"x\":0.0,\"y\":0.0,\"z\":0.0,\"element\":\"C\"}]}",
                        "structure.session_export" -> "{\"source_base64\":\"\",\"parser_version\":\"1\",\"payload\":{\"schema\":\"kinetics.structure-view.v1\",\"source_format\":\"pdb\",\"coordinate_unit\":\"angstrom\",\"atom_count\":1,\"atoms\":[{\"serial\":1,\"name\":\"CA\",\"residue\":\"GLY\",\"chain\":\"A\",\"residue_number\":1,\"element\":\"C\",\"xyz\":[0.0,0.0,0.0]}],\"limitations\":[\"Coordinates only\"]}}",
                        "structure.pinned_local_prediction_process", "structure.local_prediction_engine_adapter" -> "{\"sequence\":\"MKWVTFISLL\",\"executable_path\":\"/app-private/bin/predictor\",\"executable_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"weights_path\":\"/app-private/models/weights.bin\",\"weights_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"model_name\":\"Example\",\"model_version\":\"1\",\"model_license\":\"CC0-1.0\",\"engine_id\":\"local-example\",\"software_version\":\"1\",\"node_id\":\"device-local\",\"run_id\":\"sample\"}",
                        "genome.augustus_local_gene_candidates" -> "{\"fasta\":\">contig1\\nATGAAATAA\",\"executable_path\":\"/app-private/bin/augustus\",\"executable_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"config_path\":\"/app-private/augustus/config\",\"species\":\"human\",\"species_model_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"tool_version\":\"3.5\"}",
                        "genome.prodigal_local_gene_candidates" -> "{\"fasta\":\">contig1\\nATGAAATAA\",\"executable_path\":\"/app-private/bin/prodigal\",\"executable_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"tool_version\":\"2.6.3\",\"translation_table\":11,\"mode\":\"single\"}",
                        "genome.pinned_local_gff3_annotator" -> "{\"fasta\":\">contig1\\nATGAAATAA\",\"executable_path\":\"/app-private/bin/annotator\",\"executable_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"annotator_id\":\"local-annotator\",\"annotator_version\":\"1\",\"mode\":\"prokaryotic\",\"translation_table\":11}",
                        else -> "{}"
                    },
                    actionLabel = "Run local workflow",
                ) }
            }
            if (capability?.id == "protein.fixed_width_motif_scan") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "protein.fixed_width_motif_scan",
                    title = "Protein motif-pack scan",
                    description = "Scan a protein against a caller-supplied hash-pinned motif pack. Input JSON includes query, motifs and source/license metadata; no external pack is downloaded.",
                    sample = "{\"query\":\"ACDGACDG\",\"motifs\":[{\"id\":\"example\",\"pattern\":\"A..G\"}],\"name\":\"Example pack\",\"version\":\"1\",\"license\":\"CC0-1.0\",\"source\":\"https://example.org/motif-pack\"}",
                    actionLabel = "Scan motifs",
                ) }
            }
            if (capability?.id in setOf("protein.hmmscan_domain_evidence", "protein.hmmscan_domtblout_evidence")) {
                item { BasicResearchCapabilityCard(
                    capabilityId = capability.id ?: "protein.hmmscan_domtblout_evidence",
                    title = "HMMER domain evidence parser",
                    description = "Parse caller-supplied hmmscan domtblout with profile-pack name, version, licence, source and SHA-256 metadata. This does not run HMMER or verify the profile file itself.",
                    sample = "{\"domtblout\":\"\",\"hmmer_version\":\"3.4\",\"profile_pack\":{\"name\":\"Example profiles\",\"version\":\"1\",\"license\":\"CC0-1.0\",\"source\":\"https://example.org/profiles\",\"content_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\"}}",
                    actionLabel = "Parse domain evidence",
                ) }
            }
            if (capability?.id == "protein.hmmer_domain_candidate_ranking") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "protein.hmmer_domain_candidate_ranking",
                    title = "HMMER candidate ranking",
                    description = "Rank parsed profile-domain candidates using explicit caller-selected E-value, coverage and accuracy thresholds. Does not infer protein function or run HMMER.",
                    sample = "{\"evidence\":{\"schema\":\"kinetics.hmmscan-domain-evidence.v1\",\"hits\":[]},\"max_independent_evalue\":0.00001,\"min_profile_coverage\":0.5,\"min_query_coverage\":0.5,\"min_accuracy\":0.5}",
                    actionLabel = "Rank candidates",
                ) }
            }
            if (capability?.id == "genome.prokaryotic_orf_candidate_scan") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "genome.prokaryotic_orf_candidate_scan",
                    title = "Multi-contig prokaryotic ORF scan",
                    description = "Scan FASTA contigs for complete ORF candidates using explicit NCBI table 11 and a genome-wide work budget. Not gene annotation.",
                    sample = ">contig_1\nATG" + "GCT".repeat(29) + "TAA",
                    actionLabel = "Scan contigs",
                ) }
            }
            if (capability?.id == "kinetics.bootstrap_intervals") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "kinetics.bootstrap_intervals",
                    title = "Michaelis–Menten bootstrap intervals",
                    description = "Estimate exploratory paired-bootstrap percentile intervals for Vmax and Km. Input JSON includes substrate and rate arrays; 100 replicates minimum.",
                    sample = "{\"substrates\":[1,2,4,8,16],\"rates\":[16.7,28.6,44.4,61.5,76.2],\"replicates\":100,\"seed\":7}",
                    actionLabel = "Estimate intervals",
                ) }
            }
            if (capability?.id == "protein.design_brief_validation") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "protein.design_brief_validation",
                    title = "Protein design brief validation",
                    description = "Validate a human-reviewed research brief and enforce a generation block until model, data and safety gates are approved. Does not generate sequences.",
                    sample = "{\"schema\":\"kinetics.protein-design-brief.v1\",\"objective\":\"stability\",\"target_description\":\"Research construct\",\"length_min\":50,\"length_max\":200,\"fold_constraints\":[],\"expression_host\":\"unspecified\",\"localization\":\"unspecified\",\"disallowed_motifs\":[],\"safety_exclusions\":[\"No toxin or pathogen enhancement\"],\"human_review_required\":true}",
                    actionLabel = "Validate research brief",
                ) }
            }
            if (capability?.id in setOf("structure.geometry_screen_metrics", "structure.pdb_geometry")) {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.geometry_screen_metrics",
                    title = "Structure geometry screen",
                    description = "Summarize PDB atom/residue counts and bounded steric-overlap candidates. Geometry QC only; not a structure-quality certification.",
                    sample = "ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\nTER\nEND\n",
                    actionLabel = "Screen geometry",
                ) }
            }
            if (capability?.id == "phylo.nj_site_bootstrap") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "phylo.nj_site_bootstrap",
                    title = "Neighbour-joining site bootstrap",
                    description = "Estimate exploratory split support by resampling aligned nucleotide sites. Input JSON includes 4–10 aligned sequences and seed.",
                    sample = "{\"sequences\":{\"A\":\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\",\"B\":\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC\",\"C\":\"CCCCCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAAAAA\",\"D\":\"CCCCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAAAAAC\"},\"replicates\":100,\"seed\":7}",
                    actionLabel = "Bootstrap tree",
                ) }
            }
            if (capability?.id == "structure.prediction_envelope_validation") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.prediction_envelope_validation",
                    title = "Prediction provenance validator",
                    description = "Validate the structure-prediction envelope, input sequence hash, model/node provenance, viewer payload and confidence fields. This validates structure only; it does not run a prediction model or certify accuracy.",
                    sample = "{\"sequence\":\"G\",\"envelope\":{\"schema\":\"kinetics.structure-prediction.v1\",\"input_sequence_sha256\":\"333e0a1e27815d0ceee55c473fe3dc93d56c63e3bee2b3b4aee8eed6d70191a3\",\"sequence_length\":1,\"model\":{\"name\":\"Example model\",\"version\":\"1\",\"weights_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"license\":\"CC0-1.0\"},\"node\":{\"node_id\":\"local-example\",\"software_version\":\"1\",\"run_id\":\"sample\"},\"created_at\":\"2026-11-18T06:00:00Z\",\"predicted_structure\":{\"schema\":\"kinetics.structure-view.v1\",\"source_format\":\"pdb\",\"coordinate_unit\":\"angstrom\",\"atom_count\":1,\"atoms\":[{\"serial\":1,\"name\":\"CA\",\"residue\":\"GLY\",\"chain\":\"A\",\"residue_number\":1,\"element\":\"C\",\"xyz\":[0.0,0.0,0.0]}],\"limitations\":[\"Coordinates only\"]},\"confidence\":{\"plddt_per_residue\":[75.0],\"mean_plddt\":75.0,\"pae_mean_angstrom\":null,\"pae_max_angstrom\":null},\"limitations\":[\"Unverified example envelope\"]}}",
                    actionLabel = "Validate prediction record",
                ) }
            }
            if (capability?.id == "structure.experimental_ca_comparison") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.experimental_ca_comparison",
                    title = "Experimental CA comparison",
                    description = "Compare caller-supplied predicted and experimental PDB coordinates using exact chain/residue correspondence and superposed CA RMSD. No alignment or biological validation is inferred.",
                    sample = "{\"predicted_pdb\":\"ATOM      1  CA  ALA A   1      12.000  13.800   9.500  1.00 20.00           C\\nATOM      2  CA  GLY A   2      13.000  13.800   9.500  1.00 20.00           C\\nATOM      3  CA  SER A   3      12.000  14.800   9.500  1.00 20.00           C\\nTER\\nEND\\n\",\"experimental_pdb\":\"ATOM      1  CA  ALA A   1      12.000  13.800   9.500  1.00 20.00           C\\nATOM      2  CA  GLY A   2      13.000  13.800   9.500  1.00 20.00           C\\nATOM      3  CA  SER A   3      12.000  14.800   9.500  1.00 20.00           C\\nTER\\nEND\\n\"}",
                    actionLabel = "Compare structures",
                ) }
            }
            if (capability?.id == "structure.exact_sequence_mapping") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.exact_sequence_mapping",
                    title = "Exact sequence-to-structure mapping",
                    description = "Map a canonical protein sequence to a uniquely matching PDB chain. Input JSON includes sequence, chain_id and pdb.",
                    sample = "{\"sequence\":\"G\",\"chain_id\":\"A\",\"pdb\":\"ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\\nTER\\nEND\\n\"}",
                    actionLabel = "Map chain",
                ) }
            }
            if (capability?.id == "structure.chain_interface_contacts") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.chain_interface_contacts",
                    title = "Chain interface contacts",
                    description = "Count inter-chain heavy-atom contacts and minimum residue-pair distances from PDB. Geometric contact evidence only.",
                    sample = "{\"chain_a\":\"A\",\"chain_b\":\"B\",\"pdb\":\"ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\\nATOM      2  CA  GLY B   1      16.000  13.800   9.500  1.00 20.00           C\\nTER\\nEND\\n\"}",
                    actionLabel = "Count contacts",
                ) }
            }
            if (capability?.id == "structure.alignment_coordinate_mapping") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.alignment_coordinate_mapping",
                    title = "Alignment-based coordinate mapping",
                    description = "Map exact residue correspondences between a query protein and a PDB chain using bounded alignment. Ambiguous mappings abstain.",
                    sample = "{\"sequence\":\"G\",\"chain_id\":\"A\",\"pdb\":\"ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\\nTER\\nEND\\n\"}",
                    actionLabel = "Map by alignment",
                ) }
            }
            if (capability?.id == "structure.variant_coordinate_mapping") {
                item { BasicResearchCapabilityCard(
                    capabilityId = "structure.variant_coordinate_mapping",
                    title = "Variant-to-structure coordinate mapping",
                    description = "Map a caller-specified amino-acid substitution to a uniquely matched PDB chain. Coordinate mapping only; no effect prediction.",
                    sample = "{\"sequence\":\"G\",\"chain_id\":\"A\",\"position\":1,\"reference\":\"G\",\"alternate\":\"A\",\"pdb\":\"ATOM      1  CA  GLY A   1      12.000  13.800   9.500  1.00 20.00           C\\nTER\\nEND\\n\"}",
                    actionLabel = "Map variant",
                ) }
            }
            if (capability?.id in setOf("sequence.exact_reference_search", "sequence.local_fasta_exact_search")) {
                item { BasicResearchCapabilityCard(
                    capabilityId = "sequence.exact_reference_search",
                    title = "Exact local reference search",
                    description = "Search caller-supplied FASTA references for exact full-length matches. Input JSON includes query, reference_fasta, sequence_type and source/license metadata.",
                    sample = "{\"query\":\"ACGTACGT\",\"reference_fasta\":\">ref1\\nACGTACGT\\n>ref2\\nTTTTAAAA\",\"sequence_type\":\"DNA\",\"name\":\"Example pack\",\"version\":\"1\",\"license\":\"CC0-1.0\",\"source\":\"https://example.org/reference\"}",
                    actionLabel = "Search exact matches",
                ) }
            }
            if (capability?.id in setOf("sequence.local_alignment_reference_search", "sequence.local_fasta_alignment_search")) {
                item { BasicResearchCapabilityCard(
                    capabilityId = "sequence.local_alignment_reference_search",
                    title = "Local reference alignment",
                    description = "Run bounded Smith–Waterman local alignment against caller-supplied FASTA references. No E-values or calibrated homology claims.",
                    sample = "{\"query\":\"ACGTACGT\",\"reference_fasta\":\">ref1\\nACGTACGT\\n>ref2\\nTTTTAAAA\",\"sequence_type\":\"DNA\",\"name\":\"Example pack\",\"version\":\"1\",\"license\":\"CC0-1.0\",\"source\":\"https://example.org/reference\"}",
                    actionLabel = "Align local references",
                ) }
            }
            if (capability?.id == "structure.ligand_site_candidates" ||
                capability?.id == "structure.apo_pocket_candidates") {
                item { StructureSiteAnalysisCard() }
            }
            if (capability?.id == "chemistry.sdf_graph") item { LigandGraphPreviewCard() }
            if (capability?.id == "genomics.sam_vcf") {
                item { GenomicsVcfQcCard() }
                item { U5ResearchGateCard() }
            }
            item {
                OutlinedButton(onClick = onImport, modifier = Modifier.fillMaxWidth()) {
                    Text("Import to Work")
                }
            }
            item { Footer() }
        }
    }
}

@Composable
private fun GlobalSearchScreen(
    query: String,
    onQueryChange: (String) -> Unit,
    jobs: List<ResearchJob>,
    onSelectJob: (SearchDocument) -> Unit,
    onSelectCapability: (SearchDocument) -> Unit,
    modifier: Modifier,
) {
    val context = LocalContext.current
    val capabilities = remember(context) {
        runCatching {
            loadCapabilityCatalogue(context) + CapabilityEntry(
                id = "public.reference_databases",
                name = "Public reference databases",
                status = "implemented",
                implementation = "PublicDatabaseClient.kt",
                evidenceLevel = "none",
                domain = "Public reference databases",
            )
        }.getOrDefault(emptyList())
    }
    val documents = remember(jobs, capabilities) {
        jobs.map { job ->
            SearchDocument(
                id = "job:${job.id}",
                title = job.inputName,
                subtitle = "Research job · ${job.state}",
                searchableText = listOfNotNull(job.id, job.sha256, job.message, job.provenanceToolId).joinToString(" "),
                kind = SearchDocument.Kind.JOB,
            )
        } + capabilities.map { capability ->
            SearchDocument(
                id = "capability:${capability.id}",
                title = capability.name,
                subtitle = "${capability.domain} · ${capability.status.replace('_', ' ')}",
                searchableText = "${capability.id} ${capability.implementation} ${capability.evidenceLevel}",
                kind = SearchDocument.Kind.CAPABILITY,
            )
        }
    }
    val results = remember(query, documents) { filterSearchDocuments(query, documents) }
    Frame("Find in Molecularis", "Search your workspace.", "Searches only saved local jobs and the bundled capability catalogue. No network search is performed.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item {
                MolecularisField(
                    value = query,
                    onValueChange = onQueryChange,
                    label = "Search jobs and capabilities",
                    supportingText = "Names, job state, capability IDs and implementation metadata",
                )
            }
            if (query.isBlank()) {
                item { Empty("Start with a keyword", "Search a file name, tool name, domain or capability identifier.") }
            } else if (results.isEmpty()) {
                item { Empty("No matching results", "Try a different term. Search is limited to data currently stored on this device and the bundled catalogue.") }
            } else {
                item {
                    Text("${results.size} matching result${if (results.size == 1) "" else "s"}",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                items(results, key = { it.id }) { result ->
                    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
                        MolecularisListRow(
                            title = result.title,
                            supportingText = result.subtitle,
                            trailing = { Text("OPEN", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant) },
                            onClick = {
                                if (result.kind == SearchDocument.Kind.JOB) onSelectJob(result) else onSelectCapability(result)
                            },
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun Frame(eyebrow: String, title: String, subtitle: String, modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    BoxWithConstraints(modifier.fillMaxSize(), contentAlignment = Alignment.TopCenter) {
      val horizontalPadding = when {
          maxWidth < 390.dp -> 16.dp
          maxWidth < 600.dp -> 20.dp
          else -> 24.dp
      }
      val sectionGap = if (maxWidth < 390.dp) 16.dp else 24.dp
      Column(Modifier.fillMaxWidth().widthIn(max = 840.dp).padding(horizontal = horizontalPadding),
        verticalArrangement = Arrangement.spacedBy(sectionGap)) {
        Column(Modifier.padding(top = 20.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Text(eyebrow, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelMedium)
            Text(title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Text(subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
        }
        Box(Modifier.weight(1f).fillMaxWidth()) { content() }
      }
    }
}

@Composable
private fun RuntimeStatusCard(label: String, status: String, modifier: Modifier = Modifier) {
    val colors = if (MaterialTheme.colorScheme.background.luminance() < 0.5f) MolecularisTokens.StatusDark else MolecularisTokens.StatusLight
    val tint = when (status) { "OK" -> colors.success; "Not working" -> colors.error; else -> colors.warning }
    OutlinedCard(modifier, shape = RoundedCornerShape(10.dp)) {
        Column(Modifier.padding(9.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(5.dp)) {
                Box(Modifier.size(8.dp).clip(CircleShape).background(tint))
                Text(status, style = MaterialTheme.typography.labelSmall, color = tint, fontWeight = FontWeight.Bold)
            }
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurface,
                maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
    }
}

@Composable
private fun HomeScreen(
    jobs: List<ResearchJob>, notice: String, runtime: String?, themeFamily: String, onImport: () -> Unit,
    onRuntime: () -> Unit, onOpenWork: () -> Unit, onOpenService: (String) -> Unit,
    onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
    onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit, onAnalyzeImported: (ResearchJob) -> Unit,
    onExportAnalysis: (ResearchJob) -> Unit, onAnalyzeFastq: (ResearchJob, Int) -> Unit, modifier: Modifier,
) {
    val context = LocalContext.current
    val services = remember(context) {
        runCatching {
            loadCapabilityCatalogue(context) + CapabilityEntry(
                id = "public.reference_databases",
                name = "Public reference databases",
                status = "implemented",
                implementation = "PublicDatabaseClient.kt",
                evidenceLevel = "none",
                domain = "Public reference databases",
            )
        }.getOrDefault(emptyList())
    }
    val active = jobs.count { it.state in listOf("queued", "running", "cancel_requested") }
    val done = jobs.count { it.state == "succeeded" }
    val attention = jobs.count { it.state in listOf("failed", "recovery_required") }
    val pythonPart = runtime?.substringAfter("Python probe:", "")?.substringBefore("Native probe:")?.trim()
    val nativePart = runtime?.substringAfter("Native probe:", "")?.trim()
    val pythonState = when { runtime == null -> "Not checked"; pythonPart.isNullOrBlank() -> "Partial"; pythonPart.contains("FAILED", true) -> "Not working"; pythonPart.contains("WARNING", true) || pythonPart.contains("PARTIAL", true) -> "Partial"; else -> "OK" }
    val nativeState = when { runtime == null -> "Not checked"; nativePart.isNullOrBlank() -> "Partial"; nativePart.contains("FAILED", true) -> "Not working"; nativePart.contains("WARNING", true) || nativePart.contains("PARTIAL", true) -> "Partial"; else -> "OK" }
    val storageState = when { runtime == null -> "Not checked"; runtime.contains("Keystore AES-GCM + versioned file roundtrip: passed") -> "OK"; runtime.contains("Keystore AES-GCM + versioned file roundtrip: FAILED") -> "Not working"; else -> "Partial" }
    BoxWithConstraints(modifier.fillMaxSize()) {
        LazyColumn(Modifier.fillMaxSize(), verticalArrangement = Arrangement.spacedBy(14.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item { WorkspaceCarousel(services = services, onOpenService = onOpenService) }
            item {
                DashboardPanel("SYSTEM READINESS", "Runtime and protected storage", "Sequence engine: $pythonState  ·  Native engine: $nativeState  ·  Private storage: $storageState", "Run diagnostics", onRuntime)
            }
            item {
                DashboardPanel("RESEARCH WORK", "$active active · $done complete · $attention need attention", "Your locally stored research jobs and their current lifecycle state.", "Open Work", onOpenWork)
            }
            item {
                val latest = jobs.firstOrNull()
                DashboardPanel("RECENT ACTIVITY", latest?.inputName ?: "No research activity yet",
                    latest?.let { "Latest job: ${it.state} · timestamp ${it.analysisCreatedAt ?: it.provenanceCreatedAt ?: "unavailable"}" } ?: "Import a research input to begin your first local job.",
                    if (latest == null) "Import input" else "View Work", if (latest == null) onImport else onOpenWork)
            }
            item {
                DashboardPanel("LOCAL DATA & REFERENCES", "Private research storage", "Imported files remain in app-private storage. Public reference retrieval is available as a dedicated service.", "Open databases", { onOpenService("public.reference_databases") })
            }
            if (notice.isNotBlank()) item { Notice(notice) }
            item { Footer() }
        }
    }
}

@Composable
private fun DashboardPanel(
    eyebrow: String,
    title: String,
    detail: String,
    actionLabel: String,
    onAction: () -> Unit,
) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
            Text(eyebrow, style = MaterialTheme.typography.labelSmall, letterSpacing = 1.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Text(detail, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            TextButton(onClick = onAction, contentPadding = PaddingValues(0.dp)) { Text(actionLabel) }
        }
    }
}

@Composable
private fun WorkspaceCarousel(
    services: List<CapabilityEntry>,
    onOpenService: (String) -> Unit,
) {
    val pager = rememberPagerState(pageCount = { services.size })
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        HorizontalPager(
            state = pager,
            contentPadding = PaddingValues(horizontal = 42.dp),
            pageSpacing = 12.dp,
            modifier = Modifier.fillMaxWidth(),
        ) { page ->
            val service = services[page]
            Card(
                onClick = { onOpenService(service.id) },
                modifier = Modifier.fillMaxWidth().height(218.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
            ) {
                Column(Modifier.fillMaxSize().padding(18.dp), verticalArrangement = Arrangement.SpaceBetween) {
                    Column(verticalArrangement = Arrangement.spacedBy(9.dp)) {
                        Text(service.domain.uppercase(), style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.1.sp, maxLines = 1)
                        Text(service.name, style = MaterialTheme.typography.titleLarge,
                            color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.SemiBold, maxLines = 3)
                        Text(if (service.status == "implemented") "Implementation registered · ${service.id}" else "Not implemented · ${service.id}",
                            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2)
                    }
                    Text("OPEN SERVICE  →", style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
            }
        }
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
            val visibleCount = minOf(5, services.size)
            val firstVisible = (pager.currentPage - visibleCount / 2).coerceIn(0, (services.size - visibleCount).coerceAtLeast(0))
            repeat(visibleCount) { offset ->
                val selected = pager.currentPage == firstVisible + offset
                Box(Modifier.padding(horizontal = 3.dp)
                    .size(width = if (selected) 20.dp else 7.dp, height = 7.dp)
                    .clip(RoundedCornerShape(50))
                    .background(if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline))
            }
        }
    }
}

@Composable
private fun Metric(label: String, value: String, modifier: Modifier) {
    OutlinedCard(modifier, shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(11.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold, maxLines = 1)
            Text(value, style = MolecularisScientificTextStyle.copy(fontSize = MaterialTheme.typography.headlineMedium.fontSize, fontWeight = FontWeight.Bold))
            Text("Research jobs", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
        }
    }
}

@Composable
private fun Section(title: String, action: String, onClick: () -> Unit) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text(title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.weight(1f))
        TextButton(onClick = onClick) { Text(action) }
    }
}

@Composable
private fun WorkScreen(
    jobs: List<ResearchJob>, initialQuery: String, onImport: () -> Unit, onCancel: (ResearchJob) -> Unit,
    onResume: (ResearchJob) -> Unit, onDelete: (ResearchJob) -> Unit,
    onExport: (ResearchJob) -> Unit, onExportProvenance: (ResearchJob) -> Unit,
    onExportProvenanceSummary: (ResearchJob) -> Unit, onAnalyzeImported: (ResearchJob) -> Unit,
    onExportAnalysis: (ResearchJob) -> Unit, onAnalyzeFastq: (ResearchJob, Int) -> Unit, modifier: Modifier,
) {
    var query by rememberSaveable(initialQuery) { mutableStateOf(initialQuery) }
    var filter by rememberSaveable { mutableStateOf("All") }
    val filtered = jobs.filter { job ->
        (query.isBlank() || job.inputName.contains(query, true)) && when (filter) {
            "Active" -> job.state in listOf("queued", "running", "cancel_requested")
            "Complete" -> job.state == "succeeded"
            "Attention" -> job.state in listOf("failed", "recovery_required")
            else -> true
        }
    }
    Frame("Research activity", "Your work, organized.", "Track imports, inspect integrity and manage local files.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item {
                OutlinedTextField(query, { query = it }, Modifier.fillMaxWidth(), singleLine = true,
                    shape = RoundedCornerShape(10.dp), label = { Text("Search research jobs") })
            }
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    listOf("All", "Active", "Complete", "Attention").forEach {
                        FilterChip(filter == it, { filter = it }, label = { Text(it) })
                    }
                }
            }
            item { Button(onClick = onImport, Modifier.fillMaxWidth(), shape = RoundedCornerShape(10.dp)) { Text("Import new data") } }
            if (filtered.isEmpty()) item { Empty("No matching research jobs", "Try another search or import a dataset to begin.") }
            else items(filtered, key = { it.id }) { JobCard(it, onCancel, onResume, onDelete, onExport, onExportProvenance, onExportProvenanceSummary, onAnalyzeImported, onExportAnalysis, onAnalyzeFastq) }
        }
    }
}

@Composable
private fun JobCard(job: ResearchJob, onCancel: (ResearchJob) -> Unit, onResume: (ResearchJob) -> Unit,
                    onDelete: (ResearchJob) -> Unit, onExport: (ResearchJob) -> Unit,
                    onExportProvenance: (ResearchJob) -> Unit,
                    onExportProvenanceSummary: (ResearchJob) -> Unit,
                    onAnalyzeImported: (ResearchJob) -> Unit,
                    onExportAnalysis: (ResearchJob) -> Unit,
    onAnalyzeFastq: (ResearchJob, Int) -> Unit) {
    val active = job.state in listOf("queued", "running", "cancel_requested")
    val success = job.state == "succeeded"
    val issue = job.state in listOf("failed", "recovery_required")
    var provenanceExpanded by rememberSaveable(job.id) { mutableStateOf(false) }
    var showPhredDialog by rememberSaveable(job.id) { mutableStateOf(false) }
    var selectedPhredOffset by rememberSaveable(job.id) { mutableIntStateOf(33) }
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(40.dp).clip(RoundedCornerShape(12.dp)).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                    Text(if (success) "✓" else if (issue) "!" else "▤", fontSize = 19.sp,
                        color = if (issue) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(job.inputName, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("Research import", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                StatePill(job.state)
            }
            if (active) {
                LinearProgressIndicator(Modifier.fillMaxWidth())
                Text("Processed in the background.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            job.sha256?.let { Text("SHA-256  ${it.take(12)}…", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }
            job.message?.let { Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }
            if (job.state == "recovery_required") Text(
                "Encrypted data is preserved. If its original Keystore key is lost, creating a replacement key cannot decrypt it.",
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
            if (job.provenanceToolId != null) {
                TextButton(
                    onClick = { provenanceExpanded = !provenanceExpanded },
                    modifier = Modifier.semantics {
                        contentDescription = if (provenanceExpanded) {
                            "Hide import provenance"
                        } else {
                            "Inspect import provenance"
                        }
                    },
                ) {
                    Text(if (provenanceExpanded) "Hide provenance" else "Inspect provenance")
                }
                if (provenanceExpanded) {
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = MaterialTheme.colorScheme.surfaceVariant,
                        shape = RoundedCornerShape(12.dp),
                    ) {
                        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text("IMPORT PROVENANCE", style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            Text("Tool: ${job.provenanceToolId}", style = MaterialTheme.typography.bodySmall)
                            Text("Version: ${job.provenanceToolVersion ?: "unknown"}",
                                style = MaterialTheme.typography.bodySmall)
                            job.provenanceCreatedAt?.let {
                                val recorded = java.time.format.DateTimeFormatter.ISO_INSTANT
                                    .format(java.time.Instant.ofEpochMilli(it))
                                Text("Recorded: $recorded", style = MaterialTheme.typography.bodySmall)
                            }
                            job.sha256?.let {
                                Text("Input SHA-256: $it", style = MaterialTheme.typography.labelSmall)
                            }
                            job.provenanceParametersJson?.let {
                                Text("Parameters: $it", style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            TextButton(
                                onClick = { onExportProvenance(job) },
                                modifier = Modifier.semantics {
                                    contentDescription = "Export import provenance as JSON"
                                },
                            ) {
                                Text("Export provenance JSON")
                            }
                            TextButton(
                                onClick = { onExportProvenanceSummary(job) },
                                modifier = Modifier.semantics {
                                    contentDescription = "Export human-readable import provenance summary"
                                },
                            ) {
                                Text("Export provenance summary")
                            }
                        }
                    }
                }
            }
            if (job.analysisResultJson != null) {
                var analysisExpanded by rememberSaveable(job.id) { mutableStateOf(false) }
                TextButton(onClick = { analysisExpanded = !analysisExpanded }) {
                    Text(if (analysisExpanded) "Hide analysis result" else "View saved analysis result")
                }
                if (analysisExpanded) {
                    val result = remember(job.id, job.analysisResultJson) {
                        runCatching { JSONObject(job.analysisResultJson) }.getOrNull()
                    }
                    Text("Method: ${job.analysisToolId ?: "unknown"} · Version: ${job.analysisToolVersion ?: "unknown"}",
                        style = MaterialTheme.typography.labelSmall)
                    job.analysisCreatedAt?.let { created ->
                        Text("Saved: ${java.time.format.DateTimeFormatter.ISO_INSTANT.format(java.time.Instant.ofEpochMilli(created))}",
                            style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Text("Input SHA-256: ${job.sha256 ?: "not recorded"}",
                        style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    job.analysisParametersJson?.let {
                        Text("Parameters: $it", style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    if (result != null) {
                        Text("Records: ${result.optInt("record_count")} · Total bases: ${result.optLong("total_bases")}",
                            style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                        if (result.has("phred_offset")) Text(
                            "Encoding: Phred+${result.optInt("phred_offset")} · Mean quality: ${result.optDouble("mean_phred")}",
                            style = MaterialTheme.typography.bodySmall)
                        if (result.has("q20_fraction")) Text(
                            "Q20: ${"%.1f".format(result.optDouble("q20_fraction") * 100)}% · Q30: ${"%.1f".format(result.optDouble("q30_fraction") * 100)}%",
                            style = MaterialTheme.typography.bodySmall)
                        val records = result.optJSONArray("records") ?: result.optJSONArray("reads")
                        if (records != null) {
                            Text("RECORD PREVIEW", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant)
                            for (index in 0 until minOf(records.length(), 5)) {
                                val item = records.optJSONObject(index) ?: continue
                                val summary = buildString {
                                    append(item.optString("identifier", "record ${index + 1}"))
                                    append(" · ${item.optInt("length")} bases")
                                    if (item.has("gc_percent")) append(" · GC ${item.optDouble("gc_percent")}%")
                                    if (item.has("mean_phred")) append(" · mean Q ${item.optDouble("mean_phred")}")
                                }
                                Text(summary, style = MaterialTheme.typography.bodySmall)
                            }
                            if (records.length() > 5) Text("Showing first 5 of ${records.length()} records. Export the full result for all records.",
                                style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        val limitations = result.optJSONArray("limitations")
                        if (limitations != null) {
                            Text("LIMITATIONS", style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant)
                            for (index in 0 until limitations.length()) {
                                Text("• ${limitations.optString(index)}", style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    } else {
                        Text("Saved result is not valid JSON and cannot be rendered as a structured preview. The original stored record remains exportable.",
                            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
                    }
                    TextButton(onClick = { onExportAnalysis(job) }) { Text("Export complete analysis JSON") }
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                if (active) OutlinedButton(onClick = { onCancel(job) }) { Text("Cancel") }
                if (job.state == "cancelled" || job.state == "failed") OutlinedButton(onClick = { onResume(job) }) { Text("Resume") }
                if (success && job.analysisResultJson == null && job.inputName.lowercase().removeSuffix(".gz").substringAfterLast('.') in setOf("fa", "fasta", "fna")) OutlinedButton(onClick = { onAnalyzeImported(job) }) { Text("Run FASTA QC") }
                if (success && job.inputName.lowercase().removeSuffix(".gz").substringAfterLast('.') in setOf("fastq", "fq")) OutlinedButton(onClick = { showPhredDialog = true }) { Text("Run FASTQ QC") }
                if (success) Button(onClick = { onExport(job) }) { Text("Export") }
                if (success || issue || job.state == "cancelled") OutlinedButton(onClick = { onDelete(job) }) { Text("Delete") }
            }
        }
    }
    if (showPhredDialog) AlertDialog(
        onDismissRequest = { showPhredDialog = false },
        title = { Text("Choose FASTQ quality encoding") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Molecularis never guesses the Phred offset. Select the encoding used by this file.")
                listOf(33, 64).forEach { offset ->
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(selected = selectedPhredOffset == offset, onClick = { selectedPhredOffset = offset })
                        Column {
                            Text("Phred+$offset", style = MaterialTheme.typography.bodyMedium)
                            Text(if (offset == 33) "Sanger / modern Illumina" else "Legacy Illumina 1.3–1.7",
                                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        },
        confirmButton = { TextButton(onClick = { showPhredDialog = false; onAnalyzeFastq(job, selectedPhredOffset) }) { Text("Run QC") } },
        dismissButton = { TextButton(onClick = { showPhredDialog = false }) { Text("Cancel") } },
    )
}

@Composable
private fun StatePill(state: String) {
    val text = when (state) {
        "succeeded" -> "COMPLETE"; "queued" -> "QUEUED"; "running" -> "RUNNING"
        "cancel_requested" -> "STOPPING"; "failed" -> "FAILED"; "cancelled" -> "CANCELLED"
        "recovery_required" -> "RECOVERY"; else -> state.uppercase()
    }
    val statusColors = if (MaterialTheme.colorScheme.background.luminance() < 0.5f) {
        MolecularisTokens.StatusDark
    } else {
        MolecularisTokens.StatusLight
    }
    val statusColor = when (state) {
        "succeeded" -> statusColors.success
        "failed" -> statusColors.error
        "recovery_required" -> statusColors.warning
        "queued", "running", "cancel_requested" -> statusColors.information
        else -> MaterialTheme.colorScheme.onSurfaceVariant
    }
    Surface(
        color = MaterialTheme.colorScheme.surfaceVariant,
        shape = RoundedCornerShape(6.dp),
        modifier = Modifier.semantics { contentDescription = "Job status: $text" },
    ) {
        Text(text, Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            style = MaterialTheme.typography.labelSmall,
            color = statusColor)
    }
}

private data class CapabilityEntry(
    val id: String,
    val name: String,
    val status: String,
    val implementation: String,
    val evidenceLevel: String,
    val domain: String,
)

private fun loadCapabilityCatalogue(context: Context): List<CapabilityEntry> {
    val source = context.assets.open("capability-catalog.json")
        .bufferedReader(Charsets.UTF_8).use { it.readText() }
    val tools = JSONArray(source)
    return buildList {
        for (index in 0 until tools.length()) {
            val item = tools.getJSONObject(index)
            add(
                CapabilityEntry(
                    id = item.getString("id"),
                    name = item.getString("name"),
                    status = item.getString("status"),
                    implementation = item.getString("implementation"),
                    evidenceLevel = item.getString("evidence_level"),
                    domain = item.getString("domain"),
                ),
            )
        }
    }
}

@Composable
private fun BasicResearchCapabilityCard(
    capabilityId: String,
    title: String,
    description: String,
    sample: String,
    actionLabel: String,
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var input by rememberSaveable(capabilityId) { mutableStateOf(sample) }
    var running by remember(capabilityId) { mutableStateOf(false) }
    var result by remember(capabilityId) { mutableStateOf<String?>(null) }
    var error by remember(capabilityId) { mutableStateOf<String?>(null) }
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text(description, style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            OutlinedTextField(
                value = input,
                onValueChange = {
                    if (it.length <= AndroidBasicCapabilityRunner.MAX_INPUT_CHARS) {
                        input = it
                        result = null
                        error = null
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("Research input") },
                minLines = 3,
                maxLines = 6,
                supportingText = { Text("Processed locally · maximum 1,000,000 characters") },
            )
            Button(
                onClick = {
                    running = true
                    error = null
                    result = null
                    scope.launch {
                        val outcome = withContext(Dispatchers.IO) {
                            runCatching {
                                AndroidBasicCapabilityRunner.analyze(context, capabilityId, input)
                            }
                        }
                        outcome.onSuccess { raw ->
                            result = runCatching { JSONObject(raw).toString(2) }.getOrDefault(raw)
                        }.onFailure { error = it.message ?: "Analysis failed" }
                        running = false
                    }
                },
                enabled = !running && input.isNotBlank(),
                modifier = Modifier.fillMaxWidth(),
            ) { Text(if (running) "Analysing…" else actionLabel) }
            error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
            result?.let {
                HorizontalDivider()
                Text("RESULT", style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                Text(it, style = MaterialTheme.typography.bodySmall)
                Text("Exploratory research output only. Interpret within the stated method limitations.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun FastaQcCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var fastaText by rememberSaveable {
        mutableStateOf(">example_sequence\nACGTACGTGCGTNNACGT\n")
    }
    var running by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<SequenceQcResult?>(null) }
    var error by remember { mutableStateOf<String?>(null) }

    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("FASTA quick quality check", style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold)
            Text("Run the registered local FASTA parser and basic sequence statistics. Input stays on this device.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            OutlinedTextField(
                value = fastaText,
                onValueChange = {
                    if (it.length <= SequenceQcRunner.MAX_INPUT_CHARS) {
                        fastaText = it
                        error = null
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("FASTA input") },
                minLines = 4,
                maxLines = 8,
                supportingText = { Text("Up to 1,000,000 characters · multiple records supported") },
            )
            Button(
                onClick = {
                    running = true
                    error = null
                    result = null
                    scope.launch {
                        val outcome = withContext(Dispatchers.IO) {
                            runCatching { SequenceQcRunner.analyze(context, fastaText) }
                        }
                        outcome.onSuccess { result = it }
                            .onFailure { error = it.message ?: "FASTA analysis failed" }
                        running = false
                    }
                },
                enabled = !running && fastaText.isNotBlank(),
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text(if (running) "Analysing…" else "Analyse FASTA")
            }
            error?.let {
                Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
            }
            result?.let { summary ->
                HorizontalDivider()
                Text("${summary.recordCount} records · ${summary.totalBases} total bases",
                    fontWeight = FontWeight.SemiBold)
                summary.records.forEach { record ->
                    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(record.identifier, style = MaterialTheme.typography.labelLarge,
                            maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text("${record.length} bases · ${String.format(java.util.Locale.ROOT, "%.2f", record.gcPercent)}% GC (all symbols) · ${record.ambiguousCount} non-ACGT symbols",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                Text("Basic QC only. No sequence identity, function, pathogenicity or clinical interpretation is inferred. Independent biological validation is not claimed.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}


@Composable
private fun FastqQcCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var input by rememberSaveable { mutableStateOf("@read_1\nACGTACGT\n+\nIIII!!!!\n") }
    var offset by rememberSaveable { mutableIntStateOf(33) }
    var running by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<FastqQcResult?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("FASTQ read-quality check", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text("Wrapped FASTQ parsing. Quality encoding must be selected explicitly; it is never guessed.",
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            OutlinedTextField(value = input, onValueChange = {
                if (it.length <= SequenceQcRunner.MAX_INPUT_CHARS) { input = it; error = null }
            }, modifier = Modifier.fillMaxWidth(), label = { Text("FASTQ input") },
                minLines = 4, maxLines = 8,
                supportingText = { Text("Up to 1,000,000 characters · wrapped reads supported") })
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                FilterChip(selected = offset == 33, onClick = { offset = 33; result = null }, label = { Text("Phred+33") })
                FilterChip(selected = offset == 64, onClick = { offset = 64; result = null }, label = { Text("Phred+64") })
            }
            Button(onClick = {
                running = true; error = null; result = null
                scope.launch {
                    val outcome = withContext(Dispatchers.IO) {
                        runCatching { SequenceQcRunner.analyzeFastq(context, input, offset) }
                    }
                    outcome.onSuccess { result = it }.onFailure { error = it.message ?: "FASTQ analysis failed" }
                    running = false
                }
            }, enabled = !running && input.isNotBlank(), modifier = Modifier.fillMaxWidth()) {
                Text(if (running) "Analysing…" else "Analyse FASTQ")
            }
            error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
            result?.let { summary ->
                HorizontalDivider()
                Text("${summary.recordCount} reads · ${summary.totalBases} bases · Phred+${summary.phredOffset}",
                    fontWeight = FontWeight.SemiBold)
                Text("Mean Q ${String.format(java.util.Locale.ROOT, "%.2f", summary.meanPhred)} · Q20 ${String.format(java.util.Locale.ROOT, "%.1f", summary.q20Fraction * 100)}% · Q30 ${String.format(java.util.Locale.ROOT, "%.1f", summary.q30Fraction * 100)}%",
                    style = MaterialTheme.typography.bodySmall)
                summary.reads.take(20).forEach { read ->
                    Text("${read.identifier}: ${read.length} bases · mean Q ${String.format(java.util.Locale.ROOT, "%.2f", read.meanPhred)}",
                        style = MaterialTheme.typography.labelSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                if (summary.reads.size > 20) Text("${summary.reads.size - 20} additional reads omitted from this preview.",
                    style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("Quality summary only. No adapter detection/trimming, variant calling or clinical conclusions.",
                    style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun SettingsScreen(
    runtime: String?, onRuntime: () -> Unit, onRefresh: () -> Unit,
    themeFamily: String, onThemeFamilyChange: (String) -> Unit,
    biometricEnabled: Boolean, biometricAvailable: Boolean, onBiometricChange: (Boolean) -> Unit,
    debugBuild: Boolean, onOpenComponentGallery: () -> Unit,
    modifier: Modifier,
) {
    Frame("Workspace controls", "Settings & diagnostics.", "Understand the device, local data and privacy boundary.", modifier) {
        LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(bottom = 24.dp)) {
            item { SettingGroup("APPEARANCE · THEME", "Choose Light Classic, Dark Classic or follow your Android system appearance. Your choice is saved on this device.") {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("light" to "Light", "dark" to "Dark", "system" to "System").forEach { (key, label) ->
                        FilterChip(selected = themeFamily == key, onClick = { onThemeFamilyChange(key) }, label = { Text(label) }, modifier = Modifier.weight(1f))
                    }
                }
                Text("System sans-serif typography is used. Additional font files require licence and glyph review.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            } }
            item { SettingGroup(
                "SECURITY · BIOMETRIC APP UNLOCK",
                "Optional device-local app lock. This is not an online account login. Android manages biometric templates; Molecularis never receives or stores them. Research files remain encrypted at rest independently of this screen lock.",
            ) {
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                        Text("Unlock with biometrics or device credential", style = MaterialTheme.typography.bodyMedium)
                        Text(
                            if (biometricAvailable) "Available on this device" else "No supported biometric or device credential is currently enrolled",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    Switch(
                        checked = biometricEnabled,
                        onCheckedChange = onBiometricChange,
                        enabled = biometricAvailable || biometricEnabled,
                    )
                }
            } }
            item { SettingGroup("DEVICE RUNTIME", "Scientific processing and storage checks run locally on this device.") {
                Button(onRuntime, Modifier.fillMaxWidth()) { Text("Run runtime diagnostics") }
                val pythonPart = runtime?.substringAfter("Python probe:", "")?.substringBefore("Native probe:")?.trim()
                val nativePart = runtime?.substringAfter("Native probe:", "")?.trim()
                val pythonState = when {
                    runtime == null -> "Not checked"
                    pythonPart.isNullOrBlank() -> "Partial"
                    pythonPart.contains("FAILED", true) -> "Not working"
                    pythonPart.contains("WARNING", true) || pythonPart.contains("PARTIAL", true) -> "Partial"
                    else -> "OK"
                }
                val nativeState = when {
                    runtime == null -> "Not checked"
                    nativePart.isNullOrBlank() -> "Partial"
                    nativePart.contains("FAILED", true) -> "Not working"
                    nativePart.contains("WARNING", true) || nativePart.contains("PARTIAL", true) -> "Partial"
                    else -> "OK"
                }
                val storageState = when {
                    runtime == null -> "Not checked"
                    runtime.contains("Keystore AES-GCM + versioned file roundtrip: passed") -> "OK"
                    runtime.contains("FAILED", true) -> "Not working"
                    else -> "Partial"
                }
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    RuntimeStatusCard("Sequence engine", pythonState, Modifier.weight(1f))
                    RuntimeStatusCard("Native engine", nativeState, Modifier.weight(1f))
                    RuntimeStatusCard("Private storage", storageState, Modifier.weight(1f))
                }
            } }
            item { SettingGroup("LOCAL STORAGE", "Research inputs use Keystore-backed AES-GCM and app-private storage.") {
                OutlinedButton(onRefresh, Modifier.fillMaxWidth()) { Text("Refresh local job state") }
            } }
            item { SettingGroup(
                "PRIVACY · LOCAL DATA INVENTORY",
                "This app has no cloud account or remote compute service. Public reference searches send only the chosen public query/accession to approved database endpoints; imported research files stay local. The following information is stored locally:",
            ) {
                Text("• Imported inputs: AES-256-GCM encrypted chunks in the app's no-backup private directory. Plaintext is materialized temporarily in app-private cache for analysis/export and is removed on normal completion; stale prefixed cache files older than 24 hours are cleaned at store startup.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Job database: input display name, selected content URI, job state, byte count, SHA-256, timestamps, storage path and import provenance are stored in the app-private SQLite database. This metadata database is not separately encrypted by the current implementation.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Analysis results: FASTA/FASTQ result JSON and method parameters are currently stored in that SQLite database. Treat the device's app-private storage and OS account protection as part of the security boundary.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Public reference records: raw FASTA/mmCIF payloads are encrypted with Android Keystore AES-GCM in app-private no-backup storage. Source metadata and public FASTA QC JSON are stored in a separate app-private SQLite database and are not separately encrypted.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Public network requests: only user-entered public names/accessions are sent to NCBI, UniProtKB or RCSB. Raw sequences, VCFs, patient/sample identifiers and private research files are not submitted. Retrieved data are parsed and analysed locally.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Preferences: appearance, onboarding acknowledgement and the optional local app-lock setting are stored in private SharedPreferences.",
                    style = MaterialTheme.typography.bodySmall)
                Text("• Exports: only created after you select a destination in Android's document picker. Copies at that destination are outside Molecularis' control.",
                    style = MaterialTheme.typography.bodySmall)
                Text("Deletion removes the app-managed files and database rows where operations succeed. Flash-storage secure erasure and deletion of exported copies cannot be guaranteed. Android backup is disabled in the app manifest; merged-manifest and device verification remain pending.",
                    style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("Screenshot/Recents protection is not enabled pending explicit threat review and owner approval. Do not treat the optional app lock as protection against a compromised or rooted device.",
                    style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            } }
            item { SettingGroup("DATA PACKS & LICENCES", "Reference packs require version, source, checksum and licence metadata. Third-party engines retain their own terms.") }
            item { SettingGroup("ACCESSIBILITY", "System light/dark mode and font scaling are respected. Status is conveyed with text, not colour alone.") }
            item { SettingGroup("ABOUT KINETICS", "Research Mode · Version 0.0.1 · Apache-2.0 project code. Not for clinical use.") }
            if (debugBuild) item {
                SettingGroup("DESIGN SYSTEM · DEVELOPER", "Open the live V1 component gallery. This route is available only in debug builds.") {
                    OutlinedButton(onClick = onOpenComponentGallery, modifier = Modifier.fillMaxWidth()) {
                        Text("Open component gallery")
                    }
                }
            }
            item { Footer() }
        }
    }
}

@Composable
private fun SettingGroup(title: String, description: String, content: @Composable () -> Unit = {}) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Text(title, color = MaterialTheme.colorScheme.onSurface, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            Text(description, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            content()
        }
    }
}


@Composable
private fun InfoPill(label: String) {
    Surface(color = MaterialTheme.colorScheme.surfaceVariant, shape = RoundedCornerShape(6.dp)) {
        Text(label, Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun Empty(title: String, detail: String) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp)) {
        Column(Modifier.fillMaxWidth().padding(22.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("No recent items", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 13.sp)
            Text(title, fontWeight = FontWeight.Bold)
            Text(detail, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun Notice(message: String) {
    OutlinedCard(Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp)) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Dot(MaterialTheme.colorScheme.secondary)
            Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Text("Workspace notice", fontWeight = FontWeight.SemiBold, style = MaterialTheme.typography.labelMedium)
                Text(message, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun Dot(color: Color) {
    Box(Modifier.padding(top = 4.dp).size(9.dp).clip(CircleShape).background(color)
        .semantics { contentDescription = "Status indicator" })
}

@Composable
internal fun BiometricLockScreen(
    error: String?,
    themeFamily: String,
    onRetry: () -> Unit,
) {
    val resolvedTheme = when (themeFamily) {
        "system" -> if (isSystemInDarkTheme()) "dark" else "light"
        else -> themeFamily
    }
    val isDark = resolvedTheme == "dark"
    val palette = if (isDark) MolecularisTokens.MolecularisDarkClassic else MolecularisTokens.MolecularisLightClassic
    val scheme = if (isDark) {
        darkColorScheme(
            primary = palette.primary,
            onPrimary = palette.background,
            secondary = palette.secondary,
            tertiary = palette.tertiary,
            background = palette.background,
            surface = palette.surface,
            onSurface = palette.text,
            onBackground = palette.text,
            surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted,
            outline = palette.outline,
        )
    } else {
        lightColorScheme(
            primary = palette.primary,
            secondary = palette.secondary,
            tertiary = palette.tertiary,
            background = palette.background,
            surface = palette.surface,
            onSurface = palette.text,
            onBackground = palette.text,
            surfaceVariant = palette.surfaceAlt,
            onSurfaceVariant = palette.muted,
            outline = palette.outline,
        )
    }
    MaterialTheme(colorScheme = scheme, typography = MolecularisTypography) {
        Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
            Box(
                Modifier.fillMaxSize().padding(horizontal = 24.dp, vertical = 32.dp),
                contentAlignment = Alignment.Center,
            ) {
                Column(
                    Modifier.fillMaxWidth().widthIn(max = 420.dp)
                        .clip(RoundedCornerShape(30.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(horizontal = 16.dp, vertical = 22.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    repeat(3) {
                        Surface(
                            modifier = Modifier.fillMaxWidth().height(54.dp),
                            shape = RoundedCornerShape(12.dp),
                            color = MaterialTheme.colorScheme.surface,
                        ) {}
                    }
                    Surface(
                        modifier = Modifier.fillMaxWidth().height(54.dp),
                        shape = RoundedCornerShape(12.dp),
                        color = MaterialTheme.colorScheme.surface,
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            IconButton(
                                onClick = onRetry,
                                modifier = Modifier.size(52.dp)
                                    .semantics { contentDescription = "Unlock with device biometric or screen credential" },
                            ) {
                                Icon(
                                    Icons.Filled.Fingerprint,
                                    contentDescription = null,
                                    modifier = Modifier.size(30.dp),
                                    tint = MaterialTheme.colorScheme.primary,
                                )
                            }
                        }
                    }
                    Text(
                        "LOCAL DEVICE UNLOCK",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurface,
                        fontWeight = FontWeight.SemiBold,
                        letterSpacing = 1.1.sp,
                    )
                    if (error != null) {
                        Text(
                            error,
                            modifier = Modifier.fillMaxWidth().semantics { contentDescription = "Unlock error: $error" },
                            color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodySmall,
                        )
                    }
                    Text(
                        "Use your enrolled biometric or device screen credential. This is not an online account sign-in.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    TextButton(onClick = onRetry) { Text("Try again") }
                    Text(
                        "Android manages biometric data. Molecularis does not receive or store biometric templates.",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

@Composable
private fun Footer() {
    Text("KINETICS · Research Mode only · Not for clinical use",
        Modifier.fillMaxWidth().padding(vertical = 8.dp), color = MaterialTheme.colorScheme.onSurfaceVariant,
        style = MaterialTheme.typography.labelSmall, letterSpacing = .8.sp)
}
