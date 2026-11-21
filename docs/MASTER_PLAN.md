# Molecularis — Master Product and Engineering Plan

**Plan status:** Active execution blueprint  
**Planning date:** 2026-11-21  
**Product target:** Installed desktop applications first; installed mobile applications next  
**Primary platforms:** Linux, Windows, macOS, Android, iOS/iPadOS  
**Intended use:** Scientific research and education

## 1. Mission and product outcome

Molecularis is a cross-platform scientific research environment for exploring biological and molecular data, running reproducible analyses, inspecting structures, managing research projects and connecting to controlled compute resources.

The first complete product is an installed desktop application for Linux, Windows and macOS. Android and iOS/iPadOS applications follow, sharing the same scientific contracts, project formats, provenance model and product experience. A web companion may be considered later for collaboration or institutional access; it is not a required runtime for core research.

The product must be useful offline for local projects and supported local computations. Network access, remote compute and reference-data retrieval must be explicit, visible and controllable.

## 2. Product principles

1. Scientific correctness before feature count. Every result has a defined method, supported input, units, limitations and evidence state.
2. One coherent product. Shared domain models and contracts; platform-specific adapters only where operating systems require them.
3. Local-first research. Users can create, inspect, save and export local projects without depending on a hosted service.
4. Reproducibility by default. Record inputs, parameters, software versions, data versions, execution environment and output checksums.
5. Incremental delivery. Deliver complete, testable vertical slices; do not attempt a simultaneous rewrite of every capability.
6. Compatibility and data safety. Preserve user projects and stable identifiers through explicit, tested migrations.
7. Security and privacy by design. Least privilege, bounded execution, clear compute location, secure storage and explicit data transfer.
8. Accessibility across devices. Keyboard, pointer, touch, assistive technology, scaling and reduced-motion support are product requirements.
9. Transparent maturity. Distinguish source availability, integration, automated testing, independent validation, platform verification and release approval.
10. Research-use boundary. Clinical diagnosis, treatment, dosing and patient-specific decision support are not authorized product functions.

## 3. Platform and technology strategy

### 3.1 Delivery order

- Desktop release: Linux, Windows and macOS.
- Mobile release: Android and iOS/iPadOS.
- Optional extension: web collaboration or institutional access after installed products are established.

All five operating-system families are architectural targets. Desktop delivery has priority, but decisions must not make mobile implementation prohibitively expensive.

### 3.2 Core languages

- Python: scientific orchestration, research APIs, reference implementations and ecosystem adapters.
- Rust: safe parsing, validation, process supervision, resource controls and security-sensitive native services where justified.
- C++: profiled performance-critical kernels and mature native scientific-library integration.
- SQL and versioned schemas: persistence and language-neutral contracts.

The repository currently has a substantive Python scientific package. Rust and C++ foundations are not yet substantive cross-platform scientific engines. Their adoption must be driven by measured need, working implementations and benchmarks.

### 3.3 UI framework decision

Do not preselect a UI framework. Build a comparable feasibility slice and evaluate candidate approaches on Linux, Windows, macOS, Android and iOS/iPadOS.

Measure native filesystem integration, accessibility, keyboard and touch interaction, offline storage, large-file handling, GPU/3D rendering, mobile lifecycle, background work, packaging, signing, updates, rollback, automated testing, language interoperability, performance, contributor skills and licensing.

Record the measurements, trade-offs, prototype evidence and final architecture decision before committing the product shell to a framework.

## 4. Repository capability baseline

The current capability registry contains 130 entries:

| Registry group | Count | Current recorded state |
|---|---:|---|
| Scientific and technical tools | 68 | Marked implemented |
| UI screens | 26 | Planned |
| UI settings | 22 | Planned |
| Security features | 14 | Planned |
| **Total** | **130** | **68 marked implemented; 62 planned** |

All 68 tool entries marked implemented have declared source paths present in the audited repository snapshot. Their evidence level is currently `none`; this does not establish that each capability is integrated, independently validated, available on every platform or ready for release.

The repository contains a Kotlin/Jetpack Compose Android client, a Python scientific package, API schemas, tests, offline structure-viewer assets, a bounded Vina worker and an OpenMM adapter for caller-prepared systems. The current repository does not establish a completed desktop client, an iOS/iPadOS application, a selected five-platform UI framework or a universal compute supervisor.

The scientific package spans sequence and genome workflows, protein analysis, kinetics, structure parsing and geometry, chemistry, phylogeny, omics, microbiome, PGx research and molecular workflows. Optional tools and runtimes must be detected and declared rather than assumed to be installed.

This baseline is an inventory for planning. Each capability must be checked against its actual contract, runtime dependencies, tests and validation evidence before it is exposed as a supported product feature.

## 5. Target architecture

### 5.1 Product layers

1. Platform applications: desktop and mobile shells, navigation, accessibility, OS integration and platform lifecycle.
2. Shared product domain: projects, datasets, artifacts, workflows, jobs, settings, permissions and user-facing capability metadata.
3. Scientific service layer: typed inputs and outputs, validation, method selection, provenance and capability-specific orchestration.
4. Execution adapters: Python, Rust, C++ and approved external scientific engines behind stable interfaces.
5. Data and project layer: portable project format, versioned schemas, content checksums, atomic persistence, import/export and migration.
6. Compute layer: local execution first, optional paired Molecularis Node, and separately governed institutional or hosted execution.
7. Evidence and governance layer: tests, reference datasets, benchmarks, security controls, licences, validation records and release decisions.

### 5.2 Project and data model

Define versioned, platform-neutral contracts for projects, datasets, scientific objects, artifacts, workflows, jobs, engine manifests and provenance.

