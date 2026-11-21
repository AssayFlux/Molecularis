# Track P — Precision Medicine (PGx First): P0–P7 engineering workplan


> **Historical record:** This dated audit/workplan predates the Molecularis rebrand. Former product names, source paths and repository URLs are retained where they document the state of the project at that time. Current identity and compatibility rules are in [brand-migration.md](../brand-migration.md).

**Scope:** research-only, synthetic fixtures and public non-patient metadata. **Overall:** in progress; P0 NOT APPROVED; no patient/clinical authorization.

## Verified baseline (2026-11-11)
- Commit `e9faf7165ceeb2ee9af9ed08d663c32d0be10cda`; exact-head workflow [#42998496868](https://github.com/AssayFlux/Kinetics/actions/runs/42998496868), 9/9 jobs passed.
- Python 509 passed, 9 skipped.
- APK 70,389,586 bytes; SHA-256 `636476de0eab15b767815499d4220219f8953ff6e04f21dbb3f42b8903c76789`.
- AAB 40,260,318 bytes; SHA-256 `a0cee244440b16f7af6ab9a55be4a1e3ad976f62520e41057269b7b99abe334b`.
- JVM tests, package alignment, engine smoke checks, RDKit, SPDX, Node security and host reference comparisons passed. Engine smoke checks are not biological validation; no physical-device runtime was performed.

## P0 — governance
Draft intended use, exclusions, data inventory, threat model, quality lifecycle, validation matrix, stop-work procedure and risk register exist. Still required: qualified jurisdiction-specific legal/regulatory advice; competent ethics determination; qualified independent clinical/scientific review; approved privacy impact/lawful-basis assessment; security assessment; QMS applicability/approval; exact-source licensing; independent validation protocol approval; residual-risk disposition; formal owner P0 decision. No appointments or approvals are fabricated. P0 remains NOT APPROVED.

## P1 — public-data and synthetic foundation
Implemented metadata-only candidate catalogue, schema/checker, synthetic reference contract and aggregate-only synthetic VCF QC bound to assembly/accession/release/contig/digest/coordinate provenance. Remaining: independent reference concordance, source terms review, fuzz/resource audit and device workflow tests. Acquired catalogue entries remain empty.

## P2 — allele/haplotype research
Existing source includes provenance-bearing PGx definition parsing and conservative fully phased haplotype matching, plus PharmVar TSV parsing with exact-byte SHA-256 and accession preservation. This increment adds synthetic regression coverage for release/digest metadata, build mismatch, ambiguous definitions, exact match and unphased/incomplete abstention. No clinical star-allele caller, diplotype/phenotype inference, CNV/structural caller or treatment output.

## P3 — guideline evidence
Adds versioned research-only guideline metadata schema with source/version, licence state, build, evidence level and reviewer; clinical_decision_support is hard false. No executable recommendation mapping. Exact-source reuse permissions and independent mapping review remain required.

## P4 — human curation
Adds curation record schema with uncertain outcomes, curator role, mandatory second review and hard prohibition on autonomous final classification/clinical use. Actual qualified curators, adjudicated records and operational audit workflow remain outstanding.

## P5 — ethics preparation
Adds protocol template for question, study design, participant criteria, consent/privacy, risk, endpoints, monitoring and stop criteria. No protocol submission, ethics determination, recruitment or human-subject activity has occurred or is authorized.

## P6 — risk/governance
Adds structured risk/control and jurisdiction-review schemas. Contracts hard-prohibit patient-data and Clinical Mode authorization. Actual risk ratings, control verification, security/privacy assessment, QMS determination, independent validation and owner acceptance remain outstanding.

## P7 — regulatory preparation
Defines jurisdiction-specific classification, advice, evidence and prospective-evaluation requirements. No regulator advice, submission, clearance, prospective study or regulated deployment is claimed.

## Stop conditions
Stop affected workflow for patient/identifiable data ingress, unclear source rights, reference mismatch, leak/compromise, unsupported/ambiguous calls, misleading clinical wording, missing/withdrawn approval or unexplained discrepancy. Quarantine, preserve minimum non-sensitive audit evidence, notify owner/competent leads and reopen only after review.

## Completion semantics
Schemas, parsers, synthetic tests and green CI close software verification only. They do not close licensing, scientific, legal, ethics, privacy, clinical, regulatory, human-study or physical-device gates. P0–P7 cannot be marked fully complete until their respective evidence exists.


## Exact-head audit refresh (2026-11-11)
- Commit aee8f1e3a73dfa5136ca2472877bd541727453db; [workflow #43002587271](https://github.com/AssayFlux/Kinetics/actions/runs/43002587271) passed 9/9 jobs.
- Python 522 passed, 9 skipped; Ruff and strict mypy passed.
- Android arm64 debug APK 70,389,802 bytes (SHA-256 `4cd8ce2e1f5e6874e39d589e853fdb801c9322c56461a19703653d031f5f9fb5`); AAB 40,260,451 bytes (SHA-256 `90ce8bbfac2e6a17faf385bcffcee1ddcc179bde1ecc625ef93a5b25ff66bdc1`). 16 KB package alignment and JVM tests passed; no emulator/physical-device runtime.
- Host reference comparisons, OpenMM, Vina, RDKit descriptor/ADMET utility smoke checks, SPDX inventory and Node worker security tests passed. Smoke checks are not biological/clinical validation.
- This verifies the committed software/tests only. P0 is NOT APPROVED; independent P1 reference/source/security/device evidence and P2–P7 operational/external review gates remain open.


## 2026-11-12 — bounded PGx parser hardening (exact-head verification later confirmed)

- P2 audit identified that the provenance-aware JSON allele-definition parser and PharmVar TSV adapter accepted caller-supplied content without explicit byte/record ceilings.
- Added fail-closed positive-integer limits: PGx JSON packs default to 2 MiB, 10,000 definitions and 1,000 variants per definition; PharmVar TSV defaults to 10 MiB and 100,000 data rows. Non-text inputs and invalid limit values are rejected.
- Added synthetic negative tests for byte, definition, variant and row limits, plus invalid input types.
- These changes reduce parser resource-exhaustion exposure; they do not establish source licensing, biological correctness, comprehensive gene coverage or clinical interpretation.
- Latest code/test commits: `30c55ca47fa633a020f3c6fbc9bc3b204b85c3fd` (PharmVar) and preceding PGx commits `bbaa01f16f02fb3aa8dccaab2c3474189d7ae74b`, `76f76dde2eb923733318384e65bf6a8f2fe808de`.
- Subsequent exact-main-head workflow #44078534173 passed 9/9 jobs on 2026-11-17, including the Python unit-test, Ruff and strict-mypy steps. This confirms software verification only; independent PGx reference concordance remains open.


## 2026-11-12 — P4/P6/P7 evidence-contract hardening (exact-head CI subsequently passed)

- P4 curation records now distinguish pending, completed, disagreement and escalated second review. A research-accepted curation record requires completed second review with reviewer role, timestamp and HTTPS evidence reference; autonomous final classification and clinical use remain hard false.
- P6 residual-risk records that claim acceptance now require an accountable role, timestamp and evidence reference.
- P7 jurisdiction records marked advice-received or owner-disposition-pending now require advice evidence and a product-classification field. Patient-data and Clinical Mode authorization remain hard false.
- Added negative/positive synthetic schema tests for these conditions. These are contract checks, not actual reviews, risk acceptances or jurisdiction advice.
- The subsequent exact-main-head workflow #44078534173 passed 9/9 jobs on 2026-11-17. This verifies the committed software/contracts only; it does not establish actual curation, risk acceptance or jurisdiction advice.


## P1/P2 additional audit note — 2026-11-12

- VCF parsing enforces record/sample limits during parsing, and P1 QC retains input-byte, variant and sample ceilings. The changes are included in exact-main-head workflow #44078534173, passed 2026-11-17; independent reference concordance and fuzz/resource audit remain open.
- PharmVar variant construction now rejects boolean coordinates (Python bool is an int subclass), with synthetic negative tests.
- These code changes are included in the exact-main-head workflow #44078534173, which passed 9/9 jobs on 2026-11-17. Independent authoritative reference comparison remains open.


## 2026-11-17 — Track P bounded software-scope audit

- Audited the current `main` head `7967ccb0288ea1d5b82af18f8ab8d886d18d4733`.
- Exact-head GitHub Actions workflow [#44078534173](https://github.com/AssayFlux/Kinetics/actions/runs/44078534173) completed successfully: 9/9 jobs.
- Python foundation job: 543 collected; 534 passed and 9 skipped because optional RDKit/pysam packages were unavailable in that job. Ruff and strict mypy passed.
- Android arm64 debug APK/AAB build, package-alignment verification and JVM unit tests passed. No emulator or physical-device runtime is claimed.
- The workflow also passed host-side numerical/reference smoke comparisons, source SPDX inventory and private Node worker security tests. Those checks are not PGx biological concordance, clinical validation or external security certification.
- P1/P2 synthetic-only parser/QC/matcher foundations and P3–P7 research-only evidence contracts are therefore considered **software-foundation complete** for this bounded scope.
- **Full Track P is not closed.** P0 remains BLOCKED / NOT APPROVED; independent source/licence review, authoritative PGx concordance, fuzzing, device tests, operational curation, ethics, privacy/security/QMS, legal/regulatory advice and explicit owner acceptance remain open.
- Patient data, human-subject work, individual interpretation, clinical recommendations and Clinical Mode remain prohibited/disabled.
