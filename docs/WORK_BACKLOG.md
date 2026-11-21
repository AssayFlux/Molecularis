# Molecularis Work Backlog

Mark an item complete only with a commit SHA and verification evidence.

## P0 — Trustworthy baseline
- [ ] Re-run current CI on CORE and inspect every failure.
- [ ] Run package build, import tests, registry/schema checks and full available Python tests.
- [ ] Record baseline failures and classify them.
- [ ] Inventory existing Python modules, tests, public imports and service ownership.
- [ ] Audit dependencies, licenses, assets, data provenance and model/runtime assumptions.
- [ ] Reconcile architecture and registry metadata with actual repository contents.

## P1 — Core substrate
- [ ] Specify service identity/discovery, versioned envelopes, artifact identity, units and provenance.
- [ ] Specify C++/Python/Rust boundaries and implement minimal service lifecycle.
- [ ] Add reference service and contract tests.

## P1A — Molecularis Scientific Data Engine (MSDE)
- [x] Establish architecture, runtime, Rulebook and staged implementation specification.
- [x] Define initial artifact-manifest and query-request schemas.
- [ ] Review threat model, storage consistency and schema evolution.
- [ ] Implement immutable content-addressed artifact store and catalog.
- [ ] Implement journal recovery and bounded streaming I/O.
- [ ] Implement exact-key and ordered range indexes.
- [ ] Implement query executor, planner and completeness semantics.
- [ ] Implement evidence ledger and Rulebook DAG execution gates.
- [ ] Add domain adapters after service-specific acceptance fixtures exist.
- [ ] Benchmark scale, memory, throughput, recovery and correctness.
- [ ] Evaluate AI-assisted planning behind strict policy and verification gates.

## P2 — First scientific service: molecular
- [ ] Define entities, identifiers, graphs, coordinates and units.
- [ ] Define ENGINE, RUNTIME and RULEBOOK acceptance criteria.
- [ ] Implement native structures, algorithms, runtime and validation.
- [ ] Add scientific fixtures, integration and freeze record.

## P3 — Subsequent services
Follow docs/MASTER_DEVELOPMENT_PLAN.md. Do not start another service until prerequisites and current exit gate pass.

## P4 — System completion
- [ ] Cross-service workflows and provenance continuity.
- [ ] Security, resource limits, recovery and reproducibility.
- [ ] Performance/scaling evidence and total-system acceptance.
- [ ] Device/deployment assessment based on measured requirements.
