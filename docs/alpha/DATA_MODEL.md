# Alpha Shared Scientific Data Model

## Purpose
Define stable cross-device concepts before implementing UI and engines. The exact schema fields and units are to be reviewed against existing schemas before adoption; this is a conceptual model, not a new validated schema.

## Core entities
- User and Organization: identity, membership and policy context.
- Project: scientific workspace, access policy and configuration.
- Dataset: immutable or versioned input collection with source, license, format and checksum.
- Artifact: file or structured result with media type, checksum, size, storage location and provenance link.
- Workflow: versioned graph of tasks, dependencies, parameters and contracts.
- Job: one execution attempt with engine manifest, inputs, target, resource request and lifecycle state.
- Engine: versioned capability with runtime profile, accepted contracts, license and validation evidence.
- Provenance Record: immutable record of inputs, methods, versions, parameters, environment and outputs.
- Validation Record: test/reference/benchmark/independent-review evidence.
- Compute Node: paired local or institutional execution endpoint with declared capabilities and policy.

## Scientific semantics
Schemas must explicitly define biological sequence alphabets and ambiguity symbols; sequence coordinate conventions; chain/residue/atom identifiers; alternate locations and model numbers; molecular formal charges, isotopes and stereochemistry; coordinate frames and transforms; periodic boxes; physical quantities and dimensional units; missing values; uncertainty and confidence; and measured vs predicted vs inferred data.

Never rely on implicit units or coordinate assumptions. Every quantity has a unit and every structure has a declared coordinate frame/convention.

## Artifact and provenance invariants
- Content checksum is computed on upload and verified on download.
- Dataset versions are immutable; changes create new versions.
- A result references exact input artifact versions.
- Job records include engine/container/model/database versions and parameters.
- Provenance links to input and output checksums.
- Deletion is policy-controlled and audited.

## Compatibility
Use semantic schema versions. Readers declare supported versions; incompatible changes require a new major schema version and migration. Contract fixtures are shared across Python, Rust, C++ and TypeScript clients.