# Agentics Molecularis — Master Plan, Architecture and Acceptance Standard

**Version:** 2.1  
**Status:** Governing architectural authority; implementation is phase-gated.  
**Owner:** Molecularis / AssayFlux  
**Scope:** Agentics Molecularis and its shared scientific foundation across all A–N services.

> This is the single authoritative Agentics Molecularis plan. Supporting documents define implementation details, operational rules, scientific disciplines, candidate tools and acceptance evidence. They must remain consistent with this plan and must not create competing AI architectures or roadmaps.

## 1. Executive direction

Agentics Molecularis is the goal-directed intelligence, scientific reasoning and orchestration system of Molecularis. Its purpose is to help researchers express scientific objectives, assemble relevant knowledge, reason under explicit assumptions and constraints, construct candidate solutions, evaluate them, independently verify them and learn from approved evidence.

The system must not be limited to retrieving known molecular structures, matching PDB/X-ray records, calling pretrained predictors or reproducing examples in existing databases. Such resources are useful evidence, training material where permitted, baselines and optional methods—not the boundary of scientific exploration.

The long-term objective is a system that can work from scientific knowledge structures and governing principles to construct known and previously unrecorded candidate structures, sequences, models, mechanisms, workflows and other scientific artifacts. Novelty is not proof: every candidate must carry its derivation, assumptions, uncertainty, applicability domain and verification state. Experimental realizability and function require evidence appropriate to those claims.

Agentics is not a replacement for scientific engines, domain services, researchers or experimental validation. It coordinates and reasons over Molecularis capabilities. Domain services remain authoritative for their scientific semantics, algorithms, constraints, Rulebooks and acceptance thresholds.

## 2. Mission and north star

**Mission:** Build a trustworthy, extensible scientific intelligence system that can acquire authorized knowledge, represent scientific concepts and laws, reason with mathematical and domain constraints, construct candidate artifacts, evaluate alternatives, independently verify claims and preserve a complete evidence trail.

**Permanent lifecycle across every service A–N:**

**Understand → Represent → Reason → Construct → Evaluate → Verify → Learn.**

The lifecycle is a shared architectural contract, not a promise that every stage is already implemented in every service. Each service declares the stages and scientific claims it supports.

### Success criteria

A researcher can:
1. State a research objective and its constraints.
2. Supply or identify relevant data, sources and conditions.
3. Obtain a transparent account of the knowledge and methods selected.
4. Review a structured construction plan before execution.
5. Approve bounded operations using registered capabilities.
6. Receive reproducible scientific artifacts with complete lineage.
7. Inspect independent verification, uncertainty, failures and limitations.
8. Reuse approved outcomes as governed knowledge for later work.

## 3. Non-negotiable principles

1. **Scientific integrity over plausibility.** Fluent explanations and high model confidence do not establish truth.
2. **First principles where applicable.** Use governing mathematics, physics, chemistry and domain mechanisms with explicit assumptions and validity domains.
3. **Knowledge beyond reference examples.** Existing observations and databases inform construction but do not define the limits of exploration.
4. **One Agentics architecture.** This document is the single AI architectural authority.
5. **Domain ownership.** Every A–N service owns its scientific meaning, methods, constraints and acceptance thresholds.
6. **Pre-generation audit.** No scientific construction begins before required inputs, units, assumptions, sources, constraints, applicability, safety and resources are checked.
7. **Independent post-generation verification.** A proposer cannot be the sole verifier of its own output.
8. **Evidence classes remain explicit.** Observation, established knowledge, derivation, inference, prediction, simulation, construction, hypothesis and validation are distinct.
9. **Uncertainty is first-class.** Preserve uncertainty, sensitivity, alternative explanations, calibration limits and unknowns.
10. **Provenance is mandatory.** Inputs, knowledge, data, tools, models, parameters, environments, decisions and outputs remain traceable.
11. **Human authority is preserved.** Consequential, safety-sensitive, clinical, experimental and irreversible actions require appropriate qualified authorization.
12. **Bounded execution.** All operations have declared resource, time, concurrency, network and output limits.
13. **Fail visibly.** Missing data, unsupported conditions, failed checks and unavailable tools must never be silently converted into success.
14. **No fabricated capabilities.** A planned module or listed package is not an implemented or validated capability.
15. **Preserve working infrastructure.** Extend existing Core/MSDE, artifact, provenance, capability and workflow systems rather than creating parallel replacements.
16. **Permission-aware learning.** Data access does not imply permission to ingest, redistribute or train.
17. **Reproducibility and reversibility.** Version knowledge, models, rules and tools; support replay and rollback where feasible.
18. **Independent scientific acceptance.** Engineering CI, model benchmarks and university/experimental validation are separate evidence categories.

