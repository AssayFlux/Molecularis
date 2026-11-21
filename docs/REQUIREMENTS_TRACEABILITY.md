# Molecularis — Legacy Requirements and Repository Traceability

**Audit baseline:** CORE after PR #9 merge, 2026-11-21. **Purpose:** trace original owner requirements and R/S/I/P/G/U implementation records into the new desktop-first plan. This is a requirements map, not an implementation or validation claim.

## 1. Source hierarchy

1. Current explicit owner direction: installed desktop first (Linux, Windows, macOS), then Android and iOS/iPadOS; no website-first delivery.
2. `NORTH_STAR.md` and accepted `DECISIONS.md`: current intent and constraints.
3. Current source, schemas, tests, CI and dated evidence: truth about implementation.
4. `docs/origin/KINETICS_MASTER.md`: original owner specification; its Android-first deployment assumption is superseded, but its scientific scope and safety requirements remain.
5. R/S/I/P/G/U plans and audits: detailed work packages, implementation history, limitations and outstanding gates. Their old sequence is not automatically retained.
6. Integration matrices: candidates, not commitments or implemented services.

When sources conflict, retain useful requirements, replace only the conflicting deployment/sequence assumption, and document why.

## 2. Original 18-part owner specification

| Original part | New plan treatment | Repository truth / disposition |
|---|---|---|
| P1 direction/session protocol | Governance, decisions, evidence and PR discipline | Root direction, decision and session history retained; Master Plan is single milestone authority |
| P2 offline scientific workbench | Local-first installed product and service catalogue | Android/Python foundations exist; no complete desktop app yet |
| P3 Research/Clinical separation | Research-only boundary | PGx contracts exist; clinical decision support remains disabled and unauthorized |
| P4 language plan | Python scientific layer; Rust/C++ only when justified; platform UI undecided | Python substantive; Kotlin Android client; Rust/C++ production foundations absent |
| P5 layered/local/remote architecture | Shared contracts, local execution, optional secured compute profiles | Android/Python and bounded Vina worker exist; no universal compute manager |
| P6 repository layout | Actual baseline and target architecture | Several directories exist only as placeholders: rust, cpp, engines, datapacks, domains, benchmarks |
| P7 capability registry | Separate implementation/evidence/platform states | 130 registry entries: 68 marked implemented, 62 planned; all 68 currently evidence_level=none |
| P8 broad tool inventory | Long-term scientific portfolio, not first-release promise | Sequence, genomics, structure, chemistry, kinetics, omics, phylogeny, PGx/PKPD source modules exist at mixed maturity |
| P9 PGx pipeline | Staged, gated research pathway | VCF/genotype QC, PharmVar parser and conservative matching foundations; no validated clinical star-allele/diplotype/phenotype/guideline pipeline |
| P10 in-silico lab | Separate chemistry, docking, MD, ADMET, PK/PD workstreams | RDKit adapter, Vina runner, OpenMM prepared-system adapter, ADMET utilities and PK/PD source have explicit limitations |
| P11 structure analysis | Dedicated 3D data/viewer/analysis pathway | PDB/mmCIF subset, geometry, alignment, pockets, quality and viewer assets; no complete Mol* integration or complete prep pipeline claimed |
| P12 governance/privacy/ethics/regulation | Continuous release gates | Governance and evidence records exist; independent legal, ethics, security, privacy, scientific reviews remain open |
| P13 five-track roadmap | Dependency-based desktop-first phases | R/S/I/P/G/U plans mapped below; old sequence is historical |
| P14 research paper | Deferred evidence-led publication work | Paper/readiness materials exist; publication claims wait for independent results and approvals |
| P15 engineering rules | Contracts, tests, CI, compatibility, definition of done | Existing tests/CI/schemas retained; per-capability reconciliation required |
| P16 guardrails | Safety, security, data and licence constraints | Research-only, no false validation, least privilege, preservation and rights review retained |
| P17 working/publishing checklist | PR/release/evidence governance | Release, validation and evidence docs retained as standards |
| P18 first session | Baseline audit gate | This repository-first reset is the new planning baseline |

### Original scientific scope retained

