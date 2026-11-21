# Molecularis — Desktop-First Roadmap

**Status:** Owner-directed target roadmap for Alpha; integration into CORE proceeds through reviewed PRs. Milestones are plans, not completion claims.  
**Updated:** 2026-11-21

## Product direction

Molecularis is an installed, desktop-first scientific research application. First delivery targets are Linux, Windows and macOS desktop applications. Android and Apple iOS/iPadOS applications are required next, sharing domain logic, contracts, project formats and provenance. A website/PWA is not the first product and may be considered later as a companion only.

## Current baseline and evidence

The repository contains established Android/Kotlin/Compose and Gradle material, Python scientific packages/tests, Rust and C++ native components, Node utilities, versioned JSON Schema contracts, capability catalogues, scientific rulebooks, validation plans, provenance/governance records and scientific adapters. These are foundations to audit, not proof of cross-platform readiness.

Alpha and CORE diverged from merge base `b038ef1065dd163108bd591e5e3a7e4c0d7b438d` at the audit snapshot. Do not force-reset either branch. The Alpha baseline audit records exact SHAs, CI evidence and M0 gaps.

## Milestones

| ID | Milestone | Exit evidence |
|---|---|---|
| M0 | Baseline and branch governance | Exact SHAs, inventory, CI baseline, risk register, compatibility and migration ledger |
| M1 | Cross-platform framework feasibility | Measured vertical slice on Linux, Windows, macOS, Android and iOS/iPadOS; accessibility, graphics, packaging, licensing comparison; owner decision |
| M2 | Desktop application foundation | Installable Linux/Windows/macOS shell, design system, local projects, settings, offline workflow |
| M3 | Shared domain and local execution | Versioned project/artifact/provenance contracts, local job supervisor, first end-to-end scientific vertical slice |
| M4 | Desktop release engineering | Reproducible builds, signing, updates, rollback, install/upgrade/uninstall, filesystem and GPU/3D validation on all desktop OSes |
| M5 | Mobile application foundation | Android and iOS/iPadOS vertical slices, shared data format, lifecycle, permissions, offline and accessibility tests |
| M6 | Compute and collaboration extensions | Optional Molecularis Node, hosted workers and institution/HPC connectors with explicit policy and threat models |
| M7 | Scientific data and visualization | Canonical entities, units, coordinate frames, schemas, Mol* integration and contract tests |
| M8 | Sequence/genomics | Biotite and GWW selective adapters, reproducible workflows |
| M9 | Protein models | ESM and AlphaFold isolated profiles, model/data terms and benchmark gates |
| M10 | Structure validation | MolProbity methods/adapters in audited isolated worker |
| M11 | Chemistry | Open Chemistry components and ChemGraph workflows with reviewable inputs |
| M12 | Molecular dynamics | OpenMM setup, force-field provenance, simulation, analysis and benchmark gates |
| M13 | Notebooks and workflow federation | SciREPL-inspired notebooks and Galaxy API/federation |
| M14 | DNA/RNA nanostructure | NUAD workflows and separate NUPACK license/integration review |
| M15 | Institutional readiness | HPC connectors, deployment, monitoring, backup/restore, security and independent validation |

## Delivery sequence

M0–M4 establish desktop foundations, cross-platform architecture and local scientific execution. M5 extends the same product to mobile. M6 adds optional compute federation. M7–M14 deliver scientific vertical slices in dependency order. M15 prepares institution-scale operations and release acceptance. Parallel work is allowed only when dependencies and shared files are controlled.

## Definition of done

A milestone is done only when code, tests, schemas, docs, exact-head CI, security review (where relevant), scientific evidence (where relevant), platform-specific install/runtime/accessibility evidence and owner acceptance are recorded. A passing build is not proof of scientific validity, device support or release readiness.

## Historical work

Previous R/S/I/P/G/U tracks and detailed plans remain evidence sources until the baseline audit classifies each artifact as current, superseded, historical or needs-review. Preserve evidence and map its obligations into these milestones; do not carry old completion claims forward without exact evidence.


---

## Historical CORE roadmap (preserved, not Alpha execution authority)

