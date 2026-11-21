"""Conservative coordinate-geometry metrics for S2 structure review.

Metrics are descriptive screening signals only. They do not produce a calibrated
structure-quality grade, validation badge, or experimental/prediction confidence.
"""
from __future__ import annotations

import heapq
from collections import defaultdict
from math import atan2, degrees, floor, isfinite, sqrt
from typing import Iterable

from .structure import Atom

_VDW_RADII = {
    "H": 1.20, "C": 1.70, "N": 1.55, "O": 1.52, "F": 1.47,
    "P": 1.80, "S": 1.80, "CL": 1.75, "BR": 1.85, "I": 1.98,
}


def structure_geometry_metrics(
    atoms: Iterable[Atom],
    *,
    clash_overlap_angstrom: float = 0.4,
    severe_overlap_angstrom: float = 0.8,
    max_atoms: int = 200_000,
    max_candidate_pairs: int = 2_000_000,
    max_reported_clashes: int = 20,
) -> dict[str, object]:
    """Summarize atom/residue counts and bounded nonbonded steric-overlap candidates.

    Pairs in the same residue are excluded because this Atom model has no bond
    topology. Only elements with an explicit radius are assessed. Unknown elements
    are counted and excluded, never assigned an invented radius.
    """
    for name, value in (
        ("max_atoms", max_atoms),
        ("max_candidate_pairs", max_candidate_pairs),
        ("max_reported_clashes", max_reported_clashes),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    for name, threshold in (
        ("clash_overlap_angstrom", clash_overlap_angstrom),
        ("severe_overlap_angstrom", severe_overlap_angstrom),
    ):
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, (int, float))
            or not isfinite(threshold)
            or threshold <= 0
        ):
            raise ValueError(f"{name} must be finite and positive")
    if severe_overlap_angstrom < clash_overlap_angstrom:
        raise ValueError("severe overlap threshold must be >= clash threshold")

    points: list[Atom] = []
    for atom in atoms:
        if len(points) >= max_atoms:
            raise ValueError("Structure exceeds max_atoms")
        if not all(isfinite(value) for value in (atom.x, atom.y, atom.z)):
            raise ValueError("Structure contains non-finite coordinates")
        points.append(atom)
    if not points:
        raise ValueError("Structure must contain at least one atom")

    residue_names_by_position: dict[tuple[str, int], str] = {}
    for atom in points:
        position = (atom.chain, atom.residue_number)
        residue_name = atom.residue.strip().upper()
        previous_name = residue_names_by_position.setdefault(position, residue_name)
        if previous_name != residue_name:
            raise ValueError(
                "Conflicting residue identities at one chain position; "
                "insertion codes are not represented by this atom model"
            )
    residues = {(atom.chain, atom.residue_number, atom.residue) for atom in points}
    supported: list[tuple[int, Atom, float]] = []
    unknown_elements: dict[str, int] = defaultdict(int)
    for index, atom in enumerate(points):
        element = atom.element.strip().upper()
        radius = _VDW_RADII.get(element)
        if radius is None:
            unknown_elements[element or "<blank>"] += 1
        else:
            supported.append((index, atom, radius))

    cell_size = 4.0
    cells: dict[tuple[int, int, int], list[tuple[int, Atom, float]]] = defaultdict(list)
    for supported_atom in supported:
        atom = supported_atom[1]
        key = (floor(atom.x / cell_size), floor(atom.y / cell_size), floor(atom.z / cell_size))
        cells[key].append(supported_atom)

    top_clashes: list[tuple[float, int, dict[str, object]]] = []
    candidate_pairs = 0
    severe_count = 0
    clash_count = 0
    for index, atom, radius in supported:
        key = (floor(atom.x / cell_size), floor(atom.y / cell_size), floor(atom.z / cell_size))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for other_index, other, other_radius in cells.get(
                        (key[0] + dx, key[1] + dy, key[2] + dz), (),
                    ):
                        if other_index <= index:
                            continue
                        if atom.chain == other.chain and atom.residue_number == other.residue_number:
                            continue
                        candidate_pairs += 1
                        if candidate_pairs > max_candidate_pairs:
                            raise ValueError("Structure exceeds max_candidate_pairs")
                        distance = sqrt(
                            (atom.x - other.x) ** 2
                            + (atom.y - other.y) ** 2
                            + (atom.z - other.z) ** 2
                        )
                        overlap = radius + other_radius - distance
                        if overlap <= clash_overlap_angstrom:
                            continue
                        clash_count += 1
                        severe = overlap > severe_overlap_angstrom
                        severe_count += int(severe)
                        record = {
                            "atom_index_1": index,
                            "atom_index_2": other_index,
                            "chain_1": atom.chain,
                            "residue_1": atom.residue_number,
                            "atom_1": atom.name,
                            "chain_2": other.chain,
                            "residue_2": other.residue_number,
                            "atom_2": other.name,
                            "distance_angstrom": round(distance, 4),
                            "overlap_angstrom": round(overlap, 4),
                            "severity": "severe" if severe else "candidate",
                        }
                        heap_entry: tuple[float, int, dict[str, object]] = (overlap, candidate_pairs, record)
                        if len(top_clashes) < max_reported_clashes:
                            heapq.heappush(top_clashes, heap_entry)
                        else:
                            heapq.heappushpop(top_clashes, heap_entry)

    clashes = [
        item[2] for item in sorted(top_clashes, key=lambda entry: entry[0], reverse=True)
    ]
    return {
        "schema": "kinetics.structure-geometry-metrics.v1",
        "atom_count": len(points),
        "residue_count": len(residues),
        "assessed_atom_count": len(supported),
        "unassessed_element_counts": dict(sorted(unknown_elements.items())),
        "candidate_pair_count": candidate_pairs,
        "clash_count": clash_count,
        "severe_clash_count": severe_count,
        "clash_threshold_angstrom": clash_overlap_angstrom,
        "severe_threshold_angstrom": severe_overlap_angstrom,
        "top_clashes": clashes,
        "quality_badge": "not_assessed",
        "assessment_status": "geometry_screen_only",
        "limitations": [
            "Same-residue pairs are excluded because covalent bond topology is unavailable.",
            "Only listed element van der Waals radii are assessed; unknown elements are excluded.",
            "No hydrogens, alternate conformations, occupancies, bond geometry or protonation are inferred.",
            "This is not a MolProbity clashscore, Ramachandran analysis or calibrated quality grade.",
            "Experimental resolution/R-free and predicted pLDDT/PAE are not available in the Atom model.",
        ],
    }


