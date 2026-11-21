# Molecularis Modular System Architecture

## System layers
1. **Core** — shared contracts, service discovery, configuration, artifact identity, provenance, errors, and integration boundaries.
2. **Services** — independently owned scientific domains.
3. **Engine** — domain algorithms and scientific operations.
4. **Runtime** — execution lifecycle, resource policy, scheduling hooks, isolation boundaries, and service-specific runtime requirements.
5. **Rulebook** — formal domain rules, constraints, construction procedures, and validation criteria.
6. **Data and schemas** — versioned inputs, outputs, artifacts, and interchange contracts.
7. **Verification** — unit, integration, reference, regression, reproducibility, and performance tests.

## Service layout
Each service has its own ENGINE.md, RUNTIME.md, RULEBOOK.md, service.yaml, and language-specific source roots under src/{cpp,python,rust}. Tests, schemas, data, and benchmarks are owned by that service.

## Dependency direction
Services may depend on approved Core contracts. Core must not depend on service implementations. Cross-service calls use versioned contracts; avoid circular dependencies. Shared primitives belong in Core only when genuinely domain-neutral.

## Migration
Existing Python modules and tests remain in place until a service-by-service migration is implemented and verified. The scaffold does not imply that existing implementations have moved or that any service is complete.
