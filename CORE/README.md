# Molecularis Core

Shared, domain-neutral infrastructure only. Core owns service contracts, capability discovery, configuration, artifact identity, provenance, common errors and cross-service integration. It must not absorb domain-specific scientific algorithms.

## Current implementation

The local Python reference platform lives in `python/molecularis/platform/`. It provides a lifecycle-managed facade, content-addressed artifact storage, SQLite catalog, lineage, metadata exact/range lookup, bounded streaming, integrity checks, capability registration and Rulebook DAG execution.

See [MSDE](data-engine/README.md) for APIs, design limits and the staged implementation plan. The reference service is local and single-catalog; cross-process service discovery, cross-language bindings and the native sorted-segment index engine remain open.
