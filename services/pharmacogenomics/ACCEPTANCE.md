# Pharmacogenomics Acceptance L

Engineering acceptance is distinct from independent scientific or clinical validation.

- Canonical sample artifacts reject malformed dimensions, duplicate keys, duplicate variants, invalid genome builds and patient-classified data.
- Definition packs are bounded, release-pinned, provenance-bearing and validated before storage.
- MSDE ingestion/load verifies digests, metadata, artifact types and budgets.
- Exact matching preserves no-call and ambiguity states; build mismatch fails closed.
- Capability registry, schemas, tests, compilation and benchmark smoke pass in CI.

University review and independent PharmVar/CPIC/DPWG concordance are deferred until A–N engineering completion, as directed. This service does not implement phenotype translation or clinical decision support.
