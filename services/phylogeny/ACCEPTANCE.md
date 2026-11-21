# Phylogeny Acceptance K

Engineering acceptance: implementation and CI verification are required before marking the service complete. University scientific review and independent reference concordance are deferred until A–N engineering completion, as directed.

Required engineering evidence:
- Canonical document validation, serialization, duplicate-key rejection, digest and artifact metadata checks.
- Distance matrix, JC saturation/insufficient-site rejection, NJ, UPGMA, Newick output and deterministic seeded bootstrap.
- Resource bounds, capability registration, Rulebook execution and operation-specific rule reporting.
- Repository-wide schemas (55), registry, compilation, Ruff E9/F, all test profiles and phylogeny benchmark smoke passed.

Scientific limitations remain explicit: the supported distance model is JC69 only; no alignment, likelihood/Bayesian inference, model selection, molecular clock calibration or independent concordance is supplied. CI success is engineering evidence, not scientific accuracy certification.


## Agentics scientific acceptance

- [ ] Taxon/sample, alignment, model assumptions and applicability documented: Evolutionary biology, probability, likelihood/Bayesian inference, graph/tree algorithms, statistical models, sampling, model selection and uncertainty.
- [ ] Pre-generation checks cover alignment quality, missingness and provenance.
- [ ] Statistical model, priors/parameters and selection criteria are explicit.
- [ ] Independent convergence, support, sensitivity and alternative-model checks exist.
- [ ] Uncertainty and limitations are reported; inference is not mislabeled as observation.
- [ ] Data, alignment, software, model and seed provenance retained.
- [ ] Engineering and scientific acceptance reported separately.

Shared requirements: ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_FOUNDATION.md.
