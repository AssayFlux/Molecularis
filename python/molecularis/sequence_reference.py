"""Deterministic, exact-only local reference search for S6 triage.

This is a bounded evidence-producing primitive, not BLAST/HMMER, a gene caller,
or a calibrated homology/family classifier. A no-hit is never novelty evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO, TextIOWrapper
from hashlib import sha256
from typing import Iterable, Literal, cast
from urllib.parse import urlparse

from kinetics.sequence import DNA, PROTEIN, RNA, SequenceRecord, iter_fasta_records, validate_sequence

SequenceType = Literal["DNA", "RNA", "protein"]


@dataclass(frozen=True)
class ReferencePack:
    name: str
    version: str
    license: str
    source: str
    content_sha256: str

    def validate(self) -> None:
        if not all(isinstance(value, str) and value.strip() for value in (
            self.name, self.version, self.license, self.source, self.content_sha256
        )):
            raise ValueError("Reference pack metadata fields must be non-empty strings")
        parsed = urlparse(self.source)
        if parsed.scheme not in {"https", "http", "doi"}:
            raise ValueError("Reference pack source must be an http(s) or doi URI")
        if len(self.content_sha256) != 64 or any(
            char not in "0123456789abcdef" for char in self.content_sha256
        ):
            raise ValueError("Reference pack content_sha256 must be lowercase SHA-256 hex")


def _alphabet(sequence_type: SequenceType) -> frozenset[str]:
    return {"DNA": DNA, "RNA": RNA, "protein": PROTEIN}[sequence_type]


def _normalise(sequence: str) -> str:
    return "".join(sequence.split()).upper()


def exact_reference_search(
    query: str,
    references: Iterable[SequenceRecord],
    *,
    sequence_type: SequenceType,
    reference_pack: ReferencePack,
    max_records: int = 100_000,
    max_total_residues: int = 50_000_000,
    max_query_residues: int = 5_000_000,
) -> dict[str, object]:
    """Return exact full-length matches and a provenance-complete abstaining result."""
    reference_pack.validate()
    if sequence_type not in ("DNA", "RNA", "protein"):
        raise ValueError("sequence_type must be DNA, RNA, or protein")
    normalized_query = _normalise(query)
    if not normalized_query:
        raise ValueError("Query sequence must not be empty")
    validate_sequence(normalized_query, _alphabet(sequence_type))
    limits = {
        "max_records": max_records,
        "max_total_residues": max_total_residues,
        "max_query_residues": max_query_residues,
    }
    for name, value in limits.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if len(normalized_query) > max_query_residues:
        raise ValueError("Query sequence exceeds max_query_residues limit")

    query_hash = sha256(normalized_query.encode("ascii")).hexdigest()
    hits: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    record_count = 0
    total_residues = 0
    for record in references:
        record_count += 1
        if record_count > max_records:
            raise ValueError("Reference pack exceeds max_records limit")
        if not record.identifier or record.identifier in seen_ids:
            raise ValueError("Reference identifiers must be non-empty and unique")
        seen_ids.add(record.identifier)
        target = _normalise(record.sequence)
        if not target:
            raise ValueError(f"Reference {record.identifier!r} has an empty sequence")
        validate_sequence(target, _alphabet(sequence_type))
        total_residues += len(target)
        if total_residues > max_total_residues:
            raise ValueError("Reference pack exceeds max_total_residues limit")
        if target == normalized_query:
            hits.append({
                "reference_id": record.identifier,
                "identity": 1.0,
                "query_coverage": 1.0,
                "reference_coverage": 1.0,
                "score": float(len(normalized_query)),
                "evalue": None,
                "evidence_type": "exact_sequence",
                "source_coordinates": None,
            })

    return {
        "schema_version": 1,
        "query": {
            "sequence_sha256": query_hash,
            "length": len(normalized_query),
            "alphabet": sequence_type,
            "sequence_type": {
                "DNA": "gene", "RNA": "transcript", "protein": "protein"
            }[sequence_type],
        },
        "search": {
            "algorithm": "exact-full-length-match-v1",
            "parameters": {
                "case_normalization": "uppercase",
                "whitespace": "removed",
                "partial_matches": False,
                "similarity_search": False,
                "max_records": max_records,
                "max_total_residues": max_total_residues,
                "max_query_residues": max_query_residues,
            },
            "reference_packs": [{
                "name": reference_pack.name,
                "version": reference_pack.version,
                "license": reference_pack.license,
                "source": reference_pack.source,
                "content_sha256": reference_pack.content_sha256,
            }],
        },
        "hits": hits,
        "conclusion": {
            "annotation_status": "supported" if hits else "no_hit",
            "novelty_status": "not_established",
            "confidence": "not_calibrated",
            "abstention_reasons": [] if hits else [
                "No exact full-length match in the supplied reference pack",
                "Similarity, homology, family and domain searches were not performed",
                "Reference-pack scope and completeness are not established",
            ],
        },
        "limitations": [
            "Exact full-length matching only; no local alignment or homology inference",
            "A no-hit result is not evidence that a sequence is novel",
            "No gene function, protein function, pathogenicity or clinical interpretation",
            "Reference pack license, version and hash are caller-supplied and must be independently verified",
        ],
    }



def exact_reference_search_fasta(
    query: str,
    fasta_bytes: bytes,
    *,
    sequence_type: SequenceType,
    reference_pack: ReferencePack,
    max_fasta_bytes: int = 512 * 1024 * 1024,
    max_records: int = 100_000,
    max_total_residues: int = 50_000_000,
    max_query_residues: int = 5_000_000,
) -> dict[str, object]:
    """Verify exact FASTA bytes against pack provenance, then search records.

    The byte digest is computed from the supplied raw payload before UTF-8
    decoding. FASTA records are parsed incrementally; no homology or novelty
    inference is performed. The caller remains responsible for acquiring the
    bytes under the source's licence and pinning the correct release.
    """
    reference_pack.validate()
    if not isinstance(fasta_bytes, bytes):
        raise TypeError("fasta_bytes must be bytes")
    if (
        not isinstance(max_fasta_bytes, int)
        or isinstance(max_fasta_bytes, bool)
        or max_fasta_bytes < 1
    ):
        raise ValueError("max_fasta_bytes must be a positive integer")
    if len(fasta_bytes) > max_fasta_bytes:
        raise ValueError("FASTA payload exceeds max_fasta_bytes limit")
    actual_sha256 = sha256(fasta_bytes).hexdigest()
    if actual_sha256 != reference_pack.content_sha256:
        raise ValueError("FASTA payload SHA-256 does not match reference-pack metadata")
    try:
        stream = TextIOWrapper(BytesIO(fasta_bytes), encoding="utf-8", errors="strict")
        records = iter_fasta_records(stream)
        return exact_reference_search(
            query,
            records,
            sequence_type=sequence_type,
            reference_pack=reference_pack,
            max_records=max_records,
            max_total_residues=max_total_residues,
            max_query_residues=max_query_residues,
        )
    except UnicodeDecodeError as exc:
        raise ValueError("FASTA payload must be valid UTF-8 text") from exc


def local_alignment_reference_search(
    query: str,
    references: Iterable[SequenceRecord],
    *,
    sequence_type: SequenceType,
    reference_pack: ReferencePack,
    match_score: int = 2,
    mismatch_score: int = -1,
    gap_score: int = -2,
    max_records: int = 10_000,
    max_total_residues: int = 5_000_000,
    max_query_residues: int = 20_000,
    max_alignment_cells: int = 2_000_000,
    max_total_alignment_cells: int = 20_000_000,
    max_hits: int = 100,
) -> dict[str, object]:
    """Run bounded Smith-Waterman local alignment against caller-supplied records.

    This simple identity-scored local aligner is an exploratory triage primitive.
    It does not compute E-values, statistical significance, calibrated homology,
    family/domain membership or functional annotation.
    """
    reference_pack.validate()
    if sequence_type not in ("DNA", "RNA", "protein"):
        raise ValueError("sequence_type must be DNA, RNA, or protein")
    query_sequence = _normalise(query)
    if not query_sequence:
        raise ValueError("Query sequence must not be empty")
    validate_sequence(query_sequence, _alphabet(sequence_type))
    if len(query_sequence) > max_query_residues:
        raise ValueError("Query sequence exceeds max_query_residues")
    integer_limits = {
        "max_records": max_records,
        "max_total_residues": max_total_residues,
        "max_query_residues": max_query_residues,
        "max_alignment_cells": max_alignment_cells,
        "max_total_alignment_cells": max_total_alignment_cells,
        "max_hits": max_hits,
        "match_score": match_score,
        "mismatch_score": mismatch_score,
        "gap_score": gap_score,
    }
    for name, value in integer_limits.items():
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer")
        if name == "match_score":
            if value < 1:
                raise ValueError(f"{name} must be positive")
        elif name in {"mismatch_score", "gap_score"}:
            if value >= 0:
                raise ValueError(f"{name} must be negative")
        elif value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if mismatch_score >= 0 or gap_score >= 0:
        raise ValueError("mismatch_score and gap_score must be negative")

    hits: list[dict[str, object]] = []
    seen: set[str] = set()
    total_residues = 0
    total_cells = 0
    record_count = 0
    query_length = len(query_sequence)

    for record in references:
        record_count += 1
        if record_count > max_records:
            raise ValueError("Reference pack exceeds max_records")
        if not record.identifier or record.identifier in seen:
            raise ValueError("Reference identifiers must be non-empty and unique")
        seen.add(record.identifier)
        target = _normalise(record.sequence)
        if not target:
            raise ValueError(f"Reference {record.identifier!r} has an empty sequence")
        validate_sequence(target, _alphabet(sequence_type))
        total_residues += len(target)
        if total_residues > max_total_residues:
            raise ValueError("Reference pack exceeds max_total_residues")
        width = len(target) + 1
        cells = (query_length + 1) * width
        if cells > max_alignment_cells:
            raise ValueError("Local alignment exceeds max_alignment_cells")
        total_cells += cells
        if total_cells > max_total_alignment_cells:
            raise ValueError("Local alignment exceeds max_total_alignment_cells")

        trace = bytearray(cells)
        previous = [0] * width
        best_score = 0
        best_i = best_j = 0
        for i, query_residue in enumerate(query_sequence, 1):
            current = [0] * width
            row_offset = i * width
            for j, target_residue in enumerate(target, 1):
                diagonal = previous[j - 1] + (
                    match_score if query_residue == target_residue else mismatch_score
                )
                up = previous[j] + gap_score
                left = current[j - 1] + gap_score
                score = max(0, diagonal, up, left)
                current[j] = score
                if score:
                    if score == diagonal:
                        trace[row_offset + j] = 1
                    elif score == up:
                        trace[row_offset + j] = 2
                    else:
                        trace[row_offset + j] = 3
                if score > best_score:
                    best_score, best_i, best_j = score, i, j
            previous = current

        i, j = best_i, best_j
        matches = mismatches = gaps = aligned_query = aligned_target = 0
        while i > 0 and j > 0:
            direction = trace[i * width + j]
            if direction == 0:
                break
            if direction == 1:
                i -= 1
                j -= 1
                aligned_query += 1
                aligned_target += 1
                if query_sequence[i] == target[j]:
                    matches += 1
                else:
                    mismatches += 1
            elif direction == 2:
                i -= 1
                aligned_query += 1
                gaps += 1
            else:
                j -= 1
                aligned_target += 1
                gaps += 1
        alignment_columns = matches + mismatches + gaps
        if best_score > 0:
            hits.append({
                "reference_id": record.identifier,
                "score": best_score,
                "identity": matches / alignment_columns if alignment_columns else 0.0,
                "query_coverage": aligned_query / query_length,
                "reference_coverage": aligned_target / len(target),
                "matches": matches,
                "mismatches": mismatches,
                "gap_columns": gaps,
                "alignment_columns": alignment_columns,
                "query_start_1based": i + 1,
                "query_end_1based": best_i,
                "reference_start_1based": j + 1,
                "reference_end_1based": best_j,
                "evalue": None,
                "evidence_type": "bounded_smith_waterman_identity_scored_local_alignment",
            })

    hits.sort(key=lambda hit: (-cast(int, hit["score"]), str(hit["reference_id"])))
    return {
        "schema_version": 1,
        "query": {
            "sequence_sha256": sha256(query_sequence.encode("ascii")).hexdigest(),
            "length": query_length,
            "alphabet": sequence_type,
        },
        "search": {
            "algorithm": "bounded-smith-waterman-linear-gap-v1",
            "scoring": {
                "match": match_score,
                "mismatch": mismatch_score,
                "gap": gap_score,
            },
            "reference_pack": {
                "name": reference_pack.name,
                "version": reference_pack.version,
                "license": reference_pack.license,
                "source": reference_pack.source,
                "content_sha256": reference_pack.content_sha256,
            },
            "records_examined": record_count,
            "alignment_cells_examined": total_cells,
            "max_alignment_cells_per_record": max_alignment_cells,
            "max_total_alignment_cells": max_total_alignment_cells,
        },
        "hits": hits[:max_hits],
        "conclusion": {
            "status": "local_alignment_hits" if hits else "no_local_alignment",
            "homology": "not_established",
            "family_or_function": "not_inferred",
            "novelty": "not_established",
            "statistical_significance": "not_computed",
        },
        "limitations": [
            "Simple identity scoring and linear gaps; not BLAST, HMMER or a calibrated homology method.",
            "No E-values, statistical significance, family/domain classification or function prediction.",
            "Short local matches can occur by chance; identity and coverage are descriptive only.",
            "Reference-pack scope, licensing and biological validity require independent review.",
            "A no-hit result is not evidence of sequence novelty.",
        ],
    }
