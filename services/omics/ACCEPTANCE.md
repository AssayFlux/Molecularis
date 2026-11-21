# Omics Acceptance
Engineering acceptance is defined by automated contract/runtime tests and repository CI. CI run #44895300775 passed all four jobs: core 711 passed/12 skipped; optional Genomics 712/11, Sequence 714/9 and Chemistry 719/4. University scientific review and independent comparison against specialist references are deferred until A–N engineering completion.

Required checks: canonical artifact round-trip/digest; malformed and duplicate JSON; dimensions, identifiers, raw-count integrality and finite values; CPM, CLR, Welch, NB2, diversity and cross-omics correlation; scale mismatch rejection; artifact integrity and budgets; Ruff, compilation, JSON Schema/registry validation, all test profiles and benchmark smoke.

No claim of DESeq2/edgeR parity, biological discovery validity, clinical utility or independent scientific validation is made.


## Agentics scientific acceptance

- [ ] Assay, sample, feature and experimental design semantics documented: Probability/statistics, multivariate analysis, experimental design, normalization, multiple-testing correction, causal inference, missing-data methods and uncertainty.
- [ ] Pre-generation audit checks data permissions, metadata, batch effects and missingness.
- [ ] Statistical assumptions, normalization and multiple-testing correction are explicit.
- [ ] Diagnostics, sensitivity and independent reference tests are available.
- [ ] Effect sizes, uncertainty, confounding and causal limitations are reported.
- [ ] Data/software versions, preprocessing and lineage are reproducible.
- [ ] Engineering and scientific acceptance reported separately.

Shared requirements: ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_FOUNDATION.md.
