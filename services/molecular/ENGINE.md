# A — Molecular Engine

Status: native v1 graph model and MSDE validation capability implemented; independent scientific approval remains pending.

## Mission

Service A owns the canonical, tool-independent molecular entity model used by chemistry, structure, protein, DNA/RNA, simulation and workflow services. Python reference modules are python/molecularis/molecular_model.py and python/molecularis/molecular_service.py.

## Domain model

- MolecularAtom: stable ID, periodic-table element, integer formal charge, optional isotope/name/residue/chain and optional Cartesian position.
- MolecularBond: stable ID, two atom endpoints, bounded order and stereo annotation.
- MolecularResidue: ID/name, parent chain and explicit atom membership.
- MolecularChain: ID/name and ordered residue membership.
- Molecule: identity, atoms, bonds, hierarchy and coordinate frame.

## Native operations

Structural validation, formula in Hill order, atom/bond counts, net formal charge, adjacency, atom degree, connected components, strict versioned JSON parsing, canonical serialization, SHA-256 identity, MSDE artifact ingestion/loading and executable structural validation Rulebook.

## Contract

Coordinates are all absent or all present, finite Cartesian Angstrom values in the right-handed frame. IDs are unique. Bonds reference distinct existing atoms and duplicate undirected edges are prohibited. Hierarchy is reciprocal. Disconnected components are preserved.

## Explicit exclusions

No inferred valence, chemical sanitization, aromaticity perception, protonation, tautomer assignment, implicit hydrogens, stereochemical inference, bond-order inference, force fields, energy calculations, conformer generation, atom typing, periodic boundary conditions, symmetry expansion or experimental structure parsing. Existing RDKit functionality remains an optional Chemistry adapter, not the native Molecular model.

## Acceptance evidence

Model tests, schema and fixture checks, artifact round-trip, provenance-preserving Rulebook execution, strict parser tests and a reproducible graph benchmark harness are required. Structural validation is not a claim of chemical validity.
