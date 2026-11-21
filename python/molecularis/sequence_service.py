"""Sequence service B: canonical sequence artifacts and MSDE capabilities."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from typing import Any

from .genetic_code import translate_coding_sequence
from .platform import Artifact, Budget, Capability, ExecutionContext, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError
from .sequence import DNA, PROTEIN, RNA, reverse_complement, sequence_statistics, transcribe, validate_sequence

SEQUENCE_SCHEMA_ID = "molecularis.sequence-record.v1"
SEQUENCE_REFERENCE_SCHEMA_ID = "molecularis.sequence-artifact-reference.v1"
SEQUENCE_REPORT_SCHEMA_ID = "molecularis.sequence-operation-report.v1"
SEQUENCE_MEDIA_TYPE = "application/vnd.molecularis.sequence+json"
SEQUENCE_RULEBOOK_ID = "sequence-core-v1"
_ALPHABETS = {"DNA": DNA, "RNA": RNA, "protein": PROTEIN}
_OPERATIONS = {
    "validate": "sequence.validate.v1",
    "statistics": "sequence.analyze.v1",
    "reverse_complement": "sequence.reverse-complement.v1",
    "transcribe": "sequence.transcribe.v1",
    "translate": "sequence.translate.v1",
}


@dataclass(frozen=True, slots=True)
class SequenceDocument:
    """Immutable, canonical DNA/RNA/protein sequence record."""
    identifier: str
    sequence: str
    sequence_type: str = "DNA"
    description: str = ""

    def __post_init__(self) -> None:
        for name, value in (("identifier", self.identifier), ("description", self.description)):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be text")
        if not self.identifier.strip() or len(self.identifier) > 256:
            raise ValueError("identifier must contain 1..256 characters")
        if any(ord(char) < 32 for char in self.identifier + self.description):
            raise ValueError("sequence metadata must not contain control characters")
        if not isinstance(self.sequence, str):
            raise TypeError("sequence must be text")
        if self.sequence_type not in _ALPHABETS:
            raise ValueError("sequence_type must be DNA, RNA or protein")
        normalized = "".join(self.sequence.split()).upper()
        if not normalized:
            raise ValueError("sequence must not be empty")
        validate_sequence(normalized, _ALPHABETS[self.sequence_type])
        object.__setattr__(self, "sequence", normalized)

    def to_dict(self) -> dict[str, Any]:
        return {"schema": SEQUENCE_SCHEMA_ID, "identifier": self.identifier,
                "description": self.description, "sequence_type": self.sequence_type,
                "sequence": self.sequence}

    def to_json(self) -> bytes:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False,
                          allow_nan=False, separators=(",", ":")).encode("utf-8")

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.to_json()).hexdigest()

    @classmethod
    def from_json(cls, payload: bytes | str) -> "SequenceDocument":
        def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key: {key}")
                result[key] = value
            return result
        try:
            raw = payload.decode("utf-8") if isinstance(payload, bytes) else payload
            value = json.loads(raw, object_pairs_hook=unique_object,
                               parse_constant=lambda item: (_ for _ in ()).throw(ValueError(item)))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid sequence JSON: {exc}") from exc
        expected = {"schema", "identifier", "description", "sequence_type", "sequence"}
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("sequence document fields do not match v1 contract")
        if value["schema"] != SEQUENCE_SCHEMA_ID:
            raise ValueError("unsupported sequence schema")
        return cls(identifier=value["identifier"], description=value["description"],
                   sequence_type=value["sequence_type"], sequence=value["sequence"])


def ingest_sequence(platform: MolecularisPlatform, sequence: SequenceDocument, *,
                    parents: tuple[str, ...] = (), budget: Budget | None = None) -> Artifact:
    if not isinstance(sequence, SequenceDocument):
        raise TypeError("sequence must be a validated SequenceDocument")
    return platform.ingest(
        sequence.to_json(), media_type=SEQUENCE_MEDIA_TYPE, schema_id=SEQUENCE_SCHEMA_ID,
        metadata={"identifier": sequence.identifier, "sequence_type": sequence.sequence_type,
                  "length": len(sequence.sequence), "sequence_sha256": sequence.sha256},
        parents=parents, budget=budget)


def load_sequence(platform: MolecularisPlatform, artifact_id: str, *,
                  budget: Budget | None = None) -> SequenceDocument:
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.media_type != SEQUENCE_MEDIA_TYPE or artifact.schema_id != SEQUENCE_SCHEMA_ID:
        raise ValidationError("artifact is not a Sequence v1 document")
    if artifact.size_bytes > budget.max_bytes:
        raise ResourceLimitError("sequence artifact exceeds byte budget")
    sequence = SequenceDocument.from_json(b"".join(platform.store.read(artifact_id, budget=budget)))
    expected = {"identifier": sequence.identifier, "sequence_type": sequence.sequence_type,
                "length": len(sequence.sequence), "sequence_sha256": sequence.sha256}
    if sequence.sha256 != artifact.digest or any(
        artifact.metadata.get(key) != value for key, value in expected.items()
    ):
        raise ValidationError("sequence content or metadata failed integrity verification")
    return sequence


def _execute_operation(operation: str, sequence: SequenceDocument,
                       parameters: dict[str, Any]) -> dict[str, Any]:
    if operation == "validate":
        return {"valid": True, "sequence_type": sequence.sequence_type,
                "length": len(sequence.sequence)}
    if operation == "statistics":
        if sequence.sequence_type == "protein":
            counts: dict[str, int] = {}
            for residue in sequence.sequence:
                counts[residue] = counts.get(residue, 0) + 1
            return {"length": len(sequence.sequence), "residue_counts": dict(sorted(counts.items()))}
        return sequence_statistics(sequence.sequence)
    if operation == "reverse_complement":
        if sequence.sequence_type != "DNA":
            raise ValidationError("reverse complement currently requires DNA")
        return {"sequence": reverse_complement(sequence.sequence), "sequence_type": "DNA"}
    if operation == "transcribe":
        if sequence.sequence_type != "DNA":
            raise ValidationError("transcription requires DNA")
        return {"sequence": transcribe(sequence.sequence), "sequence_type": "RNA"}
    if operation == "translate":
        if sequence.sequence_type not in {"DNA", "RNA"}:
            raise ValidationError("translation requires DNA or RNA")
        return translate_coding_sequence(
            sequence.sequence, table_id=parameters.get("table_id", 1),
            frame=parameters.get("frame", 0), cds=parameters.get("cds", False),
            trim_partial_codon=parameters.get("trim_partial_codon", False))
    raise ValidationError(f"unsupported sequence operation: {operation}")


def register_sequence_service(platform: MolecularisPlatform) -> None:
    descriptions = {
        "validate": "Validate a stored DNA, RNA or protein sequence artifact.",
        "statistics": "Calculate deterministic sequence composition statistics.",
        "reverse_complement": "Generate the IUPAC DNA reverse complement.",
        "transcribe": "Transcribe DNA to RNA.",
        "translate": "Translate DNA/RNA with an explicit NCBI genetic-code table."}
    for operation, capability_id in _OPERATIONS.items():
        platform.register(Capability(
            id=capability_id, version="1.0.0", service="sequence", operation=operation,
            input_schema=SEQUENCE_REFERENCE_SCHEMA_ID, output_schema=SEQUENCE_REPORT_SCHEMA_ID,
            deterministic=True, description=descriptions[operation]))
        def handler(inputs: dict[str, Any], parameters: dict[str, Any],
                    context: ExecutionContext, selected: str = operation) -> dict[str, Any]:
            if len(inputs) != 1:
                raise ValidationError("sequence operation requires exactly one artifact ID")
            artifact_id = next(iter(inputs.values()))
            if not isinstance(artifact_id, str):
                raise ValidationError("sequence artifact ID must be text")
            sequence = load_sequence(platform, artifact_id, budget=context.budget)
            return {"schema": SEQUENCE_REPORT_SCHEMA_ID, "operation": selected,
                    "sequence_id": sequence.identifier, "sequence_sha256": sequence.sha256,
                    "result": _execute_operation(selected, sequence, parameters),
                    "rulebook": SEQUENCE_RULEBOOK_ID,
                    "rules_checked": ["SEQ-001", "SEQ-002", "SEQ-003", "SEQ-004", "SEQ-005"],
                    "limitations": [
                        "Sequence validity does not establish biological function or provenance.",
                        "Translation does not infer organism, gene boundaries, strand or reading frame."]}
        platform.bind(capability_id, handler)


def sequence_rulebook(operation: str, artifact_key: str = "sequence_artifact_id", *,
                      parameters: dict[str, Any] | None = None) -> Rulebook:
    if operation not in _OPERATIONS:
        raise ValueError(f"unsupported sequence operation: {operation}")
    if not isinstance(artifact_key, str) or not artifact_key.strip():
        raise ValueError("artifact_key must be non-empty text")
    return Rulebook(id=SEQUENCE_RULEBOOK_ID, version="1.0.0", operations=(Operation(
        id=f"{operation}-sequence", capability_id=_OPERATIONS[operation],
        inputs=(artifact_key,), output="sequence_result", parameters=dict(parameters or {})),))
