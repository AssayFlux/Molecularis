# Track I — Software implementation and integration audit


> **Historical record:** This document records evidence created before the product rebrand. References to Kinetics, the former repository name and historical source paths are retained where needed to preserve the accuracy of the dated evidence. The current product identity is Molecularis; see [the brand migration contract](brand-migration.md).

**Disposition: SOFTWARE CLOSED · REAL-WORLD ACCEPTANCE OPEN**

- Audit date: 2026-11-11
- Repository: `AssayFlux/Kinetics`
- Exact audited main revision: `aabe37808a5494acb2171b6ed71d2661b4dd2453`
- Exact-head CI: [GitHub Actions #42970328048](https://github.com/AssayFlux/Kinetics/actions/runs/42970328048)
- CI result: completed, success, **9/9 jobs passed**

## Scope and decision

The documented I1–I5 software scope is implemented to the current research-only boundary and audited for cross-component contracts, bounded inputs/outputs, provenance, schema enforcement, regression coverage and Android/host integration. The exact-head CI pass is the acceptance evidence for this software checkpoint. No further I-track software blocker was identified in this bounded audit that prevents moving to the next planned track.

This closes the **current software scope**; it does not promise that no future defect or enhancement will ever be needed. Defects found later must be fixed under normal regression/CI controls. Expanded scientific capabilities require a separate roadmap increment.

## Component audit

| Area | Software implementation reviewed | Automated evidence | Real acceptance still open |
|---|---|---|---|
| I1 chemistry | Host RDKit sanitization/descriptors/Morgan fingerprints; bounded Android SDF/MOL graph-only preview; provenance and explicit limitations | Pinned ethanol/benzene references, Python tests, Android integration contract and JVM/build checks | Broader curated chemistry references; named-device import/runtime; Android RDKit ABI/size/licence decision |
| I2 docking | Bounded prepared-PDBQT Vina 1.2.7 runner; protocol/input/engine/pose hashes; strict result schema; disabled-by-default authenticated Node worker | Vina engine smoke, Node worker security tests, schema/contract tests | Independent redocking/cross-docking RMSD and decoy enrichment; approved secure-node deployment; full transitive binary SBOM/licence review |
| I3 molecular dynamics | OpenMM 8.6.1 CPU runner for trusted constructed systems; bounded independent replicas/DCD; deterministic signed-32-bit seeds; provenance | Synthetic harmonic two-particle smoke and seed-boundary regression tests | Approved biomolecular force-field/parameter sources; biomolecular stability/energy/convergence and independent references; secure compute |
| I4 PK/PD and ADMET | One-compartment oral PK and Emax references; scaffold-group splitting; binary metrics/calibration; Tanimoto applicability-domain utilities; metadata-only source catalogue | SciPy DOP853 comparisons; RDKit utility smoke; deterministic/schema/edge-case tests | Approved data licences/intake; trained model; external held-out validation; PBPK remains outside implemented scope |
| I5 cohort/effect simulation | Seeded synthetic Hardy–Weinberg counts and caller-supplied additive effects; aggregate-only output contract | Determinism, count conservation, schema, bounds and aggregate-only tests | Governed real cohort intake, population/fairness/portability review and independent effect-model validation |

## Exact-head verification record

Workflow #42970328048 on the exact audited SHA completed with all nine jobs successful:

1. Python foundation, registry and tests — **490 passed, 9 skipped**; Ruff and strict mypy passed.
2. Android arm64 debug APK/AAB build and package tests — passed; 16 KB native alignment and JVM tests passed.
3. Pinned RDKit descriptor sanity fixtures — passed.
4. Pinned AutoDock Vina engine smoke — passed (engine smoke only).
5. Pinned OpenMM CPU replica smoke — passed (synthetic system only).
6. Pinned RDKit ADMET evaluation utility smoke — passed (no trained model or acquired data).
7. Private Node docking-worker security tests — passed.
8. Pinned host scientific-reference comparisons — passed.
9. Declared source dependency SPDX inventory — generated successfully.

Android artifact bundle: [workflow artifact 13832813087](https://github.com/AssayFlux/Kinetics/actions/runs/42970328048/artifacts/13832813087), 80,653,407 bytes.

## Open real-world tests and approvals

These remain explicitly open and must not be represented as completed by CI:

- **I1:** expanded independently curated chemistry references; physical Android device installation, SAF import/export, runtime and lifecycle checks; Android RDKit packaging/licence decision.
- **I2:** independent redocking/cross-docking and decoy enrichment; deployed secure node; complete transitive binary/model/dependency provenance and licence review.
- **I3:** selected/licensed biomolecular force fields and parameter sources; representative biomolecular stability, energy conservation, timestep/equilibration/replica convergence and independent reference review.
- **I4:** approved/licensed dataset intake, trained-model provenance, leakage-controlled external holdout and independent performance/calibration review. No clinical/dosing use.
- **I5:** governance for public cohorts, population/fairness/portability assessment and independent variant-effect validation.
- **Cross-cutting:** physical-device verification, full third-party licensing, security review and owner acceptance.

P0 remains blocked. Patient data, clinical workflows and Clinical Mode remain disabled.

## Next track

Track I software exit is closed. Track P is next in the approved R → S → I → P → G sequence, but remains **not started** pending its own preparation and P0-boundary review. Only public-data metadata and synthetic/non-patient preparation may proceed before P0; patient-related and clinical features remain blocked.