## 4. Scientific evidence and epistemic model

Every important scientific statement and generated artifact must declare an evidence/epistemic class. The minimum vocabulary is:

| Class | Meaning |
|---|---|
| Observed | Directly measured or recorded observation with measurement provenance |
| Established | Accepted knowledge supported by appropriate independent evidence |
| Derived | Obtained by explicit mathematical or logical derivation from stated premises |
| Inferred | Reasoned conclusion from evidence and a stated model |
| Predicted | Output of a predictive model or statistical estimator |
| Simulated | Output produced by a declared computational simulation |
| Constructed | Artifact created by an explicit construction procedure |
| Hypothesized | Candidate explanation or artifact awaiting adequate verification |
| Validated | Claim that passed a defined validation protocol within a declared scope |

Classes are not a simplistic linear ranking. A simulation may be reproducible without being experimentally confirmed; a construction may be mathematically valid without being physically stable. Reports must identify the exact claim and evidence that supports it.

### Scientific claim separation

Do not conflate:
- syntactic/schema validity;
- mathematical consistency;
- chemical or domain-specific validity;
- physical plausibility;
- stability under specified conditions;
- experimental realizability;
- biological or functional activity;
- clinical or operational utility.

Passing one level does not imply passing the next. Validation always states scope, conditions, method, reference independence and limitations.

## 5. Universal scientific lifecycle

### 5.1 Understand
Parse the objective, intended artifact, scope, constraints, acceptance criteria, supplied evidence and missing essential information. Ask for clarification or record explicit assumptions; never silently invent measurements or conditions.

### 5.2 Represent
Convert the task into typed, versioned scientific objects: entities, quantities, units, coordinate/reference systems, equations, parameters, assumptions, evidence, constraints and provenance. Preserve domain meaning.

### 5.3 Reason
Retrieve applicable knowledge and derive consequences using symbolic, numerical, probabilistic, causal, geometric or domain-specific reasoning. Distinguish laws from empirical correlations and record the validity domain of every method.

### 5.4 Construct
Generate one or more candidates using explicit construction strategies, registered algorithms and bounded resources. Support:
- **Reconstruction:** recover or assemble an artifact from observations/evidence.
- **Generalization:** extend a validated pattern or method within justified assumptions.
- **Exploration:** search candidate space under declared constraints, uncertainty and safety boundaries.

### 5.5 Evaluate
Score candidates against declared objectives, hard constraints, soft preferences, uncertainty, sensitivity, robustness and computational cost. Do not collapse all criteria into an unexplained score.

### 5.6 Verify
Run independent checks appropriate to each claim: mathematical invariants, dimensional analysis, domain validators, alternate algorithms, reference datasets, simulation checks or experimental evidence. Record passed, failed, skipped, indeterminate and not-applicable checks.

### 5.7 Learn
Capture approved observations, corrections, failed attempts, discrepancies and validation outcomes. Route them through knowledge governance. Learning may update retrieval, curated knowledge, Rulebooks, algorithms or models; these are separate controlled change types.

## 6. Target architecture

The logical architecture is:

