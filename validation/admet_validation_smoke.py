"""Pinned RDKit smoke check for ADMET split and applicability utilities."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from molecularis.admet_validation import (
    binary_admet_metrics,
    scaffold_group_split,
    tanimoto_applicability_domain,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    smiles = [
        "c1ccccc1", "Cc1ccccc1", "CCc1ccccc1",
        "C1CCCCC1", "CC1CCCCC1",
        "CCO", "CCCO", "CCN",
    ]
    split = scaffold_group_split(smiles, seed=20261111)
    metrics = binary_admet_metrics(
        [0, 0, 1, 1, 0, 1],
        [0.1, 0.3, 0.7, 0.9, 0.4, 0.6],
    )
    domain = tanimoto_applicability_domain(
        ["CCO", "c1ccccc1"],
        ["CCO", "CCCCCCCC"],
        threshold=0.4,
    )
    schema = json.loads(
        (ROOT / "api" / "admet-validation.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    for result in (split, metrics, domain):
        validator.validate(result)
    if not split["no_scaffold_overlap"]:
        raise SystemExit("Scaffold leakage detected")
    if domain["results"][0]["nearest_tanimoto_similarity"] != 1.0:
        raise SystemExit("Exact-reference similarity check failed")
    if domain["results"][1]["within_applicability_domain"]:
        raise SystemExit("Distant query unexpectedly passed applicability threshold")
    report = {
        "validation_id": "admet-evaluation-utilities-rdkit-smoke-v1",
        "overall_pass": True,
        "scaffold_group_count": split["scaffold_group_count"],
        "partition_counts": split["partition_counts"],
        "binary_metrics": {
            "roc_auc": metrics["roc_auc"],
            "average_precision": metrics["average_precision"],
            "brier_score": metrics["brier_score"],
        },
        "applicability_domain": domain["results"],
        "model_trained": False,
        "dataset_ingested": False,
        "clinical_validation": False,
        "limitations": [
            "Synthetic examples only; no ADMET endpoint data or predictive model is included",
            "Utility smoke tests do not establish model performance or clinical utility",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
