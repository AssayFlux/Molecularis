from __future__ import annotations

import pytest

from molecularis.genome_orf import scan_contig_orf_candidates
from molecularis.sequence import SequenceRecord


def test_genome_orf_scan_aggregates_contigs_and_preserves_coordinates() -> None:
    result = scan_contig_orf_candidates(
        [SequenceRecord("c1", "ATGAAATAA"), SequenceRecord("c2", "ATGCCCTAA")],
        table_id=1,
        min_protein_length=1,
    )
    assert result["contig_count"] == 2
    assert result["total_orf_candidates"] == 2
    assert result["conclusion"] == "candidate_orfs_only_not_gene_annotation"
    assert result["contigs"][0]["orfs"][0]["start"] == 0


def test_genome_orf_scan_enforces_aggregate_candidate_work_budget() -> None:
    with pytest.raises(ValueError, match="candidate work"):
        scan_contig_orf_candidates(
            [SequenceRecord("c1", "ATGATGTAA")],
            table_id=1,
            min_protein_length=1,
            max_candidate_pairs_total=1,
        )


def test_genome_orf_scan_rejects_duplicate_contigs_and_bad_limits() -> None:
    with pytest.raises(ValueError, match="unique"):
        scan_contig_orf_candidates([
            SequenceRecord("c1", "ATGAAATAA"),
            SequenceRecord("c1", "ATGAAATAA"),
        ], table_id=1, min_protein_length=1)
    with pytest.raises(ValueError, match="positive integer"):
        scan_contig_orf_candidates(
            [SequenceRecord("c1", "ATGAAATAA")], max_contigs=True,
        )
