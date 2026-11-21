# A — Molecular Rulebook

Status: ten structural rules are implemented and executable through the MSDE Rulebook runtime. Independent scientific approval remains pending.

Rule version: molecular-structural-v1. Data contract: molecularis.molecule.v1. These rules define structural integrity, not chemical or biological truth.

| Rule | Requirement | Failure condition |
|---|---|---|
| MOL-001 | Molecule has stable non-empty ID and name. | Empty, whitespace-only or overlong identifiers. |
| MOL-002 | Atom IDs are unique and elements use periodic-table symbols. | Duplicate IDs or unknown symbols. |
| MOL-003 | Formal charge is integer; isotope is positive integer or null. | Wrong types or invalid isotope. |
| MOL-004 | Bonds connect distinct existing atoms. | Self-edge or dangling endpoint. |
| MOL-005 | At most one undirected bond per atom pair. | Reversed duplicate edge. |
| MOL-006 | Bond order and stereo use bounded vocabularies. | Unsupported annotation. |
| MOL-007 | Coordinates are all absent or all present, finite, Cartesian Angstrom. | Partial/non-finite coordinates or unsupported frame/unit. |
| MOL-008 | Residue and chain membership is reciprocal. | Missing, duplicated or inconsistent hierarchy. |
| MOL-009 | Disconnected components are preserved. | Lost or omitted graph vertices. |
| MOL-010 | Serialization is versioned, strict and canonical. | Wrong version/unit, duplicate JSON keys, missing or extra fields. |

## Operational capability

Capability molecular.validate.v1 accepts a molecule artifact reference and emits a molecular validation report. It integrity-checks and parses the artifact, applies MOL-001 through MOL-010, and returns deterministic summary evidence. The Rulebook executor persists the report, run evidence and input lineage. Optional expected SHA-256 pins the expected content.

## Scientific distinctions

No valence correctness, aromaticity, protonation, tautomerism, stereochemical truth, chemical stability or biological function is asserted. No heuristics or experimental hypotheses are encoded. These rules are executable structural constraints, not experimentally or clinically validated interpretations. A named scientific reviewer must approve the Rulebook before trusted production scientific use.
