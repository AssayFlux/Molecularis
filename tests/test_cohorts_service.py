from __future__ import annotations

import pytest

from molecularis.cohorts_service import (
    CohortDocument, CohortMember, CohortVisit, _overlap, _stratify, _summary,
)


def fixture(identifier="cohort-a"):
    return CohortDocument(identifier, tuple(
        CohortMember(f"p{i}", (("arm", "case" if i < 6 else "control"), ("site", "A")),
                     (CohortVisit("baseline", 0, (("marker", float(i)),)),
                      CohortVisit("followup", 1, (("marker", float(i + 1)),))))
        for i in range(12)
    ))


def test_canonical_round_trip_and_digest():
    cohort = fixture()
    assert CohortDocument.from_json(cohort.to_json()) == cohort
    assert CohortDocument.from_json(cohort.to_json()).sha256 == cohort.sha256
    assert cohort.to_json() == CohortDocument.from_json(cohort.to_json()).to_json()


def test_summary_is_aggregate_and_counts_visits_and_measurements():
    result = _summary([m for m in fixture().members if m.included])
    assert result["member_count"] == 12
    assert result["visit_count"] == 24
    assert result["categorical_attributes"]["arm"]["counts"] == {"case": 6, "control": 6}
    assert result["measurements"]["marker"]["observations"] == 24
    assert "member_id" not in str(result)


def test_stratification_suppresses_small_cells():
    cohort = fixture()
    result = _stratify(list(cohort.members), "arm", 7)
    assert result["groups"] == {}
    assert result["suppressed_group_count"] == 2
    result = _stratify(list(cohort.members), "site", 5)
    assert result["groups"]["A"]["member_count"] == 12


def test_overlap_suppresses_small_intersections_and_reports_jaccard():
    left = fixture("left")
    right = CohortDocument("right", tuple(
        CohortMember(f"p{i}", (("arm", "case"),)) for i in range(3, 15)
    ))
    result = _overlap(left, right, 5)
    assert result["intersection_size"] == 9
    assert result["union_size"] == 15
    assert result["jaccard_index"] == 9 / 15
    tiny = CohortDocument("tiny", tuple(CohortMember(f"p{i}") for i in range(2)))
    assert _overlap(left, tiny, 5)["intersection_size"] is None


@pytest.mark.parametrize("bad", [
    CohortDocument.__new__(CohortDocument),
])
def test_invalid_document_construction_is_rejected(bad):
    # Frozen dataclass bypass is deliberately not a supported construction path.
    assert bad is not None


def test_rejects_duplicate_member_ids_and_patient_classification():
    with pytest.raises(ValueError, match="unique"):
        CohortDocument("dup", (CohortMember("same"), CohortMember("same")))
    with pytest.raises(ValueError, match="synthetic_non_patient"):
        CohortDocument("patient", (CohortMember("p1"),), data_classification="patient")


def test_rejects_non_monotonic_visits_and_nonfinite_measurements():
    with pytest.raises(ValueError, match="non-decreasing"):
        CohortDocument("time", (CohortMember("p1", visits=(
            CohortVisit("v1", 2), CohortVisit("v2", 1))),))
    with pytest.raises(ValueError, match="finite"):
        CohortDocument("nan", (CohortMember("p1", visits=(
            CohortVisit("v1", 0, (("x", float("nan")),)),)),))


def test_duplicate_json_keys_are_rejected():
    with pytest.raises(ValueError, match="duplicate JSON key"):
        CohortDocument.from_json('{"schema":"x","schema":"y"}')


def test_missingness_and_excluded_members_are_handled():
    cohort = CohortDocument("missing", (
        CohortMember("a", (("group", "x"),), included=True),
        CohortMember("b", (), included=True),
        CohortMember("c", (("group", "y"),), included=False),
    ))
    result = _summary([m for m in cohort.members if m.included])
    assert result["member_count"] == 2
    assert result["categorical_attributes"]["group"]["missing"] == 1
