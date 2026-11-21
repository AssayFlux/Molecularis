# Track G — governance, assurance and publication readiness: closure audit


> **Historical record:** This document records evidence created before the product rebrand. References to Kinetics, the former repository name and historical source paths are retained where needed to preserve the accuracy of the dated evidence. The current product identity is Molecularis; see [the brand migration contract](brand-migration.md).

**Audit date:** 2026-11-17  
**Repository:** `AssayFlux/Kinetics`, branch `main`  
**Final audited commit:** `31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1`  
**Exact-head workflow:** [#44108451571](https://github.com/AssayFlux/Kinetics/actions/runs/44108451571) — **9/9 jobs passed**

## Decision

**G0–G7 bounded research-only engineering foundation: CLOSED.**  
**Overall Track G acceptance: OPEN.**

The final exact-head workflow is attached to the current main commit. The Python foundation job reports 536 passed and 9 skipped; Ruff, mypy, governance structure/register checks and generated capability-claims reproducibility passed. The Android arm64 debug APK/AAB build, package alignment and JVM unit tests passed. The remaining scoped host-side smoke/reference jobs, Node worker security tests and source dependency inventory job also passed.

This closure is limited to repository engineering implementation and automated CI verification. It is not a legal opinion, privacy determination, ethics decision, QMS certification, security certification, scientific validation, regulatory clearance, publication endorsement or release authorization.

## G0–G7 disposition

| Work package | Engineering disposition | Carry-forward evidence still open |
|---|---|---|
| G0 Governance | Stable control IDs, control/evidence register, eight-row requirements traceability, role/cadence model and checker implemented | Owner policy acceptance; named accountable specialist appointments |
| G1 Security | Canonical threat model, UI supplement, 16-case verification matrix, security policy and incident procedure; source configuration guardrails CI-checked | Merged-manifest and physical-device tests, fuzzing, private vulnerability-channel exercise, independent assessment/retest |
| G2 Supply chain | Source SPDX inventory; CI captures Gradle runtime/build-environment graphs, Cargo tree/metadata, artifact hashes and Android Python-wheel hashes | Complete resolved SPDX/CycloneDX SBOM, build-tool/plugin completeness, vulnerability/license review, file-level notices and bundle decisions |
| G3 Quality | Requirements traceability, change/review cadence, CAPA register template and release checklist | QMS applicability advice, actual review records, CAPA effectiveness evidence and owner-approved release controls |
| G4 Privacy | Eight source-level data-flow entries, data classifications, privacy policy and prohibited-data boundary; Android source manifest guardrails checked | Merged-manifest/provider/device/network tests, retention/deletion UX evidence, qualified privacy/legal advice and jurisdiction decisions |
| G5 Scientific integrity | Generated capability claims matrix for 68 executable tool capabilities; conservative wording and validation/device/license gaps | Independent truth sets, biological/clinical validation, ancestry/subgroup/missingness analyses and domain review |
| G6 Publication | Claim-evidence ledger schema, publication integrity and authorship/reproducibility protocol | Evidence-backed claim rows, reproducible literature review, author/contribution/conflict approvals and peer/editor decisions |
| G7 Operations | Incident response, stop-work, rollback, access, backup/recovery and five tabletop scenario templates | Named operators, tabletop exercises, access review, restore exercise and dated governance review |

## Exact-head automated verification

Workflow [#44108451571](https://github.com/AssayFlux/Kinetics/actions/runs/44108451571) ran on `31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1` and completed successfully with **9/9 jobs passed**.

- Python: **536 passed, 9 skipped**.
- Ruff and mypy: passed.
- Governance structure/register checker and generated capability-claims reproducibility: passed.
- Android arm64 debug APK/AAB build, package alignment and JVM unit-test task: passed.
- Pinned Vina engine smoke check, private Node docking-worker security tests, RDKit descriptor sanity fixtures, RDKit ADMET utility smoke check, scientific reference comparisons, source dependency SPDX inventory and OpenMM CPU replica smoke check: passed.
- The nine skipped Python tests require optional RDKit/pysam packages absent from the Python foundation job. Separate pinned jobs passed narrower RDKit/engine smoke checks; skipped tests are not counted as passes.

## Explicit non-claims and open gates

1. **Roles:** the repository owner is identified; specialist security, science, privacy, data, quality, release and publication roles remain UNASSIGNED.
2. **Licensing:** the project license is Apache-2.0. Third-party artifact and data redistribution decisions remain unresolved. Raw dependency reports and hashes are not a complete SBOM or legal clearance.
3. **Security:** no independent penetration/mobile security assessment or physical-device security test is recorded.
4. **Privacy:** source manifest guardrails do not prove merged-manifest, provider, OEM or on-device network behavior; qualified jurisdictional review remains open.
5. **Scientific integrity:** synthetic/reference software comparisons do not establish biological/clinical validity, ancestry coverage or generalisability.
6. **Publication:** the manuscript claim ledger has no supported claim rows. No authorship, funding, conflict, literature novelty, journal fit or peer-review decision is fabricated.
7. **Operations:** tabletop templates remain NOT RUN. No access review, backup restore, incident response exercise or CAPA effectiveness check is claimed.
8. **P0:** remains **BLOCKED / NOT APPROVED**. No patient/clinical data, human-subject work, individual PGx interpretation, diagnosis, treatment/dosing recommendation or Clinical Mode is authorized.

## Track-order disposition

Under D-023, the sequence is **R → S → I → P → G → U**. The bounded G0–G7 engineering foundation is now closed following exact-head CI. Overall governance acceptance and external/operational gates remain carry-forward obligations; they are not waived by engineering closure. Track U is next, and its pre-existing U0–U3 work must be treated as a partial baseline rather than accepted completion.

## Final status vocabulary

- **Engineering foundation:** CLOSED.
- **Exact-head automated verification:** PASSED (9/9 jobs).
- **Independent/external assurance:** OPEN.
- **Operational exercises:** NOT RUN.
- **Overall Track G acceptance:** OPEN.