1. **Agentics Orchestrator** — objective interpretation, planning, capability discovery, approval, bounded coordination and evidence-grounded reporting.
2. **Scientific Knowledge Engine (SKE)** — typed scientific concepts, entities, relations, equations, laws, mechanisms, constraints, assumptions, evidence and applicability domains.
3. **Knowledge Representation and Reasoning** — graph, symbolic, mathematical, probabilistic, causal, geometric and constraint reasoning.
4. **Scientific Computing Foundation** — unit-aware mathematics, numerical methods, statistics, uncertainty, optimization, graph/geometry and reusable computation.
5. **Construction and Simulation** — candidate generation, reconstruction, generalization, exploration and selected domain solvers.
6. **Evaluation and Independent Verification** — objective evaluation, invariants, alternative methods, domain Rulebooks, benchmarks and explicit decision states.
7. **A–N Scientific Services** — domain-owned engines, runtimes, data, methods, Rulebooks and validators.
8. **Core / MSDE** — capability registration, typed contracts, immutable artifacts, metadata, provenance, workflow execution, resource policy and audit history.

This is a logical architecture, not a mandate to create an independent microservice or empty directory for every box. Reuse existing Molecularis infrastructure. Keep scientific meaning in the domain services; keep generic artifact identity, storage and workflow infrastructure in Core/MSDE.

### 6.1 Scientific Knowledge Engine requirements

SKE must be more than a text corpus or vector index. It must support typed, versioned, queryable scientific knowledge, including:
- concepts, entities, identifiers and domain namespaces;
- relations, mechanisms, causal links and dependencies;
- equations, variables, parameters, units and dimensional constraints;
- laws and empirical relationships as different knowledge types;
- assumptions, preconditions, boundary conditions and applicability domains;
- evidence records, source identity, citations, licenses and quality;
- uncertainty, contradictory claims, exceptions and unresolved questions;
- derivation traces and links to generated artifacts;
- version history, provenance and review state.

A law or equation must not be stored without its variables, units, assumptions, scope and known limitations. Conflicting evidence must remain visible; the system must not silently select a convenient source.

### 6.2 Reasoning requirements

Reasoning may combine:
- symbolic derivation and formal logic;
- numerical calculation and differential-equation solving;
- dimensional analysis and conservation laws;
- probability, Bayesian inference and statistical estimation;
- causal reasoning with explicit assumptions;
- graph, geometric and topological reasoning;
- domain-specific algorithms and simulation.

The system must expose the chain of computational evidence: premises, method, parameter values, intermediate results, assumptions, error/tolerance and conclusion. A natural-language rationale alone is not a derivation.

### 6.3 Proposer–Verifier separation

The component proposing a candidate must not be the only component deciding that it is valid. Where practical, use independent implementations, algorithms, invariants, data sources or domain validators. Record verifier identity/version and independence limitations. If no independent verifier exists, return an explicit unverified or indeterminate state and request review.

## 7. Shared scientific computing foundation

The scientific discipline map is maintained in [SCIENTIFIC_FOUNDATION.md](../services/ai/SCIENTIFIC_FOUNDATION.md). The following capabilities are shared foundations; their priority and depth depend on real A–N use cases.

### Mathematics and computation
- mathematical logic, algebra and discrete mathematics;
- calculus, linear algebra, tensor mathematics and numerical analysis;
- differential equations, PDEs, root finding and integration;
- geometry, differential geometry, topology and graph theory;
- symbolic computation, formal proofs and constraint solving;
- convex, nonlinear, global and multi-objective optimization;
- information theory, probability and stochastic processes.

### Physics and engineering
- classical and analytical mechanics;
- quantum mechanics and electromagnetism where relevant;
- thermodynamics and statistical mechanics;
- fluid, continuum and solid mechanics;
- waves, optics, transport and heat/mass transfer;
- materials science, control theory and computational physics;
- numerical simulation, finite-element/finite-volume methods and HPC.

### Chemistry and materials
- organic, inorganic, physical, analytical and computational chemistry;
- quantum chemistry, chemical bonding and molecular orbital theory;
- chemical thermodynamics, kinetics, catalysis and reaction mechanisms;
- stereochemistry, coordination, supramolecular, polymer and materials chemistry;
- crystallography, spectroscopy and electrochemistry.

