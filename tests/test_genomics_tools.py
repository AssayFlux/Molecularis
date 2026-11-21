from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from molecularis import genomics_tools


class _FakeCommand:
    def __init__(self, output_index: bool = False) -> None:
        self.calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        self.output_index = output_index

    def __call__(self, *args: object, **kwargs: object) -> str | None:
        self.calls.append((args, kwargs))
        if kwargs.get("catch_stdout") is False:
            if self.output_index:
                source = Path(str(args[-1]))
                Path(str(source) + ".bai").write_bytes(b"index")
            elif "-o" in args:
                Path(str(args[args.index("-o") + 1])).write_bytes(b"processed")
            return None
        return "10 + 0 in total (QC-passed reads + QC-failed reads)\n"


def _fake_pysam(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    samtools = SimpleNamespace()
    for name in ("view", "sort", "index", "flagstat"):
        setattr(samtools, name, _FakeCommand(output_index=name == "index"))
    bcftools = SimpleNamespace(norm=_FakeCommand())
    fake = SimpleNamespace(
        samtools=samtools, bcftools=bcftools,
        __samtools_version__="1.22", __bcftools_version__="1.22",
    )
    monkeypatch.setattr(genomics_tools, "_pysam", lambda: fake)
    return fake


def test_samtools_view_records_input_and_output_provenance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_pysam(monkeypatch)
    source = tmp_path / "reads.sam"
    source.write_text("@HD\\tVN:1.6\\n")
    target = tmp_path / "reads.bam"

    result = genomics_tools.samtools_view(source, target, output_format="bam", threads=2)

    assert result["engine"] == "samtools"
    assert result["operation"] == "view"
    assert result["scientific_validation"] == "not_assessed"
    assert result["output"]["sha256"]
    args, kwargs = fake.samtools.view.calls[0]
    assert "-b" in args and "-@" in args and kwargs["catch_stdout"] is False


def test_samtools_sort_index_and_flagstat_are_fixed_operations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_pysam(monkeypatch)
    source = tmp_path / "reads.bam"
    source.write_bytes(b"bam")

    sorted_result = genomics_tools.samtools_sort(source, tmp_path / "sorted.bam")
    indexed_result = genomics_tools.samtools_index(source)
    stats = genomics_tools.samtools_flagstat(source)

    assert sorted_result["operation"] == "sort"
    assert indexed_result["operation"] == "index"
    assert indexed_result["output"]["path"].endswith(".bai")
    assert "in total" in stats["report"]
    assert len(fake.samtools.sort.calls) == 1
    assert len(fake.samtools.index.calls) == 1
    assert len(fake.samtools.flagstat.calls) == 1


def test_bcftools_normalization_requires_and_hashes_explicit_reference(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _fake_pysam(monkeypatch)
    source = tmp_path / "input.vcf"
    reference = tmp_path / "reference.fa"
    source.write_text("##fileformat=VCFv4.3\\n")
    reference.write_text(">chr1\\nACGT\\n")
    target = tmp_path / "normalized.vcf.gz"

    result = genomics_tools.bcftools_normalize(source, reference, target)

    assert result["engine"] == "bcftools"
    assert result["operation"] == "norm"
    assert result["reference"]["sha256"]
    assert result["parameters"]["split_multiallelic"] is True
    args, kwargs = fake.bcftools.norm.calls[0]
    assert "-f" in args and str(reference.resolve()) in args
    assert "-m" in args and "-any" in args
    assert kwargs["catch_stdout"] is False


def test_genomics_tools_reject_unsafe_or_ambiguous_paths_and_modes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _fake_pysam(monkeypatch)
    source = tmp_path / "reads.sam"
    source.write_text("input")
    with pytest.raises(ValueError, match="output_format"):
        genomics_tools.samtools_view(source, tmp_path / "out", output_format="guess")
    with pytest.raises(ValueError, match="local reference"):
        genomics_tools.samtools_view(source, tmp_path / "out.cram", output_format="cram")
    with pytest.raises(ValueError, match="new path"):
        genomics_tools.samtools_sort(source, source)
    with pytest.raises(ValueError, match="threads"):
        genomics_tools.samtools_sort(source, tmp_path / "sorted.bam", threads=0)
    with pytest.raises(ValueError, match="BAM or CRAM"):
        genomics_tools.samtools_index(source)


def test_genomics_tools_enforce_file_size_limits(tmp_path: Path) -> None:
    source = tmp_path / "large.sam"
    source.write_bytes(b"12345")
    with pytest.raises(ValueError, match="byte limit"):
        genomics_tools.samtools_flagstat(source, max_input_bytes=4)
