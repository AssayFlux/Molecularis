"""Bounded, local FASTA quality-control workflow.

This is basic sequence parsing/statistics, not sequence identification or
biological/clinical interpretation.
"""
from __future__ import annotations

from typing import Any

from .genomics import fastq_quality_summary
from .sequence import parse_fasta, parse_fastq, sequence_statistics

MAX_FASTA_CHARS = 1_000_000
MAX_FASTA_RECORDS = 1_000
MAX_FASTA_BASES = 500_000


def _positive_limit(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def analyze_fasta_text(
    text: str,
    *,
    max_chars: int = MAX_FASTA_CHARS,
    max_records: int = MAX_FASTA_RECORDS,
    max_bases: int = MAX_FASTA_BASES,
) -> dict[str, Any]:
    """Parse bounded FASTA text and report per-record lengths/GC/ambiguous counts.

    GC percentage uses all sequence symbols as its denominator; non-ACGT
    symbols are reported separately and are not silently discarded.
    """
    max_chars = _positive_limit("max_chars", max_chars)
    max_records = _positive_limit("max_records", max_records)
    max_bases = _positive_limit("max_bases", max_bases)
    if not isinstance(text, str):
        raise TypeError("FASTA input must be text")
    if len(text) > max_chars:
        raise ValueError("FASTA input exceeds the configured character limit")
    records = parse_fasta(text)
    if len(records) > max_records:
        raise ValueError("FASTA input exceeds the configured record limit")
    total_bases = sum(len(record.sequence) for record in records)
    if total_bases > max_bases:
        raise ValueError("FASTA input exceeds the configured total-base limit")

    summaries = []
    for record in records:
        stats = sequence_statistics(record.sequence)
        summaries.append(
            {
                "identifier": record.identifier,
                "description": record.description,
                "length": int(stats["length"]),
                "gc_percent": round(float(stats["gc_fraction"]) * 100.0, 3),
                "ambiguous_count": int(stats["ambiguous_count"]),
            }
        )
    return {
        "record_count": len(summaries),
        "total_bases": total_bases,
        "gc_denominator": "all sequence symbols",
        "records": summaries,
        "limitations": [
            "Basic parsing and composition statistics only",
            "No identity, homology, gene function or protein function inference",
            "No pathogenicity or clinical interpretation",
            "Independent biological validation is not claimed",
        ],
    }


MAX_FASTQ_CHARS = 1_000_000
MAX_FASTQ_RECORDS = 10_000
MAX_FASTQ_BASES = 500_000


def analyze_fastq_text(text: str, *, phred_offset: int, max_chars: int = MAX_FASTQ_CHARS,
                       max_records: int = MAX_FASTQ_RECORDS,
                       max_bases: int = MAX_FASTQ_BASES) -> dict[str, Any]:
    """Bounded FASTQ quality summary; Phred encoding is explicitly selected."""
    max_chars = _positive_limit("max_chars", max_chars)
    max_records = _positive_limit("max_records", max_records)
    max_bases = _positive_limit("max_bases", max_bases)
    if not isinstance(text, str):
        raise TypeError("FASTQ input must be text")
    if isinstance(phred_offset, bool) or phred_offset not in (33, 64):
        raise ValueError("Select an explicit Phred offset of 33 or 64")
    if len(text) > max_chars:
        raise ValueError("FASTQ input exceeds the configured character limit")
    parsed = parse_fastq(text)
    if len(parsed) > max_records:
        raise ValueError("FASTQ input exceeds the configured record limit")
    total_bases = sum(len(record.sequence) for record, _ in parsed)
    if total_bases > max_bases:
        raise ValueError("FASTQ input exceeds the configured total-base limit")
    qualities = [quality for _, quality in parsed]
    overall = fastq_quality_summary(qualities, offset=phred_offset)
    reads = []
    for record, quality in parsed:
        summary = fastq_quality_summary([quality], offset=phred_offset)
        reads.append({"identifier": record.identifier, "length": len(record.sequence),
                      "mean_phred": round(float(summary["mean_phred"]), 3),
                      "q20_fraction": round(float(summary["q20_fraction"]), 6),
                      "q30_fraction": round(float(summary["q30_fraction"]), 6)})
    return {"record_count": len(reads), "total_bases": total_bases,
            "phred_offset": phred_offset,
            "mean_phred": round(float(overall["mean_phred"]), 3),
            "q20_fraction": round(float(overall["q20_fraction"]), 6),
            "q30_fraction": round(float(overall["q30_fraction"]), 6),
            "reads": reads,
            "limitations": ["Quality encoding is user-selected, never guessed",
                            "No adapter detection or trimming",
                            "No sliding-window trimming or paired-read rescue",
                            "No variant or clinical interpretation"]}