### Biology and life sciences
- molecular and cell biology, genetics and genomics;
- biochemistry, structural biology and evolution;
- microbiology, immunology, neuroscience and physiology;
- systems, synthetic, population and computational biology;
- bioinformatics, pharmacology and toxicology.

### Statistics and experimental methodology
- descriptive/inferential statistics and probability distributions;
- Bayesian and frequentist inference;
- regression, multivariate analysis and time series;
- causal inference, survival analysis and meta-analysis;
- experimental design, sampling, power and multiple-testing correction;
- measurement science, calibration, bias, missing data and uncertainty quantification;
- reproducibility, falsifiability and scientific method.

### Computer and information sciences
- algorithms, data structures and formal methods;
- knowledge representation, databases and graph computation;
- machine learning, deep learning and scientific ML;
- probabilistic programming, model evaluation and information retrieval;
- parallel/distributed computing, HPC, security and privacy engineering.

### Additional sciences
Materials science, crystallography, geoscience, geophysics, atmospheric and climate science, oceanography, astronomy/astrophysics, environmental science, epidemiology, cognitive science and network/complexity science may be incorporated when a defined research objective requires them. Their inclusion in the discipline map is not a claim of implemented support.

## 8. Scientific tools and dependency policy

Candidate libraries, engines and infrastructure are catalogued in [SCIENTIFIC_TOOL_REGISTRY.md](../services/ai/SCIENTIFIC_TOOL_REGISTRY.md). The registry is not an installation manifest, vendor endorsement or scientific acceptance record.

Adoption rules:
1. Audit current Molecularis code, dependencies, adapters and tests before adding anything.
2. Identify a measurable scientific or engineering gap and a concrete service use case.
3. Compare suitable alternatives, maintenance, platform support, security and performance.
4. Review exact package/executable/model/data versions, licenses and usage terms.
5. Define a narrow Molecularis adapter with typed schemas, units, provenance, budgets and explicit errors.
6. Keep optional packages in optional profiles or isolated workers; do not make all tools core dependencies.
7. Add independent reference, boundary, negative, reproducibility and failure tests.
8. Document limitations and provide an explicit unavailable state when an optional engine is absent.
9. Avoid redundant overlapping packages unless measured evidence justifies them.
10. Do not substitute a scientifically different algorithm silently when an engine is unavailable.

The first audit should examine existing NumPy/SciPy/SymPy/Pint, statistics/data packages, optimization libraries, graph/geometry tools and current A–N scientific integrations before deciding on new dependencies. GPU/HPC solvers, large model checkpoints and specialist executables require separate deployment and license review.

## 9. A–N domain ownership and scientific priorities

Every service uses the shared lifecycle and scientific contracts, but owns its domain science.

| Service | Priority scientific foundations and responsibility |
|---|---|
| A — Molecular | Molecular representations, graph theory, geometry, topology, units, physical/quantum chemistry |
| B — Sequence | Discrete mathematics, information theory, sequence algorithms, genetics, evolution, statistics |
| C — Structure | Linear algebra, coordinate geometry, topology, mechanics, crystallography, structural validation |
| D — Chemistry | Chemical graph theory, organic/inorganic/physical chemistry, thermodynamics, kinetics, quantum chemistry |
| E — Protein | Biochemistry, sequence evolution, structural biology, geometry, statistical mechanics |
| F — Genomics | Genetics, population genetics, statistics, experimental design, variant evidence and algorithms |
| G — DNA/RNA | Molecular biology, nucleic-acid chemistry, polymer physics, thermodynamics and folding |
| H — Simulation | Numerical analysis, mechanics, statistical mechanics, ODE/PDE solvers and reproducible execution |
| I — Kinetics | Differential equations, stochastic processes, chemical kinetics, parameter estimation and sensitivity |
| J — Omics | Statistics, multivariate analysis, experimental design, multiple testing and causal inference |
| K — Phylogeny | Evolution, likelihood/Bayesian inference, graph algorithms, model selection and uncertainty |
| L — Pharmacogenomics | Genetics, pharmacology, biostatistics, evidence/guideline provenance and population limitations |
| M — Cohorts | Epidemiology, sampling, biostatistics, causal inference, privacy and bias controls |
| N — Workflows | Computer science, formal methods, graph algorithms, scheduling, provenance and resource optimization |

