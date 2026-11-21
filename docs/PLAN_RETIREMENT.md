# Planning Document Retirement and Historical Record Map

**Date:** 2026-11-21  
**Canonical implementation authority:** [MASTER_PLAN.md](MASTER_PLAN.md)

The repository accumulated several generations of plans. This reset removes competing execution authority, not the evidence needed for safe migration. The original owner specification and R/S/I/P/G/U work packages were reconciled in [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md); do not discard their scientific requirements or implementation history.

## Active authority after this reset

1. `NORTH_STAR.md` — product purpose and owner-approved platform direction.
2. `docs/MASTER_PLAN.md` — single implementation plan, phase order and completion gates.
3. `docs/REPOSITORY_BASELINE.md` — exact repository snapshot and observed gaps.
4. `docs/CAPABILITY_STATUS.md` — source-to-capability mapping and migration obligations.
5. `DECISIONS.md` — append-only decision history; superseded decisions remain visible.
6. Domain-specific schemas, validation fixtures, security standards and third-party rights records remain authoritative within their technical scope unless explicitly superseded.

## Superseded planning documents

The following documents are no longer execution authorities. Their useful facts must be reconciled into the new plan; preserve the original text as dated historical evidence until the new plan and migration ledger are accepted.

| Existing document | New authority / disposition |
|---|---|
| `ROADMAP.md` | Replaced by `docs/MASTER_PLAN.md`; root roadmap becomes a short pointer |
| `docs/alpha/MASTERPLAN.md` | Superseded sequencing; useful requirements mapped in `REQUIREMENTS_TRACEABILITY.md` |
| `docs/alpha/BACKLOG.md` | Superseded as a separate backlog; retain unmigrated tasks via capability/traceability audit |
| `docs/alpha/MIGRATION_PLAN.md` | Superseded as separate roadmap; retain detailed Android data migration requirements and reconcile them before any code removal |
| `docs/alpha/BASELINE_AUDIT.md` | Historical branch snapshot; use `docs/REPOSITORY_BASELINE.md` for current snapshot |
| `docs/alpha/INTEGRATION_CATALOG.md` | Candidate details retained; use third-party register plus capability status |
| `docs/MASTER_SCIENTIFIC_INTEGRATION_PLAN.md` | Superseded; retain technical notes as historical until reconciled |
| `docs/INTEGRATION_MILESTONES.md` | Replaced by the phase sequence in master plan |
| `docs/DESKTOP_COMPUTE_ARCHITECTURE.md` | Earlier Android-first compute topology; reconcile relevant controls with current architecture |
| `docs/alpha/DEVICE_MATRIX.md` | Supporting platform acceptance matrix; not an independent roadmap |
| `docs/alpha/LANGUAGE_STRATEGY.md` | Supporting language boundary reference; framework choice remains open |
| `docs/alpha/OPERATIONS_AND_COMPUTE.md` | Supporting compute/security reference; master plan governs sequencing |
| `docs/architecture.md` | Target architecture reference; must remain consistent with master plan |
| `docs/README.md` | Documentation index; update to point to the new authority and label legacy tracks |

## Preserve; do not delete as part of plan cleanup

- `docs/origin/KINETICS_MASTER.md` and all original owner requirements; its Android-first sequence is superseded, not its scientific scope.
- R0–R10, S1–S10, I, P0–P7, G0–G7 and U0–U6 implementation plans, detailed audit records, open issues and evidence; treat them as traceability/source history, not a competing release roadmap.
- `DECISIONS.md`, `SESSION_LOG.md`, `CHANGELOG.md`, dated audits and CI evidence.
- `docs/origin/`, historical track audits and closure records.
- Scientific rulebooks, schemas, validation protocols, fixtures, SBOMs, security/privacy/ethics records, accessibility specifications and UI/design assets.
- Source code, tests, workflows, datasets, project files and user data.

These are evidence, contracts or migration inputs, not competing master plans. Deleting them would break traceability, compatibility or safe migration.

## Cleanup rule

After the owner accepts the new plan, obsolete roadmap/backlog copies may be moved into `docs/archive/` with their original dates and links recorded here. Do not permanently erase audit or scientific evidence. Do not remove a document while active links, CI checks, schemas, code comments or external references still depend on it. Perform moves/deletions through a reviewed PR and run link/documentation checks.
