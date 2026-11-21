"""Optional Biopython adapter contract tests; deterministic software checks only."""
import pytest

from molecularis.alignment_biopython import align_pairwise_biopython


def test_biopython_pairwise_adapter_returns_molecularis_primitives() -> None:
    pytest.importorskip("Bio")
    result = align_pairwise_biopython(
        "ACGT", "ACCT", match_score=2, mismatch_score=-1,
        gap_open_score=-5, gap_extend_score=-1,
    )
    assert result["schema_version"] == 1
    assert result["engine"] == "biopython.PairwiseAligner"
    assert result["mode"] == "global"
    assert result["score"] == pytest.approx(5.0)
    assert isinstance(result["coordinates"], list)
    assert result["sequence_lengths"] == [4, 4]


def test_biopython_pairwise_adapter_validates_limits_and_scoring() -> None:
    with pytest.raises(ValueError, match="mode"):
        align_pairwise_biopython("AC", "AG", mode="semiglobal")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="gap scores"):
        align_pairwise_biopython("AC", "AG", gap_open_score=1)
    with pytest.raises(ValueError, match="max_sequence_length"):
        align_pairwise_biopython("AC", "AG", max_sequence_length=1)
    with pytest.raises(ValueError, match="non-empty"):
        align_pairwise_biopython("", "AG")
    with pytest.raises(ValueError, match="max_alignment_cells"):
        align_pairwise_biopython("A" * 10, "A" * 10, max_alignment_cells=100)
