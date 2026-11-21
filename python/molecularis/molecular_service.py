"""MSDE artifact-store integration for the Molecular service (A)."""
from __future__ import annotations

from typing import Any

from .molecular_model import Molecule
from .platform import Artifact, Budget, Capability, ExecutionContext, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

MOLECULE_MEDIA_TYPE = "application/vnd.molecularis.molecule+json"
MOLECULE_SCHEMA_ID = "molecularis.molecule.v1"
VALIDATE_CAPABILITY_ID = "molecular.validate.v1"
VALIDATION_REPORT_SCHEMA_ID = "molecularis.molecular-validation-report.v1"
MOLECULE_REFERENCE_SCHEMA_ID = "molecularis.molecule-artifact-reference.v1"


def ingest_molecule(
    platform: MolecularisPlatform,
    molecule: Molecule,
    *,
    parents: tuple[str, ...] = (),
    budget: Budget | None = None,
) -> Artifact:
    """Persist a validated molecule as an immutable, provenance-linked artifact."""
    if not isinstance(molecule, Molecule):
        raise TypeError("molecule must be a validated Molecule instance")
    return platform.ingest(
        molecule.to_json(),
        media_type=MOLECULE_MEDIA_TYPE,
        schema_id=MOLECULE_SCHEMA_ID,
        metadata={
            "molecule_id": molecule.molecule_id,
            "molecule_sha256": molecule.sha256,
            "formula": molecule.formula,
            "atom_count": molecule.atom_count,
            "bond_count": molecule.bond_count,
            "net_formal_charge": molecule.net_formal_charge,
            "coordinate_unit": molecule.coordinate_unit,
            "coordinate_system": molecule.coordinate_system,
        },
        parents=parents,
        budget=budget,
    )


def load_molecule(
    platform: MolecularisPlatform,
    artifact_id: str,
    *,
    budget: Budget | None = None,
) -> Molecule:
    """Integrity-check, decode and structurally validate a stored molecule."""
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.schema_id != MOLECULE_SCHEMA_ID or artifact.media_type != MOLECULE_MEDIA_TYPE:
        raise ValidationError(
            "artifact is not a Molecular v1 document",
            details={"artifact_id": artifact_id, "schema_id": artifact.schema_id},
        )
    if artifact.size_bytes > budget.max_bytes:
        raise ResourceLimitError("molecule artifact exceeds byte budget")
    payload = b"".join(platform.store.read(artifact_id, budget=budget))
    molecule = Molecule.from_json(payload)
    expected_metadata = {
        "molecule_id": molecule.molecule_id,
        "molecule_sha256": molecule.sha256,
        "formula": molecule.formula,
        "atom_count": molecule.atom_count,
        "bond_count": molecule.bond_count,
        "net_formal_charge": molecule.net_formal_charge,
        "coordinate_unit": molecule.coordinate_unit,
        "coordinate_system": molecule.coordinate_system,
    }
    if molecule.sha256 != artifact.digest or any(
        artifact.metadata.get(key) != value for key, value in expected_metadata.items()
    ):
        raise ValidationError("molecule content or metadata does not match the verified artifact")
    return molecule


def register_molecular_service(platform: MolecularisPlatform) -> None:
    """Register the v1 validator capability and its Rulebook handler."""
    capability = Capability(
        id=VALIDATE_CAPABILITY_ID,
        version="1.0.0",
        service="molecular",
        operation="validate",
        input_schema=MOLECULE_REFERENCE_SCHEMA_ID,
        output_schema=VALIDATION_REPORT_SCHEMA_ID,
        deterministic=True,
        description="Integrity-check and structurally validate a stored Molecular v1 artifact.",
    )
    platform.register(capability)

    def validate_artifact(
        inputs: dict[str, Any], parameters: dict[str, Any], context: ExecutionContext
    ) -> dict[str, Any]:
        if len(inputs) != 1:
            raise ValidationError("molecular.validate requires exactly one molecule artifact ID")
        artifact_id = next(iter(inputs.values()))
        if not isinstance(artifact_id, str):
            raise ValidationError("molecular.validate artifact ID must be a string")
        molecule = load_molecule(platform, artifact_id, budget=context.budget)
        expected_sha = parameters.get("expected_sha256")
        if expected_sha is not None and expected_sha != molecule.sha256:
            raise ValidationError("molecule digest differs from expected_sha256")
        return {
            "schema": VALIDATION_REPORT_SCHEMA_ID,
            "valid": True,
            "molecule_id": molecule.molecule_id,
            "molecule_sha256": molecule.sha256,
            "formula": molecule.formula,
            "atom_count": molecule.atom_count,
            "bond_count": molecule.bond_count,
            "net_formal_charge": molecule.net_formal_charge,
            "connected_component_count": len(molecule.connected_components()),
            "rulebook": "molecular-structural-v1",
            "rules_checked": [
                "MOL-001", "MOL-002", "MOL-003", "MOL-004", "MOL-005",
                "MOL-006", "MOL-007", "MOL-008", "MOL-009", "MOL-010",
            ],
        }

    platform.bind(VALIDATE_CAPABILITY_ID, validate_artifact)


def molecular_validation_rulebook(
    artifact_key: str = "molecule_artifact_id",
    *,
    expected_sha256: str | None = None,
) -> Rulebook:
    """Create the canonical one-operation Rulebook for structural validation."""
    if not isinstance(artifact_key, str) or not artifact_key.strip():
        raise ValueError("artifact_key must be non-empty text")
    parameters: dict[str, Any] = {}
    if expected_sha256 is not None:
        parameters["expected_sha256"] = expected_sha256
    return Rulebook(
        id="molecular-structural-validation",
        version="1.0.0",
        operations=(
            Operation(
                id="validate-molecule",
                capability_id=VALIDATE_CAPABILITY_ID,
                inputs=(artifact_key,),
                output="molecular_validation",
                parameters=parameters,
            ),
        ),
    )
