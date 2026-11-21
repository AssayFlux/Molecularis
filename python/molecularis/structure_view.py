"""Deterministic, bounded structure payload preparation for offline viewers.

This module is a data boundary only. It does not render structures, infer chemistry,
or assign quality/confidence labels.
"""
from __future__ import annotations

import hashlib
import json
from math import isfinite
from typing import Any, Iterable

from .structure import Atom

PAYLOAD_SCHEMA = "kinetics.structure-view.v1"
SUPPORTED_SOURCE_FORMATS = frozenset({"pdb", "mmcif"})
DEFAULT_MAX_PAYLOAD_BYTES = 32 * 1024 * 1024


def _validate_payload_byte_limit(max_payload_bytes: int) -> None:
    if (
        isinstance(max_payload_bytes, bool)
        or not isinstance(max_payload_bytes, int)
        or max_payload_bytes < 1
    ):
        raise ValueError("max_payload_bytes must be a positive integer")


def prepare_viewer_payload(
    atoms: Iterable[Atom],
    *,
    source_format: str,
    max_atoms: int = 200_000,
    max_payload_bytes: int = DEFAULT_MAX_PAYLOAD_BYTES,
) -> dict[str, Any]:
    """Build a deterministic atom payload within atom-count and serialized-byte limits."""
    if not isinstance(source_format, str):
        raise ValueError("source_format must be text")
    normalized_format = source_format.lower().strip()
    if normalized_format not in SUPPORTED_SOURCE_FORMATS:
        raise ValueError("source_format must be 'pdb' or 'mmcif'")
    if isinstance(max_atoms, bool) or not isinstance(max_atoms, int) or max_atoms < 1:
        raise ValueError("max_atoms must be a positive integer")
    _validate_payload_byte_limit(max_payload_bytes)

    records: list[dict[str, Any]] = []
    seen_serials: set[int] = set()
    for atom in atoms:
        if len(records) >= max_atoms:
            raise ValueError(f"Structure exceeds configured atom limit ({max_atoms})")
        if atom.serial in seen_serials:
            raise ValueError(f"Duplicate atom serial: {atom.serial}")
        seen_serials.add(atom.serial)
        if not all(isfinite(value) for value in (atom.x, atom.y, atom.z)):
            raise ValueError(f"Atom {atom.serial} has non-finite coordinates")
        if atom.serial < 0 or atom.residue_number < 0:
            raise ValueError(f"Atom {atom.serial} has a negative identifier")
        fields = (atom.name, atom.residue, atom.chain, atom.element)
        if any(not isinstance(value, str) for value in fields):
            raise ValueError(f"Atom {atom.serial} contains a non-text annotation")
        if len(atom.name) > 8 or len(atom.residue) > 8 or len(atom.chain) > 8:
            raise ValueError(f"Atom {atom.serial} contains an oversized annotation")
        element = atom.element.strip().upper()
        if len(element) > 3:
            raise ValueError(f"Atom {atom.serial} has an invalid element label")
        records.append({
            "serial": atom.serial,
            "name": atom.name.strip(),
            "residue": atom.residue.strip(),
            "chain": atom.chain.strip(),
            "residue_number": atom.residue_number,
            "element": element,
            "xyz": [atom.x, atom.y, atom.z],
        })

    if not records:
        raise ValueError("Cannot prepare an empty structure")
    payload = {
        "schema": PAYLOAD_SCHEMA,
        "source_format": normalized_format,
        "coordinate_unit": "angstrom",
        "atom_count": len(records),
        "atoms": records,
        "limitations": [
            "Coordinates and annotations only; no inferred bonds or protonation.",
            "No secondary-structure, quality, confidence, or biological interpretation.",
            "Viewer rendering and WebView security are separate validated components.",
        ],
    }
    validate_viewer_payload(payload, max_payload_bytes=max_payload_bytes)
    return payload