The project system must support create, open, save, autosave where safe, import, export, integrity verification, backup, restore and recovery from interrupted writes. It must use explicit schema versions, checksums and atomic updates.

Scientific data models must make sequence alphabets, residue and atom identifiers, coordinate frames, units, missing values, reference builds and dataset provenance explicit. Do not rely on display labels or implicit conventions as data contracts.

### 5.3 Job and compute model

Every job has a declared capability, validated inputs, execution profile, resource limits, cancellation semantics, progress/log stream, durable state and provenance record.

Local execution is preferred when supported. A remote node is optional and must be paired, authenticated, revocable and limited to explicitly enabled capabilities. Hosted and HPC execution require separate deployment, identity, data-transfer and governance controls.

No privileged API or worker may provide unrestricted shell execution or arbitrary executable selection. Treat imported workflows, data packs and engine outputs as untrusted.

### 5.4 Visualization

Keep visualization separate from scientific computation and validation. A viewer renders supplied data; it does not certify structural quality, binding, function or biological significance.

Evaluate the existing offline viewer assets and suitable upstream components, including Mol*, through component-level compatibility, licence, performance and accessibility tests. Large structures and complex scenes require measured memory, rendering and interaction targets.

### 5.5 Core-engine-first, rule-driven scientific creation

**Owner direction:** Molecularis is to become an independent scientific creation platform across *all* scientific domains and projects in scope—not a collection of wrappers that depend on third-party databases or hosted services to produce answers. The upstream scientific projects named in the integration inventory are foundations from which Molecularis may learn, adapt, benchmark or selectively reuse computational engines and algorithms. They do not define Molecularis' product architecture, scientific semantics or long-term dependency model.

The intended development sequence is:

1. **Extract/adapt core computational capability:** inspect upstream source, methods, interfaces, build requirements and licences; identify the useful algorithms, numerical kernels, parsers, simulation engines, inference runtimes and validation methods. Reuse or adapt only where technically and legally permitted, preserving required notices and attribution. Do not copy upstream code wholesale or assume that source-code rights include model weights, parameter sets or datasets.
2. **Build Molecularis-owned core engines:** place selected capabilities behind Molecularis-owned, versioned interfaces and portable scientific data contracts. Keep upstream implementations replaceable. Where an upstream model is learned or requires specialized parameterization, treat the model and its weights as an optional inference capability; do not misrepresent it as a hand-written rule or claim equivalent capability without independent evidence.
3. **Build the Molecularis scientific framework:** establish common representations for scientific entities, units, coordinate systems, constraints, objectives, transformations, uncertainty, execution and provenance across every supported domain.
4. **Build the Molecularis rule and method system:** provide authoring, versioning, composition, review and testing of domain rules, equations, physical models, chemical constraints, algorithms, boundary conditions and optimization objectives. Rules must be explicit, traceable and scoped; they must not be invented or promoted to scientific fact without domain evidence and review.
5. **Generate scientific artifacts from requirements:** use the framework, rules and core engines to construct candidate sequences, molecular graphs, 3D structures, conformations, simulations, analyses and other outputs according to user-defined goals and constraints.
6. **Validate independently:** evaluate generated outputs with separate validators, numerical checks, reference methods, benchmarks and—where appropriate—experimental evidence. A generator must not be its own sole validator. Passing computational constraints does not prove experimental truth, biological function or clinical validity.

The product must support both **generation** and **analysis of imported material**. Reference datasets, genome assemblies, templates, model weights, force-field parameters and other data resources may still be necessary for particular methods; they are explicit, versioned, user-controlled inputs or optional resources—not a universal prerequisite or the source of Molecularis' scientific logic. A method that genuinely requires such resources must declare exactly which resources it needs and why.

This direction applies to every project/domain in the Molecularis scope, including sequence and genomics, proteins, structural biology, chemistry, molecular dynamics, DNA/RNA design and thermodynamics, omics, phylogeny and future scientific domains. No individual upstream tool is to become a mandatory dependency of the whole application.

**Architecture consequences:**
- Define Molecularis-owned interfaces and canonical data contracts before expanding engine integrations.
- Separate rule specifications, rule execution, candidate generation, optimization, validation, visualization and provenance.
- Keep third-party engines as optional adapters or replaceable backends; prefer native Molecularis implementations when justified by capability, correctness, licensing and maintenance evidence.
- Track upstream code, algorithms, models, weights, parameter sets and datasets as distinct dependency/licensing objects.
- Record for every generated artifact the requirements, rulebook versions, method/engine versions, parameters, seeds, resource manifests, execution environment, validation results and limitations.
- Never equate a generated 3D model with a physically stable or experimentally confirmed structure; report what was computed and what remains unverified.

## 6. Execution roadmap

Phases are dependency gates, not calendar promises. Each phase is planned, implemented, tested and reviewed against explicit exit criteria.

### Phase 0 — Repository and operational baseline

**Objective:** establish a trustworthy implementation and migration ledger.

Work:
- Run the full CI and test matrix on exact commit SHAs; record failures and environment constraints.
- Inspect all 130 registry entries and reconcile identifiers, source paths, imports, optional dependencies, tests and actual runtime behaviour.
- Add explicit per-capability test references and evidence records.
- Inventory Android persistence and operating-system integration: databases, schemas, preference keys, file locations, WorkManager identifiers, keystore aliases, encryption contracts, caches, backups, exports and project identifiers.
- Create representative data fixtures and migration/rollback test plans.
- Record upstream dependencies, exact versions, licences, notices, model/data terms and software bill of materials.
- Classify each repository component for reuse, extraction, adaptation, replacement or deferral.

**Exit criteria:** reviewed source inventory, capability evidence ledger, Android data/identifier inventory, dependency-rights register, exact-SHA CI report and migration risk register.

