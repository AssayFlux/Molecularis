# Molecularis Master Development Plan

Version: 2.0. Status: governing, living plan; material changes require a decision-log entry.

## Mission and delivery strategy

Follow [NORTH_STAR.md](NORTH_STAR.md). Build the shared platform first, then complete the A–N scientific services strictly one at a time. Each service is a complete vertical slice: discovery, specification, native engine, runtime, Rulebook, contracts, data, validation, tests, integration, documentation, acceptance and freeze.

## Phase 0 — Repository trust baseline

- Verify CORE head and preserve assets, history and useful existing code.
- Inventory implementations, public imports, tests, schemas, datasets, licenses, dependencies and CI.
- Establish a truthful status register and reproducible baseline.
- Audit legacy Python modules before moving or replacing them.

Exit: repository inventory, baseline and migration risks are documented.

## Phase 1 — Shared Core and MSDE platform gate

- Stable service identity/discovery and versioned request/response/error envelopes.
- Artifact identity, canonical schemas, units, provenance, run identity and capability registry.
- MSDE immutable content-addressed artifact store, catalog, journal/recovery and bounded streaming.
- Exact-key and ordered/range indexes first; other index families justified by workloads and benchmarks.
- Query execution with snapshot, budgets, pagination and explicit completeness/approximation.
- Evidence ledger and generic Rulebook DAG execution gates.
- C++/Python/Rust contract interoperability and reference service.
- Security/threat model, schema evolution and failure-recovery tests.

Exit: an executable reference service can discover, ingest, query, transform, validate and publish immutable artifacts with provenance under declared budgets. Architecture documents alone do not satisfy this gate.

## Phase 2 — Scientific services A–N

Follow [SERVICE_ROADMAP.md](SERVICE_ROADMAP.md) without parallel implementation:

A Molecular → B Sequence → C Structure → D Chemistry → E Protein → F Genomics → G DNA/RNA → H Simulation → I Kinetics → J Omics → K Phylogeny → L Pharmacogenomics → M Cohorts → N Workflows.

Each service must pass every mandatory service acceptance gate and be frozen before the next step starts. A step may reuse existing implementation after audit and migration; it does not require needless rewrites.

## Phase 3 — Cross-service integration

- Versioned artifact handoff and provenance continuity.
- Workflow DAGs, deterministic replay and bounded retry/recovery.
- Dependency invalidation when upstream artifacts or rules change.
- End-to-end scientific fixtures spanning multiple accepted services.

Exit: representative cross-domain workflows are reproducible and independently validated.

## Phase 4 — System hardening and scale

Security, isolation, resource accounting, numerical stability, dependency/supply-chain governance, backup/restore, diagnostics, performance and memory regression, failure injection and release evidence.

Exit: system-level acceptance report with explicit supported workload envelope and known limitations.

## Phase 5 — Deployment and device decisions

Only after Phase 4, measure CPU, memory, GPU, storage, operating systems, accelerators, network and concurrency needs. Publish supported profiles from measured evidence.

## Work-in-progress and change limits

- One active scientific service at a time.
- Shared-Core work only when it unblocks the platform or active service.
- Every task has scope, exact paths, acceptance criteria, dependencies and verification plan.
- Do not delete or migrate legacy code without usage/import/test audit and compatibility plan.
- No feature branches or PRs; work directly on CORE with non-force, expected-head updates.
- Preserve Assets and root README; README is updated as project state changes.
- Record architectural, order, dependency and breaking-contract decisions.

## Completion and freeze rule

A service is complete only when Engine, Runtime, Rulebook, contracts, tests, scientific evidence, integration, operational documentation and freeze record are accepted. Generic CI success is necessary but not sufficient. Frozen changes require explicit authorization or the narrowly controlled critical-remediation process.
