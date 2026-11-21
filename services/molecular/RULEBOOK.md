# A — Molecular Rulebook

Status: v1 structural rules implemented in the model; independent scientific review and operational MSDE registration remain pending.

Rules are versioned by this document and the `molecularis.molecule.v1` schema. These rules define data integrity, not chemical or biological truth.

| Rule ID | Rule | Rationale | Acceptance |
|---|---|---|---|
| MOL-001 | Every molecule has a non-empty stable molecule ID and name. | Traceable identity. | Empty, whitespace-only or overlong identifiers fail. |
| MOL-002 | Every atom has a unique ID and a valid periodic-table element symbol. | Unambiguous graph vertices. | Duplicate IDs and unknown symbols fail. |
| MOL-003 | Formal charge is an integer; isotope, when present, is a positive integer. | Preserve explicit atomic annotations. | Wrong types and invalid isotope values fail. |
| MOL-004 | Every bond joins two distinct existing atoms. | Graph integrity. | Self-edges and dangling endpoints fail. |
| MOL-005 | At most one undirected bond exists for each atom pair in v1. | Avoid ambiguous parallel-edge semantics. | Reversed duplicate edges fail. |
| MOL-006 | Bond order and stereo use enumerated values. | Portable bounded vocabulary. | Unknown values fail; no stereo is inferred. |
| MOL-007 | Coordinates are all absent or all present, finite, Cartesian, right-handed and in Angstrom. | Prevent mixed/inferred coordinate frames. | Partial, non-finite, unsupported-frame or non-Angstrom documents fail. |
| MOL-008 | Residue and chain references are complete and reciprocal. | Preserve macromolecular hierarchy. | Unknown, duplicated or inconsistent membership fails. |
| MOL-009 | Disconnected components are valid. | Support salts, complexes and multiple components. | Component enumeration preserves all atoms. |
| MOL-010 | Serialization declares schema version and coordinate units. | Reproducibility and interoperability. | Unsupported schema/unit fails closed; round-trip is lossless. |

## Scientific distinctions

- **Established data convention:** element symbols follow the periodic-table symbols; coordinate unit is explicitly Angstrom.
- **Structural invariant:** references and membership must be internally consistent.
- **Not asserted:** valence correctness, aromaticity, protonation, tautomerism, stereochemical truth, chemical stability or biological function.
- **Heuristics:** none are applied in v1.
- **Experimental hypotheses:** none are encoded as rules.

Rule approval by a named scientific reviewer is required before rules can be marked approved for trusted production execution. The current rules are implementation constraints, not clinically or experimentally validated interpretations.
