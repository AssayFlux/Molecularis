# Phylogeny Engine K

Status: implemented as a Molecularis-native Python v1 distance-based engine; independent scientific validation deferred until A–N engineering is complete.

## Canonical input
PhylogenyDocument stores 3–500 uniquely named, caller-aligned homologous nucleotide sequences, DNA-IUPAC symbols, alignment method label and deterministic SHA-256 identity. Alignment is an upstream Sequence workflow responsibility. Equal aligned lengths and bounded total cells are mandatory.

## Operations
- Strict canonical artifact validation and MSDE lifecycle.
- Pairwise Jukes–Cantor 1969 distances using pairwise deletion of gaps and ambiguous bases; minimum comparable sites are explicit.
- Neighbor joining (unrooted topology; deterministic tie-breaking; negative inferred limbs rejected).
- UPGMA (rooted ultrametric construction; molecular-clock assumption stated).
- Seeded nonparametric alignment-site bootstrap for NJ split support, bounded to 1,000 service replicates and exposing failed replicate counts.

Existing python/molecularis/phylo.py algorithms (Newick parse/serialize, leaf extraction, patristic distances, UPGMA, NJ and bootstrap) are retained and wired into the artifact service.

## Numerical and scientific boundaries
Jukes–Cantor assumes equal nucleotide frequencies and equal substitution rates; it is not a general substitution model. Pairwise deletion can make pairwise estimates use different site sets. Saturation at p >= 0.75 and insufficient comparable sites fail explicitly. NJ is not inherently rooted; its emitted Newick root is computational/arbitrary. UPGMA is valid as a dated-clock-like interpretation only under ultrametric/constant-rate assumptions. Bootstrap support is conditional on successfully reconstructed replicates and is not a posterior probability.

No native aligner, maximum-likelihood or Bayesian inference, codon model, recombination detection, gene-tree/species-tree reconciliation, ancestral reconstruction or calibrated divergence dating is claimed.


## Shared Agentics scientific foundation

Participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. Priority disciplines: Evolutionary biology, probability, likelihood/Bayesian inference, graph/tree algorithms, statistical models, sampling, model selection and uncertainty.

Use shared probability, statistics, uncertainty, evidence and provenance contracts while retaining evolutionary model semantics and validators. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
