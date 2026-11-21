# Documentation guide

This is the navigation index for the Molecularis repository. Use the living decision and roadmap files as the authority; session notes and archived instructions are historical evidence, not competing plans.

## 1. Project direction and decisions

| Purpose | Canonical document |
|---|---|
| Product purpose and scope | [North Star](../NORTH_STAR.md) |
| Master plan and track order | [Roadmap](../ROADMAP.md) |
| Approved decisions and supersessions | [Decision log](../DECISIONS.md) |
| Original owner-supplied master (read-only history) | [Archived master](origin/MOLECULARIS_MASTER.md) |
| Session-by-session engineering record | [Session log](../SESSION_LOG.md) |

## 2. Architecture and engineering

| Purpose | Document |
|---|---|
| System boundaries and component architecture | [Architecture](architecture.md) |
| Language ownership and cross-stack contracts | [Engineering integration standard](ENGINEERING_INTEGRATION_STANDARD.md) |
| Android feasibility and platform constraints | [Android feasibility](android-feasibility.md) |
| Scientific engine selection and decision gates | [Scientific engine decisions](scientific-engine-decisions.md) |
| Local build reproduction | [Local Android build](local-android-build.md) |
| Third-party dependency and license register | [Third-party inventory](third-party.md) |

## 3. Track implementation and audit

| Track | Canonical documents |
|---|---|
| R — Research platform | [R0](phase-r0-plan.md), [R1](phase-r1-plan.md), [R2](phase-r2-plan.md), [R3](phase-r3-plan.md), [R4](phase-r4-plan.md), [R5](phase-r5-plan.md), [R6](phase-r6-plan.md), [R7](phase-r7-plan.md), [R8](phase-r8-plan.md), [R9](phase-r9-plan.md), [R10](phase-r10-plan.md), [R-track audit](r-track-audit-2026-11-09.md), [R2 recovery matrix](track-r2/recovery-test-matrix.md) |
| S — Structure, sequence and discovery | [S roadmap](track-s/discovery-and-design-roadmap.md), [S1 viewer](track-s/structure-viewer-contract.md), [S2 quality metrics](track-s/structure-quality-metrics.md), [S4 prediction boundary](track-s/structure-prediction-boundary.md), [S6 unknown-sequence evidence](track-s/unknown-sequence-evidence-contract.md), [S7 contig QC](track-s/genome-contig-qc.md) |
| I — In-silico laboratory | [Software implementation/integration audit (closed)](track-i-audit-2026-11-11.md), [Research boundaries](track-i/research-boundaries.md), [engine and data-source evaluation](track-i/engine-evaluation.md) |
| P — Precision medicine preparation | [P0 evidence packet](track-p/p0-evidence-packet.md), [P0 control drafts](track-p/p0-controls-draft.md), [implementation plan](track-p/implementation-plan.md), [Public-data-only boundary](track-p/public-data-only-preparation.md), [public dataset catalog](track-p/public-dataset-catalog.md) |
| G — Governance and assurance | [Track G implementation plan](track-g/implementation-plan.md), [2026-11-12 implementation audit](track-g/audit-report-2026-11-12.md), [control/evidence register](track-g/control-evidence-register.md), [roles and cadence](track-g/roles-and-review-cadence.md), [requirements traceability](track-g/requirements-traceability.csv), [dependency decisions](track-g/dependency-decision-register.csv), [security verification matrix](track-g/security-verification-matrix.md), [data-flow inventory](track-g/data-flow-inventory.md), [capability claims matrix](track-g/capability-claims-matrix.csv), [publication integrity](track-g/publication-integrity.md), [operational controls](track-g/operational-controls.md), [CAPA register](track-g/capa-register.csv) |
| U — User interface | [Track U implementation plan](track-u/implementation-plan.md), [UI/UX specification](android-ui-ux-spec.md), [owner V1 UI specification](ui/ui-spec.md), [design system](ui/molecularis-visual-design-system.md), [device matrix](ui/device-matrix.md), [screen map](ui/screen-map.md), [quality report](ui/quality-report.md) |
| UI / design system | [UI/UX specification](android-ui-ux-spec.md), [UI document set](ui/ui-spec.md), [root UI spec](../MOLECULARIS_UI_SPEC.md) |

## 4. Validation, security and release

| Purpose | Canonical document |
|---|---|
| Dataset intake and validation policy | [Validation index](../validation/README.md) |
| CI and artifact evidence | [CI build evidence](ci-build-evidence.md) |
| Threat model | [Canonical security threat model](security-threat-model.md), [UI threat supplement](../governance/threat-model.md) |
| Security reporting | [Security policy](../SECURITY.md) |
| Privacy and data handling | [Privacy policy](../PRIVACY.md) |
| Accessibility test plan | [Accessibility plan](accessibility-test-plan.md) |
| Release hardening | [Release hardening](release-hardening.md) |
| Release gate checklist | [Release checklist](release-checklist.md) |

## 5. Repository structure and governance

- [Repository research-readiness audit](research-grade-readiness-audit-2026-11-12.md) inventories the tracked tree, identifies documentation/status drift and sets out a staged, link-safe reorganisation plan.
- Treat `api/` as versioned API/message and evidence contracts; `schemas/` as reusable domain/data schemas. Keep `data/` source catalogues distinct from `datapacks/` manifests and payloads.
- `assets/` is the single canonical artwork root. The legacy root-level `Assets/` directory was consolidated on 2026-11-12 after a content-hash/reference audit; original binary blobs were preserved byte-for-byte. Historical decision/session records may still mention the former paths as accurate records of past work.

## 6. Governance and historical material

- Current sequential order is **R → S → I → P → G → U** under D-023; D-019 is retained as the historical five-track decision it was when approved.
- [Historical parallel-track protocol](parallel-track-execution.md) is **superseded by D-019** and must not be followed.
- [Original master](origin/MOLECULARIS_MASTER.md) is preserved as read-only historical source.
- [Change history](../CHANGELOG.md) records user-visible project changes.
- [Paper skeleton](../paper/manuscript-skeleton.md) is a planning artifact, not a claim of publication readiness.

## Status vocabulary

- **Implemented:** source path and automated tests exist.
- **Regression-tested:** the named automated tests pass on the cited revision.
- **Validated:** independent reference/benchmark evidence exists and is linked.
- **Device-verified:** dated evidence exists for a named device and build.
- **Accepted/done:** the full phase exit criteria and required owner approval are recorded.
- **Blocked:** a named dependency or formal gate prevents the next action.

Never upgrade one status to another without the corresponding evidence.
