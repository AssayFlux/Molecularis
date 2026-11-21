from __future__ import annotations

import json

from scripts.gen_android_capability_catalog import (
    OUTPUT,
    REGISTRY,
    build_catalogue,
    render_catalogue,
)


def test_android_capability_catalogue_matches_registry() -> None:
    import yaml

    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert OUTPUT.read_text(encoding="utf-8") == render_catalogue(registry)


def test_catalogue_keeps_implementation_separate_from_validation() -> None:
    catalogue = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert catalogue
    assert all(item["status"] in {"planned", "implemented", "validated"} for item in catalogue)
    assert all(item["evidence_level"] in {
        "none", "benchmark", "reference-concordance", "clinical-study"
    } for item in catalogue)
    assert all(item["implementation"] for item in catalogue)


def test_domain_grouping_is_stable_and_readable() -> None:
    catalogue = build_catalogue(
        {
            "tools": [
                {
                    "id": "sequence.fasta",
                    "name": "FASTA parser",
                    "status": "implemented",
                    "implementation": "python/molecularis/sequence.py",
                    "evidence_level": "none",
                }
            ]
        }
    )
    assert catalogue[0]["domain"] == "Sequence analysis"
