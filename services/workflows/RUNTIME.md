# Workflows Runtime N

Status: implemented v1 on the local MSDE reference runtime.

Construct a canonical WorkflowDocument; ingest/load it as an immutable MSDE artifact with schema, SHA-256 metadata and optional parent lineage; validate against the active ServiceRegistry; convert it to a Rulebook; execute with RulebookExecutor and ExecutionContext/Budget; retrieve operation values and run records from the caller runtime.

Limits: 100 operations, 256 declared inputs, 256 input keys per operation and 64 KiB canonical JSON parameters per operation, plus shared MSDE budgets. External input keys must be declared and supplied exactly.

Unknown capabilities, malformed contracts, missing inputs, cycles, invalid parameters, exceeded budgets and unbound handlers fail closed. Core records failure status and completed output artifacts. Runtime is in-process, not an OS sandbox. Secrets must be injected into connectors, never persisted in workflow documents. Galaxy outputs are untrusted and require explicit validation before downstream use.
