"""Bounded contig-level genome assembly QC; not gene annotation."""
from __future__ import annotations

from collections import Counter
from typing import Iterable

from .sequence import DNA, SequenceRecord, validate_sequence


def summarize_contigs(
    records: Iterable[SequenceRecord],
    *,
    max_records: int = 1_000_000,
    max_total_bases: int = 500_000_000,
    min_contig_length: int = 1,
) -> dict[str, object]:
    """Summarize contig lengths, N50/L50, GC and ambiguous-base burden.

    Input records are consumed incrementally. Sequence content is not returned.
    No coding potential, gene boundaries, taxon or functional annotation is inferred.
    """
    for name, value in (
        ("max_records", max_records),
        ("max_total_bases", max_total_bases),
        ("min_contig_length", min_contig_length),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")

    seen_ids: set[str] = set()
    lengths: list[int] = []
    total_bases = 0
    canonical_bases = 0
    gc_bases = 0
    ambiguous_bases = 0
    n_bases = 0
    filtered_contigs = 0
    for record in records:
        if len(lengths) >= max_records:
            raise ValueError("Assembly exceeds max_records")
        if not isinstance(record.identifier, str) or not record.identifier.strip():
            raise ValueError("Contig identifier must be non-empty text")
        if record.identifier in seen_ids:
            raise ValueError("Contig identifiers must be unique")
        seen_ids.add(record.identifier)
        sequence = record.sequence.upper()
        if not sequence:
            raise ValueError(f"Contig {record.identifier!r} is empty")
        validate_sequence(sequence, DNA)
        length = len(sequence)
        if length > max_total_bases - total_bases:
            raise ValueError("Assembly exceeds max_total_bases")
        total_bases += length
        counts = Counter(sequence)
        canonical = sum(counts[base] for base in "ACGT")
        canonical_bases += canonical
        gc_bases += counts["G"] + counts["C"]
        ambiguous_bases += length - canonical
        n_bases += counts["N"]
        lengths.append(length)
        if length < min_contig_length:
            filtered_contigs += 1

    if not lengths:
        raise ValueError("Assembly contains no contigs")
    ordered = sorted(lengths, reverse=True)
    half = (total_bases + 1) // 2
    cumulative = 0
    n50 = 0
    l50 = 0
    for length in ordered:
        cumulative += length
        l50 += 1
        if cumulative >= half:
            n50 = length
            break

    return {
        "schema": "kinetics.genome-contig-qc.v1",
        "contig_count": len(lengths),
        "total_bases": total_bases,
        "longest_contig": ordered[0],
        "shortest_contig": ordered[-1],
        "n50": n50,
        "l50": l50,
        "gc_fraction": gc_bases / canonical_bases if canonical_bases else None,
        "canonical_bases": canonical_bases,
        "ambiguous_bases": ambiguous_bases,
        "n_bases": n_bases,
        "filtered_contigs_below_minimum": filtered_contigs,
        "minimum_contig_length": min_contig_length,
        "limitations": [
            "Contig statistics only; no assembly completeness or correctness is established.",
            "No read mapping, contamination, repeat, gene, transcript or functional annotation is performed.",
            "GC fraction uses only canonical A/C/G/T bases; ambiguous symbols are excluded.",
        ],
    }
