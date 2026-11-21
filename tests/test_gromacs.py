from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from molecularis.gromacs import run_gromacs


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fake_gmx(path: Path) -> Path:
    path.write_text(
        "#!/usr/bin/env python3\n"
        "import pathlib, sys\n"
        "if len(sys.argv) > 1 and sys.argv[1] == '--version':\n"
        " print('GROMACS version 2026.1'); raise SystemExit(0)\n"
        "prefix = pathlib.Path(sys.argv[sys.argv.index('-deffnm') + 1])\n"
        "pathlib.Path(str(prefix) + '.xtc').write_bytes(b'trajectory')\n"
        "pathlib.Path(str(prefix) + '.edr').write_bytes(b'energy')\n"
    )
    path.chmod(0o755)
    return path


def _kwargs(tmp_path: Path) -> dict[str, object]:
    tpr = tmp_path / "prepared.tpr"
    tpr.write_bytes(b"prepared simulation input")
    exe = _fake_gmx(tmp_path / "gmx")
    return {
        "tpr_path": tpr,
        "output_directory": tmp_path / "run",
        "executable_path": exe,
        "executable_sha256": _sha(exe),
        "tpr_sha256": _sha(tpr),
        "force_field_manifest": {
            "name": "explicit-test-force-field", "version": "1",
            "parameter_source_sha256": "a" * 64,
        },
        "run_id": "test-run-001",
        "threads": 2,
    }


def test_gromacs_execution_returns_hashed_molecularis_artifacts(tmp_path: Path) -> None:
    result = run_gromacs(**_kwargs(tmp_path))
    assert result["schema"] == "molecularis.gromacs-run.v1"
    assert result["execution_status"] == "completed"
    assert result["scientific_validation"] == "not_assessed"
    assert {item["name"] for item in result["artifacts"]} == {"molecularis.xtc", "molecularis.edr"}
    assert result["engine_version"] == "GROMACS version 2026.1"


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("threads", 0, "threads"),
        ("timeout_seconds", 0, "timeout_seconds"),
        ("tpr_sha256", "bad", "tpr_sha256"),
        ("extra_mdrun_args", ["-maxh", "1"], "extra_mdrun_args"),
        ("force_field_manifest", {}, "force_field_manifest"),
    ],
)
def test_gromacs_rejects_invalid_execution_contract(
    tmp_path: Path, key: str, value: object, message: str,
) -> None:
    kwargs = _kwargs(tmp_path)
    kwargs[key] = value
    with pytest.raises(ValueError, match=message):
        run_gromacs(**kwargs)


def test_gromacs_rejects_tpr_digest_mismatch(tmp_path: Path) -> None:
    kwargs = _kwargs(tmp_path)
    kwargs["tpr_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="TPR SHA-256"):
        run_gromacs(**kwargs)


def test_gromacs_requires_fresh_output_directory(tmp_path: Path) -> None:
    kwargs = _kwargs(tmp_path)
    Path(kwargs["output_directory"]).mkdir()
    with pytest.raises(ValueError, match="new directory"):
        run_gromacs(**kwargs)
