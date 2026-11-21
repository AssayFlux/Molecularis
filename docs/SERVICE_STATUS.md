# Service and Platform Status Register

Last verified: 2026-11-21  
Verified CORE commit: [a6b5840836a94029acb9a94819b84f6c209ffde5](https://github.com/AssayFlux/Molecularis/commit/a6b5840836a94029acb9a94819b84f6c209ffde5)

A scaffold or specification does not imply implementation or scientific validation.

## Platform

| Area | Status | Evidence / next gate |
|---|---|---|
| Governance | Established; roadmap refreshed in this documentation update | North Star, A–N roadmap, future architecture, master plan and rules |
| Existing Python package | Existing implementation; migration not performed | Audit module ownership, public imports and tests before moving |
| Core contracts/runtime | Not complete | Implement executable service lifecycle and contract tests |
| MSDE | Architecture and initial schemas specified; runtime not implemented | Implement store/catalog, journal/recovery, indexes, bounded queries and evidence ledger |
| C++ / Rust | No completed native engine claimed | Introduce only when justified by a measured need and real implementation |
| CI baseline | <badge>Green baseline</badge> | Run #127: 557 passed, 12 skipped, 0 failed |
| Optional scientific test profiles | Incomplete | 12 skips include absent RDKit, Biopython, pysam, Parasail and Biotite; add dedicated jobs |
| Scientific validation | Incomplete | Reference-concordance and domain-specific evidence remain required |

## A–N service sequence

| Step | Service | Scaffold / existing code | Engine | Runtime | Rulebook | Verification | State |
|---|---|---|---|---|---|---|---|
| A | Molecular | Spec scaffold | Not started | Not started | Not operational | Not started | Planned |
| B | Sequence | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; profile needed | Planned |
| C | Structure | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; baseline needed | Planned |
| D | Chemistry | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; RDKit profile needed | Planned |
| E | Protein | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; model/reference profile needed | Planned |
| F | Genomics | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; genomics profile needed | Planned |
| G | DNA/RNA | Scaffold | Not started | Not started | Not operational | Not started | Planned |
| H | Simulation | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; scientific validation needed | Planned |
| I | Kinetics | Scaffold + existing package | Audit required | Not started | Not operational | Existing tests; baseline needed | Planned |
| J | Omics | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; baseline needed | Planned |
| K | Phylogeny | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; baseline needed | Planned |
| L | Pharmacogenomics | Scaffold + legacy modules | Audit required | Not started | Not operational | Existing tests; evidence governance needed | Planned |
| M | Cohorts | Scaffold | Not started | Not started | Not operational | Not started | Planned |
| N | Workflows | Scaffold | Audit required | Not started | Not operational | Existing tests; integration gate pending | Planned |

## Current verified CI baseline

GitHub Actions run [#127](https://github.com/AssayFlux/Molecularis/actions/runs/44879631802): 557 passed, 12 skipped, 0 failed. The baseline pipeline includes dependency installation, package installation, capability registry validation, Ruff E9/F checks, compileall and pytest. Ruff is not yet a full style gate. Optional dependency skips are not evidence of passing those scientific capabilities.

The source SBOM is a declared dependency inventory, not a complete resolved/transitive release SBOM.

## Active phase and next exact work

**Active phase:** Phase 1 — Core/MSDE platform gate.  
**Next work:** implement and test the minimum executable Core service lifecycle and MSDE Stage 1 immutable artifact store/catalog, after confirming schemas, consistency model, threat model and recovery semantics. Keep optional scientific CI profiles as a parallel CI-only foundation task; do not begin service A until the platform gate is met.

## Reporting rule

Update this register only from repository evidence. Every status transition must cite a commit, test run, benchmark or scientific validation artifact. Never upgrade a service to complete based on documentation alone.
