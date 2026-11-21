"""Bounded, hash-pinned local BLASTP search against an installed protein database."""
from __future__ import annotations

import hashlib
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Mapping
from urllib.parse import urlparse

from .sequence import parse_fasta

_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWYBXZJ")


def _resolve_database_prefix(database_prefix: str) -> Path:
    raw = Path(database_prefix).expanduser()
    if not raw.name:
        raise ValueError("database_prefix must name a BLAST database")
    return raw.parent.resolve(strict=True) / raw.name


def _file_limit(max_bytes: int) -> Callable[[], None] | None:
    if sys.platform == "win32":
        return None

    def apply() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_FSIZE, (max_bytes, max_bytes))

    return apply


def _hash_file(path: Path, *, max_bytes: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"BLAST artifact exceeds byte limit: {path.name}")
            digest.update(chunk)
    return digest.hexdigest(), total


def hash_blast_protein_database(
    database_prefix: str,
    file_sha256: Mapping[str, str],
    *,
    max_bytes: int = 8 * 1024 * 1024 * 1024,
) -> str:
    """Verify and hash the required BLAST protein database core files."""
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 1:
        raise ValueError("max_bytes must be a positive integer")
    prefix = _resolve_database_prefix(database_prefix)
    required = {".pin", ".phr", ".psq"}
    if not required.issubset(file_sha256):
        raise ValueError("BLAST protein database manifest requires .pin, .phr and .psq")
    if any(
        not isinstance(suffix, str)
        or not suffix.startswith(".")
        or "/" in suffix
        or "\\" in suffix
        for suffix in file_sha256
    ):
        raise ValueError("BLAST database manifest keys must be simple suffixes")
    digest = hashlib.sha256()
    total = 0
    for suffix in sorted(file_sha256):
        expected = file_sha256[suffix]
        if (
            not isinstance(expected, str)
            or len(expected) != 64
            or any(char not in "0123456789abcdef" for char in expected)
        ):
            raise ValueError(f"BLAST database digest for {suffix} must be lowercase SHA-256 hex")
        artifact = Path(str(prefix) + suffix)
        if not artifact.is_file():
            raise ValueError(f"BLAST database is missing {artifact.name}")
        actual, size = _hash_file(artifact, max_bytes=max_bytes - total)
        total += size
        if actual != expected:
            raise ValueError(f"BLAST database digest mismatch for {suffix}")
        digest.update(suffix.encode("ascii") + b"\0")
        digest.update(bytes.fromhex(actual))
    return digest.hexdigest()


