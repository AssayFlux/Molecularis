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
