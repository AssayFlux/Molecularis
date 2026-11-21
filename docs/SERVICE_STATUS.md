# Service and Platform Status Register

Last verified: 2026-11-21  
Current implementation commits: L [3e758f6a90e8be8adc3b02098958db3dad11ed98](https://github.com/AssayFlux/Molecularis/commit/3e758f6a90e8be8adc3b02098958db3dad11ed98); K [cb9479a1e86f9b3130a45cca208ee33e9b9ae1bc](https://github.com/AssayFlux/Molecularis/commit/cb9479a1e86f9b3130a45cca208ee33e9b9ae1bc); G [bfb3bf8ba807e9f971a38663734d7fb455f7654b](https://github.com/AssayFlux/Molecularis/commit/bfb3bf8ba807e9f971a38663734d7fb455f7654b); H [6e03dcbc7820f26bbda7b666fb005f898f5df487](https://github.com/AssayFlux/Molecularis/commit/6e03dcbc7820f26bbda7b666fb005f898f5df487); I [4992f5ad8c9cac783a977ce0ba409d8b0bf7c5b7](https://github.com/AssayFlux/Molecularis/commit/4992f5ad8c9cac783a977ce0ba409d8b0bf7c5b7); J [67a4d577fd8239f3465ef7eb8ae56d0ab6c193e9](https://github.com/AssayFlux/Molecularis/commit/67a4d577fd8239f3465ef7eb8ae56d0ab6c193e9).

A scaffold or specification does not imply implementation or scientific validation.

## Platform

| Area | Status | Evidence / next gate |
|---|---|---|
| Governance | Established | North Star, A–N roadmap, future architecture, master plan and rules |
| Local Core reference runtime | Implemented v0.2 slice | Lifecycle facade, capability manifest loader, typed contracts and Rulebook executor |
| Artifact store | Implemented local baseline | SHA-256 blobs, SQLite WAL catalog, parent lineage, atomic publication, bounded streaming and integrity audit |
| Metadata indexes | Implemented | SQLite exact/range B-tree indexes; native sorted-segment engine is not implemented |
| Query execution | Implemented bounded snapshot pagination | Snapshot-bound offsets, deterministic ordering, result/candidate limits and explicit completeness |
| Rulebook evidence | Improved baseline | Success/failure records; input artifact lineage is attached to operation outputs |
| JSON contracts | Validated baseline | Repository-wide JSON Schema validation passed in run #135 |
| Scientific optional CI | Green baseline | Run #135: chemistry, sequence and genomics optional profiles passed |
| Language strategy | Python-first | Existing Python implementation is the supported reference; no speculative language ports are required |
| Recovery certification | Partial | P0 adds verified local catalog/object backup and restore plus expanded integrity/lineage audit; crash-boundary fault injection, encryption/signing and restore drills remain open |
| Execution isolation | Partial | P0 rejects missing artifact references, verifies artifact content and binds Agentics execution to planned input identities; handlers remain trusted in-process Python with no OS sandbox or preemptive CPU/memory/GPU isolation |
| Distributed services | Not implemented | No distributed storage, replication or cross-process service-discovery protocol |
| Scientific validation | Incomplete | Domain-specific independent reference and reproducibility evidence required |

## A–N service sequence

| Step | Service | Existing code | Engine | Runtime | Rulebook | State |
|---|---|---|---|---|---|---|
| A | Molecular | Native v1 graph model, strict serialization, graph summaries and MSDE integration | Implemented v1 | Python reference runtime and artifact-store capability | Ten executable structural rules; independent scientific approval pending | Implementation complete; scientific acceptance pending |
| B | Sequence | Existing parser, alignment, reference, GFF3, ORF and translation modules consolidated; new typed artifact service | Python v1 implementation | MSDE artifact lifecycle and five Rulebook capabilities | SEQ-001–SEQ-005 executable; review pending | Engineering implementation complete; scientific acceptance pending |
| C | Structure | PDB/mmCIF, geometry, RMSD, contacts, SASA, interactions and related adapters retained | Python v1 canonical service | MSDE artifact lifecycle and six capabilities | STR-001–STR-007 executable; university review deferred | Engineering implementation complete; review deferred until A–N build |
| D | Chemistry | Native explicit-graph v1; MSDE artifacts and optional RDKit retained | Implemented | Five capabilities | CHM-001–CHM-006 executable | Engineering complete; university review deferred |
| E | Protein | Existing descriptors, ESM local inference, HMMER evidence, motif scan and design brief retained | Native sequence/artifact v1 | MSDE artifacts and four capabilities; ESM/HMMER remain optional local workflows | PRO-001–PRO-006 executable | Engineering complete; CI run #44889593877 green; scientific review deferred |
| F | Genomics | Existing SAM/VCF, BAM/CRAM, assembly QC, GFF3, ORF, reference normalization and optional HTSlib/tool adapters retained; canonical genome artifact added | Python v1 | MSDE artifacts and five capabilities | GEN-001–GEN-007 executable | Engineering implementation complete; university review deferred |
| G | DNA/RNA | Canonical DNA/RNA artifacts, transcription, reverse transcription, explicit translation, oligo screening and Nussinov RNA fold; existing sequence/genetic-code primitives reused | Python v1 native operations | MSDE artifact lifecycle and eight capabilities | DRNA-001–DRNA-007 executable | Engineering implementation complete; CI run #44892707015 green; university review deferred |
| H | Simulation | Canonical NVT/NPT protocol artifacts, energy-series analysis, hash-pinned GROMACS TPR runner integration and existing OpenMM CPU replica runner | Python v1 | MSDE lifecycle and three capabilities; OpenMM direct trusted-object API | SIM-001–SIM-007 executable | Engineering complete; CI run #44893264385 green; scientific review deferred |
| I | Kinetics | Existing Michaelis–Menten, inhibition, fitting, bootstrap and PK/PD primitives retained; canonical reaction-network artifacts and mass-action RK4 added | Python v1 | MSDE artifact lifecycle and four capabilities | KIN-001–KIN-006 executable | Engineering complete; CI run #44894304968 green (core 702 passed/12 skipped; Chemistry 710/4; Genomics 703/11; Sequence 705/9); university review deferred |
| J | Omics | Existing CPM/CLR, Welch/NB2 differential expression, diversity, growth and correlation primitives retained; canonical matrix artifact and MSDE service added | Python v1 | MSDE artifact lifecycle and seven capabilities | OMI-001–OMI-009 executable | Engineering implementation authored; CI verification pending; university review deferred |
| K | Phylogeny | Existing Newick parser/serializer, patristic distances, JC69, NJ, UPGMA and seeded site-bootstrap algorithms retained and integrated | Python v1 canonical aligned-nucleotide artifact service | MSDE artifact lifecycle and five capabilities | PHY-001–PHY-007 executable | Engineering complete; CI run #44896994652 green; scientific review deferred |
| L | Pharmacogenomics | Existing reference-checked normalization, star-allele JSON definitions and PharmVar TSV parser retained and integrated | Python v1 canonical sample/definition artifacts and deterministic phased star-allele matching | MSDE artifact lifecycle, two capabilities and bounded definition-pack ingestion | PGX-001–PGX-007 operational | Engineering complete; CI run #44898692562 green; scientific/clinical review deferred |
| M | Cohorts | Canonical synthetic non-patient cohorts, longitudinal visits, aggregate summaries, stratification and pseudonymous overlap | Python v1 MSDE artifact lifecycle and four capabilities | COH-001–COH-008 operational | Engineering complete; CI run #44899270453 green; scientific/privacy review deferred |
| N | Workflows | Native cross-service DAG orchestration; FASTA/FASTQ QC and Galaxy adapter retained | Canonical WorkflowDocument, MSDE artifact lifecycle and Core RulebookExecutor integration | WF-001–WF-009 operational; two registered capabilities | Engineering complete; CI run #44900460557 green; scientific review deferred |

## Verification evidence

- [Run #44900460557](https://github.com/AssayFlux/Molecularis/actions/runs/44900460557), commit `220dd2a`: Workflows N verified; core 746 passed/12 skipped; optional Chemistry 754/4, Genomics 747/11, Sequence 749/9 (4 existing warnings). Registry, 64 JSON Schemas, Ruff E9/F, compilation, Workflows DAG benchmark smoke and all test profiles passed.


- [Run #44899270453](https://github.com/AssayFlux/Molecularis/actions/runs/44899270453), commit `70031be`: Cohorts M verified; core 737 passed/12 skipped; optional Chemistry 745/4, Sequence 740/9 (4 existing warnings), Genomics 738/11. Registry, 61 JSON Schemas, Ruff E9/F, compilation, Cohorts aggregate benchmark smoke and all test profiles passed.


- [Run #207](https://github.com/AssayFlux/Molecularis/actions/runs/44898692562), commit `3e758f6`: Pharmacogenomics L verified; core 728 passed/12 skipped; optional Genomics 729/11, Chemistry 736/4, Sequence 731/9 (4 existing warnings). Registry, 58 JSON Schemas, Ruff E9/F, compilation, Pharmacogenomics matching benchmark smoke and all test profiles passed.

- [Run #201](https://github.com/AssayFlux/Molecularis/actions/runs/44896994652), commit `cb9479a`: Phylogeny K verified; core 721 passed/12 skipped; optional Sequence 724/9 (4 existing warnings), Genomics 722/11, Chemistry 729/4. Registry, 55 JSON Schemas, Ruff E9/F, compilation, Phylogeny benchmark smoke and all profiles passed.

- [Run #197](https://github.com/AssayFlux/Molecularis/actions/runs/44895300775), commit `71f7355`: Omics J verified; core 711 passed/12 skipped; optional Genomics 712/11, Sequence 714/9 (4 existing warnings), Chemistry 719/4. Registry, 53 JSON Schemas, Ruff E9/F, compilation, Omics matrix benchmark smoke and all test profiles passed.

- [Run #191](https://github.com/AssayFlux/Molecularis/actions/runs/44894304968), commit `4992f5a`: Kinetics I verified; core 702 passed/12 skipped; optional Chemistry 710/4, Genomics 703/11, Sequence 705/9 (4 existing sequence warnings). Registry valid, 51 JSON Schemas, Ruff E9/F, compilation, all benchmark smoke steps including 10,000 RK4 steps, and all test profiles passed.

- Previous baseline [run #132](https://github.com/AssayFlux/Molecularis/actions/runs/44880497095): 568 passed, 12 skipped.
- [Run #133](https://github.com/AssayFlux/Molecularis/actions/runs/44880802259): optional dependency profiles passed; the core job exposed a malformed legacy JSON schema that was subsequently repaired.
- [Run #150](https://github.com/AssayFlux/Molecularis/actions/runs/44883890013), commit `7e0785a`: 608 passed, 12 skipped; core, capability registry, 28 JSON Schemas, Ruff E9/F, compilation, 1k/10k graph benchmark smoke and all sequence/genomics/chemistry optional profiles passed.
- [Run #153](https://github.com/AssayFlux/Molecularis/actions/runs/44884757468), commit `f940fe4`: core 624 passed/12 skipped; optional sequence 627 passed/9 skipped, genomics 625 passed/11 skipped, chemistry 632 passed/4 skipped. Registry, 31 JSON Schemas, Ruff E9/F, compilation, molecular benchmark smoke and 1,000-record/1,000,000-base sequence streaming benchmark all passed.
- Ruff remains limited to E9/F; this is not full style conformance.

- [Run #158](https://github.com/AssayFlux/Molecularis/actions/runs/44886827271), commit `221f444`: core 636 passed/12 skipped; optional sequence 639 passed/9 skipped, genomics 637 passed/11 skipped, chemistry 644 passed/4 skipped. Capability registry, 34 JSON Schemas, Ruff E9/F, compilation and Molecular/Molecularis Sequence/Structure benchmark smoke passed.
- [Run #159](https://github.com/AssayFlux/Molecularis/actions/runs/44886943910), commit `47e4a62`: cumulative Structure baseline, all four jobs green.
- [Run #162](https://github.com/AssayFlux/Molecularis/actions/runs/44888785327), commit `93a7b10`: Chemistry D verified; core 644 passed/12 skipped; optional Chemistry 652 passed/4 skipped, Sequence 647 passed/9 skipped, Genomics 645 passed/11 skipped. Registry valid, 37 JSON Schemas, Ruff E9/F, compile and all benchmark smoke steps passed.
- [Run #E](https://github.com/AssayFlux/Molecularis/actions/runs/44889593877), commit `d1b75c9`: Protein E verified; core 651 passed/12 skipped; optional Sequence 654 passed/9 skipped, Genomics 652 passed/11 skipped, Chemistry 659 passed/4 skipped. Registry valid, 40 JSON Schemas, Ruff E9/F, compile and Protein 10k-residue benchmark smoke passed.

## Active phase and next exact work

**Active phase:** Agentics P0 — repository truth, platform safety and reliability. Service N engineering and CI verification are complete in run #44900460557 (core 746 passed/12 skipped; optional Chemistry 754/4, Genomics 747/11, Sequence 749/9 with 4 existing warnings). Native workflow DAGs validate registered capabilities and execute through MSDE RulebookExecutor with artifact lineage. Galaxy REST and FASTA/FASTQ helpers remain optional integrations. The platform remains a local Python reference runtime; distributed execution and OS-level isolation are not accepted.

**Next:** A–N service engineering is complete. Proceed through Agentics P0: repository/dependency audit, representative cross-service typed artifact handoff, provenance continuity, failure/recovery evidence, threat model, data-egress controls and OS-level isolation. Service CI does not certify scientific correctness. University-level scientific and privacy review, independent reference comparisons and formal contract freezes will be conducted after the full A–N engineering build, as directed by the owner. Platform-wide recovery, backup/restore, cross-service artifact/provenance continuity and isolation gates remain open.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.


## Agentics Molecularis (intelligence layer)

**Official name:** Agentics Molecularis, the goal-directed agent and orchestration system of the Molecularis scientific platform. Governing plan: [AGENTICS_MOLECULARIS_MASTER_PLAN.md](AGENTICS_MOLECULARIS_MASTER_PLAN.md).

**Implemented engineering foundation:** model-agnostic planner callable contract, active A–N capability catalog, strict Workflow v1 parsing/validation, persisted plan artifact with input lineage, explicit approval gate, Core Rulebook execution path and fresh-runtime A–N bootstrap. CI evidence: [run #44901363429](https://github.com/AssayFlux/Molecularis/actions/runs/44901363429), commit `2b6eced852fb049a81f6b087bb94e5e946047750`.

**Not yet accepted:** configured production LLM provider, Sources service, real cross-service scientific artifact handoff, artifact-grounded answer composer, 50+ adversarial evaluation suite, Predictor service, model benchmark, OS-level sandbox/recovery certification, training pipeline, design safety gate and service-wide Proposer → Verifier acceptance. The governing phase sequence is P0–P7 in the v2.1 Agentics Master Plan; each phase remains unimplemented until its own code, tests and acceptance evidence are recorded.

This is an initial agent foundation, not a finished autonomous research scientist. It is not scientifically validated; university review remains separate.


## Agentics Molecularis — architecture direction update

Governing plan restored and aligned as v2.1 on 2026-11-21. The current repository evidence above remains the status baseline; this documentation update does not implement the Scientific Knowledge Engine or construction system.

**Permanent target across A–N:** Understand → Represent → Reason → Construct → Evaluate → Verify → Learn. Agentics is the orchestrator; the shared Scientific Knowledge Engine provides typed, versioned knowledge/equation/evidence contracts; each service retains domain-owned scientific engines, constraints, construction methods and verification Rulebooks.

The system is not restricted to PDB, X-ray structures, existing reference examples or pretrained predictors. These are optional evidence or candidate-generation methods. Novel candidates must be labelled constructed/hypothesized until appropriate independent evidence supports stronger claims.

**Current status:** initial AI planner/approval-gated Workflow v1 foundation remains implemented as previously recorded. The universal knowledge substrate, shared construction/evaluation primitives, full cross-service proposer/verifier integration and related scientific acceptance are roadmap work, not current completed capabilities.


## Scientific foundation documentation status (2026-11-21)

**Documentation:** The shared Agentics scientific foundation has been specified and linked across the project documentation. The current documents define the discipline map, candidate scientific tool ecosystem, Constitution, adapter requirements and staged implementation sequence.

**Implementation:** Documentation alignment is not implementation. No claim is made here that the Scientific Knowledge Engine, unit/type system, mathematics/statistics adapters, simulation adapters, full pre-generation auditor, independent verifier or training pipeline has been completed. Candidate tools remain unverified until the repository/dependency audit establishes exact installed versions, licenses and actual adapter status.

**Next engineering gate:** Agentics P0 is the active gate. SF0 repository/dependency and A–N capability audit is its first task. Record actual implementations, gaps, versions, licenses and tests; then close platform safety, integration and recovery blockers before entering P1/SF1. The SF1+ work in services/ai/IMPLEMENTATION_ROADMAP.md is subordinate to the v2.1 Master Plan. Keep this work aligned with the single Agentics Master Plan and approved A–N service order. University scientific review remains separate.
