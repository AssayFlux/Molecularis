# Agentics Molecularis — Universal Scientific Reasoning & Construction Master Plan

**Product:** Agentics Molecularis  
**Parent platform:** Molecularis by AssayFlux  
**Plan version:** 2.0 — Universal Knowledge-to-Construction Architecture  
**Status:** Governing architecture and sequential implementation plan  
**Branch:** CORE  
**Prepared:** 2026-11-21  
**Supersedes:** v1.0 where it conflicts with this plan; historical decisions remain in the decision log.

---

## 1. Executive direction

Agentics Molecularis is the agentic intelligence and scientific orchestration system of Molecularis. Its purpose is not merely to search scientific databases, retrieve known structures, call pretrained predictors or automate existing tools. Its long-term purpose is to help a researcher move from a scientific objective to a reasoned, reproducible and independently evaluated construction.

**Project-wide invariant:** every service A–N follows the same scientific approach:

**Understand → Represent → Reason → Construct → Evaluate → Verify → Learn.**

This principle is shared across all services. It is not a protein-only, molecular-X-ray-only, PDB-only or structure-prediction roadmap. Every domain keeps its own scientific semantics, engines, constraints, evidence standards and Rulebooks while participating in a shared platform.

### North Star

**Given a scientific objective, Molecularis should identify the relevant knowledge, determine the governing principles and constraints, reason about what is possible, construct candidate solutions, evaluate them through appropriate scientific methods, and distinguish established results from new hypotheses.**

The platform must grow from a system that processes known inputs into a system capable of deriving and constructing new possibilities from scientific knowledge. It must not claim that every generated candidate is correct, stable, realizable or experimentally confirmed.

## 2. Permanent project-wide principles

1. **Knowledge before pattern imitation.** Models and datasets are useful evidence and approximations, not substitutes for domain knowledge, mathematical structure or governing principles.
2. **First-principles where applicable.** Use equations, conservation laws, physical models, chemical rules, causal mechanisms, mathematical constraints and domain theory where appropriate. State assumptions and validity domains.
3. **Multiple complementary methods.** Combine symbolic reasoning, graph/geometry construction, numerical methods, optimization, simulation, statistical inference and machine learning when justified. No single method is mandatory for every task.
4. **Construct, do not only retrieve.** Retrieval supplies evidence, initial conditions, templates and comparisons. It must not define the boundary of what the platform can attempt to construct.
5. **Generalize beyond examples.** A service must be designed to handle supported classes of problems, not merely memorized fixtures or a fixed collection of reference structures.
6. **Independent verification.** A proposer must not be the sole judge of its own output. Verification uses domain-owned rules and independent checks appropriate to the claim.
7. **Epistemic honesty.** Distinguish observed, established, inferred, predicted, simulated, constructed and hypothesized results.
8. **Traceability.** Inputs, knowledge sources, assumptions, equations, software, models, parameters, seeds, intermediate artifacts and verification evidence remain traceable.
9. **Human authority.** Consequential, clinical, experimental, safety-sensitive or institutionally governed decisions remain with qualified humans.
10. **No fabricated science.** Missing evidence remains missing. Do not invent values, laws, citations, measurements, coordinates, confidence or validation outcomes.
11. **Service universality.** The same lifecycle and evidence principles apply to A–N, with domain-specific implementations rather than a generic one-size-fits-all scientific validator.
12. **Incremental engineering.** Reuse working repository foundations, implement one gated phase at a time, test engineering contracts and do not claim scientific acceptance before independent review.

## 3. Scientific epistemology and result classes

Every scientific artifact/report must declare its epistemic status. At minimum:

