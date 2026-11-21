# Test and CI Strategy

## Test pyramid
- Fast: formatting, lint, type checks, schema checks, unit tests.
- Service: service-level integration, data round-trips, runtime lifecycle and error paths.
- Scientific: reference fixtures, numerical tolerances, property tests and reproducibility.
- System: cross-service workflows, artifact provenance, cancellation and recovery.
- Performance: throughput, memory, scaling and accelerator tests when applicable.

## CI requirements
- Run on every CORE commit.
- Install from declared project metadata in a clean environment.
- Validate package build and imports.
- Run registry/schema/document consistency checks.
- Run unit and integration suites.
- Report skipped optional-tool tests explicitly.
- Separate pre-existing failures from regressions introduced by a change.
- Do not mark a job green by silently skipping required tests.

## Test data
Keep fixtures small, deterministic, licensed, checksummed and documented. Large data and model weights require a separate governed artifact strategy; do not commit them casually.

## Release gate
No service freeze while required CI checks fail, required scientific fixtures are missing, or known high-severity correctness defects remain unresolved.


## Agentics scientific and model evaluation

AI/scientific tests must cover pre-generation rejection, schema and unit validation, source/version/provenance integrity, independent post-generation checks, uncertainty reporting, adversarial/untrusted-content handling, resource enforcement, tool-unavailable behavior and failure/cancellation semantics. Numerical tests record tolerances, convergence, precision, random seeds and hardware sensitivity.

Model changes require fixed leakage-resistant evaluation sets, baseline comparison, regression thresholds, reproducible training/inference manifests and rollback evidence. Keep deterministic fixtures in ordinary CI; heavyweight datasets, GPUs and external engines use explicit optional/institutional test profiles. Report engineering CI, model benchmark results and scientific validation separately.
