from __future__ import annotations

import pytest

from molecularis.sequence_structure import (
    chain_interface_contacts, map_exact_chain_sequence, map_variant_to_structure,
)
from molecularis.structure import Atom


def atom(serial: int, residue: str, number: int, chain: str = "A") -> Atom:
    return Atom(serial, "CA", residue, chain, number, float(serial), 0.0, 0.0, "C")


def test_unique_exact_chain_mapping_preserves_structure_numbering() -> None:
    atoms = [
        atom(1, "ALA", 10), atom(2, "GLY", 11), atom(3, "SER", 12),
        atom(4, "VAL", 13), atom(5, "LEU", 14, "B"),
    ]
    result = map_exact_chain_sequence("MAGS VLK".replace(" ", ""), atoms, chain_id="A")
    assert result["status"] == "exact_unique_match"
    assert result["query_start_1based"] == 2
    mapped = result["mapped_residues"]
    assert [item["query_position_1based"] for item in mapped] == [2, 3, 4, 5]
    assert [item["structure_residue_number"] for item in mapped] == [10, 11, 12, 13]


def test_repeated_exact_match_abstains_instead_of_choosing() -> None:
    result = map_exact_chain_sequence(
        "AGSVAGSV", [atom(1, "ALA", 1), atom(2, "GLY", 2), atom(3, "SER", 3), atom(4, "VAL", 4)],
        chain_id="A",
    )
    assert result["status"] == "ambiguous_exact_match"
    assert result["candidate_query_starts_1based"] == [1, 5]
    assert result["mapped_residues"] == []


def test_no_match_and_nonstandard_residue_are_explicit() -> None:
    result = map_exact_chain_sequence("AAAA", [atom(1, "GLY", 1)], chain_id="A")
    assert result["status"] == "no_exact_match"
    with pytest.raises(ValueError, match="Unsupported/non-standard"):
        map_exact_chain_sequence("AAAA", [atom(1, "MSE", 1)], chain_id="A")


def test_mapping_validates_sequence_and_chain() -> None:
    with pytest.raises(ValueError, match="canonical"):
        map_exact_chain_sequence("ABZ", [atom(1, "ALA", 1)], chain_id="A")
    with pytest.raises(ValueError, match="chain_id"):
        map_exact_chain_sequence("A", [atom(1, "ALA", 1)], chain_id="")


def test_numbering_gaps_and_conflicting_residue_identity_abstain() -> None:
    gap = map_exact_chain_sequence(
        "AGSV", [atom(1, "ALA", 10), atom(2, "GLY", 12)], chain_id="A",
    )
    assert gap["status"] == "noncontiguous_structure_numbering"
    assert gap["mapped_residues"] == []

    with pytest.raises(ValueError, match="Conflicting residue identity"):
        map_exact_chain_sequence(
            "A", [atom(1, "ALA", 10), atom(2, "GLY", 10)], chain_id="A",
        )


def test_mapping_enforces_query_and_structure_residue_limits() -> None:
    atoms = [atom(1, "ALA", 1), atom(2, "GLY", 2)]
    with pytest.raises(ValueError, match="query sequence exceeds"):
        map_exact_chain_sequence("AG", atoms, chain_id="A", max_query_residues=1)
    with pytest.raises(ValueError, match="structure chain exceeds"):
        map_exact_chain_sequence(
            "AG", atoms, chain_id="A", max_structure_residues=1,
        )
    with pytest.raises(ValueError, match="positive integer"):
        map_exact_chain_sequence("A", atoms, chain_id="A", max_structure_residues=0)


def test_mapping_streams_and_bounds_total_atom_input() -> None:
    def atoms():
        yield atom(1, "ALA", 1, "B")
        yield atom(2, "ALA", 1, "A")
        yield atom(3, "GLY", 2, "A")

    with pytest.raises(ValueError, match="atom stream exceeds"):
        map_exact_chain_sequence("AG", atoms(), chain_id="A", max_atoms=2)
    with pytest.raises(ValueError, match="max_atoms must be a positive integer"):
        map_exact_chain_sequence("A", [atom(1, "ALA", 1)], chain_id="A", max_atoms=0)



@pytest.mark.parametrize(
    "parameter,value",
    [
        ("max_query_residues", True),
        ("max_query_residues", 1.5),
        ("max_structure_residues", False),
        ("max_structure_residues", 1.5),
        ("max_atoms", True),
        ("max_atoms", 2.5),
    ],
)
def test_mapping_rejects_non_integer_resource_limits(parameter: str, value: object) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        map_exact_chain_sequence(
            "A", [atom(1, "ALA", 1)], chain_id="A", **{parameter: value},
        )


def test_mapping_detects_overlapping_exact_occurrences() -> None:
    result = map_exact_chain_sequence(
        "AAAA", [atom(1, "ALA", 1), atom(2, "ALA", 2)], chain_id="A",
    )
    assert result["status"] == "ambiguous_exact_match"
    assert result["candidate_query_starts_1based"] == [1, 2, 3]



def test_variant_maps_only_through_unique_exact_chain_correspondence() -> None:
    atoms = [
        atom(1, "ALA", 10), atom(2, "GLY", 11),
        atom(3, "SER", 12), atom(4, "VAL", 13),
    ]
    result = map_variant_to_structure(
        "MAGS VLK".replace(" ", ""), atoms, chain_id="A",
        variant_position_1based=4, reference_amino_acid="S", alternate_amino_acid="T",
    )
    assert result["status"] == "mapped_coordinate_only"
    assert result["mapping_quality"] == "unique_contiguous_exact_sequence"
    assert result["mapped_residue"]["structure_residue_number"] == 12
    assert any("No side-chain rebuilding" in item for item in result["limitations"])


