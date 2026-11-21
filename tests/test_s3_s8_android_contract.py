from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON_BRIDGE = ROOT / "android/app/src/main/python/molecularis_probe.py"
ANDROID_JAVA = ROOT / "android/app/src/main/java/org/assayflux/molecularis"


def test_s3_s8_chaquopy_bridge_exposes_bounded_python_dispatchers() -> None:
    source = PYTHON_BRIDGE.read_text(encoding="utf-8")
    assert "def analyze_ligand_site(" in source
    assert "def analyze_apo_pockets(" in source
    assert "def infer_genetic_code_from_fasta(" in source
    assert "parse_pdb(source_text, include_hetero=True)" in source
    assert "parse_mmcif(source_text, include_hetero=True)" in source
    assert "len(fasta_text) > 1_000_000" in source
    assert "len(records) >= 1_000" in source
    assert "infer_genetic_code_candidates(records, min_records=3, min_codons=90)" in source


def test_s3_s8_android_runner_enforces_limits_and_calls_python_dispatchers() -> None:
    source = (ANDROID_JAVA / "S3S8Runner.kt").read_text(encoding="utf-8")
    assert "MAX_STRUCTURE_BYTES = 16 * 1024 * 1024" in source
    assert "MAX_FASTA_CHARS = 1_000_000" in source
    assert '"analyze_ligand_site"' in source
    assert '"analyze_apo_pockets"' in source
    assert '"infer_genetic_code_from_fasta"' in source
    assert "cutoffAngstrom.isFinite()" in source


def test_s3_s8_explore_cards_are_real_registry_gated_actions() -> None:
    ui = (ANDROID_JAVA / "MolecularisUi.kt").read_text(encoding="utf-8")
    cards = (ANDROID_JAVA / "S3S8ResearchCards.kt").read_text(encoding="utf-8")
    assert 'item { StructureSiteAnalysisCard() }' in ui
    assert 'item { GeneticCodeInferenceCard() }' in ui
    assert 'capability?.id == "structure.ligand_site_candidates"' in ui
    assert 'capability?.id == "structure.apo_pocket_candidates"' in ui
    assert 'capability?.id == "sequence.genetic_code_candidate_inference"' in ui
    assert 'ActivityResultContracts.OpenDocument()' in cards
    assert "S3S8Runner.analyzeLigandSite" in cards
    assert "S3S8Runner.analyzeApoPockets" in cards
    assert "S3S8Runner.inferGeneticCode" in cards
    assert "No affinity, specificity, mechanism or function is inferred." in cards
    assert "no organism-specific genetic code is assigned" in cards
    assert "source_sha256" in PYTHON_BRIDGE.read_text(encoding="utf-8")
    assert "generated_at_utc" in PYTHON_BRIDGE.read_text(encoding="utf-8")
    assert "Input SHA-256" in cards


def test_i1_android_ligand_graph_preview_is_bounded_and_registry_gated() -> None:
    bridge = PYTHON_BRIDGE.read_text(encoding="utf-8")
    runner = (ANDROID_JAVA / "I1ChemistryRunner.kt").read_text(encoding="utf-8")
    card = (ANDROID_JAVA / "I1ChemistryCard.kt").read_text(encoding="utf-8")
    ui = (ANDROID_JAVA / "MolecularisUi.kt").read_text(encoding="utf-8")
    assert "def analyze_ligand_sdf_graph(" in bridge
    assert "analyze_sdf_graph(source_text)" in bridge
    assert "json.dumps(analyze_sdf_graph(source_text), sort_keys=True)" in bridge
    assert "MAX_SDF_BYTES = 16 * 1024 * 1024" in runner
    assert '"analyze_ligand_sdf_graph"' in runner
    assert "ActivityResultContracts.OpenDocument()" in card
    assert "readI1LigandDocument" in card
    chemistry_source = (ROOT / "python/molecularis/chemistry.py").read_text(encoding="utf-8")
    assert "source_sha256" in bridge or "source_sha256" in chemistry_source
    assert 'capability?.id == "chemistry.sdf_graph"' in ui
    assert "LigandGraphPreviewCard()" in ui
    assert "Graph-only parsing; no chemical sanitization or valence validation" in chemistry_source
