# Alpha Initial Implementation Backlog

This is a prioritized backlog, not a claim that tasks are underway or complete. Each item needs an owner, acceptance criteria, tests and evidence link before closure.

## EPIC A — Baseline and governance
- A1 Record Alpha base SHA and repository inventory.
- A2 Enumerate languages, build systems, modules, generated files, tests and workflows.
- A3 Run exact-Alpha baseline CI and record failures.
- A4 Reconcile existing plans and evidence into current/superseded/historical/needs-review.
- A5 Create Android-to-all-device migration ledger.
- A6 Threat-model API, worker, local node, artifacts and notebook execution.

## EPIC B — Desktop-first cross-platform application
- B1 Inventory candidate UI frameworks and run a measured vertical slice on Linux, Windows, macOS, Android and iOS/iPadOS.
- B2 Record native integration, accessibility, graphics/3D, offline storage, filesystem, packaging/signing, update, mobile lifecycle and license results.
- B3 Implement desktop application shell and shared design system for Linux/Windows/macOS.
- B4 Implement local projects, settings, offline workflow and local job supervision.
- B5 Add reproducible packaging, signing, install/upgrade/uninstall, update and rollback.
- B6 Add Android and iOS/iPadOS application adapters and lifecycle parity.
- B7 Consider a web companion only after installed application milestones and owner approval.

## EPIC C — Control plane
- C1 Identity, sessions, project membership and RBAC.
- C2 Project/workspace and dataset metadata APIs.
- C3 OpenAPI and JSON Schema contract registry.
- C4 Audit events and exportable activity history.

## EPIC D — Data and jobs
- D1 Artifact upload/download with checksum and content-type validation.
- D2 Object storage and retention policies.
- D3 Durable job state machine and queue.
- D4 Job event stream, cancellation, retry and timeout.
- D5 Provenance manifest and reproducibility export.

## EPIC E — Local and institutional compute
- E1 Molecularis Node threat model and capability model.
- E2 Rust supervisor prototype and signed manifest.
- E3 Pair/revoke workflow and secure transport.
- E4 CPU/memory/disk/GPU resource controls.
- E5 Institutional scheduler connector interface.

## EPIC F — Scientific vertical slices
- F1 Canonical sequence and structure schemas.
- F2 Mol* viewer artifact integration.
- F3 Biotite sequence/structure adapter.
- F4 GWW workflow adapters.
- F5 ESM/AlphaFold isolated model profiles.
- F6 MolProbity validation worker.
- F7 Chemistry/Open Chemistry/ChemGraph adapters.
- F8 OpenMM preparation/simulation/analysis.
- F9 SciREPL-inspired notebook integration.
- F10 Galaxy federation and NUAD/NUPACK review.

## EPIC G — Release and institution readiness
- G1 Complete SBOM and upstream rights register.
- G2 Independent security/privacy review.
- G3 Scientific benchmark and independent domain review.
- G4 Cross-device accessibility and performance evidence.
- G5 Backup/restore, incident and rollback exercises.
- G6 Owner acceptance and versioned release notes.

## EPIC X — Desktop-first cross-platform application
- X1 Framework feasibility spike on Linux, Windows, macOS, Android and iOS/iPadOS; publish scored evidence and licensing review.
- X2 Desktop shell, local projects, settings and offline workflow on Linux/Windows/macOS.
- X3 Shared domain contracts, scientific runtime boundary and local job supervisor.
- X4 Desktop packaging, signing, update/rollback, accessibility and GPU/3D validation.
- X5 Android and iOS/iPadOS application adapters and lifecycle parity.
- X6 Optional web companion only after installed-app foundations and owner decision.
