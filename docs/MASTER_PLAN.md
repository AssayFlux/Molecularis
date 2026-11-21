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

- Alpha is the development branch; CORE is the integration branch.
- Work on short-lived branches and merge through reviewed pull requests.
- Each pull request records scope, baseline SHA, compatibility impact, tests, evidence, risks and rollback strategy.
- Do not force-reset shared branches or silently rewrite persisted identifiers and public contracts.
- Update implementation, tests, schemas, registry entries and evidence records together.
- Keep platform support and scientific validation as explicit per-capability states.
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

**Product success is a dependable, reproducible scientific research application across desktop and mobile—not a count of screens, source files or registry entries.**