No shared AI component may redefine a service's scientific thresholds or bypass its Rulebook. Cross-service handoffs preserve units, reference conventions, evidence class, uncertainty and provenance.

## 10. Knowledge acquisition, organizational data and learning

Agentics should learn from all relevant, authorized scientific knowledge available from universities, laboratories, research organizations, publications, repositories, standards, validated software and approved internal datasets.

This does not mean indiscriminately ingesting or training on every file. For each source, record:
- source owner, identity, version/date and retrieval method;
- license, terms, consent, privacy and permitted purposes;
- checksum, format, transformations and dataset manifest;
- scientific quality, methods, labels, bias and limitations;
- duplicate/near-duplicate and leakage analysis;
- review status, attribution and provenance.

### Separate learning pathways

- **Retrieval/index update:** make approved knowledge discoverable.
- **Curated knowledge update:** add or revise reviewed facts, equations, evidence and relations.
- **Rulebook/algorithm update:** change operational scientific methods under change control.
- **Model training/fine-tuning:** change model weights only after a measured need, permission-cleared dataset, reproducible training manifest, leakage-resistant evaluation, regression gate and rollback plan.
- **Benchmark update:** change evaluation data only with versioning and protection against test leakage.

New data does not automatically trigger model retraining. A failed prediction or construction is retained with its conditions and failure reason; it is not silently converted into a positive training label. Researcher corrections and laboratory outcomes require attribution and appropriate review before promotion to authoritative knowledge.

## 11. Artifact, workflow and reporting contracts

Every scientific workflow must use versioned typed contracts and registered capabilities. A plan and its approval are bound to the exact plan digest, input artifact identities/hashes, capability versions, permissions, data egress and resource envelope. A material change invalidates approval.

Every material result should preserve:
- objective and requested output;
- input artifacts and parent lineage;
- source/evidence records and knowledge version;
- equations, algorithms, model/tool identities and versions;
- assumptions, units, coordinates, parameters and conditions;
- environment, random seeds and nondeterminism notes;
- intermediate artifacts, logs and failure records;
- verification checks, thresholds and results;
- uncertainty, limitations and evidence class;
- explicit final decision state.

Minimum decision states: **accepted, rejected, indeterminate, failed, cancelled, needs_human_review, not_applicable**.

Reports must link claims to artifact IDs, source records or derivation traces. Do not invent citations, measurements, parameters, confidence values or test results.

## 12. Safety, security and autonomy

Autonomy is earned through evidence and explicit gates.

- **Level 0 — Advisory:** interpret questions, explain knowledge and propose plans.
- **Level 1 — Draft planning:** create structured plans and candidate parameters; no execution.
- **Level 2 — Approved execution:** execute registered bounded capabilities after explicit approval.
- **Level 3 — Bounded routine automation:** only pre-approved low-risk workflows with monitoring, budgets and rollback.
- **Level 4 — Research exploration:** controlled candidate exploration under domain safety policies, independent verification and human oversight. This is not unrestricted autonomy.

All model outputs and retrieved content are untrusted data. No arbitrary model-generated code, shell, SQL or scripts execute directly. Any permitted generated program must pass validation and run in an isolated, resource-limited environment with explicit filesystem, process and network policy.

Protect secrets, sensitive data, model weights, institutional datasets and user artifacts. Apply least privilege, egress controls, audit logs, dependency/supply-chain review and explicit retention policy. Clinical, wet-lab, hazardous, safety-sensitive, external publication and irreversible actions require qualified human/institutional authorization. AI cannot change its own safety policy or scientific acceptance criteria.