Genomics, transcriptomics, proteomics, structural biology, sequence bioinformatics, phylogenetics/evolution, molecular biology/CRISPR/primers, chemoinformatics, enzyme kinetics, systems biology, multi-omics, microbiology/metagenomics, immunoinformatics, biostatistics, PGx research, in-silico discovery, scientific visualization and infrastructure remain the long-term domain catalogue. They are not all first-release promises.

Enzyme kinetics remains a scientific domain, not obsolete branding. It was the original proposed first validation flagship. Audit its current implementation and independent SciPy comparison before deciding whether it is the first release flagship or whether a simpler sequence/structure vertical slice is a safer cross-platform demonstration.

## 3. Earlier architecture translated, not discarded

| Earlier requirement | New treatment |
|---|---|
| Offline/local-first | Retained: local desktop projects and compute must work offline; public reference retrieval remains explicit and allow-listed |
| Android-native first | Only release order is superseded; Android remains migration reference and compatibility client |
| Tier A/B/C execution | Retained as a resource-placement concept, recalibrated per OS/hardware profile |
| Python scientific orchestration | Retained as current substantive scientific layer |
| Rust parsers/supervision | Candidate role only until crate, contracts, benchmarks and cross-platform builds exist |
| C++ performance kernels | Candidate only after profiling; no substantive C++ engine currently exists |
| Offline WebView viewers | Existing assets retained for evaluation; not a reason to make web the first product |
| SQLite projects/provenance | Android store is migration input; define portable versioned project contract before sharing DB semantics |
| Optional authenticated Remote Node | Retain Vina worker as narrow prototype, not generic compute |
| R reference validation | Keep independent reference tooling outside end-user runtime |

## 4. R track — R0 to R10

- **R0:** repository skeleton, registry, checkers and CI — preserve; audit checker coverage.
- **R1:** Android arm64/Python/Rust/C++ feasibility — CI build probes exist; physical-device/runtime and full engine feasibility were not closed. Add five-platform desktop/mobile framework feasibility.
- **R2:** Compose, SQLite, SAF, encrypted import, WorkManager and provenance — substantial source exists; device, recovery, lifecycle and end-to-end evidence remain.
- **R3:** alpha, sequence/protein and enzyme kinetics — preserve kinetics and reference fixtures; verify API/UI integration and scientific evidence.
- **R4:** sequence/genomics — preserve FASTA/FASTQ, SAM/VCF/GFF3/BAM-related work; complete workflows/reference checks remain.
- **R5:** structure biology — preserve parser/geometry/viewer; full mmCIF, assemblies, quality and viewer gates remain.
- **R6:** chemistry — preserve SDF/graph and optional RDKit; stereochemistry, protonation, tautomer and runtime gates remain.
- **R7:** phylogenetics — preserve Newick, UPGMA/NJ, JC69/bootstrap; independent published-reference and viewer gates remain.
- **R8:** omics — preserve transformations and exploratory NB2; independent calibration, repeated-measures and robust inference remain.
- **R9:** catalogue/PGx — preserve source-pinned PharmVar and conservative matching; no validated clinical interpretation.
- **R10:** security/performance/release — preserve controls; device, full SBOM/licensing, accessibility, independent review and release evidence remain.

## 5. S track — S1 to S10

- **S1** offline structure viewer/session/export: payload and viewer assets exist; full acceptance remains.
- **S2** structure quality/confidence: quality module is partial; method-specific reference validation required.
- **S3** variant/interface/pocket analysis and coordinate mapping: geometry/mapping primitives exist; no biological verdict.
- **S4** prediction confidence/experimental comparison: evidence envelope exists; no bundled/validated predictor.
- **S5** deterministic session export: preserve and verify against portable project format.
- **S6** unknown-sequence triage/local alignment: bounded motif/alignment primitives exist; domain references required.
- **S7** genome annotation/gene discovery: GFF3/ORF/Augustus/Prodigal adapters exist; tools/data/concordance remain gated.
- **S8** translation tables/non-standard genetic codes: versioned code handling exists; curated truth sets required.
- **S9** protein family/domain/structure intelligence: motif/protein/mapping modules exist; curated family/domain sources and validation remain.
- **S10** constrained de novo protein design: future research-only work; model rights, evaluation, uncertainty and biosafety review required.

## 6. I track — engine and data-source decisions

