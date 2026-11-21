"""Chemistry service D: immutable molecular graph artifacts and bounded capabilities."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from typing import Any
from .chemistry import graph_descriptors, path_fingerprint, substructure_match, tanimoto
from .platform import Budget, Capability, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

CHEMISTRY_SCHEMA_ID = "molecularis.chemistry-record.v1"
CHEMISTRY_REFERENCE_SCHEMA_ID = "molecularis.chemistry-artifact-reference.v1"
CHEMISTRY_REPORT_SCHEMA_ID = "molecularis.chemistry-operation-report.v1"
CHEMISTRY_MEDIA_TYPE = "application/vnd.molecularis.chemistry+json"
CHEMISTRY_RULEBOOK_ID = "chemistry-core-v1"
OPS = {
    "validate": "chemistry.validate.v1",
    "descriptors": "chemistry.descriptors.v1",
    "fingerprint": "chemistry.fingerprint.v1",
    "substructure": "chemistry.substructure.v1",
    "similarity": "chemistry.similarity.v1",
}

@dataclass(frozen=True, slots=True)
class ChemistryDocument:
    """Canonical explicit-atom molecular graph; no inferred chemistry is implied."""
    identifier: str
    atoms: tuple[dict[str, Any], ...]
    bonds: tuple[tuple[int, int, int], ...]
    source_format: str = "native"
    source_sha256: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.identifier, str) or not self.identifier.strip() or len(self.identifier) > 256:
            raise ValueError("identifier must be bounded non-empty text")
        if self.source_format not in {"native", "sdf-v2000", "sdf-v3000"}:
            raise ValueError("unsupported source format")
        if not isinstance(self.atoms, tuple) or not self.atoms or len(self.atoms) > 100000:
            raise ValueError("atoms must be a non-empty tuple of at most 100000 records")
        if not isinstance(self.bonds, tuple) or len(self.bonds) > 200000:
            raise ValueError("bonds must be a tuple of at most 200000 records")
        for atom in self.atoms:
            if not isinstance(atom, dict) or atom.get("element") not in {
                "H", "C", "N", "O", "F", "P", "S", "CL", "BR", "I", "B", "SI"
            }:
                raise ValueError("atom has an unsupported element")
            if set(atom) != {"element", "x", "y", "z"}:
                raise ValueError("atom fields must be element, x, y and z")
            if any(isinstance(atom[k], bool) or not isinstance(atom[k], (int, float)) for k in ("x", "y", "z")):
                raise ValueError("coordinates must be finite numeric values")
            if any(not __import__("math").isfinite(atom[k]) for k in ("x", "y", "z")):
                raise ValueError("coordinates must be finite")
        seen: set[tuple[int, int]] = set()
        for bond in self.bonds:
            if (not isinstance(bond, tuple) or len(bond) != 3
                or any(isinstance(v, bool) or not isinstance(v, int) for v in bond)):
                raise ValueError("bond must contain integer atom indices and order")
            a, b, order = bond
            if a < 0 or b < 0 or a >= len(self.atoms) or b >= len(self.atoms) or a == b or order not in (1, 2, 3, 4):
                raise ValueError("bond contains invalid indices or order")
            pair = tuple(sorted((a, b)))
            if pair in seen:
                raise ValueError("duplicate atom-pair bond")
            seen.add(pair)
        if self.source_sha256 and (len(self.source_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.source_sha256)):
            raise ValueError("source_sha256 must be a lowercase SHA-256 digest")

    @classmethod
    def from_sdf(cls, identifier: str, text: str) -> "ChemistryDocument":
        try:
            raw = text.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise ValueError("SDF contains invalid Unicode") from exc
        if not raw or len(raw) > 16 * 1024 * 1024 or b"\x00" in raw:
            raise ValueError("SDF must be non-empty, NUL-free and at most 16 MiB")
        records = list(__import__("molecularis.chemistry", fromlist=["iter_sdf_records"]).iter_sdf_records(text))
        if len(records) != 1:
            raise ValueError("expected exactly one SDF molecule record")
        record = records[0]
        return cls(identifier, tuple(dict(a) for a in record["atoms"]), tuple(tuple(b) for b in record["bonds"]),
                   "sdf-v3000" if record.get("format") == "V3000" else "sdf-v2000", hashlib.sha256(raw).hexdigest())

    def to_dict(self) -> dict[str, Any]:
        return {"schema": CHEMISTRY_SCHEMA_ID, "identifier": self.identifier, "source_format": self.source_format,
                "source_sha256": self.source_sha256, "coordinate_unit": "angstrom",
                "atoms": [dict(a) for a in self.atoms], "bonds": [list(b) for b in self.bonds]}

    def to_json(self) -> bytes:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False, allow_nan=False,
                          separators=(",", ":")).encode("utf-8")

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.to_json()).hexdigest()

    def graph(self) -> dict[str, Any]:
        return {"atoms": [dict(a) for a in self.atoms], "bonds": list(self.bonds)}

    @classmethod
    def from_json(cls, payload: bytes | str) -> "ChemistryDocument":
        def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate JSON key: " + key)
                result[key] = value
            return result
        try:
            raw = payload.decode("utf-8") if isinstance(payload, bytes) else payload
            value = json.loads(raw, object_pairs_hook=unique,
                               parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("invalid Chemistry JSON: " + str(exc)) from exc
        expected = {"schema", "identifier", "source_format", "source_sha256", "coordinate_unit", "atoms", "bonds"}
        if not isinstance(value, dict) or set(value) != expected or value["schema"] != CHEMISTRY_SCHEMA_ID:
            raise ValueError("Chemistry JSON does not match exact v1 contract")
        if value["coordinate_unit"] != "angstrom" or not isinstance(value["atoms"], list) or not isinstance(value["bonds"], list):
            raise ValueError("invalid Chemistry coordinate unit or graph arrays")
        return cls(value["identifier"], tuple(value["atoms"]), tuple(tuple(b) for b in value["bonds"]),
                   value["source_format"], value["source_sha256"])


def ingest_chemistry(platform, molecule: ChemistryDocument, *, parents=(), budget=None):
    if not isinstance(molecule, ChemistryDocument):
        raise TypeError("molecule must be a ChemistryDocument")
    return platform.ingest(molecule.to_json(), media_type=CHEMISTRY_MEDIA_TYPE, schema_id=CHEMISTRY_SCHEMA_ID,
        metadata={"identifier": molecule.identifier, "chemistry_sha256": molecule.sha256,
                  "source_sha256": molecule.source_sha256, "atom_count": len(molecule.atoms),
                  "bond_count": len(molecule.bonds), "source_format": molecule.source_format,
                  "coordinate_unit": "angstrom"}, parents=parents, budget=budget)


def load_chemistry(platform, artifact_id: str, *, budget: Budget | None = None) -> ChemistryDocument:
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.media_type != CHEMISTRY_MEDIA_TYPE or artifact.schema_id != CHEMISTRY_SCHEMA_ID:
        raise ValidationError("artifact is not a Chemistry v1 document")
    if artifact.size_bytes > budget.max_bytes:
        raise ResourceLimitError("Chemistry artifact exceeds byte budget")
    doc = ChemistryDocument.from_json(b"".join(platform.store.read(artifact_id, budget=budget)))
    expected = {"identifier": doc.identifier, "chemistry_sha256": doc.sha256,
                "source_sha256": doc.source_sha256, "atom_count": len(doc.atoms),
                "bond_count": len(doc.bonds), "source_format": doc.source_format, "coordinate_unit": "angstrom"}
    if doc.sha256 != artifact.digest or any(artifact.metadata.get(k) != v for k, v in expected.items()):
        raise ValidationError("Chemistry content or metadata failed integrity verification")
    return doc


def register_chemistry_service(platform) -> None:
    descriptions = {
        "validate": "Verify canonical molecular graph artifact integrity and structural invariants.",
        "descriptors": "Calculate bounded native graph descriptors from explicit atoms and bonds.",
        "fingerprint": "Generate a deterministic bounded path fingerprint for graph comparison.",
        "substructure": "Perform exact element and bond-order subgraph matching.",
        "similarity": "Calculate Tanimoto similarity of native path fingerprints.",
    }
    for operation, capid in OPS.items():
        platform.register(Capability(id=capid, version="1.0.0", service="chemistry", operation=operation,
            input_schema=CHEMISTRY_REFERENCE_SCHEMA_ID, output_schema=CHEMISTRY_REPORT_SCHEMA_ID,
            deterministic=True, description=descriptions[operation]))
        def handler(inputs, parameters, context, selected=operation):
            required = 2 if selected in {"substructure", "similarity"} else 1
            if len(inputs) != required or any(not isinstance(v, str) for v in inputs.values()):
                raise ValidationError("Chemistry operation received invalid artifact references")
            ids = list(inputs.values())
            first = load_chemistry(platform, ids[0], budget=context.budget)
            if selected == "validate":
                result = {"valid": True, "atom_count": len(first.atoms), "bond_count": len(first.bonds)}
            elif selected == "descriptors":
                result = graph_descriptors(first.graph())
            elif selected == "fingerprint":
                result = {"algorithm": "Molecularis path-v1", "features": sorted(path_fingerprint(
                    first.graph(), max_path=parameters.get("max_path", 3),
                    max_features=parameters.get("max_features", 100000),
                    max_walk_states=parameters.get("max_walk_states", 200000)))}
            else:
                second = load_chemistry(platform, ids[1], budget=context.budget)
                if selected == "substructure":
                    result = {"match": substructure_match(first.graph(), second.graph(),
                        max_search_states=parameters.get("max_search_states", 100000)),
                        "semantics": "exact element and bond-order graph match; no aromaticity or stereochemistry"}
                else:
                    a = path_fingerprint(first.graph(), max_path=parameters.get("max_path", 3))
                    b = path_fingerprint(second.graph(), max_path=parameters.get("max_path", 3))
                    result = {"tanimoto": tanimoto(a, b), "algorithm": "Molecularis path-v1"}
            return {"schema": CHEMISTRY_REPORT_SCHEMA_ID, "operation": selected, "molecule_id": first.identifier,
                "molecule_sha256": first.sha256, "result": result, "rulebook": CHEMISTRY_RULEBOOK_ID,
                "rules_checked": [f"CHM-{i:03d}" for i in range(1, 7)],
                "limitations": ["Native graph operations do not sanitize valence, aromaticity, charge or stereochemistry.",
                    "Implicit hydrogens, protonation, tautomerism and chemical equivalence are not inferred.",
                    "Fingerprints are Molecularis path features, not Morgan/ECFP fingerprints.",
                    "No ADMET, activity, toxicity, docking, safety or clinical inference is provided."]}
        platform.bind(capid, handler)


def chemistry_rulebook(operation: str, artifact_key: str = "chemistry_artifact_id", *,
                       second_artifact_key: str = "query_chemistry_artifact_id", parameters=None) -> Rulebook:
    if operation not in OPS:
        raise ValueError("unsupported Chemistry operation: " + operation)
    if not isinstance(artifact_key, str) or not artifact_key.strip():
        raise ValueError("artifact_key must be non-empty text")
    keys = (artifact_key, second_artifact_key) if operation in {"substructure", "similarity"} else (artifact_key,)
    if len(keys) == 2 and (not isinstance(second_artifact_key, str) or not second_artifact_key.strip()
                           or second_artifact_key == artifact_key):
        raise ValueError("two-molecule operation requires distinct artifact keys")
    return Rulebook(id=CHEMISTRY_RULEBOOK_ID, version="1.0.0",
        operations=(Operation(id=f"{operation}-chemistry", capability_id=OPS[operation], inputs=keys,
                              output="chemistry_result", parameters=dict(parameters or {})),))
