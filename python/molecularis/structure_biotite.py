"""Optional Biotite mmCIF structure reader behind Molecularis-owned records.

This adapter uses Biotite's PDBx parser and AtomArray conversion, but never returns
Biotite or NumPy objects. The default model is explicit (model 1); callers can request
a different model. BinaryCIF is intentionally a separate future input path.
"""
from __future__ import annotations

from hashlib import sha256
from io import StringIO
from math import isfinite
from typing import Any


def _biotite() -> tuple[Any, Any]:
    try:
        import biotite
        from biotite.structure.io import pdbx
    except ImportError as error:
        raise RuntimeError(
            "Biotite is unavailable; install the isolated Python 3.12+ structure profile"
        ) from error
    return biotite, pdbx


def read_mmcif_biotite(
    text: str,
    *,
    model: int = 1,
    include_bonds: bool = False,
    max_input_bytes: int = 32 * 1024 * 1024,
    max_atoms: int = 500_000,
) -> dict[str, object]:
    """Parse mmCIF with Biotite and return loss-aware Molecularis primitive records.

    Atom identity fields include author-independent label chain/residue identifiers,
    insertion code, alternate-location identifier, occupancy and B-factor when
    provided by Biotite's AtomArray annotations.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("mmCIF input must be non-empty text")
    try:
        encoded = text.encode("utf-8", errors="strict")
    except UnicodeEncodeError as error:
        raise ValueError("mmCIF input contains invalid Unicode") from error
    if len(encoded) > max_input_bytes:
        raise ValueError("mmCIF input exceeds configured byte limit")
    if isinstance(model, bool) or not isinstance(model, int) or model < 1:
        raise ValueError("model must be a positive 1-based model number")
    if isinstance(max_atoms, bool) or not isinstance(max_atoms, int) or max_atoms < 1:
        raise ValueError("max_atoms must be a positive integer")
    if isinstance(max_input_bytes, bool) or not isinstance(max_input_bytes, int) or max_input_bytes < 1:
        raise ValueError("max_input_bytes must be a positive integer")

    biotite, pdbx = _biotite()
    cif = pdbx.CIFFile.read(StringIO(text))
    model_count = int(pdbx.get_model_count(cif))
    if model > model_count:
        raise ValueError(f"Requested model {model} exceeds available model count {model_count}")
    atoms = pdbx.get_structure(cif, model=model, include_bonds=include_bonds)
    atom_count = len(atoms)
    if atom_count < 1:
        raise ValueError("mmCIF contains no atoms for the requested model")
    if atom_count > max_atoms:
        raise ValueError("Parsed atom count exceeds configured max_atoms")

    def annotation(name: str, index: int, default: object) -> object:
        try:
            return getattr(atoms, name)[index].item()
        except (AttributeError, IndexError, TypeError):
            return default

    records: list[dict[str, object]] = []
    for index in range(atom_count):
        xyz = [float(value) for value in atoms.coord[index]]
        if len(xyz) != 3 or not all(isfinite(value) for value in xyz):
            raise ValueError(f"Biotite returned invalid coordinates for atom {index}")
        records.append({
            "index": index,
            "chain_id": str(annotation("chain_id", index, "")),
            "residue_id": int(annotation("res_id", index, 0)),
            "insertion_code": str(annotation("ins_code", index, "")),
            "residue_name": str(annotation("res_name", index, "")),
            "atom_name": str(annotation("atom_name", index, "")),
            "element": str(annotation("element", index, "")),
            "hetero": bool(annotation("hetero", index, False)),
            "alternate_location": str(annotation("altloc_id", index, "")),
            "occupancy": float(annotation("occupancy", index, 0.0)),
            "b_factor": float(annotation("b_factor", index, 0.0)),
            "x_angstrom": xyz[0],
            "y_angstrom": xyz[1],
            "z_angstrom": xyz[2],
        })

    bond_count = 0
    if include_bonds:
        bonds = getattr(atoms, "bonds", None)
        if bonds is not None:
            bond_count = len(bonds)

    return {
        "schema_version": 1,
        "engine": "Biotite",
        "engine_version": str(biotite.__version__),
        "format": "mmCIF",
        "input_sha256": sha256(encoded).hexdigest(),
        "model": model,
        "model_count": model_count,
        "atom_count": atom_count,
        "bond_count": bond_count,
        "atoms": records,
        "limitations": [
            "Only the requested model is materialized in the returned atom records.",
            "BinaryCIF is not accepted by this text adapter.",
            "Missing optional atom annotations are represented by conservative defaults.",
            "No author/label identifier remapping or biological assembly expansion is performed.",
        ],
    }