## 13. Existing Molecularis implementation to preserve

The existing platform includes a model-agnostic AI planning layer and approval-gated Workflow v1, A–N service bootstrap, Core/MSDE artifact/catalog/provenance foundations, capability registration and Rulebook workflow execution.

These are engineering foundations, not a complete autonomous scientific AI. Preserve existing code and public contracts; audit before replacement. The present implementation status, test evidence and open platform gaps are recorded in [SERVICE_STATUS.md](SERVICE_STATUS.md).

The following must not be represented as complete without separate evidence:
- complete Scientific Knowledge Engine and typed scientific knowledge graph;
- shared unit-aware symbolic/numerical/statistical computation layer;
- broad scientific solver integration;
- universal pre-generation auditor and independent post-generation verifier;
- full real cross-service knowledge-to-construction workflows;
- provider/deployment integration and robust artifact-grounded report generation;
- governed training pipeline and model registry;
- OS-level sandbox, recovery certification and distributed execution;
- independent university scientific validation.

## 14. Sequential implementation roadmap and phase gates

Implementation follows these phases in order. A phase is complete only when its acceptance evidence is recorded and reviewed. The detailed scientific foundation subphases SF0–SF9 are subordinate execution tasks, not a competing roadmap.

### P0 — Repository truth, safety and reliability
Reconcile actual code, contracts, dependencies, status and documentation. Close critical provenance, security, resource and recovery gaps. Establish threat model, permission boundaries, failure semantics and trustworthy baseline.

**Gate:** evidence-backed repository inventory, documented threat model, enforceable execution policy and passing baseline tests for changed areas.

### P1 — Universal scientific knowledge architecture
Define typed scientific knowledge/evidence contracts: entities, concepts, relations, equations, assumptions, units, validity domains, source provenance, uncertainty and versioning. Integrate with existing artifact lineage.

**Gate:** versioned knowledge packages can be ingested, queried, serialized, compared and traced without loss of scientific meaning.

### P2 — Shared reasoning and construction primitives
Implement unit/dimension checks, symbolic and numerical derivation, statistics and uncertainty, constraints, optimization, graph/geometry primitives, construction contracts and independent proposer/verifier boundaries.

**Gate:** reference calculations and independent checks pass; generated artifacts carry assumptions, uncertainty and provenance.

### P3 — A–N knowledge-to-construction integration
Integrate the shared foundation into A–N one domain slice at a time. Preserve service-owned engines, Rulebooks, acceptance thresholds and the approved service lifecycle. Demonstrate real typed artifact handoffs.

**Gate:** each service demonstrates its supported lifecycle and cross-service workflows preserve meaning, evidence and lineage.

### P4 — Agentics orchestration maturity
Connect intent interpretation, planner, knowledge, tool registry, approval, resource policy, execution and artifact-grounded reporting. Add adversarial, prompt-injection, ambiguity, failure and out-of-domain evaluations.

**Gate:** orchestration is policy-controlled, reproducible, auditable and passes the defined adversarial/evaluation suite.

### P5 — Optional scientific models and training
Adopt or train models only when a measured gap justifies them. Complete data/model permission review, manifests, leakage-resistant benchmarks, reproducibility and rollback.

**Gate:** every model release is permission-cleared, versioned, reproducible, benchmarked and reversible. Models remain replaceable components.

### P6 — Controlled discovery and design
Enable bounded novel candidate exploration only after domain-specific risk assessment, safety review, independent verification, resource controls and human/institutional authorization.

**Gate:** separate domain approvals; no autonomous wet-lab, clinical or hazardous action.

### P7 — Generalization, scaling and research evaluation
Evaluate performance beyond training/reference examples, test robustness and operating envelopes, improve recovery/scaling and conduct independent university/research evaluation.

**Gate:** acceptance only for claims supported by independent evidence, replication and stated limitations.

## 15. Scientific foundation subphases

The shared scientific foundation is implemented in this order:

