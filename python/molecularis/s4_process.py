"""Pinned local-process adapter for the S4 prediction envelope protocol.

The executable must accept --kinetics-request PATH, --kinetics-response PATH,
and --weights PATH, then write one JSON kinetics.structure-prediction.v1
envelope to the response path. The host remains responsible for OS network
isolation and model/runtime license approval.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable

from .s4_engine import run_local_structure_prediction


def _file_sha256(path: Path, *, max_bytes: int) -> str:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"Artifact exceeds configured byte limit: {path.name}")
            digest.update(chunk)
    return digest.hexdigest()


def _file_size_limit(max_bytes: int) -> Callable[[], None] | None:
    if sys.platform == "win32":
        return None

    def apply_limit() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_FSIZE, (max_bytes, max_bytes))

    return apply_limit


class PinnedSubprocessPredictionEngine:
    """Run a locally pinned executable through the Kinetics JSON file protocol."""

    execution_mode = "local"

    def __init__(
        self,
        *,
        executable_path: str,
        executable_sha256: str,
        weights_path: str,
        weights_sha256: str,
        model_name: str,
        model_version: str,
        model_license: str,
        engine_id: str,
        software_version: str,
        node_id: str,
        run_id: str,
        timeout_seconds: int = 1800,
        max_executable_bytes: int = 512 * 1024 * 1024,
        max_weights_bytes: int = 16 * 1024 * 1024 * 1024,
        max_response_bytes: int = 32 * 1024 * 1024,
    ) -> None:
        for name, value in (
            ("timeout_seconds", timeout_seconds),
            ("max_executable_bytes", max_executable_bytes),
            ("max_weights_bytes", max_weights_bytes),
            ("max_response_bytes", max_response_bytes),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        for text_name, text_value in (
            ("model_name", model_name),
            ("model_version", model_version),
            ("model_license", model_license),
            ("engine_id", engine_id),
            ("software_version", software_version),
            ("node_id", node_id),
            ("run_id", run_id),
        ):
            if not isinstance(text_value, str) or not text_value.strip():
                raise ValueError(f"{text_name} must be non-empty text")
        for digest_name, digest_value in (
            ("executable_sha256", executable_sha256),
            ("weights_sha256", weights_sha256),
        ):
            if (
                not isinstance(digest_value, str)
                or len(digest_value) != 64
                or any(char not in "0123456789abcdef" for char in digest_value)
            ):
                raise ValueError(f"{digest_name} must be lowercase SHA-256 hex")
        self.executable_path = str(Path(executable_path).expanduser().resolve(strict=True))
        self.weights_path = str(Path(weights_path).expanduser().resolve(strict=True))
        executable = Path(self.executable_path)
        weights = Path(self.weights_path)
        if not executable.is_file() or not os.access(executable, os.X_OK):
            raise ValueError("Prediction executable must be an executable regular file")
        if not weights.is_file():
            raise ValueError("Prediction weights must be a regular file")
        self.executable_sha256 = executable_sha256
        self.weights_sha256 = weights_sha256
        self.model_provenance = {
            "name": model_name,
            "version": model_version,
            "weights_sha256": weights_sha256,
            "license": model_license,
        }
        self.engine_id = engine_id
        self.software_version = software_version
        self.node_provenance = {
            "node_id": node_id,
            "software_version": software_version,
            "run_id": run_id,
        }
        self.timeout_seconds = timeout_seconds
        self.max_executable_bytes = max_executable_bytes
        self.max_weights_bytes = max_weights_bytes
        self.max_response_bytes = max_response_bytes
        if _file_sha256(executable, max_bytes=max_executable_bytes) != executable_sha256:
            raise ValueError("Prediction executable SHA-256 does not match approved digest")
        if _file_sha256(weights, max_bytes=max_weights_bytes) != weights_sha256:
            raise ValueError("Prediction weights SHA-256 does not match approved digest")

    def predict(self, sequence: str) -> dict[str, object]:
        executable = Path(self.executable_path)
        weights = Path(self.weights_path)
        if _file_sha256(executable, max_bytes=self.max_executable_bytes) != self.executable_sha256:
            raise ValueError("Prediction executable changed after approval")
        if _file_sha256(weights, max_bytes=self.max_weights_bytes) != self.weights_sha256:
            raise ValueError("Prediction weights changed after approval")
        with tempfile.TemporaryDirectory(prefix="kinetics-s4-") as directory:
            work = Path(directory)
            request_path = work / "request.json"
            response_path = work / "response.json"
            request_path.write_text(
                json.dumps({
                    "schema": "kinetics.local-prediction-request.v1",
                    "sequence": sequence,
                    "model": self.model_provenance,
                    "node": self.node_provenance,
                }, separators=(",", ":"), allow_nan=False),
                encoding="utf-8",
            )
            try:
                completed = subprocess.run(
                    [
                        str(executable),
                        "--kinetics-request", str(request_path),
                        "--kinetics-response", str(response_path),
                        "--weights", str(weights),
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
                    timeout=self.timeout_seconds,
                    check=False,
                    shell=False,
                    preexec_fn=_file_size_limit(self.max_response_bytes),
                )
            except subprocess.TimeoutExpired as exc:
                raise TimeoutError("Local prediction engine exceeded timeout_seconds") from exc
            if completed.returncode != 0:
                raise RuntimeError(
                    f"Local prediction engine exited with status {completed.returncode}"
                )
            if not response_path.is_file():
                raise RuntimeError("Local prediction engine did not write response.json")
            try:
                with response_path.open("rb") as response_handle:
                    response_bytes = response_handle.read(self.max_response_bytes + 1)
                if len(response_bytes) > self.max_response_bytes:
                    raise ValueError("Prediction response exceeds max_response_bytes")
                envelope = json.loads(response_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ValueError("Prediction engine returned invalid UTF-8 JSON") from exc
            if not isinstance(envelope, dict):
                raise ValueError("Prediction engine response must be a JSON object")
            return envelope


def run_pinned_local_prediction(
    sequence: str,
    engine: PinnedSubprocessPredictionEngine,
    *,
    max_residues: int = 100_000,
    max_payload_bytes: int = 32 * 1024 * 1024,
) -> dict[str, object]:
    """Execute and validate a hash-pinned local prediction process."""
    return run_local_structure_prediction(
        sequence,
        engine,
        max_residues=max_residues,
        max_payload_bytes=max_payload_bytes,
    )