def validate_viewer_payload(
    payload: dict[str, Any], *,
    max_payload_bytes: int = DEFAULT_MAX_PAYLOAD_BYTES,
) -> None:
    """Validate schema, atom invariants and the serialized WebView handoff byte ceiling."""
    _validate_payload_byte_limit(max_payload_bytes)
    if not isinstance(payload, dict):
        raise ValueError("Structure viewer payload must be a mapping")
    if payload.get("schema") != PAYLOAD_SCHEMA:
        raise ValueError("Unsupported structure viewer payload schema")
    required = {
        "schema", "source_format", "coordinate_unit", "atom_count", "atoms", "limitations",
    }
    if set(payload) != required:
        raise ValueError("Structure viewer payload has missing or unsupported fields")
    if (
        not isinstance(payload["source_format"], str)
        or payload["source_format"] not in SUPPORTED_SOURCE_FORMATS
    ):
        raise ValueError("Structure viewer payload has unsupported source_format")
    if payload["coordinate_unit"] != "angstrom":
        raise ValueError("Structure viewer payload coordinate_unit must be angstrom")
    atom_count = payload["atom_count"]
    atoms = payload["atoms"]
    if (
        isinstance(atom_count, bool) or not isinstance(atom_count, int)
        or atom_count < 1 or atom_count > 200_000
    ):
        raise ValueError("Structure viewer payload atom_count is outside the supported range")
    if not isinstance(atoms, list) or len(atoms) != atom_count:
        raise ValueError("Structure viewer payload atom_count does not match atoms")
    if not isinstance(payload["limitations"], list) or not payload["limitations"] or any(
        not isinstance(item, str) or not item.strip() for item in payload["limitations"]
    ):
        raise ValueError("Structure viewer payload limitations must be non-empty text entries")

    seen_serials: set[int] = set()
    atom_fields = {
        "serial", "name", "residue", "chain", "residue_number", "element", "xyz",
    }
    for index, atom in enumerate(atoms):
        if not isinstance(atom, dict) or set(atom) != atom_fields:
            raise ValueError(f"Structure viewer atom {index} has missing or unsupported fields")
        serial, residue_number = atom["serial"], atom["residue_number"]
        if (
            isinstance(serial, bool) or not isinstance(serial, int) or serial < 0
            or serial in seen_serials
        ):
            raise ValueError(f"Structure viewer atom {index} has an invalid or duplicate serial")
        seen_serials.add(serial)
        if (
            isinstance(residue_number, bool) or not isinstance(residue_number, int)
            or residue_number < 0
        ):
            raise ValueError(f"Structure viewer atom {index} has an invalid residue number")
        for field in ("name", "residue", "chain"):
            value = atom[field]
            if not isinstance(value, str) or len(value) > 8:
                raise ValueError(f"Structure viewer atom {index} has an invalid {field}")
        element = atom["element"]
        if (
            not isinstance(element, str) or not element.strip()
            or element != element.strip().upper() or len(element) > 3
        ):
            raise ValueError(f"Structure viewer atom {index} has an invalid element")
        xyz = atom["xyz"]
        if not isinstance(xyz, list) or len(xyz) != 3 or any(
            isinstance(value, bool) or not isinstance(value, (int, float))
            or not isfinite(value) for value in xyz
        ):
            raise ValueError(f"Structure viewer atom {index} has invalid coordinates")

    encoded_size = len(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    )
    if encoded_size > max_payload_bytes:
        raise ValueError("Structure viewer payload exceeds max_payload_bytes")