# Molecularis — Roadmap
**Status:** R implementation/host audit closed; S1–S10 bounded software scope closed; I1–I5 bounded software scope closed; Track P bounded research-only software foundation closed; **Track G bounded G0–G7 engineering foundation closed** on exact-head CI workflow [#44108451571](https://github.com/AssayFlux/Molecularis/actions/runs/44108451571) for `31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1` (9/9 jobs passed). Full P and overall G acceptance remain open because external scientific, source/licensing, ethics, privacy/security, regulatory, operational and device evidence is not complete.
**Last updated:** 2026-11-17  
**Statuses:** not-started | in-progress | blocked | done | dropped  
**Owners:** Project owner = repository owner; Engineering = implementation contributor. Dates are review/target dates, not completion claims.

The 2026-11-12 [repository research-readiness audit](docs/research-grade-readiness-audit-2026-11-12.md) records documentation and structure findings; its recommendations do not change the owner-approved track order or safety gates.

This roadmap operationalises the archived master. A phase is complete only when exit evidence exists in the repository and required owner approval is recorded.

## Current position
- Track R / R0 Foundations: owner accepted the R0 exit and authorised R1 on 2026-11-07; R0 is done.
- The owner-approved direction baseline and reconstructed historical master are present; NORTH_STAR was not changed.
- Repository skeleton, capability registry/checker/tests, reproduction stub, pre-commit configuration, CI and governance metadata are committed.
- R0 accepted by the owner when they authorised R1 on 2026-11-07. CI evidence: [R0 workflow run](https://github.com/AssayFlux/Molecularis/actions/runs/42378815901).
- D-023 (2026-11-12) is the current sequencing authority: **R → S → I → P → G → U**, with the same two-step build-then-audit gate for every track. It supersedes D-019's earlier five-track order while preserving D-019 as historical decision evidence. On 2026-11-09 the owner confirmed R complete for sequencing purposes and directed S1–S10 before I; S software scope and the I1–I5 software implementation/integration audit were subsequently closed for their bounded software scopes, and Track P was started under explicit owner authorization. S and I external scientific-validation, licensing and device obligations remain carry-forward items. D-021 defers specified external biological-validation, licensed-resource/model and physical-device requirements as carry-forward deliverables, but does not waive missing software implementation. R device/scientific/licensing/release evidence remains a carry-forward obligation. D-016 requires exact-source build/test evidence for every substantial increment; build success does not replace runtime, scientific or device validation.
- Track P bounded software foundation: P1/P2 synthetic-only QC/parser/matcher foundations and P3–P7 research-only schemas/contracts are implemented. Exact-main-head workflow [#44078534173](https://github.com/AssayFlux/Molecularis/actions/runs/44078534173) passed 9/9 jobs on `7967ccb0288ea1d5b82af18f8ab8d886d18d4733`; Python 534 passed, 9 skipped, Ruff and strict mypy passed, and Android arm64 APK/AAB packaging plus JVM tests passed. **Software foundation closed; full Track P remains open.** P0 is NOT APPROVED; independent scientific/source/licence/device and all operational/external gates remain open.
- Track G's G0–G7 bounded research-only engineering foundation is **CLOSED** on exact main commit `31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1`; exact-head workflow [#44108451571](https://github.com/AssayFlux/Molecularis/actions/runs/44108451571) completed successfully with **9/9 jobs passed**, including Android arm64 APK/AAB build, package alignment and JVM tests. Python: **536 passed, 9 skipped**; Ruff, mypy, governance checks and claims-matrix reproducibility passed. The capability claims matrix contains 68 executable tool capabilities (not 130 UI+tool entries). Overall G acceptance remains OPEN: independent security/privacy/scientific/legal reviews, complete SBOM and license clearance, device verification, owner policy acceptance, named specialist roles, and operational exercises remain outstanding. P0 remains NOT APPROVED. **Track U is the sixth and final sequential track, after G.** Existing partial U0–U3 work is retained; further U implementation waits until G's two-step engineering gate is assessed and reported.
- D-005 is approved as a broad strategic direction: build both a comprehensive, expandable PGx gene panel and a broad cross-domain gene catalogue. Treat PGx as a specialised workstream within the wider catalogue, with separate evidence and validation gates. The earlier six-gene list is not a scope limit; exact inventories and rollout waves remain evidence-led. No exhaustive panel coverage or clinically validated PGx implementation is claimed; current parser/matcher foundations remain synthetic/research-only. D-004 is approved: defer clinical-adviser recruitment until the research platform is more mature (target review after R3); P0 and all patient/clinical work remain blocked until qualified advisers and all other prerequisites are in place. D-003 (publication strategy) is approved: multiple papers over time, beginning with an evidence-backed platform/software-methods paper after R1–R3 readiness, followed by independently validated domain papers. D-001 (project license) is approved as Apache-2.0; D-002 sets a global long-term ambition including future clinical use, subject to jurisdiction-by-jurisdiction advice and approvals. The canonical Apache-2.0 LICENSE grant file is present at the repository root; the third-party dependency audit remains open.

## Track R — Research platform
| ID | Scope | Dependencies | Exit gate | Status | Owner | Date |
|---|---|---|---|---|---|---|
| R0 | Skeleton; direction files; owner-selected license (do not choose); CI lint/type/tests/native builds/16 KB/size budgets; pre-commit; registry/checker; reproduce-all stub | Direction approval | Empty-skeleton CI green; registry checks/tests; honest blocked checks; stop | done | Engineering + owner | 2026-11-07 |
| R1 | Android arm64 feasibility: embedded Python/Biopython/NumPy/SciPy, Rust FFI, C++ JNI, real scientific engine, RDKit/alternative, offline viewer, 16 KB, local APK/AAB build, SAF/lifecycle, cold start and memory | R0 approved | Reproducible arm64 APK/AAB build evidence, complete feasibility matrix and explicit owner go/no-go; CI build is not device-runtime evidence | implementation and host audit step closed; exact-source CI #2126 on `888e49b` passed all five jobs. APK 69,891,771 bytes (SHA-256 `73e66bacb3d1e45e8928c52c10b3fed14e29aa71c8e09a8df73945ffef24aa06`), AAB 39,953,771 bytes (SHA-256 `a851cdeaf921e8b8b40dd82184fb2ef8200bc7b660ab32c80da448cd22d5aadf`); JVM tests and static alignment passed. Physical-device runtime, embedded Python/Rust/JNI invocation, SciPy/device packaging decision, engine/viewer selection, performance and transitive license review remain open | Engineering + owner | 2026-11-08 |
| R2 | Compose, SQLite, SAF, provenance, cancellable/resumable WorkManager, registry, pack manager, Keystore encryption | Integrated R1 architecture findings; validation remains gated | On-device import, cancellable/resumable job, provenance inspection, security review | in-progress — Compose/SQLite/SAF/WorkManager import; resumable AES-GCM chunks, transactional import provenance, verified cache/export and Keystore-loss preservation; R Step 1 adds a bounded authenticated imported-FASTA WorkManager analysis path with transactional result/provenance storage and job-card inspection; analysis-result SAF JSON export is implemented; Robolectric fresh-install and v1→v4, v2→v4 and v3→v4 migration cases passed exact-source CI #2104; added WorkManager worker fail-closed tests for malformed/missing IDs, unknown jobs, over-limit imports and FASTQ gating (guard tests now seed committed-row metadata to exercise the intended preflight branches without Keystore/decryption; corrected tests passed exact-source CI #2126; Android device/runtime and process-recovery tests remain open; cancellation persists a resumable terminal state; new report-only encrypted orphan inventory scans unreferenced finalized/partial ciphertext without deleting it, with JVM tests for active, missing-job, stale-partial and symlink cases; interrupted-export provider behavior, migration fixtures and device verification remain open | Engineering | 2026-11-08 |
| R3 | v0.1 alpha: sequence tools, protein properties, enzyme kinetics and independent-reference validation | R2 integration; scientific validation remains gated | Offline end-to-end alpha, independent validation records and owner-approved v0.1 gate | in-progress — sequence/protein/kinetics primitives and diagnostics; pinned host-only SciPy comparison now runs on deterministic synthetic cases in CI; experimental reference validation, calibrated uncertainty and app integration remain open | Engineering + Validation | 2026-11-08 |
| R4 | Rust FASTA/FASTQ/SAM/BAM/VCF, QC, trimming, k-mers | R2/Rust feasibility | Reference concordance, bounded memory, device benchmarks | in-progress — wrapped FASTA/FASTQ parsing, FASTA QC and explicit-Phred FASTQ read-quality cards are connected to Android Explore through Chaquopy; R Step 1 adds bounded authenticated imported-FASTA analysis with durable SHA-256-linked result records, job-card inspection and SAF JSON export; Step 2 audit adds export-time source-digest revalidation and bounded result/preview guards (latest audit CI #2126 passed); exact-source ARM64 APK/AAB, JVM tests and host regression suite passed CI #2101; Robolectric SQLite fresh-install and v1→v4/v2→v4/v3→v4 migration tests passed CI #2104; imported FASTA result/export integrity and private plaintext cleanup tests are present; strict SAM/VCF end-to-end workflows, core BAM limits, CRAM Android, adapter trimming, Rust acceleration and on-device Chaquopy execution remain open | Engineering + Validation | 2026-11-08 |
| R5 | PDB/mmCIF, secondary structure, RMSD, contacts, SASA, H-bonds, salt bridges, disulfides | R2/licensed reference set | Fixed PDB benchmark/tolerances | in-progress — PDB/mmCIF atom-site parsing, contacts, superposed RMSD, approximate SASA and distance-only interaction-candidate screening; synthetic Biopython/NumPy PDB/contact/RMSD software comparison passed CI #2105; experimental structures, full mmCIF semantics, SASA/interaction concordance, viewer and device evidence remain open | Engineering + Validation | 2026-11-08 |
| R6 | Chemistry formats/descriptors/fingerprints/similarity/substructure; PCR/plasmid/cloning/CRISPR rules | R1 chemistry feasibility/license review | Tests, benchmarks and license approvals | in-progress — multi-record SDF V2000/V3000 subset parsing, new incremental SDF stream ingestion with positive-integer record/record-size/aggregate-size budgets, graph descriptors, bounded substructure matching and exploratory fingerprints; stereochemistry, aromaticity and production engine open | Engineering + Validation | 2026-11-08 |
| R7 | Search, phylogenetics, evolution; Tier B local/Tier C node; viewers/conservation/logos | R2/engine and license approvals | Reference concordance, offline viewer and node security tests | in-progress — quoted-label Newick, UPGMA/NJ, Jukes–Cantor distances and seeded site-bootstrap split support; ML/Bayesian inference, search, viewers and node security open | Engineering + Validation | 2026-11-08 |
| R8 | Omics, microbiology, systems, multi-omics and statistics | R2/datasets/R reference CI | Reproducible reference comparisons | in-progress — finite-input-checked CPM/CLR, Pearson/cross-omics correlation, fold change, logistic growth, Shannon/Gini-Simpson diversity and exploratory Welch/BH differential expression; count-model inference and broader multi-omics open | Engineering + Validation | 2026-11-08 |
| R9 | Domain rollout in waves of 10–20; preserve supplied definitions; coverage reports | Registry and capabilities | Implemented only when a tool works and is tested | in-progress — full 16-column NCBI Gene annotation ingestion/search from plain/gzip streams; new snapshot-scoped coverage/composition report with no invented completeness denominator; comprehensive PGx allele definitions and domain data packs remain open | Engineering | 2026-11-08 |
| R10 | Accessibility, low-end performance, crash testing, privacy/data safety, signed AAB, honest listing, owner-approved distribution channels (GitHub release assets and/or F-Droid only after channel review) | R3/G1–G4 | Publishing checklist, automated hardening, signed release evidence and owner release approval | in-progress — capability implementation-path integrity checks, authorized CI APK/AAB build lane plus accessibility/security/release gates, and accessibility/security/release gates retained; full hardening remains open | Engineering + owner | 2026-11-08 |

v0.1.0 = R0–R3.

## Track S — Structure excellence, protein intelligence and discovery

**Sequencing gate — CURRENT (D-023, 2026-11-12):** Execute tracks strictly **R → S → I → P → G → U**, with exactly two steps per track: (1) build the documented base; (2) audit, test and fix the remaining base gaps. D-019 records the previous five-track order and is superseded only as to the current track list/order; its two-step model remains in force. D-020's R audit/authorization of S remains historical evidence, and all R/S/I external scientific, licensing, device and release obligations remain carry-forward items. The 2026-11-08 parallel S authorization is historical and superseded. Existing partial U0–U3 implementation is retained, but further sequential U implementation begins only after G's two-step gate is assessed and reported. No phase exit evidence or clinical gate is waived.

| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| S1 | Offline-first Canvas 2D structure viewer, bounded PDB/mmCIF SAF import, provenance and JSON session export | R1 WebView, R2 | Offline asset parity/security tests, import/export build and preparation provenance; device verification remains separate | software integrated — dependency-free Canvas renderer, exact Android/web asset parity, hardened local-only WebView, bounded SAF import (16 MiB), strict UTF-8, Python parser/provenance handoff, JSON session export and bounded PNG snapshot export; physical-device import/export, screenshots, accessibility and performance remain carry-forward evidence | Engineering | 2026-11-10 |
| S2 | Geometry/torsion metrics; quality badge only after calibration | S1, fixed experimental structures | Independent geometry concordance, calibrated thresholds and explicit abstention | software implementation complete — bounded clash screening and phi/psi evidence with conservative abstention; no calibrated grade or Ramachandran classifier is enabled; calibration remains a carry-forward gate | Engineering + Validation | 2026-11-09 |
| S3 | Variant mapping, interface contacts and pocket candidates | S2, variant evidence | Capability validation; evidence not verdict | software implementation complete — exact/alignment-aware coordinate mapping with tie abstention, heavy-atom inter-chain contacts, bounded explicit-ligand proximity and apo-concavity candidate screens; insertion-code/alternate-location semantics, full chemical-component handling and independent structural validation remain carry-forward gates | Engineering + Validation | 2026-11-11 |
| S4 | Approved model prediction, confidence provenance and experimental comparison | Node security, code/weights licenses | Reproducible benchmark and calibrated confidence | software adapter implemented — hash-pinned local process protocol, bounded request/response, executable/weights digests, provenance equality and strict envelope validation; approved model/runtime/weights, secure node and calibrated benchmark remain deferred gates | Engineering + Validation | 2026-11-10 |
| S5 | Viewer session export and structure benchmark | S1–S4 as applicable | Deterministic export, benchmark-generated figures and device verification | software implementation includes bounded provenance-bearing JSON session export, Android SAF PNG/SVG snapshot export and persisted interactive-view state; exact-head CI passed; physical-device/benchmark evidence remains a carry-forward gate | Engineering + Validation | 2026-11-11 |
| S6 | Unknown-sequence triage, protein family/domain/motif search and evidence-ranked annotation | R4; versioned local reference packs | Curated positive/negative fixtures, reference concordance, calibrated thresholds, resource bounds | software workflows implemented — bounded FASTA/FASTQ and local packs, exact triage, Smith–Waterman, motif scanning, hash-pinned local BLASTP and HMMER hmmpress/hmmscan runners; curated/licensed databases, calibrated thresholds and independent concordance remain deferred | Engineering + Validation | 2026-11-10 |
| S7 | Prokaryotic and eukaryotic genome annotation pipelines, gene discovery and provenance | R4; S6; organism-specific references | Curated genome truth sets, coordinate/strand concordance, transcript and annotation review | software adapters implemented — bounded genome-wide ORF triage, Prodigal prokaryotic and AUGUSTUS eukaryotic local runners, generic GFF3 annotator integration, GFF3 hierarchy import and strand/phase-aware CDS reconstruction; approved species models, curated truth sets and accuracy validation remain deferred | Engineering + Validation | 2026-11-10 |
| S8 | Non-standard genetic-code investigation and translation-table candidate inference | S6–S7; organism-specific truth sets | Independent reference validation, confusion matrices, calibrated abstention and ambiguous-case tests | software implementation complete — bounded candidate ranking across supported NCBI tables using supplied coding-frame/internal-stop and optional complete-CDS start/terminal-stop evidence, with minimum evidence and margin-based abstention; taxonomic/codon-usage/homolog evidence, organism truth sets and calibration remain carry-forward gates | Engineering + Validation | 2026-11-11 |
| S9 | Protein sequence/domain/family intelligence and sequence-to-structure mapping | S1, S6, R5; licensed reference sets | Independent annotation comparisons, residue-mapping tests and model-vs-experiment provenance | software evidence pipeline implemented — descriptors, motifs, sequence/structure mapping, geometry/interfaces, HMMER domain evidence parsing and explicit-threshold candidate ranking; licensed profile sets, calibrated family/function assignment and independent annotation concordance remain deferred | Engineering + Validation | 2026-11-10 |
| S10 | Constrained de novo protein design research, candidate ranking and experimental validation workflow | Model/data license approval, secure compute/node, biosafety review, S6/S9 | Reproducible generation, held-out benchmarks, prospective wet-lab validation and owner approval | blocked — deterministic non-generative design-brief validation with mandatory human review exists; generation is disabled pending approved model/data licenses, secure compute, benchmarks, biosafety and wet-lab plan | Engineering + Validation + Owner | 2026-11-09 |

## Parallel execution and publication evidence

The owner briefly authorized parallel R/S/I/P work on 2026-11-08; that sequencing permission was explicitly superseded by D-019 on 2026-11-09. D-023 now controls the current order: **R → S → I → P → G → U**. The historical protocol is retained at [docs/parallel-track-execution.md](docs/parallel-track-execution.md) for audit only. Manuscript and claim/evidence records remain subject to their publication gates. P0 remains blocked; only non-patient public-data preparation is permitted before its formal gate.

## Track I — In-silico lab

**Software exit: CLOSED** on 2026-11-11 at exact main source `aabe37808a5494acb2171b6ed71d2661b4dd2453`; [workflow #42970328048](https://github.com/AssayFlux/Molecularis/actions/runs/42970328048) passed all 9 jobs. Closure covers the documented I1–I5 software foundations, contracts, bounded inputs/outputs, provenance, regression tests, Android integration preview and host-side engine/utility adapters. It does **not** claim real-world scientific validation, external-data/model qualification, licensing approval, production node deployment or physical-device acceptance. Those remain open real-test gates.

| ID | Scope | Dependencies | Software exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| I1 | Ligand prep, descriptors, drug-likeness | R1 chemistry/license | Host RDKit sanitization/descriptors/Morgan fingerprints and pinned ethanol/benzene references; bounded Android SAF SDF/MOL graph-only preview, provenance and explicit limitations; Python and Android contract tests | **software closed**; broader curated chemistry references, physical-device import/runtime and Android RDKit ABI/size/licence decision remain open |
| I2 | Node docking/virtual screening | Node, approved licenses | Pinned AutoDock Vina 1.2.7 prepared-PDBQT runner, bounded protocol, hashes and strict result envelope; disabled-by-default authenticated Node 22 worker with loopback-first/TLS remote boundary, request limits and security tests | **software closed**; approved node deployment, complete transitive binary SBOM/licence review, independent redocking/cross-docking RMSD and decoy enrichment remain open |
| I3 | Node MD | Node, engine/model/license | OpenMM 8.6.1 CPU runner for trusted constructed systems, bounded replicas/trajectories, provenance and deterministic signed-32-bit per-replica seeds; synthetic harmonic-system smoke | **software closed**; approved biomolecular force-field/parameter source, secure compute, timestep/equilibration convergence, energy/stability and independent biomolecular references remain open |
| I4 | ADMET and PK/PD/PBPK | Approved data/models | One-compartment oral PK and Emax references; SciPy DOP853 comparisons; scaffold-group split, binary metrics/calibration and Morgan/Tanimoto applicability-domain utilities with strict limits and schemas | **software closed**; approved data licences/intake, trained model, external held-out validation and PBPK evidence remain open |
| I5 | Variant-effect and virtual-cohort simulations, Research Mode | I4, fairness/model review | Seeded aggregate Hardy–Weinberg synthetic cohorts and caller-supplied additive-effect simulations; strict schema, reproducibility, count conservation and aggregate-only tests | **software closed**; governed cohort intake, population/fairness/portability review and independent variant-effect validation remain open |

### Exact-head software verification (2026-11-11)
- Source: `aabe37808a5494acb2171b6ed71d2661b4dd2453`.
- Workflow: [#42970328048](https://github.com/AssayFlux/Molecularis/actions/runs/42970328048), completed successfully; **9/9 jobs passed**.
- Python suite: **490 passed, 9 skipped**; Ruff and strict mypy passed.
- Android: arm64 debug APK/AAB packaging, package checks, JVM tests and 16 KB native alignment checks passed. Artifact: [debug build bundle](https://github.com/AssayFlux/Molecularis/actions/runs/42970328048/artifacts/13832813087), 80,653,407 bytes.
- Pinned RDKit descriptor references, Vina engine smoke, OpenMM synthetic CPU replica smoke, ADMET utility smoke, host scientific-reference comparisons, Node docking-worker security tests and declared source SPDX inventory passed.
- These are automated software/host checks. Engine smoke is not a biological benchmark; APK packaging is not a physical-device install/runtime test; source SPDX is not complete transitive binary/model/data licence approval.

### I-track real tests and acceptance — OPEN
1. I1: wider independently curated chemistry references and named Android-device install/import/export/runtime.
2. I2: independent redocking/cross-docking and decoy-enrichment benchmarks; approved secure-node deployment and full transitive binary provenance/licence review.
3. I3: licensed biomolecular force-field/parameter sources; representative stability, energy conservation and timestep/equilibration/replica convergence with independent review.
4. I4: approved/licensed dataset intake, trained-model provenance, leakage-controlled external test sets and independent performance/calibration review. PBPK remains outside implemented scope.
5. I5: governed public-cohort approvals, population/fairness/portability evaluation and independent effect-model validation.
6. Cross-cutting physical-device acceptance, third-party licence approval, security review and owner acceptance remain open. P0 and patient/clinical workflows remain blocked.

**Disposition:** I1–I5 software implementation and integration audit is **CLOSED**. Real scientific, device, licensing, data/model and secure-node acceptance is **OPEN**. Do not label I-track scientifically validated or production-ready.

## Track P — Precision Medicine (PGx First)
**Track P STARTED — 2026-11-11, by explicit project-owner authorization.** The bounded P1–P7 research-only software foundation is **CLOSED** following exact-head verification on 2026-11-17 (workflow [#44078534173](https://github.com/AssayFlux/Molecularis/actions/runs/44078534173), 9/9 jobs passed). **The full Precision Medicine track is NOT CLOSED:** P0 remains **BLOCKED / NOT APPROVED**, and external/scientific/source/licensing/operational/device acceptance evidence remains outstanding. The software closure does not authorize patient data, human-subject activity, individual interpretation, clinical recommendations or Clinical Mode.

Public-data preparation increment: `data/public-dataset-catalog.yaml` separates candidate source discovery (NCBI Gene, PharmVar, ClinVar, CPIC; all `verify_before_intake`) from acquired dataset entries (`entries: []`). A strict schema plus `scripts/check_public_dataset_catalog.py` enforce non-patient metadata, pinned hashes/timestamps, licence-review evidence and non-clinical intended-use boundaries; synthetic tests run in CI. No data payloads are present; this does not authorize intake or lift P0.
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| P0 | Intended use; legal/ethics/regulatory advice; qualified advisers; privacy/security/QMS and validation evidence | G1–G3 planning | Complete evidence packet, applicable external determinations/reviews, unresolved-risk disposition and explicit owner gate decision | blocked — engineering drafts prepared; external legal/ethics/clinical/privacy/security/regulatory determinations, independent review and formal P0 decision outstanding; NOT APPROVED | Owner + qualified advisers | 2026-11-17 |
| P1 | Genotype ingest/QC/annotation/build handling, Research Mode, public data | Public-data-only preparation may proceed within P0 boundary; any patient/human data and clinical interpretation require P0 plus their own gates | Pinned builds, thresholds and independent concordance; no patient data | software foundation closed — metadata-only candidate catalogue, synthetic reference/normalization and bounded aggregate VCF QC verified on exact head; acquired entries remain empty; independent authoritative concordance, exact-source terms review, fuzzing and device workflow remain open | Engineering + Validation | 2026-11-17 |
| P2 | PGx allele-definition and phased-haplotype research foundation; comprehensive panel remains staged | P1, exact-source licensing, established-tool review | Synthetic regression tests, then licensed reference concordance; ambiguous/incomplete never guessed | software foundation closed — provenance-aware bounded PGx/PharmVar parsers and conservative phased matcher pass synthetic tests on exact head; no licensed source pack, broad gene coverage, clinical caller, diplotype/phenotype inference or treatment output | Engineering + advisers | 2026-11-17 |
| P3 | Research-only versioned guideline evidence metadata contract | P2, exact guideline licence and independent mapping review | Schema/negative tests; approved source mapping and wording review | software contract closed — schema and negative cases are in the exact-head CI; no licensed guideline corpus or executable recommendation mapping | Engineering + advisers | 2026-11-17 |
| P4 | Human-curated variant evidence record contract | P1, evidence-source licence review and curator appointment | Schema/negative tests; operational two-reviewer workflow and adjudication audit | software contract closed — evidence-backed second-review states are enforced by schema; no qualified curator appointments or operational adjudications | Engineering + curators | 2026-11-17 |
| P5 | Ethics/adviser protocol preparation | P3–P4, competent ethics determination and required approvals | Completed approved protocol and actual review/study evidence | template foundation closed — protocol template exists; no ethics submission/determination, recruitment or human-subject study | Owner + advisers | 2026-11-17 |
| P6 | Risk/control and jurisdiction-review contracts; internal validation planning | P0–P5, qualified legal/privacy/security review | Verified controls, independent validation, residual-risk disposition and owner acceptance; Clinical Mode off | software contract closed — risk/control schema and evidence requirements pass CI; no completed risk ratings, independent assessments or accepted residual-risk dossier | Engineering + advisers | 2026-11-17 |
| P7 | Regulatory and prospective-evaluation preparation | P6, qualified jurisdiction advice and ethics approvals | Written classification/strategy, approved protocol, prospective evidence and release authorization | software contract closed — jurisdiction evidence contract passes CI; no qualified advice, regulator engagement, ethics approval or prospective evidence | Owner + advisers | 2026-11-17 |
**Track P bounded software-scope disposition (2026-11-17): CLOSED.** This closes implementation and automated verification of the documented research-only software foundation, not the full P0–P7 acceptance programme. P0 and all independent source, biological, ethics, legal, privacy/security, QMS, regulatory, operational-curation, device and owner-acceptance gates remain OPEN. Do not interpret this software closure as clinical readiness or authorization.
Further disease areas only after P7 evidence, one at a time.

## Track G — Governance, assurance and publication readiness
**Engineering status (2026-11-17):** G0–G7 research-only governance software foundations are implemented and exact-head automated checks pass on workflow [#44098272029](https://github.com/AssayFlux/Molecularis/actions/runs/44098272029), 9/9 jobs. **Overall Track G acceptance remains OPEN**: owner policy acceptance, qualified role appointments, independent security/scientific/privacy/legal reviews, complete dependency/license clearance, device tests, operational exercises, manuscript declarations and external decisions are not recorded. This does not authorize patient/clinical workflows or release.
| ID | Scope | Dependencies | Exit evidence | Status | Owner | Date |
|---|---|---|---|---|---|---|
| G0 | Governance map, stable controls, claims register, roles and traceability | R/S/I/P evidence | Complete control/evidence index, exact-head checks, owner policy acceptance and named roles | engineering foundation verified; owner acceptance and role appointments OPEN | Owner + Engineering | 2026-11-17 |
| G1 | Security assurance, threat model, abuse cases and vulnerability response | R0; P0 before sensitive data | Security tests, device evidence, private reporting exercise, independent assessment and retest | engineering specification and configuration checks present; fuzz/device/private-channel/independent assessment OPEN | Engineering + independent assessor | 2026-11-17 |
| G2 | Licensing and software supply-chain evidence | R0; before bundling | Resolved dependency graph, artifact hashes, full SBOM, upstream license/notice review and owner bundle decisions | source SPDX plus raw Gradle/Cargo/Python-wheel evidence captured; complete SBOM, transitive/file-level license review and approvals OPEN | Engineering + qualified reviewer | 2026-11-17 |
| G3 | Software quality lifecycle, traceability, change control and CAPA | P0 planning | Requirements-to-test links, review/change records, CAPA effectiveness and owner-approved release controls | structural traceability/checker and CAPA template verified; QMS advice, reviews and operating records OPEN | Owner + quality adviser | 2026-11-17 |
| G4 | Privacy, data governance, retention, deletion, backup and export | P0 before personal/human data | Source and merged-manifest inventory, provider/device tests, qualified privacy advice and owner decisions | source-level 8-flow inventory and configuration checks present; device verification and legal/privacy determinations OPEN | Engineering + qualified privacy adviser | 2026-11-17 |
| G5 | Scientific integrity, capability claims, uncertainty and bias/coverage | R/S/I/P evidence | Reproducible claim matrix, independent truth sets, subgroup/coverage analyses and reviewed limitations | generated 68-tool conservative claims matrix reproducible; independent validation, ancestry/bias analysis and domain review OPEN | Research + independent reviewers | 2026-11-17 |
| G6 | Publication and research integrity | R/S/I/P evidence | Claim-to-evidence ledger, reproducible literature review, author/contribution/COI approvals and journal decision | publication protocol and ledger structure present; ledger has no supported claim rows, author declarations/literature review/peer review OPEN | Research + all authors | 2026-11-17 |
| G7 | Incident response, stop-work, access, backup/recovery and periodic review | G0–G6 | Named operators, tested tabletop/access/recovery exercises and dated review records | procedures and five tabletop scenarios documented; exercises and operator appointments NOT RUN/OPEN | Owner + appointed operators | 2026-11-17 |

## Gene strategy (D-005 — approved strategic direction)
- Build both a comprehensive, expandable PGx gene panel and a broad cross-domain gene catalogue spanning genomics and relevant Molecularis domains.
- The cross-domain catalogue is the wider inventory; PGx is a specialised workstream within it. Maintain separate domain annotations, reference datasets, caller/assay requirements, interpretation rules and validation status.
- The earlier six-gene list is not a scope limit. Do not invent a target count or claim exhaustive coverage; define versioned inventories and prioritised implementation waves from scientific relevance, evidence, reference availability, locus/caller feasibility, ancestry coverage, licensing, compute/device constraints and independent validation.
- A gene's presence in the catalogue does not imply that a caller, assay, interpretation or clinical workflow is implemented or validated.
- PGx remains research-only and gated by qualified advisers, P0, jurisdiction-specific legal/ethics/regulatory requirements and owner approval. No patient-data or clinical work is authorized.

## Clinical adviser timing (D-004)
- Defer clinical-adviser recruitment during the current R1 engineering-feasibility phase.
- Revisit after the research platform reaches a meaningful maturity milestone, with a target review after R3.
- Recruit/engage qualified clinical expertise before P0, PGx gene-set selection or any patient-related, clinical-study or clinical-scope work. P0 remains blocked until its full gate packet and owner approval are complete.
- This is a timing decision only; it does not relax safety, legal, ethics, regulatory, QMS or evidence requirements.

## Publication strategy (D-003)
- Plan multiple papers over time, not one broad paper claiming every planned domain.
- First candidate: platform/software-methods paper after R1–R3 evidence is complete enough to support reproducible methods, validation and benchmark claims.
- Later domain papers require domain-specific independent validation and reference comparisons.
- Venue fit/requirements, authorship, affiliations, funding, competing interests and all claims require owner review at the relevant milestone. No publication or acceptance is implied.

## Mandatory gates
Direction baseline; R0 exit (accepted 2026-11-07); R1 go/no-go; P0; GPL/AGPL bundling; new language; engine-tier change; restrictive license; jurisdiction-specific legal/regulatory/ethics review; real patient data/human participants; paper venue/authorship and evidence-backed claims; NORTH_STAR change; Clinical Mode. Stop at each gate.

## Session protocol
At start read NORTH_STAR, ROADMAP, DECISIONS and latest SESSION_LOG; state phase/objective in two lines. Map every task to roadmap; drift-check before tasks/commits. At end update statuses, record decisions, append session log and report evidence/gaps/risks. Never claim unverified work.


## Owner authorization D-008 — R1 through R3
- On 2026-11-07, the owner explicitly approved proceeding with R1, R2 and R3.
- Execute them in sequence. This authorization does not mark any phase complete and does not waive technical, scientific, licensing, device, security, privacy, clinical or owner exit gates.
- R1 is still in progress. R2 starts after R1 evidence is complete and its go/no-go is documented; R3 starts after R2's exit evidence and approval.


## Owner authorization — integrated R1–R10 implementation (2026-11-08)
- The owner explicitly directed Engineering to implement Research Platform R1 through R10 as one integrated delivery, rather than stopping after R1 to request permission to begin R2/R3.
- D-016 integrated cycle: implement a substantial vertical slice, build the exact revision, run relevant automated and scientific-reference tests, inspect the artifact, exercise the app on available emulator/device targets, fix defects, and record what was and was not verified. Do not defer all testing to a later campaign.
- This changes implementation sequencing only. It does not authorize false validation claims, bypass third-party license review, enable clinical/patient workflows, or waive scientific/device/security/release exit criteria.
- See docs/research-platform-implementation.md for the current implementation inventory and unfinished scope.

## Track U — User interface (owner specification 2026-11-08)

**Current sequencing (D-023):** U is the sixth and final track, after G. Track G's bounded G0–G7 engineering foundation was assessed CLOSED on exact main commit 31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1 (workflow 44108451571, 9/9 jobs); overall G acceptance remains OPEN for independent/operational obligations. This assessment satisfies the sequencing prerequisite to begin U engineering; it does not waive G carry-forward items. Track U STARTED 2026-11-17 under D-024 and follows the same two-step gate: documented base implementation, then integration audit/tests/fixes. Pre-existing U0–U3 work remains partial baseline, not accepted completion. U4–U6 remain subject to dependencies and evidence.

| ID | Scope | Dependency | Exit gate | Status |
|---|---|---|---|---|
| U0 | D-024 monochrome V1 semantic tokens, owner-brand asset contract, generator, Compose primitives/gallery and screenshot harness | R0 | Tokens compile deterministically; owner assets preserved; screenshot, contrast and accessibility evidence reviewed | in-progress — owner V1 monochrome specification adopted by D-024; existing Light/Dark/System and local-lock source is retained for audit; exact V1 token migration, asset audit/integration, complete component system, screenshot, contrast and accessibility evidence remain open |
| U1 | Adaptive shell, search, Research Mode/status/tier chips, onboarding, schema settings | R2 | Full device/window matrix passed | in-progress — four-destination shell and responsive navigation source exist; D-015 local lock screen is compiled in CI #2039; search, onboarding, full destination map and device/window matrix remain open |
| U2 | App/vault lock, FLAG_SECURE, Recents, encrypted settings, consent, inventory, threat model | R2 | Security tests pass; threat model owner-reviewed | in-progress — opt-in AndroidX biometric/device-credential local app-lock source is present and CI #2039 passed; FLAG_SECURE, key lifecycle/recovery review, encrypted settings, consent/inventory and owner-reviewed threat model remain open |
| U3 | Tool runner, sequence viewer, enzyme-kinetics lab, results/provenance and branded export | R3 | TalkBack and 200% font-scale pass | in-progress — bounded FASTA/FASTQ QC cards launch from Explore; durable job/provenance/result/export integration and remaining viewers are open |
| U4 | Mol*/3Dmol.js bridge, alignment/tree/chart/chemistry viewers | S1–S3 | Low-end-device performance budgets met | not-started |
| U5 | Genomics, PGx Research Mode and in-silico screens | P1–P3, I2–I4 | Clinical wording adviser-reviewed before release | not-started |
| U6 | Settings, themes, localisation/RTL, motion/haptics, usability and quality report | U1–U5 | All quality bars measured and recorded | not-started |

U0 visual direction: owner-supplied Premium Minimal Monochrome V1 is the active authority under D-024. Exact light/dark values and measurements are in docs/ui/ui-spec.md. Existing owner assets and dashboard/login references remain preserved byte-for-byte; use only after auditing their actual paths and intended roles. Existing carousel/theme work is partial and must be reconciled with V1 rather than assumed complete. Token migration, asset integration, font/icon licence and glyph review, reference comparison, screenshots, contrast, accessibility and device matrix remain open.


### U1 responsive shell progress (2026-11-08)
- Implemented live Compose window-based bottom navigation, rail and permanent drawer, including compact-height landscape rail and 840dp content width cap.
- Added pure JVM boundary tests for navigation classification. Check CI against latest main SHA.
- U1 remains open: NavigationSuiteScaffold/WindowManager posture support, universal search, Research Mode/connectivity chips, onboarding, full screen map and device matrix are not complete.


### Historical owner authorization D-009 — begin Track S in parallel (2026-11-08; SUPERSEDED BY D-019)
- The owner explicitly instructed Engineering to complete R1–R10 and start Track S without waiting for another per-track approval.
- This supersedes the previous sequencing prohibition only for independently implementable Track S preparation and implementation. S1 preparation has started; full rendering remains gated on R1 WebView/runtime evidence and exact third-party license approval.
- S2–S5 remain dependent on their scientific reference sets, model/license decisions, node security and benchmark evidence. No scientific, device, production, clinical or release gate is waived.

## Integrated implementation and verification cycle — owner direction (2026-11-08)

The owner required substantial implementation and verification as one continuous cycle. Its parallel-track sequencing clause was superseded by D-019 on 2026-11-09. The build/test/fix/evidence cycle remains active, but tracks must now be executed strictly in sequence.

### Mandatory cycle
1. Plan and inspect: read NORTH_STAR, ROADMAP, DECISIONS and the latest SESSION_LOG; inspect source, assets, registry, dependencies and tests. Map changes to roadmap items.
2. Implement a substantial vertical slice: include UI, domain/orchestration, persistence/security, capability registry and real user actions as applicable. No dead buttons, fake results, placeholder success or controls that merely change appearance without applying state.
3. Build: run reproducible arm64 debug APK/AAB pipeline. Preserve exact source commit, toolchain, artifact hashes and logs. Compilation is only a build result.
4. Test the affected system: Python/Rust/C++/Kotlin tests; Android JVM and instrumentation/UI tests; registry/schema/licence/security checks; migration/recovery/import/export; navigation/action coverage; accessibility/contrast/responsive screenshot checks; runtime probes and resource checks. Emulator and physical-device tests are separate. Unavailable tests are BLOCKED or NOT RUN, never PASS.
5. Inspect the exact artifact: install and exercise the APK from that cycle; verify authentication/biometric flows, visible controls, navigation, persistence, offline behavior and crash-free paths. Record device/API/ABI, steps, expected/actual results, screenshots/logs and APK SHA-256. CI compilation is not an installed-app test.
6. Fix and repeat: any failure returns to implementation; rerun affected tests and required regression suite. Do not accept a failing baseline.
7. Record honestly: update roadmap, registry, validation manifests, UI quality report and session log. Distinguish implemented, automated-test-passed, reference-validated, emulator-verified and physical-device-verified.

### Required UI and authentication scope
- D-015 Light Classic is the sole active visual authority, with Dark Classic and System. Previous neon/Obsidian Cyan and earlier palettes are discontinued for active UI work and retained only as historical records.
- Implement actual splash/onboarding, authentication, dashboard, navigation, profile/security and appearance flows in native Compose, using original owner-provided brand assets without destructive alteration.
- No fictitious remote account service. Clearly distinguish local app-lock from account authentication.
- Biometric unlock must use AndroidX BiometricPrompt, runtime capability/enrollment checks, explicit opt-in, secure credential fallback, lockout/error handling and Keystore-backed cryptographic protection where appropriate. Never store biometric templates or passwords.
- Every visible option must perform a real action, open a real screen, or be explicitly disabled with a reason.
- Research tools are runnable only with a real registry entry, input contract, dispatcher, result model/viewer and tests. Research Mode and non-clinical restrictions remain mandatory.

### Tested-build acceptance
A build may be called tested only when its exact artifact has a recorded successful build, applicable automated regression results and required install/runtime UI evidence. Device checks that cannot be performed remain explicit blockers. A debug APK is not a production release.


## Engineering integration standard — owner direction (2026-11-09)
- Adopted `docs/ENGINEERING_INTEGRATION_STANDARD.md` and `api/engine-envelope-v1.schema.json` under D-018.
- All future implementation increments must state component ownership, call direction, transport, contract/version, boundary risks and matching caller/callee changes before coding. JSON Schema is the semantic source of truth for cross-component engine envelopes.
- Target ownership is Python (science), C++ (performance core), Rust (security), Kotlin (Android), Swift (iPhone), TypeScript/Three.js (offline 3D), Bash (build/test/deploy).
- This is a target standard, not an implementation claim. Current Kotlin/Python/C++/Rust reality and absent Swift/TypeScript sources are explicitly documented. Team size, iOS minimum version and WebView/device matrix remain TBD.
- Follow the owner's strict R → S → I → P → G → U, two-step-per-track sequence under D-023. No parallel track work until the owner changes that instruction.


### R-track exact-source audit CI update — 2026-11-09
- Commit `2ea102719fc37354f18def85bb329a60a885ee2a`, CI run #2094: all five jobs passed, including ARM64 APK/AAB, JVM tests, scientific reference fixtures, RDKit sanity fixtures and declared-source SPDX inventory.
- The imported FASTA integration slice and its Step 2 code audit now have successful exact-source CI evidence. This is not a declaration that all R1–R10 exit criteria are met. Device/runtime, migration/recovery, broader workflow coverage, independent scientific validation and full licence/security gates remain.


### Track execution order — D-019 (2026-11-09)
At the time of D-019 (2026-11-09), it superseded D-009's parallel-track sequencing and set the then-current order to R → S → I → P → G, with a two-step base-build and audit gate for each track. D-023 (2026-11-12) later superseded that five-track order and now controls the current R → S → I → P → G → U sequence. This paragraph records D-019's historical effect; it is not the current sequencing instruction.


## R-track evidence refresh — 2026-11-09 (CI #2101)

The exact-source revision `8c4128d5e448db51f2b48fec6c38ce6022fdb053` passed all five CI jobs. The Python suite collected 233 tests (229 passed, 4 skipped for optional RDKit/pysam dependencies); the separate pinned RDKit sanity job and pinned SciPy/Biopython reference-comparison job passed. Android ARM64 debug APK/AAB packaging, static alignment checks and JVM unit tests passed. See `docs/ci-build-evidence.md` and the R3/R4/R7/R8 phase plans.

This corrects stale records that the R3 bootstrap, R7 phylogenetics and R8 NB2 regression tests had not run: those modules execute in the passing Python suite. It does **not** close R. R1 device/runtime feasibility; R2 database migration, WorkManager and SAF lifecycle instrumentation; R3 independent experimental/reference uncertainty and residual/model-selection validation; R4 device-scale workflows; R5 independent structure concordance/viewer; R6 approved-engine chemistry concordance; R7 published tree concordance; R8 null/power/FDR calibration; R9 authoritative licensed PGx content and clinical gates; and R10 security, accessibility, transitive licensing, signed release and device benchmarks remain open. At the time of this 2026-11-09 evidence note, D-019's strict R → S → I → P → G order applied; S had not started at that historical checkpoint.


### S implementation step 1 — started 2026-11-09
- R implementation/host-audit step was closed on exact-source CI #2126 and recorded in D-020; S is now the next sequential engineering track.
- Initial S6 increment hardens local FASTA reference-pack resource limits: all byte/manifest/record/residue limits must be positive integers (booleans and floats are rejected). Exact bytes remain hash-verified before parsing and after ingestion.
- S1 renderer/bridge remains blocked on R1 WebView/device feasibility and exact viewer/transitive-license review. Existing S6–S9 code remains bounded research foundations, not validated biological inference.


### Owner decision D-021 — Track S external gates (2026-11-10)
The owner approved deferring independent biological validation, licensed reference/model acquisition and secure inference infrastructure, and physical-device verification as explicit carry-forward obligations. Unvalidated capabilities remain disabled. This does not close missing software: S4 prediction-engine integration, S6 homology/profile-HMM, S7 full prokaryotic/eukaryotic annotation, and S9 family/domain workflows remain open. S10 generation remains disabled. Track I stays blocked until the remaining implementable S software scope is delivered and audited. See `docs/track-s/audit-2026-11-09.md`.


### Owner decision D-022 — full S software implementation authorization (2026-11-10)
The owner authorized full implementation of all remaining S-track software and its integration/audit, including S4, S6, S7 and S9. Continue repository code, tests, documentation and capability integration without repeated permission requests. D-021's explicit external validation, licensed data/model and physical-device deferrals remain in force; no evidence may be fabricated and unvalidated capabilities remain disabled. Track I remains blocked pending S exit audit.


**Track S exit decision (2026-11-11): SOFTWARE SCOPE CLOSED.** Exact-head GitHub Actions run [42954316831](https://github.com/AssayFlux/Molecularis/actions/runs/42954316831) passed on `77ddd0f934eb8712818af1cdf8c297140d35289b`: all workflow jobs succeeded, including the 440-pass Python suite (4 optional-dependency skips), strict lint/type/registry/catalogue/reference/SPDX checks, arm64 debug APK/AAB build, Android JVM tests, package alignment and artifact/hash verification. S1–S9 software foundations and S10's deliberately non-generative boundary are integrated; S3/S8 are included in exact-head verification. This closes the implementable software scope only. D-021 carry-forward obligations are not passed or waived: independent scientific/experimental validation, licensed reference/model resources, secure inference infrastructure, full chemical semantics, and physical-device usability/performance/accessibility checks. S10 generative design remains disabled. Track I is now the next engineering track; this does not authorize clinical/patient workflows or production release.


## Track P — exact-head software audit update (2026-11-11)

- Corrected Track P test-lint defects and verified exact main commit aee8f1e3a73dfa5136ca2472877bd541727453db with workflow [#43002587271](https://github.com/AssayFlux/Molecularis/actions/runs/43002587271): all 9/9 jobs passed.
- Python: 522 passed, 9 skipped (optional RDKit/pysam dependencies absent in the Python foundation job); Ruff and strict mypy passed.
- Android arm64 debug APK: 70,389,802 bytes; SHA-256 `4cd8ce2e1f5e6874e39d589e853fdb801c9322c56461a19703653d031f5f9fb5`. AAB: 40,260,451 bytes; SHA-256 `90ce8bbfac2e6a17faf385bcffcee1ddcc179bde1ecc625ef93a5b25ff66bdc1`. 16 KB package-alignment checks and JVM unit tests passed; no emulator or physical-device runtime was performed.
- Host-side pinned scientific-reference comparisons, OpenMM CPU replica smoke, Vina engine smoke, RDKit descriptor/ADMET utility smoke, source SPDX inventory and private Node worker security tests passed. These are engineering smoke/reference checks, not independent biological or clinical validation.
- Track P research-only software foundation (P1/P2 synthetic contracts and P3/P4/P6 schemas; P5/P7 preparation) has exact-head CI evidence. This is not a P0 gate passage or a claim that P0–P7 operational/external requirements are complete.
- P0 remains NOT APPROVED. P1 independent authoritative reference concordance, exact-source terms review, fuzz/resource audit and device workflow validation remain. P2–P7 still require their respective independent reviewers, licensed sources, operational processes, ethics/regulatory determinations and acceptance evidence. Patient/clinical functions remain disabled.


## Track G — governance, assurance and publication readiness

G0–G7 bounded research-only engineering foundations are now implemented: governance/evidence mapping, security requirements and test matrix, supply-chain evidence capture, quality/traceability controls, source-level privacy/data-flow inventory, conservative scientific capability claims, publication integrity protocol and operational procedures. The baseline exact-head workflow #44098272029 passed 9/9 jobs; subsequent checker/test and dependency-evidence increments are undergoing final exact-head CI on the current main revision. **Overall Track G acceptance remains OPEN**: owner policy acceptance, specialist role appointments, complete SBOM and license clearance, independent security/privacy/scientific/legal reviews, merged-manifest/device verification, and operational tabletop/access/recovery exercises are not recorded. Track U remains next after G's two-step engineering gate is assessed and reported. P0 remains BLOCKED / NOT APPROVED; Track G cannot authorize patient data, human-subject work, Clinical Mode or regulated deployment.


## Track P — bounded software closure evidence (2026-11-17)

The current main head before this documentation update was `7967ccb0288ea1d5b82af18f8ab8d886d18d4733`. Exact-head workflow [#44078534173](https://github.com/AssayFlux/Molecularis/actions/runs/44078534173) completed successfully with 9/9 jobs. The Python foundation job collected 543 tests: 534 passed and 9 skipped because optional RDKit/pysam dependencies were unavailable in that job; Ruff and strict mypy passed. Android arm64 APK/AAB build, package alignment and JVM tests passed. Host numerical/reference smoke checks, SPDX inventory and private Node worker security tests also passed.

This evidence closes the bounded P1–P7 software foundation only. It does not demonstrate PGx biological concordance, source licensing, independent review, ethics approval, privacy/legal/regulatory compliance, operational curator activity, device runtime acceptance or clinical validity. P0 remains BLOCKED / NOT APPROVED. Patient-data, human-subject, individual interpretation, clinical recommendation and Clinical Mode pathways remain disabled.


### Track U sequencing start — 2026-11-17
- G0–G7 engineering foundation was assessed CLOSED on exact main commit 31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1; workflow 44108451571 passed 9/9 jobs. Overall G acceptance remains OPEN for independent and operational obligations.
- Started U Step 1 on branch track-u-step1-base. Added docs/track-u/implementation-plan.md and recorded D-024 for the owner's 20-section monochrome V1 prompt.
- The V1 prompt supersedes D-015 only for conflicting visual direction; research scope, asset preservation, real workflows, security/privacy and architecture constraints remain.
- U0–U3 are partial pre-existing source. U4–U6 are not started. No U completion percentage is reported before both steps are assessed.


## 2026-11-18 — Public scientific data integration
- Added direct Android retrieval source adapters for NCBI Gene/Nucleotide/Protein, UniProtKB and RCSB PDB entry IDs.
- Added encrypted local public-record payload cache and Home retrieval UI.
- Connected retrieved FASTA to the existing on-device QC adapter and RCSB mmCIF to the existing structure parser/viewer.
- Remaining: saved-record reopen/reanalyse, NCBI Gene cross-links, RCSB search, ENA/Ensembl/PubChem, provider retry/cancellation, source terms/licence metadata, exact-head build and device acceptance.
- This is a source-level integration milestone, not a release-ready or scientifically validated claim.

