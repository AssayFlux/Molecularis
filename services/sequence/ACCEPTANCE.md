# Sequence v1 Acceptance Record

Status: engineering implementation complete; CI run #153 passed; independent scientific review and formal freeze pending.

## Implemented engineering gates

- [x] Discovery and reuse inventory recorded in ENGINE.md.
- [x] Canonical typed DNA/RNA/protein record and strict JSON contract.
- [x] Immutable MSDE artifact ingestion, digest/metadata verification and lineage.
- [x] Five registered deterministic capabilities and executable Rulebook.
- [x] Versioned artifact-reference, record and operation-report schemas.
- [x] Existing FASTA/FASTQ, translation, alignment, reference-pack, ORF and GFF3 modules retained.
- [x] Unit and integration tests added for normalization, alphabets, duplicate JSON keys, artifact integrity, budgets and Rulebook operations.
- [x] Synthetic fixtures explicitly labeled; no biological reference claim.
- [x] CI coverage added for sequence service tests and streaming benchmark smoke.
- [x] CI run #153 passed: core 624 passed/12 skipped; sequence profile 627 passed/9 skipped. Registry, 31 schemas, Ruff E9/F, compilation and benchmark smoke passed.

## Required before scientific acceptance and freeze

- [ ] Independent review of IUPAC alphabet semantics and supported protein symbols.
- [ ] Independent reference concordance for translation tables and CDS edge cases.
- [ ] Independent alignment/reference-search review, including tie policy, ambiguity and no-hit abstention.
- [ ] FASTA/FASTQ and GFF3 edge-case review against authoritative specifications and fixtures.
- [ ] Reference pack source, release, checksum and license provenance review.
- [ ] Reproducibility and measured scale/performance report.
- [ ] Review of all external adapter versions, licensing and execution isolation.
- [ ] Record reviewer, date, evidence artifacts and disposition; freeze v1 contracts only after approval.

## Explicit exclusions

This acceptance record does not certify gene prediction, function annotation, homology calibration, novelty, pathogenicity, clinical use, cross-language conformance or platform-wide production readiness.


## Agentics scientific foundation acceptance

- [ ] Service scope, assumptions, validity domain and priority disciplines are documented: Discrete mathematics, string/graph algorithms, information theory, probability/statistics, genetics, evolutionary models, sequence alignment and uncertainty in annotation.
- [ ] Typed inputs/outputs preserve units, dimensions, coordinate/reference conventions and evidence class where applicable.
- [ ] Pre-generation checks reject malformed, out-of-domain or unsafe requests and preserve explicit assumptions.
- [ ] Domain-specific post-generation verification is independent of the proposing model where feasible.
- [ ] Numerical/statistical tolerances, uncertainty, sensitivity and limitations are reported where applicable.
- [ ] Source, algorithm, model/tool version, parameters, environment and artifact lineage are traceable.
- [ ] Optional adapters have license/version, resource, failure and verification evidence; registry listing alone is insufficient.
- [ ] Engineering tests and scientific acceptance evidence are reported separately.

Shared policy: ../ai/AI_CONSTITUTION.md. Discipline map: ../ai/SCIENTIFIC_FOUNDATION.md.
