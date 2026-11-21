# Service and Platform Status Register

Last verified baseline: CORE commit fa611529d83c455d1040ddad0e6dbb6484d6ae1d. A scaffold/specification does not imply implementation or validation.

## Platform
| Area | Status | Notes |
|---|---|---|
| Governance documents | In progress | Master policy and operational documents established |
| Core contracts/runtime | Not started | Minimal vertical slice remains |
| CI baseline | Failing baseline | Run 120 fails at capability registry validation; Python compile and tests skipped |
| Existing Python package | Existing implementation | Flat modules retained; migration not performed |
| C++ and Rust roots | Scaffold | No completed native engine claimed |
| MSDE | Architecture specified | Engine/runtime/Rulebook specs and initial schemas; no runtime/index implementation yet |

## Services
| Order | Service | Filesystem | Engine | Runtime | Rulebook | Verification | State |
|---:|---|---|---|---|---|---|---|
| 1 | molecular | Scaffold | Not started | Not started | Not started | Not started | Planned |
| 2 | sequence | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 3 | structure | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 4 | chemistry | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 5 | protein | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 6 | genomics | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 7 | dna-rna | Scaffold | Not started | Not started | Not started | Not started | Planned |
| 8 | simulation | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 9 | kinetics | Existing package plus scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 10 | omics | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 11 | phylogeny | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 12 | pharmacogenomics | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 13 | cohorts | Scaffold | Existing legacy modules; audit required | Not started | Not started | Not started | Planned |
| 14 | workflows | Scaffold | Existing legacy modules; audit required | Not started | Not started | Not started | Planned |

## Active work
MSDE architecture specification is established. Next exact task: resolve the P0 registry/CI baseline separately, then implement MSDE Stage 1 local artifact store and catalog.

Update this register only from verified repository evidence.
