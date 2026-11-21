from __future__ import annotations

import pytest

from molecularis.structure import Atom
from molecularis.structure_quality import structure_geometry_metrics


def atom(serial: int, chain: str, residue_number: int, x: float, element: str = "C") -> Atom:
    return Atom(serial, "CA", "ALA", chain, residue_number, x, 0.0, 0.0, element)


def test_geometry_metrics_report_clashes_without_assigning_quality_grade() -> None:
    result = structure_geometry_metrics([
        atom(1, "A", 1, 0.0),
        atom(2, "B", 2, 1.0),
        atom(3, "A", 1, 20.0),
    ])
    assert result["atom_count"] == 3
    assert result["residue_count"] == 2
    assert result["clash_count"] == 1
    assert result["severe_clash_count"] == 1
    assert result["quality_badge"] == "not_assessed"
    assert result["assessment_status"] == "geometry_screen_only"


def test_geometry_metrics_exclude_unknown_elements_and_bound_candidate_work() -> None:
    result = structure_geometry_metrics([
        atom(1, "A", 1, 0.0, "XX"),
        atom(2, "B", 2, 1.0, "C"),
    ])
    assert result["assessed_atom_count"] == 1
    assert result["unassessed_element_counts"] == {"XX": 1}
    with pytest.raises(ValueError, match="max_candidate_pairs"):
        structure_geometry_metrics(
            [atom(1, "A", 1, 0.0), atom(2, "B", 2, 1.0), atom(3, "C", 3, 2.0)],
            max_candidate_pairs=1,
        )


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"max_atoms": True}, "max_atoms"),
        ({"max_reported_clashes": 1.5}, "max_reported_clashes"),
        ({"clash_overlap_angstrom": float("nan")}, "clash_overlap_angstrom"),
        ({"severe_overlap_angstrom": 0.2}, "severe overlap"),
    ],
)
def test_geometry_metrics_reject_invalid_limits(kwargs, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        structure_geometry_metrics([atom(1, "A", 1, 0.0)], **kwargs)


def test_geometry_metrics_keep_only_configured_top_clash_records() -> None:
    result = structure_geometry_metrics(
        [atom(1, "A", 1, 0.0), atom(2, "B", 2, 1.0), atom(3, "C", 3, 2.0)],
        max_reported_clashes=1,
    )
    assert result["clash_count"] == 3
    assert len(result["top_clashes"]) == 1


def test_backbone_torsions_report_angles_without_quality_grade() -> None:
    from molecularis.structure_quality import backbone_torsion_angles

    residues = [
        ("N", "ALA", 1, 0.0, 0.0, 0.0),
        ("CA", "ALA", 1, 1.0, 0.0, 0.0),
        ("C", "ALA", 1, 1.0, 1.0, 0.0),
        ("N", "GLY", 2, 2.0, 1.0, 1.0),
        ("CA", "GLY", 2, 3.0, 1.0, 1.0),
        ("C", "GLY", 2, 3.0, 2.0, 1.0),
        ("N", "SER", 3, 4.0, 2.0, 2.0),
        ("CA", "SER", 3, 5.0, 2.0, 2.0),
        ("C", "SER", 3, 5.0, 3.0, 2.0),
    ]
    atoms = [
        Atom(i + 1, name, residue, "A", number, x, y, z, "N" if name == "N" else "C")
        for i, (name, residue, number, x, y, z) in enumerate(residues)
    ]
    result = backbone_torsion_angles(atoms, chain_id="A")
    assert result["residue_count"] == 3
    records = result["records"]
    assert records[0]["phi_degrees"] is None
    assert records[-1]["psi_degrees"] is None
    assert records[1]["phi_status"] == "available"
    assert records[1]["psi_status"] == "available"
    assert result["quality_badge"] == "not_assessed"


def test_backbone_torsions_abstain_on_missing_atoms_and_bound_input() -> None:
    from molecularis.structure_quality import backbone_torsion_angles

    atoms = [Atom(1, "CA", "ALA", "A", 1, 0.0, 0.0, 0.0, "C")]
    result = backbone_torsion_angles(atoms)
    assert result["records"][0]["phi_degrees"] is None
    with pytest.raises(ValueError, match="max_atoms"):
        backbone_torsion_angles(atoms, max_atoms=0)



def test_geometry_metrics_reject_conflicting_residue_names_at_one_position() -> None:
    atoms = [
        Atom(1, "CA", "ALA", "A", 7, 0.0, 0.0, 0.0, "C"),
        Atom(2, "CA", "GLY", "A", 7, 1.0, 0.0, 0.0, "C"),
    ]
    with pytest.raises(ValueError, match="Conflicting residue identities"):
        structure_geometry_metrics(atoms)


def test_backbone_torsions_reject_ambiguous_residue_numbering() -> None:
    from molecularis.structure_quality import backbone_torsion_angles

    atoms = [
        Atom(1, "N", "ALA", "A", 7, 0.0, 0.0, 0.0, "N"),
        Atom(2, "CA", "GLY", "A", 7, 1.0, 0.0, 0.0, "C"),
    ]
    with pytest.raises(ValueError, match="Conflicting residue identities"):
        backbone_torsion_angles(atoms)


def test_backbone_torsion_matches_known_right_handed_quarter_turn() -> None:
    """A hand-constructed C-N-CA-C plane rotation has a +90 degree phi."""
    from molecularis.structure_quality import backbone_torsion_angles

    atoms = [
        Atom(1, "C", "ALA", "A", 1, 0.0, 1.0, 0.0, "C"),
        Atom(2, "N", "GLY", "A", 2, 0.0, 0.0, 0.0, "N"),
        Atom(3, "CA", "GLY", "A", 2, 1.0, 0.0, 0.0, "C"),
        Atom(4, "C", "GLY", "A", 2, 1.0, 0.0, 1.0, "C"),
        Atom(5, "N", "SER", "A", 3, 1.0, 1.0, 1.0, "N"),
    ]
    result = backbone_torsion_angles(atoms, chain_id="A")
    middle = result["records"][1]
    assert middle["phi_status"] == "available"
    assert middle["phi_degrees"] == pytest.approx(90.0, abs=1e-8)
    assert result["quality_badge"] == "not_assessed"


def test_backbone_torsions_report_degenerate_dihedral_as_unavailable() -> None:
    from molecularis.structure_quality import backbone_torsion_angles

    atoms = [
        Atom(1, "C", "ALA", "A", 1, -1.0, 0.0, 0.0, "C"),
        Atom(2, "N", "GLY", "A", 2, 0.0, 0.0, 0.0, "N"),
        Atom(3, "CA", "GLY", "A", 2, 1.0, 0.0, 0.0, "C"),
        Atom(4, "C", "GLY", "A", 2, 2.0, 0.0, 0.0, "C"),
    ]
    result = backbone_torsion_angles(atoms, chain_id="A")
    assert result["records"][1]["phi_degrees"] is None
    assert result["records"][1]["phi_status"] == "unavailable"
