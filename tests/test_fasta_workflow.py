from __future__ import annotations

import pytest

from molecularis.workflows import analyze_fasta_text


def test_fasta_workflow_reports_multiple_records_and_ambiguous_symbols() -> None:
    result = analyze_fasta_text(">one sample\nACGTGCNN\n>two\nGGCC\n")
    assert result["record_count"] == 2
    assert result["total_bases"] == 12
    assert result["gc_denominator"] == "all sequence symbols"
    assert result["records"] == [
        {
            "identifier": "one",
            "description": "sample",
            "length": 8,
            "gc_percent": 50.0,
            "ambiguous_count": 2,
        },
        {
            "identifier": "two",
            "description": "",
            "length": 4,
            "gc_percent": 100.0,
            "ambiguous_count": 0,
        },
    ]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"max_chars": 0}, "max_chars"),
        ({"max_records": True}, "max_records"),
        ({"max_bases": 1.5}, "max_bases"),
    ],
)
def test_fasta_workflow_requires_positive_integer_limits(kwargs, message) -> None:
    with pytest.raises(ValueError, match=message):
        analyze_fasta_text(">x\nACGT\n", **kwargs)


def test_fasta_workflow_enforces_character_record_and_base_limits() -> None:
    with pytest.raises(ValueError, match="character limit"):
        analyze_fasta_text(">x\nACGT\n", max_chars=3)
    with pytest.raises(ValueError, match="record limit"):
        analyze_fasta_text(">x\nA\n>y\nC\n", max_records=1)
    with pytest.raises(ValueError, match="total-base limit"):
        analyze_fasta_text(">x\nACGT\n", max_bases=3)


def test_fasta_workflow_rejects_non_text_input() -> None:
    with pytest.raises(TypeError, match="must be text"):
        analyze_fasta_text(None)  # type: ignore[arg-type]


def test_fastq_workflow_reports_quality_with_explicit_phred_offset() -> None:
    from molecularis.workflows import analyze_fastq_text
    text = "@r1 sample\nACGT\n+\nIIII\n@r2\nGG\n+\n!!\n"
    result = analyze_fastq_text(text, phred_offset=33)
    assert result["record_count"] == 2
    assert result["total_bases"] == 6
    assert result["phred_offset"] == 33
    assert result["mean_phred"] == 26.667
    assert result["q20_fraction"] == 0.666667
    assert result["q30_fraction"] == 0.666667
    assert result["reads"][0]["identifier"] == "r1"
    assert result["reads"][0]["length"] == 4


def test_fastq_workflow_requires_explicit_phred_offset() -> None:
    from molecularis.workflows import analyze_fastq_text
    with pytest.raises(ValueError, match="explicit Phred offset"):
        analyze_fastq_text("@r\nA\n+\n!\n", phred_offset=0)


def test_fastq_workflow_rejects_invalid_quality_length_and_limits() -> None:
    from molecularis.workflows import analyze_fastq_text
    with pytest.raises(ValueError, match="length mismatch"):
        analyze_fastq_text("@r\nAC\n+\n!\n", phred_offset=33)
    with pytest.raises(ValueError, match="record limit"):
        analyze_fastq_text("@r1\nA\n+\n!\n@r2\nC\n+\n!\n",
                           phred_offset=33, max_records=1)
    with pytest.raises(ValueError, match="total-base limit"):
        analyze_fastq_text("@r\nAC\n+\n!!\n", phred_offset=33, max_bases=1)
