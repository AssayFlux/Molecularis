"""Bounded local HMMER execution and evidence parsing.

No downloads, shell expansion, or implicit executable/profile discovery occur.
The caller supplies explicit local paths and SHA-256 digests for both artifacts.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Mapping

from .hmmer import parse_hmmscan_domtblout


def _child_file_limit(max_bytes: int) -> Callable[[], None] | None:
    """Apply a kernel-enforced output-file ceiling on POSIX child processes."""
    if sys.platform == "win32":
        return None

    def apply_limit() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_FSIZE, (max_bytes, max_bytes))

    return apply_limit


def _sha256_file(path: Path, *, max_bytes: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"Artifact exceeds byte limit: {path.name}")
            digest.update(chunk)
    return digest.hexdigest(), total


def hash_pressed_profile_pack(
    profile_path: str, *, max_bytes: int = 512 * 1024 * 1024,
) -> str:
    """Hash an HMM source file and all four HMMER pressed-index siblings."""
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 1:
        raise ValueError("max_bytes must be a positive integer")
    source = Path(profile_path).expanduser().resolve(strict=True)
    if not source.is_file():
        raise ValueError("profile_path must be an HMM source file")
    digest = hashlib.sha256()
    total = 0
    for suffix in ("", ".h3m", ".h3i", ".h3f", ".h3p"):
        artifact = source if not suffix else Path(str(source) + suffix)
        if not artifact.is_file():
            raise ValueError(f"Pressed HMM profile pack is missing {artifact.name}")
        artifact_hash, size = _sha256_file(
            artifact, max_bytes=max_bytes - total,
        )
        total += size
        digest.update(suffix.encode("ascii") + b"\\0")
        digest.update(bytes.fromhex(artifact_hash))
    return digest.hexdigest()


def run_local_hmmscan(
    sequences_fasta: str,
    *,
    executable_path: str,
    executable_sha256: str,
    profile_path: str,
    profile_pack: Mapping[str, str],
    max_input_bytes: int = 64 * 1024 * 1024,
    max_profile_bytes: int = 512 * 1024 * 1024,
    max_executable_bytes: int = 512 * 1024 * 1024,
    max_output_bytes: int = 64 * 1024 * 1024,
    timeout_seconds: int = 300,
    max_domains: int = 1_000_000,
) -> dict[str, object]:
    """Run a locally installed hmmscan against one explicitly pinned HMM file."""
    if not isinstance(sequences_fasta, str) or not sequences_fasta.strip():
        raise ValueError("sequences_fasta must be non-empty text")
    fasta_bytes = sequences_fasta.encode("utf-8")
    if len(fasta_bytes) > max_input_bytes:
        raise ValueError("FASTA input exceeds max_input_bytes")
    if not sequences_fasta.lstrip().startswith(">"):
        raise ValueError("FASTA input must begin with a record header")
    for name, value in (
        ("max_input_bytes", max_input_bytes),
        ("max_profile_bytes", max_profile_bytes),
        ("max_executable_bytes", max_executable_bytes),
        ("max_output_bytes", max_output_bytes),
        ("timeout_seconds", timeout_seconds),
        ("max_domains", max_domains),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    expected_executable_hash = executable_sha256
    if (
        not isinstance(expected_executable_hash, str)
        or len(expected_executable_hash) != 64
        or any(c not in "0123456789abcdef" for c in expected_executable_hash)
    ):
        raise ValueError("executable_sha256 must be lowercase SHA-256 hex")

    executable = Path(executable_path).expanduser().resolve(strict=True)
    profile = Path(profile_path).expanduser().resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("HMMER executable_path must be an executable regular file")
    if not profile.is_file():
        raise ValueError("profile_path must be a regular file")
    executable_hash, _ = _sha256_file(
        executable, max_bytes=max_executable_bytes,
    )
    if executable_hash != expected_executable_hash:
        raise ValueError("HMMER executable SHA-256 does not match approved digest")
    profile_hash = hash_pressed_profile_pack(
        str(profile), max_bytes=max_profile_bytes,
    )
    if dict(profile_pack).get("content_sha256") != profile_hash:
        raise ValueError(
            "Pressed HMM profile-pack SHA-256 does not match profile-pack metadata"
        )

    if _sha256_file(executable, max_bytes=max_executable_bytes)[0] != executable_hash:
        raise ValueError("HMMER executable changed after approval")
    if hash_pressed_profile_pack(
        str(profile), max_bytes=max_profile_bytes,
    ) != profile_hash:
        raise ValueError("Pressed HMM profile pack changed after approval")

    with tempfile.TemporaryDirectory(prefix="kinetics-hmmscan-") as work_dir:
        work = Path(work_dir)
        fasta_path = work / "queries.fasta"
        output_path = work / "domains.tbl"
        stderr_path = work / "hmmscan.stderr"
        fasta_path.write_bytes(fasta_bytes)
        env = {
            "HOME": str(work),
            "TMPDIR": str(work),
            "TEMP": str(work),
            "TMP": str(work),
            "LANG": "C",
            "LC_ALL": "C",
        }
        try:
            with stderr_path.open("wb") as stderr_handle:
                run_result = subprocess.run(
                    [
                        str(executable),
                        "--cpu",
                        "1",
                        "--noali",
                        "--domtblout",
                        str(output_path),
                        str(profile),
                        str(fasta_path),
                    ],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=stderr_handle,
                    cwd=work,
                    env=env,
                    check=False,
                    timeout=timeout_seconds,
                    shell=False,
                    preexec_fn=_child_file_limit(max_output_bytes),
                )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("Local hmmscan exceeded timeout_seconds") from exc

        if run_result.returncode != 0:
            raise RuntimeError(f"hmmscan exited with status {run_result.returncode}")
        if stderr_path.stat().st_size > max_output_bytes:
            raise ValueError("HMMER diagnostic output exceeds max_output_bytes")
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
        if not output_path.exists():
            raise RuntimeError(
                f"hmmscan did not create domtblout (diagnostics: {stderr_text[-2000:]})"
            )
        if output_path.stat().st_size > max_output_bytes:
            raise ValueError("HMMER domtblout exceeds max_output_bytes")
        if not output_path.is_file():
            raise RuntimeError("hmmscan domtblout is not a regular file")
        # HMMER's version output is requested from the same pinned executable.
        version_result = subprocess.run(
            [str(executable), "-h"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=work,
            env=env,
            check=False,
            timeout=min(timeout_seconds, 30),
            shell=False,
        )
        if version_result.returncode != 0:
            raise RuntimeError("Pinned executable failed the HMMER version check")
        version_text = version_result.stdout[:65536].decode("utf-8", errors="replace")
        version_line = next(
            (line.strip() for line in version_text.splitlines()
             if line.startswith("# HMMER") or "HMMER " in line),
            "",
        )
        if not version_line:
            raise RuntimeError("Pinned executable did not identify itself as HMMER")
        if not stderr_text.strip() and output_path.stat().st_size == 0:
            # An empty valid result is allowed, but still parsed as an empty evidence set.
            pass
        with output_path.open("r", encoding="utf-8", errors="strict") as handle:
            evidence = parse_hmmscan_domtblout(
                handle,
                hmmer_version=version_line,
                profile_pack=dict(profile_pack),
                max_lines=max_output_bytes,
                max_line_bytes=min(max_output_bytes, 16_384),
                max_domains=max_domains,
            )
        return {
            "schema": "kinetics.local-hmmscan-run.v1",
            "execution_mode": "local",
            "executable_sha256": executable_hash,
            "profile_pack_sha256": profile_hash,
            "evidence": evidence,
            "diagnostics": stderr_text[-2000:],
            "limitations": [
                "The host must approve HMMER executable and profile-pack licenses.",
                "The caller is responsible for validating profile provenance and thresholds.",
                "Profile hits are candidates, not validated protein-family or function assignments.",
                "No network access is requested; the host must enforce OS-level network isolation.",
            ],
        }



def press_local_hmm_profile(
    *,
    hmmpress_executable_path: str,
    hmmpress_sha256: str,
    profile_path: str,
    source_hmm_sha256: str,
    profile_name: str,
    profile_version: str,
    profile_license: str,
    profile_source: str,
    timeout_seconds: int = 300,
    max_executable_bytes: int = 512 * 1024 * 1024,
    max_profile_bytes: int = 512 * 1024 * 1024,
) -> dict[str, object]:
    """Run a hash-pinned local hmmpress and produce metadata for a pressed pack."""
    for name, value in (
        ("timeout_seconds", timeout_seconds),
        ("max_executable_bytes", max_executable_bytes),
        ("max_profile_bytes", max_profile_bytes),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    for digest_name, digest_value in (
        ("hmmpress_sha256", hmmpress_sha256),
        ("source_hmm_sha256", source_hmm_sha256),
    ):
        if (
            not isinstance(digest_value, str)
            or len(digest_value) != 64
            or any(char not in "0123456789abcdef" for char in digest_value)
        ):
            raise ValueError(f"{digest_name} must be lowercase SHA-256 hex")
    for text_name, text_value in (
        ("profile_name", profile_name),
        ("profile_version", profile_version),
        ("profile_license", profile_license),
        ("profile_source", profile_source),
    ):
        if not isinstance(text_value, str) or not text_value.strip():
            raise ValueError(f"{text_name} must be non-empty text")

    executable = Path(hmmpress_executable_path).expanduser().resolve(strict=True)
    profile = Path(profile_path).expanduser().resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("hmmpress executable must be an executable regular file")
    if not profile.is_file():
        raise ValueError("profile_path must be a regular HMM source file")
    executable_hash, _ = _sha256_file(
        executable, max_bytes=max_executable_bytes,
    )
    if executable_hash != hmmpress_sha256:
        raise ValueError("hmmpress executable SHA-256 does not match approved digest")
    source_hash, _ = _sha256_file(profile, max_bytes=max_profile_bytes)
    if source_hash != source_hmm_sha256:
        raise ValueError("Source HMM SHA-256 does not match approved digest")

    with tempfile.TemporaryDirectory(prefix="kinetics-hmmpress-") as directory:
        work = Path(directory)
        stderr_path = work / "hmmpress.stderr"
        try:
            with stderr_path.open("wb") as stderr_handle:
                result = subprocess.run(
                    [str(executable), "-f", str(profile)],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=stderr_handle,
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
                    preexec_fn=_child_file_limit(max_profile_bytes),
                )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("Local hmmpress exceeded timeout_seconds") from exc
        if result.returncode != 0:
            diagnostics = stderr_path.read_text(encoding="utf-8", errors="replace")
            raise RuntimeError(
                f"hmmpress exited with status {result.returncode}: {diagnostics[-2000:]}"
            )

    pack_hash = hash_pressed_profile_pack(
        str(profile), max_bytes=max_profile_bytes,
    )
    return {
        "schema": "kinetics.pressed-hmm-profile-pack.v1",
        "hmmpress_sha256": executable_hash,
        "source_hmm_sha256": source_hash,
        "profile_pack": {
            "name": profile_name,
            "version": profile_version,
            "license": profile_license,
            "source": profile_source,
            "content_sha256": pack_hash,
        },
        "pressed_profile_prefix": str(profile),
        "limitations": [
            "The caller must independently approve profile source and license terms.",
            "The pack hash identifies source HMM and generated pressed index files.",
            "Pressing validates file production, not biological profile quality or thresholds.",
        ],
    }