### Phase 1 — Five-platform application feasibility

**Objective:** select the application framework through measured evidence.

Work:
- Build the same small project-browser and data-inspection prototype for Linux, Windows, macOS, Android and iOS/iPadOS.
- Evaluate credible native and cross-platform candidates against the criteria in Section 3.3.
- Exercise filesystem access, offline persistence, accessibility, keyboard/pointer/touch input, graphics, background lifecycle, packaging and update flows.
- Verify integration options for Python, Rust and C++ without creating duplicated business logic.

**Exit criteria:** reproducible prototypes, comparison report, identified risks, contributor/toolchain plan and an approved architecture decision.

### Phase 2 — Shared contracts and project foundation

**Objective:** create the data and execution foundations used by every client.

Work:
- Define and version project, dataset, artifact, provenance, capability, engine, workflow and job contracts.
- Define stable cross-language interfaces and compatibility rules.
- Implement project create/open/save/import/export and integrity verification.
- Add atomic writes, backup/restore, interrupted-write recovery and schema migration fixtures.
- Establish canonical sequence, molecule, structure, coordinate and unit conventions.
- Add contract tests that run across supported language boundaries.

**Exit criteria:** round-trip project tests, migration compatibility tests, corruption/recovery tests, deterministic provenance and shared contract conformance.

### Phase 3 — Desktop application foundation

**Objective:** deliver the first installable Molecularis desktop application.

Work:
- Build the desktop shell for Linux, Windows and macOS using the selected framework.
- Implement workspace navigation, project management, settings, file import/export and offline state.
- Implement job lifecycle, local process supervision, logs, cancellation, resource limits and recovery.
- Establish update, signing, packaging, uninstall and rollback procedures.
- Integrate one complete scientific vertical slice selected from repository evidence and user value.

**Exit criteria:** installable desktop packages, tested on all three desktop operating systems; offline project workflow; durable job lifecycle; accessible core navigation; and one end-to-end scientific workflow with reproducible outputs.

### Phase 4 — Scientific service delivery

**Objective:** turn repository capabilities into dependable, user-facing scientific workflows.

**Core-engine and rule-framework requirement:** All service work in this phase must follow Section 5.5. For each domain, first identify the reusable computational kernel(s), then define the Molecularis-owned contracts and rule specifications, then implement generation/analysis workflows and independent validation. Do not make third-party database retrieval the default product behavior. Explicitly document when a specific algorithm requires a reference assembly, template, model weights, force-field parameters or other external resource.

The initial engine inventory includes the named upstream projects recorded in the scientific integration register (including Biopython, Biotite, Parasail, pysam/HTSlib, Samtools, BCFtools, ESM, AlphaFold, Mol*, MolProbity, RDKit, AutoDock Vina, OpenMM, GROMACS, SciPy, NUAD, NUPACK and Galaxy). This is an inventory of candidate capabilities, not a commitment to embed every project or redistribute its assets. Galaxy is an optional external workflow interoperability target; it is not a required core scientific engine.

Recommended order, subject to Phase 0 evidence and dependency readiness:

1. Sequence and genome foundation: FASTA/FASTQ, sequence QC, translation, ORF candidate analysis, local alignment, annotation and reference-pack handling.
2. Kinetics and quantitative research: Michaelis–Menten fitting, transformations, uncertainty summaries, diagnostics and independently checked reference cases.
3. Structure data and inspection: PDB/mmCIF ingestion, identity and coordinate handling, deterministic viewer payloads, selection, representations and large-structure performance.
4. Structure analysis: sequence/structure mapping, geometry, interfaces, pockets and quality observations with method-specific limitations.
5. Chemistry: SDF ingestion, graph validation, stereochemistry and pinned RDKit profiles.
6. Docking: complete ligand/receptor preparation, bounded Vina execution, result inspection, provenance and redocking/decoy reference evaluation.
7. Molecular dynamics: trusted system preparation, topology and force-field provenance, OpenMM setup, simulation and analysis.
8. Phylogeny and omics: input validation, statistical assumptions, reference fixtures, uncertainty and calibrated interpretation.
9. PGx research workflows: source-pinned definitions, conservative matching, abstention and strict research-only presentation.
10. Advanced research workflows: protein modelling, multi-omics, microbiome, molecular design and specialist domains after data rights, dependency, compute, uncertainty and safety review.

Each service is delivered as a vertical slice: import → validation → configuration → execution → result inspection → export → provenance. A source module or registry entry alone is not a user-facing service.

**Exit criteria for each service:** typed contracts, declared units and conventions, pinned method/dependency versions, automated tests, independent reference or benchmark evidence, limitations, provenance, security review and explicit platform support.

### Phase 5 — Visualization and research workspace

**Objective:** provide coherent ways to inspect, compare and communicate results.

Work:
- Integrate supported sequence, alignment, phylogenetic, kinetics, chemistry and structure views.
- Implement synchronized selection and linked views only where stable identifiers support them.
- Provide result tables, plots, filters, annotations and exportable figures.
- Preserve source data and analysis provenance when users annotate or transform results.
- Add accessibility, large-data performance and deterministic session export tests.

**Exit criteria:** reproducible visualization sessions, supported-format coverage, accessibility checks and performance evidence on target hardware.

### Phase 6 — Compute services and extensibility

**Objective:** expand execution safely beyond the local machine.

Work:
- Define a versioned Molecularis Node protocol and explicit capability allowlist.
- Add secure pairing, identity, revocation, authentication, authorization, quotas, cancellation and audit logs.
- Add isolated engine profiles one at a time with pinned environments and verified data/model rights.
- Add institutional/HPC adapters only for workloads with demonstrated requirements.
- Define artifact transfer, interrupted-job recovery and compute-location disclosure.