| Status | Meaning | What it does not mean |
|---|---|---|
| Observed | Directly recorded measurement or experimental observation with source and conditions | Automatically error-free or universally generalizable |
| Established | Supported by accepted theory/evidence within a stated domain | True outside its assumptions/domain |
| Derived | Obtained by explicit mathematical or logical derivation from stated premises | Experimentally observed |
| Inferred | Estimated from data/model under declared assumptions | Direct measurement |
| Predicted | Model-produced estimate with model/version/provenance | Confirmed fact |
| Simulated | Result of a specified computational model and conditions | Guaranteed physical realization |
| Constructed | A candidate generated under explicit representation and constraints | Stable, functional or experimentally realizable |
| Hypothesized | A novel or insufficiently tested scientific proposition/candidate | Validated discovery |
| Validated | Passed specified independent checks at a declared evidence level | Universally true or experimentally proven unless that is what was tested |

Do not collapse these statuses into a boolean success field. Use explicit states such as accepted, rejected, indeterminate, failed, needs_human_review, and not_applicable alongside the evidence class.

### Construction and truth are separate gates

For any constructed scientific candidate, report separately as applicable:

1. Representationally well-formed.
2. Mathematically consistent.
3. Domain-rule compliant (e.g. valence, topology, sequence grammar, conservation).
4. Physically plausible under a specified model and conditions.
5. Computationally stable under declared simulation/optimization conditions.
6. Experimentally realizable (requires appropriate experimental evidence).
7. Functionally demonstrated (requires domain-appropriate functional evidence).

Passing an earlier gate never implies passing a later one. “Novel” means not found in the searched/compared reference space under a declared protocol; it does not prove globally unprecedented discovery.

## 4. Universal scientific lifecycle

Every A–N service implements this lifecycle, adapted to its domain:

1. **Understand:** parse the objective, entities, target representation, constraints, desired outputs and uncertainty.
2. **Represent:** convert inputs into canonical typed domain representations with units, coordinate/reference conventions and identity.
3. **Acquire knowledge:** obtain relevant local and approved external evidence, theory, parameters, equations and reference data. Retrieval is optional when the task is self-contained.
4. **Reason:** identify governing laws, mechanisms, dependencies, assumptions, boundary conditions and applicability domains.
5. **Formulate:** choose a construction/analysis strategy and define objective functions, constraints, uncertainty and stop conditions.
6. **Construct or compute:** produce candidates/results through native engines, deterministic algorithms, simulation, optimization or approved model adapters.
7. **Evaluate:** score candidates against explicit objectives, feasibility constraints, robustness and resource limits.
8. **Verify independently:** apply domain Rulebooks, alternative methods, invariants, reference comparisons, sensitivity analysis or experimental evidence as appropriate.
9. **Classify:** label epistemic status, confidence/uncertainty, limitations and unresolved questions.
10. **Preserve and report:** publish immutable artifacts, provenance, lineage, methods, units and claim-level evidence.

Some tasks may skip a stage only with an explicit not-applicable reason. The system must not fabricate a knowledge source or simulation when none was needed or available.

## 5. Universal architecture

### 5.1 Layered system

| Layer | Responsibility |
|---|---|
| Research Interface | Natural-language, structured, file and programmatic objectives; constraints and approval |
| Agentics Orchestrator | Intent interpretation, decomposition, capability discovery, plan construction, coordination and report composition |
| Scientific Knowledge Engine (SKE) | Typed concepts, entities, properties, relations, laws, equations, mechanisms, constraints, evidence and applicability domains |
| Knowledge Representation & Reasoning | Graphs, symbolic expressions, dimensional analysis, causal/dependency relations, constraint systems and derivation traces |
| Construction Engine | Domain-appropriate candidate generation, graph/geometry/topology synthesis, numerical construction, search and optimization |
| Evaluation Engine | Objective functions, feasibility checks, uncertainty, sensitivity, robustness and candidate ranking |
| Simulation & Computation | Numerical solvers, physical/chemical models, statistical computation and optional external scientific engines |
| Verification Engine | Independent domain Rulebooks, invariants, alternative methods, reference tests and validation evidence |
| Domain Services A–N | Scientific semantics, native algorithms, data contracts, domain construction and verification |
| Core / MSDE | Capability registry, Rulebook DAG execution, budgets, immutable artifacts, catalog, provenance and lineage |
| Evidence & Report Ledger | Claim-to-artifact mapping, status, uncertainty, reproducibility and audit history |

