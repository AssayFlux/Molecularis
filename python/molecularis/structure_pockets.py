"""Bounded ligand-proximal protein-site candidate screening.

This reports residues geometrically adjacent to one explicitly selected ligand.
It is not an apo-pocket detector, docking method, affinity score, or function predictor.
"""
from __future__ import annotations

from math import floor, isfinite, sqrt
from typing import Iterable, cast

from .structure import Atom

_WATER_NAMES = {"HOH", "WAT", "H2O", "DOD"}


def ligand_site_candidates(
    atoms: Iterable[Atom],
    *,
    ligand_chain: str,
    ligand_residue_number: int,
    ligand_residue_name: str,
    cutoff_angstrom: float = 5.0,
    max_atoms: int = 100_000,
    max_candidate_pairs: int = 2_000_000,
    max_residues: int = 10_000,
) -> dict[str, object]:
    """Return protein residues with heavy atoms within cutoff of a selected HETATM ligand.

    The caller must parse coordinates with include_hetero=True and explicitly identify
    the ligand residue. Waters, hydrogens and the selected ligand itself are excluded.
    """
    if not isinstance(ligand_chain, str) or not ligand_chain:
        raise ValueError("ligand_chain must be non-empty text")
    if isinstance(ligand_residue_number, bool) or not isinstance(ligand_residue_number, int):
        raise ValueError("ligand_residue_number must be an integer")
    if not isinstance(ligand_residue_name, str) or not ligand_residue_name.strip():
        raise ValueError("ligand_residue_name must be non-empty text")
    if ligand_residue_name.strip().upper() in {
        "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
        "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
    }:
        raise ValueError("Selected ligand residue name must not be a canonical amino acid")
    if isinstance(cutoff_angstrom, bool) or not isinstance(cutoff_angstrom, (int, float)) or not isfinite(cutoff_angstrom) or cutoff_angstrom <= 0:
        raise ValueError("cutoff_angstrom must be finite and positive")
    for name, value in (("max_atoms", max_atoms), ("max_candidate_pairs", max_candidate_pairs), ("max_residues", max_residues)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")

    ligand: list[Atom] = []
    protein: list[Atom] = []
    count = 0
    for atom in atoms:
        count += 1
        if count > max_atoms:
            raise ValueError("Structure exceeds max_atoms")
        if not all(isfinite(v) for v in (atom.x, atom.y, atom.z)):
            raise ValueError("Structure contains non-finite coordinates")
        element = atom.element.strip().upper()
        if element in {"", "H", "D"}:
            continue
        is_selected = (
            atom.chain == ligand_chain
            and atom.residue_number == ligand_residue_number
            and atom.residue.upper() == ligand_residue_name.strip().upper()
        )
        if is_selected:
            ligand.append(atom)
        elif atom.residue.upper() not in _WATER_NAMES and atom.residue.upper() in {
            "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
            "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
        }:
            protein.append(atom)
    if not ligand:
        raise ValueError("Selected ligand residue was not found among heavy atoms")
    if not protein:
        raise ValueError("No canonical protein heavy atoms were found")

    cell = float(cutoff_angstrom)
    buckets: dict[tuple[int, int, int], list[Atom]] = {}
    for atom in protein:
        key = (floor(atom.x / cell), floor(atom.y / cell), floor(atom.z / cell))
        buckets.setdefault(key, []).append(atom)

    residues: dict[tuple[str, int, str], dict[str, object]] = {}
    candidates = 0
    for lig in ligand:
        key = (floor(lig.x / cell), floor(lig.y / cell), floor(lig.z / cell))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for prot in buckets.get((key[0] + dx, key[1] + dy, key[2] + dz), ()):
                        candidates += 1
                        if candidates > max_candidate_pairs:
                            raise ValueError("Structure exceeds max_candidate_pairs")
                        distance = sqrt((lig.x-prot.x)**2 + (lig.y-prot.y)**2 + (lig.z-prot.z)**2)
                        if distance > cutoff_angstrom:
                            continue
                        residue_key = (prot.chain, prot.residue_number, prot.residue.upper())
                        if residue_key not in residues and len(residues) >= max_residues:
                            raise ValueError("Structure exceeds max_residues")
                        entry = residues.setdefault(residue_key, {
                            "chain_id": prot.chain,
                            "residue_number": prot.residue_number,
                            "residue_name": prot.residue.upper(),
                            "atom_contact_count": 0,
                            "minimum_distance_angstrom": distance,
                        })
                        entry["atom_contact_count"] = cast(int, entry["atom_contact_count"]) + 1
                        entry["minimum_distance_angstrom"] = min(cast(float, entry["minimum_distance_angstrom"]), distance)

    ranked = sorted(residues.values(), key=lambda item: (
        cast(float, item["minimum_distance_angstrom"]),
        -cast(int, item["atom_contact_count"]),
        str(item["chain_id"]), cast(int, item["residue_number"]), str(item["residue_name"]),
    ))
    return {
        "schema": "kinetics.ligand-site-candidates.v1",
        "status": "candidates_found" if ranked else "no_nearby_protein_residues",
        "ligand": {
            "chain_id": ligand_chain,
            "residue_number": ligand_residue_number,
            "residue_name": ligand_residue_name.strip().upper(),
            "heavy_atom_count": len(ligand),
        },
        "cutoff_angstrom": float(cutoff_angstrom),
        "candidate_pair_count": candidates,
        "candidate_residue_count": len(ranked),
        "residue_candidates": ranked,
        "interpretation": "ligand_proximal_geometric_site_candidates_only",
        "limitations": [
            "Requires a present, explicitly selected ligand; does not detect apo or unoccupied cavities.",
            "No ligand chemistry, bond typing, protonation, waters, metals, symmetry or biological assembly is modelled.",
            "Contact residues are not evidence of binding affinity, specificity, mechanism or biological function.",
            "Residue insertion codes and alternate conformations are not represented by the Atom model.",
        ],
    }
