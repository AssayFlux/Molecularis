# MSDE Implementation Plan

Status: staged delivery with a working local reference slice. Do not equate a completed stage's software tests with scientific validation.

## Stage 0 — Baseline and contracts
- [x] Establish versioned artifact/query drafts and format versioning.
- [x] Establish typed Python budget, capability, execution-context and error contracts.
- [x] Add JSON capability-manifest and platform-envelope schemas.
- [x] Add repository-wide JSON Schema validation to CI (repair malformed legacy schema before acceptance).
- [ ] Complete threat model and data classification review.
Exit: schemas validate; compatibility and recovery design reviewed.

## Stage 1 — Local artifact store and catalog
- [x] Immutable SHA-256 content-addressed blob store.
- [x] SQLite catalog, metadata, lineage and checksums.
- [x] Atomic temporary-file publication before catalog visibility.
- [x] Streamed ingest/read with byte and chunk limits.
- [x] Integrity verification and non-destructive orphan audit.
- [x] Exact metadata and numeric range lookup using SQLite indexes.
- [ ] Crash-boundary fault injection, catalog backup/restore and corruption-recovery matrix.
- [ ] Large-stream memory and throughput benchmarks.
Exit: fault-injection, digest, round-trip, large-stream and path-safety tests pass.

## Stage 2 — Native exact and ordered indexes
- [ ] Implement append-only sorted index segments, sparse directories, snapshots and compaction.
- [ ] Add exact verification against canonical catalog records and differential benchmarks.
- Note: current metadata indexes are SQLite B-tree indexes, not the planned native segment engine.
Exit: differential correctness tests pass; reproducible memory/latency/throughput reports published.

## Stage 3 — Query execution and planning
- [x] Bounded exact scalar metadata lookup and numeric range lookup.
- [x] Explicit result completeness and candidate limits.
- [x] Stable catalog snapshot-bound exact/range pagination with explicit completeness; typed predicate/query planner remains open.
- [ ] Deterministic cost model and bounded scan fallback.
Exit: query matrix passes and planner never violates exactness or resource limits.

## Stage 4 — Scientific index adapters
Implement only when service requirements and fixtures exist: genomic intervals and variants; sequence k-mer/minimizer candidate retrieval; structure spatial candidate retrieval; chemical descriptors/fingerprints; time-series and omics matrices; graph/relationship queries. Approximate candidate paths require exact or domain-appropriate verification.

## Stage 5 — Rulebook DAG runtime and evidence gates
- [x] Capability declaration registry and acyclic dependency validation.
- [x] In-process bounded-step Rulebook executor and immutable operation output artifacts.
- [x] Persist successful run evidence.
- [x] Persist failed Rulebook run evidence and link artifact-valued operation inputs to derived outputs.
- [ ] Preconditions/postconditions, typed input/output validation, retry policies and independent-validator gates.
- [ ] Dependency invalidation and bounded repair branches.
Exit: multi-operation workflow demonstrates candidate generation, independent checks, bounded retry and acceptance/rejection with complete lineage.

## Stage 6 — Adaptive and AI-assisted planning
Deferred until deterministic planner and evidence gates are stable. AI proposals remain untrusted and cannot alter mandatory thresholds or validators.

## Platform lifecycle and service discovery
- [x] Local reference service lifecycle and JSON capability-manifest loader.
- [ ] Add cross-process service discovery only if a concrete deployment requirement is approved; the current supported reference remains the local Python runtime.

Python is the current implementation baseline. Do not add speculative language bindings or source roots. Only mark the full platform gate passed when all mandatory Phase 1 exits in the Master Development Plan have evidence.
