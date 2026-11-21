"""Optional Biopython pairwise-alignment engine behind Molecularis-owned results.

Biopython objects are deliberately not returned from this module. The result contains
only primitive values so callers remain independent of the optional dependency.
"""
from __future__ import annotations

from math import isfinite
from typing import Literal


def align_pairwise_biopython(
    sequence_a: str,
    sequence_b: str,
    *,
    mode: Literal["global", "local"] = "global",
    match_score: float = 2.0,
    mismatch_score: float = -1.0,
    gap_open_score: float = -5.0,
    gap_extend_score: float = -1.0,
    max_sequence_length: int = 100_000,
) -> dict[str, object]:
    """Align two sequences with Biopython's PairwiseAligner.

    Gap scores follow Biopython's convention: opening a gap incurs the open
    score, and each subsequent extension incurs the extension score. The
    first optimal alignment is returned; ties are not enumerated.
    """
    if mode not in {"global", "local"}:
        raise ValueError("mode must be 'global' or 'local'")
    for name, value in (
        ("match_score", match_score),
        ("mismatch_score", mismatch_score),
        ("gap_open_score", gap_open_score),
        ("gap_extend_score", gap_extend_score),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"{name} must be a finite number")
    if gap_open_score > 0 or gap_extend_score > 0:
        raise ValueError("gap scores must be zero or negative")
    if (
        isinstance(max_sequence_length, bool)
        or not isinstance(max_sequence_length, int)
        or max_sequence_length < 1
    ):
        raise ValueError("max_sequence_length must be a positive integer")
    if not isinstance(sequence_a, str) or not isinstance(sequence_b, str):
        raise TypeError("sequences must be strings")
    a, b = sequence_a.upper(), sequence_b.upper()
    if not a or not b:
        raise ValueError("Both sequences must be non-empty")
    if len(a) > max_sequence_length or len(b) > max_sequence_length:
        raise ValueError("Sequence exceeds configured max_sequence_length")

    try:
        import Bio
        from Bio.Align import PairwiseAligner
    except ImportError as error:
        raise RuntimeError(
            "Biopython is unavailable; install the pinned optional alignment profile"
        ) from error

    aligner = PairwiseAligner()
    aligner.mode = mode
    aligner.match_score = float(match_score)
    aligner.mismatch_score = float(mismatch_score)
    aligner.open_gap_score = float(gap_open_score)
    aligner.extend_gap_score = float(gap_extend_score)
    alignment = next(iter(aligner.align(a, b)))
    coordinates = [
        [int(alignment.coordinates[0, index]), int(alignment.coordinates[1, index])]
        for index in range(alignment.coordinates.shape[1])
    ]
    return {
        "schema_version": 1,
        "engine": "biopython.PairwiseAligner",
        "engine_version": str(Bio.__version__),
        "algorithm": str(aligner.algorithm),
        "mode": mode,
        "score": float(alignment.score),
        "coordinates": coordinates,
        "sequence_lengths": [len(a), len(b)],
        "scoring": {
            "match": float(match_score),
            "mismatch": float(mismatch_score),
            "gap_open": float(gap_open_score),
            "gap_extend": float(gap_extend_score),
        },
        "tie_policy": "first alignment returned by the pinned Biopython implementation",
        "limitations": [
            "Returns alignment coordinates and score, not a rendered alignment or CIGAR.",
            "No substitution matrix, strand search, read mapping or database indexing.",
            "No guarantee that tied optimal tracebacks are stable across engine versions.",
        ],
    }
