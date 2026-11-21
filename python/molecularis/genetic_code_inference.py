"""Conservative evidence-ranked genetic-code candidate screening (S8).

Scores supplied coding-sequence records against supported NCBI translation tables.
This is a hypothesis generator, not organism identification or a calibrated classifier.
"""
from __future__ import annotations

from math import isfinite
from typing import Iterable, Mapping, cast

from .genetic_code import GENETIC_CODES


def infer_genetic_code_candidates(
    records: Iterable[Mapping[str, object]],
    *,
    table_ids: Iterable[int] | None = None,
    min_records: int = 3,
    min_codons: int = 90,
    minimum_score_margin: float = 0.05,
    max_records: int = 1_000,
    max_total_bases: int = 3_000_000,
) -> dict[str, object]:
    """Rank candidate NCBI tables from caller-supplied coding-sequence evidence.

    Each record requires sequence and may specify frame (0/1/2) and complete_cds
    (bool, default false). Complete CDS records contribute table-specific
    start/terminal-stop evidence. All records contribute internal in-frame stop
    evidence. Ambiguous bases and partial codons are rejected.

    A table is selected only when record/codon minima are met and its normalized
    penalty beats the runner-up by minimum_score_margin. This is uncalibrated.
    """
    for name, value in (("min_records", min_records), ("min_codons", min_codons),
                        ("max_records", max_records), ("max_total_bases", max_total_bases)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if min_records > max_records:
        raise ValueError("min_records cannot exceed max_records")
    if (isinstance(minimum_score_margin, bool)
            or not isinstance(minimum_score_margin, (int, float))
            or not isfinite(minimum_score_margin)
            or not 0 < minimum_score_margin <= 1):
        raise ValueError("minimum_score_margin must be finite and in (0, 1]")
    selected_ids: list[int] = []
    table_source = GENETIC_CODES if table_ids is None else table_ids
    for table_id in table_source:
        if len(selected_ids) >= len(GENETIC_CODES):
            raise ValueError("table_ids exceeds the supported candidate-table bound")
        selected_ids.append(table_id)
    if not selected_ids:
        raise ValueError("table_ids must be a non-empty sequence of unique supported IDs")
    for table_id in selected_ids:
        if isinstance(table_id, bool) or not isinstance(table_id, int) or table_id not in GENETIC_CODES:
            raise ValueError(f"Unsupported NCBI genetic code table: {table_id}")
    if len(selected_ids) < 2:
        raise ValueError("At least two supported candidate tables are required for ranking")
    if len(set(selected_ids)) != len(selected_ids):
        raise ValueError("table_ids must be a non-empty sequence of unique supported IDs")

    materialized: list[tuple[str, list[str], bool]] = []
    seen_ids: set[str] = set()
    seen_sequences: set[str] = set()
    total_bases = 0
    for index, record in enumerate(records):
        if len(materialized) >= max_records:
            raise ValueError("Input exceeds max_records")
        if not isinstance(record, Mapping):
            raise ValueError("Each record must be a mapping")
        sequence = record.get("sequence")
        if not isinstance(sequence, str):
            raise ValueError("Each record requires a sequence string")
        if len(sequence) > max_total_bases:
            raise ValueError("A record exceeds max_total_bases before normalization")
        normalized = "".join(sequence.split()).upper().replace("U", "T")
        if not normalized:
            raise ValueError("Sequences must not be empty")
        invalid = sorted(set(normalized) - set("ACGT"))
        if invalid:
            raise ValueError(f"Only unambiguous DNA/RNA bases are supported: {''.join(invalid)}")
        frame = record.get("frame", 0)
        if isinstance(frame, bool) or not isinstance(frame, int) or frame not in (0, 1, 2):
            raise ValueError("frame must be the integer 0, 1 or 2")
        complete = record.get("complete_cds", False)
        if not isinstance(complete, bool):
            raise ValueError("complete_cds must be a boolean")
        coding = normalized[frame:]
        if len(coding) % 3:
            raise ValueError("Each sequence must contain complete codons in its selected frame")
        codons = [coding[pos:pos + 3] for pos in range(0, len(coding), 3)]
        if not codons:
            raise ValueError("Each record must contain at least one complete codon")
        if complete and len(codons) < 2:
            raise ValueError("A complete CDS must contain distinct start and terminal codons")
        total_bases += len(coding)
        if total_bases > max_total_bases:
            raise ValueError("Input exceeds max_total_bases")
        record_id = record.get("id", f"record_{index + 1}")
        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError("record id must be non-empty text")
        if record_id in seen_ids:
            raise ValueError("record IDs must be unique")
        if normalized in seen_sequences:
            raise ValueError("duplicate coding sequences cannot be counted as independent evidence")
        seen_ids.add(record_id)
        seen_sequences.add(normalized)
        materialized.append((record_id, codons, complete))
    if not materialized:
        raise ValueError("At least one coding-sequence record is required")

    total_codons = sum(len(codons) for _, codons, _ in materialized)
    scores: list[dict[str, object]] = []
    for table_id in selected_ids:
        code = GENETIC_CODES[table_id]
        internal_stops = 0
        internal_codons = 0
        invalid_starts = 0
        complete_records = 0
        invalid_terminal_stops = 0
        for _, codons, complete in materialized:
            internal = codons[:-1] if complete else codons
            internal_stops += sum(codon in code.stops for codon in internal)
            internal_codons += len(internal)
            if complete:
                complete_records += 1
                invalid_starts += int(codons[0] not in code.starts)
                invalid_terminal_stops += int(codons[-1] not in code.stops)
        internal_rate = internal_stops / max(1, internal_codons)
        start_rate = invalid_starts / max(1, complete_records)
        terminal_rate = invalid_terminal_stops / max(1, complete_records)
        penalty = internal_rate + 0.25 * start_rate + 0.25 * terminal_rate
        scores.append({
            "table_id": table_id,
            "table_name": code.name,
            "penalty": penalty,
            "internal_stop_count": internal_stops,
            "internal_codon_count": internal_codons,
            "invalid_start_count": invalid_starts,
            "invalid_terminal_stop_count": invalid_terminal_stops,
            "complete_cds_count": complete_records,
        })
    scores.sort(key=lambda item: (cast(float, item["penalty"]), cast(int, item["table_id"])))
    enough = len(materialized) >= min_records and total_codons >= min_codons
    margin = cast(float, scores[1]["penalty"]) - cast(float, scores[0]["penalty"]) if len(scores) > 1 else 0.0
    selected = enough and margin >= minimum_score_margin
    warnings = [
        "Ranking uses only supplied coding-frame and optional complete-CDS evidence.",
        "No taxonomic context, codon-usage model, homolog alignment or transcript evidence is incorporated.",
        "A candidate table is not an organism identification or validated genetic-code assignment.",
        "Truth sets, independent confirmation, confusion matrices and calibrated abstention are required.",
    ]
    if not enough:
        warnings.append("Insufficient records or codons for the configured minimum evidence.")
    if not selected:
        warnings.append("No table selected: evidence is insufficient or the best-vs-runner-up margin is too small.")
    return {
        "schema": "kinetics.genetic-code-candidates.v1",
        "status": "candidate_table_ranked" if selected else ("insufficient_evidence" if not enough else "ambiguous_candidates"),
        "candidate_table_id": scores[0]["table_id"] if selected else None,
        "candidate_margin": margin,
        "minimum_score_margin": float(minimum_score_margin),
        "record_count": len(materialized),
        "codon_count": total_codons,
        "complete_cds_count": sum(int(complete) for _, _, complete in materialized),
        "ranked_candidates": scores,
        "warnings": warnings,
    }
