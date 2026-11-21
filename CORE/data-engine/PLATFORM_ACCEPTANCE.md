# MSDE Platform Acceptance Record

Status: local reference implementation v0.2; full production platform acceptance remains open.

## Implemented and covered by tests

- Typed budgets, capability descriptors, execution contexts and stable platform errors.
- Local immutable SHA-256 content-addressed object storage.
- SQLite WAL catalog with FULL synchronous durability setting.
- Atomic temporary-file publication before catalog visibility.
- Artifact metadata, parent lineage and indexed exact/numeric labels.
- Streamed ingestion and reads with byte/chunk limits.
- Digest verification, catalog audit and non-destructive orphan/dangling-lineage/temporary-file reporting.
- Consistent SQLite catalog backup plus verified referenced-object copy, manifest and atomic non-overwriting publication.
- Restore into a new store directory with catalog/object hash checks and post-restore audit (regression tests passed in [CI #44909367708](https://github.com/AssayFlux/Molecularis/actions/runs/44909367708); core 758 passed/12 skipped and all optional profiles green).
- Exact/range query pagination bound to an explicit catalog row-ID snapshot, with stable ordering and explicit completeness.
- Capability registry and acyclic bounded Rulebook DAG validation.
- Success and failure run evidence, including failed operation identity and error category.
- Input artifact IDs are linked as parents of derived Rulebook output artifacts.
- Optional dependency CI profiles for sequence, genomics and chemistry.
- Repository-wide JSON Schema validation is part of core CI and passed in run #135 after repairing a malformed legacy schema.

## Explicitly not claimed complete

- Native append-only sorted-segment index manager, Bloom filters, compaction or specialized sequence/spatial indexes. SQLite B-tree indexes are the current implementation.
- A general typed query planner, joins, opaque signed cursors or cross-process snapshot leases.
- Multi-process writer coordination across network filesystems.
- Distributed or remote object storage, replication and consensus.
- Process sandboxing, OS-level CPU/memory isolation, forced cancellation of arbitrary Python handlers.
- Encrypted/signed backups, off-host replication and scheduled restore drills.
- Full crash fault-injection at every filesystem instruction or formal power-loss certification.
- Cross-process service discovery and remote execution are not implemented; they are not prerequisites for the current local Python reference scope.
- Scientific domain validation; this platform is domain-neutral infrastructure.

## Operational constraints

- One local catalog, SQLite single-writer semantics, concurrent readers.
- Store root must be on a filesystem with reliable atomic rename semantics.
- Do not use network filesystems until locking, fsync and rename semantics are separately validated.
- Artifact IDs are logical identities; SHA-256 digests identify bytes.
- Orphan blobs are reported by audit and are not automatically deleted.
- Backup manifests are integrity checks, not cryptographic signatures; backups are not encrypted. Store backups on a separate access-controlled destination.
- Backup/restore supports a new destination only; it does not overwrite an existing store.
- Exact label queries use canonical JSON values; numeric range queries index finite JSON numeric metadata.
- Query pages must reuse the same snapshot ID. Snapshot IDs are current catalog row-ID boundaries, not durable leases; do not VACUUM the catalog while a multi-page query is in progress.
- Query results report bounded candidate count and completeness; no approximate mode is implemented.
- Rulebook handlers are trusted in-process Python code. They must be reviewed and resource-safe; declared wall-time checks occur between handlers and cannot preempt a running handler.

## Acceptance gate

The platform is accepted for the next service only after:
1. Core CI and all optional scientific profiles pass with no unexplained skips in their declared scope.
2. JSON schemas validate.
3. Artifact integrity, pagination, lineage and success/failure evidence tests pass.
4. Filesystem crash recovery, encrypted/off-host backup, security and resource-isolation risks have an explicit reviewed disposition.
5. The supported Python reference scope and any required service-integration boundaries are explicitly documented. Additional-language bindings are not required; they need a separate approved decision based on measured need.

Python is the current supported implementation baseline; no C++/Rust bindings or language ports are required by this acceptance record. This record is an implementation scope declaration, not a claim of distributed readiness or scientific validation.
