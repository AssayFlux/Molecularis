# Cohorts Acceptance M

Engineering acceptance is distinct from independent scientific, privacy or regulatory validation.

- Canonical deterministic JSON round-trips and hashes consistently.
- Duplicate identifiers/keys, malformed visits, non-finite values and unsupported classifications fail closed.
- MSDE ingestion/load verifies artifact type, digest, metadata and resource budgets.
- Aggregate summary reconciles members, visits, missingness and measurements.
- Stratification and overlap suppress cells/intersections below the configured minimum.
- Registry, schemas, compilation, tests and benchmark smoke pass in CI.

University review, privacy threat modeling and formal contract freeze remain deferred until A–N engineering completion. No patient data, clinical decisions or privacy guarantees are supported by this v1.
