"""Verified, bounded ingestion of local FASTA reference packs.

The manifest hash is checked against the exact file bytes before records are exposed.
No network access, archive extraction, or automatic license acceptance is performed.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from kinetics.sequence import SequenceRecord, iter_fasta_records, validate_sequence
from kinetics.sequence_reference import (
    ReferencePack,
    SequenceType,
    _alphabet,
    exact_reference_search,
    local_alignment_reference_search,
)


@dataclass(frozen=True)
class LoadedReferencePack:
    metadata: ReferencePack
    sequence_type: SequenceType
    records: tuple[SequenceRecord, ...]


DEFAULT_MAX_PACK_BYTES = 250_000_000
DEFAULT_MAX_MANIFEST_BYTES = 65_536
DEFAULT_MAX_RECORDS = 100_000
DEFAULT_MAX_TOTAL_RESIDUES = 50_000_000


def _open_regular_file(path: Path, *, label: str) -> Any:
    """Open a regular file without following a final-component symlink where supported."""
    if path.is_symlink():
        raise ValueError(f"{label} must not be a symbolic link")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise ValueError(f"Cannot open {label}: {exc}") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"{label} must be a regular file")
        return os.fdopen(descriptor, "rb")
    except Exception:
        os.close(descriptor)
        raise


def _read_manifest(path: Path, *, max_bytes: int) -> dict[str, Any]:
    try:
        with _open_regular_file(path, label="Reference manifest") as handle:
            raw = handle.read(max_bytes + 1)
        if len(raw) > max_bytes:
            raise ValueError("Reference manifest exceeds max_manifest_bytes")
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid reference manifest: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Reference manifest root must be a JSON object")
    return value


def _validate_manifest(value: dict[str, Any]) -> tuple[ReferencePack, SequenceType]:
    required = {
        "schema_version", "name", "version", "license", "source",
        "sequence_type", "format", "content_sha256",
    }
    if set(value) != required:
        missing = sorted(required - set(value))
        extra = sorted(set(value) - required)
        raise ValueError(f"Manifest keys mismatch; missing={missing}, extra={extra}")
    if (
        type(value["schema_version"]) is not int
        or value["schema_version"] != 1
        or value["format"] != "fasta"
    ):
        raise ValueError("Only schema_version 1 and FASTA reference packs are supported")
    raw_sequence_type = value["sequence_type"]
    if raw_sequence_type not in ("DNA", "RNA", "protein"):
        raise ValueError("sequence_type must be DNA, RNA, or protein")
    sequence_type = cast(SequenceType, raw_sequence_type)
    pack = ReferencePack(
        name=value["name"],
        version=value["version"],
        license=value["license"],
        source=value["source"],
        content_sha256=value["content_sha256"],
    )
    pack.validate()
    return pack, sequence_type


def _sha256_stream(
    handle: Any, *, max_bytes: int, chunk_bytes: int = 1_048_576,
) -> str:
    digest = hashlib.sha256()
    total = 0
    while True:
        chunk = handle.read(min(chunk_bytes, max_bytes - total + 1))
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise ValueError("Reference FASTA exceeds max_pack_bytes")
        digest.update(chunk)
    return digest.hexdigest()


def load_local_fasta_reference_pack(
    fasta_path: str | Path,
    manifest_path: str | Path,
    *,
    max_pack_bytes: int = DEFAULT_MAX_PACK_BYTES,
    max_manifest_bytes: int = DEFAULT_MAX_MANIFEST_BYTES,
    max_records: int = DEFAULT_MAX_RECORDS,
    max_total_residues: int = DEFAULT_MAX_TOTAL_RESIDUES,
) -> LoadedReferencePack:
    """Load a local FASTA pack only after verifying manifest provenance and bytes.

    The same open file descriptor is hashed, parsed, and hashed again to detect
    content changes during ingestion. Limits are enforced before/while parsing.
    """
    limits = {
        "max_pack_bytes": max_pack_bytes,
        "max_manifest_bytes": max_manifest_bytes,
        "max_records": max_records,
        "max_total_residues": max_total_residues,
    }
    for name, value in limits.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    manifest = _read_manifest(Path(manifest_path), max_bytes=max_manifest_bytes)
    pack, sequence_type = _validate_manifest(manifest)
    fasta = Path(fasta_path)
    try:
        with _open_regular_file(fasta, label="Reference FASTA") as handle:
            before = os.fstat(handle.fileno())
            if before.st_size > max_pack_bytes:
                raise ValueError("Reference FASTA exceeds max_pack_bytes")
            actual_hash = _sha256_stream(handle, max_bytes=max_pack_bytes)
            if actual_hash != pack.content_sha256:
                raise ValueError("Reference FASTA SHA-256 does not match its manifest")
            handle.seek(0)
            text_handle = io.TextIOWrapper(handle, encoding="ascii", errors="strict")
            records: list[SequenceRecord] = []
            identifiers: set[str] = set()
            total_residues = 0
            try:
                for record in iter_fasta_records(text_handle):
                    if len(records) >= max_records:
                        raise ValueError("Reference FASTA exceeds max_records")
                    if record.identifier in identifiers:
                        raise ValueError("Reference FASTA identifiers must be unique")
                    identifiers.add(record.identifier)
                    validate_sequence(record.sequence, _alphabet(sequence_type))
                    total_residues += len(record.sequence)
                    if total_residues > max_total_residues:
                        raise ValueError("Reference FASTA exceeds max_total_residues")
                    records.append(record)
            except UnicodeDecodeError as exc:
                raise ValueError("Reference FASTA must contain ASCII sequence text") from exc
            finally:
                text_handle.detach()
            after = os.fstat(handle.fileno())
            handle.seek(0)
            final_hash = _sha256_stream(handle, max_bytes=max_pack_bytes)
            if final_hash != actual_hash or (
                before.st_size != after.st_size
                or before.st_mtime_ns != after.st_mtime_ns
            ):
                raise ValueError("Reference FASTA changed during ingestion")
    except OSError as exc:
        raise ValueError(f"Cannot read reference FASTA: {exc}") from exc
    if not records:
        raise ValueError("Reference FASTA contains no records")
    return LoadedReferencePack(pack, sequence_type, tuple(records))


def search_local_fasta_reference(
    query: str,
    fasta_path: str | Path,
    manifest_path: str | Path,
    *,
    max_pack_bytes: int = DEFAULT_MAX_PACK_BYTES,
    max_manifest_bytes: int = DEFAULT_MAX_MANIFEST_BYTES,
    max_records: int = DEFAULT_MAX_RECORDS,
    max_total_residues: int = DEFAULT_MAX_TOTAL_RESIDUES,
) -> dict[str, object]:
    """Verify a local FASTA pack, then run exact-only search with its declared alphabet."""
    loaded = load_local_fasta_reference_pack(
        fasta_path,
        manifest_path,
        max_pack_bytes=max_pack_bytes,
        max_manifest_bytes=max_manifest_bytes,
        max_records=max_records,
        max_total_residues=max_total_residues,
    )
    return exact_reference_search(
        query,
        loaded.records,
        sequence_type=loaded.sequence_type,
        reference_pack=loaded.metadata,
        max_records=max_records,
        max_total_residues=max_total_residues,
    )


def search_local_fasta_alignment(
    query: str,
    fasta_path: str | Path,
    manifest_path: str | Path,
    *,
    max_pack_bytes: int = DEFAULT_MAX_PACK_BYTES,
    max_manifest_bytes: int = DEFAULT_MAX_MANIFEST_BYTES,
    max_records: int = 10_000,
    max_total_residues: int = 5_000_000,
    max_query_residues: int = 20_000,
    max_alignment_cells: int = 2_000_000,
    max_total_alignment_cells: int = 20_000_000,
    max_hits: int = 100,
) -> dict[str, object]:
    """Verify a local FASTA pack before bounded Smith–Waterman similarity triage."""
    loaded = load_local_fasta_reference_pack(
        fasta_path,
        manifest_path,
        max_pack_bytes=max_pack_bytes,
        max_manifest_bytes=max_manifest_bytes,
        max_records=max_records,
        max_total_residues=max_total_residues,
    )
    return local_alignment_reference_search(
        query,
        loaded.records,
        sequence_type=loaded.sequence_type,
        reference_pack=loaded.metadata,
        max_records=max_records,
        max_total_residues=max_total_residues,
        max_query_residues=max_query_residues,
        max_alignment_cells=max_alignment_cells,
        max_total_alignment_cells=max_total_alignment_cells,
        max_hits=max_hits,
    )
