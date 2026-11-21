"""Molecularis-owned entry points for optional scientific engines.

This module deliberately keeps native engine objects behind adapters. Availability is
not scientific validation, and optional engines are never imported at package import
time. Platform-specific and model-backed engines must be installed in an isolated,
approved runtime profile.
"""
from __future__ import annotations

import importlib.util
import shutil
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Literal


@dataclass(frozen=True)
class EngineSpec:
    engine_id: str
    family: str
    integration: str
    runtime: str
    adapter: str
    limitations: tuple[str, ...]


# All 19 named projects are listed; pysam and HTSlib are one paired stack among
# the 18 integration targets. Mol* is an existing offline viewer asset.
ENGINE_SPECS: tuple[EngineSpec, ...] = (
    EngineSpec("biopython", "sequence/alignment/structure", "integrated", "python>=3.10", "molecularis.alignment_biopython", ("File-level licence review and Android runtime proof remain open.",)),
    EngineSpec("biotite", "sequence/structure", "integrated", "isolated Python>=3.12 profile", "molecularis.structure_biotite", ("Text mmCIF only; BinaryCIF and assembly expansion remain open.",)),
    EngineSpec("parasail", "alignment", "optional-adapter", "native host library / Python bindings", "align_with_parasail", ("Only global and local affine-gap alignment are exposed; SIMD build and score-width validation remain open.",)),
    EngineSpec("pysam", "genomics", "integrated", "optional Python/native profile", "molecularis.genomics_htslib", ("Molecularis read model is not lossless for all tags and header metadata.",)),
    EngineSpec("htslib", "genomics", "integrated-via-pysam", "native library bundled by pysam or host profile", "molecularis.genomics_htslib", ("Native binary provenance and complete format differential corpus remain open.",)),
    EngineSpec("bcftools", "variant analysis", "integrated-via-pysam", "pinned optional pysam/HTSlib profile", "molecularis.genomics_tools.bcftools_normalize", ("Reference-based normalization and multiallelic splitting are exposed; full bcftools command coverage and differential validation remain open.",)),
    EngineSpec("samtools", "alignment processing", "integrated-via-pysam", "pinned optional pysam/HTSlib profile", "molecularis.genomics_tools.samtools_view/sort/index/flagstat", ("View, sort, index and flagstat operations are exposed; broader command coverage and format differential validation remain open.",)),
    EngineSpec("esm", "protein representation", "integrated-local-inference", "operator-supplied ESM checkpoint; approved PyTorch/Transformers profile", "molecularis.esm_inference.run_esm_embeddings", ("Offline embeddings and mean pooling are implemented for local Transformers ESM checkpoints; no weights are bundled and functional prediction calibration is not provided.",)),
    EngineSpec("alphafold", "protein structure prediction", "integrated-local-runner", "operator-installed AlphaFold 3 source, Google-issued model weights and local sequence databases", "molecularis.advanced_science.run_alphafold3", ("Runs the official local inference entry point with pinned interpreter, script, model and database digests; caller must obtain weights directly from Google and comply with separate terms; output accuracy remains independently unassessed.",)),
    EngineSpec("molstar", "structure visualization", "viewer-integrated", "offline Android/WebView assets", "android/app/src/main/assets/structure-viewer", ("Full data bridge, accessibility and large-structure performance remain open.",)),
    EngineSpec("molprobity", "structure validation", "integrated-local-cli", "operator-installed MolProbity command-line tools", "molecularis.advanced_science.run_molprobity_cli", ("Runs clashscore, mp_geometry or residue-analysis and preserves raw outputs; one selected tool is not a complete MolProbity report.",)),
    EngineSpec("rdkit", "cheminformatics", "integrated", "optional Python/native profile", "molecularis.chemistry_rdkit", ("Stereochemistry, salts, tautomers and broader sanitization corpus remain open.",)),
    EngineSpec("autodock-vina", "docking", "integrated", "optional host profile", "molecularis.docking_vina", ("Prepared PDBQT inputs only; independent docking benchmarks remain open.",)),
    EngineSpec("openmm", "molecular dynamics", "integrated", "optional host CPU profile", "molecularis.md_openmm", ("Caller-prepared systems only; force-field and preparation governance remain open.",)),
    EngineSpec("gromacs", "molecular dynamics", "integrated", "hash-pinned local executable; caller-prepared TPR", "molecularis.gromacs.run_gromacs", ("Executes caller-prepared TPR files and returns hashed trajectory/energy artifacts; topology preparation and physical validation remain separate.",)),
    EngineSpec("scipy", "numerical science", "integrated-reference", "optional validation environment", "SciPy-backed validation modules", ("Not a universal runtime dependency; per-workflow pins and reference tests remain open.",)),
    EngineSpec("nuad", "DNA/RNA nanotechnology", "integrated-local-design", "operator-installed NUAD and its declared dependencies", "molecularis.advanced_science.run_nuad_design", ("Runs caller-constructed NUAD designs with constraints, a fixed seed and iteration bound; NUPACK/ViennaRNA-backed constraints retain their own licensing and runtime requirements.",)),
    EngineSpec("nupack", "DNA/RNA nanotechnology", "license-blocked", "Caltech-issued license and approved deployment model required", "not enabled", ("The standard NUPACK license prohibits redistribution and use in web applications or graphical user interfaces; obtain a separate written license covering Molecularis before integration.",)),
    EngineSpec("galaxy", "workflow orchestration", "integrated-client", "separately operated HTTPS Galaxy server; injected API key", "molecularis.galaxy.GalaxyClient", ("Creates histories, uploads hashed inputs, invokes caller-selected workflows, polls execution and downloads output datasets with SHA-256; workflow mapping, scientific output validation and server-specific conformance remain open.",)),
)


