# MSDE Runtime Specification

Version: 0.2.0. Status: local Python reference runtime implemented; production isolation and distributed service runtime remain unimplemented.

## Lifecycle
1. Open configuration and storage roots.
2. Validate format/version and acquire required locks.
3. Recover journaled transactions and verify active manifest.
4. Load bounded catalog/index metadata; lazily open segments.
5. Accept typed ingest, query, build and verify jobs.
6. Enforce admission control and per-job resource budgets.
7. Stream through bounded buffers with backpressure.
8. Publish immutable artifacts/index segments atomically.
9. Commit manifest and evidence records.
10. Flush/close handles and release locks on shutdown.

## Resource budgets
Every job declares maximum memory, temporary disk, bytes read/written, CPU time, wall time, candidate count, concurrency, queue depth, retry count and output size. Budget breach returns a typed resource-limit outcome and preserves diagnostic evidence.

## Concurrency and consistency
Initial implementation: single-writer per catalog with concurrent snapshot readers. Exact/range readers bind to a catalog row-ID boundary and pass that snapshot ID across pages. This is a local catalog snapshot boundary, not a durable lease; VACUUM must not run during pagination. SQLite serializes writers. Multi-writer and distributed operation are deferred.

## Recovery
Use checksummed journal records and explicit prepare/commit states. On restart, discard uncommitted temporary objects, finish or roll back recoverable transactions, verify manifest references, and mark damaged indexes for rebuild. Canonical objects are never silently repaired by changing content.

## Errors
Stable error codes cover invalid schema, missing artifact, digest mismatch, stale index, corrupt segment, unsupported predicate, incomplete query, resource limit, cancellation, conflict, I/O failure and internal defect. Messages must not expose secrets or sensitive dataset values.

## Observability and reproducibility
Emit structured events for job lifecycle, bytes/records processed, cache/index statistics, candidate counts, validation outcomes, retries, resource peaks and recovery actions. Persist snapshot ID, engine build, configuration digest, index build IDs, query plan, input digests, Rulebook version, method versions and random seeds.

## Isolation
Treat imported data as untrusted. Bound parser depth, record size, decompression ratio, path traversal, symlink handling, file count and decompression/CPU work. Never execute code from data or Rulebook documents.
