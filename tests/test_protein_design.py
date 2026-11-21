from __future__ import annotations

import pytest

from molecularis.protein_design import validate_protein_design_brief


def brief() -> dict[str, object]:
    return {
        "schema": "kinetics.protein-design-brief.v1",
        "objective": "stability",
        "target_description": "Explore stability of a non-clinical research scaffold",
        "length_min": 80,
        "length_max": 140,
        "fold_constraints": ["retain a compact soluble fold"],
        "expression_host": "bacterial",
        "localization": "cytosolic",
        "disallowed_motifs": ["RRRR", "PPPP"],
        "safety_exclusions": ["toxicity", "pathogenicity", "host-range expansion"],
        "human_review_required": True,
    }


def test_design_brief_validation_is_deterministic_and_non_generative() -> None:
    result = validate_protein_design_brief(brief())
    assert result["status"] == "brief_validated_generation_blocked"
    assert result["generation_status"] == "blocked_no_approved_model_or_benchmark"
    assert result["experimental_status"] == "not_validated"
    assert len(result["brief_sha256"]) == 64
    assert result == validate_protein_design_brief(brief())
    assert "No amino-acid sequence" in result["limitations"][1]


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("objective", "binding", "objective"),
        ("objective", [], "objective"),
        ("length_min", True, "length_min"),
        ("length_max", 9, "length_max"),
        ("expression_host", "unknown", "expression_host"),
        ("expression_host", [], "expression_host"),
        ("localization", "unknown", "localization"),
        ("localization", [], "localization"),
        ("human_review_required", False, "human_review_required"),
        ("disallowed_motifs", ["A.*"], "literal canonical"),
        ("safety_exclusions", [], "safety_exclusions"),
    ],
)
def test_design_brief_rejects_invalid_fields(field: str, value: object, message: str) -> None:
    value_to_test = brief()
    value_to_test[field] = value
    with pytest.raises(ValueError, match=message):
        validate_protein_design_brief(value_to_test)


def test_design_brief_rejects_unknown_fields_and_invalid_length_order() -> None:
    unknown = brief()
    unknown["candidate_sequence"] = "ACDEFGHIKL"
    with pytest.raises(ValueError, match="unsupported fields"):
        validate_protein_design_brief(unknown)

    invalid = brief()
    invalid["length_min"] = 200
    invalid["length_max"] = 100
    with pytest.raises(ValueError, match="less than or equal"):
        validate_protein_design_brief(invalid)


def test_design_brief_normalizes_literal_motifs_and_whitespace() -> None:
    value = brief()
    value["target_description"] = "  stability research  "
    value["disallowed_motifs"] = ["rrr"]
    result = validate_protein_design_brief(value)
    normalized = result["normalized_brief"]
    assert normalized["target_description"] == "stability research"
    assert normalized["disallowed_motifs"] == ["RRR"]
