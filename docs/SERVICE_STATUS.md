# Service and Platform Status Register

Last verified baseline: CORE commit f0f9e245fc48b33a9b74b57869ccced87528e752  
Status meaning: Scaffold = directories/documents exist; implementation and validation are not implied.

## Platform
| Area | Status | Notes |
|---|---|---|
| Governance documents | In progress | Master policy and operational documents established |
| Core contracts/runtime | Not started | Define and implement minimal vertical slice |
| CI baseline | Needs audit | Prior registry validation failure was reported; re-run against current HEAD |
| Existing Python package | Existing implementation | Flat modules retained; migration not yet performed |
| C++ and Rust roots | Scaffold | No completed native engine claimed |

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
| 13 | cohorts | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |
| 14 | workflows | Scaffold | Existing legacy modules; audit required | Not started | Not started | Existing tests; baseline required | Planned |

## Active work
No service is currently declared active. Next approved task: audit and implement Core substrate, then begin molecular service after Core's minimal contract gate.

## Updating this register
Update only from verified repository evidence. Record commit SHA, test command/results, and date with every material status transition. Never upgrade status based solely on file presence.
