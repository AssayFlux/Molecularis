# Molecularis — Repository Baseline Inventory

**Snapshot:** CORE at `dbda3496386edf46270d54296b2204a53d7de573`  
**Tree:** `dbda3496386edf46270d54296b2204a53d7de573`  
**Date:** 2026-11-21  
**Method:** GitHub recursive Git tree (not truncated), targeted source and documentation reads. This is a repository inventory, not an exhaustive line-by-line code audit, device test, security assessment or scientific validation.

## 1. Inventory counts

| Area | Count / observation |
|---|---:|
| Tracked files | 454 |
| Directories | 75 |
| Python source files across repository | 149 |
| Python modules in `python/molecularis/` | 51 |
| Test files in `tests/` | 68 |
| Kotlin files across repository | 51 |
| API JSON schemas | 22 |
| Documentation files | 108 |
| Capability registry tool entries | 130 |
| Registry entries marked implemented | 68 |
| Registry entries marked planned | 62 |
| Implemented entries with evidence_level=none | 68 |

Registry status semantics matter: `implemented` means source code exists. It does not assert integration, independent scientific validity, platform support or release readiness.

## 2. Existing implementation assets

### Android application
- Kotlin/Jetpack Compose app, Gradle build, Android manifest, Android-specific storage, background work and UI.
- Local encrypted storage/crypto, data-pack management, import workers and provenance summaries.
- Scientific cards/runners for selected sequence, genomics, chemistry and viewer paths.
- JNI/C++ probe and Python/Chaquopy integration.
- Android is the only established full client in the tree. Retain as migration reference and compatibility implementation until replacement parity and data migration are demonstrated.

### Python scientific package
The `python/molecularis/` package includes sequence/FASTx, local reference packs/search, genetic code, ORF, BLASTP, HMMER, genomics, GFF3, variants, phylogeny, protein properties/design/motifs, structure parsing/alignment/pockets/quality/view payloads, chemistry, docking, OpenMM, omics, PK/PD and PGx-related modules.

Presence is not proof that optional dependencies are installed, end-to-end workflows are integrated, or results are independently validated. Some modules are pure Python; others require optional host tools or runtimes.

### Structure and 3D
- Android `StructureViewer.kt`.
- Offline structure-viewer HTML/CSS/JS assets in Android assets.
- A second viewer asset tree under `web/viewers/`.
- `api/structure-view-payload.schema.json`.
- Python structure parsing, alignment, pocket, quality and view-payload modules.

This is a meaningful prototype/foundation. It is not evidence of a complete Mol* integration, feature parity across desktop/mobile, large-structure performance, or independently validated structure-quality service.

### Chemistry, docking and dynamics
- Python SDF/chemistry parser and optional RDKit adapter.
- AutoDock Vina runner and a bounded Node 22 worker with docking disabled by default, explicit auth and conservative request limits.
- OpenMM adapter for bounded simulations when a trusted caller supplies a prepared system, topology and positions.
- Complete docking preparation and end-to-end system preparation/force-field pipeline remain gaps. The Node worker is Vina-specific, not a general compute platform. OpenMM is not exposed as a production node capability.

### Contracts, registry and validation
- 22 API JSON schemas, additional schemas and data catalogues.
- Capability registry and checker.
- Python tests, Android tests/workflows, Node worker tests, scientific reference scripts and fixtures.
- Validation fixtures/scripts cover selected SciPy/Biopython/RDKit/Vina/OpenMM comparisons or smoke checks.
- SBOM, governance, security and provenance material exists, but completeness and current-head acceptance must be verified.

## 3. Missing or not established in this snapshot

- No completed installed desktop client for Linux, Windows or macOS.
- No iOS/iPadOS application project.
- No selected cross-platform UI framework or five-platform feasibility evidence.
- No substantive shared Rust crate; `rust/` contains only a placeholder.
- No substantive cross-platform C++ scientific engine; current C++ source is a small Android native probe.
- No universal local job supervisor/engine manager covering the planned scientific workloads.
- No completed shared project format and cross-platform migration path proven end-to-end.
- No general hosted compute/HPC federation service.
- No complete, production-ready Mol* integration or cross-platform graphics acceptance evidence.
- No claim of complete scientific validation, security clearance, institutional readiness or clinical authorization.

## 4. Documentation conflicts observed

- `NORTH_STAR.md` and the new desktop-first `ROADMAP.md` direction are newer than some older Android-first integration plans.
- `README.md` still contains Android v0.1/v0.1.1 release-direction content and references legacy `main` branch URLs.
- `docs/MASTER_SCIENTIFIC_INTEGRATION_PLAN.md` and `docs/DESKTOP_COMPUTE_ARCHITECTURE.md` describe Android-first client/desktop-worker topology.
- `docs/INTEGRATION_MILESTONES.md` describes an Android interoperability sequence that conflicts with desktop-first delivery.
- `docs/README.md` still lists the old R/S/I/P/G/U order as current authority.
- `docs/alpha/BASELINE_AUDIT.md` includes an earlier branch snapshot and the superseded web/PWA-first direction; it is historical evidence only.
- Multiple plans repeat similar integration, validation, release and governance content without a single status ledger.

## 5. Current branch and CI snapshot

- CORE is protected and is the repository default branch.
- Alpha remains the development branch.
- A new planning branch was created from CORE: `replan/2026-11-21-repository-first`.
- PR #8 has merged into CORE at the baseline commit above.
- CORE workflow run [44854675140](https://github.com/AssayFlux/Molecularis/actions/runs/44854675140) was pending at audit time. A pending run is not a pass.

## 6. Audit limits and next inspection

This inventory does not prove every registry path is accurate or every source module works. Phase 0 must reconcile all 130 registry entries with real files, imports, tests, optional dependencies, CI jobs and evidence. It must inspect persisted Android identifiers and migrations before any retirement decision. It must also run exact-head tests and review the desktop/mobile framework spike.
