# Molecularis — Decision Log

Open questions are not decisions. Record date, context, options, choice, consequences and approver.

| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-000 | 2026-11-07 | Adopt owner master and living direction files | Approved | Project owner |
| D-001 | 2026-11-07 | Project LICENSE | Approved — Apache-2.0 selected; preserve canonical LICENSE | Project owner |
| D-018 | 2026-11-09 | Engineering language ownership and integration standard | Historical baseline; updated by D-027 | Project owner |
| D-023 | 2026-11-12 | Sequential execution order R→S→I→P→G→U | Historical; Alpha roadmap supersedes sequencing where it conflicts | Project owner |
| D-026 | 2026-11-21 | All-device product direction | Approved by explicit owner instruction; Alpha is branch name, not a brand | Project owner |
| D-027 | 2026-11-21 | Preferred core languages | Approved preference: C++, Rust and Python; TypeScript/JavaScript remains necessary for web/PWA client | Project owner |
| D-028 | 2026-11-21 | Android-native roadmap | Retired as product direction; preserve useful code and data during migration | Project owner |
| D-029 | 2026-11-21 | Alpha branch base | Created from current default branch CORE; no direct commits to CORE | Project owner direction; execution recorded by contributor |

## D-026 — All-device product direction

Molecularis becomes an all-device scientific research platform. Responsive web/PWA is the primary experience. Optional desktop packaging, a local compute connector, hosted workers and institutional/HPC connectors provide device-appropriate compute. Existing Android-specific work is audited and migrated rather than discarded. Preserve research-only and clinical-safety restrictions.

## D-027 — Preferred languages

C++, Rust and Python are preferred core languages. C++ is for measured numerical/performance kernels; Rust for safe parsers, validation and secure native services; Python for scientific orchestration and research integration. TypeScript/JavaScript is required for browser/PWA presentation and visualization. Use versioned contracts and stable ABI/IPC boundaries.

## D-028 — Android retirement and migration

No Android-native product roadmap. Existing Android/Kotlin work is migration context until equivalent cross-device capabilities and user-data migration are verified. Maintain a component parity ledger and preserve algorithms, tests, schemas, provenance and user data.

## D-029 — Alpha branch

Alpha was created from CORE, the repository's actual default branch at branch creation. It is the isolated implementation branch for the all-device transition. All Alpha changes remain separate from CORE until reviewed and merged by the repository owner.
