"""Conservative PDB parsing and geometry, including optional rigid-body RMSD fitting."""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, sqrt
from typing import Iterable


@dataclass(frozen=True)
class Atom:
    serial: int
    name: str
    residue: str
    chain: str
    residue_number: int
    x: float
    y: float
    z: float
    element: str


def parse_pdb(text: str, *, include_hetero: bool = False) -> list[Atom]:
    atoms = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not (line.startswith("ATOM  ") or (include_hetero and line.startswith("HETATM"))):
            continue
        if len(line) < 54:
            raise ValueError(f"PDB line {line_no}: truncated coordinate record")
        if line[16:17] not in (" ", "A"):
            continue
        try:
            atoms.append(
                Atom(
                    int(line[6:11]), line[12:16].strip(), line[17:20].strip(),
                    line[21:22].strip(), int(line[22:26]), float(line[30:38]),
                    float(line[38:46]), float(line[46:54]),
                    line[76:78].strip().upper() if len(line) >= 78 else "",
                )
            )
        except ValueError as exc:
            raise ValueError(f"PDB line {line_no}: invalid atom field") from exc
        if not all(isfinite(value) for value in (atoms[-1].x, atoms[-1].y, atoms[-1].z)):
            raise ValueError(f"PDB line {line_no}: coordinates must be finite")
    if not atoms:
        raise ValueError("No supported PDB coordinate records")
    return atoms


def _largest_symmetric_eigenvector(matrix: list[list[float]]) -> list[float]:
    """Jacobi eigensolver for a real symmetric 4x4 matrix."""
    size = 4
    values = [row[:] for row in matrix]
    vectors = [[1.0 if row == col else 0.0 for col in range(size)] for row in range(size)]
    for _ in range(100):
        p, q = max(
            ((i, j) for i in range(size) for j in range(i + 1, size)),
            key=lambda pair: abs(values[pair[0]][pair[1]]),
        )
        if abs(values[p][q]) < 1e-14:
            break
        app, aqq, apq = values[p][p], values[q][q], values[p][q]
        tau = (aqq - app) / (2.0 * apq)
        sign = 1.0 if tau >= 0 else -1.0
        tangent = sign / (abs(tau) + sqrt(1.0 + tau * tau))
        cosine = 1.0 / sqrt(1.0 + tangent * tangent)
        sine = tangent * cosine

        values[p][p] = app - tangent * apq
        values[q][q] = aqq + tangent * apq
        values[p][q] = values[q][p] = 0.0
        for k in range(size):
            if k not in (p, q):
                vkp, vkq = values[k][p], values[k][q]
                values[k][p] = values[p][k] = cosine * vkp - sine * vkq
                values[k][q] = values[q][k] = sine * vkp + cosine * vkq
            # Eigenvectors are rotated for every row, including p and q.
            vkp, vkq = vectors[k][p], vectors[k][q]
            vectors[k][p] = cosine * vkp - sine * vkq
            vectors[k][q] = sine * vkp + cosine * vkq

    index = max(range(size), key=lambda item: values[item][item])
    vector = [vectors[row][index] for row in range(size)]
    norm = sqrt(sum(value * value for value in vector))
    if norm == 0:
        raise ValueError("Rigid-body fit failed to determine a rotation")
    return [value / norm for value in vector]


def _optimal_rotation(mobile: list[tuple[float, float, float]],
                      reference: list[tuple[float, float, float]]) -> list[list[float]]:
    covariance = [[0.0] * 3 for _ in range(3)]
    for moving, target in zip(mobile, reference):
        for row in range(3):
            for col in range(3):
                covariance[row][col] += moving[row] * target[col]
    sxx, sxy, sxz = covariance[0]
    syx, syy, syz = covariance[1]
    szx, szy, szz = covariance[2]
    trace = sxx + syy + szz
    horn = [
        [trace, syz - szy, szx - sxz, sxy - syx],
        [syz - szy, sxx - syy - szz, sxy + syx, szx + sxz],
        [szx - sxz, sxy + syx, -sxx + syy - szz, syz + szy],
        [sxy - syx, szx + sxz, syz + szy, -sxx - syy + szz],
    ]
    w, x, y, z = _largest_symmetric_eigenvector(horn)
    return [
        [w*w + x*x - y*y - z*z, 2*(x*y - w*z), 2*(x*z + w*y)],
        [2*(x*y + w*z), w*w - x*x + y*y - z*z, 2*(y*z - w*x)],
        [2*(x*z - w*y), 2*(y*z + w*x), w*w - x*x - y*y + z*z],
    ]


