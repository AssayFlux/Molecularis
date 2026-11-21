"""Molecularis-owned, bounded GROMACS execution for caller-prepared TPR systems.

This runner executes an explicitly approved local GROMACS binary against a
caller-supplied TPR file. It does not build topologies, choose force fields,
parameterize ligands, or infer simulation settings. Outputs are hashed and
returned in a Molecularis result envelope; execution is not scientific validation.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path
from typing import Sequence

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_OUTPUT_SUFFIXES = (".xtc", ".trr", ".edr", ".log", ".gro", ".cpt")


def _digest(path: Path, limit: int) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                raise ValueError(f"{path.name} exceeds configured byte limit")
            h.update(chunk)
    return h.hexdigest(), size


def _regular_file(value: str | Path, label: str) -> Path:
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"{label} must be a regular file")
    return path


def run_gromacs(
    tpr_path: str | Path,
    output_directory: str | Path,
    *,
    executable_path: str | Path,
    executable_sha256: str,
    tpr_sha256: str,
    force_field_manifest: dict[str, str],
    run_id: str,
    threads: int = 1,
    timeout_seconds: int = 86400,
    max_tpr_bytes: int = 8 * 1024 * 1024 * 1024,
    max_output_bytes: int = 32 * 1024 * 1024 * 1024,
    extra_mdrun_args: Sequence[str] = (),
) -> dict[str, object]:
    """Run GROMACS mdrun in an isolated fresh directory and hash its artifacts.

    The TPR is the authoritative prepared simulation input. Its force-field,
    topology and parameter provenance must be supplied in force_field_manifest.
    Arbitrary extra command flags are intentionally not accepted.
    """
    for name, value in (("executable_sha256", executable_sha256), ("tpr_sha256", tpr_sha256)):
        if not isinstance(value, str) or not _SHA256.fullmatch(value):
            raise ValueError(f"{name} must be lowercase SHA-256 hex")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be non-empty")
    if not isinstance(force_field_manifest, dict) or not force_field_manifest:
        raise ValueError("force_field_manifest must be a non-empty mapping")
    required = {"name", "version", "parameter_source_sha256"}
    if not required.issubset(force_field_manifest):
        raise ValueError("force_field_manifest requires name, version and parameter_source_sha256")
    if not _SHA256.fullmatch(force_field_manifest["parameter_source_sha256"]):
        raise ValueError("parameter_source_sha256 must be lowercase SHA-256 hex")
    if any(not isinstance(k, str) or not isinstance(v, str) or not v.strip()
           for k, v in force_field_manifest.items()):
        raise ValueError("force_field_manifest keys and values must be non-empty strings")
    if isinstance(threads, bool) or not isinstance(threads, int) or not 1 <= threads <= 256:
        raise ValueError("threads must be an integer between 1 and 256")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 604800:
        raise ValueError("timeout_seconds must be between 1 and 604800")
    if extra_mdrun_args:
        raise ValueError("extra_mdrun_args is not supported; simulation flags are fixed by the approved TPR")
    for name, limit in (("max_tpr_bytes", max_tpr_bytes), ("max_output_bytes", max_output_bytes)):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError(f"{name} must be a positive integer")

    executable = _regular_file(executable_path, "executable_path")
    if not os.access(executable, os.X_OK):
        raise ValueError("GROMACS executable must be executable")
    tpr = _regular_file(tpr_path, "tpr_path")
    actual_tpr_hash, tpr_bytes = _digest(tpr, max_tpr_bytes)
    if actual_tpr_hash != tpr_sha256:
        raise ValueError("TPR SHA-256 does not match the approved digest")
    actual_executable_hash, _ = _digest(executable, 512 * 1024 * 1024)
    if actual_executable_hash != executable_sha256:
        raise ValueError("GROMACS executable SHA-256 does not match the approved digest")

    destination = Path(output_directory).expanduser().resolve()
    if destination.exists():
        raise ValueError("output_directory must be a new directory")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    prefix = destination / "molecularis"
    argv = [str(executable), "mdrun", "-s", str(tpr), "-deffnm", str(prefix), "-nt", str(threads)]
    env = {
        "HOME": str(destination), "TMPDIR": str(destination), "TEMP": str(destination),
        "TMP": str(destination), "PATH": os.defpath, "LANG": "C", "LC_ALL": "C",
    }
    try:
        completed = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, cwd=destination, env=env,
            timeout=timeout_seconds, check=False, shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError("GROMACS exceeded timeout_seconds; partial output directory retained") from exc
    if completed.returncode != 0:
        raise RuntimeError(f"GROMACS mdrun exited with status {completed.returncode}")

    artifacts: list[dict[str, object]] = []
    total = 0
    for suffix in _OUTPUT_SUFFIXES:
        path = Path(str(prefix) + suffix)
        if path.is_file():
            digest, size = _digest(path, max_output_bytes)
            total += size
            if total > max_output_bytes:
                raise ValueError("GROMACS outputs exceed max_output_bytes")
            if size:
                artifacts.append({"name": path.name, "sha256": digest, "bytes": size})
    if not artifacts or not any(item["name"].endswith((".xtc", ".trr")) for item in artifacts):
        raise RuntimeError("GROMACS completed without producing a non-empty trajectory artifact")
    version = "unknown"
    try:
        version_result = subprocess.run(
            [str(executable), "--version"], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=destination,
            env=env, timeout=min(timeout_seconds, 30), check=False, shell=False,
        )
        if version_result.returncode == 0:
            version = version_result.stdout.decode("utf-8", errors="replace")[:4096].strip()
    except subprocess.TimeoutExpired:
        pass
    return {
        "schema": "molecularis.gromacs-run.v1",
        "engine": "gromacs",
        "engine_version": version,
        "run_id": run_id,
        "execution_status": "completed",
        "input": {"tpr_path": str(tpr), "sha256": actual_tpr_hash, "bytes": tpr_bytes},
        "executable": {"path": str(executable), "sha256": actual_executable_hash},
        "force_field_manifest": dict(force_field_manifest),
        "parameters": {"threads": threads, "timeout_seconds": timeout_seconds},
        "artifacts": artifacts,
        "output_directory": str(destination),
        "scientific_validation": "not_assessed",
        "limitations": [
            "Requires a caller-prepared TPR; no topology construction or parameterization is performed.",
            "The supplied force-field manifest is provenance supplied by the caller, not independently inspected in the TPR.",
            "Trajectory and energy outputs are not independently assessed for physical validity.",
        ],
    }
