from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import validate

from molecularis.molecular_model import (
    COORDINATE_SYSTEM, MolecularAtom, MolecularBond, MolecularChain,
    MolecularResidue, Molecule,
)


def water() -> Molecule:
    return Molecule(
        molecule_id="water-1",
        name="water",
        atoms=(
            MolecularAtom("O1", "O", position_angstrom=(0.0, 0.0, 0.0)),
            MolecularAtom("H1", "H", position_angstrom=(0.96, 0.0, 0.0)),
            MolecularAtom("H2", "H", position_angstrom=(-0.24, 0.93, 0.0)),
        ),
        bonds=(
            MolecularBond("b1", "O1", "H1"),
            MolecularBond("b2", "O1", "H2"),
        ),
    )


def test_water_graph_formula_and_coordinates() -> None:
    molecule = water()
    assert molecule.formula == "H2O"
    assert molecule.coordinate_unit == "angstrom"
    assert molecule.adjacency["O1"] == ("H1", "H2")
    assert molecule.connected_components() == (("O1", "H1", "H2"),)


def test_disconnected_components_are_preserved() -> None:
    molecule = Molecule(
        "salt", "two disconnected ions",
        (MolecularAtom("Na", "Na", formal_charge=1), MolecularAtom("Cl", "Cl", formal_charge=-1)),
    )
    assert molecule.connected_components() == (("Na",), ("Cl",))
    assert molecule.formula == "ClNa"


def test_hierarchical_chain_residue_membership() -> None:
    molecule = Molecule(
        "peptide", "one-residue model",
        (
            MolecularAtom("N", "N", residue_id="r1", chain_id="A"),
            MolecularAtom("CA", "C", residue_id="r1", chain_id="A"),
        ),
        residues=(MolecularResidue("r1", "GLY", "A", ("N", "CA")),),
        chains=(MolecularChain("A", "chain A", ("r1",)),),
    )
    assert molecule.connected_components() == (("N",), ("CA",))


@pytest.mark.parametrize("element", ["Xx", "", "carbon", "c"])
def test_unknown_or_noncanonical_element_rejected(element: str) -> None:
    with pytest.raises(ValueError, match="element"):
        MolecularAtom("a", element)


def test_invalid_coordinate_values_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        MolecularAtom("a", "C", position_angstrom=(0.0, float("nan"), 1.0))


def test_coordinate_completeness_is_enforced() -> None:
    with pytest.raises(ValueError, match="every atom"):
        Molecule("m", "partial", (
            MolecularAtom("a", "C", position_angstrom=(0.0, 0.0, 0.0)),
            MolecularAtom("b", "H"),
        ))


def test_duplicate_atom_and_bond_identifiers_rejected() -> None:
    with pytest.raises(ValueError, match="atom identifiers"):
        Molecule("m", "duplicate", (MolecularAtom("a", "C"), MolecularAtom("a", "H")))
    with pytest.raises(ValueError, match="duplicate bonds"):
        Molecule("m", "parallel", (
            MolecularAtom("a", "C"), MolecularAtom("b", "O"),
        ), (
            MolecularBond("x", "a", "b"), MolecularBond("y", "b", "a"),
        ))


def test_invalid_bond_reference_and_self_bond_rejected() -> None:
    with pytest.raises(ValueError, match="unknown atom"):
        Molecule("m", "bad ref", (MolecularAtom("a", "C"),),
                 (MolecularBond("b", "a", "missing"),))
    with pytest.raises(ValueError, match="itself"):
        MolecularBond("b", "a", "a")


def test_invalid_residue_chain_membership_rejected() -> None:
    with pytest.raises(ValueError, match="unknown chain"):
        Molecule("m", "bad hierarchy", (MolecularAtom("a", "C"),),
                 residues=(MolecularResidue("r", "GLY", "A", ("a",)),))
    with pytest.raises(ValueError, match="disagree"):
        Molecule("m", "bad atom mapping", (
            MolecularAtom("a", "C", residue_id="r", chain_id="B"),
        ), residues=(MolecularResidue("r", "GLY", "A", ("a",)),),
            chains=(MolecularChain("A", "A", ("r",)),))


def test_round_trip_serialization_and_digest_are_stable() -> None:
    molecule = water()
    restored = Molecule.from_dict(molecule.to_dict())
    assert restored == molecule
    assert restored.sha256 == molecule.sha256
    assert len(molecule.sha256) == 64


def test_serialization_rejects_wrong_schema_and_units() -> None:
    payload = water().to_dict()
    wrong_schema = copy.deepcopy(payload)
    wrong_schema["schema"] = "molecularis.molecule.v0"
    with pytest.raises(ValueError, match="Unsupported molecule schema"):
        Molecule.from_dict(wrong_schema)
    wrong_unit = copy.deepcopy(payload)
    wrong_unit["coordinate_unit"] = "nm"
    with pytest.raises(ValueError, match="angstrom"):
        Molecule.from_dict(wrong_unit)


def test_supported_coordinate_system_is_explicit() -> None:
    assert water().coordinate_system == COORDINATE_SYSTEM
    with pytest.raises(ValueError, match="coordinate_system"):
        Molecule("m", "bad frame", (MolecularAtom("a", "C"),),
                 coordinate_system="unknown")


def test_residue_and_chain_references_are_complete() -> None:
    with pytest.raises(ValueError, match="listed exactly once"):
        Molecule(
            "m", "missing chain membership",
            (MolecularAtom("a", "C", residue_id="r", chain_id="A"),),
            residues=(MolecularResidue("r", "GLY", "A", ("a",)),),
            chains=(MolecularChain("A", "A", ()),),
        )


def test_versioned_json_schema_accepts_fixture() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "services/molecular/schemas/molecule-v1.schema.json").read_text())
    fixture = json.loads((root / "services/molecular/data/water.molecule.json").read_text())
    validate(instance=fixture, schema=schema)
    assert Molecule.from_dict(fixture).formula == "H2O"
