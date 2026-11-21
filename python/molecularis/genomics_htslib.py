"""Optional pysam/HTSlib alignment reader for BAM and CRAM.

This is a lazy host-side adapter. pysam/HTSlib is not currently bundled in Android.
CRAM access requires an explicit local reference FASTA; remote reference retrieval is
never enabled implicitly.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

from .genomics import SamRecord


def _pysam() -> Any:
    try:
        import pysam  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "pysam/HTSlib is unavailable; install an approved pinned pysam build "
            "before reading indexed BAM/CRAM files"
        ) from error
    return pysam


def iter_alignment_records(
    path: str | Path, *, reference_fasta: str | Path | None = None,
    region: tuple[str, int, int] | None = None,
) -> Iterator[SamRecord]:
    """Stream core alignment fields from BAM/CRAM using HTSlib.

    Region coordinates are 1-based inclusive. Region reads require an index.
    For CRAM, reference_fasta must point to a local FASTA; no network fallback occurs.
    """
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    suffix = source.suffix.lower()
    if suffix not in {".bam", ".cram"}:
        raise ValueError("Alignment input must have a .bam or .cram suffix")
    if suffix == ".cram" and reference_fasta is None:
        raise ValueError("CRAM decoding requires an explicit local reference FASTA")
    if reference_fasta is not None and not Path(reference_fasta).is_file():
        raise FileNotFoundError(reference_fasta)
    if region is not None:
        contig, start, end = region
        if not contig or not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
            raise ValueError("Region must be (contig, 1-based start, 1-based inclusive end)")

    pysam = _pysam()
    mode = "rc" if suffix == ".cram" else "rb"
    kwargs = {"reference_filename": str(reference_fasta)} if reference_fasta is not None else {}
    with pysam.AlignmentFile(str(source), mode, **kwargs) as handle:
        if region is None:
            iterator = handle.fetch(until_eof=True)
        else:
            if not handle.has_index():
                raise ValueError("Indexed region access requires a BAM/CRAM index")
            iterator = handle.fetch(region[0], region[1] - 1, region[2])

        for record in iterator:
            sequence = record.query_sequence or "*"
            if record.query_qualities is None:
                quality = "*"
            else:
                if len(record.query_qualities) != len(sequence) or any(
                    score < 0 or score > 93 for score in record.query_qualities
                ):
                    raise ValueError("HTSlib returned invalid sequence/quality data")
                quality = "".join(chr(score + 33) for score in record.query_qualities)
            yield SamRecord(
                query_name=record.query_name or "*",
                flag=int(record.flag),
                reference=record.reference_name or "*",
                position=int(record.reference_start + 1) if record.reference_start >= 0 else 0,
                mapq=int(record.mapping_quality),
                cigar=record.cigarstring or "*",
                sequence=sequence,
                quality=quality,
            )