def engine_inventory() -> list[dict[str, object]]:
    """Return the stable, JSON-serializable inventory for all requested engines."""
    return [asdict(spec) for spec in ENGINE_SPECS]


def discover_engine(engine_id: str) -> dict[str, object]:
    """Report whether an optional engine can be discovered in this process.

    Discovery never imports the engine or loads model weights. It is not a health,
    compatibility, licence, or scientific-validation check.
    """
    normalized = engine_id.strip().lower() if isinstance(engine_id, str) else ""
    spec = next((item for item in ENGINE_SPECS if item.engine_id == normalized), None)
    if spec is None:
        raise ValueError(f"Unknown engine_id: {engine_id!r}")

    python_modules = {
        "biopython": ("Bio",),
        "biotite": ("biotite",),
        "parasail": ("parasail",),
        "pysam": ("pysam",),
        "esm": ("esm",),
        "rdkit": ("rdkit",),
        "autodock-vina": ("vina",),
        "openmm": ("openmm",),
        "scipy": ("scipy",),
        "nuad": ("nuad",),
        "nupack": ("nupack",),
    }
    executables = {
        "bcftools": ("bcftools",),
        "samtools": ("samtools",),
        "molprobity": ("phenix.molprobity", "molprobity"),
        "gromacs": ("gmx", "gmx_mpi"),
    }
    if normalized == "htslib":
        found = importlib.util.find_spec("pysam") is not None
        detail = "pysam provides the HTSlib-backed interface" if found else "pysam/HTSlib not found"
    elif normalized == "molstar":
        found = False
        detail = "Viewer assets are shipped in the Android source tree; this host probe does not inspect APK assets"
    elif normalized in python_modules:
        found = any(importlib.util.find_spec(name) is not None for name in python_modules[normalized])
        detail = "Python module found" if found else "Python module not found"
    elif normalized in executables:
        paths = [shutil.which(name) for name in executables[normalized]]
        found = any(paths)
        detail = next((path for path in paths if path), "Executable not found")
    elif normalized in {"alphafold", "galaxy"}:
        found = False
        detail = "Requires separately configured model process or Galaxy server"
    else:
        found = False
        detail = "No runtime probe is defined"
    return {
        "engine_id": normalized,
        "integration": spec.integration,
        "discovered": found,
        "detail": detail,
        "discovery_only": True,
        "scientific_validation": "not_assessed",
    }


