"""Dependency-injected local S4 structure-prediction engine contract.

This module contains no bundled prediction model, weights, network client or
inference runtime. A separately installed local engine implements the protocol.
"""
from __future__ import annotations

from typing import Protocol

from .structure_prediction import validate_prediction_envelope


class LocalPredictionEngine(Protocol):
    """Contract implemented by an approved local structure-prediction engine."""

    execution_mode: str
    engine_id: str
    software_version: str
    model_provenance: dict[str, str]
    node_provenance: dict[str, str]

    def predict(self, sequence: str) -> dict[str, object]:
        """Return a kinetics.structure-prediction.v1 envelope."""


def run_local_structure_prediction(
    sequence: str,
    engine: LocalPredictionEngine,
    *,
    max_residues: int = 100_000,
    max_payload_bytes: int = 32 * 1024 * 1024,
) -> dict[str, object]:
    """Execute an injected local engine and validate its complete result envelope.

    The adapter does not download models, access the network, or launch arbitrary
    processes. The host application is responsible for installing and approving
    the engine implementation and its model/license artifacts.
    """
    if not isinstance(sequence, str):
        raise TypeError("Prediction sequence must be text")
    normalized_sequence = "".join(sequence.split()).upper()
    if not normalized_sequence or len(normalized_sequence) > max_residues:
        raise ValueError("Prediction sequence is empty or exceeds max_residues")
    if any(residue not in "ACDEFGHIKLMNPQRSTVWY" for residue in normalized_sequence):
        raise ValueError("Prediction sequence must contain canonical amino-acid residues")
    if engine.execution_mode != "local":
        raise ValueError("S4 prediction engine must declare execution_mode='local'")
    if not isinstance(engine.engine_id, str) or not engine.engine_id.strip():
        raise ValueError("Prediction engine_id must be non-empty")
    if not isinstance(engine.software_version, str) or not engine.software_version.strip():
        raise ValueError("Prediction engine software_version must be non-empty")
    expected_model_fields = {"name", "version", "weights_sha256", "license"}
    expected_node_fields = {"node_id", "software_version", "run_id"}
    if not isinstance(engine.model_provenance, dict) or set(engine.model_provenance) != expected_model_fields:
        raise ValueError("Prediction engine model_provenance is incomplete")
    if not isinstance(engine.node_provenance, dict) or set(engine.node_provenance) != expected_node_fields:
        raise ValueError("Prediction engine node_provenance is incomplete")

    for key, value in engine.model_provenance.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Prediction model provenance {key} must be non-empty text")
    digest = engine.model_provenance["weights_sha256"]
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ValueError("Prediction weights_sha256 must be lowercase SHA-256 hex")
    for key, value in engine.node_provenance.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Prediction node provenance {key} must be non-empty text")
    envelope = engine.predict(normalized_sequence)
    if not isinstance(envelope, dict):
        raise ValueError("Prediction engine must return an envelope object")
    if envelope.get("model") != engine.model_provenance:
        raise ValueError("Prediction envelope model provenance differs from installed engine")
    if envelope.get("node") != engine.node_provenance:
        raise ValueError("Prediction envelope node provenance differs from installed engine")
    validation = validate_prediction_envelope(
        normalized_sequence,
        envelope,
        max_residues=max_residues,
        max_payload_bytes=max_payload_bytes,
    )
    return {
        "schema": "kinetics.local-prediction-run.v1",
        "execution_mode": "local",
        "engine_id": engine.engine_id,
        "software_version": engine.software_version,
        "validation": validation,
        "prediction_envelope": envelope,
        "limitations": [
            "The adapter validates output structure and provenance, not model accuracy.",
            ("The host must independently approve engine code, model weights, dataset "
             "licenses and runtime dependencies."),
            ("Local execution is declared by the adapter; the host must enforce its own "
             "network isolation policy."),
            "Confidence calibration and experimental concordance remain separate release gates.",
        ],
    }
