"""Pinned local Prodigal adapter for prokaryotic gene-candidate prediction."""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable

from .gff3 import parse_gff3
from .sequence import SequenceRecord


def _sha256(path: Path, *, max_bytes: int) -> str:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            total += len(chunk)
            if total > max_bytes:
                raise ValueError("Prodigal executable exceeds max_executable_bytes")
            digest.update(chunk)
    return digest.hexdigest()


def _output_limit(max_bytes: int) -> Callable[[], None] | None:
    if sys.platform == "win32":
        return None

    def apply() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_FSIZE, (max_bytes, max_bytes))

    return apply


def run_local_prodigal(
    records: Iterable[SequenceRecord],
    *,
    executable_path: str,
    executable_sha256: str,
    tool_version: str,
    translation_table: int = 11,
    mode: str = "single",
    timeout_seconds: int = 1800,
    max_contigs: int = 100_000,
    max_total_bases: int = 500_000_000,
    max_executable_bytes: int = 512 * 1024 * 1024,
    max_gff3_bytes: int = 128 * 1024 * 1024,
) -> dict[str, object]:
    """Run a pinned Prodigal binary and validate its GFF3 gene-candidate output."""
    if mode not in {"single", "meta"}:
        raise ValueError("Prodigal mode must be single or meta")
    if (
        isinstance(translation_table, bool)
        or not isinstance(translation_table, int)
        or translation_table not in {1, 4, 11}
    ):
        raise ValueError("Prodigal supports only explicitly configured tables 1, 4 or 11")
    if not isinstance(tool_version, str) or not tool_version.strip():
        raise ValueError("tool_version must be non-empty caller-supplied text")
    for name, value in (
        ("timeout_seconds", timeout_seconds),
        ("max_contigs", max_contigs),
        ("max_total_bases", max_total_bases),
        ("max_executable_bytes", max_executable_bytes),
        ("max_gff3_bytes", max_gff3_bytes),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
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
            or record.identifier in contigs
        ):
            raise ValueError("Contig identifiers must be safe, non-empty and unique")
        sequence = "".join(record.sequence.split()).upper().replace("U", "T")
        if not sequence or any(base not in "ACGTRYSWKMBDHVN" for base in sequence):
            raise ValueError(f"Contig {record.identifier!r} contains invalid DNA")
        total_bases += len(sequence)
        if total_bases > max_total_bases:
            raise ValueError("Genome exceeds max_total_bases")
        contigs[record.identifier] = sequence
    if not contigs:
        raise ValueError("Genome contains no contigs")

    executable = Path(executable_path).expanduser().resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("Prodigal executable must be an executable regular file")
    actual_hash = _sha256(executable, max_bytes=max_executable_bytes)
    if actual_hash != executable_sha256:
        raise ValueError("Prodigal executable SHA-256 does not match approved digest")
    contig_hashes = {
        name: hashlib.sha256(sequence.encode("ascii")).hexdigest()
        for name, sequence in contigs.items()
    }
    fasta = "".join(f">{name}\n{sequence}\n" for name, sequence in contigs.items())

    with tempfile.TemporaryDirectory(prefix="kinetics-prodigal-") as directory:
        work = Path(directory)
        input_path = work / "genome.fasta"
        output_path = work / "genes.gff"
        input_path.write_text(fasta, encoding="ascii")
        try:
            result = subprocess.run(
                [
                    str(executable),
                    "-i", str(input_path),
                    "-o", str(output_path),
                    "-f", "gff",
                    "-p", mode,
                    "-g", str(translation_table),
                    "-q",
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
                preexec_fn=_output_limit(max_gff3_bytes),
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("Local Prodigal exceeded timeout_seconds") from exc
        if result.returncode != 0:
            raise RuntimeError(f"Prodigal exited with status {result.returncode}")
        if not output_path.is_file():
            raise RuntimeError("Prodigal did not create GFF output")
        if output_path.stat().st_size > max_gff3_bytes:
            raise ValueError("Prodigal GFF output exceeds max_gff3_bytes")
        with output_path.open("r", encoding="utf-8", errors="strict") as stream:
            annotation = parse_gff3(stream)
        annotation_bytes = output_path.read_bytes()

    sequence_ids = annotation.get("sequence_ids")
    features = annotation.get("features")
    if not isinstance(sequence_ids, list) or not isinstance(features, list):
        raise RuntimeError("GFF3 parser returned an invalid annotation structure")
    unknown = set(sequence_ids) - set(contigs)
    if unknown:
        raise ValueError(f"Prodigal output refers to unknown contigs: {sorted(unknown)[:5]}")
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
            raise ValueError("Prodigal feature extends beyond supplied contig length")
    return {
        "schema": "kinetics.prodigal-gene-candidates.v1",
        "execution_mode": "local",
        "tool": "Prodigal",
        "tool_version": tool_version,
        "executable_sha256": actual_hash,
        "mode": mode,
        "translation_table": translation_table,
        "input_contigs": len(contigs),
        "input_bases": total_bases,
        "input_contig_sha256": contig_hashes,
        "annotation_sha256": hashlib.sha256(annotation_bytes).hexdigest(),
        "annotation_bytes": len(annotation_bytes),
        "annotation": annotation,
        "conclusion": "prokaryotic_gene_candidates_require_review",
        "limitations": [
            "Prodigal is a prokaryotic gene caller; this adapter does not support eukaryotic prediction.",
            "GFF3 syntax and coordinate checks do not establish gene-calling accuracy.",
            "The caller must approve the Prodigal binary and its license before use.",
            "The reported Prodigal version string is caller-supplied; executable SHA-256 is verified.",
            "No functional annotation, expression, pathogenicity or organism identity is inferred.",
            "The host must enforce OS-level network isolation.",
        ],
    }