def rmsd(reference: Iterable[Atom], mobile: Iterable[Atom], *, superpose: bool = False) -> float:
    """RMSD in angstroms; optional Horn quaternion rigid-body least-squares fit."""
    first, second = list(reference), list(mobile)
    if len(first) != len(second) or not first:
        raise ValueError("Coordinate sets must have equal non-zero length")
    target: list[tuple[float, float, float]] = [
        (atom.x, atom.y, atom.z) for atom in first
    ]
    moving: list[tuple[float, float, float]] = [
        (atom.x, atom.y, atom.z) for atom in second
    ]
    if not all(isfinite(value) for point in target + moving for value in point):
        raise ValueError("Coordinate sets must contain only finite values")
    if not superpose:
        return sqrt(sum(sum((a - b) ** 2 for a, b in zip(p, q))
                        for p, q in zip(target, moving)) / len(first))

    target_center = tuple(sum(point[i] for point in target) / len(target) for i in range(3))
    moving_center = tuple(sum(point[i] for point in moving) / len(moving) for i in range(3))
    target_centered: list[tuple[float, float, float]] = [
        (
            point[0] - target_center[0],
            point[1] - target_center[1],
            point[2] - target_center[2],
        )
        for point in target
    ]
    moving_centered: list[tuple[float, float, float]] = [
        (
            point[0] - moving_center[0],
            point[1] - moving_center[1],
            point[2] - moving_center[2],
        )
        for point in moving
    ]
    rotation = _optimal_rotation(moving_centered, target_centered)
    squared = 0.0
    for point, expected in zip(moving_centered, target_centered):
        rotated = tuple(sum(rotation[i][j] * point[j] for j in range(3)) for i in range(3))
        squared += sum((rotated[i] - expected[i]) ** 2 for i in range(3))
    return sqrt(squared / len(first))


def contact_pairs(atoms: Iterable[Atom], cutoff_angstrom: float = 8.0) -> list[tuple[int, int, float]]:
    points = list(atoms)
    if not isfinite(cutoff_angstrom) or cutoff_angstrom <= 0:
        raise ValueError("cutoff must be finite and positive")
    result = []
    for i, first in enumerate(points):
        for j in range(i + 1, len(points)):
            second = points[j]
            if first.chain == second.chain and first.residue_number == second.residue_number:
                continue
            distance = sqrt(
                (first.x - second.x) ** 2 + (first.y - second.y) ** 2 + (first.z - second.z) ** 2
            )
            if distance <= cutoff_angstrom:
                result.append((i, j, distance))
    return result


