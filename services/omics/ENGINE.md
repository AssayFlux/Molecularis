# Omics Engine
Status: Python v1 engineering implementation; independent scientific review deferred until A–N completion.

## Canonical data model
Feature-by-sample matrices with unique feature and sample identifiers, explicit assay scale (raw_counts, normalized, log_expression, abundance), caller-declared units, finite non-negative values, deterministic canonical JSON and SHA-256 content identity. Matrices are capped at 2,000,000 cells; platform byte and candidate budgets apply.

## Integrated operations
- CPM normalization for raw counts; zero-library samples are rejected.
- Centered-log-ratio (CLR) transformation with explicit positive pseudocount.
- Welch unequal-variance two-group tests for normalized/log-scale data, with Benjamini-Hochberg adjustment.
- Exploratory NB2 log-link GLM differential analysis for integer raw counts, numeric caller-encoded covariates, median-of-ratios size factors where possible, moment dispersions and asymptotic Wald tests.
- Per-sample Shannon entropy and Gini-Simpson diversity.
- Pearson cross-omics feature correlation, requiring identical ordered sample identifiers.
- Existing logistic growth and general statistical primitives remain available as direct library functions.

## Explicit exclusions
No raw FASTQ/BAM/VCF quantification pipeline, transcript quantifier, alignment, batch-correction engine, repeated-measures model, single-cell normalization/trajectory engine, causal multi-omics inference, pathway-enrichment database or clinical interpretation. NB2 is exploratory, not a replacement for fully benchmarked DESeq2/edgeR analysis.

## Acceptance
Canonical round-trip/digest and duplicate-key rejection; matrix shape, identifiers, scale and finite-value checks; CPM, CLR, Welch, NB2, diversity and correlation; scale mismatch rejection; artifact integrity/budgets; full CI and benchmark smoke.
