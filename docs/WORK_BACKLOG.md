# Molecularis Work Backlog

This is the ordered engineering queue. Mark an item complete only with a commit SHA and verification evidence.

## P0 — Establish a trustworthy baseline
- [ ] Re-run current CI on CORE and inspect every failure.
- [ ] Run package build, import tests, registry/schema checks and full available Python tests.
- [ ] Record baseline failures and classify them as existing defects or environment limitations.
- [ ] Inventory existing Python modules, tests, public imports and service ownership.
- [ ] Audit dependencies, licenses, assets, data provenance and model/runtime assumptions.
- [ ] Reconcile architecture and registry metadata with actual repository contents.

## P1 — Core substrate
- [ ] Specify service identity and discovery.
- [ ] Specify versioned request/response/error envelopes.
- [ ] Specify artifact identity, units, metadata and provenance.
- [ ] Specify configuration and capability metadata.
- [ ] Specify cross-language boundary for C++/Python/Rust.
- [ ] Implement minimal service lifecycle and runtime contract.
- [ ] Add a reference example service and contract tests.
- [ ] Establish Core acceptance gate.

## P2 — First service: molecular
- [ ] Research and scope molecular entities, identifiers, graphs, coordinates and units.
- [ ] Define ENGINE, RUNTIME and RULEBOOK acceptance criteria.
- [ ] Define schemas and stable service API.
- [ ] Implement native data structures and algorithms.
- [ ] Implement native runtime integration.
- [ ] Implement and test Rulebook constraints.
- [ ] Add scientific reference fixtures and independent comparisons.
- [ ] Integrate with Core.
- [ ] Complete review, documentation, freeze and protected-path record.

## P3 — Subsequent services
Follow docs/MASTER_DEVELOPMENT_PLAN.md. Do not start a later service until its prerequisites and current service exit gate are verified.

## P4 — System completion
- [ ] Cross-service integration and end-to-end workflows.
- [ ] System security, resource limits, recovery and reproducibility.
- [ ] Performance and scaling evidence.
- [ ] Total-system acceptance report.
- [ ] Device/deployment capability assessment based on measured requirements.
