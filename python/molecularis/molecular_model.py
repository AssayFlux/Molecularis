"""Canonical molecular graph model and validation for Molecularis service A.

This module owns topology and coordinate representation only. It does not infer
chemical validity, protonation, stereochemistry, force fields, or energetics.
Coordinates, when present, are Cartesian Angstrom values in a right-handed frame.
"""
from __future__ import annotations

import hashlib
import json
from collections import deque
from dataclasses import dataclass
from math import isfinite
from typing import Any, Mapping

SCHEMA_VERSION = "molecularis.molecule.v1"
COORDINATE_UNIT = "angstrom"
COORDINATE_SYSTEM = "cartesian_right_handed"

_ELEMENTS = frozenset(
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu "
    "Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs "
    "Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl "
    "Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh "
    "Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split()
)
_BOND_ORDERS = frozenset({"single", "double", "triple", "aromatic", "unspecified"})
_BOND_STEREO = frozenset({"none", "up", "down", "cis", "trans", "E", "Z", "unknown"})


def _identifier(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise ValueError(f"{field} must be non-empty text of at most 128 characters")
    if any(ord(char) < 32 for char in value):
        raise ValueError(f"{field} must not contain control characters")


def _finite_vector(value: tuple[float, float, float] | None) -> None:
    if value is None:
        return
    if not isinstance(value, tuple) or len(value) != 3:
        raise ValueError("position_angstrom must be a 3-item tuple or None")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v) for v in value):
        raise ValueError("Coordinates must be finite real numbers")


@dataclass(frozen=True, slots=True)
class MolecularAtom:
    atom_id: str
    element: str
    formal_charge: int = 0
    isotope: int | None = None
    name: str | None = None
    residue_id: str | None = None
    chain_id: str | None = None
    position_angstrom: tuple[float, float, float] | None = None

    def __post_init__(self) -> None:
        _identifier(self.atom_id, "atom_id")
        if not isinstance(self.element, str) or self.element not in _ELEMENTS:
            raise ValueError(f"Unsupported chemical element symbol: {self.element!r}")
        if isinstance(self.formal_charge, bool) or not isinstance(self.formal_charge, int):
            raise ValueError("formal_charge must be an integer")
        if self.isotope is not None and (
            isinstance(self.isotope, bool) or not isinstance(self.isotope, int) or self.isotope < 1
        ):
            raise ValueError("isotope must be a positive integer when supplied")
        for field_name, value in (("name", self.name), ("residue_id", self.residue_id),
                                  ("chain_id", self.chain_id)):
            if value is not None:
                _identifier(value, field_name)
        _finite_vector(self.position_angstrom)


@dataclass(frozen=True, slots=True)
class MolecularBond:
    bond_id: str
    atom_1: str
    atom_2: str
    order: str = "single"
    stereo: str = "none"

    def __post_init__(self) -> None:
        _identifier(self.bond_id, "bond_id")
        _identifier(self.atom_1, "atom_1")
        _identifier(self.atom_2, "atom_2")
        if self.atom_1 == self.atom_2:
            raise ValueError("A bond cannot connect an atom to itself")
        if self.order not in _BOND_ORDERS:
            raise ValueError(f"Unsupported bond order: {self.order!r}")
        if self.stereo not in _BOND_STEREO:
            raise ValueError(f"Unsupported bond stereo value: {self.stereo!r}")


@dataclass(frozen=True, slots=True)
class MolecularResidue:
    residue_id: str
    name: str
    chain_id: str
    atom_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _identifier(self.residue_id, "residue_id")
        _identifier(self.name, "residue name")
        _identifier(self.chain_id, "chain_id")
        if not self.atom_ids:
            raise ValueError("A residue must reference at least one atom")
        if len(set(self.atom_ids)) != len(self.atom_ids):
            raise ValueError("Residue atom_ids must be unique")
        for atom_id in self.atom_ids:
            _identifier(atom_id, "residue atom_id")


@dataclass(frozen=True, slots=True)
class MolecularChain:
    chain_id: str
    name: str
    residue_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _identifier(self.chain_id, "chain_id")
        _identifier(self.name, "chain name")
        if len(set(self.residue_ids)) != len(self.residue_ids):
            raise ValueError("Chain residue_ids must be unique")
        for residue_id in self.residue_ids:
            _identifier(residue_id, "chain residue_id")


