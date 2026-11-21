"""Deterministic sequence parsing and analysis primitives; research use only."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Iterator

DNA = frozenset("ACGTRYSWKMBDHVN")
RNA = frozenset("ACGURYSWKMBDHVN")
PROTEIN = frozenset("ACDEFGHIKLMNPQRSTVWYBXZJUO*")
_COMPLEMENT = str.maketrans("ACGTRYMKSWBDHVNacgtrymkswbdhvn", "TGCAYRKM SWVHDBNtg cayrkm swvhdbn".replace(" ", ""))

@dataclass(frozen=True)
class SequenceRecord:
    identifier: str
    sequence: str
    description: str = ""

def _normalise(sequence: str) -> str:
    return "".join(sequence.split()).upper()

def iter_fasta_records(lines: Iterable[str]) -> Iterator[SequenceRecord]:
    """Yield FASTA records incrementally from an iterable of text lines."""
    header: str | None = None
    chunks: list[str] = []
    found = False
    for line_no, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith(">"):
            if header is not None:
                found = True
                yield _fasta_record(header, chunks)
            header, chunks = line[1:].strip(), []
            if not header:
                raise ValueError(f"FASTA line {line_no}: empty identifier")
        elif header is None:
            raise ValueError(f"FASTA line {line_no}: sequence before first header")
        else:
            chunks.append(line)
    if header is not None:
        found = True
        yield _fasta_record(header, chunks)
    if not found:
        raise ValueError("FASTA contains no records")


def parse_fasta(text: str) -> list[SequenceRecord]:
    """Parse FASTA text; use iter_fasta_records for large streaming inputs."""
    return list(iter_fasta_records(text.splitlines()))

def _fasta_record(header: str, chunks: list[str]) -> SequenceRecord:
    fields = header.split(maxsplit=1)
    seq = _normalise("".join(chunks))
    if not seq:
        raise ValueError(f"FASTA record {fields[0]!r}: empty sequence")
    return SequenceRecord(fields[0], seq, fields[1] if len(fields) > 1 else "")

def iter_fastq_records(
    lines: Iterable[str],
    *,
    max_records: int = 10_000_000,
    max_total_bases: int = 1_000_000_000,
    max_record_bases: int = 10_000_000,
) -> Iterator[tuple[SequenceRecord, str]]:
    """Stream wrapped FASTQ records with explicit record and base ceilings."""
    for name, limit in (
        ("max_records", max_records),
        ("max_total_bases", max_total_bases),
        ("max_record_bases", max_record_bases),
    ):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError(f"{name} must be a positive integer")
    iterator = iter(enumerate(lines, 1))
    record_count = 0
    total_bases = 0
    while True:
        header_line = None
        for item in iterator:
            if item[1].strip():
                header_line = item
                break
        if header_line is None:
            break
        line_number, header = header_line
        if not header.startswith("@") or not header[1:].strip():
            raise ValueError(f"FASTQ line {line_number}: invalid record header")
        fields = header[1:].strip().split(maxsplit=1)
        identifier = fields[0]
        description = fields[1] if len(fields) > 1 else ""
        sequence_chunks: list[str] = []
        sequence_length = 0
        plus_line = None
        for current_line, raw in iterator:
            line = raw.rstrip("\r\n")
            if line.startswith("+"):
                plus_line = (current_line, line)
                break
            if not line:
                raise ValueError(f"FASTQ line {current_line}: empty sequence line")
            chunk = _normalise(line)
            sequence_length += len(chunk)
            if sequence_length > max_record_bases:
                raise ValueError(f"FASTQ record {identifier!r} exceeds max_record_bases")
            sequence_chunks.append(chunk)
        if plus_line is None:
            raise ValueError(f"FASTQ record {identifier!r}: missing '+' separator")
        plus_identifier = plus_line[1][1:].strip().split(maxsplit=1)
        if plus_identifier and plus_identifier[0] != identifier:
            raise ValueError(f"FASTQ record {identifier!r}: separator identifier mismatch")
        sequence = "".join(sequence_chunks)
        if not sequence:
            raise ValueError(f"FASTQ record {identifier!r}: empty sequence")
        validate_sequence(sequence, DNA)
        quality_chunks: list[str] = []
        quality_length = 0
        while quality_length < sequence_length:
            try:
                quality_line_number, raw_quality = next(iterator)
            except StopIteration as exc:
                raise ValueError(
                    f"FASTQ record {identifier!r}: sequence/quality length mismatch"
                ) from exc
            quality = raw_quality.rstrip("\r\n")
            if not quality:
                raise ValueError(f"FASTQ line {quality_line_number}: empty quality line")
            if any(not 33 <= ord(char) <= 126 for char in quality):
                raise ValueError(f"FASTQ line {quality_line_number}: invalid quality character")
            if len(quality) > sequence_length - quality_length:
                raise ValueError(f"FASTQ record {identifier!r}: sequence/quality length mismatch")
            quality_chunks.append(quality)
            quality_length += len(quality)
        record_count += 1
        total_bases += sequence_length
        if record_count > max_records:
            raise ValueError("FASTQ exceeds max_records")
        if total_bases > max_total_bases:
            raise ValueError("FASTQ exceeds max_total_bases")
        yield SequenceRecord(identifier, sequence, description), "".join(quality_chunks)
    if record_count == 0:
        raise ValueError("FASTQ contains no records")


def parse_fastq(text: str) -> list[tuple[SequenceRecord, str]]:
    """Parse FASTQ text into memory; use iter_fastq_records for bounded streaming."""
    return list(iter_fastq_records(text.splitlines()))

def validate_sequence(sequence: str, alphabet: Iterable[str] = DNA) -> None:
    invalid = sorted(set(_normalise(sequence)) - set(alphabet))
    if invalid:
        raise ValueError(f"Invalid symbols: {''.join(invalid)}")

def sequence_statistics(sequence: str) -> dict[str, float | int]:
    seq = _normalise(sequence)
    if not seq:
        raise ValueError("Sequence is empty")
    counts = Counter(seq)
    canonical = sum(counts[b] for b in "ACGT")
    return {"length": len(seq), "gc_fraction": (counts["G"] + counts["C"]) / len(seq),
            "ambiguous_count": len(seq) - canonical, "a": counts["A"], "c": counts["C"],
            "g": counts["G"], "t": counts["T"], "other": len(seq) - canonical}

def reverse_complement(sequence: str) -> str:
    seq = _normalise(sequence)
    validate_sequence(seq, DNA)
    return seq.translate(_COMPLEMENT)[::-1]

def transcribe(sequence: str) -> str:
    seq = _normalise(sequence)
    validate_sequence(seq, DNA)
    return seq.replace("T", "U")

def kmer_counts(sequence: str, k: int, *, canonical_only: bool = True) -> dict[str, int]:
    seq = _normalise(sequence)
    if k < 1:
        raise ValueError("k must be >= 1")
    counts: Counter[str] = Counter()
    alphabet = set("ACGT")
    for i in range(len(seq) - k + 1):
        word = seq[i:i+k]
        if not canonical_only or set(word) <= alphabet:
            counts[word] += 1
    return dict(sorted(counts.items()))

def needleman_wunsch(a: str, b: str, *, match: int = 2, mismatch: int = -1,
                     gap: int = -2, max_cells: int = 4_000_000) -> dict[str, object]:
    """Global linear-gap alignment. Returns one deterministic optimal traceback."""
    x, y = _normalise(a), _normalise(b)
    if not x or not y:
        raise ValueError("Both sequences must be non-empty")
    rows, cols = len(x) + 1, len(y) + 1
    if max_cells < 1 or rows * cols > max_cells:
        raise ValueError("Alignment exceeds the configured memory-cell limit")
    score = [[0] * cols for _ in range(rows)]
    trace = [[""] * cols for _ in range(rows)]
    for i in range(1, rows):
        score[i][0], trace[i][0] = i * gap, "U"
    for j in range(1, cols):
        score[0][j], trace[0][j] = j * gap, "L"
    for i in range(1, rows):
        for j in range(1, cols):
            choices = (score[i-1][j-1] + (match if x[i-1] == y[j-1] else mismatch),
                       score[i-1][j] + gap, score[i][j-1] + gap)
            best = max(choices)
            score[i][j] = best
            trace[i][j] = "D" if choices[0] == best else ("U" if choices[1] == best else "L")
    ax, ay, i, j = [], [], len(x), len(y)
    while i or j:
        direction = trace[i][j]
        if direction == "D": ax.append(x[i-1]); ay.append(y[j-1]); i -= 1; j -= 1
        elif direction == "U": ax.append(x[i-1]); ay.append("-"); i -= 1
        elif direction == "L": ax.append("-"); ay.append(y[j-1]); j -= 1
        else: raise RuntimeError("Invalid alignment traceback")
    return {"score": score[-1][-1], "aligned_a": "".join(reversed(ax)),
            "aligned_b": "".join(reversed(ay)), "algorithm": "Needleman-Wunsch-linear-gap",
            "scoring": {"match": match, "mismatch": mismatch, "gap": gap}}


def trim_fastq_ends(
    record: SequenceRecord, quality: str, *, phred_offset: int = 33,
    minimum_quality: int = 20, minimum_length: int = 1,
) -> dict[str, object] | None:
    """Trim terminal low-quality bases only; returns None when below minimum_length.

    This does not perform adapter trimming, sliding-window trimming or paired-read rescue.
    """
    if phred_offset not in (33, 64):
        raise ValueError("Phred offset must be explicitly 33 or 64")
    if not 0 <= minimum_quality <= 93 or minimum_length < 1:
        raise ValueError("Quality threshold must be 0..93 and minimum_length >=1")
    if len(record.sequence) != len(quality):
        raise ValueError("Sequence/quality length mismatch")
    scores = [ord(char) - phred_offset for char in quality]
    if any(score < 0 or score > 93 for score in scores):
        raise ValueError("Quality character outside supported Phred range")
    left, right = 0, len(scores)
    while left < right and scores[left] < minimum_quality:
        left += 1
    while right > left and scores[right - 1] < minimum_quality:
        right -= 1
    if right - left < minimum_length:
        return None
    trimmed = SequenceRecord(
        record.identifier, record.sequence[left:right], record.description,
    )
    return {
        "record": trimmed,
        "quality": quality[left:right],
        "trimmed_left": left,
        "trimmed_right": len(quality) - right,
        "algorithm": "terminal low-quality trimming",
        "limitations": ["No adapter trimming", "No sliding-window quality model"],
    }