def serialize_viewer_payload(
    payload: dict[str, Any], *,
    max_payload_bytes: int = DEFAULT_MAX_PAYLOAD_BYTES,
) -> str:
    """Serialize a fully validated payload deterministically without NaN/Infinity."""
    validate_viewer_payload(payload, max_payload_bytes=max_payload_bytes)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def build_preparation_record(
    source_bytes: bytes,
    payload: dict[str, Any],
    *,
    parser_version: str,
    dropped_record_count: int = 0,
) -> dict[str, Any]:
    """Create a deterministic provenance record without retaining source content."""
    if not isinstance(source_bytes, bytes) or not source_bytes:
        raise ValueError("source_bytes must be non-empty bytes")
    if not isinstance(parser_version, str) or not parser_version.strip():
        raise ValueError("parser_version must be non-empty text")
    if (isinstance(dropped_record_count, bool)
            or not isinstance(dropped_record_count, int) or dropped_record_count < 0):
        raise ValueError("dropped_record_count must be a non-negative integer")
    payload_json = serialize_viewer_payload(payload)
    return {
        "record_schema": "kinetics.structure-preparation.v1",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_bytes": len(source_bytes),
        "source_format": payload["source_format"],
        "parser_version": parser_version.strip(),
        "payload_sha256": hashlib.sha256(payload_json.encode("utf-8")).hexdigest(),
        "payload_schema": payload["schema"],
        "atom_count": payload["atom_count"],
        "dropped_record_count": dropped_record_count,
        "coordinate_unit": payload["coordinate_unit"],
        "limitations": list(payload["limitations"]),
    }



def build_structure_session_export(
    source_bytes: bytes,
    payload: dict[str, Any],
    *,
    parser_version: str,
    max_export_bytes: int = 64 * 1024 * 1024,
) -> str:
    """Build a deterministic offline JSON session export with provenance.

    This exports prepared coordinate data and its content-addressed preparation
    record. It does not render PNG/SVG or imply a viewer is installed.
    """
    if (
        isinstance(max_export_bytes, bool)
        or not isinstance(max_export_bytes, int)
        or max_export_bytes < 1
    ):
        raise ValueError("max_export_bytes must be a positive integer")
    payload_json = serialize_viewer_payload(payload)
    preparation = build_preparation_record(
        source_bytes, payload, parser_version=parser_version,
    )
    bundle = {
        "schema": "kinetics.structure-session.v1",
        "render_state": "not_rendered",
        "preparation": preparation,
        "payload": json.loads(payload_json),
        "export_limitations": [
            "This session contains prepared coordinates and annotations only.",
            "No PNG/SVG image or interactive viewer state is included.",
            "No bonds, protonation, secondary structure, quality grade or biological interpretation is inferred.",
            "Viewer version is absent because no renderer has been approved and integrated.",
        ],
    }
    encoded = json.dumps(bundle, sort_keys=True, separators=(",", ":"), allow_nan=False)
    if len(encoded.encode("utf-8")) > max_export_bytes:
        raise ValueError("Structure session export exceeds max_export_bytes")
    return encoded

def prepare_structure_viewer_source(
    source_text: str,
    *,
    source_format: str,
    max_source_bytes: int = 16 * 1024 * 1024,
    max_atoms: int = 100_000,
) -> dict[str, Any]:
    """Parse bounded caller-supplied PDB/mmCIF text and return payload plus provenance."""
    from .structure import parse_mmcif, parse_pdb

    if not isinstance(source_text, str) or not source_text:
        raise ValueError("Structure source must be non-empty text")
    if (
        isinstance(max_source_bytes, bool)
        or not isinstance(max_source_bytes, int)
        or max_source_bytes < 1
    ):
        raise ValueError("max_source_bytes must be a positive integer")
    source_bytes = source_text.encode("utf-8")
    if len(source_bytes) > max_source_bytes:
        raise ValueError("Structure source exceeds max_source_bytes")
    normalized_format = source_format.lower().strip() if isinstance(source_format, str) else ""
    if normalized_format == "pdb":
        atoms = parse_pdb(source_text)
    elif normalized_format == "mmcif":
        atoms = parse_mmcif(source_text)
    else:
        raise ValueError("source_format must be 'pdb' or 'mmcif'")
    payload = prepare_viewer_payload(
        atoms, source_format=normalized_format, max_atoms=max_atoms,
    )
    preparation = build_preparation_record(
        source_bytes, payload, parser_version="kinetics-structure-parser-v1",
    )
    return {"payload": payload, "preparation": preparation}