**Exit criteria:** threat model and security review, resource-exhaustion tests, recovery exercises, job conformance, provenance completeness and operational documentation.

### Phase 7 — Mobile applications

**Objective:** deliver Android and iOS/iPadOS clients on shared product foundations.

Work:
- Implement the mobile shells and platform adapters using the shared domain contracts.
- Port complete workflows based on user value and mobile hardware constraints.
- Preserve Android project access and existing user data throughout migration.
- Implement explicit migration, export/import, integrity verification, backup/restore and rollback.
- Test permissions, secure storage, background lifecycle, offline operation, battery, graphics, touch and accessibility.
- Establish iOS/iPadOS signing, packaging, update and recovery procedures.

**Exit criteria:** install/upgrade tests on supported devices, successful data migration and rollback, offline workflows, accessibility checks and scientific parity evidence for each shipped capability.

### Phase 8 — Institutional readiness and release operations

**Objective:** make releases supportable, auditable and maintainable.

Work:
- Complete SBOM, licence and third-party notice review.
- Complete privacy, security, accessibility and threat-model reviews.
- Establish supported OS versions, hardware profiles, performance budgets and compatibility policy.
- Test backup/restore, disaster recovery, update rollback and incident response.
- Establish release signing, reproducible builds, release notes and evidence retention.
- Obtain independent scientific review for capabilities making scientific claims.

**Exit criteria:** versioned release record with approved scope, exact build provenance, passing required CI, platform evidence, security/licence review, scientific evidence and documented known limitations.

## 7. Scientific capability and evidence policy

Every capability record must include:
- stable capability ID and intended research use;
- input/output schema, units, coordinate or reference conventions;
- algorithm/method, implementation and dependency versions;
- required optional tools, data packs, models and hardware;
- provenance and deterministic/reproducibility expectations;
- known limitations, uncertainty and abstention behaviour;
- automated test references and independent reference/benchmark evidence;
- supported operating systems and execution profiles;
- security classification, data rights and reviewer/owner decision.

Use separate implementation and evidence states:

**Implementation:** not started → prototype → partial → integrated → deprecated.

**Evidence:** E0 planned → E1 source/method reviewed → E2 contract/adapter verified → E3 automated tests pass → E4 independent reference and target-platform validation pass → E5 independent domain review and release approval.

A capability may not be described as scientifically validated, production-ready or platform-supported without the corresponding evidence. Registry status must be updated from actual results, not from roadmap intent.

## 8. Security, privacy, licensing and safety

- Research-use only. No diagnosis, treatment, dosing or patient-specific decision support.
- Clinical Decision Support remains disabled unless separately authorized and independently validated under applicable governance.
- Do not place patient-derived or confidential research data in public repositories, fixtures, CI logs or public artifacts.
- Encrypt sensitive local data where appropriate and document key handling, recovery and data-loss implications.
- Make all network transfers, remote execution and reference-data retrieval visible and user-controlled.
- Apply least privilege, process isolation, bounded inputs, bounded memory/CPU/time, safe archive handling and dependency pinning.
- Review code, models, datasets, fonts, icons, viewer assets and documentation for their individual licence and redistribution terms.
- Preserve uncertainty and abstention; never convert a screening result into an unsupported biological conclusion.

## 9. Delivery governance

- For the owner-directed implementation work in this project, commit authorized changes directly to `CORE`; do not create feature branches or pull requests unless the owner explicitly changes this instruction.
- Before each write, read the current `CORE` file/blob SHA and use it for updates. Verify the resulting file and commit on `CORE`.
- Do not force-reset the branch, rewrite shared history, or silently change persisted identifiers and public contracts.
- Each implementation change records scope, baseline SHA, compatibility impact, tests actually run, evidence, risks and rollback strategy.
- Update implementation, tests, schemas, registry entries, dependency/licence records and evidence records together where applicable.
- Keep platform support and scientific validation as explicit per-capability states.
- Check exact-commit CI after meaningful implementation batches. A pending, skipped or unrun test is not a pass.
- Plan milestones from dependency evidence and demonstrated capacity, not optimistic calendar dates.

## 10. Definition of done

A feature or release is complete only when all applicable conditions are met:

1. User-visible workflow and documented contract are implemented.
2. Exact-head CI and required automated tests pass.
3. Inputs, outputs, units, dependencies and limitations are explicit.
4. Data migration and backward compatibility are tested where applicable.
5. Security, privacy and licensing requirements are reviewed.
6. Scientific reference/benchmark validation is complete where scientific claims are made.
7. Supported-platform installation and runtime evidence is recorded.
8. Accessibility, performance and offline behaviour meet declared requirements.
9. Provenance, export, recovery and rollback work as specified.
10. Known issues and residual risks are documented and accepted by the responsible reviewer.

## 11. Immediate execution priorities

1. Complete the exact-commit repository and capability evidence ledger.
2. Complete the Android persisted-data and identifier inventory before any migration work.
3. Run the five-platform framework feasibility spike and record the decision.
4. Define shared project, artifact, provenance and job contracts.
5. Build the desktop project shell and local job lifecycle.
6. Select the first scientific vertical slice using implementation quality, user value, reference data and validation cost.
7. Deliver the selected workflow end-to-end before expanding the service catalogue.
8. Establish continuous security, accessibility, licence and scientific-evidence gates from the first release candidate.
9. Define Molecularis-owned scientific object/constraint contracts, a rule-authoring and versioning model, candidate-generation interfaces and independent validation interfaces; apply this foundation across every scientific domain.
10. For each upstream project, record the extractable computational capability separately from code, model-weight, parameter and dataset rights; keep adapters optional and replaceable.

**Product success is a dependable, reproducible scientific research application across desktop and mobile—not a count of screens, source files or registry entries.**


