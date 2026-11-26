# Molecularis Work Backlog

**Current position (2026-11-26):** Engineering implementation for services A–N and the P1–P3 reference implementations is recorded complete on their respective tested commits. SF0 repository/dependency inventory is complete for audited HEAD `e36e32705045ab6311d20713d8f2a47b8c5af715`; see [SF0 Repository Truth Audit](SF0_REPOSITORY_TRUTH_AUDIT.md). The shared Core/MSDE platform remains a local reference implementation, not a fully accepted production platform. P0 security, integration, exact-HEAD CI, dependency/license and recovery residuals remain open. P0 acceptance and university scientific/privacy review remain prerequisites for production use, restricted-data processing and model training.

The [Agentics Molecularis Master Plan](AGENTICS_MOLECULARIS_MASTER_PLAN.md) is the single authority for Agentics architecture and phases. This backlog records actionable work only. Mark an item complete only with a commit and the relevant verification evidence.

## P0 — Repository truth, platform safety and reliability

- [x] SF0 repository/dependency audit: tracked-tree inventory, canonical Python package and compatibility namespace, A–N service/capability declarations, package/version declarations, license/data/model governance, adapters, schemas, tests and CI configuration inventoried in [SF0 Repository Truth Audit](SF0_REPOSITORY_TRUTH_AUDIT.md). Remaining exact-HEAD CI, measured coverage, per-dependency legal/security review and source-specific data/model permission verification are explicitly retained as P0 follow-up gates.
- [ ] Reconcile capability contracts and demonstrate real typed artifact handoff across representative services.
- [ ] Verify provenance continuity from source artifacts through multi-service workflows and final reports.
- [ ] Add deterministic replay, dependency invalidation, cancellation, timeout and failure-propagation evidence.
- [ ] Complete threat model, trust boundaries, privacy classification, secret handling and enforceable data-egress policy with institutional review. The 2026-11-26 deny-by-default policy primitive is implemented, but adapter and network-boundary enforcement remains open.
- [x] Add an opt-in OCI runner for digest-pinned tools with network disabled, read-only root, dropped capabilities, no-new-privileges, non-root execution, bounded CPU/memory/PIDs/tmpfs/time and explicit mounts.
- [ ] Integrate the OCI runner into approved capability execution; test against a real rootless runtime, enforce output disk quotas and verify process-tree termination.
- [x] Replace Boolean AI approval with canonical approval payload bound to principal, nonce, plan/workflow hash, input artifacts, capability catalog, execution policy and resource budget.
- [ ] Integrate institutional identity/signature verification and atomic one-use approval consumption.
- [x] Implement verified catalog/object backup and restore with non-overwrite semantics and corruption checks; verified in [CI #44909367708](https://github.com/AssayFlux/Molecularis/actions/runs/44909367708) (core 758 passed/12 skipped; optional Chemistry 766/4, Genomics 759/11, Sequence 761/9 with 4 existing warnings).
- [ ] Add filesystem crash-boundary fault injection, restore drills, encryption/signing and a reviewed corruption-recovery matrix.
- [x] Generate SPDX 2.3 inventory of installed Python distributions and observed dependency edges as a CI artifact.\n- [x] Add CI known-vulnerability scanning for resolved Python environments using pip-audit across core and optional scientific profiles; exact-HEAD run [#45846604545](https://github.com/AssayFlux/Molecularis/actions/runs/45846604545) passed with no known Python dependency vulnerabilities.\n- [x] Extend SPDX inventory to installed Python distributions and dpkg/rpm native package metadata where available; exact-HEAD CI uploaded the SPDX 2.3 artifact in [run #45846604545](https://github.com/AssayFlux/Molecularis/actions/runs/45846604545).\n- [ ] Add publisher attestations, verified package/binary hashes, OS/native vulnerability scanning and reviewed license report.\n- [x] Add fail-closed data-classification and exact-scope egress authorization primitives with regression tests.\n- [ ] Wire the egress policy into every external adapter and enforce destination controls at the network boundary.\n- [ ] Publish a reviewed platform acceptance report with exact supported and unsupported operating conditions.

**P0 gate:** repository truth is reconciled; representative cross-service workflows preserve typed meaning and provenance; security, isolation, recovery and failure behavior have reproducible evidence or explicitly accepted blockers. Do not start P1 until this gate passes.

P1, P2 and the P3 A–N integration implementation were delivered on the owner's explicit requests while P0 tasks remain open. This records engineering implementation only and does not waive the P0 gate. P4 orchestration expansion, model training, production deployment and restricted-data processing remain blocked until the applicable P0 controls are integrated, tested and formally accepted by the institution.\n\nSee [P0 Platform Trust, Safety and Reliability Audit](P0_PLATFORM_AUDIT.md) for the evidence-backed baseline, threat model, data classifications, dependency inventory and exact P0 residual gates. The 2026-11-26 hardening delivery adds a deny-by-default egress policy primitive, Python dependency vulnerability scanning in CI and a broader SPDX environment inventory; it does not pass the external P0 gates.

## P1 — Universal Scientific Knowledge Engine

- [x] Define typed concepts, entities, relations and domain knowledge packages.
- [x] Represent quantities, dimensions, units, coordinate/reference systems and conversions.
- [x] Represent equations/laws with typed variables and mechanisms with ordered typed steps, assumptions, applicability domains and source/evidence links; expressions remain inert data.
- [x] Preserve evidence class, source/version, provenance, uncertainty, explicit contradictory claims and immutable package history.
- [x] Add versioned knowledge schemas, deterministic query interfaces, Core ArtifactStore persistence/lineage and type/unit/provenance round-trip tests, including quantity serialization and Core artifact round-trip.
- [x] Define A–N knowledge ownership boundaries.

**P1 engineering gate:** passed by CI #45046306359 on tested commit `819eb1fff6785fa49530ab5bf8b30e5280111712` (769 passed, 12 skipped, 0 failed; 66 JSON schemas validated). This is a domain-neutral reference substrate, not comprehensive scientific knowledge or independent scientific validation. P0 remains open, so P1 completion does not authorize progression to model training.

## P2 — Shared reasoning and construction primitives

- [x] Add a restricted symbolic arithmetic AST, deterministic expression evaluation, variable discovery, derivation traces and dimensional inference using P1 dimensions.
- [x] Add bounded numerical root solving, dense linear-system solving with partial pivoting, and composite Simpson integration with error estimates and convergence diagnostics.
- [x] Add descriptive statistics, Pearson correlation, Welch hypothesis tests, OLS regression with confidence intervals, Benjamini–Hochberg FDR correction, explicit-prior Beta–Binomial Bayesian posterior, deterministic bootstrap intervals, first-order uncertainty propagation and seeded Monte Carlo.
- [x] Add local finite-difference sensitivity, binary probability calibration and two-group power/sample-size planning with explicit assumptions.
- [x] Add deterministic graph topology/path primitives, coordinate-frame/unit-safe 3D vector geometry, hard/soft constraints, weighted bounded multi-objective grid search, and explicit infeasible/budget-exhausted states.
- [x] Define reconstruction/generalization/exploration tasks, bounded candidate contracts, pre-publication audit, independent verifier identity/method/check/evidence contract and versioned JSON Schema.
- [x] Reuse the existing ScientificCore proposer/verifier boundary; demonstrate separate proposer and verifier implementations for sequence and chemical-formula representation fixtures, with failed independent checks blocking publication.
- [x] Add positive, negative, boundary, determinism, unit/dimension, linear algebra, integration, graph, geometry, solver, inference, regression, FDR, power-analysis, uncertainty, optimization and independent-verification tests.

**P2 engineering gate: PASSED.** GitHub Actions [run #45049391363](https://github.com/AssayFlux/Molecularis/actions/runs/45049391363) on tested commit `4bf332e9b1161d111a047517e5a5212e9e51a2d9`: 804 passed, 12 skipped, 0 failed; 67 JSON schemas validated; Ruff error/F checks, benchmark smoke tests and Chemistry/Genomics/Sequence optional profiles passed. Two-domain fixtures validate contract separation and representation consistency only; they do not establish chemical validity, molecular stability or experimental realizability. P0 remains open and its platform acceptance gate is not waived.

**P2 gate:** engineering implementation and CI passed on the exact code commit above. P0 platform safety, integration and recovery gates remain open and are not waived.

## P3 — A–N knowledge-to-construction integration

- [x] Add a single-runtime bootstrap for all fourteen existing native domain services and their capability registrations.
- [x] Add a machine-readable A–N catalog: domain ownership, native Rulebook, accepted artifact schemas/media types, capability contracts, scope and non-claims.
- [x] Add immutable, assertion-free framework KnowledgePackages for A–N; factual content remains gated on source/license/permission review.
- [x] Add explicit, caller-owned typed handoffs with target schema/media validation, transformation/version, assumptions, evidence class, passed-verification record and source/verifier/evidence artifact lineage.
- [x] Add positive sequence→protein and DNA/RNA→sequence handoff tests; reject failed verification, unknown schemas and duplicate bootstrap.
- [x] Add a synthetic contract-only test matrix for all 182 ordered A–N handoff pairs.
- [x] Preserve existing domain-specific algorithms, schemas, Rulebooks, service tests and scientific limitations.
- [ ] Populate domain knowledge packages with reviewed, source-attributed facts, equations and mechanisms.
- [ ] Obtain independent scientific review/reference replication for cross-domain conversions.
- [ ] Add domain-semantic adapters and independently reviewed reference fixtures for every cross-domain pair required by approved research workflows. The 182-pair synthetic matrix covers transport/provenance only.

**P3 engineering gate: PASSED.** GitHub Actions [run #45088241792](https://github.com/AssayFlux/Molecularis/actions/runs/45088241792) on exact tested commit `2c9ae812ec7ecf213ca8fbc4303132e5e34b43a3`: core 817 passed/12 skipped; Genomics 818/11; Chemistry 825/4; Sequence 820/9 (4 existing warnings); 69 JSON schemas validated; SPDX 2.3 inventory generated for 43 installed Python distributions; Ruff, compilation and benchmark smoke steps passed. The 182-pair synthetic matrix establishes transport/provenance contracts only, not scientific semantic conversion. Source-backed knowledge population and independent scientific acceptance remain open.


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