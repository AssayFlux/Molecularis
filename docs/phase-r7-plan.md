# R7 — Phylogenetics

**Status:** In progress. Distance-tree methods are exploratory.

## Scope
- Newick parsing, quoted labels, leaf listing and patristic distances.
- UPGMA and neighbour-joining from validated distance matrices.
- Added Jukes–Cantor 1969 distance estimation with pairwise deletion, minimum comparable sites and saturation rejection; alignment-to-distance neighbour-joining entry point.
- Added deterministic site-column bootstrap split support for Jukes–Cantor + neighbour-joining, reporting requested/successful/failed replicate counts.
- Maximum-likelihood/Bayesian inference, tree search and interactive offline viewers remain future work.

## Current source
Implemented in `python/molecularis/phylo.py`. Non-finite/negative input distances and negative inferred neighbour-joining limbs are rejected rather than silently clipped.

## Limitations
- UPGMA assumes an ultrametric clock-like distance structure.
- Neighbour joining is distance-based and does not infer a substitution model.
- Bootstrap is distance-based and limited to the implemented JC69 + neighbour-joining path; it is not likelihood/Bayesian support. No tree viewer or model selection.

## Exit evidence
Published reference matrices/trees, independent topology and branch-length concordance, tie/degenerate cases, large-tree performance, provenance and offline visualization tests.


### R7 model-based distance increment

Added Jukes–Cantor 1969 nucleotide distance estimation with pairwise deletion of ambiguous/gap columns, minimum comparable-site requirements and explicit saturation rejection. Added a neighbour-joining-from-alignment entry point that constructs a model-corrected distance matrix before tree inference. This is a simple substitution model, not maximum likelihood or Bayesian inference; it has no rate heterogeneity, codon model, bootstrap or model selection. Regression tests execute in the exact-source Python CI suite; see the 2026-11-09 CI #2101 audit record below.


### Model-corrected nucleotide distances

Jukes–Cantor 1969 distances with pairwise deletion and saturation rejection now feed neighbour joining from aligned DNA sequences. This is a simple distance correction, not maximum-likelihood/Bayesian inference, rate heterogeneity, model selection or bootstrap support.

### Nonparametric site-bootstrap increment

Added deterministic, seeded alignment-column resampling for Jukes-Cantor + neighbour-joining split support. Reports requested, successful and failed replicate counts and computes support only over successful trees; invalid/saturated/negative-limb replicates are not silently repaired. This remains an exploratory distance-bootstrap utility, not maximum-likelihood/Bayesian inference. Independent published-reference concordance remains required; regression execution is now confirmed by CI #2101.


### Exact-source automated audit — 2026-11-09 (CI #2101)
- Source commit: `8c4128d5e448db51f2b48fec6c38ce6022fdb053`; [workflow #2101](https://github.com/AssayFlux/Molecularis/actions/runs/42554027490) completed successfully across all five jobs.
- Python CI collected 233 tests: 229 passed, 4 skipped (3 optional RDKit adapter tests because RDKit is not installed in the base Python test environment; 1 optional pysam test because pysam is not installed). The separate pinned RDKit descriptor sanity job passed.
- The suite executed the R3/R4 sequence and research primitive tests, R5 structure/structure-view tests, R6 core chemistry tests, R7 phylogenetics tests, R8 omics tests, R9 catalogue/variant-reference tests and R10 registry/SBOM/configuration checks.
- The pinned host scientific-reference job passed its Michaelis–Menten/SciPy comparison and genetic-code/Biopython comparison steps. These are bounded synthetic/software-reference checks, not independent experimental validation.
- Android ARM64 debug APK/AAB packaging, static package/ELF alignment checks and `:app:testDebugUnitTest` passed. APK: 69,875,151 bytes, SHA-256 `059abb9e3a299b5295b8f08772b976195d7be1cd7db46dce34faa7bcf486d2d9`; AAB: 39,952,539 bytes, SHA-256 `9c8e2ca3a81c4ef2b1fb041aefee99ace5cbfb3292574b815c6a87549210044e`.
- Boundaries: no emulator or physical-device installation/runtime evidence; no Android migration/WorkManager/SAF instrumentation; no end-to-end on-device Chaquopy run; no R5 independent structure concordance, R6 approved-engine chemistry concordance, R7 published tree concordance, R8 null/power/FDR calibration, or R9 authoritative licensed PGx content. R10 security/licence/release gates remain open.


## Host-side neighbour-joining reference comparison — 2026-11-09

Added `validation/phylo_biopython_reference.py` to compare the local neighbour-joining implementation against Biopython 1.88's independent `DistanceTreeConstructor.nj` on a deterministic additive four-taxon distance matrix with unequal terminal branches. The harness compares all six patristic pair distances with a 1e-8 tolerance, asserts leaf identity and fails CI if any comparison differs.

This is synthetic algorithm/software concordance, not a published phylogeny or biological evolutionary validation. It does not validate sequence search, maximum-likelihood/Bayesian inference, model selection, rate heterogeneity, real alignment uncertainty, large-tree scaling, viewers or node security.


### Neighbour-joining degenerate-input regression increment — 2026-11-09

Added deterministic regression cases for the two-taxon base case, exact pair-distance preservation, asymmetric/non-zero-diagonal rejection and deterministic tie handling on an equidistant four-taxon matrix. These tests harden matrix edge handling but do not replace the outstanding published-tree/topology reference corpus or large-tree performance study.
