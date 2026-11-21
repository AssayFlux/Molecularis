# Molecularis Work Backlog
Mark an item complete only with a commit SHA and verification evidence. Services A, B and C are authorized; the Core/MSDE platform acceptance gate remains open and must not be reported as passed.
## P0 — Trustworthy baseline
- [x] Baseline CI repaired. Evidence: run #127.
- [x] Implement local MSDE reference slice. Evidence: commits 5b39b44 and ccae6c1; run #130.
- [x] Add optional scientific dependency profiles for sequence, genomics and chemistry. Evidence: all three profile jobs passed in run #133.
- [x] Repair malformed legacy JSON schema and pass repository-wide JSON Schema validation. Evidence: run #135.
- [ ] Audit Python modules, public imports, tests and service ownership.
- [ ] Audit dependencies, licenses, data provenance, model/runtime assumptions and security.
- [ ] Expand Ruff beyond E9/F; introduce targeted strict typing.
- [ ] Establish reproducibility, scientific reference and performance baselines.
## P1 — Core/MSDE platform
- [x] Typed platform budgets, capability and execution-context contracts.
- [x] Local service lifecycle and JSON capability manifest loader.
- [x] SHA-256 immutable blob store, SQLite catalog, lineage and atomic publication.
- [x] Bounded streaming, digest verification and non-destructive integrity audit.
- [x] Exact scalar and numeric range metadata lookup.
- [x] Capability registry and acyclic Rulebook DAG execution.
- [x] Successful and failed Rulebook run evidence.
- [x] Input artifact lineage on derived operation outputs.
- [x] Snapshot-bound exact/range query pagination with explicit completeness.
- [x] CI jobs for optional scientific dependency profiles.
- [ ] Native sorted-segment index manager, manifest snapshots and compaction, or a benchmark-backed formal decision to retain SQLite indexes.
- [ ] Crash-boundary fault injection, catalog backup/restore and corruption-recovery matrix.
- [ ] Typed query plan, deterministic cost model and bounded scan fallback.
- [ ] Preconditions/postconditions, typed Rulebook input/output validation, retry policies and independent-validator gates.
- [ ] Cross-process service discovery and language-neutral request/response runtime.
- [ ] C++/Python/Rust conformance suite and executable cross-language reference service.
- [ ] Threat model, sandboxing and operational resource-isolation controls.
## P2 — Scientific service sequence
Execute exactly one letter at a time, following [SERVICE_ROADMAP.md](SERVICE_ROADMAP.md).
- [ ] A — Molecular (v1 engineering implementation complete; run #150 green with 608 passed/12 skipped and 1k/10k benchmark smoke; independent scientific approval and formal freeze pending)
- [x] B — Sequence (Python v1 engineering implementation complete; independent scientific review and freeze pending)
- [x] C — Structure (Python v1 engineering implementation complete; university review deferred until A–N completion)
- [x] D — Chemistry (native graph v1, MSDE artifacts, five capabilities and CHM-001–CHM-006; scientific review deferred)
- [x] E — Protein (canonical sequence artifacts, four MSDE capabilities, PRO-001–PRO-006; scientific review deferred)
- [x] F — Genomics (canonical genome artifacts, five MSDE capabilities, GEN-001–GEN-007; CI verification pending)
- [x] G — DNA/RNA (canonical DNA/RNA artifacts, eight MSDE capabilities, DRNA-001–DRNA-007, transcription/reverse-transcription, explicit translation, primer screen and bounded Nussinov RNA fold; CI pending, scientific review deferred)
- [x] G — DNA/RNA CI verification (run #44892707015: core 679 passed/12 skipped; optional Sequence 682/9, Chemistry 687/4, Genomics 680/11; registry, schemas, Ruff E9/F, compilation and benchmarks green)
- [x] H — Simulation (canonical NVT/NPT protocol, MSDE lifecycle, energy-series analysis, hash-pinned GROMACS integration, OpenMM direct API, SIM-001–SIM-007; CI pending, scientific review deferred)
- [x] H — Simulation CI verification (run #44893264385: core 696 passed/12 skipped; optional Chemistry 704/4, Genomics 697/11, Sequence 699/9; registry, schemas, Ruff E9/F, compilation and benchmarks green)
- [x] I — Kinetics implementation and CI verification (canonical reaction-network artifact, bounded mass-action RK4, four capabilities, KIN-001–KIN-006, schemas, tests and benchmark; run #44894304968 green: core 702/12 skipped, Chemistry 710/4, Genomics 703/11, Sequence 705/9)
- [x] J — Omics (canonical matrix artifacts, seven MSDE operations, OMI-001–OMI-009, schemas, tests and benchmark; CI run #44895300775 green: core 711/12 skipped, Genomics 712/11, Sequence 714/9, Chemistry 719/4)
- [x] K — Phylogeny implementation (canonical aligned nucleotide artifacts, JC69 pairwise distances, NJ, UPGMA, seeded bootstrap, five MSDE capabilities, PHY-001–PHY-007, schemas, tests and benchmark; CI verification pending, scientific review deferred)
- [x] K — Phylogeny CI verification (run #44896994652: core 721 passed/12 skipped; Sequence 724/9, Genomics 722/11, Chemistry 729/4; registry, 55 schemas, Ruff E9/F, compilation and phylogeny benchmark green)
- [x] L — Pharmacogenomics implementation and CI verification (canonical synthetic non-patient sample and source-pinned definition artifacts, phased star-allele matching, two MSDE capabilities, PGX-001–PGX-007, schemas, tests and benchmark; run #44898692562 green: core 728/12 skipped, Genomics 729/11, Chemistry 736/4, Sequence 731/9; scientific/clinical review deferred)
- [x] M — Cohorts implementation and CI verification (canonical synthetic non-patient artifacts, four MSDE capabilities, COH-001–COH-008, schemas, tests and benchmark; run #44899270453 green: core 737/12 skipped, Chemistry 745/4, Sequence 740/9, Genomics 738/11)
- [x] N — Workflows implementation and CI verification (canonical WorkflowDocument, bounded DAG validation/planning, MSDE artifact lifecycle, Core RulebookExecutor execution, two capabilities, WF-001–WF-009, schemas, tests and benchmark; run #44900460557 green: core 746/12 skipped, Chemistry 754/4, Genomics 747/11, Sequence 749/9)
Each letter requires discovery/audit, Engine, Runtime, Rulebook, schemas/contracts, implementation, integration, mandatory tests, independent scientific evidence, documentation, acceptance and freeze.
## P3 — System integration and release
- [ ] Cross-service workflows and provenance continuity.
- [ ] Deterministic replay, dependency invalidation and failure recovery.
- [ ] Security, resource limits, backup/restore and supply-chain governance.
- [ ] System-scale performance and scientific acceptance report.
- [ ] Complete resolved release SBOM and license evidence.
- [ ] Device/deployment assessment based on measured requirements.
## Active task
A's engineering implementation is complete; independent scientific approval and freeze remain pending. B's Python v1 engineering implementation is complete. C's Python v1 engineering implementation is complete and CI-verified in run #159. D's Chemistry Python v1 engineering implementation is complete and CI-verified in run #44888785327 (core 644 passed/12 skipped; optional chemistry 652 passed/4 skipped; sequence 647 passed/9 skipped; genomics 645 passed/11 skipped). E Protein Python v1 implementation is complete and CI-verified in run #44889593877 (core 651 passed/12 skipped; optional sequence 654 passed/9 skipped; genomics 652 passed/11 skipped; chemistry 659 passed/4 skipped). Per owner direction, university scientific review and contract freezes for A–N are deferred until the entire engineering build is complete. F Genomics CI evidence was recorded in the latest status commit. G DNA/RNA engineering implementation and CI verification complete in run #44892707015 (core 679 passed/12 skipped; optional Sequence 682/9, Chemistry 687/4, Genomics 680/11). University scientific review and formal contract freeze remain deferred until A–N engineering completion. H Simulation engineering implementation and CI verification complete in run #44893264385 (core 696 passed/12 skipped; optional Chemistry 704/4, Genomics 697/11, Sequence 699/9). University scientific review and formal contract freeze remain deferred until A–N engineering completion. I — Kinetics engineering implementation and CI verification complete in run #44894304968 (core 702 passed/12 skipped; optional Chemistry 710/4, Genomics 703/11, Sequence 705/9). University scientific review and formal freeze remain deferred until A–N engineering completion. J — Omics engineering implementation and CI verification complete in run #44895300775 (core 711 passed/12 skipped; Genomics 712/11, Sequence 714/9, Chemistry 719/4). K — Phylogeny engineering implementation and CI verification complete in run #44896994652 (core 721/12 skipped; Sequence 724/9, Genomics 722/11, Chemistry 729/4). University scientific review and formal freeze remain deferred until A–N engineering completion. M — Cohorts engineering implementation and CI verification complete in run #44899270453 (core 737/12 skipped; Chemistry 745/4, Sequence 740/9, Genomics 738/11). N — Workflows native DAG orchestration engineering and CI verification complete in run #44900460557 (core 746/12 skipped; Chemistry 754/4, Genomics 747/11, Sequence 749/9). All A–N service engineering is complete. University scientific/privacy review and formal contract freeze remain deferred; proceed to platform-wide integration and acceptance.

## P4 — Agentics Molecularis intelligence system
The detailed scope, architecture, acceptance metrics and gates are governed by [AGENTICS_MOLECULARIS_MASTER_PLAN.md](AGENTICS_MOLECULARIS_MASTER_PLAN.md). Do not mark phase work complete without commit and CI/benchmark evidence.

### Existing implementation
- [x] Model-agnostic planner callable contract, active A–N capability catalog, strict Workflow v1 validation, persisted plan artifact with input lineage, explicit approval gate and execution through Core Rulebook runtime.
- [x] A–N fresh-runtime bootstrap.
- [x] CI verification of the initial AI implementation: [run #44901363429](https://github.com/AssayFlux/Molecularis/actions/runs/44901363429), commit `2b6eced852fb049a81f6b087bb94e5e946047750`.
- [ ] Real cross-service scientific artifact handoff and provenance continuity.

### Agentics phases — sequential gates
- [ ] **P0 — Hygiene and platform safety:** reconcile docs/status; threat model; OS-level sandbox; resource/network isolation; cancellation/timeout; failed-run evidence; artifact-store backup/restore and crash/corruption tests.
- [ ] **P1 — Sources service:** audit/reuse existing adapters; RCSB PDB, UniProt, AlphaFold DB, InterPro, PubChem and NCBI Entrez; offline cache, rate limits, retries, checksums, license ledger and ambiguity-aware resolver.
- [ ] **P2 — Orchestrator:** deployment-configured provider adapter and secure secrets; schema-derived tools; intent/clarification; approval bound to plan/input hashes; artifact-only answer composer; 50+ grounded/adversarial evals.
- [ ] **P3 — Predictor:** separate PredictorAdapter service; exact model/checkpoint/license review; mmCIF and confidence artifacts; predicted namespace; local MSA; verification Rulebooks; post-cutoff leakage-aware benchmark.
- [ ] **P4 — Data/training:** versioned snapshots, checksums, license ledger, quality filters, sequence clustering, temporal/cluster splits, reproducible PyTorch harness and model registry.
- [ ] **P5 — Optional design:** disabled by default; proposer/verifier loop, biosecurity screening, human review and institutional approval.
- [ ] **P6 — Generalize:** service-specific Proposer → Verifier patterns, domain acceptance criteria, independent checks and end-to-end artifact lineage.

**Gate rule:** implement one phase only, add tests, obtain green CI and update docs from evidence, then stop and report. University scientific review remains independent and is not replaced by software CI.


## Agentics Molecularis — revised universal roadmap (2026-11-21)

The detailed governing plan is now v2.0: [AGENTICS_MOLECULARIS_MASTER_PLAN.md](AGENTICS_MOLECULARIS_MASTER_PLAN.md). This section supersedes the earlier narrow P0–P6 ordering where inconsistent.

- [ ] P0 — Repository truth, sandbox/security, failure evidence and artifact recovery.
- [ ] P1 — Universal Scientific Knowledge Engine: typed knowledge, laws/equations, units, assumptions, evidence, uncertainty, applicability and versioning.
- [ ] P2 — Shared reasoning/construction primitives: symbolic derivation, dimensional checks, constraints, optimization, candidate/evaluation contracts and independent Proposer–Verifier.
- [ ] P3 — Integrate knowledge-to-construction into all A–N services, one service/domain slice at a time; preserve existing engines and domain Rulebooks.
- [ ] P4 — Mature Agentics orchestration, optional provider adapter, approval binding, artifact-grounded reporting and 50+ adversarial evaluations.
- [ ] P5 — Optional scientific models/training only after measured baseline gap, exact license review and leakage-resistant evaluation. Predictors are optional, never the architecture centre.
- [ ] P6 — Controlled discovery/design with domain safety, independent verification and human/institutional gates.
- [ ] P7 — Generalization, scaling and independent university/research evaluation.

**Permanent service rule:** Understand → Represent → Reason → Construct → Evaluate → Verify → Learn applies to every service A–N. Engineering CI and scientific acceptance remain separate. No phase may be marked complete without commit and evidence.


## Agentics scientific foundation and tool ecosystem

- [ ] Publish and maintain the AI Constitution and enforce its rules in schemas, runtime policy and tests.
- [ ] Audit existing scientific dependencies, tools, adapters and A–N capability coverage before adding packages.
- [ ] Define shared scientific types: quantities, dimensions, units, coordinate/reference systems and evidence classes.
- [ ] Build the versioned Scientific Knowledge Engine and evidence/provenance contracts.
- [ ] Integrate symbolic/numerical mathematics, statistics, uncertainty and optimization through adapters.
- [ ] Add graph, geometry and topology primitives required by domain construction.
- [ ] Select physics, chemistry, biology and simulation tools based on service gaps and validated use cases.
- [ ] Enforce pre-generation audit and independent post-generation verification for scientific outputs.
- [ ] Build permission-aware knowledge acquisition, dataset manifests and model governance.
- [ ] Keep optional tools isolated; document exact versions, licenses, resource requirements and limitations.

Governing detail: [Agentics Master Plan](AGENTICS_MOLECULARIS_MASTER_PLAN.md) · [AI Constitution](../services/ai/AI_CONSTITUTION.md) · [Scientific Foundation](../services/ai/SCIENTIFIC_FOUNDATION.md) · [Tool Registry](../services/ai/SCIENTIFIC_TOOL_REGISTRY.md) · [Implementation Roadmap](../services/ai/IMPLEMENTATION_ROADMAP.md).
