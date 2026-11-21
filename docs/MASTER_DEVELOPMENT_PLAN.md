# Molecularis Master Development Plan

Version: 2.0. Status: governing, living plan; material changes require a decision-log entry.

## Mission and delivery strategy

Follow [NORTH_STAR.md](NORTH_STAR.md). Build the shared platform first, then complete the A–N scientific services strictly one at a time. Each service is a complete vertical slice: discovery, specification, native engine, runtime, Rulebook, contracts, data, validation, tests, integration, documentation, acceptance and freeze.

## Phase 0 — Repository trust baseline

- Verify CORE head and preserve assets, history and useful existing code.
- Inventory implementations, public imports, tests, schemas, datasets, licenses, dependencies and CI.
- Establish a truthful status register and reproducible baseline.
- Audit legacy Python modules before moving or replacing them.

Exit: repository inventory, baseline and migration risks are documented.

## Phase 1 — Shared Core and MSDE platform gate

- Stable service identity/discovery and versioned request/response/error envelopes.
- Artifact identity, canonical schemas, units, provenance, run identity and capability registry.
- MSDE immutable content-addressed artifact store, catalog, journal/recovery and bounded streaming.
- Exact-key and ordered/range indexes first; other index families justified by workloads and benchmarks.
- Query execution with snapshot, budgets, pagination and explicit completeness/approximation.
- Evidence ledger and generic Rulebook DAG execution gates.
- C++/Python/Rust contract interoperability and reference service.
- Security/threat model, schema evolution and failure-recovery tests.

Exit: an executable reference service can discover, ingest, query, transform, validate and publish immutable artifacts with provenance under declared budgets. Architecture documents alone do not satisfy this gate.

## Phase 2 — Scientific services A–N

Follow [SERVICE_ROADMAP.md](SERVICE_ROADMAP.md) without parallel implementation:

A Molecular → B Sequence → C Structure → D Chemistry → E Protein → F Genomics → G DNA/RNA → H Simulation → I Kinetics → J Omics → K Phylogeny → L Pharmacogenomics → M Cohorts → N Workflows.

Each service must pass every mandatory service acceptance gate and be frozen before the next step starts. A step may reuse existing implementation after audit and migration; it does not require needless rewrites.

## Phase 3 — Cross-service integration

- Versioned artifact handoff and provenance continuity.
- Workflow DAGs, deterministic replay and bounded retry/recovery.
- Dependency invalidation when upstream artifacts or rules change.
- End-to-end scientific fixtures spanning multiple accepted services.

Exit: representative cross-domain workflows are reproducible and independently validated.

## Phase 4 — System hardening and scale

Security, isolation, resource accounting, numerical stability, dependency/supply-chain governance, backup/restore, diagnostics, performance and memory regression, failure injection and release evidence.

Exit: system-level acceptance report with explicit supported workload envelope and known limitations.

## Phase 5 — Deployment and device decisions

Only after Phase 4, measure CPU, memory, GPU, storage, operating systems, accelerators, network and concurrency needs. Publish supported profiles from measured evidence.

## Work-in-progress and change limits

- One active scientific service at a time.
- Shared-Core work only when it unblocks the platform or active service.
- Every task has scope, exact paths, acceptance criteria, dependencies and verification plan.
- Do not delete or migrate legacy code without usage/import/test audit and compatibility plan.
- No feature branches or PRs; work directly on CORE with non-force, expected-head updates.
- Preserve Assets and root README; README is updated as project state changes.
- Record architectural, order, dependency and breaking-contract decisions.

## Completion and freeze rule

A service is complete only when Engine, Runtime, Rulebook, contracts, tests, scientific evidence, integration, operational documentation and freeze record are accepted. Generic CI success is necessary but not sufficient. Frozen changes require explicit authorization or the narrowly controlled critical-remediation process.


## Agentics Molecularis intelligence and scientific foundation track

The A–N service engineering sequence and their present evidence states are recorded in [SERVICE_STATUS.md](SERVICE_STATUS.md). Service engineering completion is not the same as independent scientific acceptance. The next intelligence-layer programme is governed by the single [Agentics Molecularis Master Plan](AGENTICS_MOLECULARIS_MASTER_PLAN.md); there is no separate competing AI roadmap.

The existing planner, Workflow v1, Core/MSDE and A–N bootstrap are preserved. The scientific foundation documents define target capabilities and tool candidates; they do not claim that the Scientific Knowledge Engine, shared scientific solvers, full construction/verifier system or model training pipeline is implemented.

The governing sequence is:
- **P0 — Repository truth, safety and reliability:** reconcile current implementation, close critical safety/recovery/provenance gaps and establish enforceable controls.
- **P1 — Universal scientific knowledge architecture:** typed knowledge, laws/equations, evidence, assumptions, applicability and provenance.
- **P2 — Shared reasoning and construction primitives:** units/dimensional analysis, symbolic/numerical methods, statistics/uncertainty, constraints, optimization, candidate/evaluation contracts and independent verification.
- **P3 — A–N knowledge-to-construction integration:** connect shared capabilities to domain-owned engines and Rulebooks without generic duplicate service wrappers.
- **P4 — Agentics orchestration maturity:** provider-neutral planning, registered tools, approval binding, artifact-grounded reporting and adversarial evaluation.
- **P5 — Optional scientific models and training:** only after measured need, permission-cleared data, leakage-resistant evaluation, reproducible manifests and rollback.
- **P6 — Controlled discovery and design:** domain safety review, independent verification and human/institutional authorization.
- **P7 — Generalization, scaling and research evaluation:** independent replication, reproducibility, operating-envelope and university review.

No later phase begins until its predecessor's gate is evidenced. Engineering CI, model benchmarks and scientific/experimental acceptance are reported separately. The detailed scientific disciplines, tool candidates and implementation sequence are in services/ai/SCIENTIFIC_FOUNDATION.md, services/ai/SCIENTIFIC_TOOL_REGISTRY.md and services/ai/IMPLEMENTATION_ROADMAP.md.


## Agentics Molecularis — universal scientific construction direction (2026-11-21)

This direction supersedes narrower descriptions of Agentics phases where they conflict with the current governing [Master Plan v2.0](AGENTICS_MOLECULARIS_MASTER_PLAN.md).

**Permanent rule for every service A–N:** Understand → Represent → Reason → Construct → Evaluate → Verify → Learn. The principle applies equally to Molecular, Sequence, Structure, Chemistry, Protein, Genomics, DNA/RNA, Simulation, Kinetics, Omics, Phylogeny, Pharmacogenomics, Cohorts and Workflows.

The shared target is a Scientific Knowledge Engine plus typed reasoning, construction, evaluation and independent verification contracts. Domain services retain their own scientific knowledge, laws, equations, constraints, algorithms, Rulebooks and evidence thresholds. This is not a mandate to rewrite existing services or create fourteen generic AI wrappers.

External databases, PDB/X-ray observations, pretrained predictors and hosted models are optional evidence/method adapters. They must not define the boundary of construction or make Molecularis dependent on one data modality. Distinguish observed, established, derived, inferred, predicted, simulated, constructed, hypothesized and validated results. A mathematically valid or generated candidate is not automatically physically stable, experimentally realizable or functional.

**Roadmap authority:** P0 safety/reliability → P1 universal knowledge architecture → P2 shared reasoning/construction primitives → P3 A–N domain integration → P4 Agentics orchestration → P5 optional models/training → P6 controlled discovery/design → P7 independent generalization/research evaluation. Execute one phase at a time and require its gate before proceeding. Do not treat documentation as implementation evidence.
