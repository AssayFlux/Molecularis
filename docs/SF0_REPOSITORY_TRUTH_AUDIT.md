# SF0 — Repository Truth and Dependency Audit

**Audit date:** 2026-11-26  
**Repository:** `AssayFlux/Molecularis`  
**Branch:** `CORE`  
**Audited HEAD:** `e36e32705045ab6311d20713d8f2a47b8c5af715`  
**Scope:** tracked-tree inventory, Python package layout, A–N service/capability declarations, test inventory, dependency declarations, license/data/model governance, external adapters, CI configuration, and documentation consistency.  
**Method:** GitHub recursive Git tree at the exact HEAD plus targeted source/configuration/documentation inspection. This is a repository-truth inventory, not a line-by-line code review, local execution, vulnerability scan, legal opinion, scientific certification, or confirmation of the contents of external deployment environments.

## 1. Executive result

Molecularis is a Python-first scientific-computing repository with fourteen domain services (A–N), a separate AI service/documentation area, a shared local Core/MSDE runtime and artifact store, a scientific knowledge representation layer, mathematical/statistical reasoning primitives, scientific-engine adapters, schemas, tests, benchmarks and validation fixtures.

The repository is substantial and contains implemented software—not merely plans. At the same time, the registry and governance files intentionally distinguish implementation from validation, and that distinction must be retained.

**SF0 inventory result:** the tracked repository and its principal engineering/dependency boundaries have been inventoried and reconciled against the current tree. The audit has identified concrete follow-up work; it does not declare P0 accepted, certify every implementation, or authorize training on any data.

## 2. Exact tracked-tree inventory

The recursive Git tree at the audited HEAD is complete (`truncated=false`) and contains **464 tracked files**.

| Extension / class | Count |
|---|---:|
| Python (`.py`) | 219 |
| Markdown (`.md`) | 97 |
| JSON (`.json`) | 79 |
| YAML (`.yaml`) | 20 |
| PNG | 14 |
| JPG | 8 |
| SVG | 4 |
| GIF | 4 |
| TXT | 8 |
| PDBQT | 2 |
| MJS | 2 |
| Other (workflow yml, TOML, HTML, CFF, gitignore, py.typed) | 7 |
| **Total** | **464** |

Primary areas include:

- `python/molecularis/`: 85 Python files, including the platform package.
- `python/kinetics/`: 12 Python files forming a legacy compatibility namespace.
- `tests/`: 90 `test_*.py` files plus `tests/__init__.py`.
- `services/`: 15 service directories (14 scientific domains plus AI), containing service specifications, schemas, data/fixtures and benchmark programs.
- `docs/`: 22 tracked documents.
- `api/`: 20 JSON schemas.
- `Assets/`: 31 tracked visual/brand assets.
- `validation/`: 21 reference fixtures, scripts and optional-profile requirement files.
- `CORE/`: 11 data-engine documents and schemas.
- `scripts/`: 7 engineering/validation scripts.

Two zero-byte files are intentional Python packaging markers: `python/molecularis/py.typed` and `tests/__init__.py`. No other zero-byte tracked file was found. The 31 Assets files are preserved and are not classified as obsolete code.

## 3. Package and implementation layout

### Canonical package

The canonical Python package is `python/molecularis/`. It contains:

- Fourteen domain-service implementations and supporting domain modules.
- Shared platform contracts, lifecycle service, capability registry/runtime and content-addressed ArtifactStore under `platform/`.
- Agentics planner/orchestration entry point in `ai.py`.
- Scientific knowledge model in `knowledge.py`.
- Mathematical/statistical reasoning primitives in `reasoning.py`.
- Construction, provenance and proposer/verifier contracts in `scientific_core.py`.
- Optional engine registry in `scientific_engines.py`.
- Bootstrap, catalog and cross-domain integration modules.
- External-tool adapters for sequence, genomics, chemistry, structure, simulation, docking, protein inference and related operations.

### Legacy compatibility namespace

`python/kinetics/` contains an `__init__.py` lazy compatibility namespace and eleven very small re-export modules pointing to canonical `molecularis.*` implementations. They are not separate scientific engines or substantive duplicate implementations. Do not delete them as “empty placeholders” without first proving no import/API compatibility depends on them and updating the compatibility test. Their continued presence should be treated as deliberate compatibility debt, not as the canonical package layout.

