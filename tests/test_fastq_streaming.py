from __future__ import annotations

import pytest

from molecularis.sequence import iter_fastq_records


def test_streaming_fastq_handles_wrapped_records_and_limits() -> None:
    text = "@r1 description\nAC\nGT\n+r1\nII\nII\n@r2\nNN\n+\n!!\n"
    records = list(iter_fastq_records(text.splitlines(), max_records=2, max_total_bases=6))
    assert [(record.identifier, record.sequence, quality) for record, quality in records] == [
        ("r1", "ACGT", "IIII"), ("r2", "NN", "!!"),
    ]


def test_streaming_fastq_rejects_mismatched_quality_and_invalid_bases() -> None:
    with pytest.raises(ValueError, match="sequence/quality length"):
        list(iter_fastq_records(["@r1", "ACGT", "+", "III"]))
    with pytest.raises(ValueError, match="Invalid symbols"):
        list(iter_fastq_records(["@r1", "ACX", "+", "III"]))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_records": 0},
        {"max_total_bases": True},
        {"max_record_bases": 0},
    ],
)
def test_streaming_fastq_rejects_invalid_limits(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        list(iter_fastq_records(["@r1", "A", "+", "!"], **kwargs))


def test_streaming_fastq_rejects_plus_identifier_mismatch() -> None:
    with pytest.raises(ValueError, match="separator identifier mismatch"):
        list(iter_fastq_records(["@r1", "AC", "+r2", "!!"]))