## 12. Complete scientific product scope

Molecularis is intended to cover all scientific project families in its approved scope. These are product domains, not separate apps with unrelated data models. They share projects, artifacts, rules, jobs, provenance, visualization and validation infrastructure.

| Domain | Scientific work to support | Generated or analyzed artifacts |
|---|---|---|
| Sequence science | Parsing, QC, alignment, translation, motifs, ORFs, sequence design | Sequences, alignments, annotations, reports |
| Genomics and variant science | Read processing, reference mapping, variant representation, normalization and QC | BAM/CRAM/VCF/BCF outputs, variant sets, QC reports |
| Protein science | Sequence properties, embeddings, prediction, design and comparison | Protein sequences, feature vectors, candidate structures and confidence reports |
| Structural biology | Structure parsing, construction, geometry, alignment, validation and visualization | PDB/mmCIF-like structures, coordinate models, validation reports and 3D scenes |
| Chemistry and molecular design | Molecular graphs, valence/stereochemistry checks, conformers, descriptors and candidate generation | Molecular graphs, conformers, SDF-like artifacts and property reports |
| Docking and interaction analysis | Ligand/receptor preparation, docking, pose ranking and interaction analysis | Prepared systems, poses, scores and interaction reports |
| Molecular dynamics | System construction, parameterization, minimization, equilibration, simulation and trajectory analysis | Topologies, coordinate sets, trajectories, energies and analysis artifacts |
| DNA/RNA design and thermodynamics | Sequence design, base-pairing constraints, folding, complexes, ensembles and optimization | Designed strands, structures, complexes, thermodynamic predictions |
| Kinetics and quantitative biology | Model specification, fitting, diagnostics, sensitivity and uncertainty | Equations, fitted parameters, plots, residuals and reports |
| Phylogeny and evolution | Sequence comparison, tree construction, support and visualization | Alignments, trees, support statistics and figures |
| Omics and microbiome | QC, normalization, statistical analysis, feature comparison and reproducible workflows | Matrices, differential analyses, community profiles and reports |
| Pharmacology/PK-PD and PGx research | Model-based research, genotype/phenotype data analysis, curated interpretation and uncertainty | Research models, cohort summaries and evidence-linked reports |
| General scientific computing | Numerical methods, optimization, statistics, unit conversion and reusable computation | Reproducible numerical results, plots and data artifacts |
| Workflow interoperability | Reproducible pipelines, external workflow submission and result import | Workflow definitions, job manifests, logs and result bundles |

Domain breadth does not imply simultaneous implementation. Each domain is enabled only when its contracts, rulebooks, generation/analysis methods, validation evidence and target-platform execution are ready. The same scientific object must have the same meaning across desktop and mobile clients.

## 13. Upstream engine strategy and complete integration inventory

The named upstream projects are candidate sources of computational capability. Molecularis must inspect and selectively adapt their useful algorithms, methods, numerical kernels, parsers, inference runtimes, simulation engines and validators. The goal is to build Molecularis-owned core engines and contracts, then build the unified rule framework and scientific generators on top.

| Upstream project | Capability to study/adapt | Molecularis-owned capability built around it | Important boundary |
|---|---|---|---|
| Biopython | Sequence parsing, alignment and biological data utilities | Canonical sequence objects, parsers, analysis and rule interfaces | Preserve format semantics and licensing; do not assume every module is required |
| Biotite | Sequence/structure algorithms and structural file handling | Structure/sequence model adapters and geometry services | Keep optional; verify Python/runtime compatibility |
| Parasail | SIMD pairwise alignment kernels | Versioned alignment service and common result schema | Check saturation, scoring matrices, gap conventions and traceback correctness |
| pysam | Python interface to HTSlib data access | Read/alignment I/O adapter and streaming contracts | Preserve header, tags, read groups and indexing semantics |
| HTSlib | Native SAM/BAM/CRAM/VCF/BCF primitives | Native genomics I/O boundary and format interoperability | Track bundled notices and format/version compatibility |
| Samtools | Read inspection, sorting, indexing and statistics | Genomics processing operations with safe process/resource controls | Explicit executable/version, bounded execution and output verification |
| BCFtools | Variant parsing, normalization, filtering and statistics | Variant transformation and validation services | Reference build and normalization parameters must be explicit |
| ESM | Learned protein representations and model inference | Optional protein embedding/prediction engine contract | Model architecture, weights, tokenization and model terms are separate from source code |
| AlphaFold | Learned protein structure prediction pipeline | Optional protein structure inference backend and output adapter | Requires model weights and often large reference resources/compute; no equivalence claim without evidence |
| Mol* | 3D molecular/biological visualization | Molecularis-owned visualization data contract and cross-platform viewer integration | Rendering is not scientific validation; audit component and asset licences |
| MolProbity | Structural geometry and stereochemical validation methods | Independent structure validation service | Establish exact toolchain, dependencies, input preparation and licences |
| RDKit | Cheminformatics graph, sanitization, stereochemistry and conformer algorithms | Canonical chemistry graph and molecular design services | Pin versions; do not deserialize untrusted pickle payloads |
| AutoDock Vina | Docking search/scoring engine | Docking job contract, pose handling and independent benchmark workflow | Score is not experimental binding affinity; preparation is a separate responsibility |
| OpenMM | Molecular mechanics and molecular dynamics execution | Simulation system/job/trajectory contracts and analysis services | Caller-prepared systems are not a complete preparation pipeline; force-field terms/parameters matter |
| GROMACS | Molecular dynamics and trajectory processing | Optional simulation backend using the common system/job model | Prepared topology/TPR and force-field compatibility must be explicit |
| SciPy | Numerical optimization, statistics and scientific algorithms | Reference methods and selected numerical services | Optional dependency; pin algorithm settings and compare numerical behavior |
| NUAD | DNA design/search/optimization methods | Molecularis nucleic-acid candidate generator | Confirm canonical source, API, assumptions and licence before adaptation |
| NUPACK | Nucleic-acid thermodynamics, folding and complex analysis | Optional thermodynamic evaluation backend and common output schema | Verify access/distribution terms and model/parameter semantics |
| Galaxy | Workflow execution and interoperability | Optional external workflow connector | Not a core scientific engine or mandatory service; secure external server integration only |

