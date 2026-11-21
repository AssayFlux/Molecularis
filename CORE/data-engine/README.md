# Molecularis Scientific Data Engine (MSDE)

Status: local platform implementation v0.1 exists; full platform gate remains open.

MSDE is a Molecularis-owned, domain-neutral data substrate for scientific artifacts, indexing, streaming, provenance, evidence and Rulebook execution support. Scientific services consume stable Core contracts; Core does not depend on service implementations.

## Executable implementation

The Python reference implementation is in `python/molecularis/platform/`:

- `contracts.py`: budgets, capability descriptors, execution context and typed platform errors.
- `store.py`: immutable SHA-256 object store, SQLite catalog, lineage, scalar metadata indexes, bounded streaming, integrity audit and run ledger.
- `runtime.py`: capability registry and validated acyclic Rulebook DAG executor.
- `service.py`: lifecycle-managed local reference service and JSON capability-manifest loader.

Quick start:

```python
from molecularis.platform import MolecularisPlatform

platform = MolecularisPlatform("./molecularis-data")
platform.start()
artifact = platform.ingest(
    b"scientific payload",
    media_type="application/octet-stream",
    schema_id="urn:example:raw:1",
    metadata={"dataset": "example", "quality_score": 0.98},
)
assert platform.store.get(artifact.artifact_id).digest == artifact.digest
platform.close()
```

The local catalog uses SQLite WAL with full synchronous mode. Immutable blob bytes are written and fsynced to a temporary file, then atomically renamed into the digest path before the catalog transaction makes the artifact visible. Catalog metadata and lineage are transactional. Readers verify object size and SHA-256 before returning content. Orphan blobs are reported, never silently deleted.

## Contracts

- `schemas/artifact-manifest.schema.json` and `schemas/query-request.schema.json`: initial MSDE interchange drafts.
- `schemas/capability-manifest.schema.json`: JSON capability declaration contract.
- `schemas/platform-envelope.schema.json`: language-neutral request/response/error envelope.

The Python runtime is a reference implementation, not yet a cross-language wire service. Capability manifests declare data only; they never import or execute code.

## Explicit limits

- One local catalog; SQLite provides single-writer transaction serialization and concurrent snapshot readers.
- Metadata exact/range indexes currently use SQLite B-tree indexes, not the planned append-only sorted-segment index engine.
- Query API supports exact scalar metadata and numeric ranges; it is not a general query planner.
- Rulebook execution is in-process. Handlers are trusted code; this is not an OS sandbox and cannot forcibly interrupt arbitrary handlers.
- The current executor has bounded step count, output size and wall-time checks between operations, not preemptive CPU/memory/GPU isolation.
- Distributed storage, remote backends, replication, C++/Rust bindings, specialized biological indexes and AI planning are not implemented.
- Crash safety is designed around immutable blob publication plus SQLite transactions; comprehensive power-loss and boundary-by-boundary fault-injection certification remains open.

MSDE is not a scientific inference model. Search and ranking do not establish scientific truth. AI proposals cannot bypass deterministic contracts, resource controls or independent verification.
