# MSDE Platform Acceptance Record

This record distinguishes the implemented local foundation from capabilities deliberately deferred.

## Implemented in this release

- Typed Python contracts for budgets, capabilities, execution contexts and query outcomes.
- Local immutable SHA-256 content-addressed object storage.
- SQLite catalog with WAL and FULL synchronous durability settings.
- Atomic temp-file publication before catalog visibility.
- Artifact metadata, parent lineage and indexed exact/numeric labels.
- Streamed ingestion and reads with byte/chunk limits.
- Digest verification, catalog audit and non-destructive orphan reporting.
- Explicitly incomplete bounded exact/range queries.
- Capability registry and acyclic bounded Rulebook DAG execution.
- Persisted run evidence and immutable operation outputs.

## Explicitly not claimed complete

- Multi-process writer coordination across network filesystems.
- Distributed or remote object storage, replication and consensus.
- General SQL-like query planner, joins or arbitrary predicate language.
- Compaction/LSM index segment engine, Bloom filters or specialized sequence/spatial indexes.
- Process sandboxing, OS-level CPU/memory isolation, cancellation of arbitrary Python handlers.
- Full crash fault-injection at every filesystem instruction or formal power-loss certification.
- Cross-language C++/Rust bindings and executable service discovery protocol.
- Scientific domain validation; this platform is domain-neutral infrastructure.

## Operational constraints

- One local catalog, SQLite single-writer semantics, concurrent readers.
- Store root must be on a filesystem with reliable atomic rename semantics.
- Do not use network filesystems until their locking, fsync and rename semantics are separately validated.
- Artifact IDs are logical identities; SHA-256 digests identify bytes.
- Orphan blobs are reported by audit and are not automatically deleted.
- Exact label queries use canonical JSON values; numeric range queries index JSON numeric metadata.
- Query results report bounded candidate count and completeness; no approximate mode is implemented.

## Gate

The local platform gate is accepted only after CI executes the platform test suite and the repository's full baseline. This record is an implementation scope declaration, not a claim of distributed readiness or scientific validation.