def backbone_torsion_angles(
    atoms: Iterable[Atom],
    *,
    chain_id: str | None = None,
    max_atoms: int = 200_000,
    max_residues: int = 50_000,
) -> dict[str, object]:
    """Calculate observed backbone phi/psi dihedrals without assigning outlier grades.

    Only N, CA and C atoms are used. Residue-number gaps, missing backbone atoms,
    and duplicate atom names are reported as unavailable rather than reconstructed.
    Alternate locations and insertion codes are not represented by the Atom model.
    """
    for name, limit in (("max_atoms", max_atoms), ("max_residues", max_residues)):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError(f"{name} must be a positive integer")
    grouped: dict[tuple[str, int, str], dict[str, tuple[float, float, float]]] = {}
    residue_names_by_position: dict[tuple[str, int], str] = {}
    atom_count = 0
    for atom in atoms:
        atom_count += 1
        if atom_count > max_atoms:
            raise ValueError("Structure exceeds max_atoms")
        if chain_id is not None and atom.chain != chain_id:
            continue
        name = atom.name.strip().upper()
        if name not in {"N", "CA", "C"}:
            continue
        coordinate = (atom.x, atom.y, atom.z)
        if not all(isfinite(value) for value in coordinate):
            raise ValueError("Backbone coordinates must be finite")
        position = (atom.chain, atom.residue_number)
        residue_name = atom.residue.upper()
        previous_name = residue_names_by_position.setdefault(position, residue_name)
        if previous_name != residue_name:
            raise ValueError(
                "Conflicting residue identities at one chain position; "
                "insertion codes are not represented by this atom model"
            )
        key = (atom.chain, atom.residue_number, residue_name)
        residue_atoms = grouped.setdefault(key, {})
        if name in residue_atoms:
            raise ValueError(f"Duplicate backbone atom {name} at {key}")
        residue_atoms[name] = coordinate
        if len(grouped) > max_residues:
            raise ValueError("Structure exceeds max_residues")

    if not grouped:
        raise ValueError("No backbone N/CA/C atoms found for the selected chain")
    by_chain: dict[str, list[tuple[tuple[str, int, str], dict[str, tuple[float, float, float]]]]] = defaultdict(list)
    for key, residue_atoms in grouped.items():
        by_chain[key[0]].append((key, residue_atoms))

    def subtract(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def cross(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def dihedral(
        p0: tuple[float, float, float], p1: tuple[float, float, float],
        p2: tuple[float, float, float], p3: tuple[float, float, float],
    ) -> float | None:
        b0 = subtract(p0, p1)
        axis = subtract(p2, p1)
        b2 = subtract(p3, p2)
        axis_norm = sqrt(dot(axis, axis))
        if axis_norm <= 1e-12:
            return None
        unit = (axis[0] / axis_norm, axis[1] / axis_norm, axis[2] / axis_norm)
        projection0 = dot(b0, unit)
        projection2 = dot(b2, unit)
        v = (b0[0] - projection0 * unit[0], b0[1] - projection0 * unit[1], b0[2] - projection0 * unit[2])
        w = (b2[0] - projection2 * unit[0], b2[1] - projection2 * unit[1], b2[2] - projection2 * unit[2])
        if dot(v, v) <= 1e-24 or dot(w, w) <= 1e-24:
            return None
        angle = atan2(dot(cross(unit, v), w), dot(v, w))
        return degrees(angle)

    records: list[dict[str, object]] = []
    for chain, chain_residues in sorted(by_chain.items()):
        chain_residues.sort(key=lambda item: item[0][1])
        for index, (key, current) in enumerate(chain_residues):
            previous = chain_residues[index - 1] if index > 0 else None
            following = chain_residues[index + 1] if index + 1 < len(chain_residues) else None
            phi = None
            psi = None
            if (
                previous is not None and previous[0][1] + 1 == key[1]
                and "C" in previous[1] and {"N", "CA", "C"} <= current.keys()
            ):
                phi = dihedral(previous[1]["C"], current["N"], current["CA"], current["C"])
            if (
                following is not None and key[1] + 1 == following[0][1]
                and {"N", "CA", "C"} <= current.keys() and "N" in following[1]
            ):
                psi = dihedral(current["N"], current["CA"], current["C"], following[1]["N"])
            records.append({
                "chain_id": chain,
                "residue_number": key[1],
                "residue_name": key[2],
                "phi_degrees": phi,
                "psi_degrees": psi,
                "phi_status": "available" if phi is not None else "unavailable",
                "psi_status": "available" if psi is not None else "unavailable",
            })

    return {
        "schema": "kinetics.backbone-torsion-screen.v1",
        "residue_count": len(records),
        "records": records,
        "assessment_status": "torsion_angles_only",
        "quality_badge": "not_assessed",
        "limitations": [
            "No Ramachandran outlier classification or residue-specific probability model is applied.",
            "Missing backbone atoms and residue-number gaps are not reconstructed.",
            "Alternate locations, insertion codes, chain breaks and peptide-bond validation need richer parser metadata.",
            "Angles are geometric observations, not a calibrated structure-quality score.",
        ],
    }
