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

- Primary languages: C++, Python and Rust.
- Python: orchestration, research-facing APIs and scientific interfaces.
- C++: performance-sensitive numerical/geometry kernels when benchmarks justify it.
- Rust: memory-safe systems, concurrency, parsers and resource management when justified.
- Other languages require written technical justification.
- Use versioned language-neutral schemas/contracts; specify units, coordinate frames, precision, nullability, errors and determinism.
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
