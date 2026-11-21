"""Pinned local AUGUSTUS adapter for eukaryotic GFF3 gene prediction."""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable

from .gff3 import parse_gff3
from .sequence import SequenceRecord

_SPECIES = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")


def _sha256_file(path: Path, *, max_bytes: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"AUGUSTUS artifact exceeds byte limit: {path.name}")
            digest.update(chunk)
    return digest.hexdigest(), total


def hash_augustus_species_model(
    config_path: str,
    species: str,
    *,
    max_files: int = 100_000,
    max_bytes: int = 2 * 1024 * 1024 * 1024,
) -> str:
    """Hash every regular file in one AUGUSTUS species parameter directory."""
    if not isinstance(species, str) or not _SPECIES.fullmatch(species):
        raise ValueError("species must be a safe AUGUSTUS species identifier")
    if (
        isinstance(max_files, bool) or not isinstance(max_files, int) or max_files < 1
        or isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 1
    ):
        raise ValueError("AUGUSTUS model limits must be positive integers")
    config = Path(config_path).expanduser().resolve(strict=True)
    if not config.is_dir():
        raise ValueError("config_path must be an AUGUSTUS configuration directory")
    model_dir = config / "species" / species
    if not model_dir.is_dir():
        raise ValueError(f"AUGUSTUS species model is missing: {species}")
    files = sorted(model_dir.rglob("*"))
    regular_files: list[Path] = []
    for path in files:
        if path.is_symlink():
            raise ValueError("AUGUSTUS species model must not contain symlinks")
        if path.is_file():
            regular_files.append(path)
    if not regular_files or len(regular_files) > max_files:
        raise ValueError("AUGUSTUS species model is empty or exceeds max_files")
    digest = hashlib.sha256()
    total = 0
    for path in regular_files:
        relative = path.relative_to(model_dir).as_posix()
        file_hash, size = _sha256_file(path, max_bytes=max_bytes - total)
        total += size
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(bytes.fromhex(file_hash))
    return digest.hexdigest()


def _output_limit(max_bytes: int) -> Callable[[], None] | None:
    if sys.platform == "win32":
        return None

    def apply() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_FSIZE, (max_bytes, max_bytes))

    return apply


