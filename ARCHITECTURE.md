# Molecularis Modular System Architecture

## System layers
1. Core — shared contracts, service discovery, configuration, artifact identity, provenance, errors and integration boundaries.
2. MSDE — shared scientific data engine for immutable artifacts, native indexes, streaming queries, evidence lineage and Rulebook execution support. See docs/MSDE_ARCHITECTURE.md.
3. Services — independently owned scientific domains.
4. Engine — domain algorithms and scientific operations.
5. Runtime — execution lifecycle, resource policy, scheduling hooks, isolation and service-specific runtime requirements.
6. Rulebook — formal domain rules, constraints, construction procedures and validation criteria.
7. Data and schemas — versioned inputs, outputs, artifacts and interchange contracts.
8. Verification — unit, integration, reference, regression, reproducibility and performance tests.

## Dependency direction
Services may depend on approved Core/MSDE contracts. Core/MSDE must not depend on service implementations. Domain adapters are registered by services and invoked through versioned contracts. Cross-service calls use versioned contracts; avoid circular dependencies.

## MSDE authority boundary
Canonical artifacts and manifests are authoritative; indexes are derived and rebuildable. Query completeness and approximation are explicit. MSDE organizes evidence and runs generic data operations; scientific services and Rulebooks own domain semantics and acceptance criteria. No index or AI planner can certify scientific truth.

## Service layout
Each service has ENGINE.md, RUNTIME.md, RULEBOOK.md, service.yaml and language-specific source roots under src/{cpp,python,rust}. Tests, schemas, data and benchmarks are service-owned.

## Migration
Existing Python modules and tests remain in place until service-by-service migration is implemented and verified.
