# Molecularis Core

Shared, domain-neutral infrastructure only. Core owns service contracts, capability discovery, configuration, artifact identity, provenance, common errors and cross-service integration. It must not absorb domain-specific scientific algorithms.

## Current implementation

The local Python reference platform lives in `python/molecularis/platform/`. It provides a lifecycle-managed facade, content-addressed artifact storage, SQLite catalog, lineage, metadata exact/range lookup, bounded streaming, integrity checks, capability registration and Rulebook DAG execution.

See [MSDE](data-engine/README.md) for APIs, design limits and the staged implementation plan. The reference service is local and single-catalog; cross-process service discovery, cross-language bindings and the native sorted-segment index engine remain open.


## Agentics scientific foundation integration

Agentics Molecularis is the intelligence and orchestration layer above the scientific platform. It uses the shared scientific contracts, knowledge/evidence model, unit-aware computation, provenance and verification gates while delegating domain operations to A–N service engines. It must not bypass Core contracts, MSDE artifact integrity, resource budgets or service-owned Rulebooks.

The governing architecture is documented in [Agentics Molecularis Master Plan](../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md); shared scientific disciplines and candidate adapters are documented in [Scientific Foundation](../services/ai/SCIENTIFIC_FOUNDATION.md) and [Scientific Tool Registry](../services/ai/SCIENTIFIC_TOOL_REGISTRY.md). These are target specifications, not claims that every listed tool is installed or validated.
