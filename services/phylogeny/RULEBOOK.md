# Phylogeny Rulebook K

Rulebook ID: phylogeny-core-v1 · Version: 1.0.0

| Rule | Requirement | Rationale / acceptance |
|---|---|---|
| PHY-001 | Taxon IDs are unique, bounded and non-empty; 3–500 taxa | Prevent ambiguous leaf identity; invalid IDs rejected |
| PHY-002 | Input is a rectangular, equal-length DNA-IUPAC alignment | Pairwise columns must be homologous; unequal lengths/symbols rejected |
| PHY-003 | Artifact schema, canonical digest and metadata agree | Detect corruption and schema confusion |
| PHY-004 | JC distances use only unambiguous A/C/G/T pairs; minimum sites required; saturated p >= 0.75 fails | Make missing-data and model domain explicit |
| PHY-005 | NJ rejects materially negative inferred limbs and reports an arbitrary computational root | Avoid silent branch-length clipping and false rooting |
| PHY-006 | UPGMA output is explicitly conditional on ultrametric/constant-rate assumption | Prevent unsupported clock interpretation |
| PHY-007 | Bootstrap seed, requested/successful/failed replicates and conditional denominator are reported | Reproducible support and visible failure accounting |

Only rules listed for the selected operation are emitted as rules_checked. These are operation applicability declarations backed by the corresponding runtime validation path; they are not independent scientific approval.

## Exceptions
Saturated or insufficient pairwise comparisons, malformed artifacts, and invalid trees fail. No substitution imputation is performed. Pairwise deletion means distances can be based on different site counts, which are included in distance-matrix output.

## Exclusions
No likelihood/Bayesian model selection, molecular clock dating, recombination, codon evolution, gene-tree/species-tree reconciliation, ancestral sequence reconstruction or clinical/functional interpretation.


## Agentics scientific rules

- Apply the universal lifecycle under phylogenetic domain authority.
- Pre-audit alignment quality, taxa, sampling, model assumptions, missing data and evidence provenance.
- Declare likelihood/Bayesian assumptions, priors, substitution/rate models and model-selection criteria.
- Independently assess convergence, support metrics, sensitivity and alternative topologies where feasible.
- Preserve uncertainty and avoid treating a single inferred tree as established evolutionary history.
- Record dataset, alignment, model, software, seed and lineage versions.

Priority disciplines: Evolutionary biology, probability, likelihood/Bayesian inference, graph/tree algorithms, statistical models, sampling, model selection and uncertainty.
See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
