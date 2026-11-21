"""Bounded six-frame ORF candidate enumeration; not a gene annotation caller."""
from __future__ import annotations

from hashlib import sha256

from kinetics.genetic_code import GENETIC_CODES, translate_coding_sequence

# Hard ceiling on start-to-stop combinations examined across all six frames.
MAX_CANDIDATE_ORF_PAIRS = 1_000_000


def find_orf_candidates(
    sequence: str,
    *,
    table_id: int = 11,
    min_protein_length: int = 30,
    max_orfs: int = 10_000,
    max_sequence_bases: int = 100_000_000,
    max_open_starts: int = 100_000,
    max_candidate_orf_pairs_total: int | None = None,
) -> dict[str, object]:
    """Enumerate complete start-to-stop ORFs on both strands and all frames.

    Coordinates are 0-based, half-open on the normalized input sequence. Nested
    starts are retained. Only canonical DNA/RNA is accepted; no code is inferred.
    """
    if (
        isinstance(table_id, bool)
        or not isinstance(table_id, int)
        or table_id not in GENETIC_CODES
    ):
        raise ValueError(f"Unsupported NCBI genetic code table: {table_id}")
    if (
        not isinstance(min_protein_length, int)
        or isinstance(min_protein_length, bool)
        or min_protein_length < 1
    ):
        raise ValueError("min_protein_length must be a positive integer")
    if not isinstance(max_orfs, int) or isinstance(max_orfs, bool) or max_orfs < 1:
        raise ValueError("max_orfs must be a positive integer")
    if not isinstance(max_sequence_bases, int) or isinstance(max_sequence_bases, bool) or max_sequence_bases < 1:
        raise ValueError("max_sequence_bases must be a positive integer")
    if not isinstance(max_open_starts, int) or isinstance(max_open_starts, bool) or max_open_starts < 1:
        raise ValueError("max_open_starts must be a positive integer")
    if max_candidate_orf_pairs_total is None:
        max_candidate_orf_pairs_total = MAX_CANDIDATE_ORF_PAIRS
    if (not isinstance(max_candidate_orf_pairs_total, int)
            or isinstance(max_candidate_orf_pairs_total, bool)
            or not 1 <= max_candidate_orf_pairs_total <= MAX_CANDIDATE_ORF_PAIRS):
        raise ValueError("max_candidate_orf_pairs_total must be between 1 and the hard ceiling")
    dna = "".join(sequence.split()).upper().replace("U", "T")
    if not dna:
        raise ValueError("Genome sequence must not be empty")
    if len(dna) > max_sequence_bases:
        raise ValueError("Genome sequence exceeds max_sequence_bases")
    invalid = sorted(set(dna) - set("ACGT"))
    if invalid:
        raise ValueError(f"ORF scan requires unambiguous DNA/RNA bases: {''.join(invalid)}")

    reverse = dna.translate(str.maketrans("ACGT", "TGCA"))[::-1]
    code = GENETIC_CODES[table_id]
    orfs: list[dict[str, object]] = []
    candidate_pairs_examined = 0

    for strand, oriented in (("+", dna), ("-", reverse)):
        for frame in range(3):
            open_starts: list[int] = []
            for position in range(frame, len(oriented) - 2, 3):
                codon = oriented[position:position + 3]
                if codon in code.starts:
                    if len(open_starts) >= max_open_starts:
                        raise ValueError("Open ORF start count exceeds max_open_starts")
                    open_starts.append(position)
                if codon in code.stops:
                    for start in open_starts:
                        candidate_pairs_examined += 1
                        if candidate_pairs_examined > max_candidate_orf_pairs_total:
                            raise ValueError(
                                "ORF start-to-stop candidate work exceeds "
                                "MAX_CANDIDATE_ORF_PAIRS"
                            )
                        coding_sequence = oriented[start:position + 3]
                        translated = translate_coding_sequence(
                            coding_sequence, table_id=table_id, cds=True,
                        )["protein"]
                        if not isinstance(translated, str):
                            raise RuntimeError("Genetic-code translator returned a non-string protein")
                        protein = translated
                        if len(protein) < min_protein_length:
                            continue
                        if len(orfs) >= max_orfs:
                            raise ValueError("ORF count exceeds max_orfs")
                        if strand == "+":
                            start_coordinate, end_coordinate = start, position + 3
                        else:
                            start_coordinate, end_coordinate = (
                                len(dna) - (position + 3),
                                len(dna) - start,
                            )
                        orfs.append({
                            "start": start_coordinate,
                            "end": end_coordinate,
                            "strand": strand,
                            "frame": frame,
                            "start_codon": oriented[start:start + 3],
                            "stop_codon": codon,
                            "nucleotide_length": position + 3 - start,
                            "protein": protein,
                            "protein_length": len(protein),
                        })
                    open_starts = []

    return {
        "sequence_sha256": sha256(dna.encode("ascii")).hexdigest(),
        "sequence_length": len(dna),
        "table_id": table_id,
        "table_name": code.name,
        "coordinate_system": "0-based half-open on normalized input sequence",
        "min_protein_length": min_protein_length,
        "resource_limits": {
            "max_orfs": max_orfs,
            "max_sequence_bases": max_sequence_bases,
            "max_open_starts_per_frame": max_open_starts,
            "max_candidate_orf_pairs_total": max_candidate_orf_pairs_total,
            "candidate_orf_pairs_examined": candidate_pairs_examined,
        },
        "orf_count": len(orfs),
        "orfs": orfs,
        "limitations": [
            "Heuristic complete ORF enumeration only; not a gene prediction or annotation pipeline",
            "No promoter, ribosome-binding site, splice site, intron, transcript or operon model",
            "Genomic eukaryotic genes commonly contain introns and cannot be annotated by this ORF scan alone",
            "No organism identity, genetic-code inference, protein family, domain or function prediction",
            "Results depend on the explicitly selected translation table and minimum length threshold",
        ],
    }
