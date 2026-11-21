# Molecularis — Alpha Branch Masterplan

**Branch:** Alpha  
**Repository:** AssayFlux/Molecularis  
**Product:** Molecularis by AssayFlux  
**Status:** Owner-directed target architecture and implementation plan; implementation is not implied by this document.  
**Baseline branch:** CORE (branch point recorded when Alpha was created)  
**Date:** 2026-11-21

## 1. North Star

Molecularis is an all-device scientific research platform. It must provide a coherent experience on phone, tablet, laptop, desktop and workstation without defining itself as an Android application. The installed desktop application is the first user experience on Linux, Windows and macOS. Android and Apple iOS/iPadOS applications follow on the same domain model and contracts. A web companion is deferred and is not the first product. Remote and institutional compute are supported through authenticated, policy-controlled execution.

The platform exists to help researchers create, inspect, execute, compare and reproduce scientific workflows. It is not a clinical decision-support system. Clinical claims and deployment remain disabled unless separately authorized, validated and legally cleared.

## 2. Owner language preference

The preferred core languages are C++, Rust and Python.

- C++17 or a later explicitly approved standard: performance-critical numerical kernels, simulation/geometry kernels, mature native scientific-library bindings and measured hotspots.
- Rust: memory-safe parsers, format validation, provenance/security-sensitive services, worker supervisors, resource controls and native cross-platform components.
- Python: scientific orchestration, research APIs, reference implementations, workflow composition and adapters where the scientific ecosystem materially benefits.
- UI implementation language(s): determined by the cross-platform framework feasibility spike. TypeScript/JavaScript may be used inside an installed desktop/mobile shell if justified, but does not make the product website-first or replace the scientific core.
- SQL: persistence and migrations.
- C/CUDA/OpenCL or other runtimes only when required by a selected upstream engine and accepted in a documented decision; do not introduce additional general-purpose languages casually.

Do not use Kotlin/Android as the product foundation. Preserve useful Kotlin/Android code only as migration reference or a temporary compatibility shell until replacement parity and data migration are proven.

## 3. Repository baseline

Alpha was created from the current repository default branch CORE. The current README and architecture baseline describe an Android-native/offline-first workbench with Kotlin/Compose, Python, C++17, Rust, JS/WebView, SQLite, contracts and optional remote compute. The existing architecture file explicitly says it records intended boundaries rather than a fully implemented runtime.

The previous roadmap has sequential R/S/I/P/G/U tracks and substantial research-only, scientific-validation and governance gates. Those records must be reconciled, not erased. Preserve useful completed work, schemas, tests, evidence, provenance, rulebooks and safety restrictions. Reclassify Android-specific delivery assumptions and track ordering where they conflict with the new all-device direction.

No claim is made here that every component in the repository is complete, production-ready, scientifically validated, secure or cross-device tested. The first implementation task is a clean, exact-commit inventory and evidence audit.

## 4. Product experience

### 4.1 Application delivery order
- First: installed desktop applications for Linux, Microsoft Windows and macOS.
- Second: installed Android and Apple iOS/iPadOS applications sharing domain logic, project formats, contracts and design system.
- Later/optional: web companion for collaboration or institutional access, only after installed applications are established.
- The product must not require a website, browser or cloud connection for ordinary local desktop workflows.
- UI framework selection is an open evidence-based decision. Evaluate a representative vertical slice on all five OS families before selecting a framework; do not assume PWA/React is primary.
- Accessibility, offline operation, native filesystem integration and scientific visualization are core requirements.

### 4.2 Compute topology
- Installed application: UI, lightweight visualization, input validation, local project management and user-controlled local workflows.
- Molecularis Node: user-installed local connector for filesystem access, local CPU/GPU and native engines; least privilege, explicit pairing and visible consent.
- Hosted worker: isolated execution for supported workloads.
- Institutional/HPC connector: queued jobs via institution-approved scheduler/API.
- Cloud compute: optional, opt-in, cost-transparent and region/policy-aware.

The application UI must never be treated as a security boundary or trusted execution sandbox for arbitrary scientific code. Heavy workloads are jobs with resource limits, cancellation, logs, artifacts and provenance.

## 5. Core product domains

1. Workspace and project management.
2. Dataset ingestion, validation, metadata and versioning.
3. Sequence and genomics analysis.
4. Protein sequence/model workflows.
5. Macromolecular structure inspection and validation.
6. Molecular chemistry, graph operations and reaction workflows.
7. Molecular docking and scoring, only with documented setup and validation.
8. Molecular dynamics and simulation.
9. DNA/RNA nanostructure design.
10. Workflow orchestration and reproducible notebooks.
11. Results, plots, 3D visualization and comparison.
12. Provenance, audit, licensing and scientific governance.
13. Compute-node and institutional execution management.