The inventory has 19 named upstream projects; pysam and HTSlib are treated as one paired integration stack in the 18-stack planning count. The inventory is not a promise to bundle every tool, model, binary, database or parameter set. For each project, the integration register must distinguish:
- source code and source licence;
- compiled binaries and redistribution terms;
- model architecture and model-weight terms;
- parameter sets and force-field terms;
- reference databases and dataset terms;
- trademarks, notices, citation requirements and attribution;
- supported versions, operating systems, hardware and known limitations.

**Adaptation rule:** first extract the scientific behavior and contracts needed by Molecularis; then decide whether to reuse a library, wrap an executable, port a narrow algorithm, implement an independent method or defer the capability. Never copy an entire upstream application merely to claim integration. Never infer rights to weights or datasets from an open-source code licence.

## 14. Scientific framework, rules and generation architecture

The scientific framework is a first-class product subsystem, not a set of scattered hard-coded checks.

### 14.1 Scientific object model

Define canonical, versioned representations for:
- sequences, residues, chains, reads, variants, annotations and coordinate systems;
- atoms, bonds, charges, stereochemistry, conformers, molecules and assemblies;
- structures, models, coordinate frames, transforms, periodic boxes and topology;
- physical quantities, dimensional units, uncertainty, distributions and numerical precision;
- design goals, constraints, objectives, candidate sets, optimization traces and feasibility states;
- workflows, methods, engines, resources, artifacts, validation findings and provenance.

Preserve source identifiers and raw source values alongside normalized values. All transforms must declare coordinate, unit and convention changes. No lossy conversion may occur silently.

### 14.2 Rule package model

Each rule package must declare:
- stable ID, semantic version, domain and intended use;
- author, reviewer, source references and approval state;
- scientific definition, rationale, assumptions and applicability domain;
- typed inputs/outputs, units, coordinate/reference conventions and preconditions;
- equations, algorithms, constraints, tolerances and numerical settings;
- dependencies, optional resources and execution requirements;
- failure/abstention behavior, known limitations and uncertainty semantics;
- positive, negative, boundary, adversarial and regression tests;
- compatibility and migration policy.

Rules can be declarative where practical. Executable extensions must run in a constrained environment with explicit capabilities, resource limits and no implicit network or filesystem authority. Unreviewed user rules remain private/untrusted until reviewed; rule execution must never silently elevate their trust level.

### 14.3 Rule lifecycle and governance

Rule lifecycle: proposed → authored → technically implemented → tested → independently reviewed → approved for a declared scope → versioned/released → superseded/retired. Record who authored, implemented, reviewed and approved each rule. Changes to equations, thresholds, units, assumptions or applicability require version changes and regression evidence.

A rule can be valid for one scope and invalid for another. The framework must support explicit applicability ranges and abstain when inputs are outside them. Conflicting rules must be reported and resolved through declared precedence or a domain-reviewed composition policy, never hidden by arbitrary execution order.

### 14.4 Generation and inverse-design loop

A generic generation workflow is:

1. Parse a user's scientific goal into a typed specification.
2. Check feasibility, required inputs and applicability of selected rule packages.
3. Construct candidate representations using domain-specific generators.
4. Evaluate hard constraints and reject invalid candidates with traceable reasons.
5. Score/optimize feasible candidates using declared objective functions and uncertainty-aware methods.
6. Optionally refine candidates with physics-based simulation or learned inference where justified.
7. Validate finalists using independent methods.
8. Present alternatives, trade-offs, unsatisfied constraints and uncertainty.
9. Save the artifact, rule/model/resource manifest and complete provenance.

The engine must distinguish hard constraints from soft objectives, and deterministic rules from stochastic search. It must record random seeds, stopping conditions, search budgets and numerical tolerances. It must report when a search is incomplete or no feasible candidate was found; it must not fabricate a result to satisfy the request.

### 14.5 3D construction and geometry

3D generation is not just rendering. A generated model must include typed entities, connectivity/topology, coordinate units and frame, stereochemistry where relevant, constraints and provenance. Geometry construction, energy minimization, conformational search, learned structure inference and visualization are separate operations.

A structure may be:
- a schematic or idealized geometry;
- a rule-constructed candidate;
- a minimized/optimized computational model;
- a model predicted by a learned method;
- an experimentally derived structure;
- a hybrid/refined model.

The UI and export metadata must preserve this distinction. Do not label an idealized or generated structure as experimentally confirmed or physically stable without supporting evidence.

### 14.6 Independent validation

Every generator has an independent validation contract. Validation should use a different method or implementation where practical and include invariant checks, reference comparisons, numerical diagnostics and experimental evidence when available. Validation results must state exactly which properties were checked, thresholds, method versions and limitations. A valid file, a geometrically plausible model and a scientifically correct model are different claims.

## 15. Reference data, models and parameter-resource policy

Molecularis is not to be designed as a database lookup product. Its primary scientific behavior comes from Molecularis-owned rules, algorithms, generators and execution engines. However, some scientific methods inherently require reference information or trained parameters. The correct policy is **no universal database dependency**, not a claim that every method can operate without any external resource.