### Language/runtime truth

- Root package: `molecularis-workbench`, version `0.1.0`.
- Build backend: setuptools (`setuptools>=68`).
- Declared Python floor: `>=3.10`.
- CI interpreter: Python 3.11.
- Canonical implementation language: Python.
- No C++, Rust, Java or other compiled first-party implementation tree appears in the tracked inventory. Native dependencies may still be supplied by optional third-party wheels or host executables.

## 4. A–N service inventory

The repository contains these fourteen domain service directories, each with its corresponding canonical Python service implementation and service-level engineering materials:

| Key | Service directory | Domain |
|---|---|---|
| A | `services/molecular/` | Molecular representations and operations |
| B | `services/sequence/` | Biological sequence processing |
| C | `services/structure/` | Molecular structure and geometry |
| D | `services/chemistry/` | Chemical graphs and chemistry |
| E | `services/protein/` | Protein analysis and design briefs |
| F | `services/genomics/` | Genomic reads, variants and annotation |
| G | `services/dna-rna/` | DNA/RNA sequence and structure operations |
| H | `services/simulation/` | Simulation contracts and adapters |
| I | `services/kinetics/` | Reaction and kinetic models |
| J | `services/omics/` | Omics matrices and analysis |
| K | `services/phylogeny/` | Phylogenetic analysis |
| L | `services/pharmacogenomics/` | Pharmacogenomic evidence and matching |
| M | `services/cohorts/` | Cohort/population operations |
| N | `services/workflows/` | Workflow DAGs and orchestration |

A fifteenth directory, `services/ai/`, contains Agentics specifications, constitution, acceptance criteria, scientific foundation and tool registry. It is not a fifteenth A–N domain service.

The tree contains 15 `service.yaml` manifests, 15 `ACCEPTANCE.md` files, 15 `RULEBOOK.md` files, 14 `RUNTIME.md` files and 16 `ENGINE.md` files. These counts describe tracked documents, not a claim that every service has identical runtime or validation maturity.

## 5. Capability registry truth

`capabilities/registry.yaml` is a machine-readable registry with **124 tool records**.

At this snapshot:

| Registry field | Count |
|---|---:|
| `status: implemented` | 124 |
| `status: validated` | 0 |
| `status: planned` | 0 |
| `evidence_level: none` | 124 |
| Benchmark/reference-concordance/clinical-study evidence levels | 0 |

Interpretation: all 124 registry records declare that a corresponding implementation path exists. None is declared validated in this registry and none carries a non-empty evidence level. This does not mean there are no tests; it means implementation status is not being promoted to scientific validation status. This is a positive governance distinction, but the registry should eventually link each capability to its test/reference evidence and independently reviewed acceptance record.

The registry validation script checks identifiers, implementation paths and declared references. It does not itself establish scientific validity.

## 6. Tests, schemas, benchmarks and CI

### Test inventory

There are 90 tracked `tests/test_*.py` files. The names cover the platform/runtime/store, Agentics, knowledge and reasoning layers, scientific core, engine adapters, A–N domain services, schemas, cross-domain handoffs, package compatibility and SBOM generation.

The inventory confirms broad test-file coverage by subsystem, but file presence is not a measured line/branch coverage percentage. The audit did not execute pytest, optional profiles, mypy or Ruff.

### Schemas and validation fixtures

The tree includes 20 files under `api/`, additional service-level schemas, shared Core schemas and schema/fixture validation scripts. The repository-wide schema validator discovers files matching `*.schema.json`; the historical P1–P3 milestone records report 66–69 validated schemas at their respective tested commits. A fresh exact-HEAD run is required to establish the current number and result.

The `validation/` area contains source/reference comparison programs, chemistry and structure fixtures, docking PDBQT fixtures and optional profile requirement files. These are not equivalent to comprehensive benchmark datasets.

### CI definition

`.github/workflows/ci.yml` runs on pushes and pull requests targeting `CORE`, and on manual dispatch. It installs the development profile, installs Molecularis editable, emits an installed-Python SPDX inventory, validates the capability registry and JSON schemas, runs Ruff E9/F checks, compiles Python, runs benchmark smoke programs and executes the core test suite. Optional Chemistry, Genomics and Sequence profiles are represented in the workflow.

