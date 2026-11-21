from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from molecularis.admet_validation import binary_admet_metrics


def test_binary_admet_metrics_are_correct_for_perfect_and_tied_scores() -> None:
    perfect = binary_admet_metrics([0, 0, 1, 1], [0.05, 0.2, 0.8, 0.95])
    assert perfect["roc_auc"] == 1.0
    assert perfect["average_precision"] == 1.0
    assert perfect["brier_score"] < 0.03
    assert perfect["sensitivity"] == 1.0
    assert perfect["specificity"] == 1.0

    tied = binary_admet_metrics([0, 1], [0.5, 0.5])
    assert tied["roc_auc"] == 0.5
    assert tied["average_precision"] == 0.5


def test_binary_admet_metrics_reject_invalid_and_single_class_labels() -> None:
    with pytest.raises(ValueError, match="both positive and negative"):
        binary_admet_metrics([1, 1], [0.1, 0.9])
    with pytest.raises(ValueError, match="integer 0 or 1"):
        binary_admet_metrics([0.0, 1.0], [0.1, 0.9])
    with pytest.raises(ValueError, match="finite and in"):
        binary_admet_metrics([0, 1], [0.1, float("nan")])


def test_admet_metrics_result_matches_strict_schema() -> None:
    result = binary_admet_metrics(
        [0, 0, 1, 1, 0, 1],
        [0.1, 0.3, 0.7, 0.9, 0.4, 0.6],
    )
    schema_path = (
        Path(__file__).resolve().parents[1] / "api" / "admet-validation.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(result)


def test_scaffold_split_is_deterministic_and_has_no_scaffold_overlap() -> None:
    pytest.importorskip("rdkit")
    from molecularis.admet_validation import scaffold_group_split

    smiles = [
        "c1ccccc1", "Cc1ccccc1", "CCc1ccccc1",
        "C1CCCCC1", "CC1CCCCC1",
        "CCO", "CCCO", "CCN",
    ]
    first = scaffold_group_split(smiles, seed=17)
    second = scaffold_group_split(smiles, seed=17)
    assert first == second
    assert first["no_scaffold_overlap"] is True
    partitions = [
        set(first["train_indices"]),
        set(first["validation_indices"]),
        set(first["test_indices"]),
    ]
    assert not partitions[0] & partitions[1]
    assert not partitions[0] & partitions[2]
    assert not partitions[1] & partitions[2]
    assert sum(first["partition_counts"]) == len(smiles)
    schema_path = (
        Path(__file__).resolve().parents[1] / "api" / "admet-validation.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(first)


def test_tanimoto_applicability_domain_identifies_exact_and_distant_queries() -> None:
    pytest.importorskip("rdkit")
    from molecularis.admet_validation import tanimoto_applicability_domain

    result = tanimoto_applicability_domain(
        ["CCO", "c1ccccc1"],
        ["CCO", "CCCCCCCC"],
        threshold=0.4,
    )
    assert result["results"][0]["nearest_tanimoto_similarity"] == 1.0
    assert result["results"][0]["within_applicability_domain"] is True
    assert result["results"][1]["within_applicability_domain"] is False
    schema_path = (
        Path(__file__).resolve().parents[1] / "api" / "admet-validation.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(result)
