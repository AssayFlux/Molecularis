# Chemistry Runtime D — v1

Status: implemented reference runtime.

The service registers deterministic versioned capabilities with the shared MSDE platform. Ingestion publishes immutable canonical JSON artifacts with source and canonical hashes, metadata and optional parent lineage. Loads verify media type, schema, byte budget, artifact digest and metadata.

Limits: SDF input 16 MiB; 100,000 explicit atoms; 200,000 bonds; fingerprint path length at most 6 with configurable feature and traversal ceilings; substructure matching has a configurable state ceiling. The shared execution context enforces the artifact byte budget.

Errors are explicit validation or resource-limit failures. No network calls, implicit external process execution or automatic fallback to RDKit occur. Current handlers are trusted in-process Python; OS sandboxing, preemptive cancellation and GPU isolation remain Core-level future work.