The CI configuration does not by itself prove that a run passed on the audited HEAD. The GitHub commit-status query for this HEAD returned no status records, and the commit-associated workflow-run query exposed no run record. Therefore **current-HEAD CI is unverified in this audit**. Historical P1/P2/P3 CI results in the backlog refer to earlier exact commits and must not be represented as current-HEAD test results.

## 7. Dependency and runtime inventory

Root `pyproject.toml` declares no mandatory runtime dependencies. The project is intentionally Python-standard-library-first, with the following optional profiles:

| Extra | Declared packages | Actual purpose / caveat |
|---|---|---|
| `docking` | `vina==1.2.7` | Optional host docking runner; prepared PDBQT inputs |
| `md` | `openmm==8.6.1` | Optional molecular dynamics runner; caller-prepared systems |
| `sequence` | `biopython>=1.83,<2`, `biotite>=1.0,<2`, `parasail>=1.3.4,<2` | Optional sequence/structure adapters |
| `genomics` | `pysam>=0.22,<1` | Optional pysam/HTSlib stack |
| `chemistry` | `rdkit>=2023.9` | Optional chemistry adapter |
| `dev` | jsonschema, mypy, pytest, PyYAML, ruff, types-PyYAML, tomli | Development/validation tools |

`requirements-dev.txt` separately declares development tools and also includes `pre-commit`. This creates two sources of development dependency truth (the `dev` extra and requirements file); they should be reconciled or explicitly documented as intentionally different.

The source contains additional adapters for tools such as HMMER, BLAST+, Prodigal, AUGUSTUS, GROMACS, AlphaFold 3, ESM, Vina, OpenMM, RDKit, Biopython, Biotite, pysam/HTSlib, bcftools and samtools. These adapters have different operating models: some use optional Python distributions, some call host executables, some need operator-supplied model weights/databases, and some are local protocol/runner integrations. An adapter or registry entry does not prove the executable, database, model checkpoint, GPU or external service is installed or available.

No model checkpoint file (for example `.pt`, `.pth`, `.safetensors`, `.onnx`, `.ckpt` or `.h5`) appears in the audited tracked extension inventory. Model inference therefore depends on separately provisioned checkpoints and governed external databases where specified.

### SBOM limits

`scripts/generate_environment_sbom.py` inventories installed Python distributions and their declared `Requires-Dist` edges. It deliberately emits `NOASSERTION` for package licenses and does not attest hashes, publisher identity, OS/native libraries or executables. It is an installed-Python inventory, not a complete software supply-chain SBOM.

## 8. Licensing, data and model permissions

### Repository license

The root `LICENSE` is Apache License 2.0. This describes the repository's declared license; it does not automatically relicense third-party packages, external executables, datasets, scientific databases, model weights, fixtures or visual assets whose ownership/terms may differ.

### External dependencies and engines

The dependency policy requires purpose, exact version, license, security/maintenance state, transitive dependencies, deployment profile, egress and scientific scope to be reviewed before adoption. The current installed-environment SBOM does not establish those license or publisher facts. The full third-party license review remains open.

### Data catalogs

`data/public-dataset-catalog.yaml` and `data/admet-source-catalog.yaml` are metadata-only candidate catalogs. Their active `entries` arrays are empty, and candidate sources are marked `verify_before_intake`. They explicitly do not contain patient records or dataset payloads. The catalog lists are discovery leads, not approvals to ingest, redistribute, interpret clinically or train on the data.

### Model/data training authorization

The repository policy correctly states that access is not training permission. No blanket organizational-data training authorization is evidenced by the repository. Each source, dataset and checkpoint requires source identity, version, checksum, license/terms, privacy classification, intended use and redistribution/training permissions. The audit found no tracked model-weight bundle.

## 9. Duplicates, compatibility files and placeholder assessment

