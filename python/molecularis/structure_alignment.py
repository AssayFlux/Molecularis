"""Bounded semi-global sequence-to-structure alignment with ambiguity abstention.

This maps coordinates only. It does not model mutations or infer biological
function, stability, pathogenicity, or clinical significance.
"""
from __future__ import annotations

from math import isfinite
from typing import Iterable

from .sequence_structure import THREE_TO_ONE
from .structure import Atom


def map_chain_sequence_by_alignment(
    query_sequence: str,
    atoms: Iterable[Atom],
    *,
    chain_id: str,
    match_score: int = 2,
    mismatch_score: int = -1,
    gap_score: int = -2,
    minimum_identity: float = 0.8,
    minimum_structure_coverage: float = 0.8,
    max_query_residues: int = 20_000,
    max_structure_residues: int = 20_000,
    max_atoms: int = 200_000,
    max_alignment_cells: int = 2_000_000,
) -> dict[str, object]:
    """Align a complete observed chain to a query subsequence and map exact pairs.

    Query prefix/suffix overhangs are free; internal insertions/deletions use a
    linear gap score. If more than one optimal placement/traceback exists, the
    function abstains rather than selecting an arbitrary coordinate mapping.
    Only identical aligned residues are mapped.
    """
    if not isinstance(query_sequence, str) or not query_sequence.strip():
        raise ValueError("query_sequence must be non-empty text")
    query = "".join(query_sequence.split()).upper()
    if set(query) - set(THREE_TO_ONE.values()):
        raise ValueError("query_sequence must contain only canonical amino acids")
    if not isinstance(chain_id, str) or not chain_id:
        raise ValueError("chain_id must be non-empty text")
    for name, value in (
        ("match_score", match_score),
        ("mismatch_score", mismatch_score),
        ("gap_score", gap_score),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer")
    for name, limit in (
        ("max_query_residues", max_query_residues),
        ("max_structure_residues", max_structure_residues),
        ("max_atoms", max_atoms),
        ("max_alignment_cells", max_alignment_cells),
    ):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError(f"{name} must be a positive integer")
    if match_score <= 0 or mismatch_score >= match_score or gap_score >= 0:
        raise ValueError("Alignment scores must satisfy match > 0, mismatch < match and gap < 0")
    for name, threshold in (
        ("minimum_identity", minimum_identity),
        ("minimum_structure_coverage", minimum_structure_coverage),
    ):
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or not isfinite(threshold):
            raise ValueError(f"{name} must be a finite number between 0 and 1")
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(f"{name} must be a finite number between 0 and 1")
    if len(query) > max_query_residues:
        raise ValueError("Query sequence exceeds max_query_residues")

    residues: dict[int, str] = {}
    residue_names: dict[int, str] = {}
    atom_count = 0
    for atom in atoms:
        atom_count += 1
        if atom_count > max_atoms:
            raise ValueError("Structure exceeds max_atoms")
        if atom.chain != chain_id:
            continue
        if atom.residue_number not in residues and len(residues) >= max_structure_residues:
            raise ValueError("Structure chain exceeds max_structure_residues")
        residue_name = atom.residue.upper()
        amino_acid = THREE_TO_ONE.get(residue_name)
        if amino_acid is None:
            raise ValueError(f"Unsupported/non-standard residue {residue_name}; alignment abstained")
        previous = residues.setdefault(atom.residue_number, amino_acid)
        previous_name = residue_names.setdefault(atom.residue_number, residue_name)
        if previous != amino_acid or previous_name != residue_name:
            raise ValueError("Conflicting residue identity at one chain position")
    ordered = sorted(residues.items())
    if not ordered:
        raise ValueError(f"No canonical residues found for chain {chain_id}")
    if any(
        current != previous + 1
        for (previous, _), (current, _) in zip(ordered, ordered[1:])
    ):
        return {
            "schema": "kinetics.structure-alignment-map.v1",
            "status": "abstained_noncontiguous_structure_numbering",
            "chain_id": chain_id,
            "mapped_residues": [],
            "limitations": ["Insertion codes and residue-number gaps are not reconstructed."],
        }
    if len(ordered) > max_structure_residues:
        raise ValueError("Structure chain exceeds max_structure_residues")
    structure_sequence = "".join(amino_acid for _, amino_acid in ordered)
    rows, cols = len(query) + 1, len(structure_sequence) + 1
    if rows * cols > max_alignment_cells:
        raise ValueError("Alignment exceeds max_alignment_cells")

    scores = [[0] * cols for _ in range(rows)]
    counts = [[0] * cols for _ in range(rows)]
    traces = [[""] * cols for _ in range(rows)]
    for i in range(rows):
        counts[i][0] = 1
        traces[i][0] = "S"  # free query prefix
    for j in range(1, cols):
        scores[0][j] = j * gap_score
        counts[0][j] = 1
        traces[0][j] = "L"

    for i in range(1, rows):
        for j in range(1, cols):
            diagonal = scores[i - 1][j - 1] + (
                match_score if query[i - 1] == structure_sequence[j - 1] else mismatch_score
            )
            up = scores[i - 1][j] + gap_score
            left = scores[i][j - 1] + gap_score
            best = max(diagonal, up, left)
            choices = []
            if diagonal == best:
                choices.append(("D", counts[i - 1][j - 1]))
            if up == best:
                choices.append(("U", counts[i - 1][j]))
            if left == best:
                choices.append(("L", counts[i][j - 1]))
            scores[i][j] = best
            counts[i][j] = min(2, sum(count for _, count in choices))
            traces[i][j] = choices[0][0]

    best_score = max(scores[i][cols - 1] for i in range(rows))
    endpoints = [i for i in range(rows) if scores[i][cols - 1] == best_score]
    path_count = min(2, sum(counts[i][cols - 1] for i in endpoints))
    if path_count != 1:
        return {
            "schema": "kinetics.structure-alignment-map.v1",
            "status": "abstained_ambiguous_optimal_alignment",
            "chain_id": chain_id,
            "alignment_score": best_score,
            "optimal_endpoint_count": len(endpoints),
            "mapped_residues": [],
            "limitations": ["Multiple optimal alignments exist; no coordinate placement was selected."],
        }

    i, j = endpoints[0], cols - 1
    aligned: list[tuple[int, int, bool]] = []
    while j > 0:
        direction = traces[i][j]
        if direction == "D":
            aligned.append((i - 1, j - 1, query[i - 1] == structure_sequence[j - 1]))
            i -= 1
            j -= 1
        elif direction == "U":
            i -= 1
        elif direction == "L":
            j -= 1
        else:
            raise RuntimeError("Invalid alignment traceback state")
    aligned.reverse()
    matched = [(qi, sj) for qi, sj, identical in aligned if identical]
    identity = len(matched) / len(aligned) if aligned else 0.0
    coverage = len(matched) / len(ordered)
    if identity < minimum_identity or coverage < minimum_structure_coverage:
        return {
            "schema": "kinetics.structure-alignment-map.v1",
            "status": "abstained_below_mapping_threshold",
            "chain_id": chain_id,
            "alignment_score": best_score,
            "aligned_pair_count": len(aligned),
            "identity": identity,
            "structure_coverage": coverage,
            "minimum_identity": float(minimum_identity),
            "minimum_structure_coverage": float(minimum_structure_coverage),
            "mapped_residues": [],
            "limitations": ["Alignment did not meet caller-selected identity/coverage thresholds."],
        }

    mapped = [
        {
            "query_position_1based": qi + 1,
            "chain_id": chain_id,
            "structure_residue_number": ordered[sj][0],
            "residue_name": residue_names[ordered[sj][0]],
            "amino_acid": structure_sequence[sj],
        }
        for qi, sj in matched
    ]
    return {
        "schema": "kinetics.structure-alignment-map.v1",
        "status": "aligned_coordinate_mapping",
        "chain_id": chain_id,
        "alignment_score": best_score,
        "aligned_pair_count": len(aligned),
        "identity": identity,
        "structure_coverage": coverage,
        "query_start_1based": min(qi for qi, _ in matched) + 1,
        "query_end_1based": max(qi for qi, _ in matched) + 1,
        "mapped_residues": mapped,
        "limitations": [
            "Only identical aligned residue pairs are mapped; mismatches are omitted.",
            "Linear-gap semi-global alignment is not a calibrated homology method.",
            "No mutation modelling, structural/functional effect, pathogenicity or clinical inference.",
            "Insertion codes, alternate locations and unresolved residues are not reconstructed.",
        ],
    }
