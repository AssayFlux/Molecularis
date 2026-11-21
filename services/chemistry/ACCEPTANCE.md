# Chemistry D — Engineering acceptance record

Status: Engineering implementation complete and CI-verified. University scientific review, independent reference comparison and formal contract freeze are deferred until A–N engineering completion under DEC-0010.

## Implemented slice
- Immutable canonical explicit-atom molecular graph artifacts with SHA-256 identity and MSDE lineage.
- Bounded SDF V2000/V3000 ingestion using the existing parser.
- Five executable MSDE capabilities: validation, graph descriptors, path fingerprint, substructure matching and Tanimoto similarity.
- Executable Rulebook CHM-001–CHM-006; versioned JSON Schemas and capability registry.
- Existing optional RDKit adapter retained for sanitization, stereochemistry-aware canonical SMILES, molecular descriptors and Morgan fingerprints. It is not silently substituted for the native graph algorithms.

## Explicit exclusions
Native v1 does not claim chemical valence/aromaticity sanitization, stereochemical interpretation, protonation/tautomer normalization, implicit-hydrogen inference, reaction balancing, conformer generation, quantum chemistry, ADMET or clinical prediction. Path fingerprints are not ECFP/Morgan fingerprints. No university scientific acceptance or production readiness is claimed.

## Verification
Engineering commit: b2db7823c2fe3d1a0a48c9479a13b571ebb1b98c (initial D implementation); lint correction: b7d077e07c95cf94fab1c862b025651e179077a9.

CI run [#44888785327](https://github.com/AssayFlux/Molecularis/actions/runs/44888785327) on 93a7b10: all four jobs succeeded. Core: 644 passed, 12 skipped. Optional Chemistry: 652 passed, 4 skipped; Sequence: 647 passed, 9 skipped, 4 warnings; Genomics: 645 passed, 11 skipped. Capability registry valid; 37 JSON Schemas validated; Ruff E9/F, Python compilation and all benchmark smoke steps passed.


## Agentics scientific acceptance

- [ ] Chemical scope, assumptions, supported domains and units documented: Chemical graph theory, organic/inorganic/physical chemistry, thermodynamics, kinetics, quantum chemistry, stereochemistry, reaction mechanisms and analytical uncertainty.
- [ ] Pre-generation checks validate schema, valence, charge, stereochemistry, conditions and resource limits.
- [ ] Independent post-generation checks support each declared chemical claim.
- [ ] Thermodynamic/kinetic/numerical assumptions, uncertainty and limitations reported where applicable.
- [ ] Provenance, tool versions, parameters and artifact lineage retained.
- [ ] Optional tools have license/version and independent verification evidence.
- [ ] Engineering and scientific acceptance are separate.

Shared requirements: ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_FOUNDATION.md.