@dataclass(frozen=True, slots=True)
class Molecule:
    molecule_id: str
    name: str
    atoms: tuple[MolecularAtom, ...]
    bonds: tuple[MolecularBond, ...] = ()
    residues: tuple[MolecularResidue, ...] = ()
    chains: tuple[MolecularChain, ...] = ()
    coordinate_system: str = COORDINATE_SYSTEM

    def __post_init__(self) -> None:
        _identifier(self.molecule_id, "molecule_id")
        _identifier(self.name, "molecule name")
        if not self.atoms:
            raise ValueError("A molecule must contain at least one atom")
        if self.coordinate_system != COORDINATE_SYSTEM:
            raise ValueError(f"coordinate_system must be {COORDINATE_SYSTEM!r}")
        atom_ids = [atom.atom_id for atom in self.atoms]
        bond_ids = [bond.bond_id for bond in self.bonds]
        residue_ids = [residue.residue_id for residue in self.residues]
        chain_ids = [chain.chain_id for chain in self.chains]
        for label, values in (("atom", atom_ids), ("bond", bond_ids),
                              ("residue", residue_ids), ("chain", chain_ids)):
            if len(values) != len(set(values)):
                raise ValueError(f"{label} identifiers must be unique")

        atom_by_id = {atom.atom_id: atom for atom in self.atoms}
        residue_by_id = {residue.residue_id: residue for residue in self.residues}
        chain_by_id = {chain.chain_id: chain for chain in self.chains}
        edge_keys: set[frozenset[str]] = set()
        for bond in self.bonds:
            if bond.atom_1 not in atom_by_id or bond.atom_2 not in atom_by_id:
                raise ValueError(f"Bond {bond.bond_id!r} references an unknown atom")
            edge = frozenset((bond.atom_1, bond.atom_2))
            if edge in edge_keys:
                raise ValueError("Parallel duplicate bonds are not supported in molecule v1")
            edge_keys.add(edge)

        positions = [atom.position_angstrom is not None for atom in self.atoms]
        if any(positions) and not all(positions):
            raise ValueError("Coordinates must be supplied for every atom or for none")

        residue_atom_ids: set[str] = set()
        for residue in self.residues:
            if residue.chain_id not in chain_by_id:
                raise ValueError(f"Residue {residue.residue_id!r} references an unknown chain")
            for atom_id in residue.atom_ids:
                if atom_id not in atom_by_id:
                    raise ValueError(f"Residue {residue.residue_id!r} references an unknown atom")
                if atom_id in residue_atom_ids:
                    raise ValueError(f"Atom {atom_id!r} belongs to more than one residue")
                atom = atom_by_id[atom_id]
                if atom.residue_id != residue.residue_id or atom.chain_id != residue.chain_id:
                    raise ValueError(f"Atom {atom_id!r} and residue membership disagree")
                residue_atom_ids.add(atom_id)

        for atom in self.atoms:
            if atom.residue_id is not None:
                residue = residue_by_id.get(atom.residue_id)
                if residue is None or atom.atom_id not in residue.atom_ids:
                    raise ValueError(f"Atom {atom.atom_id!r} references inconsistent residue membership")
            if atom.chain_id is not None and atom.chain_id not in chain_by_id:
                raise ValueError(f"Atom {atom.atom_id!r} references an unknown chain")
            if atom.residue_id is None and atom.chain_id is not None and self.residues:
                raise ValueError(f"Atom {atom.atom_id!r} has a chain but no residue in a hierarchical model")

        chain_residue_ids: set[str] = set()
        for chain in self.chains:
            for residue_id in chain.residue_ids:
                residue = residue_by_id.get(residue_id)
                if residue is None or residue.chain_id != chain.chain_id:
                    raise ValueError(f"Chain {chain.chain_id!r} has inconsistent residue membership")
                if residue_id in chain_residue_ids:
                    raise ValueError(f"Residue {residue_id!r} belongs to multiple chains")
                chain_residue_ids.add(residue_id)
        if self.residues and chain_residue_ids != set(residue_ids):
            raise ValueError("Every residue must be listed exactly once by its parent chain")

    @property
    def coordinate_unit(self) -> str:
        return COORDINATE_UNIT

    @property
    def formula(self) -> str:
        counts: dict[str, int] = {}
        for atom in self.atoms:
            counts[atom.element] = counts.get(atom.element, 0) + 1
        order = (["C"] if "C" in counts else []) + (["H"] if "H" in counts else [])
        order += sorted(element for element in counts if element not in {"C", "H"})
        return "".join(element + (str(counts[element]) if counts[element] != 1 else "")
                       for element in order)

    @property
    def adjacency(self) -> dict[str, tuple[str, ...]]:
        neighbours: dict[str, list[str]] = {atom.atom_id: [] for atom in self.atoms}
        for bond in self.bonds:
            neighbours[bond.atom_1].append(bond.atom_2)
            neighbours[bond.atom_2].append(bond.atom_1)
        return {atom_id: tuple(values) for atom_id, values in neighbours.items()}

    def connected_components(self) -> tuple[tuple[str, ...], ...]:
        adjacency = self.adjacency
        unseen = {atom.atom_id for atom in self.atoms}
        components: list[tuple[str, ...]] = []
        for atom in self.atoms:
            if atom.atom_id not in unseen:
                continue
            queue = deque([atom.atom_id])
            unseen.remove(atom.atom_id)
            component: list[str] = []
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbour in adjacency[current]:
                    if neighbour in unseen:
                        unseen.remove(neighbour)
                        queue.append(neighbour)
            components.append(tuple(component))
        return tuple(components)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA_VERSION,
            "molecule_id": self.molecule_id,
            "name": self.name,
            "coordinate_unit": COORDINATE_UNIT,
            "coordinate_system": self.coordinate_system,
            "atoms": [
                {
                    "atom_id": atom.atom_id, "element": atom.element,
                    "formal_charge": atom.formal_charge, "isotope": atom.isotope,
                    "name": atom.name, "residue_id": atom.residue_id, "chain_id": atom.chain_id,
                    "position_angstrom": list(atom.position_angstrom)
                    if atom.position_angstrom is not None else None,
                } for atom in self.atoms
            ],
            "bonds": [
                {"bond_id": bond.bond_id, "atom_1": bond.atom_1, "atom_2": bond.atom_2,
                 "order": bond.order, "stereo": bond.stereo} for bond in self.bonds
            ],
            "residues": [
                {"residue_id": residue.residue_id, "name": residue.name,
                 "chain_id": residue.chain_id, "atom_ids": list(residue.atom_ids)}
                for residue in self.residues
            ],
            "chains": [
                {"chain_id": chain.chain_id, "name": chain.name,
                 "residue_ids": list(chain.residue_ids)} for chain in self.chains
            ],
        }

    @property
    def sha256(self) -> str:
        encoded = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Molecule":
        if not isinstance(value, Mapping):
            raise ValueError("Molecule document must be an object")
        if value.get("schema") != SCHEMA_VERSION:
            raise ValueError(f"Unsupported molecule schema: {value.get('schema')!r}")
        if value.get("coordinate_unit") != COORDINATE_UNIT:
            raise ValueError("Molecule coordinate_unit must be 'angstrom'")

        def sequence(key: str) -> list[Any]:
            result = value.get(key, [])
            if not isinstance(result, list):
                raise ValueError(f"{key} must be an array")
            return result

        atoms = []
        for item in sequence("atoms"):
            if not isinstance(item, Mapping):
                raise ValueError("Each atom must be an object")
            position = item.get("position_angstrom")
            if position is not None:
                if not isinstance(position, (list, tuple)) or len(position) != 3:
                    raise ValueError("position_angstrom must contain three coordinates")
                position = tuple(position)
            atoms.append(MolecularAtom(
                atom_id=item.get("atom_id"), element=item.get("element"),
                formal_charge=item.get("formal_charge", 0), isotope=item.get("isotope"),
                name=item.get("name"), residue_id=item.get("residue_id"),
                chain_id=item.get("chain_id"), position_angstrom=position,
            ))
        bonds = []
        for item in sequence("bonds"):
            if not isinstance(item, Mapping):
                raise ValueError("Each bond must be an object")
            bonds.append(MolecularBond(
                bond_id=item.get("bond_id"), atom_1=item.get("atom_1"),
                atom_2=item.get("atom_2"), order=item.get("order", "single"),
                stereo=item.get("stereo", "none"),
            ))
        residues = []
        for item in sequence("residues"):
            if not isinstance(item, Mapping):
                raise ValueError("Each residue must be an object")
            residues.append(MolecularResidue(
                residue_id=item.get("residue_id"), name=item.get("name"),
                chain_id=item.get("chain_id"), atom_ids=tuple(item.get("atom_ids", ())),
            ))
        chains = []
        for item in sequence("chains"):
            if not isinstance(item, Mapping):
                raise ValueError("Each chain must be an object")
            chains.append(MolecularChain(
                chain_id=item.get("chain_id"), name=item.get("name"),
                residue_ids=tuple(item.get("residue_ids", ())),
            ))
        return cls(
            molecule_id=value.get("molecule_id"), name=value.get("name"),
            atoms=tuple(atoms), bonds=tuple(bonds), residues=tuple(residues),
            chains=tuple(chains), coordinate_system=value.get("coordinate_system", COORDINATE_SYSTEM),
        )
