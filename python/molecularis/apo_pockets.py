"""Bounded probe-grid apo cavity candidates; geometry only, never affinity."""
from __future__ import annotations

from collections import deque
from math import floor, isfinite
from typing import Iterable, cast

from .structure import Atom

_AMINO_ACIDS = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
    "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
}


def apo_pocket_candidates(
    atoms: Iterable[Atom],
    *,
    grid_spacing_angstrom: float = 1.0,
    small_probe_radius_angstrom: float = 1.4,
    large_probe_radius_angstrom: float = 3.0,
    generic_atom_radius_angstrom: float = 1.7,
    max_atoms: int = 20_000,
    max_grid_points: int = 250_000,
    max_distance_checks: int = 5_000_000,
    min_pocket_grid_points: int = 4,
    max_pockets: int = 100,
) -> dict[str, object]:
    """Find concavity candidates reachable by a small probe but not a large probe.

    Uses canonical protein heavy atoms and a generic atom radius. It is a coarse
    geometric screen, not a chemically parameterized pocket or druggability model.
    """
    for name, value in (
        ("max_atoms", max_atoms), ("max_grid_points", max_grid_points),
        ("max_distance_checks", max_distance_checks),
        ("min_pocket_grid_points", min_pocket_grid_points), ("max_pockets", max_pockets),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    for name, numeric_value in (
        ("grid_spacing_angstrom", grid_spacing_angstrom),
        ("small_probe_radius_angstrom", small_probe_radius_angstrom),
        ("large_probe_radius_angstrom", large_probe_radius_angstrom),
        ("generic_atom_radius_angstrom", generic_atom_radius_angstrom),
    ):
        if (
            isinstance(numeric_value, bool)
            or not isinstance(numeric_value, (int, float))
            or not isfinite(numeric_value)
            or numeric_value <= 0
        ):
            raise ValueError(f"{name} must be finite and positive")
    if small_probe_radius_angstrom >= large_probe_radius_angstrom:
        raise ValueError("small probe radius must be smaller than large probe radius")

    protein: list[Atom] = []
    atom_count = 0
    for atom in atoms:
        atom_count += 1
        if atom_count > max_atoms:
            raise ValueError("Structure exceeds max_atoms")
        if not all(isfinite(value) for value in (atom.x, atom.y, atom.z)):
            raise ValueError("Structure contains non-finite coordinates")
        if atom.element.strip().upper() not in {"H", "D", ""} and atom.residue.upper() in _AMINO_ACIDS:
            protein.append(atom)
    if not protein:
        raise ValueError("No canonical protein heavy atoms were found")

    spacing = float(grid_spacing_angstrom)
    reach = float(generic_atom_radius_angstrom + large_probe_radius_angstrom)
    margin = reach + spacing
    protein_minima = [min(getattr(atom, axis) for atom in protein) for axis in ("x", "y", "z")]
    protein_maxima = [max(getattr(atom, axis) for atom in protein) for axis in ("x", "y", "z")]
    minima = [value - margin for value in protein_minima]
    maxima = [value + margin for value in protein_maxima]
    nx, ny, nz = tuple(int((high - low) / spacing) + 1 for low, high in zip(minima, maxima))
    point_count = nx * ny * nz
    if point_count > max_grid_points:
        raise ValueError("Grid exceeds max_grid_points")

    buckets: dict[tuple[int, int, int], list[Atom]] = {}
    for atom in protein:
        key = (floor(atom.x / reach), floor(atom.y / reach), floor(atom.z / reach))
        buckets.setdefault(key, []).append(atom)

    small_free = bytearray(point_count)
    large_free = bytearray(point_count)
    small_sq = float(generic_atom_radius_angstrom + small_probe_radius_angstrom) ** 2
    large_sq = reach**2
    checks = 0
    for k in range(nz):
        z = minima[2] + k * spacing
        for j in range(ny):
            y = minima[1] + j * spacing
            for i in range(nx):
                x = minima[0] + i * spacing
                key = (floor(x / reach), floor(y / reach), floor(z / reach))
                nearest_sq = float("inf")
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        for dz in (-1, 0, 1):
                            for atom in buckets.get((key[0] + dx, key[1] + dy, key[2] + dz), ()):
                                checks += 1
                                if checks > max_distance_checks:
                                    raise ValueError("Grid exceeds max_distance_checks")
                                distance_sq = (x - atom.x) ** 2 + (y - atom.y) ** 2 + (z - atom.z) ** 2
                                if distance_sq < nearest_sq:
                                    nearest_sq = distance_sq
                index = i + nx * (j + ny * k)
                if nearest_sq > small_sq:
                    small_free[index] = 1
                if nearest_sq > large_sq:
                    large_free[index] = 1

    def flood_fill(mask: bytearray) -> bytearray:
        reached = bytearray(point_count)
        queue: deque[int] = deque()

        def seed(index: int) -> None:
            if mask[index] and not reached[index]:
                reached[index] = 1
                queue.append(index)

        for k in range(nz):
            for j in range(ny):
                seed(nx * (j + ny * k))
                seed(nx - 1 + nx * (j + ny * k))
        for k in range(nz):
            for i in range(nx):
                seed(i + nx * ny * k)
                seed(i + nx * (ny - 1 + ny * k))
        for j in range(ny):
            for i in range(nx):
                seed(i + nx * j)
                seed(i + nx * (j + ny * (nz - 1)))
        while queue:
            index = queue.popleft()
            i = index % nx
            j = (index // nx) % ny
            k = index // (nx * ny)
            neighbours = []
            if i > 0:
                neighbours.append(index - 1)
            if i + 1 < nx:
                neighbours.append(index + 1)
            if j > 0:
                neighbours.append(index - nx)
            if j + 1 < ny:
                neighbours.append(index + nx)
            if k > 0:
                neighbours.append(index - nx * ny)
            if k + 1 < nz:
                neighbours.append(index + nx * ny)
            for neighbour in neighbours:
                if mask[neighbour] and not reached[neighbour]:
                    reached[neighbour] = 1
                    queue.append(neighbour)
        return reached

    small_reachable = flood_fill(small_free)
    large_reachable = flood_fill(large_free)
    candidate = bytearray(point_count)
    for index in range(point_count):
        i = index % nx
        j = (index // nx) % ny
        k = index // (nx * ny)
        point = (minima[0] + i * spacing, minima[1] + j * spacing, minima[2] + k * spacing)
        inside_model_bounds = all(
            protein_minima[axis] <= point[axis] <= protein_maxima[axis]
            for axis in range(3)
        )
        if inside_model_bounds and small_reachable[index] and not large_reachable[index]:
            candidate[index] = 1
    visited = bytearray(point_count)
    pockets: list[dict[str, object]] = []
    for start in range(point_count):
        if not candidate[start] or visited[start]:
            continue
        queue = deque([start])
        visited[start] = 1
        component: list[int] = []
        while queue:
            index = queue.popleft()
            component.append(index)
            i = index % nx
            j = (index // nx) % ny
            k = index // (nx * ny)
            neighbours = []
            if i > 0:
                neighbours.append(index - 1)
            if i + 1 < nx:
                neighbours.append(index + 1)
            if j > 0:
                neighbours.append(index - nx)
            if j + 1 < ny:
                neighbours.append(index + nx)
            if k > 0:
                neighbours.append(index - nx * ny)
            if k + 1 < nz:
                neighbours.append(index + nx * ny)
            for neighbour in neighbours:
                if candidate[neighbour] and not visited[neighbour]:
                    visited[neighbour] = 1
                    queue.append(neighbour)
        if len(component) < min_pocket_grid_points:
            continue
        if len(pockets) >= max_pockets:
            raise ValueError("Grid exceeds max_pockets")
        count = len(component)
        centroid = [
            sum(
                minima[axis] + (
                    (index % nx) if axis == 0 else
                    ((index // nx) % ny) if axis == 1 else
                    (index // (nx * ny))
                ) * spacing
                for index in component
            ) / count
            for axis in range(3)
        ]
        pockets.append({
            "grid_point_count": count,
            "approximate_volume_angstrom3": count * spacing**3,
            "centroid_angstrom": centroid,
        })
    pockets.sort(key=lambda pocket: (
        -cast(int, pocket["grid_point_count"]),
        tuple(cast(list[float], pocket["centroid_angstrom"])),
    ))
    for rank, pocket in enumerate(pockets, start=1):
        pocket["rank"] = rank
    return {
        "schema": "kinetics.apo-pocket-candidates.v1",
        "status": "candidates_found" if pockets else "no_apo_pocket_candidates",
        "atom_count": len(protein),
        "grid_dimensions": [nx, ny, nz],
        "grid_point_count": point_count,
        "distance_check_count": checks,
        "grid_spacing_angstrom": spacing,
        "small_probe_radius_angstrom": float(small_probe_radius_angstrom),
        "large_probe_radius_angstrom": float(large_probe_radius_angstrom),
        "generic_atom_radius_angstrom": float(generic_atom_radius_angstrom),
        "pocket_candidate_count": len(pockets),
        "pocket_candidates": pockets,
        "interpretation": "coarse_probe_accessibility_concavity_candidates_only",
        "limitations": [
            "Uses one generic atom radius and canonical protein heavy atoms only.",
            "Ignores element-specific radii, ligand chemistry, waters, ions, metals, protonation and biological assemblies.",
            "Grid spacing and six-neighbour connectivity affect candidate shape and volume.",
            "Does not calculate affinity, ligandability, specificity, function or druggability.",
            "Independent structural reference validation is required before scientific interpretation.",
        ],
    }
