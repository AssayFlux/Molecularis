# Service and Platform Status Register

Last verified: 2026-11-21  
Current implementation commits: K pending CI; G [bfb3bf8ba807e9f971a38663734d7fb455f7654b](https://github.com/AssayFlux/Molecularis/commit/bfb3bf8ba807e9f971a38663734d7fb455f7654b); H [6e03dcbc7820f26bbda7b666fb005f898f5df487](https://github.com/AssayFlux/Molecularis/commit/6e03dcbc7820f26bbda7b666fb005f898f5df487); I [4992f5ad8c9cac783a977ce0ba409d8b0bf7c5b7](https://github.com/AssayFlux/Molecularis/commit/4992f5ad8c9cac783a977ce0ba409d8b0bf7c5b7); J [67a4d577fd8239f3465ef7eb8ae56d0ab6c193e9](https://github.com/AssayFlux/Molecularis/commit/67a4d577fd8239f3465ef7eb8ae56d0ab6c193e9).

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
| Native C++ / Rust interoperability | Not implemented | Language-neutral schemas exist; bindings and conformance tests remain required |
| Recovery certification | Partial | Atomic blob publication and integrity audit; crash-boundary fault injection and backup/restore remain open |
| Execution isolation | Partial | In-process trusted handlers; no OS-level sandbox or preemptive CPU/memory/GPU isolation |
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
| K | Phylogeny | Existing Newick parser/serializer, patristic distances, JC69, NJ, UPGMA and seeded site-bootstrap algorithms retained and integrated | Python v1 canonical aligned-nucleotide artifact service | MSDE artifact lifecycle and five capabilities | PHY-001–PHY-007 executable | Engineering implementation complete; CI verification pending; scientific review deferred |
| L | Pharmacogenomics | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| M | Cohorts | Scaffold | Not started | Not started | Not operational | Planned |
| N | Workflows | Existing workflow code; audit pending | Not started | Not started | Not operational | Planned |

## Verification evidence

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

**Active phase:** Service K — Phylogeny Python v1 implementation authored; CI verification pending. University scientific review, independent reference comparisons and formal freeze deferred until A–N engineering completion per owner direction. The platform is not yet a distributed, multi-language, OS-isolated production runtime.

**Next:** proceed to L — Pharmacogenomics after K CI verification. K supports canonical alignments, JC69 distances, neighbor joining, UPGMA and seeded site-bootstrap. university scientific review and formal freeze remain deferred until A–N engineering completion. University-level scientific review, cross-reference testing and formal contract freezes will be conducted after the full A–N engineering build, as directed by the owner. Platform-wide recovery, backup/restore, service discovery, language conformance and isolation gates remain open.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.
