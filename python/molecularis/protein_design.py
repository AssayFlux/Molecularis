"""Typed, non-generative protein-design brief validation and release gates.

This module validates research intent only. It does not generate sequences, rank
candidates, predict structure, or establish biological safety or function.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

_SCHEMA = "kinetics.protein-design-brief.v1"
_OBJECTIVES = frozenset({"stability", "solubility", "expression", "foldability"})
_HOSTS = frozenset({"unspecified", "bacterial", "yeast", "mammalian", "cell_free", "other"})
_LOCALIZATIONS = frozenset({
    "unspecified", "cytosolic", "secreted", "membrane", "extracellular", "other",
})
_AMINO_ACIDS = re.compile(r"^[ACDEFGHIKLMNPQRSTVWY]+$")


def _text_list(
    value: Any, field: str, *, minimum: int, maximum: int, max_length: int = 500,
) -> list[str]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError(f"{field} must contain between {minimum} and {maximum} entries")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip() or len(item) > max_length:
            raise ValueError(
                f"{field} entries must be non-empty text up to {max_length} characters"
            )
        result.append(item.strip())
    if len(set(result)) != len(result):
        raise ValueError(f"{field} entries must be unique")
    return result


def validate_protein_design_brief(brief: dict[str, Any]) -> dict[str, object]:
    """Validate a bounded, human-reviewed research brief without generating a sequence."""
    required = {
        "schema", "objective", "target_description", "length_min", "length_max",
        "fold_constraints", "expression_host", "localization", "disallowed_motifs",
        "safety_exclusions", "human_review_required",
    }
    if not isinstance(brief, dict) or set(brief) != required:
        raise ValueError("Protein design brief has missing or unsupported fields")
    if brief["schema"] != _SCHEMA:
        raise ValueError("Unsupported protein design brief schema")
    objective = brief["objective"]
    if not isinstance(objective, str) or objective not in _OBJECTIVES:
        raise ValueError("objective must be one of stability, solubility, expression or foldability")
    description = brief["target_description"]
    if not isinstance(description, str) or not description.strip() or len(description) > 1000:
        raise ValueError("target_description must be non-empty text up to 1000 characters")

    minimum, maximum = brief["length_min"], brief["length_max"]
    for name, value in (("length_min", minimum), ("length_max", maximum)):
        if isinstance(value, bool) or not isinstance(value, int) or not 10 <= value <= 1000:
            raise ValueError(f"{name} must be an integer between 10 and 1000")
    if minimum > maximum:
        raise ValueError("length_min must be less than or equal to length_max")

    fold_constraints = _text_list(
        brief["fold_constraints"], "fold_constraints", minimum=0, maximum=32,
    )
    safety_exclusions = _text_list(
        brief["safety_exclusions"], "safety_exclusions", minimum=1, maximum=32,
    )
    motifs = _text_list(
        brief["disallowed_motifs"], "disallowed_motifs", minimum=0, maximum=100,
        max_length=64,
    )
    for motif in motifs:
        if not _AMINO_ACIDS.fullmatch(motif.upper()):
            raise ValueError("disallowed_motifs must be literal canonical amino-acid strings")
    host = brief["expression_host"]
    if not isinstance(host, str) or host not in _HOSTS:
        raise ValueError("expression_host is not supported")
    localization = brief["localization"]
    if not isinstance(localization, str) or localization not in _LOCALIZATIONS:
        raise ValueError("localization is not supported")
    if brief["human_review_required"] is not True:
        raise ValueError("human_review_required must be true")

    normalized = {
        "schema": _SCHEMA,
        "objective": objective,
        "target_description": description.strip(),
        "length_min": minimum,
        "length_max": maximum,
        "fold_constraints": fold_constraints,
        "expression_host": host,
        "localization": localization,
        "disallowed_motifs": [motif.upper() for motif in motifs],
        "safety_exclusions": safety_exclusions,
        "human_review_required": True,
    }
    canonical = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return {
        "schema": "kinetics.protein-design-brief-validation.v1",
        "status": "brief_validated_generation_blocked",
        "brief_sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest(),
        "normalized_brief": normalized,
        "generation_status": "blocked_no_approved_model_or_benchmark",
        "experimental_status": "not_validated",
        "required_gates": [
            "Model, weights and dataset licenses must be reviewed and approved.",
            "Independent held-out benchmarks and failure analysis must pass.",
            "Similarity, intellectual-property and biosafety review must pass.",
            "A human-reviewed experimental plan and owner approval are required.",
            "Prospective wet-lab measurements are required before claiming function.",
        ],
        "limitations": [
            "Brief validation is not a biological safety assessment.",
            "No amino-acid sequence, candidate ranking or structure prediction was generated.",
            "User-supplied exclusions and motif strings are declarations, not verified filters.",
            "A validated brief does not establish foldability, activity, safety or manufacturability.",
        ],
    }
