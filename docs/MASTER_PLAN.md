# Molecularis — Repository-First Master Plan

**Status:** New canonical implementation plan, prepared from the live CORE repository snapshot  
**Baseline commit:** `dbda3496386edf46270d54296b2204a53d7de573`  
**Baseline tree:** `dbda3496386edf46270d54296b2204a53d7de573`  
**Plan date:** 2026-11-21  
**Authority:** `NORTH_STAR.md`, this plan, approved entries in `DECISIONS.md`, [legacy requirements traceability](REQUIREMENTS_TRACEABILITY.md), and the evidence ledger linked below.

> This document replaces the competing implementation roadmaps and masterplans as the single execution authority. It is a plan, not a claim that planned applications, services, integrations, validation or platform support already exist.

## 1. Product direction

Molecularis is an installed, desktop-first scientific research platform.

1. **First delivery:** installed applications for Linux, Microsoft Windows and macOS.
2. **Next delivery:** installed Android and Apple iOS/iPadOS applications.
3. **Later and optional:** web companion for collaboration or institutional access. It is not the first product, a required runtime, or a substitute for desktop software.

All clients share scientific meaning, domain logic, project/artifact formats, schemas, provenance and design language. Platform-specific code is limited to UI and OS integration where necessary. Ordinary local desktop research must work offline and must not depend on a website or hosted service.

Preferred core languages are C++, Rust and Python. The UI framework is deliberately undecided until a measured feasibility spike covers all five target OS families. Do not select a framework from preference or marketing claims alone.

## 2. Rules that protect the existing repository

This is a gradual migration, not a greenfield rewrite.

- Preserve existing source, scientific methods, tests, schemas, capability IDs, API identifiers, database contents, user files, encryption semantics, provenance and validation records unless a reviewed migration proves they can be retired.
- Do not remove or replace the Android application until the replacement has demonstrated feature parity for each migrated workflow, successful export/import, integrity checks, backup/restore and rollback.
- Keep compatibility readers and adapters for old project/data versions for a declared deprecation window.
- Never change a persisted identifier, schema ID, protocol field, database name, preference key, WorkManager tag, keystore alias, cryptographic AAD label or cache prefix without an explicit versioned migration and compatibility tests.
- Preserve scientific terminology. For example, enzyme kinetics is a scientific domain, not obsolete branding. Rename only product identity and user-facing labels where justified; do not mass-rename scientific identifiers.
- Keep CORE as protected integration branch. Implement on a review branch and merge through PR with exact-head CI.
- No milestone is complete merely because documentation, a registry entry, a compiling binary or a green unit-test job exists.

## 3. Repository baseline and honest status

The baseline inventory is recorded in [REPOSITORY_BASELINE.md](REPOSITORY_BASELINE.md). At the baseline snapshot it found:

- 454 tracked files and 75 directories.
- 51 Python modules under `python/molecularis/`, with 68 test files under `tests/`.
- 51 Kotlin source files across the repository; the Android application is the only established client implementation.
- 22 JSON schemas under `api/`.
- 130 tool entries in `capabilities/registry.yaml`: 68 marked `implemented`, 62 marked `planned`. All 68 currently marked implemented have `evidence_level: none`; the registry defines implemented as source code existing, not as validated.
- A bounded Node 22 worker for optional AutoDock Vina docking.
- Existing structure parsing/analysis modules, structure-view payload schema and an offline viewer implementation in Android/web viewer assets.
- An OpenMM runner that accepts a caller-prepared OpenMM system/topology/positions; complete preparation and force-field pipeline remain gaps.
- An optional host-side RDKit adapter; availability depends on an installed, approved runtime.
- Android/Kotlin/Compose, Gradle, Python/Chaquopy and a small JNI/C++ probe.

The repository does **not** yet contain a completed desktop application, an iOS/iPadOS application, a selected cross-platform UI framework, a substantive shared Rust crate, or a substantive cross-platform C++ scientific engine. The current Rust directory is a placeholder; the current C++ implementation is a small native probe. These must not be presented as finished foundations.

