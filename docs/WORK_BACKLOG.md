# Molecularis Work Backlog

**Current position (2026-11-22):** Engineering implementation for services A–N is recorded complete. P1 Scientific Knowledge Engine reference implementation is merged and passes CI. The shared Core/MSDE platform remains a local reference implementation, not a fully accepted production platform. P0 platform safety, integration and recovery residuals remain open; P0 is still a prerequisite for progression into P2/P3/P4 and model training. University scientific/privacy review and formal service freezes remain separate gates.

The [Agentics Molecularis Master Plan](AGENTICS_MOLECULARIS_MASTER_PLAN.md) is the single authority for Agentics architecture and phases. This backlog records actionable work only. Mark an item complete only with a commit and the relevant verification evidence.

## P0 — Repository truth, platform safety and reliability

- [ ] SF0 repository/dependency audit: inventory actual code, A–N capabilities, package versions, licenses, data/model permissions, adapters and test coverage.
- [ ] Reconcile capability contracts and demonstrate real typed artifact handoff across representative services.
- [ ] Verify provenance continuity from source artifacts through multi-service workflows and final reports.
- [ ] Add deterministic replay, dependency invalidation, cancellation, timeout and failure-propagation evidence.
- [ ] Complete threat model, trust boundaries, privacy classification, secret handling and data-egress policy.
- [ ] Implement and test OS-level process isolation, resource enforcement and reliable termination before untrusted tools/models execute.
- [x] Implement verified catalog/object backup and restore with non-overwrite semantics and corruption checks; verified in [CI #44909367708](https://github.com/AssayFlux/Molecularis/actions/runs/44909367708) (core 758 passed/12 skipped; optional Chemistry 766/4, Genomics 759/11, Sequence 761/9 with 4 existing warnings).
- [ ] Add filesystem crash-boundary fault injection, restore drills, encryption/signing and a reviewed corruption-recovery matrix.
- [ ] Publish a reviewed platform acceptance report with exact supported and unsupported operating conditions.

**P0 gate:** repository truth is reconciled; representative cross-service workflows preserve typed meaning and provenance; security, isolation, recovery and failure behavior have reproducible evidence or explicitly accepted blockers. Do not start P1 until this gate passes.

P1 was implemented on the owner's explicit request while these P0 tasks remain open. This does not waive the P0 gate: no P2/P3/P4 progression or model training until the P0 blockers are resolved or formally accepted.\n\nSee [P0 Platform Trust, Safety and Reliability Audit](P0_PLATFORM_AUDIT.md) for the evidence-backed baseline, threat model, data classifications, dependency inventory and exact P0 residual gates.

## P1 — Universal Scientific Knowledge Engine

- [x] Define typed concepts, entities, relations and domain knowledge packages.
- [x] Represent quantities, dimensions, units, coordinate/reference systems and conversions.
- [x] Represent equations/law records with typed variables, assumptions, applicability domains and source links; expressions remain inert data.
- [x] Preserve evidence class, source/version, provenance, uncertainty, explicit contradictory claims and immutable package history.
- [x] Add versioned knowledge schemas, deterministic query interfaces, Core ArtifactStore persistence/lineage and type/unit/provenance round-trip tests.
- [x] Define A–N knowledge ownership boundaries.

**P1 engineering gate:** passed by CI #45045807328 on tested commit `25b3e47f0eab45a9ac70defe96090e34b1ebfde5` (769 passed, 12 skipped, 0 failed; 66 JSON schemas validated). This is a domain-neutral reference substrate, not comprehensive scientific knowledge or independent scientific validation. P0 remains open, so P1 completion does not authorize progression to model training.

## P2 — Shared reasoning and construction primitives

- [ ] Add symbolic expressions, derivation traces and dimensional checks.
- [ ] Add numerical calculation, solver diagnostics, precision and convergence reporting.
- [ ] Add probability, statistics, uncertainty propagation, sensitivity and calibration.
- [ ] Add constraint/feasibility checks, optimization objectives and bounded search.
- [ ] Define reconstruction, generalization and exploration task/candidate contracts.
- [ ] Separate proposer and verifier implementations; add non-circular independent checks.
- [ ] Demonstrate reproducible construction and verification in at least two distinct scientific domains.

**P2 gate:** candidate artifacts are generated under explicit assumptions and independently evaluated with reproducible evidence.

## P3 — A–N knowledge-to-construction integration

- [ ] Map each A–N service to shared contracts while preserving domain-owned engines, laws, algorithms and Rulebooks.
- [ ] Add service-specific construction, evaluation and verification methods only where scientifically justified.
- [ ] Add known, edge, negative, constructed and out-of-domain fixtures.
- [ ] Demonstrate typed cross-service handoffs and continuous provenance.
- [ ] Label observations, established facts, derivations, inferences, predictions, simulations, constructions, hypotheses and validations distinctly.

**P3 gate:** every service demonstrates the lifecycle stages it claims to support; cross-domain workflows preserve scientific meaning and lineage.

## P4 — Agentics orchestration maturity

- [ ] Add a deployment-configured, provider-neutral model adapter and secure credential handling.
- [ ] Derive constrained tool calls from registered capability schemas.
- [ ] Bind approval to exact plan, inputs, knowledge/tool versions, egress and resource envelope.
- [ ] Add an artifact-grounded answer composer with claim-to-evidence mapping.
- [ ] Add at least 50 grounded/adversarial evaluations, including prompt injection, fabricated laws, unit errors and out-of-domain requests.
- [ ] Add bounded iteration, cancellation, traces and policy enforcement.

**P4 gate:** curated evaluations meet documented thresholds and unsupported scientific claims are rejected.

## P5 — Optional scientific models and training

- [ ] Demonstrate a measured need and baseline before model selection or training.
- [ ] Obtain explicit permission and verify data, code and checkpoint licenses.
- [ ] Add deduplication, leakage-resistant splits, reproducible training manifests and model registry.
- [ ] Separate retrieval/index updates, curated knowledge updates, Rulebook/algorithm changes and model-weight training.
- [ ] Add benchmark, calibration, regression and rollback evidence.

**P5 gate:** any model update is lawful, reproducible, benchmarked, calibrated and reversible. Organization data is not automatically training-authorized.

## P6 — Controlled discovery and design

- [ ] Define domain-specific risk and safety policies.
- [ ] Bound candidate generation, objectives, search budgets and stop conditions.
- [ ] Require independent verification, adversarial screening and qualified human/institutional review.
- [ ] Keep high-risk capabilities disabled by default until separately approved.

**P6 gate:** each discovery/design capability receives its own explicit safety and institutional authorization.

## P7 — Generalization and independent research evaluation

- [ ] Evaluate beyond training and reference examples.
- [ ] Obtain independent university review and reference replication.
- [ ] Publish reproducibility, scaling, recovery and limitations reports.
- [ ] Freeze only the service/domain contracts supported by the evidence.

**P7 gate:** accept only the scientific claims justified by independent evidence.

## Completed engineering record — A–N

The current service-by-service implementation state and CI references are maintained in [SERVICE_STATUS.md](SERVICE_STATUS.md). The following is the engineering sequence, not a claim of independent scientific acceptance:

- [x] A — Molecular
- [x] B — Sequence
- [x] C — Structure
- [x] D — Chemistry
- [x] E — Protein
- [x] F — Genomics
- [x] G — DNA/RNA
- [x] H — Simulation
- [x] I — Kinetics
- [x] J — Omics
- [x] K — Phylogeny
- [x] L — Pharmacogenomics
- [x] M — Cohorts
- [x] N — Workflows

**Not implied by these checkmarks:** university scientific/privacy approval, formal contract freeze, full cross-service scientific handoff, distributed production readiness, OS isolation or complete platform recovery certification.

## Existing Agentics implementation

- [x] Model-agnostic planner callable contract and active A–N capability catalog.
- [x] Strict Workflow v1 parsing/validation and bounded operation count.
- [x] Artifact integrity checks and persisted plan artifact with input lineage.
- [x] Explicit approval gate and execution through the Core Rulebook runtime.
- [x] Fresh-runtime A–N bootstrap.
- [x] Initial implementation CI: [run #44901363429](https://github.com/AssayFlux/Molecularis/actions/runs/44901363429), commit `2b6eced852fb049a81f6b087bb94e5e946047750`.

The Scientific Knowledge Engine, general construction system, independent proposer/verifier framework, configured production provider, training pipeline and full cross-service scientific orchestration are not yet implemented/accepted.

## Reporting rule

Every completed task must record exact files, commit SHA, tests and CI run, pass/fail/skip counts, benchmark or scientific evidence, open risks and the next gate. Engineering CI, model evaluation and scientific/experimental validation must be reported separately.