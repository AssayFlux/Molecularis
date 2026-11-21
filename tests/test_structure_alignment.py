from __future__ import annotations

import pytest

from molecularis.structure import Atom
from molecularis.structure_alignment import map_chain_sequence_by_alignment


def make_atoms(sequence: str, start: int = 10) -> list[Atom]:
    from molecularis.sequence_structure import THREE_TO_ONE
    reverse = {value: key for key, value in THREE_TO_ONE.items()}
    return [
        Atom(i + 1, "CA", reverse[residue], "A", start + i, float(i), 0.0, 0.0, "C")
        for i, residue in enumerate(sequence)
    ]


def test_alignment_maps_chain_with_internal_query_insertion() -> None:
    result = map_chain_sequence_by_alignment(
        "MAGSQVLK", make_atoms("MAGSVLK"), chain_id="A",
    )
    assert result["status"] == "aligned_coordinate_mapping"
    mapped = result["mapped_residues"]
    assert [item["query_position_1based"] for item in mapped] == [1, 2, 3, 4, 6, 7, 8]
    assert [item["structure_residue_number"] for item in mapped] == list(range(10, 17))
    assert result["structure_coverage"] == 1.0


def test_alignment_maps_structure_fragment_to_query_subsequence() -> None:
    result = map_chain_sequence_by_alignment(
        "MKWVTFISLL", make_atoms("WVTF"), chain_id="A",
    )
    assert result["status"] == "aligned_coordinate_mapping"
    assert [item["query_position_1based"] for item in result["mapped_residues"]] == [3, 4, 5, 6]


def test_repeated_optimal_placements_abstain() -> None:
    result = map_chain_sequence_by_alignment(
        "AGSVAGSV", make_atoms("AGSV"), chain_id="A",
    )
    assert result["status"] == "abstained_ambiguous_optimal_alignment"
    assert result["mapped_residues"] == []


def test_low_identity_abstains_without_partial_coordinate_claim() -> None:
    result = map_chain_sequence_by_alignment(
        "MAGS", make_atoms("MATS"), chain_id="A",
    )
    assert result["status"] == "abstained_below_mapping_threshold"
    assert result["mapped_residues"] == []


def test_alignment_rejects_resource_overrun_and_bad_thresholds() -> None:
    atoms = make_atoms("MAGSVLK")
    with pytest.raises(ValueError, match="max_alignment_cells"):
        map_chain_sequence_by_alignment(
            "MAGSQVLK", atoms, chain_id="A", max_alignment_cells=2,
        )
    with pytest.raises(ValueError, match="minimum_identity"):
        map_chain_sequence_by_alignment(
            "MAGSQVLK", atoms, chain_id="A", minimum_identity=1.5,
        )
    with pytest.raises(ValueError, match="positive integer"):
        map_chain_sequence_by_alignment(
            "MAGSQVLK", atoms, chain_id="A", max_atoms=True,
        )


def test_alignment_rejects_noncontiguous_numbering() -> None:
    atoms = make_atoms("AG")
    atoms[1] = Atom(2, "CA", "GLY", "A", 12, 1.0, 0.0, 0.0, "C")
    result = map_chain_sequence_by_alignment("AG", atoms, chain_id="A")
    assert result["status"] == "abstained_noncontiguous_structure_numbering"