## 6. Shared platform architecture

Use a modular, contract-first architecture:

- Cross-platform installed application UI: select after a desktop-first feasibility spike across Linux, Windows, macOS, Android and iOS/iPadOS. Evaluate Qt/C++, Tauri/Rust and other credible options against native integration, accessibility, graphics/3D, packaging/signing, updates, offline storage, mobile lifecycle and licensing. No framework is approved until the evidence and owner decision are recorded.
- API/control plane: Python service layer initially, with Rust services where isolation, parsing or operational reliability warrants it.
- Native libraries: C++ and Rust libraries behind stable C ABI or versioned IPC contracts.
- Job orchestration: API, durable queue, scheduler, worker supervisor, event stream and artifact service.
- Persistence: PostgreSQL for shared relational state; SQLite for local node metadata/cache where appropriate; object storage for large artifacts.
- Contracts: versioned JSON Schema/OpenAPI plus explicit semantic versions and compatibility tests.
- Visualization: Mol* for molecular structures, with other viewers only when justified.
- Local connector: Rust-first supervisor with signed/versioned manifests, capability allowlists and OS-specific adapters.
- Packaging: signed platform-specific desktop application releases first; Android/iOS application packages next; OCI containers for optional server workers. A web deployment is a later companion, not the primary release.

These are target choices. Existing components should be retained where they meet the requirements. A technology choice is not an implementation claim.

## 7. Scientific integration scope from the supplied ZIP

The ZIP contains text snapshots rather than Git repositories. The exact commit/version and complete upstream history are not established by the archive. Twelve external projects are in scope:

| Upstream project | Molecularis role | Initial integration posture |
|---|---|---|
| Genome-Wide Workbench (GWW) | Genomic discovery, alignment, phylogeny and primer-related workflow orchestration | Selective workflow/algorithm adapters; do not embed blindly |
| Biotite | Python sequence/structure formats, analysis and visualization utilities | Python adapter/library evaluation |
| ESM | Protein embeddings, variant scoring, inverse folding and ESMFold/model workflows | Optional isolated model workers; weights/data reviewed separately |
| AlphaFold | Protein structure prediction | Optional HPC/cloud/local-GPU worker profile; database/model storage and terms audited |
| Mol* | Interactive macromolecular structure viewer | Preferred web visualization integration |
| MolProbity | Structure validation methods and reports | Isolated audited worker/adapters; do not expose legacy PHP deployment publicly |
| OpenMM | Molecular dynamics engine | Native worker profile; complete system preparation and force-field provenance required |
| ChemGraph | Agent-assisted computational chemistry workflows | Isolated optional workflow service; human review of inputs and outputs |
| Open Chemistry | Molecular editing/interoperability ecosystem | Select component reuse; dependency and license review |
| NUAD | DNA/RNA nanostructure design | Optional specialized workflow; NUPACK is separate and requires its own license review |
| Galaxy | Workflow platform and tool ecosystem | Federated/API integration; do not merge Galaxy's full codebase into core |
| SciREPL | Browser notebook, multi-language REPL and offline/PWA interaction patterns | Adapt UX and safe browser-kernel ideas; heavy/native tasks use remote/local workers |

The legacy AssayFlux Kinetics snapshot in the ZIP is migration context, not a thirteenth external integration. The complete register is in ALPHA_INTEGRATION_CATALOG.md.

## 8. Scientific integrity and evidence

Every scientific capability must declare:
- inputs and accepted formats;
- units, coordinate conventions and reference frames;
- method and algorithm version;
- tool, container, model, database and parameter versions;
- provenance and input/output checksums;
- expected limitations, uncertainty and confidence semantics;
- resource requirements and supported runtime profiles;
- validation dataset, benchmark, tolerances and independent-review status;
- license and redistribution constraints.

Use evidence levels:
- E0 planned;
- E1 source reviewed;
- E2 adapter and contract implemented;
- E3 automated tests pass;
- E4 reference benchmark and platform/runtime validation pass;
- E5 independent domain review and release approval.

Do not label a result clinically actionable. Research-use status must be visible in the UI and exported reports.

## 9. Security and privacy

