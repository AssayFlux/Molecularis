# Track P — Precision Medicine (PGx First): bounded software closure audit


> **Historical record:** This dated audit/workplan predates the Molecularis rebrand. Former product names, source paths and repository URLs are retained where they document the state of the project at that time. Current identity and compatibility rules are in [brand-migration.md](../brand-migration.md).

**Audit date:** 2026-11-17  
**Verified baseline:** `7967ccb0288ea1d5b82af18f8ab8d886d18d4733`  
**Exact-head workflow:** [#44078534173](https://github.com/AssayFlux/Kinetics/actions/runs/44078534173) — 9/9 jobs passed.

## Decision

**P1–P7 bounded research-only software foundation: CLOSED.**  
**P0 and full Track P: OPEN / BLOCKED.**

The software closure covers only the research-only foundations described below. It is not a clinical, scientific, regulatory, ethics, privacy, security or release approval.

## Phase disposition

| Phase | Software foundation | Remaining acceptance evidence |
|---|---|---|
| P0 | Intended-use, governance, privacy, security, validation and risk drafts/evidence packet prepared | Competent legal/regulatory and ethics determinations; qualified clinical/scientific review; privacy/lawful-basis and security review; QMS applicability; source rights; independent validation protocol; risk disposition; formal owner gate decision |
| P1 | Metadata-only candidate catalogue; synthetic reference contract; bounded aggregate-only VCF QC; provenance and fail-closed checks | Exact-source terms review, acquired/licensed non-patient resources, authoritative reference concordance, fuzz/resource audit, device workflow verification |
| P2 | Bounded provenance-aware PGx/PharmVar parsing and conservative phased haplotype matching; synthetic negative/abstention tests | Licensed release-pinned source packs, independent biological concordance, broader gene coverage, CNV/SV and complex-allele evidence; no clinical star-allele/diplotype/phenotype engine |
| P3 | Versioned research-only guideline evidence schema; clinical decision support hard-disabled | Licensed guideline corpus, reviewed source mapping and independent wording/evidence review |
| P4 | Human-curation record schema with evidence-backed second-review states | Qualified curator appointments, real adjudication records, operational audit trail |
| P5 | Ethics/adviser protocol template | Competent ethics determination and approval/non-applicability record before any human-subject activity |
| P6 | Risk/control and jurisdiction-review schemas with evidence requirements | Completed risk ratings, control verification, independent security/privacy/QMS review, residual-risk acceptance |
| P7 | Jurisdiction-specific regulatory evidence contract | Qualified jurisdiction advice, classification/strategy, regulator engagement if applicable, approved protocol and prospective evidence |

## Exact-head verification

- GitHub Actions: 9/9 jobs passed.
- Python: 543 collected; 534 passed, 9 skipped because optional RDKit/pysam packages were unavailable in the Python foundation job.
- Ruff and strict mypy: passed.
- Android arm64 debug APK/AAB build, package-alignment verification and JVM tests: passed.
- Host numerical/reference smoke checks, SPDX inventory and private Node worker security tests: passed.
- No emulator or physical-device runtime is claimed.
- Host smoke/reference checks are not independent PGx biological concordance or clinical validation.

## Data and safety boundary

- `data/public-dataset-catalog.yaml` remains metadata-only; acquired entries are empty.
- Synthetic fixtures are not biological cohort evidence.
- No patient or identifiable records, human-subject activity, individual genotype interpretation, diagnosis, treatment/dosing recommendation, clinical report or Clinical Mode is authorized.
- Ambiguous, incomplete or unphased matching must abstain; no guess-based interpretation is accepted.

## Final status

This closes the **bounded software foundation** for the Precision Medicine (PGx First) track. It does not close the full track. P0 remains **BLOCKED / NOT APPROVED**, and all external/scientific/licensing/operational/device gates remain open until actual evidence is produced and reviewed. The next sequential track may proceed under the project’s track-order decision, while these P obligations remain explicit carry-forward items.