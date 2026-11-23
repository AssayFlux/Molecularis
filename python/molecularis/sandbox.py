"""Opt-in OCI process isolation for untrusted scientific tools.

This adapter invokes a locally available Docker/Podman-compatible runtime using
an immutable image digest, no network, read-only root filesystem, dropped
capabilities, non-root UID/GID, and explicit CPU/memory/PID/time bounds.
It is not enabled implicitly by the in-process Rulebook executor.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import os
import re
import shutil
import subprocess
import tempfile
import time

from .platform.contracts import ValidationError, ResourceLimitError


_IMAGE_DIGEST = re.compile(r"^.+@sha256:[a-f0-9]{64}$")


@dataclass(frozen=True, slots=True)
class SandboxPolicy:
    max_wall_seconds: int = 120
    memory_mb: int = 2048
    cpus: float = 2.0
    pids: int = 128
    tmpfs_mb: int = 256

    def __post_init__(self) -> None:
        if not 1 <= self.max_wall_seconds <= 86_400:
            raise ValueError("max_wall_seconds must be in 1..86400")
        if not 64 <= self.memory_mb <= 1_048_576:
            raise ValueError("memory_mb must be in 64..1048576")
        if not 0.1 <= self.cpus <= 256:
            raise ValueError("cpus must be in 0.1..256")
        if not 1 <= self.pids <= 65_536:
            raise ValueError("pids must be in 1..65536")
        if not 16 <= self.tmpfs_mb <= self.memory_mb:
            raise ValueError("tmpfs_mb must be >=16 and <= memory_mb")


@dataclass(frozen=True, slots=True)
class SandboxResult:
    exit_code: int
    elapsed_seconds: float
    timed_out: bool
    output_directory: str


class OCIContainerRunner:
    """Run a pinned tool image with a deliberately narrow host interface."""

    def __init__(self, *, runtime: str = "docker", policy: SandboxPolicy | None = None) -> None:
        if runtime not in {"docker", "podman"}:
            raise ValueError("runtime must be docker or podman")
        self.runtime = runtime
        self.policy = policy or SandboxPolicy()

    def _command(
        self, image: str, argv: Sequence[str], input_dir: Path, output_dir: Path,
        cidfile: Path,
    ) -> list[str]:
        if not isinstance(image, str) or not _IMAGE_DIGEST.fullmatch(image):
            raise ValidationError("sandbox image must be pinned by sha256 digest")
        if not argv or len(argv) > 256 or any(
            not isinstance(arg, str) or "\x00" in arg or len(arg) > 8192 for arg in argv
        ):
            raise ValidationError("sandbox argv must contain 1..256 bounded strings")
        if any(not arg for arg in argv):
            raise ValidationError("sandbox argv entries must not be empty")
        source = input_dir.resolve(strict=True)
        target = output_dir.resolve(strict=True)
        if not source.is_dir() or not target.is_dir() or source == target:
            raise ValidationError("sandbox input/output mounts must be distinct existing directories")
        if source in target.parents or target in source.parents:
            raise ValidationError("sandbox input and output directories must not be nested")
        policy = self.policy
        return [
            self.runtime, "run", "--rm", "--pull=never", "--cidfile", str(cidfile),
            "--network=none", "--read-only", "--cap-drop=ALL",
            "--security-opt=no-new-privileges", "--pids-limit", str(policy.pids),
            "--memory", f"{policy.memory_mb}m", "--cpus", str(policy.cpus),
            "--ipc=private", "--user", f"{os.getuid()}:{os.getgid()}",
            "--workdir", "/work",
            "--tmpfs", f"/tmp:rw,noexec,nosuid,nodev,size={policy.tmpfs_mb}m",
            "--mount", f"type=bind,src={source},dst=/input,readonly",
            "--mount", f"type=bind,src={target},dst=/output",
            image, *argv,
        ]

    def run(
        self, *, image: str, argv: Sequence[str], input_dir: str | Path,
        output_dir: str | Path,
    ) -> SandboxResult:
        executable = shutil.which(self.runtime)
        if executable is None:
            raise ValidationError(f"required OCI runtime is not installed: {self.runtime}")
        self.runtime = executable
        with tempfile.TemporaryDirectory(prefix="molecularis-sandbox-") as temp:
            cidfile = Path(temp) / "container.id"
            command = self._command(
                image, argv, Path(input_dir), Path(output_dir), cidfile
            )
            started = time.monotonic()
            timed_out = False
            exit_code = -1
            try:
                completed = subprocess.run(
                    command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, check=False,
                    timeout=self.policy.max_wall_seconds,
                    env={"PATH": os.defpath, "LANG": "C"},
                )
                exit_code = completed.returncode
            except subprocess.TimeoutExpired:
                timed_out = True
                if cidfile.exists():
                    container_id = cidfile.read_text(encoding="utf-8").strip()
                    if container_id and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{5,127}", container_id):
                        try:
                            subprocess.run(
                                [self.runtime, "rm", "-f", container_id],
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, check=False, timeout=10,
                                env={"PATH": os.defpath, "LANG": "C"},
                            )
                        except (subprocess.TimeoutExpired, OSError):
                            pass
                raise ResourceLimitError(
                    "sandbox execution exceeded wall-time budget",
                    details={"max_wall_seconds": self.policy.max_wall_seconds},
                )
            except OSError as exc:
                raise ValidationError("OCI runtime invocation failed") from exc
            return SandboxResult(
                exit_code=exit_code, elapsed_seconds=time.monotonic() - started,
                timed_out=timed_out, output_directory=str(Path(output_dir).resolve()),
            )
