"""Build-pinned reference sequence contracts for non-clinical variant normalization.

This module validates reference identity and coordinate metadata before delegating
literal biallelic small-variant normalization. It performs no variant interpretation.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256

from .genomics import normalize_small_variant

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REFERENCE_ALPHABET = frozenset("ACGTN")


@dataclass(frozen=True)
class ReferenceSequence:
    """Immutable reference contig with explicit build, release and byte provenance.

    The digest is calculated over the exact uppercase ASCII sequence supplied here.
    Coordinates are 1-based closed; the contig sequence is held in memory by caller.
    """

    assembly: str
    accession: str
    release: str
    contig: str
    sequence: str
    sequence_sha256: str
    retrieved_at: str
    coordinate_system: str = "1-based-closed"
    data_classification: str = "public_non_patient_synthetic"

    def validate(self) -> None:
        for field_name in ("assembly", "accession", "release", "contig"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip() or value != value.strip():
                raise ValueError(f"Reference {field_name} must be a non-empty trimmed string")
        if self.coordinate_system != "1-based-closed":
            raise ValueError("Reference coordinate_system must be 1-based-closed")
        if self.data_classification != "public_non_patient_synthetic":
            raise ValueError("Only public non-patient synthetic reference fixtures are accepted")
        if not isinstance(self.sequence, str) or not self.sequence:
            raise ValueError("Reference sequence must be a non-empty string")
        if self.sequence != self.sequence.upper() or any(
            base not in _REFERENCE_ALPHABET for base in self.sequence
        ):
            raise ValueError("Reference sequence must be uppercase A/C/G/T/N without whitespace")
        if not isinstance(self.sequence_sha256, str) or not _SHA256.fullmatch(
            self.sequence_sha256
        ):
            raise ValueError("Reference sequence_sha256 must be a lowercase SHA-256 digest")
        actual_digest = sha256(self.sequence.encode("ascii")).hexdigest()
        if actual_digest != self.sequence_sha256:
            raise ValueError("Reference sequence SHA-256 does not match sequence bytes")
        if not isinstance(self.retrieved_at, str):
            raise ValueError("Reference retrieved_at must be timezone-aware ISO-8601")
        try:
            timestamp = datetime.fromisoformat(self.retrieved_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(
                "Reference retrieved_at must be timezone-aware ISO-8601"
            ) from exc
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("Reference retrieved_at must include a timezone")


def normalize_against_reference(
    reference: ReferenceSequence,
    chrom: str,
    position: int,
    ref: str,
    alt: str,
) -> dict[str, object]:
    """Normalize a literal biallelic variant and bind output to a verified reference.

    This is representation normalization only: no transcript mapping, phasing,
    pathogenicity, pharmacogenomic matching or clinical interpretation is performed.
    """
    reference.validate()
    if chrom != reference.contig:
        raise ValueError("Variant chromosome/contig does not match reference contig")
    normalized = normalize_small_variant(
        chrom, position, ref, alt, reference.sequence
    )
    return {
        **normalized,
        "reference_assembly": reference.assembly,
        "reference_accession": reference.accession,
        "reference_release": reference.release,
        "reference_contig": reference.contig,
        "reference_sequence_sha256": reference.sequence_sha256,
        "reference_retrieved_at": reference.retrieved_at,
        "coordinate_system": reference.coordinate_system,
        "interpretation_performed": False,
    }
