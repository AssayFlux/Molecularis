from __future__ import annotations

import pytest

from molecularis import infer_genetic_code_candidates


def test_genetic_code_inference_ranks_table_that_avoids_internal_stops() -> None:
    records = [
        {"id": "cds-0", "sequence": "ATG" + "AAA" * 10 + "TGA" + "CCC" * 10 + "TAA",
         "complete_cds": True},
        {"id": "cds-1", "sequence": "ATG" + "AAG" * 10 + "TGA" + "CCG" * 10 + "TAA",
         "complete_cds": True},
        {"id": "cds-2", "sequence": "ATG" + "GCT" * 10 + "TGA" + "GCC" * 10 + "TAA",
         "complete_cds": True},
    ]
    result = infer_genetic_code_candidates(records, table_ids=[1, 4], min_codons=30, minimum_score_margin=0.02)
    assert result["status"] == "candidate_table_ranked"
    assert result["candidate_table_id"] == 4
    assert result["ranked_candidates"][0]["internal_stop_count"] == 0
    assert result["ranked_candidates"][1]["internal_stop_count"] == 3
    assert any("not an organism identification" in warning for warning in result["warnings"])


def test_genetic_code_inference_abstains_on_insufficient_or_tied_evidence() -> None:
    short = infer_genetic_code_candidates(
        [{"sequence": "ATGAAA"}, {"sequence": "ATGAAG"}],
        table_ids=[1, 4], min_codons=30,
    )
    assert short["status"] == "insufficient_evidence"
    assert short["candidate_table_id"] is None
    tied = infer_genetic_code_candidates(
        [
            {"id": "tie-a", "sequence": "ATG" + "AAA" * 20},
            {"id": "tie-b", "sequence": "ATG" + "AAG" * 20},
            {"id": "tie-c", "sequence": "ATG" + "GCT" * 20},
        ],
        table_ids=[1, 4], min_codons=30,
    )
    assert tied["status"] == "ambiguous_candidates"
    assert tied["candidate_table_id"] is None


@pytest.mark.parametrize("records", [
    [{"sequence": "ATGN"}],
    [{"sequence": "ATGA"}],
    [{"sequence": "ATG", "frame": True}],
    [{"sequence": "ATG", "complete_cds": 1}],
])
def test_genetic_code_inference_rejects_ambiguous_or_malformed_records(records) -> None:
    with pytest.raises(ValueError):
        infer_genetic_code_candidates(records)


def test_genetic_code_inference_enforces_limits_and_supported_tables() -> None:
    records = [{"sequence": "ATGAAA"}]
    with pytest.raises(ValueError, match="max_records"):
        infer_genetic_code_candidates(records * 2, max_records=1)
    with pytest.raises(ValueError, match="Unsupported"):
        infer_genetic_code_candidates(records, table_ids=[99])


def test_genetic_code_inference_rejects_duplicate_records_as_nonindependent() -> None:
    repeated = {"sequence": "ATG" + "AAA" * 20}
    with pytest.raises(ValueError, match="duplicate coding sequences"):
        infer_genetic_code_candidates([repeated, repeated, repeated])


def test_genetic_code_inference_requires_competing_candidate_tables() -> None:
    with pytest.raises(ValueError, match="At least two"):
        infer_genetic_code_candidates([{"sequence": "ATGAAA"}], table_ids=[1])


def test_genetic_code_inference_bounds_candidate_table_iterables() -> None:
    def endless_tables():
        while True:
            yield 1

    with pytest.raises(ValueError, match="exceeds the supported candidate-table bound"):
        infer_genetic_code_candidates([{"sequence": "ATGAAA"}], table_ids=endless_tables())


def test_genetic_code_inference_requires_distinct_start_and_terminal_codons() -> None:
    with pytest.raises(ValueError, match="distinct start and terminal"):
        infer_genetic_code_candidates(
            [{"sequence": "ATG", "complete_cds": True}], table_ids=[1, 4]
        )
