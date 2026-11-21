"""Microbenchmark for Molecular v1 graph construction and traversal."""
from __future__ import annotations
import argparse
import json
from time import perf_counter
from molecularis.molecular_model import MolecularAtom, MolecularBond, Molecule

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atoms", type=int, default=10000)
    args = parser.parse_args()
    if args.atoms < 1:
        parser.error("--atoms must be positive")
    started = perf_counter()
    atoms = tuple(MolecularAtom(f"a{i}", "C") for i in range(args.atoms))
    bonds = tuple(MolecularBond(f"b{i}", f"a{i}", f"a{i + 1}") for i in range(args.atoms - 1))
    molecule = Molecule("benchmark-chain", "synthetic carbon chain", atoms, bonds)
    construction = perf_counter() - started
    started = perf_counter()
    components = len(molecule.connected_components())
    traversal = perf_counter() - started
    print(json.dumps({"benchmark":"molecular-v1-linear-chain","atoms":molecule.atom_count,
        "bonds":molecule.bond_count,"components":components,"construction_seconds":construction,
        "connected_components_seconds":traversal,"sha256":molecule.sha256}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
