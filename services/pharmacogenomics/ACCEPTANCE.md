# Pharmacogenomics Acceptance L

Engineering acceptance is distinct from independent scientific or clinical validation.

- Canonical sample artifacts reject malformed dimensions, duplicate keys, duplicate variants, invalid genome builds and patient-classified data.
- Definition packs are bounded, release-pinned, provenance-bearing and validated before storage.
- MSDE ingestion/load verifies digests, metadata, artifact types and budgets.
- Exact matching preserves no-call and ambiguity states; build mismatch fails closed.
- Capability registry, schemas, tests, compilation and benchmark smoke pass in CI.

University review and independent PharmVar/CPIC/DPWG concordance are deferred until A–N engineering completion, as directed. This service does not implement phenotype translation or clinical decision support.


## Agentics scientific acceptance

- [ ] Variant, allele, diplotype and phenotype definitions and applicability documented: Genetics, pharmacology, biostatistics, population variation, causal/evidence appraisal, guideline provenance, allele nomenclature and uncertainty.
- [ ] Pre-generation checks validate reference build, nomenclature, data permissions and source versions.
- [ ] Independent evidence/rule checks and conflict handling are demonstrated.
- [ ] Population limitations and uncertainty are explicit.
- [ ] No unsupported clinical claims or autonomous treatment actions.
- [ ] Qualified review gates and complete provenance are implemented.
- [ ] Engineering and scientific acceptance reported separately.

Shared requirements: ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_FOUNDATION.md.
