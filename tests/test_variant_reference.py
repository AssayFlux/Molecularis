from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

import pytest

from molecularis.variant_reference import ReferenceSequence, normalize_against_reference


def _reference() -> ReferenceSequence:
    sequence = "CAAAATGCC"
    return ReferenceSequence(
        assembly="synthetic-build-v1",
        accession="SYNTHETIC:CONTIG1",
        release="fixture-1",
        contig="chrSynthetic1",
        sequence=sequence,
        sequence_sha256=sha256(sequence.encode("ascii")).hexdigest(),
        retrieved_at="2026-11-09T00:00:00Z",
    )


def test_reference_bound_normalization_records_build_and_sequence_provenance() -> None:
    reference = _reference()
    result = normalize_against_reference(reference, "chrSynthetic1", 4, "A", "AA")
    assert (result["pos"], result["ref"], result["alt"]) == (1, "C", "CA")
    assert result["reference_assembly"] == "synthetic-build-v1"
    assert result["reference_accession"] == "SYNTHETIC:CONTIG1"
    assert result["reference_sequence_sha256"] == reference.sequence_sha256
    assert result["coordinate_system"] == "1-based-closed"
    assert result["interpretation_performed"] is False


def test_reference_rejects_sequence_digest_mismatch() -> None:
    reference = _reference()
    with pytest.raises(ValueError, match="SHA-256 does not match"):
        normalize_against_reference(
            replace(reference, sequence="CAAAATGCA"),
            "chrSynthetic1", 4, "A", "AA",
        )


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"coordinate_system": "0-based-half-open"}, "coordinate_system"),
        ({"data_classification": "patient"}, "public non-patient"),
        ({"retrieved_at": "2026-11-09T00:00:00"}, "timezone"),
        ({"sequence": "caaaATGCC"}, "uppercase"),
        ({"sequence": "CAAA ATGCC"}, "uppercase"),
    ],
)
def test_reference_rejects_ambiguous_metadata(
    changes: dict[str, str], message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        normalize_against_reference(
            replace(_reference(), **changes),
            "chrSynthetic1", 1, "C", "T",
        )


def test_reference_requires_matching_contig_and_reference_allele() -> None:
    reference = _reference()
    with pytest.raises(ValueError, match="contig"):
        normalize_against_reference(reference, "chrOther", 1, "C", "T")
    with pytest.raises(ValueError, match="does not match"):
        normalize_against_reference(reference, "chrSynthetic1", 1, "A", "T")
