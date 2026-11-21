# Service and Platform Status Register

Last verified: 2026-11-21  
Verified CORE commit: [ccae6c1d4fa28dad62d456f2731b03a7f24dfe2e](https://github.com/AssayFlux/Molecularis/commit/ccae6c1d4fa28dad62d456f2731b03a7f24dfe2e)

A scaffold or specification does not imply implementation or scientific validation.

## Platform

| Area | Status | Evidence / next gate |
|---|---|---|
| Governance | Established | North Star, A–N roadmap, future architecture, master plan and rules |
| Existing Python package | Existing implementation; migration not performed | Audit module ownership, public imports and tests before moving |
| Local Core reference runtime | Implemented v0.1 | Lifecycle facade, capability manifest loader, typed contracts and Rulebook executor; tests in `tests/test_platform_*.py` |
| MSDE Stage 1 | Implemented local slice | SHA-256 blob store, SQLite WAL catalog, lineage, atomic publication, bounded streaming, integrity audit |
| Metadata indexes | Functional SQLite indexes | Exact scalar and numeric range lookups; not yet native sorted-segment index engine |
| Query execution | Partial | Bounded candidate/result limits and completeness flag; snapshot pagination/planner still open |
| Evidence | Partial | Successful run records and immutable operation artifacts; failure/partial evidence and input lineage remain open |
| Native C++ / Rust interoperability | Not implemented | Language-neutral schemas exist; bindings and cross-language conformance tests remain required |
| Security / recovery certification | Partial | Path-safe digest-derived object layout; fault-injection, backup/restore and full threat model remain open |
| CI | <badge color="success">Green</badge> | Run #130: 568 passed, 12 skipped, 0 failed |
| Optional scientific test profiles | Incomplete | 12 skips include absent RDKit, Biopython, pysam, Parasail and Biotite |
| Scientific validation | Incomplete | Reference-concordance and domain-specific evidence remain required |

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

## Verified CI baseline

GitHub Actions [run #130](https://github.com/AssayFlux/Molecularis/actions/runs/44880315191): **568 passed, 12 skipped, 0 failed**. The workflow validates the capability registry, Ruff E9/F, Python compilation and pytest. Optional scientific dependency skips remain outstanding. Ruff is not yet a full style gate.

## Active phase and next exact work

**Active phase:** Phase 1 — Core/MSDE platform gate. The local reference slice is functional but the full gate is not passed.

**Next:** finish failed/partial run evidence and input lineage; add stable snapshot-bound pagination and typed query planning; implement the native sorted-segment exact/range index engine; add fault-injection/backup/restore tests and schema validation; then complete language-neutral service discovery and C++/Rust conformance.

Do not begin service A until the Phase 1 exit criteria in the Master Development Plan are evidenced.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.
