"""Transparent PCR/CRISPR sequence utilities; not a clinical or wet-lab substitute."""
from __future__ import annotations

from typing import cast

from .sequence import DNA, _normalise, validate_sequence

_WALLACE = {"A": 2.0, "T": 2.0, "G": 4.0, "C": 4.0}


def primer_properties(sequence: str) -> dict[str, float | int | bool | str]:
    seq = _normalise(sequence)
    validate_sequence(seq, DNA)
    if not 15 <= len(seq) <= 40:
        raise ValueError("Primer length must be between 15 and 40 nt for this screening utility")
    canonical = set(seq) <= set("ACGT")
    if not canonical:
        raise ValueError("Primer screening requires unambiguous A/C/G/T bases")
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    tm = sum(_WALLACE[base] for base in seq)
    return {
        "length": len(seq),
        "gc_fraction": gc,
        "wallace_tm_c": tm,
        "gc_clamp": seq[-1] in "GC",
        "screening_flags": not (0.35 <= gc <= 0.65 and 45 <= tm <= 75),
        "limitations": "Wallace estimate only; no salt, Mg2+, concentration, hairpin or dimer model",
    }


def scan_spcas9_ngg(sequence: str, *, strand: str = "both") -> list[dict[str, object]]:
    """Find NGG PAM sites on either strand; coordinates are 0-based half-open."""
    seq = _normalise(sequence)
    validate_sequence(seq, DNA)
    if strand not in {"both", "+", "-"}:
        raise ValueError("strand must be both, + or -")
    results: list[dict[str, object]] = []
    if strand in {"both", "+"}:
        for index in range(max(0, len(seq) - 2)):
            pam = seq[index:index + 3]
            if len(pam) == 3 and pam[1:] == "GG":
                results.append({"strand": "+", "start": index, "end": index + 3, "pam": pam})
    if strand in {"both", "-"}:
        reverse = seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]
        for index in range(max(0, len(reverse) - 2)):
            pam = reverse[index:index + 3]
            if len(pam) == 3 and pam[1:] == "GG":
                start = len(seq) - (index + 3)
                results.append({"strand": "-", "start": start, "end": start + 3, "pam": pam})
    return sorted(results, key=lambda item: (cast(int, item["start"]), str(item["strand"])))