This is a logical architecture, not a mandate to split every component into a separate process or service. Start with modular in-process components where safe and useful; introduce distributed boundaries only when justified by measured needs.

### 5.2 Agentics authority boundary

Agentics interprets goals, reasons about available operations, proposes workflows, coordinates approved work and explains evidence. It is not itself the authority for scientific laws, domain thresholds, experimental truth or clinical decisions.

LLMs are optional reasoning/planning/reporting components. They must not be the only mechanism that stores scientific knowledge, executes mathematical reasoning or verifies outputs. Deterministic domain engines and typed scientific artifacts remain first-class.

### 5.3 Scientific Knowledge Engine (SKE)

The SKE is a shared knowledge substrate, not merely a vector database or an LLM prompt corpus. It must support:

- Typed scientific entities, concepts, quantities, dimensions, units and coordinate/reference systems.
- Relations with direction, type, scope and evidence.
- Equations and symbolic expressions with variable definitions, units, assumptions and validity domains.
- Laws, mechanisms and empirical relationships with evidence class and known limitations.
- Constraints, boundary conditions, conservation rules and dependency graphs.
- Evidence records linking knowledge statements to publications, datasets, measurements, derivations or expert-curated sources.
- Versioning, temporal validity, conflicting claims, uncertainty and provenance.
- Domain-specific extensions without flattening distinct scientific meanings into generic text.

A knowledge statement must carry, where applicable: identifier, formal statement, type, variables/entities, units, assumptions, applicability domain, evidence class, source/derivation, uncertainty, version, review state and known exceptions. Conflicting evidence must remain visible rather than silently overwritten.

### 5.4 Knowledge representation and reasoning

Use the representation that preserves scientific meaning:
- Typed property/knowledge graphs for entities and relations.
- Symbolic algebra and equation systems for derivations.
- Dimensional analysis and unit-aware quantities.
- Constraint satisfaction and optimization for feasibility.
- Causal/dependency graphs where causality is justified.
- Geometric, topological, sequence, reaction-network and matrix representations in their respective domains.

Do not represent every scientific fact as untyped text or every scientific problem as a language-model completion. Preserve exact numerical precision, units and coordinate conventions. A learned correlation must not be relabelled as a physical law.

### 5.5 Construction and evaluation

The shared Construction Engine provides orchestration/contracts and reusable primitives; the scientific construction algorithm remains domain-owned. Supported construction modes:

- **Reconstruction:** recover/assemble a representation from supplied observations or constraints.
- **Generalization:** extend a known mechanism/model to a new supported context with explicit assumptions.
- **Exploration:** search a defined candidate space for previously unobserved possibilities.

Each construction task declares input representation, search space, constraints, objective(s), algorithm, budget, stopping criteria, candidate identity, uncertainty and verification plan. Multi-objective trade-offs must remain explicit; do not hide them in one opaque score.

### 5.6 Proposer–Verifier separation

A Proposer generates candidates. A Verifier independently checks them. They may share canonical inputs but must not share an unexamined assumption that makes verification circular. Verification may use different algorithms, analytical invariants, independent implementations, alternative physical models, benchmark references or experiments.

The Verifier returns accepted/rejected/indeterminate/needs_human_review with metrics, thresholds, rule versions and evidence. A failed candidate remains a useful artifact with failure reason; it must not be silently discarded.

## 6. Universal service architecture A–N

Every service must have its own:
- Domain ontology/knowledge package and formal concepts.
- Canonical input/output representations and versioned schemas.
- Governing principles, equations, mechanisms and constraints where applicable.
- Analysis and construction algorithms.
- Evaluation metrics and explicit objective functions.
- Independent verification Rulebook and evidence levels.
- Provenance, uncertainty and reproducibility contracts.
- Tests for known cases, edge cases, out-of-distribution cases and constructed candidates.

