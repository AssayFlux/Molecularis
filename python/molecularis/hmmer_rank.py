"""Conservative thresholded ranking of HMMER profile-domain evidence."""
from __future__ import annotations

import math
from typing import Any


def rank_hmmer_domain_candidates(
    evidence: dict[str, Any],
    *,
    max_independent_evalue: float,
    min_profile_coverage: float,
    min_query_coverage: float,
    min_accuracy: float,
    max_candidates: int = 100_000,
) -> dict[str, object]:
    """Rank profile matches using explicit caller thresholds; never infer function."""
    if not isinstance(evidence, dict) or evidence.get("schema") != (
        "kinetics.hmmscan-domain-evidence.v1"
    ):
        raise ValueError("evidence must be a parsed HMMER domain-evidence object")
    thresholds = {
        "max_independent_evalue": max_independent_evalue,
        "min_profile_coverage": min_profile_coverage,
        "min_query_coverage": min_query_coverage,
        "min_accuracy": min_accuracy,
    }
    for name, value in thresholds.items():
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError(f"{name} must be a finite number")
    if max_independent_evalue <= 0:
        raise ValueError("max_independent_evalue must be positive")
    for name in ("min_profile_coverage", "min_query_coverage", "min_accuracy"):
        if not 0.0 <= thresholds[name] <= 1.0:
            raise ValueError(f"{name} must be in [0, 1]")
    if (
        isinstance(max_candidates, bool)
        or not isinstance(max_candidates, int)
        or max_candidates < 1
    ):
        raise ValueError("max_candidates must be a positive integer")

    raw_hits = evidence.get("hits")
    if not isinstance(raw_hits, list):
        raise ValueError("HMMER evidence hits must be a list")
    if len(raw_hits) > max_candidates:
        raise ValueError("HMMER evidence exceeds max_candidates")

    candidates: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_hits):
        if not isinstance(raw, dict):
            raise ValueError(f"HMMER evidence hit {index} must be an object")
        required_ints = (
            "profile_length", "query_length", "hmm_start_1based",
            "hmm_end_1based", "alignment_start_1based", "alignment_end_1based",
        )
        if any(
            isinstance(raw.get(field), bool) or not isinstance(raw.get(field), int)
            for field in required_ints
        ):
            raise ValueError(f"HMMER evidence hit {index} has invalid coordinates")
        profile_length = raw["profile_length"]
        query_length = raw["query_length"]
        hmm_start = raw["hmm_start_1based"]
        hmm_end = raw["hmm_end_1based"]
        query_start = raw["alignment_start_1based"]
        query_end = raw["alignment_end_1based"]
        if (
            profile_length < 1
            or query_length < 1
            or not 1 <= hmm_start <= hmm_end <= profile_length
            or not 1 <= query_start <= query_end <= query_length
        ):
            raise ValueError(f"HMMER evidence hit {index} has out-of-range coordinates")
        evalue = raw.get("independent_evalue")
        accuracy = raw.get("accuracy")
        domain_score = raw.get("domain_score")
        if (
            isinstance(evalue, bool)
            or not isinstance(evalue, (int, float))
            or not math.isfinite(evalue)
            or isinstance(accuracy, bool)
            or not isinstance(accuracy, (int, float))
            or not math.isfinite(accuracy)
            or isinstance(domain_score, bool)
            or not isinstance(domain_score, (int, float))
            or not math.isfinite(domain_score)
        ):
            raise ValueError(f"HMMER evidence hit {index} has invalid statistics")
        if evalue < 0 or not 0 <= accuracy <= 1:
            raise ValueError(f"HMMER evidence hit {index} has invalid statistics")
        profile_coverage = (hmm_end - hmm_start + 1) / profile_length
        query_coverage = (query_end - query_start + 1) / query_length
        failures: list[str] = []
        if evalue > max_independent_evalue:
            failures.append("independent_evalue_above_threshold")
        if profile_coverage < min_profile_coverage:
            failures.append("profile_coverage_below_threshold")
        if query_coverage < min_query_coverage:
            failures.append("query_coverage_below_threshold")
        if accuracy < min_accuracy:
            failures.append("accuracy_below_threshold")
        candidates.append({
            "profile_id": raw.get("profile_id"),
            "profile_accession": raw.get("profile_accession"),
            "query_id": raw.get("query_id"),
            "domain_number": raw.get("domain_number"),
            "independent_evalue": float(evalue),
            "domain_score": float(domain_score),
            "profile_coverage": profile_coverage,
            "query_coverage": query_coverage,
            "accuracy": float(accuracy),
            "status": "passes_caller_thresholds" if not failures else "below_threshold",
            "failed_thresholds": failures,
        })

    candidates.sort(
        key=lambda item: (
            item["status"] != "passes_caller_thresholds",
            item["independent_evalue"],
            -float(item["domain_score"]),
            -float(item["profile_coverage"]),
            str(item["profile_id"]),
            int(item["domain_number"] or 0),
        )
    )
    rank = 0
    for candidate in candidates:
        if candidate["status"] == "passes_caller_thresholds":
            rank += 1
            candidate["rank"] = rank
        else:
            candidate["rank"] = None
    return {
        "schema": "kinetics.hmmer-ranked-domain-candidates.v1",
        "thresholds": thresholds,
        "candidate_count": len(candidates),
        "passing_candidate_count": rank,
        "candidates": candidates,
        "conclusion": (
            "ranked_profile_domain_candidates_require_expert_review"
            if rank
            else "no_profile_candidates_passed_caller_thresholds"
        ),
        "limitations": [
            "Thresholds are caller-selected and are not calibrated by this module.",
            "Ranking does not establish protein family, domain function or orthology.",
            "No novelty, pathogenicity, organism identity or biological mechanism is inferred.",
            "Profile database licensing and provenance remain separate approval gates.",
        ],
    }
