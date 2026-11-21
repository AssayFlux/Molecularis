# Service and Platform Status Register

Last verified: 2026-11-21  
Current implementation commit: [172c895eebf04c093ec8758ae093d855c3c55add](https://github.com/AssayFlux/Molecularis/commit/172c895eebf04c093ec8758ae093d855c3c55add)

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
| JSON contracts | CI validation added | Repository-wide schema validation exposed and is correcting one malformed legacy schema |
| Scientific optional CI | Implemented | Run #133: sequence, genomics and chemistry profile jobs passed |
| Native C++ / Rust interoperability | Not implemented | Language-neutral schemas exist; bindings and conformance tests remain required |
| Recovery certification | Partial | Atomic blob publication and integrity audit; crash-boundary fault injection and backup/restore remain open |
| Execution isolation | Partial | In-process trusted handlers; no OS-level sandbox or preemptive CPU/memory/GPU isolation |
| Distributed services | Not implemented | No distributed storage, replication or cross-process service-discovery protocol |
| Scientific validation | Incomplete | Domain-specific independent reference and reproducibility evidence required |

## A–N service sequence

| Step | Service | Existing code | Engine | Runtime | Rulebook | State |
|---|---|---|---|---|---|---|
| A | Molecular | Existing modules; audit pending | Not started | Not started | Not operational | Planned |
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
- [Run #133](https://github.com/AssayFlux/Molecularis/actions/runs/44880802259): all three optional dependency profiles passed; core job exposed a malformed legacy JSON schema wrapped in literal escape markers. The schema is being corrected and the core job must pass before this baseline is upgraded.
- Ruff remains limited to E9/F; this is not full style conformance.

## Active phase and next exact work

**Active phase:** Core/MSDE platform hardening. The local reference implementation has artifact storage, bounded query pagination and success/failure Rulebook evidence. The platform is not yet a distributed, multi-language, OS-isolated production runtime.

**Next:** pass repository-wide schema validation and core CI; then add crash fault injection and backup/restore tests, a durable index segment layer or evidence-backed SQLite index decision, process-level service discovery, C++/Rust conformance, and security/resource-isolation review.

Do not begin service A until the explicit platform acceptance criteria are met and recorded with passing evidence.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.
