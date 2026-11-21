# P0 — Governance and safety evidence packet

**Status: OWNER-AUTHORIZED RESEARCH-TESTING GATE OPEN (D-025, 2026-11-18).**  
**Institutional approval:** The project owner declares that institutional ethics approval has been obtained. The approval document, reference, institution, date, approved protocol scope and conditions have not yet been attached to this repository and are not independently verified here.  
**Engineering authorization:** Full software implementation and testing, including institutionally authorized patient-data research testing, are authorized by the project owner.  
**Remaining boundary:** This does not by itself establish regulatory clearance, clinical validity, medical-device authorization or permission for clinical deployment or treatment decisions.

## 1. Draft intended use (owner/adviser review required)
Molecularis is being developed as an offline-first computational biology and in-silico research workbench. Current permitted work is software development, synthetic fixtures and appropriately licensed public non-patient research resources. Outputs are exploratory research artifacts with provenance, limitations and uncertainty; they are not patient-specific medical advice or a substitute for professional judgment.

The eventual PGx research scope is a future objective, not a current authorization. Intended use, users, outputs, deployment model and jurisdictions must be specified and reviewed before patient-related work.

## 2. Owner-authorized research-testing scope and continuing boundaries

The owner has instructed that P0 must not act as a blanket engineering-development blocker. The owner also declares that institutional ethics approval has been obtained. Accordingly, engineering implementation and research testing with datasets covered by that institutional approval are authorized for this project.

Before importing any patient-derived dataset, the operator must ensure that the exact activity, dataset, user, location, retention and analysis are within the institution's approval and applicable consent/authorization. The approval reference and scope must be entered in the project approval record when supplied. This repository does not claim to have independently inspected the approval.

- Patient-data research testing: owner-authorized within the declared institutional approval scope; keep data on the authorized device/environment and out of source control, GitHub issues/PRs, CI logs, test fixtures and public artifacts.
- Human-subject recruitment, consent collection, interventions and prospective evaluation: only within the exact approved protocol and institutional procedures.
- Clinical diagnosis, treatment/medication selection, dosing, patient-facing recommendations and clinical decision support: remain disabled unless separately designed, validated and authorized.
- Clinical-system connections, remote processing and cross-border transfer: remain disabled until their specific security, privacy, legal and institutional controls are implemented and approved.
- No feature may claim clinical validity, clinical utility or regulatory clearance merely because research testing is authorized.

## 3. Evidence register

| ID | Required evidence | Current status | Evidence owner |
|---|---|---|---|
| P0-E01 | Intended-use statement, users, outputs, exclusions and deployment boundaries | Draft here; review pending | Project owner + qualified advisers |
| P0-E02 | Jurisdiction and product classification assessment, including privacy, health-data and medical-device rules | Pending; qualified external advice required | Legal/regulatory adviser |
| P0-E03 | Research ethics / IRB / IEC determination and approval or documented non-applicability, as applicable | Project owner declares institutional approval obtained; approval reference, copy, scope and conditions are pending attachment and repository verification | Research lead + ethics body |
| P0-E04 | Qualified clinical pharmacology / PGx and scientific adviser review, conflicts and scope | Pending; no adviser review claimed | Project owner |
| P0-E05 | Data inventory, lawful basis/authority, privacy impact assessment, minimisation, retention/deletion and data-subject handling | Engineering data-boundary and lifecycle draft in p0-controls-draft.md; legal/privacy review and lawful-basis determination pending | Privacy lead / legal adviser |
| P0-E06 | Threat model, security architecture, access control, encryption/key lifecycle, logging, incident response and recovery | P-specific threat-model draft in p0-controls-draft.md; security review and control verification pending | Security owner |
| P0-E07 | Software quality lifecycle: requirements, risk controls, traceability, verification, change control, defect/CAPA and release records | Draft lifecycle outline in p0-controls-draft.md; owner/adviser approval pending; no QMS certification claimed | Engineering + owner |
| P0-E08 | Dataset/source terms, attribution, redistribution and intended-use review for each exact release | Candidate catalogue only; no acquired entries approved | Data curator + legal reviewer |
| P0-E09 | Independent scientific validation strategy, truth sets, metrics, subgroup/bias analysis and abstention | Draft staged validation matrix in p0-controls-draft.md; independent reviewer approval pending; no clinical validation claimed | Independent scientific reviewers |
| P0-E10 | Incident, stop-work, withdrawal, breach escalation and safe disablement procedure | Draft stop-work and incident workflow in p0-controls-draft.md; owner/security/privacy review pending | Owner + security/privacy leads |
| P0-E11 | Consolidated risk register with mitigations, residual-risk acceptance and owners | Initial draft below; review pending | Engineering + owner + advisers |
| P0-E12 | Final evidence review and explicit owner P0 gate decision recorded in DECISIONS.md | D-025 opens engineering and institutionally authorized research-testing scope; clinical deployment decision remains separate and open | Project owner |