def run_local_blastp(
    query_fasta: str,
    *,
    executable_path: str,
    executable_sha256: str,
    database_prefix: str,
    database_file_sha256: Mapping[str, str],
    database_id: str,
    database_version: str,
    database_license: str,
    database_source: str,
    max_input_bytes: int = 32 * 1024 * 1024,
    max_database_bytes: int = 8 * 1024 * 1024 * 1024,
    max_executable_bytes: int = 512 * 1024 * 1024,
    max_output_bytes: int = 64 * 1024 * 1024,
    max_queries: int = 100_000,
    max_total_residues: int = 20_000_000,
    max_hits: int = 1_000_000,
    max_target_seqs: int = 100,
    evalue_threshold: float = 10.0,
    timeout_seconds: int = 600,
) -> dict[str, object]:
    """Run BLASTP locally and parse a bounded tabular candidate-hit report."""
    if not isinstance(query_fasta, str) or not query_fasta.strip():
        raise ValueError("query_fasta must be non-empty text")
    query_bytes = query_fasta.encode("utf-8")
    if len(query_bytes) > max_input_bytes:
        raise ValueError("BLAST query FASTA exceeds max_input_bytes")
    for name, value in (
        ("max_input_bytes", max_input_bytes),
        ("max_database_bytes", max_database_bytes),
        ("max_executable_bytes", max_executable_bytes),
        ("max_output_bytes", max_output_bytes),
        ("max_queries", max_queries),
        ("max_total_residues", max_total_residues),
        ("max_hits", max_hits),
        ("max_target_seqs", max_target_seqs),
        ("timeout_seconds", timeout_seconds),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if (
        isinstance(evalue_threshold, bool)
        or not isinstance(evalue_threshold, (int, float))
        or not math.isfinite(evalue_threshold)
        or evalue_threshold <= 0
    ):
        raise ValueError("evalue_threshold must be finite and positive")
    for text_name, text_value in (
        ("database_id", database_id),
        ("database_version", database_version),
        ("database_license", database_license),
        ("database_source", database_source),
    ):
        if not isinstance(text_value, str) or not text_value.strip():
            raise ValueError(f"{text_name} must be non-empty text")
    if urlparse(database_source).scheme not in {"https", "http", "doi"}:
        raise ValueError("database_source must be an http(s) or doi URI")
    if (
        not isinstance(executable_sha256, str)
        or len(executable_sha256) != 64
        or any(char not in "0123456789abcdef" for char in executable_sha256)
    ):
        raise ValueError("executable_sha256 must be lowercase SHA-256 hex")

    records = parse_fasta(query_fasta)
    if len(records) > max_queries:
        raise ValueError("BLAST query FASTA exceeds max_queries")
    queries: dict[str, int] = {}
    total_residues = 0
    for record in records:
        if record.identifier in queries:
            raise ValueError("BLAST query identifiers must be unique")
        sequence = record.sequence.upper()
        if not sequence or any(residue not in _AMINO_ACIDS for residue in sequence):
            raise ValueError(f"BLAST query {record.identifier!r} contains invalid amino acids")
        total_residues += len(sequence)
        if total_residues > max_total_residues:
            raise ValueError("BLAST query FASTA exceeds max_total_residues")
        queries[record.identifier] = len(sequence)

    executable = Path(executable_path).expanduser().resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("BLAST executable must be an executable regular file")
    executable_hash, _ = _hash_file(executable, max_bytes=max_executable_bytes)
    if executable_hash != executable_sha256:
        raise ValueError("BLAST executable SHA-256 does not match approved digest")
    database_hash = hash_blast_protein_database(
        database_prefix, database_file_sha256, max_bytes=max_database_bytes,
    )
    database = _resolve_database_prefix(database_prefix)
    if _hash_file(executable, max_bytes=max_executable_bytes)[0] != executable_hash:
        raise ValueError("BLAST executable changed after approval")
    if hash_blast_protein_database(
        str(database), database_file_sha256, max_bytes=max_database_bytes,
    ) != database_hash:
        raise ValueError("BLAST database changed after approval")

    with tempfile.TemporaryDirectory(prefix="kinetics-blastp-") as directory:
        work = Path(directory)
        query_path = work / "queries.fasta"
        output_path = work / "hits.tsv"
        stderr_path = work / "blastp.stderr"
        query_path.write_bytes(query_bytes)
        try:
            with stderr_path.open("wb") as stderr:
                result = subprocess.run(
                    [
                        str(executable),
                        "-query", str(query_path),
                        "-db", str(database),
                        "-out", str(output_path),
                        "-outfmt",
                        "6 qseqid sseqid pident length mismatch gapopen "
                        "qstart qend sstart send evalue bitscore qlen slen",
                        "-evalue", str(evalue_threshold),
                        "-max_target_seqs", str(max_target_seqs),
                        "-num_threads", "1",
                    ],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=stderr,
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
                    preexec_fn=_file_limit(max_output_bytes),
                )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("Local BLASTP exceeded timeout_seconds") from exc
        if result.returncode != 0:
            raise RuntimeError(f"Local BLASTP exited with status {result.returncode}")
        if not output_path.is_file():
            raise RuntimeError("BLASTP did not create its tabular output")
        if output_path.stat().st_size > max_output_bytes:
            raise ValueError("BLASTP output exceeds max_output_bytes")
        hits: list[dict[str, object]] = []
        hits_per_query: dict[str, int] = {}
        with output_path.open("r", encoding="utf-8", errors="strict") as stream:
            for line_number, raw in enumerate(stream, 1):
                if len(raw.encode("utf-8")) > 16_384:
                    raise ValueError("BLASTP output line exceeds 16384 bytes")
                fields = raw.rstrip("\r\n").split("\t")
                if len(fields) != 14:
                    raise ValueError(f"BLASTP output line {line_number} must have 14 fields")
                (
                    query_id, subject_id, identity_s, length_s, mismatch_s, gapopen_s,
                    qstart_s, qend_s, sstart_s, send_s, evalue_s, bitscore_s,
                    qlen_s, slen_s,
                ) = fields
                if query_id not in queries or not subject_id:
                    raise ValueError(f"BLASTP output line {line_number} has an unknown query")
                try:
                    identity = float(identity_s)
                    alignment_length = int(length_s)
                    mismatches = int(mismatch_s)
                    gap_opens = int(gapopen_s)
                    qstart, qend = int(qstart_s), int(qend_s)
                    sstart, send = int(sstart_s), int(send_s)
                    evalue, bitscore = float(evalue_s), float(bitscore_s)
                    query_length, subject_length = int(qlen_s), int(slen_s)
                except ValueError as exc:
                    raise ValueError(f"BLASTP output line {line_number} has invalid numbers") from exc
                if any(not math.isfinite(value) for value in (identity, evalue, bitscore)):
                    raise ValueError(f"BLASTP output line {line_number} has non-finite values")
                if (
                    not 0.0 <= identity <= 100.0
                    or alignment_length < 1
                    or mismatches < 0
                    or gap_opens < 0
                    or query_length != queries[query_id]
                    or subject_length < 1
                    or not (1 <= qstart <= qend <= query_length)
                    or not (1 <= sstart <= send <= subject_length)
                    or evalue < 0
                    or evalue > evalue_threshold
                    or bitscore < 0
                ):
                    raise ValueError(f"BLASTP output line {line_number} has invalid coordinates")
                if len(hits) >= max_hits:
                    raise ValueError("BLASTP output exceeds max_hits")
                hits_per_query[query_id] = hits_per_query.get(query_id, 0) + 1
                if hits_per_query[query_id] > max_target_seqs:
                    raise ValueError("BLASTP output exceeds max_target_seqs for a query")
                hits.append({
                    "query_id": query_id,
                    "subject_id": subject_id,
                    "percent_identity": identity,
                    "alignment_length": alignment_length,
                    "mismatches": mismatches,
                    "gap_opens": gap_opens,
                    "query_start_1based": qstart,
                    "query_end_1based": qend,
                    "subject_start_1based": sstart,
                    "subject_end_1based": send,
                    "evalue": evalue,
                    "bit_score": bitscore,
                    "query_length": query_length,
                    "subject_length": subject_length,
                })
        version_result = subprocess.run(
            [str(executable), "-version"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=work,
            env={"PATH": os.defpath, "LANG": "C", "LC_ALL": "C"},
            timeout=min(timeout_seconds, 30),
            check=False,
            shell=False,
        )
        if version_result.returncode != 0:
            raise RuntimeError("Pinned BLASTP executable failed its version check")
        version = version_result.stdout[:4096].decode("utf-8", errors="replace").strip()
        if not version:
            raise RuntimeError("Pinned BLASTP executable did not identify its version")
        return {
            "schema": "kinetics.local-blastp-evidence.v1",
            "execution_mode": "local",
            "tool": "blastp",
            "tool_version": version,
            "executable_sha256": executable_hash,
            "database": {
                "id": database_id,
                "version": database_version,
                "license": database_license,
                "source": database_source,
                "content_sha256": database_hash,
            },
            "query_count": len(queries),
            "hit_count": len(hits),
            "hits": hits,
            "conclusion": "candidate_homology_hits_require_review" if hits else "no_hits_reported",
            "limitations": [
                "The database license, source and biological curation are caller-supplied.",
                "Similarity hits are candidates and do not establish function or orthology.",
                "No remote BLAST service or network access is used.",
                "The host must enforce OS-level network isolation.",
                "E-values and bit scores depend on database size and search parameters.",
            ],
        }