- **SF0:** audit existing repository packages, versions, licenses, adapters and A–N capability gaps.
- **SF1:** typed scientific quantities, dimensions, units and reference systems.
- **SF2:** SKE knowledge/evidence/provenance substrate.
- **SF3:** symbolic and numerical mathematics.
- **SF4:** statistics, uncertainty, experimental design and causal methods.
- **SF5:** selected physics, chemistry, biology and simulation adapters.
- **SF6:** constraints, optimization, graph/geometry/topology and construction primitives.
- **SF7:** A–N integration and independent verification.
- **SF8:** permission-aware knowledge ingestion and model governance.
- **SF9:** Agentics orchestration and adversarial evaluation.

SF0 must precede package additions or model training. The candidate tool catalogue must not be installed wholesale.

## 16. Evaluation framework

Evaluate Agentics across distinct dimensions; never collapse them into a single quality score.

| Dimension | Evaluation focus |
|---|---|
| Knowledge quality | Source reliability, provenance, coverage, contradictions and versioning |
| Reasoning correctness | Derivation validity, assumptions, unit consistency and domain applicability |
| Construction quality | Constraint satisfaction, novelty claims, completeness and reproducibility |
| Verification independence | Method independence, reference quality, invariant coverage and false acceptance |
| Statistical reliability | Calibration, uncertainty, sensitivity, bias and leakage resistance |
| Tool reliability | Correct versions, adapter contracts, resource behavior and failure handling |
| Safety/security | Permission enforcement, sandboxing, egress, adversarial robustness and human gates |
| Workflow integrity | Approval binding, lineage, deterministic replay and failure propagation |
| Generalization | Out-of-domain performance, distribution shift and robustness |
| Scientific validity | Independent reference comparison, replication and experimental evidence where appropriate |

Each evaluation suite records dataset/source version, split strategy, metrics, thresholds, environment, random seed, confidence intervals and known limitations.

## 17. Definition of done for every AI/scientific capability

A capability is not complete until it has:
1. A documented purpose, scope, non-goals and scientific claim boundary.
2. Typed versioned input/output/error contracts.
3. Domain assumptions, units, applicability and constraints.
4. Real implementation with no fake success or placeholder behavior.
5. Provenance for inputs, sources, tools, parameters and outputs.
6. Pre-generation checks where construction is involved.
7. Independent post-generation verification appropriate to the claim.
8. Unit, property, reference, negative, boundary and regression tests.
9. Resource, security, permission and failure controls.
10. Reproducibility and explicit uncertainty/limitations.
11. Documentation, benchmark evidence and exact commit/CI results.
12. Human/domain acceptance where required.

Engineering acceptance does not equal scientific acceptance. University and qualified expert review remains a separate gate.

## 18. Governance and document authority

- This file is the **single authoritative Agentics Molecularis Master Plan**.
- [AI Constitution](../services/ai/AI_CONSTITUTION.md) defines mandatory rules.
- [ENGINE](../services/ai/ENGINE.md) defines technical architecture and implementation responsibilities.
- [RULEBOOK](../services/ai/RULEBOOK.md) defines operational and scientific policy.
- [ACCEPTANCE](../services/ai/ACCEPTANCE.md) defines phase and evidence gates.
- [SCIENTIFIC FOUNDATION](../services/ai/SCIENTIFIC_FOUNDATION.md) maps disciplines and A–N priorities.
- [SCIENTIFIC TOOL REGISTRY](../services/ai/SCIENTIFIC_TOOL_REGISTRY.md) catalogs candidate software and adapter requirements.
- [IMPLEMENTATION ROADMAP](../services/ai/IMPLEMENTATION_ROADMAP.md) decomposes scientific foundation phases into implementation work.
- [WORK BACKLOG](WORK_BACKLOG.md) tracks tasks; [SERVICE STATUS](SERVICE_STATUS.md) records verified state.

Supporting documents may add detail but may not contradict this plan. Material changes require an explicit decision-log entry. Never report planned capabilities as implemented or scientific claims as validated without evidence.
