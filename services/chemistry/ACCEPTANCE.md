# Chemistry D — Engineering acceptance record

Status: Engineering implementation complete pending CI evidence. University scientific review, independent reference comparison and formal contract freeze are deferred until A–N engineering completion under DEC-0010.

## Implemented slice
- Immutable canonical explicit-atom molecular graph artifacts with SHA-256 identity and MSDE lineage.
- Bounded SDF V2000/V3000 ingestion using the existing parser.
- Five executable MSDE capabilities: validation, graph descriptors, path fingerprint, substructure matching and Tanimoto similarity.
- Executable Rulebook CHM-001–CHM-006; versioned JSON Schemas and capability registry.
- Existing optional RDKit adapter retained for sanitization, stereochemistry-aware canonical SMILES, molecular descriptors and Morgan fingerprints. It is not silently substituted for the native graph algorithms.

## Explicit exclusions
Native v1 does not claim chemical valence/aromaticity sanitization, stereochemical interpretation, protonation/tautomer normalization, implicit-hydrogen inference, reaction balancing, conformer generation, quantum chemistry, ADMET or clinical prediction. Path fingerprints are not ECFP/Morgan fingerprints. No university scientific acceptance or production readiness is claimed.

## Verification
Record the exact commit and CI run here after the CORE workflow completes.
