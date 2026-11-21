# Track G0 — governance control and evidence register


> **Historical record:** This dated audit/workplan predates the Molecularis rebrand. Former product names, source paths and repository URLs are retained where they document the state of the project at that time. Current identity and compatibility rules are in [brand-migration.md](../brand-migration.md).

**Baseline date:** 2026-11-17  
**Status:** G0–G7 bounded research-only engineering foundation **CLOSED** on exact-head commit `31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1`; workflow [#44108451571](https://github.com/AssayFlux/Kinetics/actions/runs/44108451571) passed 9/9 jobs. Overall Track G acceptance remains OPEN; no independent or operational approval is inferred.  
**Authority:** Owner instruction to execute G; D-023 sequence R → S → I → P → G → U.  
**Scope:** research-only software governance. This register is not an approval, certification, legal opinion, ethics determination or independent review.

## Status vocabulary

- **IMPLEMENTED:** repository artifact or code exists.
- **AUTOMATED-CHECK:** an automated check exists; exact-head result must be cited separately.
- **PARTIAL:** some engineering controls exist, but required scope or evidence is incomplete.
- **OPEN:** evidence, implementation, review or decision is missing.
- **NOT-APPLICABLE (JUSTIFIED):** documented rationale and accountable reviewer are recorded.
- **ACCEPTED:** named authority has made and recorded the decision. Never infer acceptance from a draft, schema or green CI.

An item remains OPEN when evidence is absent, stale, unreviewed, ambiguous or not linked to the exact release/commit. Draft and partial controls do not count as accepted.

## Final exact-head automated evidence (2026-11-17)

- Final main commit: `31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1`.
- Workflow [#44108451571](https://github.com/AssayFlux/Kinetics/actions/runs/44108451571): **9/9 jobs passed**.
- Python foundation: **536 passed, 9 skipped**; Ruff, mypy, governance structure/register checks and capability-claims reproducibility passed.
- Android arm64 debug APK/AAB build, package alignment and JVM unit tests passed. CI also captured Gradle runtime/build-environment graphs, Cargo tree/metadata, resolved artifact hashes and Android Python-wheel hashes.
- Scoped host-side Vina, RDKit, ADMET, OpenMM and scientific-reference smoke/comparison jobs passed; Node worker security tests and source dependency SPDX inventory passed.
- The nine skipped Python tests require optional RDKit/pysam packages absent from the Python foundation job. They are not represented as passes; separate pinned jobs passed their narrower smoke checks.
- Raw dependency reports are not a complete resolved SBOM or license decision. Physical-device, independent security/privacy/scientific/legal review, ethics, owner policy/risk acceptance and operational gates remain OPEN.
- **Engineering foundation: CLOSED. Overall Track G acceptance: OPEN.**

## Control register

| ID | Control / required outcome | Current repository evidence | Status | Accountable role | Next action / acceptance evidence |
|---|---|---|---|---|---|
| G0-01 | Single governance index with stable IDs, status vocabulary and evidence links | This register; implementation plan; docs index | IMPLEMENTED — draft | G-ROLE-OWNER | Owner review and policy acceptance |
| G0-02 | Track/phase status reflects evidence, not aspiration | ROADMAP.md; README.md; track plans; SECURITY.md corrected | PARTIAL | G-ROLE-OWNER + G-ROLE-ENG | Reconcile all historical/stale status claims; exact-head evidence |
| G0-03 | Every capability claim maps to implementation, tests, validation, device evidence and limits | capabilities/registry.yaml; generated capability-claims-matrix.csv; validation/README.md | PARTIAL | G-ROLE-SC + G-ROLE-ENG | Add test-level links and independent records; do not promote evidence_level none |
| G0-04 | Decision authority, approval and supersession are recorded | DECISIONS.md; D-023 | IMPLEMENTED — partial | G-ROLE-OWNER | Record actual G policy decisions and appointments; do not infer approval |
| G0-05 | Requirements and risks map to controls, verification and residual-risk disposition | requirements-traceability.csv; P0 packet and risk schemas | PARTIAL | G-ROLE-QUALITY + G-ROLE-OWNER | Complete risk register and qualified review/owner disposition |
| G0-06 | Change history and evidence remain auditable | SESSION_LOG.md; CHANGELOG.md; Git history; CI artifacts | PARTIAL | G-ROLE-ENG | Link each substantial change to exact-head CI and artifact evidence |
| G1-01 | Threat model covers app, imports, storage, native/runtime, WebView, supply chain and optional remote boundary | docs/security-threat-model.md; scoped UI supplement | IMPLEMENTED — engineering draft | G-ROLE-SEC | Independent threat-model review and residual-risk approval |
| G1-02 | Abuse cases and parser/resource boundaries are tested | Existing parser/import tests; security-verification-matrix.md | PARTIAL | G-ROLE-SEC + G-ROLE-ENG | Execute fuzz, lifecycle, concurrency, URI and device test matrix |
| G1-03 | Vulnerability reporting and incident handling are operational | SECURITY.md; operational-controls.md | PARTIAL — procedure draft | G-ROLE-SEC | Appoint security contact; test private reporting route and triage process |
| G1-04 | Independent security review and remediation evidence exist | No independent assessment recorded | OPEN — external | Independent security assessor | Commission review, track findings, retest and owner residual-risk decision |
| G2-01 | Direct and transitive build/runtime dependencies are enumerated with exact versions and hashes | scripts/generate_source_sbom.py; sbom/; docs/third-party.md | PARTIAL — source declarations plus resolved Gradle/Cargo CI reports and artifact hashes; SPDX remains source-only | G-ROLE-DATA + G-ROLE-ENG | Convert raw Gradle/Cargo/Python-wheel reports into a complete resolved SBOM; bind it to exact artifact hashes and review licenses |
| G2-02 | Every distributed component has license, notices and redistribution decision | LICENSE; docs/third-party.md | OPEN — candidate-only | Qualified legal/licensing reviewer | Exact-artifact/file-level audit, notices, source obligations and explicit bundle decision |
| G2-03 | Datasets, models, reference packs and guideline content have source-specific rights/provenance | data/, datapacks/, docs/third-party.md; P source gates | PARTIAL — policy only | G-ROLE-DATA | Per-release accession, checksum, terms, intended use, attribution and reviewer evidence |
| G2-04 | Build provenance and artifact integrity are reproducible | CI build workflow; artifact hash checker; build evidence | PARTIAL | G-ROLE-RELEASE | Archive exact source, resolved graph, artifact digests, provenance attestation and signing evidence |
| G3-01 | Requirements trace to design, code, tests and release claims | requirements-traceability.csv; registry; tests | PARTIAL — initial map | G-ROLE-QUALITY | Add test-level mapping and verify all material requirements |
| G3-02 | Code/design review and change control are recorded | Git history; CONTRIBUTING.md; review guidance | PARTIAL | G-ROLE-ENG | Define required review evidence and branch protections; retain PR references |
| G3-03 | Defect, nonconformance and corrective-action process exists | capa-register.csv; operational-controls.md | IMPLEMENTED — blank register/template | G-ROLE-QUALITY | Populate only when real findings occur; verify root cause and effectiveness |
| G3-04 | Release criteria and artifact approvals are enforced | docs/release-checklist.md; docs/release-hardening.md | PARTIAL — checklist only | G-ROLE-RELEASE + G-ROLE-OWNER | Tie authorization to exact hashes and completed checks |
| G4-01 | Data flows, assets, trust boundaries and storage destinations are inventoried | data-flow-inventory.md; PRIVACY.md; threat model; manifest | PARTIAL — source-level inventory | G-ROLE-PRIV + G-ROLE-ENG | Verify merged manifest, provider/device behavior and retention/export UX; obtain qualified privacy review |
| G4-02 | Data minimisation, retention, deletion, backup and export behavior are tested | Data-flow inventory; release checklist; manifest | PARTIAL — design/source evidence | G-ROLE-PRIV + G-ROLE-ENG | Add provider/device tests and user-facing retention/export disclosures |
| G4-03 | Lawful basis, roles, notices and jurisdiction obligations are determined | No qualified determination recorded | OPEN — external | Qualified privacy/legal adviser | Written jurisdiction-specific advice; DPIA if applicable; owner accepts policy |
| G5-01 | Scientific claims are scoped to evidence level and abstention behavior | capability-claims-matrix.csv; registry; validation index | IMPLEMENTED — generated draft | G-ROLE-SC | Verify all generated claims and add independent validation records where available |
| G5-02 | Independent reference datasets, protocols and metrics are pre-specified | Synthetic reference scripts and validation docs | PARTIAL — software comparisons only | Independent domain reviewers | Approve governed truth sets, methods, tolerances, coverage and subgroup analysis |
| G5-03 | Bias, missingness, uncertainty and generalisability are reported | Registry and validation policy; no independent domain report | OPEN | G-ROLE-SC + independent reviewers | Add protocol/results; retain unvalidated status until evidence exists |
| G6-01 | Manuscript claims map to exact code, data, methods and results | paper/claim-evidence-ledger.csv; publication-integrity.md | PARTIAL — empty ledger and protocol | G-ROLE-PUB | Populate only evidence-backed claims; attach exact artifact/commit records |
| G6-02 | Authorship, contributions, conflicts, funding and data/code availability are declared | publication-integrity.md | OPEN | All authors + corresponding author | Complete journal-specific declarations and obtain each author's approval |
| G6-03 | Novelty and journal fit are supported by current literature review | No systematic novelty review recorded | OPEN | Corresponding author + domain co-authors | Conduct reproducible literature/software comparison; avoid unsupported priority claims |
| G7-01 | Stop-work, incident, rollback and safe-disablement processes are operational | operational-controls.md; P0 controls draft; release checklists | PARTIAL — procedure only | G-ROLE-OWNER + G-ROLE-SEC | Run tabletop scenarios and record decisions/CAPA |
| G7-02 | Access, secrets, backup/recovery and periodic reviews are governed | Operational controls; repository/security docs | PARTIAL — requirements only | G-ROLE-ENG + G-ROLE-RELEASE | Perform dated access review and recovery exercise; retain evidence |
| G7-03 | Governance exceptions and residual risks have accountable acceptance | P6 schema contract; risk decisions not yet recorded | OPEN | G-ROLE-OWNER + G-ROLE-QUALITY | Record actual scope, rationale, expiry/review date and supporting evidence |

## Role assignments

See [accountability and review cadence](roles-and-review-cadence.md). The repository owner (GitHub: AssayFlux) is the only role identified by repository ownership. Engineering, security, scientific, privacy, quality, data, release and publication roles remain unassigned pending explicit appointments. Independent reviewers must be external to the work they assess.

## Current blockers and non-delegable evidence

1. **P0:** remains BLOCKED / NOT APPROVED. No patient/clinical data, human-subject work, individual PGx interpretation, Clinical Mode or regulated deployment.
2. **Independent scientific validation:** synthetic software concordance is not biological/clinical validation.
3. **Legal/licensing/privacy/ethics:** repository changes cannot substitute for qualified advice, source-specific license decisions or competent ethics determinations.
4. **Independent security review:** no independent penetration/mobile security assessment is recorded.
5. **Device evidence:** CI build/JVM tests do not establish physical-device runtime, lifecycle, accessibility or performance.
6. **Publication:** a paper cannot claim novelty, best-in-class performance, accuracy or impact without reproducible evidence and current comparison.
7. **Operations:** incident tabletop, access review and backup/recovery exercises have not been performed or recorded.

## Review cadence and evidence retention

- Review this register at every track exit and before every public release or manuscript submission.
- Review open controls, roles, vulnerabilities, dependencies, CAPA and P0 boundary monthly while development is active.
- Every status change must include date, reviewer/authority, exact commit or artifact, evidence URI, scope and limitations.
- External evidence must record issuing organisation/person, credentials/authority where relevant, date, scope, version, limitations and permission to retain/share the report.
- Never create fictitious incidents, CAPAs, reviews, test outcomes, appointments or approvals. An empty register means no record has been entered, not that no defects exist.
