# Workflows Acceptance N

Engineering acceptance is distinct from scientific validation of each invoked capability.

- Canonical workflow documents round-trip and hash deterministically.
- DAG validation rejects duplicate IDs, undeclared inputs, missing capabilities and cycles.
- Topological ordering is deterministic regardless of declaration order.
- MSDE artifact lifecycle verifies schema, metadata and digest.
- Multi-capability execution uses Core RulebookExecutor and records input/output lineage and run status.
- Invalid/extra inputs fail closed; byte, operation and runtime budgets apply.
- Existing FASTA/FASTQ helpers and Galaxy connector remain available; connector credentials are not persisted.
- Registry, schemas, Ruff, compilation, tests and DAG benchmark smoke pass in CI.

University review, scientific comparisons, live Galaxy tests and platform-wide recovery/isolation gates remain deferred.
