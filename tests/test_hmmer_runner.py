from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from molecularis.hmmer_runner import (
    hash_pressed_profile_pack,
    press_local_hmm_profile,
    run_local_hmmscan,
)


PACK_BASE = {
    "name": "synthetic-profile-pack",
    "version": "1",
    "license": "CC0-1.0",
    "source": "https://example.org/profiles",
}


def _artifacts(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    executable = tmp_path / "hmmscan"
    executable.write_bytes(b"synthetic hmmscan executable")
    executable.chmod(0o755)
    profile = tmp_path / "profiles.hmm"
    profile.write_text("HMMER3/f\nsynthetic profile\n", encoding="ascii")
    for suffix in (".h3m", ".h3i", ".h3f", ".h3p"):
        Path(str(profile) + suffix).write_bytes(("pressed" + suffix).encode("ascii"))
    pack = {
        **PACK_BASE,
        "content_sha256": hash_pressed_profile_pack(str(profile)),
    }
    return executable, profile, pack


def test_local_hmmscan_pins_binary_and_profile_and_parses_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    executable, profile, pack = _artifacts(tmp_path)
    row = (
        "PF00001 PF00001.1 100 query-1 - 80 1e-20 72.5 0.1 1 1 "
        "1e-18 1e-18 70.0 0.0 5 75 3 73 2 75 0.98 kinase-like domain\n"
    )

    def fake_run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        if "-h" in args:
            return subprocess.CompletedProcess(args, 0, b"# HMMER 3.4 (fixture)\n", b"")
        output_index = args.index("--domtblout") + 1
        Path(args[output_index]).write_text(row, encoding="utf-8")
        return subprocess.CompletedProcess(args, 0, b"", b"")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = run_local_hmmscan(
        ">query-1\n" + "A" * 80 + "\n",
        executable_path=str(executable),
        executable_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(),
        profile_path=str(profile),
        profile_pack=pack,
    )
    assert result["execution_mode"] == "local"
    assert result["evidence"]["domain_hit_count"] == 1
    assert result["profile_pack_sha256"] == pack["content_sha256"]


def test_local_hmmscan_rejects_unpinned_executable_and_profile(
    tmp_path: Path,
) -> None:
    executable, profile, pack = _artifacts(tmp_path)
    with pytest.raises(ValueError, match="executable SHA-256"):
        run_local_hmmscan(
            ">q\nAAAA\n",
            executable_path=str(executable),
            executable_sha256="0" * 64,
            profile_path=str(profile),
            profile_pack=pack,
        )
    with pytest.raises(ValueError, match="profile-pack SHA-256"):
        run_local_hmmscan(
            ">q\nAAAA\n",
            executable_path=str(executable),
            executable_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(),
            profile_path=str(profile),
            profile_pack={**pack, "content_sha256": "a" * 64},
        )


def test_local_hmmscan_rejects_input_and_limit_errors(tmp_path: Path) -> None:
    executable, profile, pack = _artifacts(tmp_path)
    digest = hashlib.sha256(executable.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="FASTA"):
        run_local_hmmscan(
            "AAAA",
            executable_path=str(executable),
            executable_sha256=digest,
            profile_path=str(profile),
            profile_pack=pack,
        )
    with pytest.raises(ValueError, match="timeout_seconds"):
        run_local_hmmscan(
            ">q\nAAAA",
            executable_path=str(executable),
            executable_sha256=digest,
            profile_path=str(profile),
            profile_pack=pack,
            timeout_seconds=0,
        )



def test_pressed_profile_pack_requires_all_index_files(tmp_path: Path) -> None:
    profile = tmp_path / "profiles.hmm"
    profile.write_text("HMMER3/f\\n", encoding="ascii")
    with pytest.raises(ValueError, match="missing"):
        hash_pressed_profile_pack(str(profile))



def test_pinned_hmmpress_builds_complete_profile_pack(tmp_path: Path) -> None:
    import sys

    profile = tmp_path / "profiles.hmm"
    profile.write_text("HMMER3/f\nsynthetic profile\n", encoding="ascii")
    executable = tmp_path / "hmmpress.py"
    executable.write_text(
        "#!" + sys.executable + "\n"
        "import pathlib, sys\n"
        "profile=pathlib.Path(sys.argv[-1])\n"
        "for suffix in ('.h3m','.h3i','.h3f','.h3p'):\n"
        " pathlib.Path(str(profile)+suffix).write_bytes(('index'+suffix).encode())\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    result = press_local_hmm_profile(
        hmmpress_executable_path=str(executable),
        hmmpress_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(),
        profile_path=str(profile),
        source_hmm_sha256=hashlib.sha256(profile.read_bytes()).hexdigest(),
        profile_name="fixture",
        profile_version="1",
        profile_license="CC0-1.0",
        profile_source="https://example.org/fixture",
    )
    assert result["profile_pack"]["content_sha256"] == hash_pressed_profile_pack(
        str(profile)
    )
