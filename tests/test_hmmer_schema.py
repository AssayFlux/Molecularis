from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from molecularis.hmmer import parse_hmmscan_domtblout
PACK = {
    "name": "synthetic-profile-pack",
    "version": "1",
    "license": "CC0-1.0",
    "source": "https://example.org/profiles",
    "content_sha256": "a" * 64,
}
ROW = (
    "PF00001 PF00001.1 100 query-1 - 80 1e-20 72.5 0.1 1 1 "
    "1e-18 1e-18 70.0 0.0 5 75 3 73 2 75 0.98 kinase-like domain"
)


def test_hmmscan_evidence_matches_versioned_schema() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "api" / "hmmscan-domain-evidence.schema.json").read_text())
    result = parse_hmmscan_domtblout(
        [ROW], hmmer_version="3.4", profile_pack=PACK,
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(result)
