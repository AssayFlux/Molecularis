from __future__ import annotations

import pytest

from molecularis.structure import Atom, rmsd


def atom(serial: int, x: float, y: float, z: float) -> Atom:
    return Atom(serial, "CA", "GLY", "A", serial, x, y, z, "C")


def test_rmsd_without_superposition_measures_raw_coordinates() -> None:
    reference = [atom(1, 0, 0, 0), atom(2, 1, 0, 0), atom(3, 0, 1, 0)]
    translated = [atom(1, 5, 2, 0), atom(2, 6, 2, 0), atom(3, 5, 3, 0)]
    assert rmsd(reference, translated) > 1


def test_rmsd_superposition_removes_rigid_rotation_and_translation() -> None:
    reference = [
        atom(1, 0, 0, 0), atom(2, 1, 0, 0),
        atom(3, 0, 1, 0), atom(4, 0, 0, 1),
    ]
    # Mobile coordinates are rotated +90 degrees around Z and translated.
    mobile = [
        atom(1, 5, -2, 3), atom(2, 5, -1, 3),
        atom(3, 4, -2, 3), atom(4, 5, -2, 4),
    ]
    assert rmsd(reference, mobile, superpose=True) == pytest.approx(0, abs=1e-8)


def test_rmsd_requires_equal_non_empty_coordinate_sets() -> None:
    with pytest.raises(ValueError):
        rmsd([atom(1, 0, 0, 0)], [])


def test_rmsd_and_contact_cutoff_reject_non_finite_values() -> None:
    with pytest.raises(ValueError, match="finite"):
        rmsd([atom(1, float("nan"), 0, 0)], [atom(1, 0, 0, 0)])


def test_mmcif_atom_site_loop_parses_coordinates_and_altloc() -> None:
    from molecularis.structure import parse_mmcif

    cif = """data_demo
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.label_alt_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM 1 C CA GLY A 1 . 0.0 0.0 0.0
ATOM 2 C CA GLY A 1 B 9.0 9.0 9.0
ATOM 3 N N GLY A 1 A 1.0 0.0 0.0
#
"""
    atoms = parse_mmcif(cif)
    assert len(atoms) == 2
    assert atoms[0].name == "CA"
    assert atoms[1].element == "N"
    assert atoms[1].x == 1.0


def test_mmcif_rejects_non_finite_coordinates() -> None:
    from molecularis.structure import parse_mmcif

    cif = """data_demo
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM 1 C CA GLY A 1 NaN 0.0 0.0
#
"""
    with pytest.raises(ValueError, match="finite"):
        parse_mmcif(cif)



def test_sasa_single_atom_area_and_occlusion_are_deterministic() -> None:
    from math import pi

    from molecularis.structure import solvent_accessible_surface_area

    single = solvent_accessible_surface_area([atom(1, 0, 0, 0)], sphere_points=48)
    assert single["total_area_angstrom2"] == pytest.approx(4 * pi * (1.7 + 1.4) ** 2)
    pair = solvent_accessible_surface_area(
        [atom(1, 0, 0, 0), atom(2, 3, 0, 0)], sphere_points=48,
    )
    assert pair["total_area_angstrom2"] < 2 * single["total_area_angstrom2"]
    assert pair == solvent_accessible_surface_area(
        [atom(1, 0, 0, 0), atom(2, 3, 0, 0)], sphere_points=48,
    )


def test_sasa_rejects_unsupported_elements_and_invalid_resolution() -> None:
    from molecularis.structure import solvent_accessible_surface_area

    unknown = Atom(1, "X", "UNK", "A", 1, 0.0, 0.0, 0.0, "")
    with pytest.raises(ValueError, match="Unsupported"):
        solvent_accessible_surface_area([unknown])
    with pytest.raises(ValueError, match="sphere_points"):
        solvent_accessible_surface_area([atom(1, 0, 0, 0)], sphere_points=4)



def test_structural_interaction_candidates_use_explicit_geometry() -> None:
    from molecularis.structure import interaction_candidates

    atoms = [
        Atom(1, "NZ", "LYS", "A", 1, 0.0, 0.0, 0.0, "N"),
        Atom(2, "OD1", "ASP", "B", 2, 3.0, 0.0, 0.0, "O"),
        Atom(3, "SG", "CYS", "A", 3, 10.0, 0.0, 0.0, "S"),
        Atom(4, "SG", "CYS", "B", 4, 12.0, 0.0, 0.0, "S"),
    ]
    result = interaction_candidates(atoms)
    assert len(result["salt_bridge_candidates"]) == 1
    assert len(result["disulfide_candidates"]) == 1
    assert len(result["hydrogen_bond_candidates"]) == 1