def align_with_parasail(
    sequence_a: str,
    sequence_b: str,
    *,
    mode: Literal["global", "local"] = "global",
    match_score: int = 2,
    mismatch_score: int = -1,
    gap_open: int = 5,
    gap_extend: int = 1,
    alphabet: str = "ACGTN",
    max_sequence_length: int = 100_000,
    max_alignment_cells: int = 4_000_000,
) -> dict[str, object]:
    """Run Parasail traceback alignment using a Molecularis-owned result envelope.

    Parasail's affine-gap API uses positive gap penalties; returned scores and
    traceback are engine outputs. This wrapper does not enumerate tied alignments.
    """
    if mode not in {"global", "local"}:
        raise ValueError("mode must be 'global' or 'local'")
    for name, value in (("match_score", match_score), ("mismatch_score", mismatch_score),
                        ("gap_open", gap_open), ("gap_extend", gap_extend)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer")
    if match_score <= 0 or mismatch_score > 0 or gap_open < 0 or gap_extend < 0:
        raise ValueError("Use positive match, non-positive mismatch, and non-negative gap penalties")
    if not isinstance(sequence_a, str) or not isinstance(sequence_b, str):
        raise TypeError("sequences must be strings")
    a, b = sequence_a.upper(), sequence_b.upper()
    if not a or not b:
        raise ValueError("Both sequences must be non-empty")
    if len(a) > max_sequence_length or len(b) > max_sequence_length:
        raise ValueError("Sequence exceeds max_sequence_length")
    if (len(a) + 1) * (len(b) + 1) > max_alignment_cells:
        raise ValueError("Alignment exceeds max_alignment_cells")
    if not isinstance(alphabet, str) or len(set(alphabet)) != len(alphabet) or not alphabet:
        raise ValueError("alphabet must be non-empty text with unique symbols")
    if set(a + b) - set(alphabet):
        raise ValueError("Sequences contain symbols not represented in the configured alphabet")

    try:
        import parasail  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError("Parasail Python bindings are unavailable in this runtime") from error

    matrix = parasail.matrix_create(alphabet, match_score, mismatch_score)
    function = parasail.nw_trace if mode == "global" else parasail.sw_trace
    result = function(a, b, gap_open, gap_extend, matrix)
    if getattr(result, "saturated", False):
        raise OverflowError("Parasail reported score saturation; result is not accepted")
    traceback = getattr(result, "traceback", None)
    if traceback is None:
        raise RuntimeError("Parasail did not return traceback data")
    cigar_object = getattr(result, "cigar", None)
    cigar = cigar_object.decode if cigar_object is not None else None
    score = float(result.score)
    if not isfinite(score):
        raise RuntimeError("Parasail returned a non-finite alignment score")
    return {
        "schema_version": 1,
        "engine": "parasail",
        "engine_version": str(getattr(parasail, "__version__", "unknown")),
        "algorithm": "needleman-wunsch" if mode == "global" else "smith-waterman",
        "mode": mode,
        "score": score,
        "traceback": {
            "query": str(traceback.query),
            "reference": str(traceback.ref),
            "comparison": str(traceback.comp),
        },
        "cigar": str(cigar) if cigar is not None else None,
        "sequence_lengths": [len(a), len(b)],
        "scoring": {
            "match": match_score,
            "mismatch": mismatch_score,
            "gap_open": gap_open,
            "gap_extend": gap_extend,
            "gap_penalty_convention": "positive penalties passed to Parasail",
        },
        "limitations": [
            "Global and local modes only; no semi-global end-gap configuration.",
            "The first engine traceback is returned; tied optimal tracebacks are not enumerated.",
            "No claim of parity with Molecularis or Biopython until differential fixtures pass.",
        ],
    }
