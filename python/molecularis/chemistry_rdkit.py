"""Optional RDKit-backed chemistry adapter.

RDKit is not currently bundled in the Android application. These functions use the
real RDKit sanitization/descriptor/fingerprint engine when it is installed on a host.
"""
from __future__ import annotations

from hashlib import sha256
from math import isfinite
from typing import Any


def _rdkit() -> tuple[Any, Any, Any, Any, Any]:
    try:
        from rdkit import Chem, DataStructs, rdBase  # type: ignore[import-not-found]
        from rdkit.Chem import Descriptors, rdFingerprintGenerator, rdMolDescriptors  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "RDKit backend is unavailable in this runtime; install an approved, "
            "version-pinned RDKit distribution before using production chemistry"
        ) from error
    return Chem, DataStructs, rdBase, Descriptors, (rdFingerprintGenerator, rdMolDescriptors)


def rdkit_backend_info() -> dict[str, str]:
    """Return the exact active RDKit version or a clear unavailable status."""
    try:
        _, _, version, _, _ = _rdkit()
    except RuntimeError as error:
        return {"available": "false", "status": str(error)}
    return {"available": "true", "engine": "RDKit", "version": version.rdkitVersion}


def _bounded_utf8(value: str, *, label: str, maximum: int) -> bytes:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    try:
        encoded = value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as error:
        raise ValueError(f"{label} must contain valid Unicode scalar values") from error
    if len(encoded) > maximum:
        raise ValueError(f"{label} exceeds the {maximum}-byte UTF-8 limit")
    if b"\x00" in encoded:
        raise ValueError(f"{label} must not contain NUL bytes")
    return encoded


def _describe(
    molecule: Any, *, source_format: str, input_bytes: bytes,
    remove_hs: bool | None = None,
) -> dict[str, object]:
    Chem, _, version, descriptors, modules = _rdkit()
    fingerprint_generator, mol_descriptors = modules
    if molecule is None:
        raise ValueError("RDKit could not parse the supplied molecule")
    # MolFromSmiles/MolFromMolBlock sanitizes by default. Sanitize explicitly so
    # the recorded operation is clear and failure is surfaced.
    Chem.SanitizeMol(molecule)
    canonical = Chem.MolToSmiles(molecule, canonical=True, isomericSmiles=True)
    radius, bits = 2, 2048
    generator = fingerprint_generator.GetMorganGenerator(radius=radius, fpSize=bits)
    fingerprint = generator.GetFingerprint(molecule)
    chiral_centres = Chem.FindMolChiralCenters(molecule, includeUnassigned=True)
    numeric_descriptors = {
        "molecular_weight": float(descriptors.MolWt(molecule)),
        "exact_molecular_weight": float(descriptors.ExactMolWt(molecule)),
        "crippen_logp": float(descriptors.MolLogP(molecule)),
        "tpsa_angstrom2": float(descriptors.TPSA(molecule)),
        "fraction_csp3": float(descriptors.FractionCSP3(molecule)),
    }
    if not all(isfinite(value) for value in numeric_descriptors.values()):
        raise ValueError("RDKit returned a non-finite molecular descriptor")
    aromatic_atom_count = sum(1 for atom in molecule.GetAtoms() if atom.GetIsAromatic())
    h_bond_donors = int(descriptors.NumHDonors(molecule))
    h_bond_acceptors = int(descriptors.NumHAcceptors(molecule))
    rule_of_five_criteria: dict[str, dict[str, float | int | bool]] = {
        "molecular_weight_da": {
            "observed": numeric_descriptors["molecular_weight"],
            "maximum": 500.0,
            "pass": numeric_descriptors["molecular_weight"] <= 500.0,
        },
        "crippen_logp": {
            "observed": numeric_descriptors["crippen_logp"],
            "maximum": 5.0,
            "pass": numeric_descriptors["crippen_logp"] <= 5.0,
        },
        "h_bond_donors": {
            "observed": h_bond_donors,
            "maximum": 5,
            "pass": h_bond_donors <= 5,
        },
        "h_bond_acceptors": {
            "observed": h_bond_acceptors,
            "maximum": 10,
            "pass": h_bond_acceptors <= 10,
        },
    }
    return {
        "descriptor_schema_version": 2,
        "engine": "RDKit",
        "engine_version": version.rdkitVersion,
        "source_format": source_format,
        "input_provenance": {
            "sha256_utf8": sha256(input_bytes).hexdigest(),
            "utf8_bytes": len(input_bytes),
            "preprocessing": "none; exact supplied text passed to RDKit parser",
        },
        "representation_assumptions": {
            "sanitization": "RDKit Chem.SanitizeMol",
            "canonicalization": "RDKit canonical isomeric SMILES",
            "protonation": "input state retained; no protonation adjustment",
            "tautomer": "input tautomer retained; no tautomer canonicalization",
            "aromaticity": "RDKit sanitization/aromaticity model",
            "stereochemistry": "isomeric SMILES; unassigned centers are reported, not inferred",
            "hydrogen_handling": (
                "RDKit parser defaults" if remove_hs is None
                else f"MolFromMolBlock removeHs={remove_hs}"
            ),
            "molecular_weight_unit": "Da",
            "exact_molecular_weight_unit": "Da",
            "tpsa_unit": "angstrom^2",
            "crippen_logp_unit": "dimensionless",
            "fraction_csp3_unit": "dimensionless",
        },
        "sanitization": "RDKit Chem.SanitizeMol",
        "canonical_isomeric_smiles": canonical,
        "formula": mol_descriptors.CalcMolFormula(molecule),
        **numeric_descriptors,
        "h_bond_donors": h_bond_donors,
        "h_bond_acceptors": h_bond_acceptors,
        "rotatable_bonds": int(descriptors.NumRotatableBonds(molecule)),
        "ring_count": int(descriptors.RingCount(molecule)),
        "aliphatic_ring_count": int(mol_descriptors.CalcNumAliphaticRings(molecule)),
        "aromatic_ring_count": int(mol_descriptors.CalcNumAromaticRings(molecule)),
        "formal_charge": sum(int(atom.GetFormalCharge()) for atom in molecule.GetAtoms()),
        "heavy_atom_count": int(molecule.GetNumHeavyAtoms()),
        "aromatic_atom_count": aromatic_atom_count,
        "atom_count": int(molecule.GetNumAtoms()),
        "bond_count": int(molecule.GetNumBonds()),
        "chiral_centres": chiral_centres,
        "rule_of_five_screen": {
            "criteria": rule_of_five_criteria,
            "pass_count": sum(1 for item in rule_of_five_criteria.values() if bool(item["pass"])),
            "criterion_count": len(rule_of_five_criteria),
            "all_criteria_pass": all(bool(item["pass"]) for item in rule_of_five_criteria.values()),
            "interpretation": (
                "heuristic physicochemical screen only; not a prediction of absorption, "
                "bioavailability, safety, efficacy or clinical suitability"
            ),
        },
        "morgan_fingerprint": {
            "algorithm": "Morgan", "radius": radius, "bits": bits,
            "on_bits": list(fingerprint.GetOnBits()),
        },
        "limitations": [
            "Descriptor values depend on the exact RDKit release and sanitization model",
            "Protonation, tautomer and conformer selection are not inferred",
            "No biological activity or clinical interpretation is provided",
        ],
    }