## 4. Work products to prepare
- Intended-use and claims register: users, environment, inputs/outputs, foreseeable misuse, exclusions and jurisdiction assumptions.
- Data protection assessment: data-flow inventory, classification, lawful authority, minimisation, purpose limitation, retention/deletion, access, data-subject requests, cross-border transfer and breach response.
- Threat model: assets, trust boundaries, attacker capabilities, abuse cases, controls, residual risks and verification evidence. Do not introduce sensitive data to test this draft.
- Software quality plan: requirements/traceability, architecture review, risk management, code review, reproducible builds, verification, defect handling, change control, release approval and monitoring.
- Scientific validation plan: independent reference sets, inclusion/exclusion criteria, pre-specified metrics, build/coordinate handling, error analysis, calibration, subgroup coverage, uncertainty and abstention.
- Dataset approval record: exact accession/release, source URL, terms, retrieval date, SHA-256, attribution, intended use, known bias, redistribution status and reviewer evidence.
- Stop/withdrawal plan: triggers, responsible decision-maker, disabling affected capabilities, preserving audit evidence and reopening only after documented review.

## 5. Initial risk register (engineering draft)

| Risk | Initial control | Residual status |
|---|---|---|
| Exploratory output mistaken for patient advice | Research-only UX, explicit limitations, no patient-care workflow or clinical claims | Open; misuse/wording review required |
| Incorrect reference build/coordinate interpretation | Explicit assembly/accession/contig/coordinate contract, digest verification, abstention | Open; independent truth-set concordance required |
| Unlicensed or misused public resource | Candidate-only catalogue; exact-release terms review before intake | Open; human review per source |
| Sensitive data enters an unapproved workflow | Reject patient data at boundaries; no intake path; synthetic fixtures only | Open; threat-model negative tests required |
| Software defect creates misleading output | Bounded schemas, provenance, regression tests, review and traceability | Open; QMS and independent verification plan required |
| Population bias / poor generalisability | Record cohort/source and coverage; subgroup analysis and abstention plan | Open; governed references and adviser review required |
| Security compromise or data exposure | Minimise data, local-first design, threat model, access/key controls, incident plan | Open; security review and verification required |

This is not a completed risk analysis. Severity, likelihood, detectability, acceptability criteria, control verification and residual-risk sign-off require qualified review.

P-specific data governance, threat-model, quality-lifecycle, validation and stop-work drafts are collected in [p0-controls-draft.md](p0-controls-draft.md). They are engineering working documents, not approvals.

## 6. External determinations and reviews
Repository changes cannot manufacture:
- Jurisdiction-specific legal and regulatory advice for each intended deployment.
- Ethics committee / IRB / IEC determination and approval or documented exemption/non-applicability where appropriate.
- Qualified clinical pharmacology, pharmacogenomics and scientific review.
- Privacy/legal determination of lawful basis, controller/processor roles, consent/data-use terms and cross-border obligations.
- Independent scientific validation and, if required by intended use, prospective clinical evaluation.

The project owner authorizes preparation and may approve internal project decisions. Owner authorization does not replace independent determinations.

## 7. P0 exit checklist
- [ ] Intended use, user groups, outputs, exclusions and jurisdictions are specific and reviewed.
- [ ] Applicable legal/privacy/regulatory requirements have written qualified advice.
- [ ] Ethics/IRB/IEC applicability is determined by the competent body; required approval is obtained.
- [ ] Qualified clinical/scientific advisers have reviewed scope and evidence plan.
- [ ] Privacy impact assessment and data governance are complete.
- [ ] Threat model and security controls are reviewed and tested.
- [ ] Quality lifecycle, traceability, verification and change controls are approved for intended scope.
- [ ] Exact dataset/source terms and data-use rights are reviewed.
- [ ] Independent validation plan and acceptance criteria are approved.
- [ ] Risk register, stop/withdrawal and incident plans are reviewed; residual risks dispositioned.
- [ ] Project owner reviews the complete evidence packet and records the formal P0 decision.

**Disposition:** the owner-authorized engineering and institutional research-testing scope is OPEN under D-025. This packet is not a clinical-deployment approval: clinical decision support, diagnosis, treatment/dosing recommendations and patient-facing clinical functionality remain disabled until their separate evidence and authorization are complete.


## 6. Owner declaration and approval-record completion

On 2026-11-18, the project owner stated in the KINETICS project conversation that institutional approval has been obtained and authorized the engineering team to proceed with the full system, including patient-data testing within that approval. This is recorded as an owner declaration, not as independent verification of the underlying approval.

Approval-record fields to complete when the owner supplies the source document: issuing institution/ethics committee, approval or reference number, approval date, protocol title/version, principal investigator, covered population and data types, permitted analyses, consent/waiver basis, storage and retention conditions, participating sites, expiry/continuing-review date, and any restrictions.

The application must display a concise research-use caution and must not send patient data to GitHub, CI, telemetry or an unapproved remote service. The Android app's current input payload encryption does not mean every metadata/result store is encrypted; see PRIVACY.md and the Track U security audit. This record does not assert that all P0 evidence items, independent security review, scientific validation or clinical deployment requirements are complete.
