"""Pinned local GFF3 annotation-engine integration for S7.

This is an adapter contract, not a bundled gene caller. A compatible local
executable must write validated GFF3 to the requested output path.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable

from .gff3 import parse_gff3
from .genetic_code import GENETIC_CODES
from .sequence import SequenceRecord


def _hash_file(path: Path, max_bytes: int) -> str:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                raise ValueError("Gene-caller executable exceeds max_executable_bytes")
            digest.update(chunk)
    return digest.hexdigest()


def _limit_output(max_bytes: int) -> Callable[[], None] | None:
    if sys.platform == "win32":
        return None

    def apply() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_FSIZE, (max_bytes, max_bytes))

    return apply


def run_pinned_local_gff3_annotator(
    records: Iterable[SequenceRecord],
    *,
    executable_path: str,
    executable_sha256: str,
    annotator_id: str,
    annotator_version: str,
    mode: str = "prokaryotic",
    translation_table: int = 11,
    timeout_seconds: int = 1800,
    max_contigs: int = 100_000,
    max_total_bases: int = 500_000_000,
    max_executable_bytes: int = 512 * 1024 * 1024,
    max_gff3_bytes: int = 128 * 1024 * 1024,
) -> dict[str, object]:
    """Run a pinned local annotator and strictly validate its GFF3 coordinates."""
    if mode not in {"prokaryotic", "eukaryotic"}:
        raise ValueError("mode must be prokaryotic or eukaryotic")
    for name, value in (
        ("translation_table", translation_table),
        ("timeout_seconds", timeout_seconds),
        ("max_contigs", max_contigs),
        ("max_total_bases", max_total_bases),
        ("max_executable_bytes", max_executable_bytes),
        ("max_gff3_bytes", max_gff3_bytes),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if translation_table not in GENETIC_CODES:
        raise ValueError("translation_table is not a supported NCBI genetic code")
    for text_name, text_value in (
        ("annotator_id", annotator_id),
        ("annotator_version", annotator_version),
    ):
        if not isinstance(text_value, str) or not text_value.strip():
            raise ValueError(f"{text_name} must be non-empty text")
    if (
        not isinstance(executable_sha256, str)
        or len(executable_sha256) != 64
        or any(char not in "0123456789abcdef" for char in executable_sha256)
    ):
        raise ValueError("executable_sha256 must be lowercase SHA-256 hex")
    contigs: dict[str, str] = {}
    total_bases = 0
    for record in records:
        if len(contigs) >= max_contigs:
            raise ValueError("Genome exceeds max_contigs")
        if (
            not isinstance(record.identifier, str)
            or not record.identifier
            or not record.identifier.isascii()
            or any(char.isspace() or ord(char) < 33 or char == ">" for char in record.identifier)
        ):
            raise ValueError("Contig identifiers must be safe non-empty ASCII tokens")
        if record.identifier in contigs:
            raise ValueError("Contig identifiers must be unique")
        sequence = "".join(record.sequence.split()).upper().replace("U", "T")
        if not sequence or any(base not in "ACGTRYSWKMBDHVN" for base in sequence):
            raise ValueError(f"Contig {record.identifier!r} is empty or contains invalid DNA")
        if len(sequence) > max_total_bases - total_bases:
            raise ValueError("Genome exceeds max_total_bases")
        contigs[record.identifier] = sequence
        total_bases += len(sequence)
    if not contigs:
        raise ValueError("Genome contains no contigs")

    executable = Path(executable_path).expanduser().resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("Annotator executable must be an executable regular file")
    if _hash_file(executable, max_executable_bytes) != executable_sha256:
        raise ValueError("Annotator executable SHA-256 does not match approved digest")

    executable_hash = _hash_file(executable, max_executable_bytes)
    if executable_hash != executable_sha256:
        raise ValueError("Annotator executable changed after approval")
    contig_hashes = {
        name: hashlib.sha256(sequence.encode("ascii")).hexdigest()
        for name, sequence in contigs.items()
    }
    fasta = "".join(f">{name}\n{sequence}\n" for name, sequence in contigs.items())
    with tempfile.TemporaryDirectory(prefix="kinetics-s7-") as directory:
        work = Path(directory)
        input_path = work / "genome.fasta"
        output_path = work / "annotation.gff3"
        input_path.write_text(fasta, encoding="ascii")
        try:
            result = subprocess.run(
                [
                    str(executable),
                    "--kinetics-input-fasta", str(input_path),
                    "--kinetics-output-gff3", str(output_path),
                    "--kinetics-mode", mode,
                    "--kinetics-translation-table", str(translation_table),
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=work,
                env={
                    "HOME": str(work),
                    "TMPDIR": str(work),
                    "TEMP": str(work),
                    "TMP": str(work),
                    "PATH": os.defpath,
                    "LANG": "C",
                    "LC_ALL": "C",
                },
                timeout=timeout_seconds,
                check=False,
                shell=False,
                preexec_fn=_limit_output(max_gff3_bytes),
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("Local gene annotator exceeded timeout_seconds") from exc
        if result.returncode != 0:
            raise RuntimeError(f"Local gene annotator exited with status {result.returncode}")
        if not output_path.is_file():
            raise RuntimeError("Local gene annotator did not create annotation.gff3")
        if output_path.stat().st_size > max_gff3_bytes:
            raise ValueError("Gene annotation exceeds max_gff3_bytes")
        with output_path.open("r", encoding="utf-8", errors="strict") as stream:
            annotation = parse_gff3(stream)
        annotation_bytes = output_path.read_bytes()
    sequence_ids = annotation.get("sequence_ids")
    features = annotation.get("features")
    if not isinstance(sequence_ids, list) or not isinstance(features, list):
        raise RuntimeError("GFF3 parser returned an invalid annotation structure")
    unknown = set(sequence_ids) - set(contigs)
    if unknown:
        raise ValueError(f"Annotation refers to unknown contigs: {sorted(unknown)[:5]}")
    for feature in features:
        if not isinstance(feature, dict):
            raise RuntimeError("GFF3 parser returned an invalid feature")
        seqid, end = feature.get("seqid"), feature.get("end")
        if (
            not isinstance(seqid, str)
            or isinstance(end, bool)
            or not isinstance(end, int)
            or seqid not in contigs
        ):
            raise RuntimeError("GFF3 parser returned invalid feature coordinates")
        if end > len(contigs[seqid]):
            raise ValueError("GFF3 feature extends beyond supplied contig length")
    return {
        "schema": "kinetics.local-genome-annotation.v1",
        "execution_mode": "local",
        "annotator": {"id": annotator_id, "version": annotator_version,
                      "executable_sha256": executable_hash},
        "mode": mode,
        "translation_table": translation_table,
        "input_contigs": len(contigs),
        "input_bases": total_bases,
        "input_contig_sha256": contig_hashes,
        "annotation_sha256": hashlib.sha256(annotation_bytes).hexdigest(),
        "annotation_bytes": len(annotation_bytes),
        "annotation": annotation,
        "conclusion": "syntax_and_coordinate_validated_gene_caller_output",
        "limitations": [
            "This adapter does not bundle, install or scientifically validate a gene caller.",
            "GFF3 syntax and coordinate checks do not establish gene-calling accuracy.",
            "The caller must independently approve executable, database and model licenses.",
            "The host must enforce OS-level network isolation.",
            "Eukaryotic mode is available only if the supplied annotator implements it.",
            "No expression, function, pathogenicity or organism identity is inferred.",
        ],
    }
