# Chemistry Engine D — v1 engineering slice

Status: implemented; independent scientific review deferred until A–N completion.

## Ownership and inputs
The native engine owns a canonical explicit-atom graph model and bounded operations over SDF V2000/V3000 input. Existing parsers, graph descriptors, path fingerprints, exact subgraph matcher and Tanimoto function are reused. Input coordinates are Angstroms. Atom elements are restricted to the current explicit supported set.

## Algorithms
- Strict bounded SDF parsing; one molecule per ingest; UTF-8 provenance SHA-256.
- Canonical JSON graph artifact with exact fields and deterministic SHA-256 identity.
- Connected components, cycle rank, heteroatom count and degree histogram.
- Deterministic SHA-256 path features, maximum path length 1–6, caller-set feature/walk ceilings.
- Backtracking exact element/bond-order subgraph match with a hard search-state ceiling.
- Set-based Tanimoto similarity over native path features.

## Optional adapter
The existing RDKit adapter remains an optional, version-reported backend for chemical sanitization, canonical isomeric SMILES, molecular descriptors and Morgan fingerprints. It is not a required runtime dependency and does not replace native capability semantics.

## Non-goals
No implicit H, valence/aromaticity sanitization, stereochemical assignment, tautomer/protonation normalization, reactions, conformers, force fields, quantum chemistry, docking, ADMET, activity or clinical predictions.


## Shared Agentics scientific foundation

Participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. Priority disciplines: Chemical graph theory, organic/inorganic/physical chemistry, thermodynamics, kinetics, quantum chemistry, stereochemistry, reaction mechanisms and analytical uncertainty.

Use shared units/dimensions, evidence, uncertainty and provenance contracts while retaining this service's chemical semantics, algorithms and validators. Agentics cannot override the chemistry Rulebook. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