Classify resources as:
1. **Core rules and algorithms:** versioned Molecularis-owned definitions and implementations; included with the application when licensing and size permit.
2. **Optional reference resources:** genome assemblies, annotations, templates, chemical dictionaries or curated reference sets; downloaded/imported only when a selected method requires them.
3. **Model weights:** separately licensed and versioned artifacts for learned inference; never assumed to be covered by model source-code licensing.
4. **Physical parameter sets:** force fields, bonded/non-bonded parameters, thermodynamic tables and calibration constants; method-specific and provenance-tracked.
5. **User-provided resources:** local files or institutional resources with user-controlled paths, permissions and provenance.
6. **Generated artifacts:** outputs created by Molecularis; stored in project packages with checksums and complete generation provenance.

For every resource, record origin, version, checksum, licence/terms, date, compatibility, required method and whether it is redistributable. Do not silently download or update resources during a scientific job. Explain when a resource is required, what capability it enables and what alternatives exist. Where a method cannot operate without a reference, fail clearly rather than substituting an unverified default.

## 16. User experience and primary workflows

The UI is organized around research projects and tasks, not around a catalogue of third-party tool names.

### 16.1 Core workspace areas

- **Home/workspaces:** recent projects, new project, recovery and local/remote compute status.
- **Project explorer:** scientific objects, datasets, generated artifacts, workflows and provenance.
- **Design studio:** goal/specification entry, rule selection, constraints, candidate generation and optimization.
- **Analysis studio:** imported data inspection, method selection, execution and result comparison.
- **Structure studio:** 2D/3D molecular and macromolecular inspection, selection, geometry and validation findings.
- **Simulation studio:** system setup, parameter manifests, job controls, trajectories and numerical diagnostics.
- **Rulebook studio:** browse, author, test, compare, version and review scientific rule packages.
- **Workflow studio:** compose local methods and optional external workflows with typed inputs/outputs.
- **Results and reports:** tables, plots, validation findings, uncertainty, provenance and export.
- **Settings and governance:** storage, compute, privacy, data resources, licences, accessibility and diagnostics.

### 16.2 End-to-end task flow

Every major scientific task follows a consistent flow: choose/create project → describe goal or import input → validate and normalize → choose method/rules/resources → preview cost and execution location → run/cancel/monitor → inspect candidate/result → independently validate → compare alternatives → save/export with provenance.

Do not require users to understand upstream library names. Show the method, its scientific assumptions and the engine used in an expandable technical details view.

### 16.3 Design and accessibility

The application must support keyboard-only operation, screen readers, high-contrast and scalable layouts, pointer and touch, reduced motion, clear error recovery and accessible scientific charts. Complex 3D interactions must have keyboard-accessible alternatives and textual/structured result views. Never communicate scientific quality only through color.

## 17. Cross-platform runtime and deployment matrix

Platform support is capability-specific. The UI may exist on a platform while a compute engine is unavailable there; the UI must communicate that distinction.

| Platform | Primary role | Execution expectations |
|---|---|---|
| Linux desktop | First-class research workstation | Broad local CPU/GPU/native execution subject to tested engine profiles |
| Windows desktop | First-class research workstation | Local execution for supported profiles; documented native toolchain and GPU limits |
| macOS desktop | First-class research workstation | Local CPU/GPU profiles supported by measured compatibility; no assumption of CUDA |
| Android | Mobile research client | Project management, inspection, lightweight local analysis and explicitly supported native tasks; heavy work may use paired node |
| iOS/iPadOS | Mobile research client | Project management, inspection, lightweight local analysis and explicitly supported native tasks; heavy work may use paired node |
| Molecularis Node | Optional user-controlled compute extension | Isolated, allowlisted engine profiles with pairing, quotas, authentication and provenance |
| Institutional/HPC | Optional governed extension | Site-specific deployment, identity, scheduler, storage and data-governance integration |

The selected application framework must not dictate scientific semantics. Scientific contracts and project files remain portable. Build and release pipelines must separately test each OS, CPU architecture, GPU/runtime combination and engine profile claimed as supported.

## 18. Engineering quality, testing and scientific verification

Use layered verification; no single test suite proves all product claims.

- **Static and contract checks:** type checking, linting, schema validation, API compatibility and dependency-policy checks.
- **Unit tests:** parsers, validators, rule evaluation, numerical kernels, serializers and error semantics.
- **Property and fuzz tests:** malformed scientific files, parser boundaries, coordinate transforms, units, numerical extremes and archive handling.
- **Golden/regression fixtures:** versioned non-sensitive data with checksums and documented expected results.
- **Differential testing:** compare selected outputs with independent implementations such as upstream tools, while documenting method differences.
- **Scientific benchmarks:** curated cases with known provenance, expected ranges, tolerances and domain review.
- **Generation tests:** feasibility, constraint satisfaction, candidate diversity, deterministic seeds, search-limit behavior and failure-to-find behavior.
- **3D tests:** topology/coordinate consistency, stereochemistry, geometry, serialization round-trip, rendering fidelity and large-scene performance.
- **Simulation tests:** conservation/energy diagnostics where applicable, integration stability, unit correctness, reproducibility limits and reference systems.
- **Integration tests:** complete user workflows from project input through output, export and provenance.
- **Platform tests:** installation, upgrades, offline behavior, filesystem permissions, background lifecycle, GPU/graphics and accessibility on each claimed OS.
- **Security tests:** sandbox escape attempts, malicious archives/files, path traversal, symlinks, process exhaustion, dependency compromise and secret leakage.
- **Release tests:** reproducible build metadata, signing, SBOM, notices, rollback and recovery.

Tests must never contain patient-identifiable or confidential institutional data. Test data must have documented rights and provenance. A benchmark comparison is not proof of general scientific validity; report its domain and limitations.

