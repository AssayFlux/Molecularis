# Cohorts Runtime M

Status: implemented v1 Python reference runtime on MSDE.

## Lifecycle
Construct and validate immutable CohortDocument values; serialize deterministic UTF-8 JSON; ingest into the MSDE artifact store with schema/media type, SHA-256 metadata and optional parent lineage; load only after artifact type, size, digest, metadata and candidate-budget checks; execute registered capabilities through the existing in-process Rulebook runtime.

## Capabilities
- `cohorts.validate.v1`: one cohort artifact.
- `cohorts.summary.v1`: one cohort artifact.
- `cohorts.stratify.v1`: one cohort artifact and `field` parameter.
- `cohorts.overlap.v1`: two cohort artifacts sharing a documented pseudonym namespace.

All capabilities are deterministic. `minimum_cell_size` defaults to 5 and is bounded to 2–1000. The runtime returns aggregate JSON reports and does not export member rows.

## Resource and error behavior
Input size is bounded by MSDE Budget; records are capped at 100,000 members, 1,000,000 visits and 128 attributes/measurement fields per record. Invalid schemas, duplicate keys/IDs, invalid timepoints, unsupported classifications and integrity mismatches fail closed. Resource budget violations raise ResourceLimitError. Execution is in-process and is not an OS sandbox.

## Reproducibility and shutdown
Canonical sorted-key JSON and stable iteration order make artifacts and reports deterministic. No background workers, external executables, network access or persistent service process are required.