The latest CORE CI run at the baseline was pending when this plan was prepared: [run 44854675140](https://github.com/AssayFlux/Molecularis/actions/runs/44854675140). Do not treat pending as passed. Recheck the run before using it as acceptance evidence.

## 4. Capability status model

Every capability has two independent dimensions:

**Implementation state**
- `not_started`: no Molecularis implementation.
- `prototype`: limited proof of concept.
- `partial`: useful code exists, but workflow or critical requirements are incomplete.
- `integrated`: end-to-end product workflow exists behind a supported interface.
- `deprecated`: retained only for migration/history.

**Evidence state**
- `E0 planned`
- `E1 source and method reviewed`
- `E2 contract and adapter implemented`
- `E3 automated tests pass`
- `E4 independent reference/benchmark and target-platform validation pass`
- `E5 independent domain review and release approval`

A capability is not scientifically validated because it is marked implemented. Each capability record must include intended use, supported inputs, outputs, units/conventions, limitations, engine/version, dependencies, provenance, security boundary, test references, evidence state, supported platforms and owner/reviewer decision.

The capability registry must be reconciled with source and test evidence. Its present 68/62 counts are a starting inventory, not a release score.

## 5. Target architecture

### 5.1 Installed clients
- Desktop client: Linux, Windows and macOS first.
- Mobile clients: Android and iOS/iPadOS next.
- Optional web companion only after installed-client foundations.

### 5.2 Shared domain and scientific core
- Platform-neutral project, dataset, artifact, workflow, job, provenance and settings models.
- Stable, versioned, language-neutral contracts.
- Python for scientific orchestration, adapters and reference implementations.
- Rust for safe parsing, process supervision, resource controls and security-sensitive services where justified.
- C++ for measured performance-critical kernels and mature native scientific integrations.
- Do not add languages or duplicate algorithms without a concrete technical reason.

### 5.3 Execution topology
- Local execution on the user's computer is preferred when feasible.
- Molecularis Node is an optional, explicitly paired local compute connector.
- Hosted workers and institutional/HPC schedulers are optional extensions.
- The UI is not a security boundary. Engines and imported workflows are untrusted; use capability allowlists, least privilege, bounded resources, cancellation, audit logs and isolated processes.
- No arbitrary shell or unrestricted code execution in a privileged API or worker process.

### 5.4 Data and visualization
- Portable, versioned project and artifact formats with checksums and atomic writes.
- Canonical sequence, structure, molecule, coordinate, unit and provenance semantics.
- Existing viewer assets are retained and evaluated; Mol* is a candidate integration, not assumed to be present.
- Keep the viewer separate from scientific validators and compute engines.

## 6. Delivery phases

Phases are dependency gates, not calendar promises. Re-estimate after each gate using actual staffing, hardware, upstream compatibility and evidence requirements.

### Phase 0 — Exact baseline and migration ledger
**Goal:** establish what really exists and what can safely be reused.

Work:
- Run exact-commit CI and record all jobs, results and failures.
- Complete source inventory across Android/Kotlin, Python, Rust, C++, Node, web assets, schemas, tests and build systems.
- Reconcile every capability registry entry to an existing source file, tests and actual runtime availability.
- Identify duplicate, stale, missing and conflicting documentation.
- Inventory persisted Android data and identifiers, package IDs, storage formats, crypto, background jobs and export paths.
- Create upstream source/version/licence/SBOM register.
- Classify each asset as retain, extract, adapt, replace, defer or retire.

Exit: reviewed baseline, capability ledger, data migration ledger, risk register, exact-head CI evidence and owner-approved framework evaluation criteria.

### Phase 1 — Cross-platform framework feasibility
**Goal:** choose the UI/application technology from evidence, not assumption.

Build the same small vertical slice on Linux, Windows, macOS, Android and iOS/iPadOS. Compare credible candidates (including native and cross-platform options) against:
- native filesystem and OS integration;
- accessibility, keyboard, pointer, touch and screen-reader support;
- offline project storage and large-file handling;
- GPU/3D rendering and scientific visualization;
- background execution and mobile lifecycle;
- packaging, signing, notarization, updates and rollback;
- crash reporting, test automation and reproducible CI;
- C++/Rust/Python interoperability;
- performance, memory, contributor skill and licence obligations.

Exit: measured comparison, working prototype evidence on each OS family, risks and owner-recorded architecture decision. No framework is preselected by this plan.

### Phase 2 — Shared contracts and project foundation
**Goal:** make platform-independent data and workflow semantics before migrating screens.

Work:
- Define project, dataset, artifact, provenance, job, capability and engine manifests.
- Version schemas and implement compatibility tests.
- Define canonical sequence, macromolecular structure, small molecule, coordinate frame, units and identifier models.
- Add project create/open/save/export/import with checksums, atomic writes and migration support.
- Define a stable boundary for Python, Rust and C++ components.
- Preserve legacy Android readers and data access.

Exit: cross-language contract tests, project round-trip, version migration fixtures, corruption recovery and reproducible provenance.

### Phase 3 — Desktop application foundation
**Goal:** first real Molecularis installed application.

Work:
- Build desktop shell for Linux, Windows and macOS using the framework selected in Phase 1.
- Implement workspace, projects, settings, file import/export, offline state and accessibility foundations.
- Add local job supervision with logs, cancellation, resource limits and durable state.
- Connect one existing scientific workflow end-to-end, beginning with a bounded sequence workflow and/or structure inspection selected by the Phase 0 audit.
- Provide install, upgrade, uninstall and rollback paths.

Exit: signed/reproducible installable packages and documented runtime tests on all three desktop OSes; offline project workflow and one end-to-end scientific vertical slice.

### Phase 4 — Desktop visualization and scientific vertical slices
**Goal:** turn existing scientific code into coherent, user-facing services.

Priority order, adjusted only by dependency evidence:
1. Sequence and genomics foundation: FASTA/FASTQ, QC, translation, ORFs, alignment, annotation and reference-pack workflows.
2. Structure data and 3D inspection: PDB/mmCIF parsing, atom/residue identity, coordinate conventions, viewer payload, selection, representations, large-structure performance and offline viewer integration.
3. Structure analysis: alignment, pockets and quality observations with clearly stated method limits.
4. Chemistry: molecule import, sanitization, stereochemistry, descriptors and graph operations through a pinned RDKit profile.
5. Docking: complete input preparation, bounded Vina execution, result inspection, provenance and reference validation.
6. Molecular dynamics: trusted system preparation, topology/force-field provenance, OpenMM setup, simulation, analysis and reproducibility.
7. Protein modelling: optional ESM/AlphaFold isolated profiles, weights/data rights, hardware requirements, benchmarks and uncertainty handling.
8. Advanced genomics/omics/PGx: research-only evidence, curated references and independent review; no clinical interpretations.
9. DNA/RNA nanostructure design and specialist workflows after exact source and thermodynamic dependency review.

Exit for each service: an end-to-end UI-to-result workflow, explicit supported inputs/outputs, method and dependency versions, provenance, limitations, tests, reference validation and platform support statement.

### Phase 5 — Compute services
**Goal:** safely extend compute beyond the local desktop.

Work:
- Evolve the existing Vina-only Node worker into a versioned capability-bounded Molecularis Node only after threat model and pairing design.
- Add durable jobs, authentication, host identity, revocation, quotas, cancellation, recovery, logs and artifact transfer.
- Add isolated engine profiles one by one; never expose generic shell or user-selected executables.
- Add hosted workers and institutional/HPC connectors only where a validated workload requires them.

Exit: independent security review, threat-model closure, deployment/recovery exercises, resource exhaustion tests and job/provenance conformance.

### Phase 6 — Mobile applications
**Goal:** deliver Android and iOS/iPadOS using the same scientific semantics and project formats.

Work:
- Preserve Android compatibility while replacing its UI/platform architecture incrementally.
- Implement iOS/iPadOS application and platform adapters.
- Port capabilities by vertical slice, not screen-by-screen copying.
- Validate storage permissions, background lifecycle, battery, offline use, touch accessibility, graphics and secure storage.
- Migrate local user data with export/import, checksums, backup/restore and rollback.

Exit: install/upgrade tests on supported physical devices, data migration and recovery evidence, accessibility, offline and scientific parity evidence.

### Phase 7 — Workflow, notebooks and federation
**Goal:** make workflows reproducible and composable.

Work:
- Versioned workflow manifests, dependency graphs and deterministic execution semantics.
- Notebook/repl UX only with a threat-modelled isolated kernel.
- Galaxy API/federation only when the operational cost and user need are justified.
- Exportable run bundles and complete provenance.

Exit: reproducible workflow round-trips, isolation/security review, auditability and reference tests.

### Phase 8 — Institutional and release readiness
**Goal:** support governed institutional deployments.

Work:
- Full SBOM and third-party rights clearance.
- Security/privacy/accessibility reviews.
- Backup/restore, disaster recovery, incident response and update rollback drills.
- Performance, compatibility and reliability targets based on measured workloads.
- Independent scientific review and owner acceptance.

Exit: all required evidence attached to a versioned release record. No clinical or regulated-use claim is implied.

## 7. External projects and integration policy

The candidate ecosystem is documented in [THIRD_PARTY_INTEGRATION_REGISTER.md](THIRD_PARTY_INTEGRATION_REGISTER.md). Candidates include Biotite, Mol*, MolProbity, RDKit, OpenMM, ESM, AlphaFold, Genome-Wide Workbench, Open Chemistry, ChemGraph, NUAD, Galaxy and SciREPL.

For every upstream component, record exact repository, release/commit, files/modules used, licence and notices, transitive dependencies, model/data terms, supported OS/ABI, security posture, Molecularis adapter, tests, benchmark, upgrade policy and removal path. Code, weights, datasets, databases and assets have separate rights. Never import an entire upstream platform without a component-level justification.

## 8. Migration and compatibility gates

For each legacy Android capability:
1. inventory behaviour, source, tests, data stores and stable identifiers;
2. extract platform-neutral logic where possible;
3. define the replacement contract and data format;
4. implement the new client path alongside the old path;
5. compare outputs and migrate representative data;
6. test export/import, checksum, backup/restore, rollback and failure recovery;
7. obtain owner acceptance before removing the legacy path.

Never silently upload user files. Never delete old user data during migration. Keep a documented rollback window.

## 9. Scientific integrity, safety and intended use

Molecularis remains research-use only. No clinical diagnosis, treatment, dosing or patient-specific decision support is authorized by this plan. Clinical/regulated use requires separate owner authorization, qualified independent review, applicable ethics/legal/regulatory approvals and validated evidence.

Every scientific result must expose inputs, units/conventions, method and version, dependencies/model/data versions, provenance, limitations, uncertainty semantics, validation state and supported runtime. A viewer is not a validator; a parser is not a predictor; an execution envelope is not a working scientific engine; a simulation adapter is not system preparation; docking scores are not experimental binding free energies.

## 10. Project control and reporting

- CORE: protected integration branch.
- Alpha: development branch; keep it aligned through reviewed PRs, not force resets.
- Use short-lived feature branches for substantial migrations.
- Each PR states baseline SHA, scope, compatibility impact, tests, evidence, risks and rollback.
- Update the capability registry and migration ledger with code changes.
- Report status using separate fields: planned, source-present, integrated, tested, reference-validated, platform-verified, independently reviewed, release-approved.
- No percentage-complete claims without a defined denominator and auditable evidence.

## 11. Definition of done

A deliverable is complete only when:
- implementation and documentation are merged;
- exact-head CI passes;
- contracts and migrations are backward-compatible or versioned;
- security and licence review are complete where applicable;
- scientific reference/benchmark evidence is attached where applicable;
- target-platform install/runtime/accessibility/offline evidence is attached;
- limitations and known failures are documented;
- rollback and data recovery are demonstrated;
- owner acceptance is recorded.

## 12. Reconciliation with the original Molecularis/Kinetics scope

This plan was cross-checked against the original 18-part owner specification, the R0–R10 foundation/science plans, S1–S10 discovery roadmap, I-track engine evaluations, P0–P7 PGx governance pathway, G0–G7 assurance work and U0–U6 interface/viewer programme. The detailed requirement-to-source mapping and retained open gates are in [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md). The original Android-first deployment sequence is superseded, not the scientific scope, offline-first principle, provenance model, engine-tier thinking, governance, research-only boundary or owner UI design contract.

### 12.1 Scientific service portfolio and delivery order

The long-term portfolio includes sequence bioinformatics; genomics and transcriptomics; proteomics and protein discovery; structural biology and 3D visualization; chemoinformatics; enzyme kinetics; phylogenetics/evolution; systems biology; multi-omics; microbiology/metagenomics; immunoinformatics; biostatistics; PGx research; in-silico discovery; molecular biology/CRISPR/primer tools; PK/PD; and workflow/provenance infrastructure. Registry presence does not mean each service is a deliverable. Each is independently gated by data, engine, licence, contracts, tests, validation and platform support.

Initial delivery candidates should be selected after Phase 0 by a weighted readiness review: existing working source, smallest missing dependency chain, scientific reference availability, local/offline feasibility, user value, cross-platform feasibility, safety/licence risk and time to a complete end-to-end workflow. Do not pre-commit to a broad catalogue. Enzyme kinetics remains a candidate flagship from the original specification; sequence QC/import is another candidate because there is an existing Android path and Python tests. Choose one or at most two vertical slices based on exact-head evidence and independent reference quality.

### 12.2 3D structure service — explicit staged scope

3D structure work is a first-class scientific service, not just a viewer screen. Its staged scope is:
1. **Data foundation:** PDB and mmCIF ingestion, stable atom/residue/chain identity, alternate locations, insertion codes, assemblies, coordinate units/frames, model numbering, missing atoms/residues and validation diagnostics.
2. **Preparation pipeline:** explicit, provenance-recorded choices for biological assembly, protonation, hydrogens, alternate conformers, waters, ions/metals, cofactors, ligands and missing atoms/residues. No silent repair or inferred chemistry.
3. **Viewer:** offline-capable 3D rendering, representations, chain/residue/atom selection, sequence-to-structure mapping, camera/view state, annotations, export and accessibility; evaluate Mol* selectively against the existing viewer assets and target framework.
4. **Analysis:** contacts, distances, RMSD/superposition, SASA, secondary structure, hydrogen-bond/salt-bridge/disulfide candidates, interfaces, pockets, residue environments and variant mapping, each with method definitions and limitations.
5. **Quality and prediction:** geometry/validation metrics and predicted-model confidence kept distinct from experimental resolution/R-free; prediction engines and weights are separate optional profiles, never bundled by assumption.
6. **Evidence:** fixed public reference structures, independent implementations, mmCIF edge cases, large-file and GPU/CPU benchmarks, visual correctness, accessibility and platform/device tests.

Current structure.py, structure_alignment.py, structure_pockets.py, structure_quality.py, structure_view.py, sequence_structure.py, Android StructureViewer.kt, viewer assets and API schema are foundations. They do not establish the full service above. Mol* is a candidate integration, not an existing dependency or guaranteed choice.

### 12.3 Engine tiers and compute placement

Retain the original Tier A/B/C concept but make it hardware-profile-specific: **A** local lightweight capabilities suitable for ordinary supported hardware; **B** optional local engines/data packs that pass measured resource and ABI tests; **C** optional paired node, workstation, GPU or institutional/HPC execution. A capability may have different placement by OS/device. Record CPU, RAM, disk, GPU, runtime, licence, network, timeout, cancellation and output-size requirements in engine manifests. Never equate Tier C with cloud upload by default; user consent and data locality are explicit.

### 12.4 Cross-cutting requirements retained from the earlier tracks

- Registry remains Tool → Engine → Data pack → Domain, with method/version, source/licence, runtime, tier, status, platform, evidence and validation path. Do not mark a tool validated from source presence or a smoke test.
- Data packs are versioned, checksum-verified, licence-reviewed, source-attributed and explicitly delivered (bundled, optional local download or remote-only). No runtime executable-code downloads.
- Result provenance includes immutable input/output digests, reference/model/data release, parameters, units, seeds, warnings, environment, compute placement and limitations.
- Scientific validation includes synthetic truth fixtures, independent references, calibration/uncertainty, negative cases, benchmark/performance, domain review and reproducibility. Prediction, docking, MD and clinical-adjacent services each need independent validation.
- PGx remains a staged research-only pathway with indeterminate/abstention states, ancestry coverage disclosure and separate source/guideline versions. No clinical interpretation or recommendations.
- Security/privacy, accessibility, data migration, source/model/data rights and governance are continuous gates, not a final paperwork phase.
- Research-paper and publication work follows validated, reproducible results; it does not drive or overstate product capability.

## 13. Canonical supporting records

- [Repository baseline](REPOSITORY_BASELINE.md)
- [Capability and migration status](CAPABILITY_STATUS.md)
- [Plan retirement and historical-document map](PLAN_RETIREMENT.md)
- [North Star](../NORTH_STAR.md)
- [Decision log](../DECISIONS.md)
- [Validation framework](../validation/README.md)
- [Security threat model](security-threat-model.md)
- [Third-party integration register](THIRD_PARTY_INTEGRATION_REGISTER.md)
