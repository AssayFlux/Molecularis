from __future__ import annotations

import subprocess

import pytest

from molecularis.platform.contracts import ResourceLimitError, ValidationError
from molecularis.sandbox import OCIContainerRunner, SandboxPolicy


def test_sandbox_command_is_digest_pinned_and_restrictive(tmp_path):
    source = tmp_path / "input"
    target = tmp_path / "output"
    source.mkdir()
    target.mkdir()
    runner = OCIContainerRunner(policy=SandboxPolicy(max_wall_seconds=7, memory_mb=512))
    command = runner._command(
        "registry.example/tool@sha256:" + "a" * 64,
        ("python", "/tool/run.py", "--input", "/input/data.json"),
        source, target, tmp_path / "container.id",
    )
    assert "--network=none" in command
    assert "--read-only" in command
    assert "--cap-drop=ALL" in command
    assert "--security-opt=no-new-privileges" in command
    assert "--pids-limit" in command
    assert "--memory" in command
    assert "--cpus" in command
    assert "--pull=never" in command
    assert command[-4:] == [
        "registry.example/tool@sha256:" + "a" * 64,
        "python", "/tool/run.py", "--input", "/input/data.json",
    ][-4:]


def test_sandbox_rejects_mutable_images_and_shell_strings(tmp_path):
    source = tmp_path / "input"
    target = tmp_path / "output"
    source.mkdir()
    target.mkdir()
    runner = OCIContainerRunner()
    with pytest.raises(ValidationError, match="sha256"):
        runner._command("latest", ("tool",), source, target, tmp_path / "cid")
    with pytest.raises(ValidationError, match="argv"):
        runner._command(
            "registry.example/tool@sha256:" + "b" * 64,
            (), source, target, tmp_path / "cid",
        )
    with pytest.raises(ValidationError, match="nested"):
        runner._command(
            "registry.example/tool@sha256:" + "b" * 64,
            ("tool",), source, source / "nested", tmp_path / "cid",
        )


def test_sandbox_runner_invokes_runtime_without_shell(tmp_path, monkeypatch):
    source = tmp_path / "input"
    target = tmp_path / "output"
    source.mkdir()
    target.mkdir()
    monkeypatch.setattr("molecularis.sandbox.shutil.which", lambda name: "/usr/bin/docker")
    observed = {}

    def fake_run(command, **kwargs):
        observed["command"] = command
        observed["kwargs"] = kwargs
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr("molecularis.sandbox.subprocess.run", fake_run)
    result = OCIContainerRunner().run(
        image="registry.example/tool@sha256:" + "c" * 64,
        argv=("tool", "--input", "/input/a"),
        input_dir=source, output_dir=target,
    )
    assert result.exit_code == 0
    assert observed["command"][0] == "/usr/bin/docker"
    assert "shell" not in observed["kwargs"]
    assert observed["kwargs"]["stdin"] == subprocess.DEVNULL
    assert observed["kwargs"]["stdout"] == subprocess.DEVNULL
    assert observed["kwargs"]["stderr"] == subprocess.DEVNULL


def test_sandbox_policy_rejects_unbounded_limits():
    with pytest.raises(ValueError):
        SandboxPolicy(max_wall_seconds=0)
    with pytest.raises(ValueError):
        SandboxPolicy(memory_mb=32)
    with pytest.raises(ValueError):
        SandboxPolicy(pids=0)
