from __future__ import annotations

import pytest


def test_biotite_adapter_returns_molecularis_records_for_mmcif() -> None:
    pytest.importorskip("biotite")
    from molecularis.structure_biotite import read_mmcif_biotite

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
_atom_site.pdbx_PDB_ins_code
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.occupancy
_atom_site.B_iso_or_equiv
_atom_site.pdbx_PDB_model_num
ATOM 1 C CA GLY A 1 . ? 0.0 0.0 0.0 1.0 12.0 1
ATOM 2 N N GLY A 1 . ? 1.0 0.0 0.0 1.0 13.0 1
#
"""
    result = read_mmcif_biotite(cif)
    assert result["format"] == "mmCIF"
    assert result["model"] == 1
    assert result["atom_count"] == 2
    assert result["engine"] == "Biotite"
    atoms = result["atoms"]
    assert isinstance(atoms, list)
    assert atoms[0]["chain_id"] == "A"
    assert atoms[0]["residue_name"] == "GLY"
    assert atoms[0]["x_angstrom"] == pytest.approx(0.0)


def test_biotite_adapter_enforces_input_and_atom_bounds() -> None:
    from molecularis.structure_biotite import read_mmcif_biotite

    with pytest.raises(ValueError, match="byte limit"):
        read_mmcif_biotite("data_x", max_input_bytes=2)
    with pytest.raises(ValueError, match="max_atoms"):
        read_mmcif_biotite("data_x", max_atoms=0)
