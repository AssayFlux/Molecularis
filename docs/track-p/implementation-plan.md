# Track P — Precision Medicine (PGx First): implementation and verification plan

**Track status:** STARTED 2026-11-11 by project-owner authorization (D-022).  
**Execution model:** two steps — (1) build the documented base; (2) audit, test and fix the base.  
**P0 status:** owner-authorized engineering and institutional research-testing scope OPEN under D-025 (2026-11-18); approval record details pending attachment.  
**Allowed data:** synthetic/public data and patient-derived research data within the exact institutional approval scope and approved environment. Real patient data must not enter GitHub, CI, fixtures, logs or public artifacts.

## Component ownership and integration boundaries
- **Python:** reference-build metadata, normalization/QC, provenance, scientific comparisons and future research analysis.
- **C++:** performance-critical algorithms only after measured need and reviewed cross-language contract; no independent clinical interpretation logic.
- **Kotlin/Android:** Research Mode workflows, bounded import, local persistence, user-visible provenance and safe failure/abstention states.
- **Rust:** security-sensitive parsing or bounded native components only where an explicit integration contract and tests exist.
- **Shared contracts:** versioned JSON Schema/API contracts; source build, coordinate convention, reference digest, parameters and software versions travel with every result.
- **Data boundary:** patient-derived research data may be used only within the institutional approval scope declared by the owner; apply minimisation, access control, retention and approved storage. Clinical decision support and patient-specific recommendations remain disabled.

## Step 1 — build the base

### P0 — governance and safety preparation
1. Draft intended use, excluded use, users, outputs and jurisdiction questions.
2. Create evidence register, data/privacy inventory, threat model, quality lifecycle outline, risk register and stop/incident plan.
3. Identify independent legal, ethics, clinical pharmacology/PGx and scientific determinations required; record evidence owners and status without claiming appointments or approvals.
4. Define independent validation questions, reference truth-set requirements, metrics, subgroup analysis and abstention criteria.
5. Keep every P0 document visibly DRAFT until reviewed and approved by the competent party.

### P1 — public-data and synthetic foundation
1. Maintain metadata-only candidate sources; no source is approved merely because it is public.
2. For future acquired non-patient resources, pin accession/release, exact terms, attribution, retrieval time, intended use and SHA-256; retain provenance and known limitations.
3. Expand synthetic reference-build, contig, coordinate, REF/ALT and normalization fixtures; label every fixture synthetic.
4. Build genotype parsing/QC only against synthetic fixtures until P0 and relevant data-use gates pass. Bind every QC result to a verified synthetic reference sequence (assembly/accession/release/contig/digest/coordinate system); reject unsupported ploidy, mismatched contigs/REF alleles, ambiguous builds, malformed alleles and uncertain mappings rather than guessing.
5. Keep genotype-to-phenotype interpretation, star-allele calling, diplotype/phenotype assignment and guideline recommendations out of scope until later P gates and qualified review.

### P2–P7 — bounded research-only software foundations implemented; operational gates remain open
- **P2:** provenance-bearing PGx definition and PharmVar parsers, conservative phased haplotype matching, digest/release checks, input ceilings and abstention on ambiguous, incomplete or unphased inputs. Synthetic fixtures only; no clinical star-allele caller, diplotype/phenotype inference, CNV/SV caller or treatment output.
- **P3:** versioned research-only guideline evidence schema; clinical decision support is hard-disabled. No executable recommendation mapping or licensed guideline corpus.
- **P4:** human-curation record contract with explicit second-review states and evidence requirements. No qualified curator appointments, real adjudications or operational curation service.
- **P5:** ethics/adviser protocol template only. No ethics submission, determination, recruitment or human-subject study.
- **P6:** risk/control and residual-risk evidence contracts. No completed independent security/privacy/QMS assessment, verified control dossier or accepted residual-risk record.
- **P7:** jurisdiction-review and regulatory-evidence contract. No qualified jurisdiction advice, regulator engagement, clearance or prospective evaluation.

## Step 2 — audit, test and fix
- Verify schema contracts and negative cases; malformed, ambiguous, out-of-range and mismatched-reference inputs must fail closed.
- Test deterministic outputs, provenance preservation, coordinate/build conversions and digest tampering with synthetic truth fixtures.
- Review source terms and attribution for every exact acquired release; remove or quarantine unapproved resources.
- Review privacy/security threat controls and confirm no patient-data path is reachable.
- Run exact-head CI after a stable implementation increment; record exact commit, workflow, jobs and skipped/not-run checks.
- Review Research Mode wording; no diagnostic, treatment, dosing or patient-specific recommendations.
- Record defects, risk decisions, evidence links and owner disposition. CI success is not scientific or clinical validation.

## Exit criteria and closure semantics
The **bounded software foundation** for P1–P7 is closed only when the exact-head automated workflow passes and the repository records the implemented contracts, tests and limitations. This does not close the full Precision Medicine track: P0 and all external, scientific, source/licensing, operational, device, ethics, privacy, security, regulatory and owner-acceptance gates remain open. P0 cannot be passed by owner authorization alone; it requires the competent external determinations and a separate formal owner gate decision. Physical-device tests and any human-subject/clinical evaluation are separate evidence classes.

## Current open items and verified software baseline
- **P0 research-testing scope is owner-authorized under D-025.** The owner declares institutional ethics approval obtained; approval reference and protocol scope are pending attachment. Independent security/privacy review, qualified scientific validation and clinical/regulatory deployment decisions remain open.
- The public dataset catalogue contains candidate metadata only; acquired entries remain empty. No third-party source payload is approved or acquired by this track.
- **P1:** aggregate-only synthetic VCF QC and reference-bound provenance are implemented. Independent authoritative reference concordance, exact-source terms review, fuzz/resource audit and device workflow verification remain open.
- **P2:** parser/matcher contracts and synthetic regression coverage are implemented; licensed real-source packs, independent biological concordance, broad gene coverage and structural-variant/CNV support remain open.
- **P3–P7:** research-only schemas, templates and validation contracts are implemented; guideline mapping, curator operations, ethics determination, completed risk/control verification and jurisdiction-specific advice remain open.
- Exact-head baseline before this documentation closure: commit `7967ccb0288ea1d5b82af18f8ab8d886d18d4733`; workflow [#44078534173](https://github.com/AssayFlux/Molecularis/actions/runs/44078534173), 9/9 jobs passed. Python suite: 534 passed, 9 skipped (optional RDKit/pysam dependencies unavailable in that job); Ruff and strict mypy passed. Android arm64 APK/AAB build, package alignment and JVM tests passed. This is software/CI evidence, not independent PGx validation or device runtime acceptance.
- Patient-data research testing is authorized only within the declared institutional approval. Individual clinical interpretation, diagnosis, treatment/dosing recommendations, patient-facing clinical reports and Clinical Mode are not authorized by D-025.
