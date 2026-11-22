# Agentics Molecularis — Acceptance and Phase Gates

The governing architecture and detailed scope are in [AGENTICS_MOLECULARIS_MASTER_PLAN.md](../../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md). This checklist is evidence-driven. A checked item requires a commit and test/CI/benchmark evidence.

## Existing implementation evidence

- [x] Model-agnostic callable planner and active A–N capability catalog.
- [x] Strict Workflow v1 parsing/validation and bounded operation count.
- [x] Exact declared input keys and artifact integrity checks.
- [x] Persisted plan artifact with input parent lineage.
- [x] Explicit approval gate and Core Rulebook execution path.
- [x] Fresh-runtime A–N bootstrap.
- [x] Initial implementation CI: [run #44901363429](https://github.com/AssayFlux/Molecularis/actions/runs/44901363429), commit `2b6eced852fb049a81f6b087bb94e5e946047750`.

This evidence does not prove the new knowledge-to-construction architecture is implemented or scientifically validated.

## P0 — Repository truth, safety and reliability

- [ ] Reconcile docs, code, branch and CI.
- [ ] Threat model, trust boundaries, privacy and egress policy.
- [ ] OS-level sandbox, resource isolation and process-tree termination.
- [ ] Failure, cancellation, timeout and partial-run evidence.
- [ ] Artifact backup/restore, corruption and crash-boundary tests.
- [ ] Reproducibility and documentation baseline.

**Gate:** engineering safety/recovery evidence is complete; blockers are explicit.

## P1 — Universal Scientific Knowledge Engine

- [x] Typed concepts/entities/relations and versioned domain knowledge packages.
- [x] Quantities, SI dimensions, units, safe compound-unit conversion and coordinate/reference systems.
- [x] Equation/law records with typed variables, assumptions, applicability domains and source references, plus ordered mechanism steps with typed entity/evidence references; equation expressions are inert text.
- [x] Evidence classes/statuses, provenance/source/license metadata, uncertainty and explicit contradictory-evidence links.
- [x] Versioned JSON knowledge/quantity schemas, deterministic query interfaces and Core ArtifactStore persistence with parent lineage.
- [x] A–N domain knowledge boundary map.
- [x] Deterministic fixtures and round-trip/type/unit/provenance tests, including quantity and Core artifact round-trip serialization.

**Gate: ENGINEERING PASSED.** CI #45046306359 on `819eb1fff6785fa49530ab5bf8b30e5280111712`: 769 passed, 12 skipped, 0 failed; 66 JSON Schemas validated; Ruff, compilation, benchmark smoke tests and optional Chemistry/Genomics/Sequence profiles passed. The gate covers the reference implementation only; it does not claim comprehensive knowledge or independent scientific validation. P0 remains open and blocks progression to later phases and model training.

## P2 — Shared reasoning and construction primitives

- [x] Restricted symbolic expressions, safe AST evaluation, derivation traces and dimensional inference.
- [x] Bounded bisection solver, partial-pivot dense linear-system solver and composite Simpson integration with residual/error and convergence diagnostics.
- [x] Descriptive statistics, correlation, deterministic bootstrap, first-order uncertainty propagation and seeded Monte Carlo.
- [x] Local sensitivity and binary probability calibration metrics.
- [x] Deterministic graph topology/path operations, unit/reference-frame-safe 3D vector geometry, hard/soft constraints, bounded weighted grid optimization and explicit infeasible/budget-exhausted states.
- [x] Reconstruction/generalization/exploration task and candidate contracts, pre-generation audit and versioned schema.
- [x] Distinct proposer/verifier examples in sequence and chemical formula representation domains.
- [x] Negative, boundary, determinism, dimensional, linear algebra, integration, graph, geometry, solver, uncertainty and optimization tests.

**Engineering gate: PASSED.** GitHub Actions [run #45047445495](https://github.com/AssayFlux/Molecularis/actions/runs/45047445495), tested commit `b55efdaaae8e276c17c22b272fec94b0131f316e`: 788 passed, 12 skipped, 0 failed; 67 JSON schemas validated; Ruff, compilation, benchmark smoke tests and all optional scientific profiles passed. Domain fixtures demonstrate software contract behavior and verifier separation; they are not independent scientific validation. P0 safety, integration and recovery gates remain open and are not waived.

## P3 — A–N Knowledge-to-Construction integration

- [ ] Service-specific knowledge packages and governing principles.
- [ ] Construction/evaluation interfaces adapted to existing service engines.
- [ ] Domain Rulebooks and independent checks.
- [ ] Known, edge, negative, constructed and out-of-domain test cases.
- [ ] Cross-service typed artifact handoff and provenance continuity.
- [ ] Evidence and epistemic labels on all scientific outputs.

**Gate:** each service demonstrates its own lifecycle; cross-domain workflows pass engineering and applicable scientific review gates.

## P4 — Agentics orchestration maturity

- [ ] Intent/entity/task and clarification contracts.
- [ ] Optional provider-neutral LLM adapter and deterministic mock.
- [ ] Capability-schema-derived constrained tool calls.
- [ ] SKE-aware Workflow v1 planner and approval binding.
- [ ] Artifact-only claim-grounded answer composer.
- [ ] Trace, cancellation, bounded iteration and policy enforcement.
- [ ] At least 50 grounded/adversarial evaluation cases.
- [ ] Prompt injection, fabricated laws, unit errors, uncertainty, out-of-domain and unsupported-claim tests.

**Gate:** curated evaluation thresholds pass; zero unsupported scientific claims in the curated suite; every claim resolves to artifact fields.

## P5 — Optional scientific models and training

- [ ] Baseline demonstrates a measured need.
- [ ] Exact data/code/checkpoint license and privacy audit.
- [ ] Model provenance, dataset snapshot and leakage-resistant split.
- [ ] Reproducible benchmark and calibration.
- [ ] Optional predictor adapters remain one method among many.
- [ ] Predictions/simulations/constructed candidates remain distinct from observations.

**Gate:** reproducible benchmark demonstrates justified improvement; no unsupported accuracy claims.

## P6 — Controlled discovery and design

- [ ] Per-domain risk assessment and policy.
- [ ] Bounded candidate generation and objective/stop conditions.
- [ ] Independent verification and adversarial screening.
- [ ] Human and institutional review.
- [ ] Biosecurity/chemical safety review where relevant.
- [ ] Disabled-by-default deployment policy and audit.

**Gate:** separate approval for each domain/capability; no autonomous wet-lab or clinical actions.

## P7 — Generalization and independent research evaluation

- [ ] Generalization beyond training/reference examples.
- [ ] Independent university review and reference replication.
- [ ] Reproducibility, scaling and recovery report.
- [ ] Formal domain contract freeze and limitations register.

**Gate:** acceptance only for claims supported by the stated evidence level.

## Required phase report

1. Exact files changed and commit SHA.
2. Tests added and executed.
3. CI URL and exact tested commit.
4. Pass/fail/skip/not-tested counts.
5. Benchmark and scientific evidence, kept separate.
6. Open risks and explicit non-claims.
7. Gate state: passed, failed or blocked.
8. Exact next phase (not started until gate passes).

University scientific/privacy review remains separate from engineering CI.


## Scientific foundation and tool ecosystem acceptance

- [ ] Scientific discipline map reviewed and A–N coverage gaps recorded.
- [ ] Existing package/tool inventory completed; exact versions, licenses and optional/external status verified.
- [ ] Tool registry entries are not represented as installed or validated without evidence.
- [ ] Typed quantities, dimensions, units and coordinate/reference conventions have positive and negative tests.
- [ ] Knowledge/evidence artifacts preserve source, license, assumptions, applicability, uncertainty, version and provenance.
- [ ] Symbolic and numerical computation adapters have reference, precision, convergence and failure tests.
- [ ] Statistical methods have reference datasets, assumptions, uncertainty and leakage-resistant evaluation.
- [ ] Every scientific construction passes a pre-generation audit and independent post-generation verification.
- [ ] Tool adapters declare schemas, version, dependencies, resource limits, egress, failure modes and verification strategy.
- [ ] Selected physics/chemistry/biology tools pass domain-specific boundary and reproducibility tests.
- [ ] No optional dependency is silently required by the core runtime.
- [ ] Model training is blocked until permission, baseline, leakage, evaluation and rollback gates pass.

**Scientific foundation gate:** at least one reproducible end-to-end knowledge-to-computation-to-verification example passes in two distinct scientific domains, with provenance and limitations. This is an engineering gate; independent scientific review remains separate.
