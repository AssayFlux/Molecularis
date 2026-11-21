from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import validate

from molecularis.molecular_model import MolecularAtom, MolecularBond, Molecule
from molecularis.molecular_service import (
    MOLECULE_SCHEMA_ID,
    ingest_molecule,
    load_molecule,
    molecular_validation_rulebook,
    register_molecular_service,
)
from molecularis.platform import Budget, ExecutionContext, MolecularisPlatform
from molecularis.platform.contracts import ValidationError


def water() -> Molecule:
    return Molecule(
        "water-service-test", "water",
        (
            MolecularAtom("O", "O", position_angstrom=(0.0, 0.0, 0.0)),
            MolecularAtom("H1", "H", position_angstrom=(0.9572, 0.0, 0.0)),
            MolecularAtom("H2", "H", position_angstrom=(-0.239, 0.927, 0.0)),
        ),
        (MolecularBond("b1", "O", "H1"), MolecularBond("b2", "O", "H2")),
    )


def test_molecule_artifact_round_trip_and_metadata(tmp_path) -> None:
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    molecule = water()
    artifact = ingest_molecule(platform, molecule)
    restored = load_molecule(platform, artifact.artifact_id)
    assert restored == molecule
    assert artifact.schema_id == MOLECULE_SCHEMA_ID
    root = Path(__file__).resolve().parents[1]
    reference_schema = json.loads(
        (root / "services/molecular/schemas/molecule-artifact-reference-v1.schema.json").read_text()
    )
    validate(instance=artifact.artifact_id, schema=reference_schema)
    assert artifact.metadata["formula"] == "H2O"
    assert artifact.metadata["atom_count"] == 3
    platform.close()


def test_artifact_parent_lineage_is_preserved(tmp_path) -> None:
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    source = platform.ingest(b"source", media_type="text/plain", schema_id="test:source")
    artifact = ingest_molecule(platform, water(), parents=(source.artifact_id,))
    assert artifact.parents == (source.artifact_id,)
    platform.close()


def test_wrong_artifact_type_is_rejected(tmp_path) -> None:
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    artifact = platform.ingest(b"not a molecule", media_type="text/plain", schema_id="test:raw")
    with pytest.raises(ValidationError, match="not a Molecular"):
        load_molecule(platform, artifact.artifact_id)
    platform.close()


def test_molecular_rulebook_executes_and_records_provenance(tmp_path) -> None:
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    molecule_artifact = ingest_molecule(platform, water())
    register_molecular_service(platform)
    context = ExecutionContext(service_id="molecular", budget=Budget(max_bytes=1_000_000))
    result = platform.execute(
        molecular_validation_rulebook(expected_sha256=water().sha256),
        {"molecule_artifact_id": molecule_artifact.artifact_id},
        context=context,
    )
    report = result["molecular_validation"]
    assert report["valid"] is True
    assert report["formula"] == "H2O"
    assert report["rules_checked"][-1] == "MOL-010"
    root = Path(__file__).resolve().parents[1]
    report_schema = json.loads((root / "services/molecular/schemas/molecular-validation-report-v1.schema.json").read_text())
    validate(instance=report, schema=report_schema)
    run = platform.store.get_run(context.run_id)
    assert run["status"] == "succeeded"
    assert molecule_artifact.artifact_id in run["inputs"]
    output_artifact = platform.store.get(run["outputs"][0])
    assert molecule_artifact.artifact_id in output_artifact.parents
    platform.close()


def test_rulebook_rejects_expected_digest_mismatch(tmp_path) -> None:
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    molecule_artifact = ingest_molecule(platform, water())
    register_molecular_service(platform)
    with pytest.raises(ValidationError, match="expected_sha256"):
        platform.execute(
            molecular_validation_rulebook(expected_sha256="0" * 64),
            {"molecule_artifact_id": molecule_artifact.artifact_id},
        )
    platform.close()


def test_rulebook_supports_custom_artifact_input_key(tmp_path) -> None:
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    artifact = ingest_molecule(platform, water())
    register_molecular_service(platform)
    result = platform.execute(
        molecular_validation_rulebook("input_molecule"),
        {"input_molecule": artifact.artifact_id},
    )
    assert result["molecular_validation"]["valid"] is True
    platform.close()


def test_molecule_load_enforces_byte_budget(tmp_path) -> None:
    from molecularis.platform.contracts import ResourceLimitError

    platform = MolecularisPlatform(tmp_path)
    platform.start()
    artifact = ingest_molecule(platform, water())
    with pytest.raises(ResourceLimitError, match="byte budget"):
        load_molecule(platform, artifact.artifact_id, budget=Budget(max_bytes=1))
    platform.close()