| Service | Knowledge and reasoning emphasis | Construction / discovery examples (illustrative, not current feature claims) |
|---|---|---|
| A — Molecular | Molecular identity, graph theory, stereochemistry, bonding, descriptors and physical chemistry | Molecular graph/representation construction, constrained molecular transformations and candidate exploration |
| B — Sequence | Sequence alphabets, grammar, alignment, evolutionary/statistical models and sequence constraints | Sequence assembly, constrained sequence generation, motif/ORF reasoning and comparative hypotheses |
| C — Structure | Geometry, topology, coordinate systems, stereochemistry, structural constraints and energy models | 3D geometry/structure construction, conformational exploration and structural hypothesis evaluation |
| D — Chemistry | Chemical laws, valence, reaction mechanisms, electron/bond representations, thermodynamics and kinetics | Reaction/pathway construction, product candidates, mechanism hypotheses and chemical-space exploration |
| E — Protein | Sequence–structure–function relationships, folding/energetics, domains, interactions and uncertainty | Protein representation/conformation/function hypotheses and design candidates under safety gates |
| F — Genomics | Genome organization, variation, inheritance, population/statistical models and coordinate systems | Variant interpretation hypotheses, haplotype/annotation construction and genomic model exploration |
| G — DNA/RNA | Base pairing, sequence grammar, thermodynamics, folding, kinetics and molecular interactions | Oligo/nucleic-acid construction, folding hypotheses and constrained sequence exploration |
| H — Simulation | Governing differential equations, force fields, ensembles, boundary conditions, numerical stability and sampling | Simulation protocol/system construction, parameter exploration and model comparison |
| I — Kinetics | Reaction networks, rate laws, ODEs, stochastic processes, identifiability and conservation | Network/mechanism construction, parameter inference and kinetic hypothesis testing |
| J — Omics | Measurement models, normalization, statistics, latent structure, batch effects and multi-omics relations | Analysis model construction, pathway/feature hypotheses and experimental-design exploration |
| K — Phylogeny | Evolutionary models, substitution processes, tree metrics, uncertainty and sampling assumptions | Tree/network reconstruction, model comparison and evolutionary hypothesis evaluation |
| L — Pharmacogenomics | Allele definitions, haplotypes, variant function, evidence grading and population limits | Diplotype/phenotype hypothesis construction and evidence-aware interpretation; no autonomous prescribing |
| M — Cohorts | Study design, causal inference, sampling, missingness, privacy and statistical uncertainty | Cohort construction, synthetic-data generation under safeguards and study-design exploration |
| N — Workflows | Typed contracts, dependency graphs, execution semantics, provenance and resource constraints | Scientific workflow synthesis, dependency optimization and reproducible multi-domain plans |

This table defines the common direction; it does not assert that the examples are implemented. Existing A–N service code remains the execution foundation and must be audited/reused, not discarded for a speculative rewrite.

## 7. Knowledge and evidence acquisition

External databases, papers, experimental datasets, pretrained models and reference structures are evidence sources—not the definition of the scientific universe.

- Implement connectors as optional, versioned adapters with caching, rate limits, checksums and offline fixtures.
- Preserve source accession/URL, exact release/version, retrieval date, checksum, transformations, attribution and specific license/terms.
- Verify license and permitted use for each dataset, model code, checkpoint and derived asset; never assume a whole database has one blanket license.
- Maintain local knowledge packs for offline and reproducible operation.
- Capture derivations and expert-curated rules as first-class versioned knowledge artifacts.
- Preserve conflicts, uncertainty, negative results and known limitations.
- Use external predictors (including structure prediction) as optional candidate generators; never make any one database, modality or predictor a mandatory prerequisite for all scientific construction.
- Avoid training data leakage: record dataset snapshots, split manifests, cutoff dates and similarity/cluster policies.

## 8. Data, models and computation governance

Every input/model/dataset/derived result has immutable identity and provenance. Record model/provider/version, checkpoint and weights hash, input hash, parameters, seed, runtime, precision/device, resource use and confidence outputs where relevant. Predictions and simulations must be labelled as such.

Training is not an early shortcut. Establish a deterministic baseline and evaluation set first. Train/fine-tune only when a measured gap justifies it and rights, compute, privacy, leakage and reproducibility controls are in place. Synthetic data and synthetic labels must never be represented as experimental observations.