- The 11 small modules under `python/kinetics/` are explicit compatibility re-exports to canonical `python/molecularis/` modules. They are not empty implementations and should not be deleted without an API migration.
- The `python/kinetics/__init__.py` is a lazy compatibility namespace to avoid import-cycle regressions.
- The two zero-byte files are legitimate Python markers.
- The scientific tool registry and roadmap contain planned/candidate integrations; their documentation explicitly says they are not installation claims.
- The repository contains 124 declared implemented capabilities but no registry evidence-level promotion. This is an evidence gap, not proof that the source files are placeholders.
- A broad text search for `TODO`, `NotImplementedError`, `stub`, `placeholder`, `pass`, broad exception handling and subprocess patterns was used as a triage aid. Search hits require contextual review; words such as “TODO” can occur inside unrelated identifiers/URLs and broad exception handling may be intentional in validation/reporting code. This audit does not label all such hits as defects.
- No tracked files were deleted during SF0. In particular, Assets and compatibility files were preserved.

## 10. Documentation drift found

The existing `docs/P0_PLATFORM_AUDIT.md` describes a 2026-11-23 snapshot of 445 tracked blobs. The audited tree at HEAD `e36e327...` contains 464 tracked files. `docs/SERVICE_STATUS.md` states “Last verified: 2026-11-21”, which predates this audit. These documents must not be treated as current inventories without their snapshot dates.

The root README and governing master plan describe the intended architecture accurately at a high level, but the audit reinforces that intended architecture, implementation status, CI status and scientific evidence are four separate claims.

## 11. Findings and disposition

| ID | Finding | Severity | Required disposition |
|---|---|---|---|
| SF0-01 | 464-file inventory differs from the 445-file count in the prior P0 audit | Medium | Snapshot-specific counts recorded here; retain prior report as historical or reconcile it |
| SF0-02 | Service status last verified 2026-11-21 | Medium | Refresh only after exact-HEAD CI and implementation review |
| SF0-03 | 124 registry tools all have evidence level `none` | High | Add capability-to-test/reference/evidence mapping; do not equate implementation with validation |
| SF0-04 | Installed Python SBOM leaves licenses/hashes/publishers as NOASSERTION and omits OS/native tools | High | Add resolved package hashes, license review, OS/native inventory, vulnerability scan and attestations |
| SF0-05 | Dataset catalogs are candidate-only, active entries empty, terms pending | High | Complete per-source permission review before ingestion or training |
| SF0-06 | External engine availability is environment-dependent | High | Build deployment-specific tool inventory with version, digest, model/database and resource requirements |
| SF0-07 | Development dependencies are declared in both pyproject dev extra and requirements-dev | Low | Reconcile or document source-of-truth relationship |
| SF0-08 | Eleven legacy re-export modules remain under `python/kinetics/` | Low | Preserve for compatibility; define future deprecation/migration policy |
| SF0-09 | Current-HEAD CI evidence not available in the audit response | High | Run the full CI suite against this exact commit |
| SF0-10 | Test-file count does not provide line/branch coverage or scientific acceptance | Medium | Produce measured coverage and independent domain reference evidence |

## 12. SF0 gate decision

**Repository inventory and static dependency/governance baseline: COMPLETE.**

**P0 platform and scientific acceptance: NOT PASSED.** The following remain open and are not waived by this audit:

1. Exact-HEAD full CI execution and measured test coverage.
2. Capability-level evidence mapping and independent scientific reference validation.
3. Complete dependency/license/security/SBOM review including native executables.
4. Per-dataset and per-model permission verification.
5. Real sandbox integration, identity/approval enforcement, egress controls and recovery drills as listed in the P0 backlog.
6. Representative end-to-end cross-service typed handoff and provenance verification.

SF0 establishes what is in the repository and what the repository itself claims. It does not establish that all external tools are installed, all algorithms are correct, all data is licensed for training, or the platform is safe for restricted data.

## 13. Recommended next engineering order

1. Refresh exact-HEAD CI and static checks; record measured coverage.
2. Reconcile service/capability manifests with actual runtime registration and add evidence references.
3. Build a resolved software inventory for Python packages, native executables, containers, models and databases.
4. Review licenses and data/model terms before any ingestion or training.
5. Continue P0 integration, identity, isolation, egress, failure/recovery and provenance gates.
6. Only after P0 acceptance, proceed to Agentics orchestration maturity and the controlled training plan.

**Audit authority:** this document is the SF0 repository snapshot for HEAD `e36e32705045ab6311d20713d8f2a47b8c5af715`. Re-run the inventory whenever CORE advances materially; do not silently reuse these counts for a later commit.
