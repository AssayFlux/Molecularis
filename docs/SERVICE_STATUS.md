# Service and Platform Status Register

Last verified: 2026-11-21  
Current implementation commit: [7e0785a781a9423746717c3f96c2ad7ed6a1f92a](https://github.com/AssayFlux/Molecularis/commit/fb2afc2017eb0e74e4d4e9209d33323f5b279e6c).

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
| C | Structure | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
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
- Ruff remains limited to E9/F; this is not full style conformance.

## Active phase and next exact work

**Active phase:** Service B — Python v1 engineering implementation complete; independent scientific review and formal freeze pending. Service A remains implementation-complete but independently unreviewed and unfrozen under authorized sequencing exception DEC-0009. The platform is not yet a distributed, multi-language, OS-isolated production runtime.

**Next:** obtain independent scientific review of A's structural Rulebook and fixture provenance, then review B's sequence semantics, genetic-code tables, fixture provenance and adapter evidence. Record approvals and freeze each service contract before advancing. Platform-wide recovery, backup/restore, service discovery, language conformance and isolation gates remain open.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.