Optional engines may include local numerical/scientific software or remote providers. Every adapter must declare version, license, input/output contract, resource requirements, network policy and fallback behavior. Core functionality must not silently depend on unavailable external services.

## 9. Workflow, artifact and report contracts

Reuse existing Workflow v1, capability registry, Rulebook runtime and MSDE. Do not build a parallel planner/executor.

Every workflow operation declares capability/version, typed inputs, output schema, parameters, dependencies, method/model identity, resource budget, permissions/egress, timeout, verification Rulebooks, failure/cancellation/retry behavior and provenance.

Every scientific artifact should include:
- Immutable content identity, media/schema version and domain/service.
- Epistemic status and validation state.
- Parent/input artifact IDs and transformation lineage.
- Source/knowledge references and exact versions.
- Method, engine, model and configuration.
- Units, coordinate/reference conventions and transformations.
- Assumptions, applicability domain and uncertainty.
- Verification rule IDs/versions, metrics, thresholds and evidence artifacts.
- Reproducibility metadata and failure/partial status where applicable.

Every report claim maps to artifact IDs and field paths. Narrative can explain evidence but cannot create unsupported values or references. Distinguish absent evidence from a negative result.

## 10. Agentics operating lifecycle and autonomy

Request → interpret → clarify → discover knowledge/capabilities → formulate → plan → validate → explain/approve → execute → evaluate → independently verify → classify → report → audit.

Start with one orchestrator and typed specialist stages. Add multi-agent delegation only after the single-orchestrator path is safe, measurable and traceable. Agents communicate through typed contracts/artifact references; every delegation has allowlisted tools, task bounds, budget, timeout, provenance and termination conditions.

- **L0 Explain:** explain knowledge/capabilities/evidence; no execution.
- **L1 Draft:** produce plan/candidate strategy; no scientific operation.
- **L2 Approved execution:** execute a user-approved bounded workflow.
- **L3 Bounded iteration:** finite, pre-authorized optimization/search loops with stop conditions.
- **L4 Consequential autonomy:** disabled and out of scope absent separate governance and institutional approval.

Planning never implies execution. Approval binds to exact plan digest, inputs, capability versions, egress and resource envelope. Material changes invalidate approval.

## 11. Safety, security, privacy and responsible construction

- Model output, retrieved pages, papers, sequence headers, annotations, filenames and tool results are untrusted data, never instructions.
- Never execute model-generated code, shell commands, SQL or arbitrary scripts.
- Use OS-level isolation for untrusted execution; enforce CPU, memory, GPU, disk, process, network, wall-time, concurrency and output bounds.
- Network denied by default; allowlist capability-specific egress and obtain consent before user data leaves the environment.
- Preserve failed, cancelled, timed-out and partial outputs as explicit evidence.
- Do not commit secrets, patient-identifiable data or private research data; minimize and redact logs.
- Apply domain-specific safety and biosecurity policies to biological, chemical and other sensitive design capabilities. Keep high-risk design disabled until risk assessment, screening, human review and institutional authorization are recorded.
- Clinical interpretation, prescribing, experimental authorization and wet-lab execution are not delegated to Agentics.
- Respect all data, software, model and checkpoint licenses and use restrictions.

## 12. Existing implementation — preserve and extend

The repository already contains:
- `python/molecularis/ai.py`: model-agnostic callable planner, active capability catalog, strict Workflow v1 validation, operation bounds, persisted plan artifact with input lineage and explicit approval before execution.
- `python/molecularis/workflows_service.py`: workflow DAG validation, capability resolution and execution through Core Rulebook runtime.
- `python/molecularis/bootstrap.py`: A–N service bootstrap.
- Core/MSDE: content-addressed artifacts, catalog, lineage, budgets, capability registry and Rulebook execution evidence.
- Existing service A–N implementations and service Rulebooks/specifications.