def parse_mmcif(text: str, *, include_hetero: bool = False) -> list[Atom]:
    """Parse the mmCIF _atom_site loop into the shared Atom model.

    Coordinates and identifiers are read from label_* fields with auth_* fallbacks.
    An mmCIF parser is not a full chemical-component or symmetry interpreter.
    """
    import shlex

    lexer = shlex.shlex(text, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = "#"
    tokens = list(lexer)
    atoms: list[Atom] = []
    index = 0
    while index < len(tokens):
        if tokens[index].lower() != "loop_":
            index += 1
            continue
        index += 1
        tags: list[str] = []
        while index < len(tokens) and tokens[index].startswith("_"):
            tags.append(tokens[index].lower())
            index += 1
        if not tags:
            continue
        values: list[str] = []
        while index < len(tokens):
            token = tokens[index]
            if token.lower() in {"loop_", "stop_"} or token.lower().startswith(("data_", "save_")):
                break
            if token.startswith("_") and len(values) % len(tags) == 0:
                break
            values.append(token)
            index += 1
        if not any(tag.startswith("_atom_site.") for tag in tags):
            continue
        if len(values) % len(tags):
            raise ValueError("mmCIF atom_site loop has an incomplete row")
        columns = {tag: position for position, tag in enumerate(tags)}

        def field(row: list[str], *names: str, default: str = "") -> str:
            for name in names:
                position = columns.get(("_atom_site." + name).lower())
                if position is not None and row[position] not in {".", "?"}:
                    return row[position]
            return default

        required = ("type_symbol", "Cartn_x", "Cartn_y", "Cartn_z")
        if any(("_atom_site." + name).lower() not in columns for name in required):
            raise ValueError("mmCIF atom_site loop lacks required element/coordinate columns")
        for offset in range(0, len(values), len(tags)):
            row = values[offset:offset + len(tags)]
            group = field(row, "group_PDB", default="ATOM").upper()
            if group != "ATOM" and not (include_hetero and group == "HETATM"):
                continue
            alternate = field(row, "label_alt_id", "auth_alt_id", default="")
            if alternate not in {"", "A"}:
                continue
            try:
                serial = int(field(row, "id", default=str(len(atoms) + 1)))
                residue_number = int(field(row, "label_seq_id", "auth_seq_id", default="0"))
                x = float(field(row, "Cartn_x"))
                y = float(field(row, "Cartn_y"))
                z = float(field(row, "Cartn_z"))
            except ValueError as exc:
                raise ValueError("mmCIF atom_site loop contains an invalid numeric field") from exc
            if not all(isfinite(value) for value in (x, y, z)):
                raise ValueError("mmCIF coordinates must be finite")
            atoms.append(Atom(
                serial=serial,
                name=field(row, "label_atom_id", "auth_atom_id"),
                residue=field(row, "label_comp_id", "auth_comp_id"),
                chain=field(row, "label_asym_id", "auth_asym_id"),
                residue_number=residue_number,
                x=x, y=y, z=z,
                element=field(row, "type_symbol").upper(),
            ))
    if not atoms:
        raise ValueError("No supported mmCIF atom_site coordinates")
    return atoms

_VDW_RADII = {
    "H": 1.20, "C": 1.70, "N": 1.55, "O": 1.52, "F": 1.47,
    "P": 1.80, "S": 1.80, "CL": 1.75, "BR": 1.85, "I": 1.98,
}


def solvent_accessible_surface_area(
    atoms: Iterable[Atom], *, probe_radius: float = 1.4, sphere_points: int = 96,
) -> dict[str, object]:
    """Estimate per-atom and total SASA using deterministic Shrake-Rupley sampling.

    This geometric approximation uses element van der Waals radii and a spherical
    solvent probe. It does not add hydrogens, assign atom-specific radii, or infer
    residue-level relative accessibility.
    """
    points = list(atoms)
    if not points or len(points) > 2000:
        raise ValueError("SASA requires 1..2000 atoms")
    if not isfinite(probe_radius) or probe_radius <= 0:
        raise ValueError("Probe radius must be finite and positive")
    if not isinstance(sphere_points, int) or not 12 <= sphere_points <= 4096:
        raise ValueError("sphere_points must be an integer between 12 and 4096")

    radii: list[float] = []
    coordinates: list[tuple[float, float, float]] = []
    for atom in points:
        element = atom.element.strip().upper()
        if element not in _VDW_RADII:
            raise ValueError(f"Unsupported atom element for SASA: {element or '<blank>'}")
        coordinate = (atom.x, atom.y, atom.z)
        if not all(isfinite(value) for value in coordinate):
            raise ValueError("SASA coordinates must be finite")
        radii.append(_VDW_RADII[element])
        coordinates.append(coordinate)

    # Fibonacci sphere gives deterministic, approximately uniform surface samples.
    offset = 2.0 / sphere_points
    increment = 3.141592653589793 * (3.0 - sqrt(5.0))
    unit_points: list[tuple[float, float, float]] = []
    for index in range(sphere_points):
        y = ((index * offset) - 1.0) + offset / 2.0
        radial = sqrt(max(0.0, 1.0 - y * y))
        angle = index * increment
        unit_points.append((radial * cos(angle), y,
                            radial * sin(angle)))

    expanded = [radius + probe_radius for radius in radii]
    neighbours: list[list[int]] = [[] for _ in points]
    for first in range(len(points)):
        for second in range(first + 1, len(points)):
            delta = tuple(coordinates[first][axis] - coordinates[second][axis] for axis in range(3))
            threshold = expanded[first] + expanded[second]
            if sum(value * value for value in delta) < threshold * threshold:
                neighbours[first].append(second)
                neighbours[second].append(first)

    per_atom: list[dict[str, float | int]] = []
    total_area = 0.0
    for index, center in enumerate(coordinates):
        radius = expanded[index]
        exposed = 0
        for unit in unit_points:
            surface = tuple(center[axis] + radius * unit[axis] for axis in range(3))
            occluded = False
            for neighbour in neighbours[index]:
                delta = tuple(surface[axis] - coordinates[neighbour][axis] for axis in range(3))
                if sum(value * value for value in delta) < expanded[neighbour] ** 2:
                    occluded = True
                    break
            if not occluded:
                exposed += 1
        area = 4.0 * 3.141592653589793 * radius * radius * exposed / sphere_points
        total_area += area
        per_atom.append({"serial": points[index].serial, "area_angstrom2": area})

    return {
        "total_area_angstrom2": total_area,
        "per_atom": per_atom,
        "algorithm": "Shrake-Rupley with deterministic Fibonacci sphere points",
        "probe_radius_angstrom": probe_radius,
        "sphere_points": sphere_points,
        "warnings": [
            "Approximate surface area depends on sphere-point resolution",
            "Uses generic element radii; no hydrogens or atom-specific radii are inferred",
            "No residue-level relative accessibility or biological assembly is calculated",
        ],
    }

def interaction_candidates(
    atoms: Iterable[Atom], *, hydrogen_bond_range: tuple[float, float] = (2.5, 3.5),
    salt_bridge_cutoff: float = 4.0, disulfide_range: tuple[float, float] = (1.8, 2.3),
) -> dict[str, object]:
    """Report heavy-atom interaction candidates; geometric screening, not energetics."""
    points = list(atoms)
    if not points or len(points) > 5_000:
        raise ValueError("Interaction analysis requires 1..5000 atoms to bound pairwise screening")
    for name, bounds in (("hydrogen_bond_range", hydrogen_bond_range), ("disulfide_range", disulfide_range)):
        if len(bounds) != 2 or not all(isfinite(x) for x in bounds) or not 0 < bounds[0] < bounds[1]:
            raise ValueError(f"{name} must be finite, positive and increasing")
    if not isfinite(salt_bridge_cutoff) or salt_bridge_cutoff <= 0:
        raise ValueError("salt_bridge_cutoff must be finite and positive")
    if any(not all(isfinite(x) for x in (a.x, a.y, a.z)) for a in points):
        raise ValueError("Atom coordinates must be finite")

    def d(a: Atom, b: Atom) -> float:
        return sqrt((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)

    def residue(a: Atom) -> tuple[str, int, str]:
        return a.chain, a.residue_number, a.residue.upper()

    nitrogens = [a for a in points if a.element.upper() == "N"]
    oxygens = [a for a in points if a.element.upper() == "O"]
    positive = [a for a in points if
        (a.residue.upper() == "LYS" and a.name.strip().upper() == "NZ") or
        (a.residue.upper() == "ARG" and a.name.strip().upper() in {"NE", "NH1", "NH2"})]
    negative = [a for a in points if
        (a.residue.upper() == "ASP" and a.name.strip().upper() in {"OD1", "OD2"}) or
        (a.residue.upper() == "GLU" and a.name.strip().upper() in {"OE1", "OE2"})]
    sulfurs = [a for a in points if a.residue.upper() in {"CYS", "CYX"}
               and a.name.strip().upper() == "SG" and a.element.upper() == "S"]

    hbonds = []
    for donor in nitrogens:
        for acceptor in oxygens:
            if residue(donor) != residue(acceptor):
                distance = d(donor, acceptor)
                if hydrogen_bond_range[0] <= distance <= hydrogen_bond_range[1]:
                    hbonds.append({"donor_serial_candidate": donor.serial,
                                   "acceptor_serial_candidate": acceptor.serial,
                                   "distance_angstrom": distance})
    salt = []
    for cation in positive:
        for anion in negative:
            if residue(cation) != residue(anion):
                distance = d(cation, anion)
                if distance <= salt_bridge_cutoff:
                    salt.append({"positive_atom_serial": cation.serial,
                                 "negative_atom_serial": anion.serial,
                                 "distance_angstrom": distance})
    disulfides = []
    for index, first in enumerate(sulfurs):
        for second in sulfurs[index + 1:]:
            if residue(first) != residue(second):
                distance = d(first, second)
                if disulfide_range[0] <= distance <= disulfide_range[1]:
                    disulfides.append({"first_sulfur_serial": first.serial,
                                       "second_sulfur_serial": second.serial,
                                       "distance_angstrom": distance})
    return {
        "hydrogen_bond_candidates": hbonds, "salt_bridge_candidates": salt,
        "disulfide_candidates": disulfides,
        "method": "distance-only heavy-atom geometric screening",
        "warnings": [
            "Hydrogen-bond candidates omit hydrogen positions and angular geometry",
            "No protonation, tautomer, solvent, occupancy or alternate-conformation model",
            "Salt-bridge and disulfide candidates require independent review",
        ],
    }

