from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

from molecularis.prodigal import run_local_prodigal
from molecularis.sequence import SequenceRecord


def _prodigal(tmp_path: Path, *, end: int = 9) -> tuple[Path, str]:
    executable = tmp_path / "prodigal.py"
    gff = (
        "##gff-version 3\n"
        f"ctg1\tProdigal\tCDS\t1\t{end}\t.\t+\t0\tID=gene1\n"
    )
    script = "\n".join([
        "#!" + sys.executable,
        "import pathlib, sys",
        "args=sys.argv[1:]",
        "output=pathlib.Path(args[args.index('-o')+1])",
        f"output.write_text({gff!r})",
    ])
    executable.write_text(script + "\n", encoding="utf-8")
    executable.chmod(0o755)
    return executable, hashlib.sha256(executable.read_bytes()).hexdigest()


def test_pinned_prodigal_emits_coordinate_checked_candidates(tmp_path: Path) -> None:
    executable, digest = _prodigal(tmp_path)
    result = run_local_prodigal(
        [SequenceRecord("ctg1", "ATGAAATAA")],
        executable_path=str(executable),
        executable_sha256=digest,
        tool_version="fixture-1",
    )
    assert result["conclusion"] == "prokaryotic_gene_candidates_require_review"
    assert result["annotation"]["feature_count"] == 1


def test_prodigal_rejects_tampering_and_out_of_bounds_coordinates(
    tmp_path: Path,
) -> None:
    executable, _ = _prodigal(tmp_path)
    with pytest.raises(ValueError, match="SHA-256"):
        run_local_prodigal(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256="0" * 64,
            tool_version="fixture-1",
        )
    executable, digest = _prodigal(tmp_path, end=99)
    with pytest.raises(ValueError, match="beyond supplied contig"):
        run_local_prodigal(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256=digest,
            tool_version="fixture-1",
        )
