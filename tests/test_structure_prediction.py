from __future__ import annotations

import hashlib

import pytest

from molecularis.structure import Atom
from molecularis.structure_prediction import (
    compare_predicted_to_experimental_ca,
    validate_prediction_envelope,
)
from molecularis.structure_view import prepare_viewer_payload


def _atom(serial: int, residue: str, number: int, x: float) -> Atom:
    return Atom(serial, "CA", residue, "A", number, x, 0.0, 0.0, "C")


def _envelope(sequence: str) -> dict[str, object]:
    digest = hashlib.sha256(sequence.encode("ascii")).hexdigest()
    payload = prepare_viewer_payload([_atom(1, "ALA", 1, 0.0)], source_format="pdb")
    return {
        "schema": "kinetics.structure-prediction.v1",
        "input_sequence_sha256": digest,
        "sequence_length": len(sequence),
        "model": {
            "name": "synthetic-model",
            "version": "1.0",
            "weights_sha256": "a" * 64,
            "license": "review-required",
        },
        "node": {"node_id": "node-test", "software_version": "1.0", "run_id": "run-1"},
        "created_at": "2026-11-09T04:00:00Z",
        "predicted_structure": payload,
        "confidence": {
            "plddt_per_residue": [80.0] * len(sequence),
            "mean_plddt": 80.0,
            "pae_mean_angstrom": None,
            "pae_max_angstrom": None,
        },
        "limitations": ["Synthetic test envelope only"],
    }


def test_prediction_envelope_validates_provenance_and_abstains_from_quality_claims() -> None:
    result = validate_prediction_envelope("AG", _envelope("AG"))
    assert result["status"] == "unverified_prediction"
    assert result["mean_plddt"] == 80.0
    assert result["confidence_calibration"] == "not_assessed"
    assert result["model_license_status"] == "not_approved"


def test_prediction_envelope_rejects_sequence_hash_and_confidence_mismatch() -> None:
    envelope = _envelope("AG")
    envelope["input_sequence_sha256"] = "b" * 64
    with pytest.raises(ValueError, match="SHA-256"):
        validate_prediction_envelope("AG", envelope)

    envelope = _envelope("AG")
    envelope["confidence"]["plddt_per_residue"] = [80.0]
    with pytest.raises(ValueError, match="length"):
        validate_prediction_envelope("AG", envelope)


def test_experimental_ca_comparison_requires_exact_correspondence_and_hashes() -> None:
    predicted = [_atom(1, "ALA", 1, 10.0), _atom(2, "GLY", 2, 11.0)]
    experimental = [_atom(1, "ALA", 1, 0.0), _atom(2, "GLY", 2, 1.0)]
    result = compare_predicted_to_experimental_ca(
        predicted, experimental,
        predicted_source_sha256="a" * 64,
        experimental_source_sha256="b" * 64,
    )
    assert result["matched_ca_residues"] == 2
    assert result["superposed_ca_rmsd_angstrom"] == pytest.approx(0.0, abs=1e-8)
    assert result["tm_score"] is None


def test_experimental_ca_comparison_rejects_mismatched_residue_keys() -> None:
    with pytest.raises(ValueError, match="do not match"):
        compare_predicted_to_experimental_ca(
            [_atom(1, "ALA", 1, 0.0)],
            [_atom(1, "GLY", 1, 0.0)],
            predicted_source_sha256="a" * 64,
            experimental_source_sha256="b" * 64,
        )
