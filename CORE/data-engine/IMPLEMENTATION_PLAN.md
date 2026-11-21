# MSDE Implementation Plan

Status: staged proposal. No implementation stage is complete.

## Stage 0 — Baseline and contracts
- Record existing CI failure and repair separately as a platform task.
- Define artifact, provenance, query, index-manifest, job, error and evidence schemas.
- Establish storage format versioning and compatibility policy.
- Define threat model and data classification.
Exit: schemas validate; compatibility and recovery design reviewed.

## Stage 1 — Local artifact store and catalog
- Implement immutable content-addressed object storage and chunk manifests.
- Implement catalog metadata, lineage and checksums.
- Add atomic publication, journal recovery and corruption tests.
- Provide streaming ingest/read APIs with bounded memory.
Exit: crash-injection, digest, round-trip, large-stream and path-safety tests pass.

## Stage 2 — Native exact and ordered indexes
- Implement exact-key lookup and sorted range index segments.
- Add sparse block directory, optional Bloom filters, snapshot manifests and compaction.
- Add exact verification against canonical catalog records.
- Benchmark against linear scans and standard-library baselines.
Exit: differential correctness tests pass; reproducible memory/latency/throughput reports published.

## Stage 3 — Query execution and planning
- Implement typed predicates, planner/executor, streaming filters and pagination.
- Add statistics and deterministic cost model with bounded scan fallback.
- Record plan and completeness in every query result.
Exit: query matrix passes and planner never violates exactness or resource limits.

## Stage 4 — Scientific index adapters
Implement only when service requirements and fixtures exist: genomic intervals and variants; sequence k-mer/minimizer candidate retrieval; structure spatial candidate retrieval; chemical descriptors/fingerprints; time-series and omics matrices; graph/relationship queries.
Every approximate candidate path must have exact or domain-appropriate verification.
Exit: each adapter has domain-specific differential tests and provenance.

## Stage 5 — Rulebook DAG runtime and evidence gates
- Validate typed operation DAGs and capability declarations.
- Execute bounded steps with immutable intermediates and dependency invalidation.
- Support explicit retry/repair branches and independent validators.
- Produce auditable evidence bundles and final disposition.
Exit: protein-structure example demonstrates candidate generation, independent checks, bounded retry and acceptance/rejection with complete lineage.

## Stage 6 — Adaptive and AI-assisted planning
- Add measured adaptive partitioning and index selection.
- Evaluate learned cost estimates only after deterministic planner is stable.
- Permit AI to propose plans/parameters within typed capabilities.
- Require policy checks, human approval where configured, and mandatory independent validation.
Exit: AI proposals cannot bypass invariants; performance and failure modes are measured.

Implement one stage at a time. Do not call a prototype production-ready based on synthetic benchmarks alone.
