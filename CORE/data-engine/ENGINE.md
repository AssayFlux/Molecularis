# MSDE Engine Specification

Version: 0.1.0-draft. Status: proposed architecture; not implemented.

## Mission
Provide a reusable, auditable, bounded-resource substrate that lets Molecularis services ingest, identify, store, index, retrieve, transform and verify very large scientific datasets and intermediate artifacts.

## Design invariants
1. Every artifact has a stable identifier, schema/type, content digest, size, provenance and lifecycle state.
2. Raw inputs are immutable. Transformations create new artifacts and explicit parent links.
3. Indexes are derived and rebuildable; canonical artifact bytes and manifests are authoritative.
4. Exact queries return complete verified matches or an explicit incomplete/error status. Approximate search is labelled and exposes verification behavior.
5. Index results never constitute scientific validation.
6. Scans, queues, caches, retries, fan-out and memory allocations are bounded by declared budgets.
7. Large payloads are streamed or memory-mapped in chunks; full materialization is opt-in and budget-checked.
8. Every query and transformation is attributable to engine version, schema version, parameters and input snapshot.
9. Corruption, stale indexes and interrupted writes are detectable and recoverable.
10. Core contracts remain domain-neutral; biological semantics live in service adapters.

## Layered architecture
- Artifact catalog: identity, type, schema, digest, size, labels, lineage and retention metadata.
- Object store: immutable content-addressed blobs/chunks with checksums and atomic publication.
- Transaction journal: write-ahead intent/commit records and recovery metadata.
- Index manager: versioned index families, manifests, build/rebuild, compaction and health.
- Query planner: selects eligible index paths from query shape, data statistics, freshness and budget.
- Query executor: bounded streaming operators, filters, joins and deterministic ordering where requested.
- Evidence ledger: run records, source references, parameters, checks, reports and decision history.
- Verification gate: validates integrity, completeness, schema and domain-provided acceptance predicates.
- Rulebook adapter: turns declared data requirements and operation dependencies into plans; scientific algorithms remain in services.

## Artifact identity and storage
Artifact identity is independent of filename or storage location. Use SHA-256 over canonical bytes or a documented canonical representation. Keep logical artifact ID separate from content digest so identical bytes can have distinct scientific roles or provenance contexts.

Store large objects as immutable blobs, optionally chunked. A manifest records ordered chunk digests, byte lengths, media/schema type, encoding, source, license/provenance and parent artifact IDs. Verify chunk and whole-object digests on ingest and configurable read checkpoints. Never rewrite source objects in place.

The catalog stores metadata and references, not large payloads. Storage backends are abstract interfaces; first native backend should be local filesystem with atomic temp-write, fsync where supported, and rename publication. Remote/object-store backends are later adapters.

## Index portfolio
No universal index. Each index declares supported predicates, update model, complexity expectations, memory/disk overhead, exactness, build version and invalidation rules.

Initial families, staged:
- Exact key: artifact IDs, identifiers and composite keys.
- Ordered/range: numeric and lexical ranges, timestamps and sortable metadata.
- Hierarchical partition: partition pruning over declared dimensions; adaptive partition selection is evidence-driven.
- Interval: genomic coordinates and other start/end ranges.
- Inverted: token/term-to-record postings for annotations and metadata.
- Sequence: k-mer/minimizer candidate index followed by exact alignment/verification.
- Spatial: coordinate-cell candidate index followed by exact geometric checks.
- Vector/embedding: future optional approximate-nearest-neighbor index; never required for exact correctness.

Native storage evolution proposal: append-only write-ahead journal plus immutable sorted index segments (LSM-style), sparse block directories and optional Bloom filters for negative membership checks. Range queries merge sorted runs. Compaction creates new immutable segments and atomically advances a manifest. Bloom filters may reject definite non-membership only; positive results require exact lookup. A native B+tree may be evaluated for update-heavy/range workloads after benchmarks. Do not implement both without evidence.

## Query contract
A query declares target type/schema, typed predicate values with units/coordinate conventions, exact or approximate mode, snapshot boundary, result limit/pagination token, and CPU/memory/I/O/wall-time/candidate budgets.

Response includes results or streaming cursor, snapshot ID, index versions, candidates examined, exact matches, completeness, approximation label, warnings and provenance. A budget cutoff returns incomplete, never silently partial-as-complete.

## Adaptive planning
Planner selects indexes and scan operators using predicate support, freshness, selectivity estimates, partition statistics, expected I/O, memory and explicit budgets. It may fall back to a bounded scan. Planner decisions are recorded for replay and benchmark review. Initially use deterministic rules; learned cost models are future optional hints and cannot override correctness or budgets.

## Rulebook and repeated scientific verification
A Rulebook declares a versioned DAG of operations and gates. Each node defines inputs, outputs, method identity, parameter schema, resource budget, preconditions, postconditions, retry policy and evidence requirements. Intermediate artifacts are immutable and linked to their parent run.

Example protein-structure workflow:
1. Resolve sequence and source evidence through indexes.
2. Validate sequence identity, completeness and provenance.
3. Generate candidate structures using an explicitly selected Molecularis capability.
4. Run independent structural checks: geometry, clashes, stereochemistry, confidence/uncertainty and domain constraints.
5. Compare against predeclared acceptance thresholds and independent evidence.
6. Route failures to an allowed correction/retry node with bounded attempts and recorded parameter changes.
7. Re-run all invalidated downstream checks.
8. Publish only a result that passes mandatory gates; otherwise return rejected/needs-review with complete evidence.

A repeated check is not independent merely because it runs twice. Independence requires a distinct method, data source, implementation, or justified validation design.

## Evidence and provenance
Record immutable run ID, parent run, input artifact IDs/digests, dataset and model versions, code/engine build, schema and Rulebook versions, parameters, random seeds, environment/hardware where relevant, resource usage, warnings, intermediate outputs, validator identities/results, reviewer overrides and final disposition. Preserve failed runs as evidence; do not overwrite them.

## AI-readiness boundary
Future AI components may propose query plans, select approved methods, prioritize candidates, suggest parameter changes, or summarize evidence. They operate through typed capability contracts and sandboxed budgets. They cannot invent provenance, mark artifacts verified without validators, change thresholds silently, suppress failed checks, exceed resource limits, call undeclared capabilities, or turn approximate retrieval into exact claims.

Every AI proposal is a plan requiring validation, policy authorization and an auditable decision record. Deterministic execution and independent verification remain authoritative.

## Deferred decisions
Distributed consensus, multi-writer replication, vector index implementation, GPU acceleration, compression codecs, encryption/key management, retention/erasure policy and remote storage require explicit use cases, threat model, data classification and benchmarks.
