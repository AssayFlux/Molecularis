# R8 — Omics and multi-omics

**Status:** In progress. Current statistical routines are exploratory.

## Scope
- CPM and CLR transformations; Pearson and cross-omics correlation; fold changes; diversity metrics and logistic growth.
- Exploratory two-group Welch unequal-variance testing with Student-t p-values and Benjamini–Hochberg q-values for pre-normalized/log-scale features.
- Added an exploratory NB2 log-link count GLM for raw integer counts, numeric covariates (including caller-encoded batch indicators), size-factor normalization, method-of-moments dispersion, IRLS/Wald tests and BH correction.
- Paired/repeated-measure designs, dispersion moderation, robust compositional methods, pathway analysis and multi-omics integration remain future work.

## Current source
Implemented in `python/molecularis/omics.py`. Inputs are checked for finite values and invalid dimensions.

## Limitations
- Welch tests require independent biological samples and pre-normalized/log-scale input.
- NB2 count GLM and numeric design covariates exist, but dispersion is not moderated; batch indicators must be caller-encoded; repeated-measures inference, robust outlier handling and pathway analysis are absent.
- CPM/CLR alone do not resolve compositional bias or confounding.
- Multiple-testing correction covers only the feature family supplied to the function.

## Exit evidence
Independent synthetic and public reference datasets; null calibration, power, false-discovery and effect-size checks; covariate/design tests; reference-tool concordance; reproducible provenance and performance benchmarks.


### R8 count-model source increment

Added an exploratory NB2 log-link GLM for raw integer counts with condition effect, numeric covariates (including caller-encoded batch dummy variables), median-of-ratios size factors when possible, library-size fallback, per-feature method-of-moments dispersion, IRLS fitting, Wald tests and BH q-values. This is not a DESeq2/edgeR replacement: dispersion is not moderated/shrunk, p-values are asymptotic, repeated measures and robust outlier handling are absent, and the model requires independent samples with a full-rank design. Regression tests execute in the exact-source Python CI suite; see the 2026-11-09 CI #2101 audit record below. Independent simulation/reference calibration is mandatory before validation status.


### Count-aware model increment

An exploratory NB2 log-link GLM now accepts raw integer counts, size factors, numeric covariates and caller-encoded batch indicators. It uses unmoderated per-feature moment dispersion and asymptotic Wald tests with BH correction. It is not DESeq2/edgeR-equivalent and is not validated for small-sample inference, repeated measures or outlier-heavy designs.


### NB2 all-zero feature guard

Features with all-zero raw counts are now retained in the tested family with p=1, neutral effect estimates and an explicit non-estimable warning, rather than attempting an artificial IRLS fit. The all-zero-feature regression test executed in the exact-source Python CI suite (CI #2101). Independent statistical calibration remains outstanding.


### Exact-source automated audit — 2026-11-09 (CI #2101)
- Source commit: `8c4128d5e448db51f2b48fec6c38ce6022fdb053`; [workflow #2101](https://github.com/AssayFlux/Molecularis/actions/runs/42554027490) completed successfully across all five jobs.
- Python CI collected 233 tests: 229 passed, 4 skipped (3 optional RDKit adapter tests because RDKit is not installed in the base Python test environment; 1 optional pysam test because pysam is not installed). The separate pinned RDKit descriptor sanity job passed.
- The suite executed the R3/R4 sequence and research primitive tests, R5 structure/structure-view tests, R6 core chemistry tests, R7 phylogenetics tests, R8 omics tests, R9 catalogue/variant-reference tests and R10 registry/SBOM/configuration checks.
- The pinned host scientific-reference job passed its Michaelis–Menten/SciPy comparison and genetic-code/Biopython comparison steps. These are bounded synthetic/software-reference checks, not independent experimental validation.
- Android ARM64 debug APK/AAB packaging, static package/ELF alignment checks and `:app:testDebugUnitTest` passed. APK: 69,875,151 bytes, SHA-256 `059abb9e3a299b5295b8f08772b976195d7be1cd7db46dce34faa7bcf486d2d9`; AAB: 39,952,539 bytes, SHA-256 `9c8e2ca3a81c4ef2b1fb041aefee99ace5cbfb3292574b815c6a87549210044e`.
- Boundaries: no emulator or physical-device installation/runtime evidence; no Android migration/WorkManager/SAF instrumentation; no end-to-end on-device Chaquopy run; no R5 independent structure concordance, R6 approved-engine chemistry concordance, R7 published tree concordance, R8 null/power/FDR calibration, or R9 authoritative licensed PGx content. R10 security/licence/release gates remain open.


## Host-side NB2 likelihood reference comparison — 2026-11-09

Added `validation/omics_nb2_scipy_reference.py` to compare the exploratory per-feature NB2 GLM against an independent SciPy maximum-likelihood fit on a deterministic raw-count dataset. Both fits use the same explicitly calculated median-of-ratios size factors and fixed per-feature moment dispersion; the SciPy implementation independently optimizes the NB2 log likelihood and computes Fisher-information standard errors/Wald p-values. Coefficient, standard-error and p-value tolerances are recorded, and CI fails closed.

This is a bounded synthetic numerical comparison, not a full DESeq2/edgeR replacement or statistical calibration study. Dispersion moderation, repeated measures, outlier robustness, null/power/FDR calibration, batch designs, real omics datasets and independent biological validation remain open.
