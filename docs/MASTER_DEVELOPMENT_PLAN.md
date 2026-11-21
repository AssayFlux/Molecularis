# Molecularis Master Development Plan

Version: 1.1. Status: living plan; changes require a recorded decision.

## Delivery strategy
Build shared platform foundations before scientific services, then complete one service vertical slice at a time. A vertical slice includes specification, engine, runtime, Rulebook, data contracts, validation, tests, integration, docs and freeze.

## Phase 0 — Repository and governance baseline
Confirm CORE branch, inventory source/tests/schemas/data/dependencies/licenses/assets/CI, record baseline failures and establish change control. Exit: reproducible repository inventory and baseline.

## Phase 1 — Core substrate and MSDE
- Stable service identity/discovery and versioned request/response/error envelopes.
- Artifact identity, schemas, provenance and run identity.
- MSDE local object store, catalog, journal recovery, bounded streaming, exact and range indexes, query planner and evidence ledger.
- Cross-language contracts for C++, Python and Rust.
- Minimal service lifecycle and contract tests.
Exit: a service can discover, query, transform, validate and publish artifacts with provenance and bounded resources.

## Phase 2 — Native molecular foundations
Recommended order: Molecular, Sequence, Structure, Chemistry, Protein, Genomics, DNA/RNA, Simulation, Kinetics, Omics, Phylogeny, Pharmacogenomics, Cohorts, Workflows. Record dependency changes in DECISION_LOG.

## Phase 3 — Cross-service integration
Versioned contracts, scientifically valid artifact handoff, provenance continuity, deterministic replay and failure recovery.

## Phase 4 — System hardening
Security, resource limits, numerical stability, reproducibility, backup/recovery, diagnostics, regression and scientific reference validation.

## Phase 5 — Device and deployment decisions
Only after total-system completion, measure CPU, memory, GPU, storage, OS and accelerator requirements.

## Work-in-progress limits
One active scientific service at a time. Shared-Core/MSDE tasks only when they unblock the platform. Every task has scope, acceptance criteria, affected paths and verification plan.

## Completion rule
A service is complete only when engine, runtime, Rulebook, data contracts, tests, scientific evidence, docs, integration and freeze record are accepted.
