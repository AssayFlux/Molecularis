# Service implementation template

Copy this structure for a new service:
- ENGINE.md — scientific scope, algorithms, APIs, invariants, and acceptance criteria.
- RUNTIME.md — runtime architecture, lifecycle, resource needs, execution model, and failure handling.
- RULEBOOK.md — formal rules, constraints, construction procedures, and validation requirements.
- service.yaml — machine-readable identity, status, languages, contracts, and ownership.
- src/cpp, src/python, src/rust — native implementation roots; use only languages justified by the design.
- tests — unit, integration, regression, and scientific-reference tests.
- schemas — versioned input/output contracts.
- data — service-owned reference data and fixtures, with provenance and licenses.
- benchmarks — reproducible performance and numerical benchmarks.

Do not mark a service complete until the completion checklist in MASTER_ENGINEERING_RULEBOOK.md is satisfied.
