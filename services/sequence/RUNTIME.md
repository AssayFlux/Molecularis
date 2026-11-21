# Sequence Runtime

Status: Python v1 reference runtime integrated with MSDE; independent review and freeze pending.

## Lifecycle

1. Construct and validate a SequenceDocument.
2. Ingest canonical JSON bytes as an immutable MSDE artifact.
3. Resolve a capability from the service registry.
4. Execute the matching sequence-core-v1 Rulebook with exactly one sequence artifact ID.
5. Verify media type, schema, content digest and identity metadata before execution.
6. Persist the operation report and run evidence through the shared Rulebook executor.
7. Close the platform through the shared Core lifecycle.

## Resource and failure semantics

The runtime inherits MSDE Budget limits for input/output bytes, candidates, results and wall time. The artifact store performs bounded streaming and digest verification. Sequence-specific parsers expose record/base/feature/cell limits; callers must pass explicit ceilings for large data. Invalid schema, alphabets, artifact identity, operation parameters or resource exhaustion fail closed. Failed Rulebook executions are recorded by Core. Native v1 capabilities do not fetch network data, invoke a shell or call an external scientific engine.

## Determinism and provenance

Canonical sequence bytes and SHA-256 are stable for identical normalized records. Capability and Rulebook versions are explicit. Run evidence includes input artifact lineage, capability, Rulebook, parameters and elapsed time through MSDE. Optional backends must record package/version and scoring/algorithm settings in their own result.

## Language boundaries

Python is the implemented reference runtime. C++ and Rust are future targets only; no binding, ABI or cross-language conformance is claimed. Core remains responsible for artifact identity, lifecycle and execution evidence.


## Agentics scientific execution requirements

AI-proposed operations enter through registered, typed capabilities. Validate schemas, units/dimensions, reference conventions, assumptions, resource budgets and domain limits before execution. Preserve tool/algorithm versions, parameters, environment, seeds where relevant, source artifacts, logs and output lineage. Enforce cancellation, timeout and explicit unavailable/failure states; do not silently substitute a different method. AI output is untrusted input and cannot bypass service policy. See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
