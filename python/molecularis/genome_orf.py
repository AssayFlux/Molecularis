"""Bounded per-contig six-frame ORF candidate workflow.

This is a prokaryotic-oriented candidate triage primitive, not a gene caller:
it does not model promoters, ribosome-binding sites, operons, gene boundaries,
or functional annotation. Eukaryotic genes require supplied transcript models.
"""
from __future__ import annotations

from hashlib import sha256
from typing import Iterable

from .orf import MAX_CANDIDATE_ORF_PAIRS, find_orf_candidates
from .sequence import SequenceRecord


def scan_contig_orf_candidates(
    records: Iterable[SequenceRecord],
    *,
    table_id: int = 11,
    min_protein_length: int = 30,
    max_contigs: int = 100_000,
    max_total_bases: int = 100_000_000,
    max_total_orfs: int = 100_000,
    max_candidate_pairs_total: int = MAX_CANDIDATE_ORF_PAIRS,
) -> dict[str, object]:
    """Scan supplied contigs with one aggregate work/output budget."""
    for name, value in (
        ("max_contigs", max_contigs),
        ("max_total_bases", max_total_bases),
        ("max_total_orfs", max_total_orfs),
        ("max_candidate_pairs_total", max_candidate_pairs_total),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if max_candidate_pairs_total > MAX_CANDIDATE_ORF_PAIRS:
        raise ValueError("max_candidate_pairs_total exceeds the hard ORF work ceiling")

    seen: set[str] = set()
    contig_results: list[dict[str, object]] = []
    total_bases = 0
    total_orfs = 0
    total_pairs = 0
    for record in records:
        if len(contig_results) >= max_contigs:
            raise ValueError("Genome exceeds max_contigs")
        if not isinstance(record.identifier, str) or not record.identifier.strip():
            raise ValueError("Contig identifier must be non-empty text")
        if record.identifier in seen:
            raise ValueError("Contig identifiers must be unique")
        seen.add(record.identifier)
        sequence = "".join(record.sequence.split()).upper().replace("U", "T")
        if not sequence:
            raise ValueError(f"Contig {record.identifier!r} is empty")
        if len(sequence) > max_total_bases - total_bases:
            raise ValueError("Genome exceeds max_total_bases")
        remaining_pairs = max_candidate_pairs_total - total_pairs
        remaining_orfs = max_total_orfs - total_orfs
        if remaining_pairs < 1 or remaining_orfs < 1:
            raise ValueError("Genome-wide ORF candidate work or output budget exhausted")
        result = find_orf_candidates(
            sequence,
            table_id=table_id,
            min_protein_length=min_protein_length,
            max_orfs=remaining_orfs,
            max_sequence_bases=max_total_bases,
            max_candidate_orf_pairs_total=remaining_pairs,
        )
        resource_limits = result.get("resource_limits")
        if not isinstance(resource_limits, dict):
            raise RuntimeError("ORF scanner omitted resource-limit evidence")
        examined = resource_limits.get("candidate_orf_pairs_examined")
        orf_count = result.get("orf_count")
        orfs = result.get("orfs")
        if (
            isinstance(examined, bool) or not isinstance(examined, int)
            or isinstance(orf_count, bool) or not isinstance(orf_count, int)
            or not isinstance(orfs, list)
        ):
            raise RuntimeError("ORF scanner returned an invalid candidate result")
        total_bases += len(sequence)
        total_orfs += orf_count
        total_pairs += examined
        contig_results.append({
            "contig_id": record.identifier,
            "sequence_sha256": sha256(sequence.encode("ascii")).hexdigest(),
            "sequence_length": len(sequence),
            "orf_count": orf_count,
            "candidate_orf_pairs_examined": examined,
            "orfs": orfs,
        })
    if not contig_results:
        raise ValueError("Genome contains no contigs")
    return {
        "schema": "kinetics.genome-orf-candidates.v1",
        "method": "six_frame_complete_start_to_stop_enumeration",
        "table_id": table_id,
        "min_protein_length": min_protein_length,
        "contig_count": len(contig_results),
        "total_bases": total_bases,
        "total_orf_candidates": total_orfs,
        "candidate_orf_pairs_examined": total_pairs,
        "resource_limits": {
            "max_contigs": max_contigs,
            "max_total_bases": max_total_bases,
            "max_total_orfs": max_total_orfs,
            "max_candidate_pairs_total": max_candidate_pairs_total,
        },
        "contigs": contig_results,
        "conclusion": "candidate_orfs_only_not_gene_annotation",
        "limitations": [
            "Six-frame complete ORF enumeration is a candidate screen, not a validated gene caller.",
            "No promoter, ribosome-binding site, operon, gene-boundary or functional model is applied.",
            "Do not use this method alone for eukaryotic genomes; use supplied transcript annotations.",
            "Genetic code and minimum protein length are caller-selected, not inferred.",
            "No biological accuracy or organism-specific performance is established.",
        ],
    }
