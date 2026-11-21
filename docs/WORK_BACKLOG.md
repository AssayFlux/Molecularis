# Molecularis Work Backlog

Mark an item complete only with a commit SHA and verification evidence. Priority order follows the Master Development Plan. Do not start service A until the Core/MSDE platform gate passes.

## P0 — Maintain trustworthy baseline

- [x] Resolve the previously failing baseline CI gates. Evidence: CORE commit a6b5840836a94029acb9a94819b84f6c209ffde5; run #127.
- [ ] Add dedicated optional-dependency CI profiles so RDKit, Biopython, Biotite, Parasail and pysam tests execute rather than skip.
- [ ] Add package build/import checks and schema validation coverage.
- [ ] Inventory Python modules, public imports, tests and service ownership.
- [ ] Audit dependencies, licenses, data provenance, model/runtime assumptions and security.
- [ ] Progressively expand Ruff beyond the current E9/F baseline; add type checking where practical.
- [ ] Establish coverage, reproducibility, scientific reference and performance baselines.

## P1 — Core and MSDE platform gate

- [ ] Specify and implement service identity/discovery and versioned request/response/error envelopes.
- [ ] Define artifact/run identity, schema evolution, units and provenance contracts.
- [ ] Review MSDE threat model, storage consistency, crash recovery and schema evolution.
- [ ] Implement immutable content-addressed artifact store and catalog.
- [ ] Implement journal recovery, atomic publication and bounded streaming I/O.
- [ ] Implement exact-key and ordered/range indexes.
- [ ] Implement query executor/planner, snapshots, budgets and completeness semantics.
- [ ] Implement evidence ledger and generic Rulebook DAG execution gates.
- [ ] Add cross-language contract tests and executable reference service.
- [ ] Benchmark correctness, throughput, memory, storage growth and recovery.

**Platform exit:** executable reference service discovers, ingests, queries, transforms, validates and publishes immutable artifacts with provenance under bounded budgets.

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

Each letter requires discovery/audit, Engine, Runtime, Rulebook, schemas/contracts, implementation, integration, mandatory tests, independent scientific evidence, documentation, acceptance and freeze. No next letter until accepted.

## P3 — System integration and release

- [ ] Cross-service workflows and provenance continuity.
- [ ] Deterministic replay, dependency invalidation and failure recovery.
- [ ] Security, resource limits, backup/restore and supply-chain governance.
- [ ] System-scale performance and scientific acceptance report.
- [ ] Release SBOM with resolved artifacts, hashes, native binaries and license evidence.
- [ ] Device/deployment assessment based on measured requirements.

## Active task

Phase 1 Core/MSDE platform gate. See [SERVICE_STATUS.md](SERVICE_STATUS.md) for the verified baseline and next exact task.
