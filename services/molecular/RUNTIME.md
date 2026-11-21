# A — Molecular Runtime

Status: local Python reference runtime, immutable artifact integration and Rulebook validation capability implemented. Cross-process and C++/Rust bindings remain unimplemented.

## API

- ingest_molecule(platform, molecule, parents, budget) writes canonical JSON as an immutable artifact.
- load_molecule(platform, artifact_id, budget) verifies blob integrity, media type, schema ID and embedded digest before strict parsing.
- register_molecular_service(platform) registers deterministic capability molecular.validate.v1.
- molecular_validation_rulebook() constructs the canonical validation DAG.

## Artifact contract

Media type: application/vnd.molecularis.molecule+json. Schema ID: molecularis.molecule.v1. Metadata records molecule ID/digest, formula, atom/bond counts, net charge and coordinate frame. Parent artifact IDs are preserved. Validation emits molecularis.molecular-validation-report.v1; the shared Rulebook executor persists output and run evidence.

## Resource and determinism

Graph validation, adjacency and components are O(V+E). Artifact boundaries enforce byte budgets and the store verifies content-addressed blobs. No combinatorial chemistry operation occurs. Output order follows input order; canonical JSON key ordering stabilizes digests. The model is not an OS sandbox.

## Errors and language status

Malformed values, unknown/missing/extra fields, duplicate JSON keys, non-finite constants, unsupported schema/units, wrong artifact type and digest mismatch fail closed. Python is the only implemented reference runtime. C++/Rust bindings and cross-language conformance are not claimed.
