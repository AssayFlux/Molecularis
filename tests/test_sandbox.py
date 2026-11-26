from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from molecularis.platform.contracts import ValidationError
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
    nested = source / "nested"
    nested.mkdir()
    with pytest.raises(ValidationError, match="nested"):
        runner._command(
            "registry.example/tool@sha256:" + "b" * 64,
            ("tool",), source, nested, tmp_path / "cid",
        )


def test_sandbox_runner_invokes_runtime_without_shell(tmp_path, monkeypatch):
    source = tmp_path / "input"
    target = tmp_path / "output"
    source.mkdir()
    target.mkdir()
    monkeypatch.setattr("molecularis.sandbox.shutil.which", lambda name: "/usr/bin/docker")
    observed = {}

    class FakeProcess:
        pid = 12345

        def __init__(self, command, **kwargs):
            observed["command"] = command
            observed["kwargs"] = kwargs

        def wait(self, timeout=None):
            return 0

        def poll(self):
            return 0

    monkeypatch.setattr("molecularis.sandbox.subprocess.Popen", FakeProcess)
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
    assert observed["kwargs"]["start_new_session"] is True


def test_sandbox_policy_rejects_unbounded_limits():
    with pytest.raises(ValueError):
        SandboxPolicy(max_wall_seconds=0)
    with pytest.raises(ValueError):
        SandboxPolicy(memory_mb=32)
    with pytest.raises(ValueError):
        SandboxPolicy(pids=0)


def test_sandbox_timeout_kills_client_process_group_and_removes_container(tmp_path, monkeypatch):
    source = tmp_path / "input"
    target = tmp_path / "output"
    source.mkdir()
    target.mkdir()
    monkeypatch.setattr("molecularis.sandbox.shutil.which", lambda name: "/usr/bin/docker")
    observed = {"waits": 0, "signals": [], "commands": []}

    class FakeProcess:
        pid = 23456

        def __init__(self, command, **kwargs):
            self.command = command
            self.cidfile = Path(command[command.index("--cidfile") + 1])
            self.cidfile.write_text("container123", encoding="utf-8")

        def poll(self):
            return None if observed["waits"] == 0 else -9

        def wait(self, timeout=None):
            observed["waits"] += 1
            if observed["waits"] == 1:
                raise subprocess.TimeoutExpired(self.command, timeout)
            return -9

    def fake_killpg(pid, sig):
        observed["signals"].append((pid, sig))

    def fake_run(command, **kwargs):
        observed["commands"].append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr("molecularis.sandbox.subprocess.Popen", FakeProcess)
    monkeypatch.setattr("molecularis.sandbox.os.killpg", fake_killpg)
    monkeypatch.setattr("molecularis.sandbox.subprocess.run", fake_run)
    from molecularis.platform.contracts import ResourceLimitError
    with pytest.raises(ResourceLimitError, match="wall-time"):
        OCIContainerRunner(policy=SandboxPolicy(max_wall_seconds=1)).run(
            image="registry.example/tool@sha256:" + "d" * 64,
            argv=("tool",), input_dir=source, output_dir=target,
        )
    assert observed["signals"]
    assert observed["commands"] == [["/usr/bin/docker", "rm", "-f", "container123"]]
