# A — Molecular Runtime

Status: local Python reference runtime implemented for the v1 model; cross-process and native bindings remain open.

## Lifecycle

The v1 runtime is a pure in-process value model. Construction validates objects immediately; invalid objects fail with `ValueError`. It performs no file, network, database, subprocess or GPU operations. The caller owns persistence and execution budgets.

## Serialization

Use `Molecule.to_dict()` and `Molecule.from_dict()` for the `molecularis.molecule.v1` document. The contract requires Angstrom coordinates and the `cartesian_right_handed` frame. Unknown schema versions and unsupported units fail closed. `Molecule.sha256` hashes canonical JSON with sorted object keys and finite JSON values.

## Resource and determinism policy

- Graph validation and adjacency construction are O(V + E), excluding identifier hashing.
- Connected components are O(V + E).
- No implicit atom expansion or combinatorial chemistry operation occurs.
- Input collection size is currently caller-bounded; the MSDE service wrapper must apply artifact and execution budgets before accepting untrusted large documents.
- Output ordering follows the supplied atom/bond/residue/chain order; the digest is stable for identical serialized ordering.
- No random operation exists in v1.

## Errors

Malformed identifiers, element symbols, coordinates, references, duplicate IDs/edges, inconsistent hierarchy, schema versions or units raise explicit errors. The model does not repair or silently normalize invalid input.

## Integration boundary

Python is the current reference implementation. The manifest's C++ and Rust roots are reserved for future implementations and are not represented as implemented. Cross-language conformance must be established against the JSON schema and shared golden fixtures before those runtimes are advertised.

## Shutdown and cancellation

No long-running task or owned resource exists in this in-process model; cancellation and shutdown are therefore not applicable. A future service process must implement the platform lifecycle contract rather than extending this module with hidden global state.
