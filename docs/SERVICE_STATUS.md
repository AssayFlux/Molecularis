# Service and Platform Status Register

Last verified: 2026-11-21  
Current implementation commit: [221f44481d4aa1ad59590d5fb7b29f6e9ebe3bfd](https://github.com/AssayFlux/Molecularis/commit/221f44481d4aa1ad59590d5fb7b29f6e9ebe3bfd).

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
| D | Chemistry | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| E | Protein | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| F | Genomics | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| G | DNA/RNA | Scaffold | Not started | Not started | Not operational | Planned |
| H | Simulation | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| I | Kinetics | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| J | Omics | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| K | Phylogeny | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| L | Pharmacogenomics | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
| M | Cohorts | Scaffold | Not started | Not started | Not operational | Planned |
| N | Workflows | Existing workflow code; audit pending | Not started | Not started | Not operational | Planned |

## Verification evidence

- Previous baseline [run #132](https://github.com/AssayFlux/Molecularis/actions/runs/44880497095): 568 passed, 12 skipped.
- [Run #133](https://github.com/AssayFlux/Molecularis/actions/runs/44880802259): optional dependency profiles passed; the core job exposed a malformed legacy JSON schema that was subsequently repaired.
- [Run #150](https://github.com/AssayFlux/Molecularis/actions/runs/44883890013), commit `7e0785a`: 608 passed, 12 skipped; core, capability registry, 28 JSON Schemas, Ruff E9/F, compilation, 1k/10k graph benchmark smoke and all sequence/genomics/chemistry optional profiles passed.
- [Run #153](https://github.com/AssayFlux/Molecularis/actions/runs/44884757468), commit `f940fe4`: core 624 passed/12 skipped; optional sequence 627 passed/9 skipped, genomics 625 passed/11 skipped, chemistry 632 passed/4 skipped. Registry, 31 JSON Schemas, Ruff E9/F, compilation, molecular benchmark smoke and 1,000-record/1,000,000-base sequence streaming benchmark all passed.
- Ruff remains limited to E9/F; this is not full style conformance.

- [Run #158](https://github.com/AssayFlux/Molecularis/actions/runs/44886827271), commit `221f444`: core 636 passed/12 skipped; optional sequence 639 passed/9 skipped, genomics 637 passed/11 skipped, chemistry 644 passed/4 skipped. Capability registry, 34 JSON Schemas, Ruff E9/F, compilation and Molecular/Molecularis Sequence/Structure benchmark smoke passed.

## Active phase and next exact work

**Active phase:** Service C — Python v1 engineering implementation complete; university review and formal freeze deferred until the complete A–N engineering build per owner direction. A and B engineering implementations remain complete; their university reviews are likewise deferred. The platform is not yet a distributed, multi-language, OS-isolated production runtime.

**Next:** proceed to D — Chemistry. University-level scientific review, cross-reference testing and formal contract freezes will be conducted after the full A–N engineering build, as directed by the owner. Platform-wide recovery, backup/restore, service discovery, language conformance and isolation gates remain open.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.
