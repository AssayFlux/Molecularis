# Molecularis Work Backlog

Mark an item complete only with a commit SHA and verification evidence. Do not start service A until the Core/MSDE platform gate passes.

## P0 — Trustworthy baseline

- [x] Baseline CI repaired. Evidence: run #127.
- [x] Implement local MSDE reference slice. Evidence: commits 5b39b44 and ccae6c1; run #130.
- [ ] Add dedicated optional-dependency CI profiles for RDKit, Biopython, Biotite, Parasail and pysam.
- [ ] Add schema validation and package build/import coverage.
- [ ] Audit Python modules, public imports, tests and service ownership.
- [ ] Audit dependencies, licenses, data provenance, model/runtime assumptions and security.
- [ ] Expand Ruff beyond E9/F; introduce targeted strict typing.
- [ ] Establish reproducibility, scientific reference and performance baselines.

## P1 — Finish Core/MSDE platform gate

- [x] Typed platform budgets, capability and execution-context contracts.
- [x] Local service lifecycle and JSON capability manifest loader.
- [x] SHA-256 immutable blob store, SQLite catalog, lineage and atomic publication.
- [x] Bounded streaming, digest verification and non-destructive integrity audit.
- [x] Exact scalar and numeric range metadata lookup.
- [x] Capability registry and acyclic Rulebook DAG execution.
- [x] Successful run evidence ledger.
- [ ] Failed/partial run evidence and input artifact lineage.
- [ ] Snapshot-bound pagination, typed query plan and deterministic planner.
- [ ] Native sorted-segment indexes, compaction and differential benchmarks.
- [ ] Crash-boundary fault injection, backup/restore and corruption-recovery matrix.
- [ ] Full JSON schema validation in CI and compatibility policy tests.
- [ ] Cross-process service discovery and language-neutral request/response runtime.
- [ ] C++/Python/Rust conformance suite and executable cross-language reference service.
- [ ] Threat model, sandboxing and operational resource-isolation controls.

## P2 — Scientific service sequence

Execute exactly one letter at a time, following [SERVICE_ROADMAP.md](SERVICE_ROADMAP.md).

- [ ] A — Molecular
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

Continue Phase 1 Core/MSDE platform gate. See [SERVICE_STATUS.md](SERVICE_STATUS.md) for evidence and next exact work.
