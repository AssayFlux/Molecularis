# Track G implementation audit — 2026-11-12


> **Historical record:** This document records evidence created before the product rebrand. References to Kinetics, the former repository name and historical source paths are retained where needed to preserve the accuracy of the dated evidence. The current product identity is Molecularis; see [the brand migration contract](brand-migration.md).

**Audit type:** repository implementation and automated-control audit  
**Audit status:** IN PROGRESS — not a Track G closure or independent assurance report  
**Repository:** `AssayFlux/Kinetics`, branch `main`  
**Evidence baseline at report creation:** `d0ab281cbdbb6156e58fcca92373ab301c78316a`  
**Sequence:** R → S → I → P → G → U (D-023)

## 1. Executive result

The G0–G7 engineering framework is present in the repository and now has automated structural checks. The audit found and corrected two implementation defects during CI:

1. A Ruff line-length failure in the claims generator.
2. A stale claims CSV that included UI catalogue records in addition to executable tool capabilities. The generator's intended scope is the registry's `tools` collection; the corrected matrix contains **68 tool capabilities**, not 130.

The latest exact-head workflow for the evidence baseline above, [#43140079689](https://github.com/AssayFlux/Kinetics/actions/runs/43140079689), was pending when this report was prepared. Therefore this report does **not** claim exact-head CI success. The preceding run [#43139734705](https://github.com/AssayFlux/Kinetics/actions/runs/43139734705) confirmed Ruff, mypy, registry validation and the governance structure checker passed, but failed the claims-matrix reproducibility check before the scope correction. Its Android build was still running. The older run [#43136845552](https://github.com/AssayFlux/Kinetics/actions/runs/43136845552) had passed the Android arm64 APK/AAB build, JVM tests, dependency evidence capture and scientific/engine smoke jobs, but failed Python linting before the lint correction.

**Conclusion:** G engineering implementation is substantial but not yet verified on the final exact head. Track G remains OPEN.

## 2. Implemented repository controls

| Work package | Repository evidence | Current engineering status |
|---|---|---|
| G0 Governance | Control/evidence register, 8-row requirements map, roles/cadence, status vocabulary | Draft controls implemented; owner policy acceptance and role appointments open |
| G1 Security | Canonical app threat model, UI supplement, 16-case verification matrix, SECURITY.md and response procedure | Engineering specification implemented; device/fuzz/private-channel and independent assessment open |
| G2 Supply chain | 16-row dependency decision register, source SPDX inventory, Gradle/Cargo dependency reports and artifact hashes in Android CI | Partial inventory; Python wheel/plugin completeness, full SBOM and license decisions open |
| G3 Quality | Traceability checker, CAPA template, release checklist and CI checks | Structural controls implemented; QMS applicability, actual reviews and operating records open |
| G4 Privacy | 8-flow source-level data inventory and privacy/security requirements | Source inventory only; merged manifest, device/provider tests and qualified advice open |
| G5 Scientific integrity | Generated 68-tool capability claims matrix and registry-to-matrix checks | Claims are conservatively scoped; independent truth sets, subgroup analysis and scientific validation open |
| G6 Publication | Claim-evidence ledger and publication integrity protocol | Protocol implemented; author approvals, literature review and peer/editor decisions open |
| G7 Operations | Incident, stop-work, rollback, access, backup/recovery procedures and five tabletop scenarios | Procedure templates only; operators and exercises open |

## 3. Automated coverage

- **30 control IDs** across G0–G7 are enumerated in the control register and mapped in requirements traceability.
- **8 G requirement rows** map to the control IDs, artifacts, verification approach and remaining limitations.
- **16 security verification cases** have unique stable IDs; their statuses remain OPEN or PARTIAL until actual evidence is attached.
- **68 tool capabilities** are generated from `capabilities/registry.yaml`'s `tools` collection. Every row keeps validation, device and license status explicit; the matrix does not convert implementation into scientific validation.
- **16 dependency decision rows** explicitly distinguish candidate versions from approved redistribution. Blank hashes or UNASSIGNED reviewers remain unresolved rather than inferred.
- CI runs the governance structure checker and verifies that the generated claims matrix is reproducible.

The checks validate document/register integrity. They do not establish that security, privacy, scientific, legal, device or operational controls have passed.

## 4. Open findings and non-delegable evidence

| Finding | Required evidence | Gate |
|---|---|---|
| Exact-head CI | All required jobs pass on one final main SHA; failures fixed and rerun | G0/G3 |
| Dependency completeness | Resolved Gradle plugins/modules, Cargo, Python wheels and build tools tied to exact APK/AAB hashes; complete SPDX/CycloneDX coverage | G2 |
| Redistribution rights | Qualified file/artifact/data/model license review and explicit decisions for each intended bundle | G2 |
| Device security/privacy | Merged manifests, physical-device tests, URI lifecycle, Keystore, logging, WebView and traffic evidence | G1/G4 |
| Independent security | Qualified assessor report, remediation and independent retest | G1 |
| Privacy/legal/QMS | Qualified jurisdiction-specific advice and QMS applicability determination | G3/G4 |
| Scientific validation | Independent reviewers, governed truth sets, pre-specified protocols, uncertainty and subgroup/missingness reports | G5 |
| Publication integrity | Reproducible literature review, actual author/contribution/COI declarations and exact claim evidence | G6 |
| Operational readiness | Named operators; dated incident tabletop, access review and backup/recovery exercises | G7 |
| Owner decisions | Governance-policy acceptance and documented residual-risk/release decisions within lawful scope | G0/G7 |

The repository owner is identified as the owner role. Security, scientific, privacy, quality, data, engineering, release and publication roles remain UNASSIGNED. Implementers cannot self-appoint as independent reviewers.

## 5. Safety and scope boundaries

- P0 remains **BLOCKED / NOT APPROVED**.
- No patient/clinical data, identifiable human-subject activity, individual clinical/PGx interpretation, diagnosis, treatment/dosing recommendation or Clinical Mode.
- No unreviewed engine, model, dataset or guideline content is approved for product bundling.
- CI APK/AAB builds are engineering/debug evidence, not signed production releases.
- Synthetic/software-reference concordance is not biological or clinical validation.
- Track U remains after G under D-023; existing U0–U3 material is retained as prior partial work and is not accepted complete.

## 6. Exit decision

**G0–G7 engineering framework:** implemented at draft/partial maturity.  
**Exact-head automated verification:** pending for the report baseline; prior attempts exposed and corrected defects.  
**Independent/external and operational evidence:** open.  
**Track G closure:** NOT APPROVED / OPEN.

Do not mark G closed or start the next sequential U implementation until the exact-head software gate is verified, the owner reviews the engineering scope, and the outstanding G acceptance requirements are either completed or explicitly carried as non-waivable release blockers. Legal, ethics, independent review and other qualified external determinations cannot be replaced by repository edits or owner permission.