Do not duplicate these systems. The current AI foundation is an initial planning/execution layer, not a finished autonomous scientific discovery system. Current limitations include provider configuration, a complete SKE, shared construction/evaluation contracts, full cross-service scientific handoff, independent proposer/verifier evidence, report composer, OS-level sandbox and recovery certification.

## 13. Sequential implementation roadmap and gates

Phases are sequential. Implement one phase at a time, report exact evidence, then stop. No phase is complete because its documents exist.

### P0 — Repository truth, safety and platform reliability
- Reconcile docs, actual code, branch and CI.
- Threat model, trust boundaries, network/egress policy and privacy classification.
- OS-level sandbox design and implementation; process-tree termination; resource limits.
- Failed/intermediate/cancelled run evidence.
- Artifact backup/restore, corruption and crash-boundary tests.
- Reproducibility baseline, schema validation and documentation consistency.

**Gate:** evidence-backed platform safety/recovery baseline; unresolved controls listed as blockers.

### P1 — Universal scientific knowledge architecture
- Formalize SKE concepts, typed entities/relations, quantities/units, equations/laws/mechanisms, assumptions, applicability domains and evidence records.
- Define versioned knowledge artifact/schema contracts and provenance.
- Define conflict, uncertainty, temporal validity and review states.
- Define representation contracts for graph, symbolic, geometry, sequence, reaction network, matrices and workflow domains.
- Define knowledge query/reasoning interfaces and deterministic fixture suite.
- Map A–N knowledge package boundaries and shared concepts without erasing domain semantics.

**Gate:** executable schemas and reference implementation; round-trip tests preserve types, units, assumptions, provenance and conflicts. No claim of comprehensive scientific knowledge.

### P2 — Shared reasoning and construction primitives
- Unit/dimension-aware quantities and validation.
- Symbolic expression/equation representation and derivation traces.
- Constraint systems, feasibility checks and optimization contracts.
- Typed candidate, objective, uncertainty and evaluation artifacts.
- Proposer–Verifier protocol and non-circular verification policy.
- Reconstruction/generalization/exploration task contracts.
- Deterministic minimal end-to-end examples from more than one distinct service domain.

**Gate:** reference examples construct candidates and independently evaluate them with reproducible artifacts; explicit indeterminate/failure states tested.

### P3 — Knowledge-to-Construction integration across A–N
- Add service-specific knowledge packages and construction/evaluation interfaces one service at a time.
- Audit and adapt existing A–N engines; no unnecessary rewrite.
- Map each service's laws, constraints, algorithms, metrics and acceptance criteria.
- Cross-service typed artifact handoff and provenance continuity.
- Independent domain verification and negative/adversarial cases.
- Preserve each service's scientific authority and versioned Rulebook.

**Gate:** every service demonstrates its own scoped lifecycle; cross-domain workflows prove compatibility. Scientific acceptance remains separate until university review.

### P4 — Agentics intelligence and orchestration maturity
- Intent/entity/task contracts and clarification.
- Provider-neutral LLM adapter (optional) and deterministic mock.
- Capability schemas → constrained tool definitions.
- Planner uses SKE query/reasoning interfaces and construction contracts.
- Approval bound to exact plan/input hashes, egress and resource envelope.
- Evidence-only report composer with claim/field citations.
- Session/run trace, cancellation and bounded iteration.
- At least 50 grounded/adversarial evaluation cases including injection, fabricated laws, unit errors, uncertainty, out-of-domain requests, unsafe intent and unsupported claims.

**Gate:** evaluation suite passes declared thresholds; zero unsupported scientific claims in curated cases; all outputs trace to artifacts; approval/policy tests pass.

### P5 — Optional specialist scientific models and training
- Add model adapters only where benchmarked gaps justify them.
- Structure predictors are optional tools within Structure/Protein workflows, not the system's centre.
- Verify exact code, checkpoint, training-data and output licenses separately.
- Dataset snapshots, checksums, quality filters, leakage-resistant temporal/cluster splits and model registry.
- Reproducible training/evaluation harness only after baseline and license/privacy review.
- Post-cutoff or otherwise leakage-aware benchmark; calibration and uncertainty evaluation.
- Clearly separate predicted, simulated, constructed and observed artifacts.

