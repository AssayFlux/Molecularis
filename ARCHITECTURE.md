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
Each service has ENGINE.md, RUNTIME.md, RULEBOOK.md, service.yaml and Python implementation modules under the current Molecularis source package. Tests, schemas, data and benchmarks are service-owned. Do not create speculative language-specific source roots; an additional language requires an approved, measured architecture decision.

## Migration
Existing Python modules and tests remain in place until service-by-service migration is implemented and verified.


## Agentics scientific foundation

Agentics Molecularis is the coordination and reasoning layer; it is not a replacement for domain engines or a scientific authority. Its shared scientific foundation comprises typed scientific contracts, versioned knowledge/evidence, units and reference systems, mathematical and statistical computation, domain simulation adapters, construction, independent verification and evaluation. Each A–N service owns its scientific semantics, laws/equations, algorithms, constraints, Rulebooks and acceptance thresholds.

The universal service lifecycle is **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. A service may participate in only the stages supported by its declared capability. Scientific outputs preserve epistemic class, uncertainty, assumptions, applicability domain and provenance across service boundaries. The AI proposer cannot certify its own result or bypass service Rulebooks, approval, resource or safety policy.

The discipline map, tool catalogue and staged implementation are defined in [Scientific Foundation](services/ai/SCIENTIFIC_FOUNDATION.md), [Scientific Tool Registry](services/ai/SCIENTIFIC_TOOL_REGISTRY.md), [AI Constitution](services/ai/AI_CONSTITUTION.md) and [Agentics Master Plan](docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md). These are target specifications; listing a package does not mean it is installed, integrated or scientifically accepted.
