from __future__ import annotations

import pytest

from molecularis.genome_qc import summarize_contigs
from molecularis.sequence import SequenceRecord


def test_contig_qc_reports_n50_gc_and_ambiguity() -> None:
    result = summarize_contigs([
        SequenceRecord("c1", "GGCC"),
        SequenceRecord("c2", "ATNN"),
        SequenceRecord("c3", "A"),
    ])
    assert result["contig_count"] == 3
    assert result["total_bases"] == 9
    assert result["n50"] == 4
    assert result["l50"] == 2
    assert result["gc_fraction"] == pytest.approx(4 / 7)
    assert result["ambiguous_bases"] == 2
    assert result["n_bases"] == 2


def test_contig_qc_is_incremental_and_rejects_duplicate_or_invalid_contigs() -> None:
    def records():
        yield SequenceRecord("a", "ACGT")
        yield SequenceRecord("b", "NNNN")

    result = summarize_contigs(records(), max_records=2)
    assert result["total_bases"] == 8
    with pytest.raises(ValueError, match="unique"):
        summarize_contigs([SequenceRecord("a", "ACGT"), SequenceRecord("a", "TTTT")])
    with pytest.raises(ValueError, match="Invalid symbols"):
        summarize_contigs([SequenceRecord("bad", "ACGT-")])


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"max_records": True}, "max_records"),
        ({"max_total_bases": 1.5}, "max_total_bases"),
        ({"min_contig_length": 0}, "min_contig_length"),
    ],
)
def test_contig_qc_rejects_invalid_limits(kwargs, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        summarize_contigs([SequenceRecord("a", "ACGT")], **kwargs)