- **AutoDock Vina 1.2.7:** pinned Python adapter and bounded Node worker exist; worker docking disabled by default. Missing ligand/receptor preparation, production deployment/isolation, redocking and decoy-enrichment evidence.
- **OpenMM 8.6.1 CPU:** accepts trusted prepared systems; synthetic harmonic-bond smoke only. Missing force-field/ligand preparation, biomolecular references and production profiles.
- **GROMACS:** alternative only; defer until OpenMM workflow and workload justify second engine.
- **RDKit:** optional host adapter; no all-platform packaging claim.
- **ADMET datasets/models:** candidate only; endpoint, release, rights, leakage, calibration, applicability and external validation required.
- **Biotite, Mol*, MolProbity, ESM, AlphaFold, Open Chemistry, Genome-Wide Workbench, ChemGraph, NUAD, Galaxy, SciREPL:** selective candidates only. Exact component, commit, licence, data/model terms and benchmark required. Do not adopt an entire upstream platform by name alone.

## 7. P track — PGx and precision-medicine research

Preserve P0–P7 contracts, risk records, synthetic/public fixtures and the scope exactly as documented. This plan does not expand the authorized scope.

- **P0:** governance/legal/ethics prerequisites open; competent external determinations required.
- **P1:** synthetic/public references; preserve source release, digest, build and coordinate requirements.
- **P2:** PharmVar parser and conservative complete/phased matching; no comprehensive allele caller.
- **P3:** guideline evidence schema; no executable recommendations or licensed guideline corpus.
- **P4:** human-curation contracts; no operational qualified curation service.
- **P5:** ethics/adviser templates; no ethics approval or participant study.
- **P6:** risk/control contracts; no independent assessment or accepted residual risk.
- **P7:** jurisdiction evidence contracts; no legal opinion or regulatory clearance.

No patient-derived data in GitHub, CI, fixtures, logs or public artifacts. No diagnosis, treatment, dosing or patient-specific interpretation. Clinical Decision Support remains disabled.

## 8. G track — governance and assurance

Retain G0–G7 control/evidence register, data-flow inventory, operational controls, publication integrity, role/review cadence and security verification matrix. Engineering closure is not overall acceptance. Independent security/privacy/legal/scientific/ethics reviews, resolved transitive SBOM/licences, device checks and owner risk acceptance remain distinct gates.

## 9. U track — UI, UX and visualization

Retain owner-supplied Premium Minimal Monochrome Design System V1 and U0–U6 requirements. Adapt for the selected desktop-first framework; do not discard the design contract.

- Home, Work, Settings show real persisted state, never mock account or fabricated job/result counts.
- Import/export, encrypted storage, local biometric lock, job lifecycle, cancellation, resume, recovery and provenance remain critical.
- Service cards distinguish registry presence, runnable engine, platform availability and validation state.
- U3 result presentation, U4 viewers, U5 genomics/PGx research screens and U6 accessibility/localisation/usability remain requirements.
- Desktop adds keyboard, pointer, filesystem, large datasets, assistive tech and window-resizing acceptance; mobile keeps touch/lifecycle/permissions.
- Existing web viewer assets do not authorize web-first product delivery.

## 10. Evidence that must be rechecked

Historical CI links prove only the exact historical SHA and job scope. Re-run exact-head workflows before changing status. Recheck R1 physical-device/native/Python runtime; R2 encryption/recovery/process death/import/export; R3 kinetics reference reproducibility; R4 format/normalization; R5 structure/mmCIF/viewer; R6 RDKit/chemistry; R7 phylogenetic references; R8 statistical calibration; R9 source/licence/abstention; R10 security/accessibility/performance/SBOM; S/I/P/G/U external and domain acceptance.

## 11. Resulting sequencing

The old R → S → I → P → G → U order is a historical track-control sequence, not the desktop-first product release sequence. Use dependency gates: (1) repository/data audit; (2) five-platform feasibility; (3) shared contracts/project/provenance/jobs; (4) installed desktop foundation; (5) one validated scientific vertical slice; (6) expand scientific services and 3D; (7) optional compute profiles; (8) Android compatibility migration and iOS/iPadOS; (9) advanced workflows/institutional operations/publication. Security, licensing, accessibility, validation and governance run continuously across all phases.
