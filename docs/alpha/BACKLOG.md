# Alpha Initial Implementation Backlog

This is a prioritized backlog, not a claim that tasks are underway or complete. Each item needs an owner, acceptance criteria, tests and evidence link before closure.

## EPIC A — Baseline and governance
- A1 Record Alpha base SHA and repository inventory.
- A2 Enumerate languages, build systems, modules, generated files, tests and workflows.
- A3 Run exact-Alpha baseline CI and record failures.
- A4 Reconcile existing plans and evidence into current/superseded/historical/needs-review.
- A5 Create Android-to-all-device migration ledger.
- A6 Threat-model API, worker, local node, artifacts and notebook execution.

## EPIC B — Cross-device client
- B1 Choose/reuse web client framework after source audit.
- B2 Implement responsive application shell and navigation.
- B3 Define accessible design tokens and component library.
- B4 Implement PWA manifest, service worker and offline shell.
- B5 Build browser/device automation and WCAG 2.2 AA checks.

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