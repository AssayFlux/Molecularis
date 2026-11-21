from __future__ import annotations

import json
from pathlib import Path


def test_sequence_annotation_schema_requires_provenance_and_abstention() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "sequence-annotation-evidence.schema.json").read_text(encoding="utf-8")
    )
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    required = set(schema["required"])
    assert {"query", "search", "hits", "conclusion", "limitations"} <= required
    query_required = set(schema["properties"]["query"]["required"])
    assert {"sequence_sha256", "length", "alphabet", "sequence_type"} <= query_required
    pack_required = set(
        schema["properties"]["search"]["properties"]["reference_packs"]
        ["items"]["required"]
    )
    assert {"name", "version", "license", "source", "content_sha256"} <= pack_required
    conclusion = schema["properties"]["conclusion"]["properties"]
    assert conclusion["novelty_status"]["const"] == "not_established"
    assert "abstention_reasons" in schema["properties"]["conclusion"]["required"]
    assert schema["properties"]["limitations"]["minItems"] == 1
