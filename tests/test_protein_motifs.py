from __future__ import annotations

from hashlib import sha256
import json

import pytest

from molecularis.protein_motifs import MotifPack, scan_protein_motif_pack


def make_pack(document: object | None = None) -> tuple[bytes, MotifPack]:
    value = document if document is not None else {
        "schema_version": 1,
        "motifs": [
            {"id": "site-b", "pattern": "H.D", "description": "synthetic fixture"},
            {"id": "site-a", "pattern": "MKW"},
        ],
    }
    payload = json.dumps(value, separators=(",", ":")).encode()
    pack = MotifPack(
        name="synthetic-motifs",
        version="1",
        license="CC0-1.0",
        source="https://example.org/motifs",
        content_sha256=sha256(payload).hexdigest(),
    )
    return payload, pack


def test_fixed_width_motif_scan_reports_coordinates_and_provenance() -> None:
    payload, pack = make_pack()
    result = scan_protein_motif_pack("AAMKWPHAD", payload, motif_pack=pack)
    assert [(hit["motif_id"], hit["start_1based"], hit["end_1based"])
            for hit in result["hits"]] == [("site-a", 3, 5), ("site-b", 7, 9)]
    assert result["hits"][1]["matched_sequence"] == "HAD"
    assert result["search"]["motif_pack"]["content_sha256"] == pack.content_sha256
    assert result["conclusion"]["family_or_function"] == "not_inferred"


def test_no_match_does_not_claim_novelty_or_absence_of_function() -> None:
    payload, pack = make_pack()
    result = scan_protein_motif_pack("AAAAAA", payload, motif_pack=pack)
    assert result["hits"] == []
    assert result["conclusion"]["status"] == "no_motif_match"
    assert result["conclusion"]["novelty"] == "not_established"


def test_pack_hash_and_json_are_verified() -> None:
    payload, pack = make_pack()
    with pytest.raises(ValueError, match="SHA-256"):
        scan_protein_motif_pack("MKW", payload + b" ", motif_pack=pack)
    with pytest.raises(ValueError, match="valid UTF-8 JSON"):
        scan_protein_motif_pack(
            "MKW", b"\xff", motif_pack=MotifPack(
                "x", "1", "CC0", "https://example.org", sha256(b"\xff").hexdigest()
            )
        )


@pytest.mark.parametrize("query", ["", "ABCD", "ACD*"])
def test_query_must_be_nonempty_canonical_protein(query: str) -> None:
    payload, pack = make_pack()
    with pytest.raises(ValueError):
        scan_protein_motif_pack(query, payload, motif_pack=pack)


def test_motif_pack_rejects_bad_patterns_duplicate_ids_and_duplicate_json_keys() -> None:
    for definitions in (
        [{"id": "x", "pattern": "A*"}],
        [{"id": "x", "pattern": "A."}, {"id": "x", "pattern": "G."}],
    ):
        payload, pack = make_pack({"schema_version": 1, "motifs": definitions})
        with pytest.raises(ValueError):
            scan_protein_motif_pack("AAAA", payload, motif_pack=pack)
    payload = b'{"schema_version":1,"schema_version":1,"motifs":[{"id":"x","pattern":"A."}]}'
    pack = MotifPack("x", "1", "CC0", "https://example.org", sha256(payload).hexdigest())
    with pytest.raises(ValueError, match="duplicate key"):
        scan_protein_motif_pack("AAAA", payload, motif_pack=pack)


def test_resource_limits_are_strict_and_enforced() -> None:
    payload, pack = make_pack()
    with pytest.raises(ValueError, match="max_query_residues"):
        scan_protein_motif_pack("MKW", payload, motif_pack=pack, max_query_residues=2)
    with pytest.raises(ValueError, match="max_pack_bytes"):
        scan_protein_motif_pack("MKW", payload, motif_pack=pack, max_pack_bytes=1)
    with pytest.raises(ValueError, match="max_comparisons"):
        scan_protein_motif_pack("MKW", payload, motif_pack=pack, max_comparisons=1)
    with pytest.raises(ValueError, match="max_hits"):
        scan_protein_motif_pack("MKWPHAD", payload, motif_pack=pack, max_hits=1)


def test_limits_reject_booleans_and_non_integers() -> None:
    payload, pack = make_pack()
    for key, value in (("max_motifs", True), ("max_hits", 1.5)):
        with pytest.raises(ValueError, match="positive integer"):
            scan_protein_motif_pack("MKW", payload, motif_pack=pack, **{key: value})
