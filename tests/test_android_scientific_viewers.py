import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_home_routes_to_real_offline_structure_and_chemistry_viewers() -> None:
    ui = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/MolecularisUi.kt").read_text()
    viewer = (
        ROOT / "android/app/src/main/java/org/assayflux/molecularis/StructureViewer.kt"
    ).read_text()
    chemistry = (
        ROOT / "android/app/src/main/java/org/assayflux/molecularis/I1ChemistryCard.kt"
    ).read_text()
    assert "ServiceDetailScreen" in ui
    assert "ENGINE SOURCE REGISTERED" in ui
    assert "Android workflow: not connected" in ui
    assert "A registered Python engine is not automatically runnable" in ui
    assert "HorizontalPager(" in ui
    assert "OPEN SERVICE" in ui
    assert "fun ExploreScreen" not in ui
    assert "MolecularisTab.Explore" not in ui
    assert "StructureViewerPreview(publicRecord = publicStructureRecord)" in ui
    assert "LigandGraphPreviewCard()" in ui
    assert "WebViewAssetLoader" in viewer
    assert "settings.blockNetworkLoads = true" in viewer
    assert 'CreateDocument("image/svg+xml")' in viewer
    assert 'CreateDocument("image/png")' in viewer
    assert "Ligand chemistry workspace" in chemistry
    assert "DialogProperties(usePlatformDefaultWidth = false)" in chemistry
    assert "fullScreen" in chemistry
    assert "DialogProperties(usePlatformDefaultWidth = false)" in viewer
    assert "fullScreen" in viewer
    assert "RDKit sanitization" in chemistry


def test_vcf_research_screen_is_attestation_gated_and_aggregate_only() -> None:
    card = (
        ROOT / "android/app/src/main/java/org/assayflux/molecularis/GenomicsVcfQcCard.kt"
    ).read_text()
    runner = (
        ROOT / "android/app/src/main/java/org/assayflux/molecularis/GenomicsVcfQcRunner.kt"
    ).read_text()
    gate = (
        ROOT / "android/app/src/main/java/org/assayflux/molecularis/U5ResearchGateCard.kt"
    ).read_text()
    assert "enabled = !busy && selectedUri != null && authorizationConfirmed" in card
    assert "MAX_INPUT_BYTES = 5 * 1024 * 1024" in runner
    assert "sample identifiers and genotype strings" in card
    assert "RESEARCH TESTING · OWNER AUTHORIZED" in gate
    assert "institutional approval" in gate
    assert "not bundled or presented as runnable on Android" in gate
    assert "ResearchStore" not in card
    assert "openOutputStream" not in card
    assert "Clinical Mode" not in card



def test_android_vcf_chaquopy_bridge_returns_only_aggregate_qc() -> None:
    bridge_path = ROOT / "android/app/src/main/python/molecularis_probe.py"
    spec = importlib.util.spec_from_file_location("molecularis_probe_u5_test", bridge_path)
    assert spec is not None and spec.loader is not None
    bridge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bridge)
    fixture = (
        "##fileformat=VCFv4.3\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYNTHETIC_SAMPLE\n"
        "chr1\t10\t.\tA\tG\t50\tPASS\t.\tGT\t0/1\n"
    )
    report = json.loads(bridge.summarize_vcf_research_qc(fixture))
    assert report["record_count"] == 1
    assert report["sample_count"] == 1
    assert report["source_sha256"]
    assert "SYNTHETIC_SAMPLE" not in str(report)
    assert "0/1" not in str(report)
    assert "genotypes" not in report and "samples" not in report


def test_android_safe_insets_status_cards_and_gzip_imports() -> None:
    ui = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/MolecularisUi.kt").read_text()
    main = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/MainActivity.kt").read_text()
    vcf = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/GenomicsVcfQcCard.kt").read_text()
    structure = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/StructureViewer.kt").read_text()
    chemistry = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/I1ChemistryCard.kt").read_text()
    sequence = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/SequenceFileSupport.kt").read_text()
    assert "WindowInsets.safeDrawing" in ui
    assert 'getString("theme_family", "system")' in main
    assert "RuntimeStatusCard" in ui
    assert "runtime?.let { Text(it" not in ui
    assert "GZIPInputStream" in vcf
    assert "GZIPInputStream" in structure
    assert "GZIPInputStream" in chemistry
    assert "GZIPInputStream" in sequence
    assert "total <= maxBytes" in sequence


def test_owner_blueprint_has_one_actionable_card_per_capability() -> None:
    ui = (ROOT / "android/app/src/main/java/org/assayflux/molecularis/MolecularisUi.kt").read_text()
    catalogue = json.loads((ROOT / "android/app/src/main/assets/capability-catalog.json").read_text())
    assert len(catalogue) == 68
    assert "rememberPagerState(pageCount = { services.size })" in ui
    assert "onOpenService(service.id)" in ui
    assert "capabilities.firstOrNull { it.id == selectedServiceId }" in ui
    assert "val visibleCount = minOf(5, services.size)" in ui
    assert 'id = "public.reference_databases"' in ui
    assert "DashboardPanel(\"SYSTEM READINESS\"" in ui
    assert "DashboardPanel(\"RESEARCH WORK\"" in ui
    assert "DashboardPanel(\"RECENT ACTIVITY\"" in ui
    assert "DashboardPanel(\"LOCAL DATA & REFERENCES\"" in ui
    assert "NavigationBar(" not in ui
    assert "NavigationRail(" not in ui
    assert 'label = { Text("Search") }' in ui
    assert 'contentDescription = "Open profile"' in ui
    assert "Icons.Filled.Fingerprint" in ui
    assert "import androidx.compose.material.icons.filled.Fingerprint" in ui
    assert 'if (capability?.id == "genomics.sam_vcf")' in ui
    assert 'if (domain == "Genomics" || domain == "Variant")' not in ui
    assert "repeat(3)" in ui
    assert "LOCAL DEVICE UNLOCK" in ui
    assert "not an online account sign-in" in ui
    assert "Public reference databases" in ui[ui.index("private fun GlobalSearchScreen"):]
    assert '"local_profile_name"' in ui
    assert '"local_profile_avatar_uri"' in ui
    assert "ProfileAvatarButton" in ui
    assert '"local_workspace_id"' in ui
    assert "Device-local workspace ID" in ui
    assert "Remote sign-in, password reset, account recovery" in ui
