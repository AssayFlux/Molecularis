# Repository documentation and research-readiness audit


> **Historical record:** This document records evidence created before the product rebrand. References to Kinetics, the former repository name and historical source paths are retained where needed to preserve the accuracy of the dated evidence. The current product identity is Molecularis; see [the brand migration contract](brand-migration.md).

**Audit date:** 2026-11-12  
**Audited revision:** `dafc3cad56bc6b9b9b49cc30f9e5f65bbd655c47`  
**Repository:** [AssayFlux/Kinetics](https://github.com/AssayFlux/Kinetics)  
**Method:** GitHub recursive Git tree plus targeted review of the direction files, README, documentation index, architecture, engineering standard, validation/security/licensing documents, Track P plans and evidence, CI workflow, citation metadata and session history.

## Executive assessment

Kinetics has a substantial, unusually broad engineering foundation for an early-stage, offline-first scientific workbench. Its strongest differentiators are the intended capability → engine → data-pack → domain registry, provenance-first workflows, Android/offline constraints, explicit language boundaries, reproducible validation ambitions and conservative separation of research software from clinical authorization.

**It is not yet a research-grade validated scientific platform.** The repository is best described as a research-platform engineering prototype with selected automated software checks and a growing validation/governance framework. The gap is not primarily more folders or more prose: it is traceable evidence that each scientific capability is correct, reproducible, independently compared, appropriately licensed and tested on its declared deployment target.

This audit does not claim every source file was manually code-reviewed. The recursive tree covered 356 tracked files in 55 directories; the review sampled canonical documentation and critical cross-cutting contracts. A file-by-file scientific/code audit remains a separate activity.

## Repository inventory

- 356 tracked files and 55 non-root directories in the audited tree; GitHub reported the recursive tree as not truncated.
- Major implementation areas: `android/`, `python/kinetics/`, `rust/`, `cpp/`, `web/`, `remote-node/`, `engines/`, `datapacks/`, `domains/`, `capabilities/`.
- Scientific evidence and quality areas: `tests/`, `validation/`, `benchmarks/`, `data/`, `schemas/`, `api/`, `sbom/`, `paper/`.
- Governance and design areas: `governance/`, `docs/track-p/`, `docs/track-s/`, `docs/track-i/`, `docs/ui/`, `assets/`, legacy `Assets/`.
- Root direction and project files include README, North Star, roadmap, decision log, session log, license, citation, changelog, security/privacy and contributor guidance.

## Findings and required corrections

### 1. Documentation authority and freshness

- The root README and ROADMAP contain useful status summaries, but some verification summaries still refer to older I-track checkpoints. A reader could mistake an earlier green workflow for verification of the current main revision.
- The README's P table previously described P2–P7 as not started even though research-only schemas, templates and evidence contracts had since been added. This is now corrected to distinguish software preparation from operational/external acceptance.
- `docs/ci-build-evidence.md` is a chronological evidence ledger with older dated runs. It must not be treated as a current-head CI dashboard. Exact source SHA and workflow link are mandatory for every claim.
- `SESSION_LOG.md` is approximately 248 KB. It preserves useful history but is too large to be the first operational read for a new contributor. Keep it append-only for historical traceability; use the README, docs index, roadmap and concise current audit reports for navigation.
- `ROADMAP.md` and `DECISIONS.md` are substantial living ledgers. Do not delete history. Add concise summaries and link focused phase plans rather than duplicating long narrative in multiple locations.

### 2. Directory and naming consistency

- Both `Assets/` and `assets/` exist. This is legal on case-sensitive systems but confusing across platforms and can conceal duplicate artwork. Do not blindly rename: first inventory all references, compare file hashes, select one canonical lower-case location and preserve compatibility or update every reference in one reviewed migration.
- The root `Assets/` contains large legacy design exports and animations; `assets/` contains the newer brand/design asset structure. Distinguish source-of-truth artwork, generated assets and reference-only previews.
- `api/` and `schemas/` coexist. Document their ownership clearly: API/message and evidence record contracts versus reusable domain/data/file schemas. Avoid creating near-duplicate schemas.
- `data/` and `datapacks/` should remain distinct: source catalogues and metadata versus installable pack manifests/content. Keep actual acquired scientific datasets out until source rights and validation are recorded.
- `engines/`, `domains/`, `datapacks/`, `paper/` and `governance/` currently contain several placeholder-only areas. This is acceptable; document them as planned extension points, not evidence of delivered functionality.

### 3. Scientific validation maturity

For every capability promoted beyond implemented, require:
1. A versioned method specification, input/output contract and declared applicability domain.
2. Golden and adversarial test vectors with source, release, checksum, coordinate/build conventions and license metadata.
3. Independent reference implementation or authoritative truth-set comparison, with tolerances and discrepancy adjudication.
4. Reproducible benchmark protocol, raw outputs, hardware/software environment, runtime and peak-memory measurements.
5. Uncertainty, missingness, abstention and failure semantics; no silent best-guess output.
6. Bias/coverage analysis where relevant, including ancestry/population representation for genomic resources.
7. Device/runtime evidence for every Android capability advertised as device-supported.
8. A machine-readable evidence record linked from the capability registry.

Host smoke tests and synthetic fixtures are valuable software tests, but do not establish experimental, biological, clinical or device validity.

### 4. Software supply chain and data governance

- Maintain exact versions, source commits, hashes, SPDX identifiers, notices and redistribution terms for direct and transitive dependencies.
- Keep the SBOM generated from the actual release/build graph; compare it with the checked-in inventory and fail CI on drift.
- Treat public availability as distinct from reuse/redistribution permission. Every acquired dataset needs release-specific terms, attribution, provenance, integrity digest and intended-use review.
- Verify that CI checks generated catalogues, schema compatibility, docs links, reproducible artifacts and security-sensitive parser limits.
- Add dependency vulnerability and secret scanning, artifact provenance/attestation and signed release evidence when the release pipeline is ready.

### 5. Architecture and integration

- Preserve the owner-approved stack boundaries: Kotlin is UI/platform orchestration; Python owns scientific workflows; Rust/C++ are used only behind versioned contracts and measured need; WebView code is presentation-only.
- Keep one canonical cross-component envelope and versioned schemas. Add compatibility tests for producer/consumer pairs, schema migrations and malformed payloads.
- Require every capability registry entry to resolve to existing implementation, tests, engine/data-pack metadata and evidence appropriate to its status.
- Keep the optional remote node disabled unless authentication, authorization, transport security, tenancy/isolation, audit, cancellation, quotas and deployment tests are independently reviewed.
- Do not advertise offline capability until airplane-mode tests prove it for the named workflow and device.

### 6. Track P safety boundary

P0 remains **BLOCKED / NOT APPROVED**. P1 is restricted to synthetic fixtures and permitted non-patient public-source metadata/resources. P2–P7 schemas and templates are engineering contracts only; they are not actual curator reviews, ethics approvals, legal advice, risk acceptance, regulatory classification or prospective evidence. No patient-data, individual clinical interpretation, treatment recommendation or Clinical Mode workflow is authorized.

## Target documentation structure

Keep the current source layout stable while making ownership explicit:

- Root: concise entry point, license, citation, changelog, security/privacy and contributor guide.
- `docs/README.md`: single documentation map and status vocabulary.
- `docs/architecture/`: current architecture, integration contracts and deployment boundaries (migration only after link audit).
- `docs/validation/`: validation strategy, evidence schema, reference-comparison protocol and device test protocol.
- `docs/quality/`: QMS-lite lifecycle, risk process, defect/change control and release checklist.
- `docs/tracks/{r,s,i,p}/`: active phase plans, audit reports and track-specific evidence.
- `docs/ui/`: design and accessibility specifications.
- `docs/archive/`: superseded plans and historical reports, clearly marked; preserve immutable source history.
- `docs/origin/`: owner-supplied historical master only.
- `SESSION_LOG.md`: concise append-only session index; move detailed old narratives only through a separate reviewed archival change.

This is a target map, not a claim that all folders already exist. A physical migration should be a dedicated PR with link checking and no simultaneous scientific code changes.

## Prioritized execution plan

| Priority | Action | Exit evidence |
|---|---|---|
| P0 | Freeze and publish a single current-status dashboard; distinguish source revision, CI state, software implementation, scientific validation, device verification and external approvals | README links to exact current evidence; no stale green status presented as current |
| P1 | Add documentation-link, heading, schema-reference and status-consistency checks to CI | CI fails on broken internal links and contradictory status claims |
| P2 | Define a capability-level validation/evidence record and make registry promotion evidence-gated | Registry checker rejects unsupported validated/device-verified claims |
| P3 | Build reference-comparison suites per scientific domain with pinned truth sets and independent tools | Reproducible reports, tolerances, discrepancy review and provenance |
| P4 | Complete dependency/data licensing and generated SBOM reconciliation | Release-specific SBOM, license notices and data rights evidence |
| P5 | Complete Android physical-device and offline workflow matrix; separately audit optional remote compute | Dated device logs, failure/recovery results and deployment security evidence |
| P6 | Perform case-sensitive asset consolidation and docs folder migration | Full reference search, hash comparison, redirects/compatibility and link CI |
| P7 | Independent scientific, security, privacy, ethics and regulatory reviews where applicable | Signed reports and explicit gate decisions; no self-certification |

## What makes Kinetics distinctive — and what would make it excellent

Potential differentiators are the integrated offline-first Android scientific workbench, cross-language capability registry, reproducibility/provenance model, and explicit device-tier and evidence gates across genomics, structure, chemistry and omics. These are promising design choices, not proof of uniqueness or superiority.

Kinetics will earn research-grade credibility by publishing transparent methods, exact data/software versions, benchmark protocols and raw reproducible results; by comparing against established tools; by reporting failures and limitations; and by obtaining independent scrutiny. Breadth alone will not make it best. A smaller set of deeply validated workflows is more credible than a large catalogue of unverified features.

## Audit limitations

- No local checkout, build, test execution or full static analysis was performed during this documentation/tree audit.
- The GitHub tree and targeted file reads establish repository structure and document contents at the audited SHA, not runtime correctness.
- No external benchmark, competitor comparison, license counsel, ethics determination, clinical review or regulatory advice was performed.
- Findings should be re-audited after the next substantial repository migration or release.


## Follow-up correction — asset-root consolidation (2026-11-12)

After this audit snapshot, the case-sensitive artwork directories were reconciled. The legacy root-level `Assets/` files were moved into the canonical lowercase `assets/brand/` and `assets/design-previews/` locations by reusing their original Git blob SHAs. The duplicate organization SVG was already present byte-for-byte as `assets/brand/brand-logo.svg`; the former `Assets/Kinetics.png` was renamed to `assets/brand/kinetics-background.jpg` because the bytes are JPEG. No supplied binary artwork was converted or recompressed. Active asset documentation and the README now use the lowercase paths. This follow-up does not claim that the separate docs-folder migration or other audit recommendations are complete.
