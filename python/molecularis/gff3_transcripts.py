"""Bounded reconstruction of transcript CDS models from supplied GFF3 and genome records.

This reconstructs annotation supplied by the caller; it does not discover genes,
transcripts, splice sites, promoters or biological function.
"""
from __future__ import annotations

from collections import defaultdict
from typing import TypedDict, cast

from .genetic_code import translate_coding_sequence
from .sequence import reverse_complement


class _Feature(TypedDict):
    seqid: str
    source: str
    type: str
    start: int
    end: int
    score: float | None
    strand: str
    phase: int | None
    attributes: dict[str, str]


def reconstruct_gff3_cds(
    annotation: dict[str, object],
    contigs: dict[str, str],
    *,
    table_id: int = 11,
    max_transcripts: int = 100_000,
    max_total_cds_bases: int = 100_000_000,
) -> dict[str, object]:
    """Reconstruct spliced CDS sequences using GFF3 coordinates and phases.

    Coordinates are converted from 1-based inclusive. Minus-strand segments are
    reverse-complemented and concatenated in transcriptional order. Phase
    continuity is checked across segments. Translation is attempted only for
    complete, canonical CDSs with a valid start, stop and no internal stop.
    """
    for name, value in (
        ("max_transcripts", max_transcripts),
        ("max_total_cds_bases", max_total_cds_bases),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if annotation.get("schema") != "kinetics.gff3-annotation-import.v1":
        raise ValueError("annotation must be a validated Kinetics GFF3 import result")
    raw_features = annotation.get("features")
    if not isinstance(raw_features, list):
        raise ValueError("annotation features must be a list")

    features = cast(list[_Feature], raw_features)
    transcripts: dict[str, _Feature] = {}
    cds_by_transcript: dict[str, list[_Feature]] = defaultdict(list)
    for feature in features:
        identifier = feature["attributes"].get("ID")
        if feature["type"].lower() in {"mrna", "transcript"} and identifier:
            if identifier in transcripts:
                raise ValueError(f"Duplicate transcript ID: {identifier}")
            transcripts[identifier] = feature
        if feature["type"] == "CDS":
            parents = feature["attributes"].get("Parent", "")
            if not parents:
                raise ValueError("Every CDS feature must name at least one transcript Parent")
            for parent in parents.split(","):
                cds_by_transcript[parent].append(feature)

    if not cds_by_transcript:
        raise ValueError("Annotation contains no CDS features")
    if len(cds_by_transcript) > max_transcripts:
        raise ValueError("Transcript count exceeds max_transcripts")

    results: list[dict[str, object]] = []
    total_bases = 0
    for transcript_id in sorted(cds_by_transcript):
        transcript = transcripts.get(transcript_id)
        if transcript is None:
            raise ValueError(f"CDS Parent {transcript_id!r} is not an imported transcript feature")
        segments = cds_by_transcript[transcript_id]
        seqid = transcript["seqid"]
        strand = transcript["strand"]
        if strand not in {"+", "-"}:
            raise ValueError(f"Transcript {transcript_id!r} must have an explicit strand")
        if any(
            segment["seqid"] != seqid or segment["strand"] != strand
            for segment in segments
        ):
            raise ValueError(
                f"Transcript {transcript_id!r} has inconsistent CDS sequence or strand"
            )
        if any(
            segment["start"] < transcript["start"] or segment["end"] > transcript["end"]
            for segment in segments
        ):
            raise ValueError(f"Transcript {transcript_id!r} has CDS outside transcript bounds")
        genome = contigs.get(seqid)
        if genome is None:
            raise ValueError(f"Genome sequence {seqid!r} is missing")
        genome = "".join(genome.split()).upper().replace("U", "T")
        if any(segment["end"] > len(genome) for segment in segments):
            raise ValueError(f"Transcript {transcript_id!r} CDS exceeds genome sequence bounds")

        ordered = sorted(
            segments,
            key=lambda item: item["start"],
            reverse=strand == "-",
        )
        pieces: list[str] = []
        phase_rows: list[dict[str, int]] = []
        coding_length = 0
        first_phase = 0
        phase_consistent = True
        for index, segment in enumerate(ordered):
            phase = segment["phase"]
            if phase is None:
                raise ValueError("CDS phase is required for every CDS segment")
            expected_phase = (
                phase if index == 0
                else (3 - (coding_length - first_phase) % 3) % 3
            )
            if index == 0:
                first_phase = phase
            if phase != expected_phase:
                phase_consistent = False
            left, right = segment["start"] - 1, segment["end"]
            piece = genome[left:right]
            if strand == "-":
                piece = reverse_complement(piece)
            pieces.append(piece)
            phase_rows.append({
                "start": segment["start"],
                "end": segment["end"],
                "phase": phase,
                "expected_phase": expected_phase,
            })
            coding_length += len(piece)
        coding_sequence = "".join(pieces)
        total_bases += len(coding_sequence)
        if total_bases > max_total_cds_bases:
            raise ValueError("Reconstructed CDS work exceeds max_total_cds_bases")

        translation: str | None = None
        translation_status = "not_attempted"
        translation_reason: str | None = None
        if not phase_consistent:
            translation_status = "abstained"
            translation_reason = "CDS phase continuity is inconsistent"
        elif ordered[0]["phase"] != 0:
            translation_status = "partial_cds"
            translation_reason = (
                "First CDS phase is non-zero; complete 5-prime CDS is not established"
            )
        else:
            try:
                translated = translate_coding_sequence(
                    coding_sequence, table_id=table_id, cds=True,
                )
                translation_value = translated["protein"]
                if not isinstance(translation_value, str):
                    raise RuntimeError("Translator returned a non-string protein")
                translation = translation_value
                translation_status = "translated"
            except ValueError as exc:
                translation_status = "abstained"
                translation_reason = str(exc)

        results.append({
            "transcript_id": transcript_id,
            "seqid": seqid,
            "strand": strand,
            "cds_segment_count": len(ordered),
            "cds_length": len(coding_sequence),
            "coordinate_system": (
                "1-based inclusive GFF3 input; spliced sequence in transcriptional orientation"
            ),
            "phase_consistent": phase_consistent,
            "segment_phases": phase_rows,
            "cds_sequence": coding_sequence,
            "translation_status": translation_status,
            "protein_sequence": translation,
            "translation_reason": translation_reason,
        })

    return {
        "schema": "kinetics.gff3-transcript-cds.v1",
        "table_id": table_id,
        "transcript_count": len(results),
        "total_cds_bases": total_bases,
        "transcripts": results,
        "limitations": [
            ("Reconstructs caller-supplied GFF3 CDS annotations; does not predict "
             "genes or transcripts"),
            ("No splice-site, promoter, transcript completeness or alternative-splicing "
             "inference is performed"),
            ("Translation is emitted only when supplied phases and explicit translation "
             "table permit complete-CDS validation"),
            "No organism or genetic code is inferred; table_id is caller-selected",
            "Protein family, domain, function and biological validity are not established",
        ],
    }