**Gate:** reproducible benchmark and license/privacy audit; demonstrated improvement over deterministic baseline; no unsupported accuracy claims.

### P6 — Controlled discovery and design capabilities
- Enable reconstruction/generalization/exploration by domain only after P3/P4 safety and verification readiness.
- Domain-specific risk assessment and biosecurity/chemical safety policy where relevant.
- Candidate generation with bounded search, explicit objectives and stopping conditions.
- Independent verification, adversarial screening, human review and institutional approval.
- Preserve negative results and uncertainty; no autonomous wet-lab/clinical actions.

**Gate:** separate approval per capability/domain; screening and independent review evidence; disabled by default until approved.

### P7 — Generalization, scaling and research evaluation
- Extend proposer/verifier and knowledge packs to new scientific domains without breaking shared contracts.
- Evaluate generalization beyond training/reference examples.
- Measure compute/resource scaling, reproducibility and failure recovery.
- Independent university review, benchmark replication and scientific contract freeze.
- Publish a system report separating engineering, computational evidence and experimental validation.

**Gate:** university/institutional acceptance and reproducibility evidence for each claimed scientific capability; remaining limitations published.

## 14. Evaluation framework

Evaluate at several levels, not by one aggregate score:

- **Representation:** schema validity, units, identity and round-trip preservation.
- **Reasoning:** derivation correctness, assumption visibility, dimensional consistency and applicability-domain handling.
- **Construction:** feasibility rate, constraint violations, search coverage, novelty protocol and reproducibility.
- **Evaluation:** objective validity, sensitivity, robustness and uncertainty calibration.
- **Verification:** independence, false acceptance/rejection, indeterminate handling and reference agreement.
- **Generalization:** held-out contexts, temporal/cluster separation and out-of-distribution behavior.
- **Orchestration:** plan validity, capability correctness, approval binding, safe failure and traceability.
- **Operations:** latency, throughput, resource bounds, recovery and deterministic replay.

Metrics and thresholds are domain-owned and must be justified. A high model score cannot replace a scientific acceptance criterion.

## 15. Definition of done for every service

A service is not complete under this architecture until it has:
1. A documented domain knowledge model and applicability boundaries.
2. Canonical versioned representations, units and provenance.
3. Reusable analysis and construction methods appropriate to its scope.
4. Explicit objectives, constraints and evaluation metrics.
5. A domain-owned independent verification Rulebook.
6. Known-case, edge-case, constructed-candidate, negative and out-of-domain tests.
7. Reproducibility and resource-bound evidence.
8. Typed integration with Core/MSDE and other relevant services.
9. Epistemic labels, uncertainty and claim-level evidence.
10. Engineering CI evidence and separate scientific review/acceptance status.

If a service has no meaningful construction task in a particular subdomain, it must document why and still support the lifecycle for the tasks it does own. Do not invent a generator merely to satisfy terminology.

## 16. Governance, sequencing and reporting

- Continue development directly on CORE using expected-head, non-force updates.
- One phase at a time; no silent phase skipping.
- Preserve useful existing code and public contracts; changes require migration evidence.
- External tools/models remain optional and explicitly governed.
- University scientific/privacy review is separate from engineering CI and is conducted after the owner-directed A–N engineering sequence.
- Every report lists changed files, commit, CI/tests, exact pass/fail/skip/not-tested counts, gate state, limitations and next phase.
- Never claim “discovery”, “understands physics”, “scientifically validated” or “production-ready” without a precise evidence standard and supporting results.

## 17. Explicit non-claims

This plan does not claim that the current repository already contains a complete SKE, universal scientific reasoning, general-purpose novel structure/code generation, a production autonomous agent, certified sandbox, complete cross-service scientific compatibility, trained foundation models or experimental validation. These are goals with phase gates, not present capabilities.

**Final north star:** Molecularis should become a general scientific knowledge-to-construction platform: it uses established knowledge and governing principles to reason, build candidates, test them and responsibly explore what is not yet known—across all fourteen services.
