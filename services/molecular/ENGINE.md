# A — Molecular Engine

Status: implementation in progress; v1 graph model and structural validation implemented.

## Mission and ownership

Service A owns the canonical, tool-independent molecular entity model used by later services. Its primary object is a molecular graph with stable identifiers and optional 3D coordinates. It is the shared foundation for chemistry, structure, protein, DNA/RNA, simulation and workflow services.

The Python reference implementation is `python/molecularis/molecular_model.py`. It is dependency-free and does not delegate graph construction or validation to RDKit, Open Babel, Biotite or another external engine.

## v1 domain objects

- `MolecularAtom`: stable atom ID, periodic-table element symbol, integer formal charge, optional isotope/name/residue/chain IDs and optional Cartesian position.
- `MolecularBond`: stable bond ID, two atom endpoints, order and a bounded stereo annotation.
- `MolecularResidue`: residue ID/name, parent chain and explicit atom membership.
- `MolecularChain`: chain ID/name and ordered residue membership.
- `Molecule`: identity, atoms, bonds, hierarchy and coordinate-frame declaration.

## Coordinate and identity contract

- Coordinates are either absent for every atom or present for every atom.
- Coordinate values are finite Cartesian coordinates in Angstrom.
- The only v1 frame is `cartesian_right_handed`; no implicit conversion is performed.
- Atom, bond, residue and chain identifiers are unique within their respective namespaces.
- Bonds reference existing atoms, cannot be self-edges, and cannot duplicate an undirected edge.
- Hierarchical atom/residue/chain membership must be internally consistent.
- Disconnected components are valid and are preserved.

## Native operations

- Validate graph references and hierarchy at construction.
- Derive a simple elemental formula using Hill ordering.
- Produce deterministic adjacency and connected components.
- Serialize to the versioned JSON contract and calculate a SHA-256 digest over canonical JSON.

## Explicit exclusions in v1

No inferred valence or chemical sanitization, aromaticity perception, protonation/tautomer assignment, implicit hydrogens, stereochemical inference, bond-order inference, force fields, energy calculations, conformer generation, atom typing, periodic boundary conditions, symmetry expansion or experimental structure parsing. These belong to later scoped work and must not be silently guessed by this model.

## Acceptance gates

- Unit and graph invariants pass the service-local test suite.
- JSON schema validates serialized fixtures.
- Round-trip serialization preserves values and digest.
- Independent reference fixtures cover common small molecules and hierarchical macromolecule fragments.
- Package compatibility tests prove existing public imports remain stable.
- No claim of complete chemical validity is made from structural validation alone.