## 19. Performance, reliability and resource management

Each capability declares a resource profile: expected input sizes, CPU threads, memory, GPU/VRAM, disk scratch, network needs, expected runtime, cancellation support and output size. Profiles are estimates until benchmarked on named hardware.

The job supervisor must enforce per-job and aggregate quotas, process isolation, bounded logs, scratch-space cleanup, cancellation, timeouts, crash recovery and fair scheduling. Long-running jobs must survive application restart through durable job state where the execution backend permits it.

Performance targets are established from representative workloads and named hardware tiers, not guessed globally. Measure startup, project open/save, large-file import, sequence throughput, structure rendering, memory growth, job launch/cancel, simulation throughput and battery/thermal behavior on mobile.

## 20. Data portability, backup and collaboration

A Molecularis project must be portable and inspectable without requiring a live Molecularis server. Define a documented package format with:
- manifest and schema version;
- scientific objects and artifact references;
- source/input checksums;
- rule, engine, model and resource manifests;
- job/workflow records and provenance;
- user annotations and presentation state;
- optional embedded resources with licence/size warnings.

Support directory-based and packaged projects where appropriate. Provide import preview, path remapping, collision handling, schema migration, integrity verification and export validation. Backups must be restorable and tested. Collaboration/synchronization is deferred until conflict resolution, identity, encryption, permissions and offline merge semantics are designed; do not imply multi-user collaboration from file sharing alone.

## 21. Documentation, support and scientific communication

Maintain:
- user guides for project, design, analysis, structure, simulation and rulebook workflows;
- developer guides for contracts, engine adapters, rule packages, plugins and build environments;
- scientific method cards describing equations, assumptions, units, applicability and limitations;
- engine integration records with upstream version, source, licence and adaptation notes;
- platform compatibility and hardware matrices;
- release notes, migration guides and known-issues records;
- reproducibility/export guidance and citation instructions.

Scientific reports must distinguish inputs, methods, computed observations, predictions, assumptions, validation findings and interpretations. Do not present a confidence score without defining what it measures and how it was calibrated.

## 22. Risk register and mitigations

| Risk | Consequence | Required mitigation |
|---|---|---|
| Over-broad scope | Many partial features and no dependable product | Deliver vertical slices; gate domains on evidence |
| Upstream coupling | Architecture becomes difficult to replace or port | Molecularis-owned contracts; optional adapters |
| Licence/model/data ambiguity | Redistribution or use may be unlawful | Separate rights review for code, weights, parameters and datasets |
| Rules encode unsupported assumptions | Plausible but incorrect generated artifacts | Domain review, applicability bounds, independent validation |
| Generator validates itself | False confidence | Separate validators and differential/reference checks |
| Reference-data dependence | Hidden downloads, stale results or privacy exposure | Explicit resource manifests and user-controlled acquisition |
| Learned model overclaim | Misleading predictions or false certainty | Model provenance, calibration, scope limits and abstention |
| 3D visual plausibility bias | Rendered model mistaken for physical truth | Label model origin and validation state in UI and exports |
| Native dependency fragmentation | Builds fail across OS/CPU/GPU | Reproducible profiles, compatibility matrix and CI |
| Mobile resource limits | Crashes, battery drain and poor experience | Capability-specific mobile profiles and optional paired node |
| Unsafe imported files/workflows | Code execution, data loss or resource exhaustion | Sandboxing, safe parsers, quotas and explicit permissions |
| Data migration failure | Loss of existing Android user projects | Inventory, backups, round-trip tests and rollback |
| Premature clinical positioning | Regulatory, ethical and user harm | Research-only scope and separate authorization/evidence gates |
| Unverified CI claims | False release confidence | Exact-SHA CI records and transparent status |

## 23. Open architecture decisions and decision gates

The following must be decided through evidence and recorded in the decision log; this plan does not silently choose them:
- five-platform UI framework and rendering stack;
- language-neutral ABI/IPC contract details and where Rust/C++ boundaries are justified;
- project package/container format and encryption model;
- rule representation/DSL and safe execution model;
- plugin/engine packaging and environment isolation mechanism;
- supported local GPU APIs and per-engine accelerator matrix;
- desktop update/signing/distribution channels and mobile store strategy;
- synchronization/collaboration scope and conflict semantics;
- exact initial domain vertical slice after capability and validation audit;
- per-engine upstream version pins, licence compatibility and redistribution decisions.

Decision records must include context, options, chosen option, consequences, rejected alternatives, evidence, owner and date. Until a decision is approved, keep the architecture behind replaceable interfaces and avoid irreversible dependencies.

## 24. Master plan completion and maintenance

This document is the active product and engineering execution plan. It is considered planning-complete when:
- all approved product domains and five target OS families are represented;
- the core-engine-first and rule-driven scientific creation direction is explicit;
- upstream projects and resource rights are separately inventoried;
- scientific object, rule, generation, validation and provenance architecture is defined;
- project, compute, UX, portability, security, testing, release and governance requirements are covered;
- phases have dependency-aware work and measurable exit criteria;
- open decisions and risks are visible rather than silently assumed.

Planning completeness does not mean implementation completion. Update this plan when the owner approves a product-direction change, an architecture decision changes, a phase gate is passed, or new evidence changes the scope or risk. Keep implementation status in the capability/evidence ledger and record exact commit/test evidence there; do not turn this plan into a second, manually duplicated status tracker.

**Ultimate product outcome:** Molecularis is an independent, cross-platform scientific creation and research environment. Scientists define and review rules; Molecularis core engines apply those rules and methods to generate, analyze and optimize scientific artifacts; independent validation evaluates what was produced; and every result carries reproducible provenance, uncertainty and limitations.
