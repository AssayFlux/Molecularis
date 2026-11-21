from __future__ import annotations

import pytest

from molecularis.hmmer import parse_hmmscan_domtblout
from molecularis.hmmer_rank import rank_hmmer_domain_candidates


ROW = (
    "PF00001 PF00001.1 100 query-1 - 80 1e-20 72.5 0.1 1 1 "
    "1e-18 1e-18 70.0 0.0 5 75 3 73 2 75 0.98 kinase-like domain"
)
PACK = {
    "name": "fixture",
    "version": "1",
    "license": "CC0-1.0",
    "source": "https://example.org/fixture",
    "content_sha256": "a" * 64,
}


def _evidence() -> dict[str, object]:
    return parse_hmmscan_domtblout(
        [ROW], hmmer_version="3.4", profile_pack=PACK,
    )


def test_hmmer_domain_candidates_rank_with_explicit_thresholds() -> None:
    result = rank_hmmer_domain_candidates(
        _evidence(),
        max_independent_evalue=1e-5,
        min_profile_coverage=0.5,
        min_query_coverage=0.5,
        min_accuracy=0.8,
    )
    assert result["passing_candidate_count"] == 1
    assert result["candidates"][0]["rank"] == 1
    assert result["candidates"][0]["status"] == "passes_caller_thresholds"


def test_hmmer_domain_candidates_abstain_when_thresholds_fail() -> None:
    result = rank_hmmer_domain_candidates(
        _evidence(),
        max_independent_evalue=1e-30,
        min_profile_coverage=0.99,
        min_query_coverage=0.99,
        min_accuracy=0.99,
    )
    assert result["passing_candidate_count"] == 0
    assert result["candidates"][0]["rank"] is None
    assert result["conclusion"] == "no_profile_candidates_passed_caller_thresholds"


def test_hmmer_domain_candidates_reject_invalid_thresholds() -> None:
    with pytest.raises(ValueError, match="max_independent_evalue"):
        rank_hmmer_domain_candidates(
            _evidence(),
            max_independent_evalue=float("nan"),
            min_profile_coverage=0.5,
            min_query_coverage=0.5,
            min_accuracy=0.5,
        )
