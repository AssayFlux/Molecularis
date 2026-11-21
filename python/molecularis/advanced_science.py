"""Bounded local execution for AlphaFold 3, MolProbity CLI and NUAD.

These adapters execute caller-installed, separately licensed scientific runtimes.
They hash inputs and executables, isolate outputs, and preserve raw result artifacts.
They do not bundle upstream weights, parameter databases or third-party runtimes.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_DNA = frozenset("ACGT")


def _file_digest(path: Path, limit: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                raise ValueError(f"{path.name} exceeds configured byte limit")
            digest.update(chunk)
    return digest.hexdigest(), size


def _tree_digest(path_value: str | Path, *, max_files: int, max_bytes: int) -> dict[str, Any]:
    root_input = Path(path_value).expanduser()
    if root_input.is_symlink():
        raise ValueError("Directory inputs must not be symlinks")
    root = root_input.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Directory input must be a directory")
    digest = hashlib.sha256()
    total = 0
    count = 0
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs):
            if (current_path / name).is_symlink():
                raise ValueError("Directory inputs must not contain symlinks")
        for name in sorted(files):
            item = current_path / name
            if item.is_symlink() or not item.is_file():
                raise ValueError("Directory inputs must contain only regular files")
            relative = item.relative_to(root).as_posix()
            count += 1
            if count > max_files:
                raise ValueError("Directory input exceeds max_files")
            file_hash, size = _file_digest(item, max_bytes - total)
            total += size
            digest.update(relative.encode("utf-8") + b"\0")
            digest.update(bytes.fromhex(file_hash))
            if total > max_bytes:
                raise ValueError("Directory input exceeds max_bytes")
    if count == 0:
        raise ValueError("Directory input must not be empty")
    return {"path": str(root), "sha256": digest.hexdigest(),
            "file_count": count, "bytes": total}


def _verified_file(value: str | Path, expected_sha256: str, label: str,
                   *, max_bytes: int = 2 * 1024**3, executable: bool = False) -> tuple[Path, str, int]:
    if not isinstance(expected_sha256, str) or not _SHA256.fullmatch(expected_sha256):
        raise ValueError(f"{label} expected SHA-256 must be lowercase hex")
    raw = Path(value).expanduser()
    if raw.is_symlink():
        raise ValueError(f"{label} must not be a symlink")
    path = raw.resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"{label} must be a regular file")
    if executable and not os.access(path, os.X_OK):
        raise ValueError(f"{label} must be executable")
    digest, size = _file_digest(path, max_bytes)
    if digest != expected_sha256:
        raise ValueError(f"{label} SHA-256 mismatch")
    return path, digest, size


def _fresh_directory(value: str | Path) -> Path:
    path = Path(value).expanduser().resolve()
    if path.exists():
        raise ValueError("Output directory must be new")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir()
    return path


def _collect_artifacts(root: Path, *, max_files: int, max_bytes: int) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    total = 0
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs.sort()
        for name in dirs:
            if (current_path / name).is_symlink():
                raise RuntimeError("Scientific runtime produced a symlink directory")
        for name in sorted(files):
            path = current_path / name
            if path.is_symlink() or not path.is_file():
                raise RuntimeError("Scientific runtime produced a non-regular artifact")
            digest, size = _file_digest(path, max_bytes - total)
            total += size
            if total > max_bytes or len(artifacts) >= max_files:
                raise RuntimeError("Scientific runtime output exceeds configured bounds")
            artifacts.append({"path": path.relative_to(root).as_posix(),
                              "sha256": digest, "bytes": size})
    return artifacts


def run_alphafold3(
    input_json: str | Path,
    output_directory: str | Path,
    *,
    python_executable: str | Path,
    python_sha256: str,
    run_script: str | Path,
    run_script_sha256: str,
    model_directory: str | Path,
    model_directory_sha256: str,
    database_directory: str | Path,
    database_directory_sha256: str,
    run_id: str,
    jax_backend: str = "cpu",
    flash_attention_implementation: str = "xla",
    timeout_seconds: int = 86400,
    max_input_bytes: int = 64 * 1024 * 1024,
    max_model_bytes: int = 2 * 1024**4,
    max_database_bytes: int = 4 * 1024**4,
    max_output_bytes: int = 64 * 1024**3,
) -> dict[str, Any]:
    """Run the official AlphaFold 3 entry point with explicitly pinned local assets.

    AlphaFold 3 source code and model parameters have distinct terms. The caller
    must obtain weights directly from Google and comply with the model terms.
    This runner never downloads or redistributes model weights or databases.
    """
    if not isinstance(run_id, str) or not run_id.strip() or len(run_id) > 200:
        raise ValueError("run_id must be non-empty text up to 200 characters")
    if jax_backend not in {"cpu", "gpu", "mps"}:
        raise ValueError("jax_backend must be cpu, gpu or mps")
    if flash_attention_implementation not in {"xla", "triton", " cudnn"}:
        raise ValueError("Unsupported flash attention implementation")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 604800:
        raise ValueError("timeout_seconds must be in [1, 604800]")
    python, python_hash, _ = _verified_file(python_executable, python_sha256, "python_executable", executable=True, max_bytes=512 * 1024**2)
    script, script_hash, _ = _verified_file(run_script, run_script_sha256, "run_script", max_bytes=64 * 1024**2)
    model = _tree_digest(model_directory, max_files=2_000_000, max_bytes=max_model_bytes)
    database = _tree_digest(database_directory, max_files=10_000_000, max_bytes=max_database_bytes)
    if model["sha256"] != model_directory_sha256 or not _SHA256.fullmatch(model_directory_sha256):
        raise ValueError("AlphaFold model directory SHA-256 mismatch")
    if database["sha256"] != database_directory_sha256 or not _SHA256.fullmatch(database_directory_sha256):
        raise ValueError("AlphaFold database directory SHA-256 mismatch")
    raw_input = Path(input_json).expanduser()
    if raw_input.is_symlink():
        raise ValueError("AlphaFold input JSON must not be a symlink")
    input_path = raw_input.resolve(strict=True)
    if not input_path.is_file():
        raise ValueError("AlphaFold input JSON must be a regular file")
    input_hash, input_size = _file_digest(input_path, max_input_bytes)
    try:
        parsed = json.loads(input_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("AlphaFold input must be valid UTF-8 JSON") from exc
    if not isinstance(parsed, dict) or not isinstance(parsed.get("name"), str) or not isinstance(parsed.get("sequences"), list) or not parsed["sequences"]:
        raise ValueError("AlphaFold input requires a name and non-empty sequences array")

    output = _fresh_directory(output_directory)
    argv = [
        str(python), str(script), f"--json_path={input_path}",
        f"--model_dir={model['path']}", f"--output_dir={output}",
        f"--db_dir={database['path']}", f"--jax_backend={jax_backend}",
        f"--flash_attention_implementation={flash_attention_implementation}",
    ]
    env = {"HOME": str(output), "TMPDIR": str(output), "TEMP": str(output),
           "TMP": str(output), "PATH": os.defpath, "LANG": "C", "LC_ALL": "C"}
    try:
        completed = subprocess.run(argv, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=output,
            env=env, timeout=timeout_seconds, check=False, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError("AlphaFold 3 exceeded timeout; partial output retained") from exc
    log = completed.stdout[:2 * 1024 * 1024].decode("utf-8", "replace")
    if completed.returncode != 0:
        raise RuntimeError(f"AlphaFold 3 exited with status {completed.returncode}: {log[-4000:]}")
    artifacts = _collect_artifacts(output, max_files=100_000, max_bytes=max_output_bytes)
    structures = [item for item in artifacts if item["path"].lower().endswith((".cif", ".mmcif", ".pdb"))]
    if not structures:
        raise RuntimeError("AlphaFold 3 completed without a structure artifact")
    return {
        "schema": "molecularis.alphafold3-run.v1", "engine": "alphafold3",
        "run_id": run_id, "execution_status": "completed",
        "input": {"path": str(input_path), "sha256": input_hash, "bytes": input_size},
        "python": {"path": str(python), "sha256": python_hash},
        "entrypoint": {"path": str(script), "sha256": script_hash},
        "model_directory": model, "database_directory": database,
        "parameters": {"jax_backend": jax_backend,
                       "flash_attention_implementation": flash_attention_implementation,
                       "timeout_seconds": timeout_seconds},
        "artifacts": artifacts, "structure_artifacts": structures,
        "stdout_tail": log[-4000:],
        "scientific_validation": "not_assessed",
        "limitations": ["Model parameters must be obtained directly from Google and used under their separate terms.",
                        "Database provenance is represented by a content digest, not biological coverage or freshness.",
                        "Output structure generation is not independent accuracy validation or clinical evidence."]
    }


def run_molprobity_cli(
    pdb_path: str | Path,
    output_directory: str | Path,
    *,
    executable_path: str | Path,
    executable_sha256: str,
    tool: str,
    run_id: str,
    timeout_seconds: int = 1800,
    max_input_bytes: int = 512 * 1024**2,
    max_output_bytes: int = 16 * 1024**2,
) -> dict[str, Any]:
    """Run one installed MolProbity command-line validator on a PDB file."""
    allowed = {"clashscore", "mp_geometry", "residue-analysis"}
    if tool not in allowed:
        raise ValueError(f"tool must be one of {sorted(allowed)}")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be non-empty")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 86400:
        raise ValueError("timeout_seconds must be in [1, 86400]")
    executable, executable_hash, _ = _verified_file(
        executable_path, executable_sha256, "MolProbity executable",
        executable=True, max_bytes=512 * 1024**2)
    raw = Path(pdb_path).expanduser()
    if raw.is_symlink():
        raise ValueError("PDB input must not be a symlink")
    pdb = raw.resolve(strict=True)
    if not pdb.is_file() or pdb.suffix.lower() not in {".pdb", ".ent"}:
        raise ValueError("MolProbity input must be a regular PDB/ENT file")
    input_hash, input_size = _file_digest(pdb, max_input_bytes)
    output = _fresh_directory(output_directory)
    env = {"HOME": str(output), "TMPDIR": str(output), "TEMP": str(output),
           "TMP": str(output), "PATH": os.defpath, "LANG": "C", "LC_ALL": "C"}
    try:
        completed = subprocess.run([str(executable), str(pdb)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, cwd=output, env=env,
            timeout=timeout_seconds, check=False, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(f"MolProbity {tool} exceeded timeout; partial output retained") from exc
    raw_output = completed.stdout
    if len(raw_output) > max_output_bytes:
        raise RuntimeError("MolProbity output exceeds max_output_bytes")
    text_output = raw_output.decode("utf-8", "replace")
    if completed.returncode != 0:
        raise RuntimeError(f"MolProbity {tool} exited with status {completed.returncode}: {text_output[-4000:]}")
    digest = hashlib.sha256(raw_output).hexdigest()
    artifacts = _collect_artifacts(output, max_files=10_000, max_bytes=max_output_bytes)
    return {
        "schema": "molecularis.molprobity-run.v1", "engine": "molprobity",
        "tool": tool, "run_id": run_id, "execution_status": "completed",
        "input": {"path": str(pdb), "sha256": input_hash, "bytes": input_size},
        "executable": {"path": str(executable), "sha256": executable_hash},
        "stdout": text_output, "stdout_sha256": digest,
        "artifacts": artifacts, "scientific_validation": "tool_completed",
        "limitations": ["Results are the raw output of the selected MolProbity command; interpret with its versioned reference data and documentation.",
                        "This is not a complete all-metrics MolProbity report unless every required command is run."]
    }


def run_nuad_design(
    design: Any,
    constraints: list[Any],
    output_directory: str | Path,
    *,
    random_seed: int,
    max_iterations: int,
    run_id: str,
) -> dict[str, Any]:
    """Run NUAD's stochastic DNA sequence search on caller-constructed design objects.

    NUAD is MIT-licensed. NUPACK/ViennaRNA-backed constraints remain subject to
    their own separate runtime and licensing requirements.
    """
    if isinstance(random_seed, bool) or not isinstance(random_seed, int) or not 0 <= random_seed <= 2**32 - 1:
        raise ValueError("random_seed must be an unsigned 32-bit integer")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or not 1 <= max_iterations <= 10_000_000:
        raise ValueError("max_iterations must be in [1, 10000000]")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be non-empty")
    if not isinstance(constraints, list) or not constraints or len(constraints) > 10_000:
        raise ValueError("constraints must be a non-empty bounded list")
    try:
        search = importlib.import_module("nuad.search")
        constraint_module = importlib.import_module("nuad.constraints")
    except ImportError as exc:
        raise RuntimeError("NUAD requires an approved local installation and dependencies") from exc
    if not isinstance(design, constraint_module.Design):
        raise ValueError("design must be a nuad.constraints.Design")
    if any(not isinstance(item, constraint_module.Constraint) for item in constraints):
        raise ValueError("every constraint must be a NUAD Constraint")
    output = _fresh_directory(output_directory)
    params = search.SearchParameters(
        constraints=constraints, random_seed=random_seed,
        max_iterations=max_iterations, out_directory=str(output),
        restart=False, force_overwrite=False, debug_log_file=False,
        info_log_file=False, scrolling_output=False,
    )
    search.search_for_sequences(design, params)
    strands: list[dict[str, str]] = []
    for strand in design.strands:
        sequence = strand.sequence()
        normalized = sequence.upper()
        if not normalized or set(normalized) - _DNA:
            raise RuntimeError("NUAD produced an invalid or incomplete DNA strand sequence")
        strands.append({"name": str(strand.name), "sequence": normalized})
    if not strands:
        raise RuntimeError("NUAD design contained no strands")
    result_path = output / "molecularis-nuad-sequences.json"
    result_path.write_text(json.dumps({"schema": "molecularis.nuad-sequences.v1",
        "run_id": run_id, "random_seed": random_seed,
        "max_iterations": max_iterations, "strands": strands},
        sort_keys=True, separators=(",", ":")), encoding="utf-8")
    result_hash, result_size = _file_digest(result_path, 16 * 1024 * 1024)
    return {
        "schema": "molecularis.nuad-run.v1", "engine": "nuad",
        "run_id": run_id, "execution_status": "completed",
        "random_seed": random_seed, "max_iterations": max_iterations,
        "strand_count": len(strands), "strands": strands,
        "sequence_artifact": {"path": str(result_path),
                              "sha256": result_hash, "bytes": result_size},
        "scientific_validation": "constraints_evaluated_by_nuad_search",
        "limitations": ["NUAD's search is stochastic; reproducibility also depends on dependency/runtime versions and custom constraint purity.",
                        "A max-iteration stop does not imply all constraints were satisfied.",
                        "NUPACK/ViennaRNA-backed constraints require separately licensed local runtimes."]
    }