Treat uploaded scientific files, notebooks, workflow definitions, models and third-party engines as untrusted inputs. Use tenant/project authorization, least privilege, short-lived credentials, signed job manifests, isolated workers, CPU/memory/time/disk/network limits, immutable audit events, encrypted transport and appropriately encrypted storage. No arbitrary shell or code execution in the API process. Local-node pairing must be explicit and revocable. No telemetry or cloud upload without clear user control.

Clinical/health data is not authorized by this architecture. Any future handling requires explicit owner approval, ethics/legal review, jurisdiction-specific privacy assessment, data minimization, access logging, retention/deletion policy and qualified oversight.

## 10. Migration policy

- Preserve scientific domain logic and tests while decoupling them from Android lifecycle/UI.
- Replace Android screens with shared cross-platform installed-app flows by capability, not by blind screen copying.
- Replace WorkManager scheduling with durable server/local job queues; retain deterministic job semantics.
- Replace Android-only storage with a migration path to project artifacts and local encrypted cache.
- Replace JNI only where a stable C ABI, Rust API or IPC boundary is demonstrably better; do not rewrite working native code for fashion.
- Keep old Android app builds only as a temporary migration/reference artifact; no new Android-native roadmap.
- Provide export/import and integrity verification for existing local user data before retiring any legacy storage.

## 11. Milestones

M0 — baseline audit, branch governance, architecture decisions and security threat model.  
M1 — desktop application shell for Linux/Windows/macOS, UI framework spike, design system, local projects and offline storage.  
M2 — shared domain/contracts, local job supervisor, artifact/provenance model and first end-to-end local scientific workflow.  
M3 — desktop packaging, signing, update/rollback and filesystem/graphics/accessibility validation across all three desktop OSes.  
M4 — Android and iOS/iPadOS application feasibility/vertical slices, shared project format and mobile lifecycle adapters.  
M5 — optional Molecularis Node/remote compute pairing, signed manifests, resource controls and institution/HPC connectors.  
M6 — shared scientific data model, schemas, rulebooks, contract tests and Mol* visualization.  
M7 — Biotite and GWW genomics/sequence workflows.  
M8 — ESM and AlphaFold isolated prediction workers.  
M9 — structure validation and MolProbity audited adapters.  
M10 — chemistry, Open Chemistry and ChemGraph workflows.  
M11 — OpenMM preparation, simulation and analysis.  
M12 — SciREPL-inspired notebooks and Galaxy federation.  
M13 — NUAD workflow and external NUPACK integration review.  
M14 — institution/HPC operations, cross-platform security/scientific validation and release readiness.

Each milestone has build, audit and owner-acceptance gates. Dependencies may be refined after repository audit; milestones are not completion claims.

## 12. Alpha execution rules

- All work on branch Alpha; no direct commits to CORE.
- Record base SHA, toolchain versions, exact commands and CI links.
- Keep changes reviewable; prefer small PR-sized commits.
- Update docs, tests, schemas, changelog and provenance with code.
- Preserve legacy plans as historical where useful; do not silently rewrite evidence.
- No bulk upstream source copy before license/security audit.
- Do not add credentials, datasets, model weights or large binaries to Git.
- Require exact-head CI and documented tests for every substantial increment.
- No release, clinical claim or scientific capability promotion without the corresponding evidence.

## 13. First deliverables

1. Complete repository file/build/test inventory and current CI baseline.
2. Current architecture and decision reconciliation.
3. Android-to-web/local-node migration ledger.
4. Versioned domain/API schemas and job lifecycle.
5. Threat model and local-node security design.
6. Cross-device test matrix.
7. Per-upstream source/version/license manifest.
8. Vertical-slice workflow demonstrating upload → validation → job → result → provenance → export.

## 14. Acceptance

Alpha is ready for a first public all-device preview only when the desktop applications on Linux, Windows and macOS; authentication where needed; local projects; artifact lifecycle; local job status; one validated scientific vertical slice; provenance; accessible UI; security review; install/upgrade/uninstall and rollback evidence; supported hardware/OS matrix and documentation are complete. This does not imply clinical readiness or validation of all twelve upstream integrations.


## 15. Owner correction — desktop-first, not website-first

On 2026-11-21 the owner explicitly corrected the initial Alpha direction: desktop application first for Linux, Microsoft Windows and macOS; Android and Apple mobile applications are also required. No website/PWA-first strategy. This section supersedes any remaining web-first wording in earlier planning text. The web companion is deferred until after installed application foundations. Update all linked plans and milestone documents consistently; preserve historical records rather than deleting evidence.
