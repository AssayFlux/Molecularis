"""Strict S4 prediction-evidence envelope and experimental CA comparison.

No prediction engine or node client is implemented here. This module validates
provenance-bearing outputs supplied by a separately approved prediction service.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime
from math import isclose, isfinite
from typing import Any, Iterable

from .structure import Atom, rmsd
from .structure_view import validate_viewer_payload

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWY")


def validate_prediction_envelope(
    sequence: str,
    envelope: dict[str, Any],
    *,
    max_residues: int = 100_000,
    max_payload_bytes: int = 32 * 1024 * 1024,
) -> dict[str, object]:
    """Validate sequence/model/node provenance and per-residue confidence fields.

    A valid envelope is structurally well-formed only. Model accuracy, confidence
    calibration, license compatibility and node trust require independent review.
    """
    if isinstance(max_residues, bool) or not isinstance(max_residues, int) or max_residues < 1:
        raise ValueError("max_residues must be a positive integer")
    normalized = "".join(sequence.split()).upper() if isinstance(sequence, str) else ""
    if not normalized or set(normalized) - _AMINO_ACIDS:
        raise ValueError("sequence must contain canonical amino-acid letters")
    if len(normalized) > max_residues:
        raise ValueError("sequence exceeds max_residues")
    expected_hash = hashlib.sha256(normalized.encode("ascii")).hexdigest()

    required = {
        "schema", "input_sequence_sha256", "sequence_length", "model", "node",
        "created_at", "predicted_structure", "confidence", "limitations",
    }
    if not isinstance(envelope, dict) or set(envelope) != required:
        raise ValueError("Prediction envelope has missing or unsupported fields")
    if envelope["schema"] != "kinetics.structure-prediction.v1":
        raise ValueError("Unsupported prediction envelope schema")
    if envelope["input_sequence_sha256"] != expected_hash:
        raise ValueError("Prediction input sequence SHA-256 does not match")
    if (
        isinstance(envelope["sequence_length"], bool)
        or not isinstance(envelope["sequence_length"], int)
        or envelope["sequence_length"] != len(normalized)
    ):
        raise ValueError("Prediction sequence_length does not match input")

    model = envelope["model"]
    if not isinstance(model, dict) or set(model) != {
        "name", "version", "weights_sha256", "license",
    }:
        raise ValueError("Prediction model provenance is incomplete")
    for field in ("name", "version", "license"):
        if not isinstance(model[field], str) or not model[field].strip():
            raise ValueError(f"Prediction model {field} must be non-empty text")
    if not isinstance(model["weights_sha256"], str) or not _SHA256.fullmatch(model["weights_sha256"]):
        raise ValueError("Prediction model weights_sha256 must be lowercase SHA-256 hex")

    node = envelope["node"]
    if not isinstance(node, dict) or set(node) != {"node_id", "software_version", "run_id"}:
        raise ValueError("Prediction node provenance is incomplete")
    for field in ("node_id", "software_version", "run_id"):
        if not isinstance(node[field], str) or not node[field].strip():
            raise ValueError(f"Prediction node {field} must be non-empty text")
    created_at = envelope["created_at"]
    if not isinstance(created_at, str):
        raise ValueError("Prediction created_at must be timezone-aware ISO-8601 text")
    try:
        parsed_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Prediction created_at must be valid ISO-8601") from exc
    if parsed_time.tzinfo is None or parsed_time.utcoffset() is None:
        raise ValueError("Prediction created_at must include a timezone")

    structure = envelope["predicted_structure"]
    if not isinstance(structure, dict):
        raise ValueError("Prediction structure must be an object")
    validate_viewer_payload(structure, max_payload_bytes=max_payload_bytes)

    confidence = envelope["confidence"]
    if not isinstance(confidence, dict) or set(confidence) != {
        "plddt_per_residue", "mean_plddt", "pae_mean_angstrom", "pae_max_angstrom",
    }:
        raise ValueError("Prediction confidence fields are incomplete")
    plddt = confidence["plddt_per_residue"]
    if not isinstance(plddt, list) or len(plddt) != len(normalized):
        raise ValueError("Per-residue pLDDT length must match input sequence length")
    values: list[float] = []
    for value in plddt:
        if (
            isinstance(value, bool) or not isinstance(value, (int, float))
            or not isfinite(value) or not 0.0 <= value <= 100.0
        ):
            raise ValueError("pLDDT values must be finite numbers in [0, 100]")
        values.append(float(value))
    mean_plddt = confidence["mean_plddt"]
    if (
        isinstance(mean_plddt, bool) or not isinstance(mean_plddt, (int, float))
        or not isfinite(mean_plddt) or not 0.0 <= mean_plddt <= 100.0
        or not isclose(float(mean_plddt), sum(values) / len(values), rel_tol=1e-6, abs_tol=1e-4)
    ):
        raise ValueError("mean_plddt does not match per-residue values")
    for field in ("pae_mean_angstrom", "pae_max_angstrom"):
        value = confidence[field]
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, (int, float))
            or not isfinite(value) or value < 0
        ):
            raise ValueError(f"{field} must be null or a finite non-negative number")
    if not isinstance(envelope["limitations"], list) or not envelope["limitations"] or any(
        not isinstance(item, str) or not item.strip() for item in envelope["limitations"]
    ):
        raise ValueError("Prediction limitations must be non-empty text entries")

    return {
        "schema": "kinetics.structure-prediction-validation.v1",
        "status": "unverified_prediction",
        "input_sequence_sha256": expected_hash,
        "sequence_length": len(normalized),
        "mean_plddt": sum(values) / len(values),
        "model_license_status": "not_approved",
        "confidence_calibration": "not_assessed",
        "node_trust_status": "not_assessed",
        "limitations": [
            "Envelope validation does not establish prediction accuracy or confidence calibration.",
            "Model weights and dataset licenses require separate review before redistribution.",
            "Node identity, transport security and execution integrity require independent verification.",
            "Predicted coordinates are not experimental evidence.",
        ],
    }


def compare_predicted_to_experimental_ca(
    predicted_atoms: Iterable[Atom],
    experimental_atoms: Iterable[Atom],
    *,
    predicted_source_sha256: str,
    experimental_source_sha256: str,
    max_residues: int = 100_000,
) -> dict[str, object]:
    """Compare matching CA coordinates by exact chain/residue identity and superposed RMSD."""
    if (
        not isinstance(max_residues, int)
        or isinstance(max_residues, bool)
        or max_residues < 1
    ):
        raise ValueError("max_residues must be a positive integer")
    for name, value in (
        ("predicted_source_sha256", predicted_source_sha256),
        ("experimental_source_sha256", experimental_source_sha256),
    ):
        if not isinstance(value, str) or not _SHA256.fullmatch(value):
            raise ValueError(f"{name} must be lowercase SHA-256 hex")

    def ca_index(atoms: Iterable[Atom], label: str) -> dict[tuple[str, int, str], Atom]:
        indexed: dict[tuple[str, int, str], Atom] = {}
        for atom in atoms:
            if atom.name.strip().upper() != "CA":
                continue
            key = (atom.chain, atom.residue_number, atom.residue)
            if key in indexed:
                raise ValueError(f"{label} contains duplicate CA residue keys")
            if len(indexed) >= max_residues:
                raise ValueError(f"{label} exceeds max_residues")
            if not all(isfinite(value) for value in (atom.x, atom.y, atom.z)):
                raise ValueError(f"{label} contains non-finite CA coordinates")
            indexed[key] = atom
        if not indexed:
            raise ValueError(f"{label} contains no CA coordinates")
        return indexed

    predicted = ca_index(predicted_atoms, "Predicted structure")
    experimental = ca_index(experimental_atoms, "Experimental structure")
    if predicted.keys() != experimental.keys():
        raise ValueError("Predicted and experimental CA residue keys do not match exactly")
    keys = sorted(predicted)
    rmsd_value = rmsd(
        [experimental[key] for key in keys],
        [predicted[key] for key in keys],
        superpose=True,
    )
    return {
        "schema": "kinetics.structure-experimental-comparison.v1",
        "status": "coordinate_comparison_only",
        "predicted_source_sha256": predicted_source_sha256,
        "experimental_source_sha256": experimental_source_sha256,
        "matched_ca_residues": len(keys),
        "superposed_ca_rmsd_angstrom": rmsd_value,
        "tm_score": None,
        "limitations": [
            "Exact chain/residue/residue-name keys are required; no alignment is performed.",
            "CA RMSD depends on the supplied residue correspondence and does not measure all-atom quality.",
            "No TM-score, confidence calibration, biological function or experimental validity is inferred.",
        ],
    }
