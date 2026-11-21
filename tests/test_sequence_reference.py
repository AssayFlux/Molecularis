from __future__ import annotations

import hashlib

import pytest

from molecularis.sequence import SequenceRecord
from molecularis.sequence_reference import ReferencePack, exact_reference_search


def pack() -> ReferencePack:
    return ReferencePack(
        name="synthetic-test-pack",
        version="1.0",
        license="CC0-1.0",
        source="https://example.org/reference-pack",
        content_sha256=hashlib.sha256(b"fixture-pack").hexdigest(),
    )


def test_exact_reference_search_emits_provenance_and_match_evidence() -> None:
    result = exact_reference_search(
        " acgt ", [SequenceRecord("ref-1", "ACGT")],
        sequence_type="DNA", reference_pack=pack(),
    )
    assert result["query"]["sequence_sha256"] == hashlib.sha256(b"ACGT").hexdigest()
    assert result["hits"][0]["identity"] == 1.0
    assert result["conclusion"]["annotation_status"] == "supported"
    assert result["conclusion"]["novelty_status"] == "not_established"
    assert result["search"]["reference_packs"][0]["license"] == "CC0-1.0"


def test_no_hit_abstains_and_never_claims_novelty() -> None:
    result = exact_reference_search(
        "ACGA", [SequenceRecord("ref-1", "ACGT")],
        sequence_type="DNA", reference_pack=pack(),
    )
    assert result["hits"] == []
    assert result["conclusion"]["annotation_status"] == "no_hit"
    assert result["conclusion"]["novelty_status"] == "not_established"
    assert len(result["conclusion"]["abstention_reasons"]) >= 1


@pytest.mark.parametrize("kwargs", [
    {"max_records": 0},
    {"max_total_residues": 0},
])
def test_search_rejects_invalid_resource_limits(kwargs: dict[str, int]) -> None:
    with pytest.raises(ValueError):
        exact_reference_search(
            "ACGT", [], sequence_type="DNA", reference_pack=pack(), **kwargs,
        )


def test_search_rejects_invalid_pack_hash_and_duplicate_reference_ids() -> None:
    bad = ReferencePack("pack", "1", "CC0", "https://example.org", "not-a-hash")
    with pytest.raises(ValueError, match="SHA-256"):
        exact_reference_search("ACGT", [], sequence_type="DNA", reference_pack=bad)
    with pytest.raises(ValueError, match="unique"):
        exact_reference_search(
            "ACGT", [SequenceRecord("dup", "ACGT"), SequenceRecord("dup", "ACGT")],
            sequence_type="DNA", reference_pack=pack(),
        )


def test_protein_exact_match_uses_protein_alphabet() -> None:
    result = exact_reference_search(
        "MKWVTF", [SequenceRecord("p1", "MKWVTF")],
        sequence_type="protein", reference_pack=pack(),
    )
    assert result["hits"][0]["evidence_type"] == "exact_sequence"
    assert result["query"]["alphabet"] == "protein"



def test_exact_reference_search_bounds_query_and_validates_integer_limits() -> None:
    from molecularis.sequence_reference import ReferencePack, exact_reference_search
    from molecularis.sequence import SequenceRecord

    pack = ReferencePack(
        name="fixture", version="1", license="CC0-1.0",
        source="https://example.org/reference",
        content_sha256="a" * 64,
    )
    refs = [SequenceRecord(identifier="r1", sequence="ATG")]
    with pytest.raises(ValueError, match="max_query_residues"):
        exact_reference_search(
            "ATGATG", refs, sequence_type="DNA", reference_pack=pack,
            max_query_residues=5,
        )
    with pytest.raises(ValueError, match="positive integer"):
        exact_reference_search(
            "ATG", refs, sequence_type="DNA", reference_pack=pack,
            max_records=True,
        )
    with pytest.raises(ValueError, match="positive integer"):
        exact_reference_search(
            "ATG", refs, sequence_type="DNA", reference_pack=pack,
            max_total_residues=1.5,
        )



def test_fasta_reference_search_verifies_raw_bytes_and_emits_exact_hits() -> None:
    from molecularis.sequence_reference import exact_reference_search_fasta

    payload = b">ref-1 sample\nACGT\n>ref-2\nTTTT\n"
    reference_pack = ReferencePack(
        name="fixture-fasta", version="1", license="CC0-1.0",
        source="https://example.org/fasta",
        content_sha256=hashlib.sha256(payload).hexdigest(),
    )
    result = exact_reference_search_fasta(
        "ACGT", payload, sequence_type="DNA", reference_pack=reference_pack,
    )
    assert [hit["reference_id"] for hit in result["hits"]] == ["ref-1"]
    expected_digest = hashlib.sha256(payload).hexdigest()
    assert result["search"]["reference_packs"][0]["content_sha256"] == expected_digest


def test_fasta_reference_search_rejects_hash_mismatch_and_byte_budget() -> None:
    from molecularis.sequence_reference import exact_reference_search_fasta

    payload = b">ref-1\nACGT\n"
    reference_pack = ReferencePack(
        name="fixture-fasta", version="1", license="CC0-1.0",
        source="https://example.org/fasta", content_sha256="a" * 64,
    )
    with pytest.raises(ValueError, match="SHA-256"):
        exact_reference_search_fasta(
            "ACGT", payload, sequence_type="DNA", reference_pack=reference_pack,
        )
    with pytest.raises(ValueError, match="max_fasta_bytes"):
        exact_reference_search_fasta(
            "ACGT", payload, sequence_type="DNA",
            reference_pack=ReferencePack(
                name="fixture-fasta", version="1", license="CC0-1.0",
                source="https://example.org/fasta",
                content_sha256=hashlib.sha256(payload).hexdigest(),
            ),
            max_fasta_bytes=4,
        )


def test_bounded_local_alignment_reports_partial_match_coordinates_and_provenance() -> None:
    from molecularis.sequence_reference import local_alignment_reference_search

    result = local_alignment_reference_search(
        "ACGT", [SequenceRecord("ref", "TTACGTAA")],
        sequence_type="DNA", reference_pack=pack(),
    )
    hit = result["hits"][0]
    assert hit["reference_id"] == "ref"
    assert hit["score"] == 8
    assert hit["identity"] == 1.0
    assert hit["query_coverage"] == 1.0
    assert (hit["reference_start_1based"], hit["reference_end_1based"]) == (3, 6)
    assert hit["evalue"] is None
    assert result["conclusion"]["homology"] == "not_established"


def test_bounded_local_alignment_abstains_and_enforces_cell_budgets() -> None:
    from molecularis.sequence_reference import local_alignment_reference_search

    no_hit = local_alignment_reference_search(
        "AAAA", [SequenceRecord("ref", "TTTT")],
        sequence_type="DNA", reference_pack=pack(),
    )
    assert no_hit["hits"] == []
    assert no_hit["conclusion"]["novelty"] == "not_established"
    with pytest.raises(ValueError, match="max_alignment_cells"):
        local_alignment_reference_search(
            "ACGT", [SequenceRecord("ref", "ACGT")],
            sequence_type="DNA", reference_pack=pack(), max_alignment_cells=4,
        )
    with pytest.raises(ValueError, match="max_total_alignment_cells"):
        local_alignment_reference_search(
            "ACGT", [SequenceRecord("r1", "ACGT"), SequenceRecord("r2", "ACGT")],
            sequence_type="DNA", reference_pack=pack(), max_total_alignment_cells=40,
        )
