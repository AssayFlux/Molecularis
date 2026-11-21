# Molecularis AI acceptance

## Implemented engineering checks
- Model-agnostic planner callable contract.
- Live capability catalog.
- Strict Workflow v1 parsing and DAG validation.
- Exact external input declaration.
- Persisted plan artifacts and parent lineage.
- Explicit approval gate.
- Execution through existing Molecularis workflow/runtime.
- Rejection tests for invalid capability, malformed provenance and unapproved execution.

## Still required
- Provider adapter with deployment-managed credentials.
- A–N all-service bootstrap acceptance on supported Python versions.
- Real scientific cross-service artifact contract and handoff tests.
- Prompt-injection and adversarial model-output testing.
- Timeout, cancellation, concurrency, isolation and recovery tests.
- Human-readable scientific report generation with evidence citations.
- University scientific validation.