def analyze_smiles(smiles: str) -> dict[str, object]:
    """Parse, sanitize and describe a bounded SMILES string using RDKit."""
    input_bytes = _bounded_utf8(smiles, label="SMILES", maximum=1_000_000)
    Chem, _, _, _, _ = _rdkit()
    molecule = Chem.MolFromSmiles(smiles, sanitize=True)
    return _describe(
        molecule, source_format="SMILES", input_bytes=input_bytes,
    )


def analyze_molblock(molblock: str) -> dict[str, object]:
    """Parse and sanitize a bounded V2000/V3000 mol block using RDKit."""
    input_bytes = _bounded_utf8(molblock, label="Mol block", maximum=10_000_000)
    Chem, _, _, _, _ = _rdkit()
    molecule = Chem.MolFromMolBlock(
        molblock, sanitize=True, removeHs=False, strictParsing=True,
    )
    return _describe(
        molecule, source_format="molblock",
        input_bytes=input_bytes, remove_hs=False,
    )


def morgan_tanimoto(
    first_smiles: str, second_smiles: str, *, radius: int = 2, bits: int = 2048,
) -> float:
    """Calculate Morgan-fingerprint Tanimoto similarity using RDKit."""
    if not isinstance(radius, int) or isinstance(radius, bool) or not 1 <= radius <= 6:
        raise ValueError("Morgan radius must be an integer in 1..6")
    if not isinstance(bits, int) or isinstance(bits, bool) or not 256 <= bits <= 16_384 or bits & (bits - 1):
        raise ValueError("Morgan bit count must be a power of two in 256..16384")
    _bounded_utf8(first_smiles, label="First SMILES", maximum=1_000_000)
    _bounded_utf8(second_smiles, label="Second SMILES", maximum=1_000_000)
    Chem, DataStructs, _, _, modules = _rdkit()
    generator_module, _ = modules
    first = Chem.MolFromSmiles(first_smiles, sanitize=True)
    second = Chem.MolFromSmiles(second_smiles, sanitize=True)
    if first is None or second is None:
        raise ValueError("RDKit could not parse one or both SMILES inputs")
    generator = generator_module.GetMorganGenerator(radius=radius, fpSize=bits)
    return float(DataStructs.TanimotoSimilarity(
        generator.GetFingerprint(first), generator.GetFingerprint(second),
    ))
