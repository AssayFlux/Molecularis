# Molecularis Work Backlog

Mark an item complete only with a commit SHA and verification evidence. Service A implementation is explicitly authorized; the Core/MSDE platform acceptance gate remains open and must not be reported as passed.

## P0 — Trustworthy baseline

- [x] Baseline CI repaired. Evidence: run #127.
- [x] Implement local MSDE reference slice. Evidence: commits 5b39b44 and ccae6c1; run #130.
- [x] Add optional scientific dependency profiles for sequence, genomics and chemistry. Evidence: all three profile jobs passed in run #133.
- [x] Repair malformed legacy JSON schema and pass repository-wide JSON Schema validation. Evidence: run #135.
- [ ] Audit Python modules, public imports, tests and service ownership.
- [ ] Audit dependencies, licenses, data provenance, model/runtime assumptions and security.
- [ ] Expand Ruff beyond E9/F; introduce targeted strict typing.
- [ ] Establish reproducibility, scientific reference and performance baselines.

## P1 — Core/MSDE platform

- [x] Typed platform budgets, capability and execution-context contracts.
- [x] Local service lifecycle and JSON capability manifest loader.
- [x] SHA-256 immutable blob store, SQLite catalog, lineage and atomic publication.
- [x] Bounded streaming, digest verification and non-destructive integrity audit.
- [x] Exact scalar and numeric range metadata lookup.
- [x] Capability registry and acyclic Rulebook DAG execution.
- [x] Successful and failed Rulebook run evidence.
- [x] Input artifact lineage on derived operation outputs.
- [x] Snapshot-bound exact/range query pagination with explicit completeness.
- [x] CI jobs for optional scientific dependency profiles.
- [ ] Native sorted-segment index manager, manifest snapshots and compaction, or a benchmark-backed formal decision to retain SQLite indexes.
- [ ] Crash-boundary fault injection, catalog backup/restore and corruption-recovery matrix.
- [ ] Typed query plan, deterministic cost model and bounded scan fallback.
- [ ] Preconditions/postconditions, typed Rulebook input/output validation, retry policies and independent-validator gates.
- [ ] Cross-process service discovery and language-neutral request/response runtime.
- [ ] C++/Python/Rust conformance suite and executable cross-language reference service.
- [ ] Threat model, sandboxing and operational resource-isolation controls.

## P2 — Scientific service sequence

Execute exactly one letter at a time, following [SERVICE_ROADMAP.md](SERVICE_ROADMAP.md).

- [ ] A — Molecular (v1 engineering implementation complete; run #150 green with 608 passed/12 skipped and 1k/10k benchmark smoke; independent scientific approval and formal freeze pending)
- [ ] B — Sequence
- [ ] C — Structure
- [ ] D — Chemistry
- [ ] E — Protein
- [ ] F — Genomics
- [ ] G — DNA/RNA
- [ ] H — Simulation
- [ ] I — Kinetics
- [ ] J — Omics
- [ ] K — Phylogeny
- [ ] L — Pharmacogenomics
- [ ] M — Cohorts
- [ ] N — Workflows

Each letter requires discovery/audit, Engine, Runtime, Rulebook, schemas/contracts, implementation, integration, mandatory tests, independent scientific evidence, documentation, acceptance and freeze.

## P3 — System integration and release

- [ ] Cross-service workflows and provenance continuity.
- [ ] Deterministic replay, dependency invalidation and failure recovery.
- [ ] Security, resource limits, backup/restore and supply-chain governance.
- [ ] System-scale performance and scientific acceptance report.
- [ ] Complete resolved release SBOM and license evidence.
- [ ] Device/deployment assessment based on measured requirements.

## Active task

A's v1 engineering implementation and CI verification are complete. Obtain independent scientific approval for MOL-001–MOL-010 and fixture provenance, record the decision, then freeze A. Continue the open Core/MSDE hardening gates; do not advance to B until A is accepted.
