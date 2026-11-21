# Chemistry Rulebook D — chemistry-core-v1

Status: executable native v1 baseline; scientific approval pending.

- CHM-001 — Identity: exact schema, canonical JSON and SHA-256 content identity.
- CHM-002 — Graph integrity: supported elements, finite Angstrom coordinates, unique atom-pair bonds, valid distinct endpoints and bond orders 1–4.
- CHM-003 — Explicitness: formulas/masses and graph descriptors are limited to explicit atoms; implicit hydrogens are never inferred.
- CHM-004 — Fingerprint bounds: path length 1–6 and hard feature/walk-state ceilings; overflow fails closed.
- CHM-005 — Match semantics: exact element and bond-order subgraph match; aromaticity and stereochemistry are not compared.
- CHM-006 — Similarity semantics: set Tanimoto on Molecularis path-v1 features; empty/empty follows the native Tanimoto definition.

Each operation returns limitations and identifies the rules checked. Rules are operational constraints, not independent proof of chemical correctness.
