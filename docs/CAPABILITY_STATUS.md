# Molecularis — Capability and Migration Status

**Baseline:** CORE `dbda3496386edf46270d54296b2204a53d7de573`  
**Purpose:** Map existing repository assets to the new desktop-first delivery programme.  
**Status:** Initial source-tree mapping; per-capability runtime and scientific evidence audit remains Phase 0 work.

## Status vocabulary

- **Present / prototype:** source or UI asset exists.
- **Partial:** a bounded component exists, but a full user workflow or prerequisite is missing.
- **Planned:** no verified implementation was established in the baseline inventory.
- **Evidence:** source presence, tests, reference validation, platform validation and independent review are tracked separately.

## 1. Platform and shared foundations

| Capability | Current repository evidence | Baseline assessment | Migration action |
|---|---|---|---|
| Android client | Kotlin/Compose, Gradle, storage, workers, UI | Present; migration-critical | Preserve and keep build/tests until parity |
| Linux desktop client | No desktop application project | Not started | Build after five-platform framework spike |
| Windows desktop client | No desktop application project | Not started | Build with desktop foundation |
| macOS desktop client | No desktop application project | Not started | Build with desktop foundation |
| Android next-generation client | Existing client only | Migration target | Port after shared contracts and desktop proof |
| iOS/iPadOS client | No iOS project observed | Not started | Add native platform adapter/client after architecture gate |
| Cross-platform UI framework | No approved framework or five-platform spike | Not decided | Measure candidates; record owner decision |
| Shared Rust core | Rust directory placeholder only | Not started | Introduce only for justified safe parsing/supervision boundaries |
| Shared C++ engine | Android C++ probe only | Not started | Build only measured scientific kernels behind stable API |
| Python scientific layer | 51 modules under `python/molecularis/` | Substantial source present; mixed maturity | Preserve, test, modularize and expose through stable contracts |
| Portable project format | Multiple schemas/contracts and Android storage | Partial | Inventory stores; define versioned cross-platform project package |
| Provenance and capability registry | Registry, schemas, validation/governance records | Partial | Reconcile entries and attach verifiable evidence |

## 2. Scientific capability families

| Service family | Existing source | What is still needed |
|---|---|---|
| Sequence parsing and QC | FASTA/FASTQ modules, Android workers/cards, tests | Shared project integration, broader format/runtime tests and reference evidence |
| Sequence search and translation | Reference packs, exact search, genetic code, BLASTP, HMMER | Runtime manifests, datasets, resource profiles, end-to-end desktop workflow |
| Genomics and annotation | SAM/VCF, ORF, GFF3, HMMER, Augustus/Prodigal-related adapters | Curated references, coordinate/normalization review, complete workflows and independent concordance |
| Protein properties/design | Protein descriptors, motifs, design modules | Domain review, workflow UI, benchmarks and explicit uncertainty |
| Structure parsing | PDB geometry, sequence/structure mapping and structure-view payload | mmCIF edge cases, canonical identity/coordinate contracts and cross-platform fixtures |
| 3D structure viewing | Android viewer, offline HTML/CSS/JS assets, web viewer assets | Viewer choice/integration decision, feature audit, desktop/mobile rendering, large-file performance and accessibility |
| Structure alignment/pockets/quality | Python modules and tests | Reference comparisons; do not imply MolProbity equivalence |
| Protein prediction | Prediction-related contracts/modules | Real model runtime, weights/data rights, isolated profiles, benchmarks and calibration |
| Chemistry | SDF parser and optional RDKit adapter | Pinned supported runtime, complete input/output workflow, edge-case references |
| Docking | Vina runner, schema and bounded Node service | Receptor/ligand preparation, runtime profiles, reproducibility, reference benchmark and security review |
| Molecular dynamics | OpenMM adapter and smoke/reference script | Trusted preparation pipeline, force-field/ligand parameter provenance, reference systems and resource validation |
| Omics/phylogeny/PKPD/PGx | Multiple Python modules and schemas | Evidence-led domain audits, curated references and research-only boundaries |
| DNA/RNA nanostructures | No complete workflow established | Exact NUAD source/licence review, thermodynamic dependencies and validated workflow |
| Notebooks/workflow federation | Workflow modules and SciREPL/Galaxy references in docs | Isolated execution model, durable manifests, security review and justified federation |

## 3. External integration candidates

Candidate projects: Biotite, Mol*, MolProbity, RDKit, OpenMM, ESM, AlphaFold, Genome-Wide Workbench, Open Chemistry, ChemGraph, NUAD, Galaxy and SciREPL.

No candidate is considered integrated merely because it appears in a plan. Exact upstream commit, release, component, licence, dependencies, model/data terms, supported OS/ABI, adapter, tests, benchmarks and removal plan are mandatory before adoption. NUPACK is a separate licence/integration review from NUAD.

## 4. Required Phase 0 reconciliation

For each of the 130 registry entries:
1. verify referenced implementation path exists;
2. inspect implementation and public entry point;
3. map unit/integration tests and CI job;
4. identify optional dependency and supported runtime;
5. identify schemas and stable IDs;
6. classify source state: prototype, partial, integrated or absent;
7. record evidence level E0–E5;
8. record platform status independently;
9. identify migration target and compatibility requirements;
10. update registry and this status record from evidence, not assumptions.

The initial registry count (68 implemented, 62 planned) must not be used as a progress percentage. The 68 source-present entries currently carry `evidence_level: none`.
