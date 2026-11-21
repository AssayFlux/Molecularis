from __future__ import annotations

import hashlib

import pytest

from molecularis.s4_engine import run_local_structure_prediction
from molecularis.structure import Atom
from molecularis.structure_view import prepare_viewer_payload


class _FakeEngine:
    execution_mode = "local"
    engine_id = "fixture-engine"
    software_version = "1.0"
    model_provenance = {
        "name": "synthetic",
        "version": "1",
        "weights_sha256": "a" * 64,
        "license": "test-only",
    }
    node_provenance = {
        "node_id": "local-fixture",
        "software_version": "1.0",
        "run_id": "fixture-run",
    }

    def predict(self, sequence: str) -> dict[str, object]:
        payload = prepare_viewer_payload(
            [Atom(1, "CA", "ALA", "A", 1, 0.0, 0.0, 0.0, "C")],
            source_format="pdb",
        )
        return {
            "schema": "kinetics.structure-prediction.v1",
            "input_sequence_sha256": hashlib.sha256(sequence.encode("ascii")).hexdigest(),
            "sequence_length": len(sequence),
            "model": self.model_provenance,
            "node": self.node_provenance,
            "created_at": "2026-11-10T00:00:00Z",
            "predicted_structure": payload,
            "confidence": {
                "plddt_per_residue": [80.0] * len(sequence),
                "mean_plddt": 80.0,
                "pae_mean_angstrom": None,
                "pae_max_angstrom": None,
            },
            "limitations": ["Synthetic fixture"],
        }


def test_s4_adapter_executes_local_engine_and_validates_result() -> None:
    result = run_local_structure_prediction("AG", _FakeEngine())
    assert result["execution_mode"] == "local"
    assert result["engine_id"] == "fixture-engine"
    assert result["validation"]["status"] == "unverified_prediction"


def test_s4_adapter_rejects_remote_or_mismatched_engine_provenance() -> None:
    engine = _FakeEngine()
    engine.execution_mode = "remote"
    with pytest.raises(ValueError, match="local"):
        run_local_structure_prediction("AG", engine)

    class _MismatchedEnvelopeEngine(_FakeEngine):
        def predict(self, sequence: str) -> dict[str, object]:
            envelope = super().predict(sequence)
            envelope["node"] = {**self.node_provenance, "node_id": "other"}
            return envelope

    with pytest.raises(ValueError, match="node provenance"):
        run_local_structure_prediction("AG", _MismatchedEnvelopeEngine())
