# Service and Platform Status Register

Last verified: 2026-11-21  
Current implementation commit: [e2957f801f307f1c5cdc470e1f9ca0e3e12bee68](https://github.com/AssayFlux/Molecularis/commit/e2957f801f307f1c5cdc470e1f9ca0e3e12bee68).

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
| A | Molecular | Native v1 graph model, hierarchy, coordinates and serialization | In progress | Local Python reference model | v1 structural rules; scientific approval pending | Implementation in progress |
| B | Sequence | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
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
- [Run #142](https://github.com/AssayFlux/Molecularis/actions/runs/44882468777), commit `e2957f8`: 593 passed, 12 skipped; core, schema validation, Ruff, compilation and all sequence/genomics/chemistry optional profiles passed.
- Ruff remains limited to E9/F; this is not full style conformance.

## Active phase and next exact work

**Active phase:** Service A — Molecular v1 foundational model, while Core/MSDE hardening continues. The platform is not yet a distributed, multi-language, OS-isolated production runtime.

**Next:** run and repair A-specific and repository-wide tests, integrate the molecular artifact with the MSDE contracts, add independent chemistry/macromolecule reference fixtures, then close A's acceptance gates. Continue platform crash recovery, backup/restore, service discovery, language conformance and isolation work. The platform gate remains open.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.
