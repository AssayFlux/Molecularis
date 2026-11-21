#!/usr/bin/env python3
"""Validate the metadata-only ADMET source inventory; never downloads data."""
from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    catalog = yaml.safe_load(
        (ROOT / "data" / "admet-source-catalog.yaml").read_text(encoding="utf-8")
    )
    schema = json.loads(
        (ROOT / "api" / "admet-source-catalog.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(catalog)
    if catalog["entries"]:
        raise SystemExit("ADMET data intake is blocked; entries must remain empty")
    expected = {"pubchem-bioassay", "chembl", "tox21", "fda-dilirank-2"}
    actual = {item["source_id"] for item in catalog["candidate_sources"]}
    if actual != expected:
        raise SystemExit(f"Unexpected ADMET source inventory: {sorted(actual)}")
    if any(
        item["license_review_status"] != "verify_before_intake"
        for item in catalog["candidate_sources"]
    ):
        raise SystemExit(
            "Every ADMET source must remain gated pending exact-release licence review"
        )
    print(
        json.dumps(
            {
                "validation_id": "admet-source-catalog-metadata-only-v1",
                "overall_pass": True,
                "candidate_sources": sorted(actual),
                "acquired_entries": 0,
                "patient_data": False,
                "model_selected": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
