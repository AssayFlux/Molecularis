from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

from molecularis.augustus import hash_augustus_species_model, run_local_augustus
from molecularis.sequence import SequenceRecord


def _fixtures(tmp_path: Path, *, end: int = 9) -> tuple[Path, Path, str, str]:
    config = tmp_path / "augustus-config"
    species_dir = config / "species" / "fixture_species"
    species_dir.mkdir(parents=True, exist_ok=True)
    (species_dir / "parameters.cfg").write_text("synthetic model", encoding="utf-8")
    executable = tmp_path / "augustus.py"
    gff = (
        "##gff-version 3\n"
        f"ctg1\tAUGUSTUS\tgene\t1\t{end}\t.\t+\t.\tID=g1\n"
    )
    script = "\n".join([
        "#!" + sys.executable,
        "import pathlib, sys",
        "args=sys.argv[1:]",
        "out=pathlib.Path(args[2].split('=',1)[1])",
        f"out.write_text({gff!r})",
    ])
    executable.write_text(script + "\n", encoding="utf-8")
    executable.chmod(0o755)
    return (
        config,
        executable,
        hash_augustus_species_model(str(config), "fixture_species"),
        hashlib.sha256(executable.read_bytes()).hexdigest(),
    )


def test_pinned_augustus_runs_eukaryotic_gff3_pipeline(tmp_path: Path) -> None:
    config, executable, model_hash, executable_hash = _fixtures(tmp_path)
    result = run_local_augustus(
        [SequenceRecord("ctg1", "ATGAAATAA")],
        executable_path=str(executable),
        executable_sha256=executable_hash,
        config_path=str(config),
        species="fixture_species",
        species_model_sha256=model_hash,
        tool_version="fixture-1",
    )
    assert result["conclusion"] == "eukaryotic_gene_candidates_require_review"
    assert result["annotation"]["feature_count"] == 1


def test_augustus_rejects_model_tampering_and_out_of_bounds(
    tmp_path: Path,
) -> None:
    config, executable, model_hash, executable_hash = _fixtures(tmp_path)
    (config / "species" / "fixture_species" / "parameters.cfg").write_text(
        "tampered", encoding="utf-8",
    )
    with pytest.raises(ValueError, match="species-model SHA-256"):
        run_local_augustus(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256=executable_hash,
            config_path=str(config),
            species="fixture_species",
            species_model_sha256=model_hash,
            tool_version="fixture-1",
        )
    config, executable, model_hash, executable_hash = _fixtures(tmp_path, end=99)
    with pytest.raises(ValueError, match="beyond supplied contig"):
        run_local_augustus(
            [SequenceRecord("ctg1", "ATGAAATAA")],
            executable_path=str(executable),
            executable_sha256=executable_hash,
            config_path=str(config),
            species="fixture_species",
            species_model_sha256=model_hash,
            tool_version="fixture-1",
        )
