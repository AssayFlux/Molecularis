# Molecularis Master Engineering Rulebook

Status: governing policy. Applies to all repository work and every A–N service step.

## 1. North Star and scientific ownership

- Build a trustworthy, modular, Molecularis-native scientific computing system.
- Molecularis owns domain models, core algorithms, runtime contracts, data substrate and Rulebooks.
- External tools may be optional adapters, import/export bridges, research references or independent benchmarks. They must not become hidden mandatory execution backends.
- Published methods may be independently implemented with attribution and license compliance.
- Never claim implementation, accuracy, clinical utility or scientific validation without evidence.

## 2. Ordered execution

- Complete shared Core/MSDE platform gate before service A.
- Build services strictly A–N as defined in docs/SERVICE_ROADMAP.md.
- Exactly one service may be in active implementation.
- Complete and freeze the current service before starting the next.
- Shared-Core work is permitted only when it unblocks the platform or active service.
- Any change to service order or dependencies requires a DECISION_LOG entry.

## 3. Service separation

- **Engine:** domain algorithms, data structures, transformations and deterministic capabilities.
- **Runtime:** lifecycle, configuration, scheduling hooks, isolation, resource budgets, cancellation, errors, observability and shutdown.
- **Rulebook:** domain ontology, admissibility, constraints, generation/selection procedures, validation criteria, evidence requirements and acceptance.
- **Core/MSDE:** shared contracts, artifact identity/storage, indexes, query execution, provenance and generic workflow evidence.
- Core/MSDE must not own service-specific scientific semantics. Services must not duplicate shared Core behavior.

## 4. Rulebook requirements

Every executable rule must have a stable ID, version, rationale, scope/applicability, typed inputs/outputs, preconditions, postconditions, method identity, parameters, resource budgets, evidence requirements, failure behavior and testable acceptance criteria. Distinguish established facts, assumptions, heuristics, model predictions and hypotheses. Rule dependencies must be explicit and acyclic unless a bounded iterative protocol is formally specified. Rulebooks cannot waive validators or silently downgrade acceptance criteria.

## 5. Data, provenance and evidence

- Canonical artifacts are immutable and content-addressed; indexes are derived and rebuildable.
- Record input identities, output identity, schema, method/build, parameters, software/model versions, reference-data versions, units, random seeds and execution environment as applicable.
- Preserve intermediate and failed outputs as evidence where policy permits.
- Exactness, approximation, completeness, uncertainty and unsupported states are explicit.
- Every dataset/model/dependency requires provenance, terms/license review and integrity information.
- Never treat an index, cache, prediction score or AI output as scientific truth.

## 6. Validation

- Define scientific questions, intended domain, assumptions, operating range, known failure modes and acceptance thresholds before implementation.
- Use unit, property, golden-fixture, regression, integration, independent-reference, reproducibility and performance tests as appropriate.
- Repeating the same method is not independent validation.
- Reference tools must not be silently called as production implementations of native capabilities.
- Report what passed, failed, skipped and was not tested.
- Software CI success is not scientific validation or clinical evidence.

## 7. Resource and failure policy

All ingestion, queries, generation, simulation and workflow execution must declare or inherit bounded CPU, memory, GPU, disk, I/O, wall-time, concurrency and candidate limits. Cancellation, timeout, retry, partial output, corruption and recovery semantics must be explicit. A partial result must never be represented as complete.

## 8. Language and interfaces

- Python is the current implementation language and supported reference for Core/MSDE, services and Agentics.
- Do not create speculative C++, Rust or other-language source trees, placeholders, bindings or duplicate implementations.
- An additional language requires a concrete measured need, an explicit architecture decision, benchmark evidence, maintenance/security/licensing review and a defined interoperability boundary.
- Use versioned schemas/contracts; specify units, coordinate frames, precision, nullability, errors and determinism.
- Avoid duplicate algorithms without a measured reason. Preserve compatibility or document a versioned migration.

## 9. AI and automation

AI may propose plans, rules, parameters, code or repairs. Such proposals are untrusted until validated. AI cannot bypass typed contracts, authorization, resource budgets, provenance, mandatory validators, scientific thresholds or human approval requirements. No unbounded agent loops.

## 10. Repository and change control

- Develop directly on CORE; no feature branches or pull requests.
- Fetch current HEAD before every edit; use non-force expected-head updates.
- Preserve history, Assets, useful code and root README.
- Inspect references, imports and tests before deleting/moving files.
- Do not modify frozen service files without explicit authorization, except controlled urgent security/scientific-correctness remediation.
- Record architectural, dependency, order and breaking-contract decisions.
- Keep changes scoped, test them and verify resulting commit/tree.

## 11. Completion and freeze

A service is complete only when its Engine, Runtime, Rulebook, contracts, implementation, tests, scientific evidence, integration, operations docs and freeze record are accepted. Freeze records include commit, tests, evidence level, supported scope, limitations and protected paths. Subsequent changes require change control.

## 12. System and deployment decisions

Complete all services and cross-service integration, then harden and benchmark the total system. Device, accelerator, operating-system, cluster and deployment support claims must be based on measured evidence.


## 13. Agentics and the shared scientific foundation

The single governing AI architecture is [Agentics Molecularis Master Plan](docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md). The [AI Constitution](services/ai/AI_CONSTITUTION.md) is mandatory for Agentics and all A–N integrations; service Rulebooks may strengthen but may not weaken it.

- Apply **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn** across A–N without erasing domain ownership.
- Before scientific generation, audit objective, inputs, units/dimensions, assumptions, constraints, knowledge versions, validity domain, safety and resource feasibility.
- After generation, require independent verification appropriate to the claim. A proposer is never its own sole verifier.
- Keep mathematical consistency, domain validity, physical plausibility, stability, experimental realizability and demonstrated function as separate claims.
- Use authorized, license-cleared, quality-reviewed sources. Data access is not training permission. Keep retrieval/knowledge updates separate from model-weight training.
- Scientific tools must be registered adapters with versions, schemas, units, provenance, licenses, resource limits, failure semantics and verification methods. The tool catalogue is not an install list.
- Audit and reuse existing Molecularis capabilities before adding dependencies or parallel stores/runtimes. Optional engines remain optional and fail explicitly when unavailable.
- Preserve evidence class, uncertainty, assumptions, applicability, provenance and limitations through all service handoffs.
- Engineering CI, computational reference tests and independent scientific/experimental acceptance are distinct evidence levels.

Detailed requirements: [AI Constitution](services/ai/AI_CONSTITUTION.md), [Scientific Validation Standard](docs/SCIENTIFIC_VALIDATION_STANDARD.md) and [Scientific Tool Registry](services/ai/SCIENTIFIC_TOOL_REGISTRY.md).