def run_local_augustus(
    records: Iterable[SequenceRecord],
    *,
    executable_path: str,
    executable_sha256: str,
    config_path: str,
    species: str,
    species_model_sha256: str,
    tool_version: str,
    timeout_seconds: int = 3600,
    max_contigs: int = 100_000,
    max_total_bases: int = 500_000_000,
    max_executable_bytes: int = 512 * 1024 * 1024,
    max_model_bytes: int = 2 * 1024 * 1024 * 1024,
    max_gff3_bytes: int = 256 * 1024 * 1024,
) -> dict[str, object]:
    """Run a pinned local AUGUSTUS binary/species model and validate GFF3 output."""
    if not isinstance(species, str) or not _SPECIES.fullmatch(species):
        raise ValueError("species must be a safe AUGUSTUS species identifier")
    for name, value in (
        ("timeout_seconds", timeout_seconds),
        ("max_contigs", max_contigs),
        ("max_total_bases", max_total_bases),
        ("max_executable_bytes", max_executable_bytes),
        ("max_model_bytes", max_model_bytes),
        ("max_gff3_bytes", max_gff3_bytes),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    for digest_name, digest_value in (
        ("executable_sha256", executable_sha256),
        ("species_model_sha256", species_model_sha256),
    ):
        if (
            not isinstance(digest_value, str)
            or len(digest_value) != 64
            or any(char not in "0123456789abcdef" for char in digest_value)
        ):
            raise ValueError(f"{digest_name} must be lowercase SHA-256 hex")
    if not isinstance(tool_version, str) or not tool_version.strip():
        raise ValueError("tool_version must be non-empty caller-supplied text")

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
            raise ValueError(f"Contig {record.identifier!r} contains invalid DNA")
        if len(sequence) > max_total_bases - total_bases:
            raise ValueError("Genome exceeds max_total_bases")
        contigs[record.identifier] = sequence
        total_bases += len(sequence)
    if not contigs:
        raise ValueError("Genome contains no contigs")

    executable = Path(executable_path).expanduser().resolve(strict=True)
    config = Path(config_path).expanduser().resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("AUGUSTUS executable must be an executable regular file")
    if not config.is_dir():
        raise ValueError("config_path must be an AUGUSTUS configuration directory")
    executable_hash, _ = _sha256_file(executable, max_bytes=max_executable_bytes)
    if executable_hash != executable_sha256:
        raise ValueError("AUGUSTUS executable SHA-256 does not match approved digest")
    model_hash = hash_augustus_species_model(
        str(config), species, max_bytes=max_model_bytes,
    )
    if model_hash != species_model_sha256:
        raise ValueError("AUGUSTUS species-model SHA-256 does not match approved digest")
    contig_hashes = {
        name: hashlib.sha256(sequence.encode("ascii")).hexdigest()
        for name, sequence in contigs.items()
    }
    fasta = "".join(f">{name}\n{sequence}\n" for name, sequence in contigs.items())

    with tempfile.TemporaryDirectory(prefix="kinetics-augustus-") as directory:
        work = Path(directory)
        input_path = work / "genome.fasta"
        output_path = work / "annotation.gff3"
        input_path.write_text(fasta, encoding="ascii")
        try:
            result = subprocess.run(
                [
                    str(executable),
                    f"--species={species}",
                    "--gff3=on",
                    f"--outfile={output_path}",
                    str(input_path),
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
                    "AUGUSTUS_CONFIG_PATH": str(config),
                    "LANG": "C",
                    "LC_ALL": "C",
                },
                timeout=timeout_seconds,
                check=False,
                shell=False,
                preexec_fn=_output_limit(max_gff3_bytes),
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("Local AUGUSTUS exceeded timeout_seconds") from exc
        if result.returncode != 0:
            raise RuntimeError(f"AUGUSTUS exited with status {result.returncode}")
        if not output_path.is_file():
            raise RuntimeError("AUGUSTUS did not create GFF3 output")
        if output_path.stat().st_size > max_gff3_bytes:
            raise ValueError("AUGUSTUS GFF3 output exceeds max_gff3_bytes")
        with output_path.open("r", encoding="utf-8", errors="strict") as stream:
            annotation = parse_gff3(stream)
        annotation_bytes = output_path.read_bytes()

    sequence_ids = annotation.get("sequence_ids")
    features = annotation.get("features")
    if not isinstance(sequence_ids, list) or not isinstance(features, list):
        raise RuntimeError("GFF3 parser returned an invalid annotation structure")
    unknown = set(sequence_ids) - set(contigs)
    if unknown:
        raise ValueError(f"AUGUSTUS output refers to unknown contigs: {sorted(unknown)[:5]}")
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
            raise ValueError("AUGUSTUS feature extends beyond supplied contig length")
    return {
        "schema": "kinetics.augustus-gene-candidates.v1",
        "execution_mode": "local",
        "tool": "AUGUSTUS",
        "tool_version": tool_version,
        "executable_sha256": executable_hash,
        "species_model_sha256": model_hash,
        "species": species,
        "input_contigs": len(contigs),
        "input_bases": total_bases,
        "input_contig_sha256": contig_hashes,
        "annotation_sha256": hashlib.sha256(annotation_bytes).hexdigest(),
        "annotation_bytes": len(annotation_bytes),
        "annotation": annotation,
        "conclusion": "eukaryotic_gene_candidates_require_review",
        "limitations": [
            "AUGUSTUS species models are caller-supplied and require license/provenance review.",
            "GFF3 syntax and coordinate checks do not establish gene-calling accuracy.",
            "The caller-supplied version string is not independently authenticated.",
            "No functional annotation, expression, pathogenicity or organism identity is inferred.",
            "The host must enforce OS-level network isolation.",
        ],
    }
