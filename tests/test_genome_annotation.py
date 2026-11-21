from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

from molecularis.genome_annotation import run_pinned_local_gff3_annotator
from molecularis.sequence import SequenceRecord


def _annotator(tmp_path: Path, *, end: int = 9) -> tuple[Path, str]:
    executable = tmp_path / "annotator.py"
    gff3 = (
        "##gff-version 3\n"
        f"ctg1\ttest\tgene\t1\t{end}\t.\t+\t.\tID=g1\n"
    )
    script = "\n".join([
        "#!" + sys.executable,
        "import pathlib, sys",
        "args=sys.argv[1:]",
        "out=pathlib.Path(args[args.index('--kinetics-output-gff3')+1])",
        f"out.write_text({gff3!r})",
    ])
    executable.write_text(script + "\n", encoding="utf-8")
    executable.chmod(0o755)
    return executable, hashlib.sha256(executable.read_bytes()).hexdigest()


def test_local_annotator_runs_and_validates_gff3_against_input_contig(
    tmp_path: Path,
) -> None:
    executable, digest = _annotator(tmp_path)
    result = run_pinned_local_gff3_annotator(
        [SequenceRecord("ctg1", "ATGAAATAA")],
        executable_path=str(executable),
        executable_sha256=digest,
        annotator_id="synthetic",
        annotator_version="1",
    )
    assert result["annotation"]["feature_count"] == 1
    assert result["conclusion"] == "syntax_and_coordinate_validated_gene_caller_output"


def test_local_annotator_rejects_hash_mismatch_and_out_of_bounds_feature(
    tmp_path: Path,
) -> None:
    executable, _ = _annotator(tmp_path)
    with pytest.raises(ValueError, match="SHA-256"):
        run_pinned_local_gff3_annotator(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256="0" * 64,
            annotator_id="synthetic",
            annotator_version="1",
        )
    executable, digest = _annotator(tmp_path, end=99)
    with pytest.raises(ValueError, match="beyond supplied contig"):
        run_pinned_local_gff3_annotator(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256=digest,
            annotator_id="synthetic",
            annotator_version="1",
        )
