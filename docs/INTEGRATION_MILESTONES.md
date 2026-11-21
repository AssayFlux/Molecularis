> **HISTORICAL / SUPERSEDED FOR EXECUTION (2026-11-21):** This document is retained as source history and technical evidence. Do not use it as an active roadmap or implementation authority. The current repository-first plan is [docs/MASTER_PLAN.md](../MASTER_PLAN.md) for files in `docs/`, or [Master Plan](../MASTER_PLAN.md) for files in `docs/alpha/`. Current exact inventory: [REPOSITORY_BASELINE.md](../REPOSITORY_BASELINE.md); capability mapping: [CAPABILITY_STATUS.md](../CAPABILITY_STATUS.md). Reconcile any still-useful details into the current plan before implementation. No completion or validation claim is implied by this historical document.

---


# Molecularis — Integration Milestones

**Status:** Proposed milestone framework; dates and staffing are not committed.  
**Date:** 2026-11-20

## Milestone sequence

| Milestone | Outcome | Required evidence / gate |
|---|---|---|
| M0 — Baseline | Confirm repository baseline, architecture boundaries and current open gates | Exact-head audit, source inventory, dependency/SBOM snapshot, risks and owner-approved architecture decision |
| M1 — Scientific foundation | Shared data representations and versioned contracts | Schema compatibility tests, reference fixtures, unit and coordinate consistency |
| M2 — Desktop interoperability | Bounded worker and Android job-package round-trip | Pairing/security design, offline package tests, resource/cancellation/recovery tests |
| M3 — Structure workflows | Structure parsing, quality observations and viewer integration | Biotite/Mol* licence review, independent structure comparisons, Android device tests |
| M4 — Protein models | Optional ESM/AlphaFold runtime profiles | Model/data rights, reproducible builds, benchmark protocol/results and confidence calibration |
| M5 — Chemistry | RDKit and selected Open Chemistry adapters | Molecule fixtures, descriptor parity, licence and native runtime evidence |
| M6 — Simulation | Complete preparation-to-OpenMM workflow | Topology/parameter provenance, reference-system results, resource and stability tests |
| M7 — Genomics/design | Selected genome and nucleic-acid workflows | Versioned references, curated fixtures, exact dependency/licence review |
| M8 — Workflow layer | Reproducible job/workflow manifests and optional notebook UX | Threat model, provenance completeness, deterministic execution boundaries |
| M9 — Release readiness | Cross-platform and scientific acceptance | Security, privacy, licence, performance, accessibility, device and independent review reports |

## Indicative effort

Earlier planning discussions used broad ranges of roughly 2–8 weeks per phase, depending on scope and dependencies. These are rough planning estimates only, not delivery commitments. Re-estimate after M0 when the exact scope, available hardware, maintainers and acceptance workload are known.

## Execution discipline

- Follow the current approved project track order and two-step build-then-audit rule.
- Do not start a dependent milestone before its prerequisites are evidenced.
- Each milestone has an implementation record and a separate audit/acceptance record.
- A blocked or deferred engine remains explicitly unavailable; do not substitute a mock result.
- Update the integration matrix, runtime matrix, third-party register, validation evidence and roadmap together.
- Record changes to scope, sequence, licensing or intended use in `DECISIONS.md`.

## Definition of done

A milestone is done only when its artifacts are merged, exact-head automated tests pass, reference/platform evidence appropriate to its scope is attached, open risks are dispositioned, documentation is current and the required owner/reviewer gate is recorded. A document or catalogue entry alone does not complete a milestone.
