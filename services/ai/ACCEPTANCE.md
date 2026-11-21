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

- [ ] Typed concepts/entities/relations and domain packages.
- [ ] Quantities, dimensions, units and reference systems.
- [ ] Equations/laws/mechanisms with variables, assumptions and applicability domains.
- [ ] Evidence class, provenance, uncertainty, versioning and conflicting-claim representation.
- [ ] Knowledge artifact schemas and query/reasoning interfaces.
- [ ] A–N domain knowledge boundary map.
- [ ] Deterministic fixtures and round-trip/type/unit/provenance tests.

**Gate:** executable reference implementation preserves scientific semantics and provenance. No claim of comprehensive knowledge.

## P2 — Shared reasoning and construction primitives

- [ ] Symbolic expressions, derivation traces and dimensional checks.
- [ ] Constraint/feasibility and optimization contracts.
- [ ] Candidate, objective, uncertainty and evaluation artifacts.
- [ ] Reconstruction/generalization/exploration task contracts.
- [ ] Proposer–Verifier separation and non-circular verification.
- [ ] Reproducible examples in at least two distinct service domains.
- [ ] Explicit accepted/rejected/indeterminate/failure behavior.

**Gate:** candidates are generated and independently evaluated with reproducible evidence.

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