def test_variant_mapping_abstains_for_ambiguous_or_uncovered_positions() -> None:
    ambiguous = map_variant_to_structure(
        "AGSVAGSV", [atom(1, "ALA", 1), atom(2, "GLY", 2), atom(3, "SER", 3), atom(4, "VAL", 4)],
        chain_id="A", variant_position_1based=1,
        reference_amino_acid="A", alternate_amino_acid="T",
    )
    assert ambiguous["status"] == "abstained"
    assert ambiguous["mapping_status"] == "ambiguous_exact_match"

    uncovered = map_variant_to_structure(
        "MAGS", [atom(1, "GLY", 10), atom(2, "SER", 11)],
        chain_id="A", variant_position_1based=1,
        reference_amino_acid="M", alternate_amino_acid="L",
    )
    assert uncovered["status"] == "not_covered_by_structure"


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"variant_position_1based": True}, "positive integer"),
        ({"reference_amino_acid": "Z"}, "canonical"),
        ({"alternate_amino_acid": "A"}, "must differ"),
    ],
)
def test_variant_mapping_rejects_invalid_variant_inputs(kwargs, message: str) -> None:
    parameters = {
        "variant_position_1based": 1,
        "reference_amino_acid": "A",
        "alternate_amino_acid": "V",
    }
    parameters.update(kwargs)
    with pytest.raises(ValueError, match=message):
        map_variant_to_structure(
            "AG", [atom(1, "ALA", 1), atom(2, "GLY", 2)],
            chain_id="A", **parameters,
        )



def test_chain_interface_contacts_report_bounded_geometric_residue_pairs() -> None:
    atoms = [
        Atom(1, "CA", "ALA", "A", 10, 0.0, 0.0, 0.0, "C"),
        Atom(2, "CB", "ALA", "A", 10, 0.0, 1.0, 0.0, "C"),
        Atom(3, "CA", "GLY", "B", 20, 4.0, 0.0, 0.0, "C"),
        Atom(4, "CA", "SER", "B", 21, 20.0, 0.0, 0.0, "C"),
        Atom(5, "H", "ALA", "B", 22, 0.5, 0.0, 0.0, "H"),
    ]
    result = chain_interface_contacts(atoms, chain_a="A", chain_b="B")
    assert result["residue_pair_count"] == 1
    assert result["atom_contact_count"] == 2
    assert result["residue_contacts"][0]["residue_a"] == 10
    assert result["residue_contacts"][0]["residue_b"] == 20
    assert result["interpretation"] == "geometric_interface_contacts_only"


def test_chain_interface_contacts_validate_chains_and_resource_limits() -> None:
    atoms = [atom(1, "ALA", 1), atom(2, "GLY", 2, "B")]
    with pytest.raises(ValueError, match="different"):
        chain_interface_contacts(atoms, chain_a="A", chain_b="A")
    with pytest.raises(ValueError, match="max_atoms"):
        chain_interface_contacts(atoms, chain_a="A", chain_b="B", max_atoms=1)
    with pytest.raises(ValueError, match="max_candidate_pairs"):
        chain_interface_contacts(
            atoms + [atom(3, "SER", 3, "B")],
            chain_a="A", chain_b="B", max_candidate_pairs=1,
        )


def test_chain_interface_contacts_enforces_residue_pair_output_limit() -> None:
    atoms = [
        atom(1, "ALA", 1, "A"),
        atom(2, "GLY", 1, "B"),
        atom(3, "SER", 2, "B"),
    ]
    with pytest.raises(ValueError, match="max_residue_pairs"):
        chain_interface_contacts(
            atoms, chain_a="A", chain_b="B", max_residue_pairs=1,
        )



def test_chain_interface_contacts_are_deterministic_under_atom_permutation() -> None:
    atoms = [
        Atom(1, "CA", "ALA", "A", 10, 0.0, 0.0, 0.0, "C"),
        Atom(2, "CA", "GLY", "A", 11, 0.0, 0.0, 0.0, "C"),
        Atom(3, "CA", "SER", "B", 20, 3.0, 0.0, 0.0, "C"),
        Atom(4, "CA", "VAL", "B", 21, -3.0, 0.0, 0.0, "C"),
    ]
    forward = chain_interface_contacts(atoms, chain_a="A", chain_b="B")
    reversed_input = chain_interface_contacts(list(reversed(atoms)), chain_a="A", chain_b="B")
    assert forward["residue_contacts"] == reversed_input["residue_contacts"]
    assert forward["residue_pair_count"] == 4


def test_chain_interface_contacts_include_exact_cutoff_and_reject_nonfinite_coordinates() -> None:
    boundary = [
        Atom(1, "CA", "ALA", "A", 1, 0.0, 0.0, 0.0, "C"),
        Atom(2, "CA", "GLY", "B", 2, 8.0, 0.0, 0.0, "C"),
    ]
    result = chain_interface_contacts(
        boundary, chain_a="A", chain_b="B", cutoff_angstrom=8.0,
    )
    assert result["residue_pair_count"] == 1
    assert result["residue_contacts"][0]["minimum_distance_angstrom"] == 8.0

    invalid = [boundary[0], Atom(3, "CA", "GLY", "B", 2, float("nan"), 0.0, 0.0, "C")]
    with pytest.raises(ValueError, match="non-finite"):
        chain_interface_contacts(invalid, chain_a="A", chain_b="B")
