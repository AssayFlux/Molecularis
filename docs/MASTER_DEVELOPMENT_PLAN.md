# Molecularis Master Development Plan

Version: 1.0  
Status: Living plan; changes require a recorded decision.

## Delivery strategy
Build the platform substrate, then complete one service vertical slice at a time. A vertical slice includes specification, engine, runtime, Rulebook, data contracts, validation, tests, integration, documentation, and freeze review. Do not start implementation of the next service until the current service's exit gate is passed, except for explicitly authorized shared-Core work.

## Phase 0 — Repository and governance baseline
- Confirm CORE branch and protect the direct-commit workflow.
- Inventory existing source, tests, schemas, data, dependencies, licenses, assets, and CI.
- Record known failing checks and baseline test results.
- Establish document ownership, decision log, service register, and change-control procedure.
- Keep existing implementations intact while migration is designed.

Exit: repository inventory and baseline are reproducible; governance documents are authoritative.

## Phase 1 — Core substrate
- Stable service identity and discovery contract.
- Versioned request, response, error, and artifact envelopes.
- Configuration and capability metadata.
- Provenance and run identity.
- Logging, diagnostics, and status model.
- Runtime plugin boundary without mandatory third-party scientific engines.
- Cross-language ABI/process boundary strategy for C++, Python, and Rust.
- Minimal test harness and CI gates.

Exit: a minimal example service can be discovered, configured, invoked, validated, and reported through Core.

## Phase 2 — Native molecular foundations
Recommended initial service order:
1. Molecular — shared molecular entities, identifiers, units, coordinate and graph foundations.
2. Sequence — sequence objects, parsing, transformations, alignment and translation.
3. Structure — coordinate models, geometry, topology and structural validation.
4. Chemistry — chemical graphs, stereochemistry, properties and transformations.
5. Protein — protein-specific representation, analysis, design and prediction foundations.
6. Genomics — genome, read, variant and annotation models and algorithms.
7. DNA/RNA — nucleic-acid structure, interaction and design methods.
8. Simulation — physical models, numerical integration and simulation runtime.
9. Kinetics — reaction networks, kinetics and pharmacokinetic/pharmacodynamic models.
10. Omics — expression and multi-omics data models and analyses.
11. Phylogeny — evolutionary models and tree inference.
12. Pharmacogenomics — genotype-to-guideline and response modeling.
13. Cohorts — population and virtual cohort models.
14. Workflows — cross-service orchestration and external workflow interoperability.

This order is provisional. Before each service starts, verify actual dependency edges and adjust only through a recorded architecture decision. Work on one service at a time.

## Phase 3 — Cross-service integration
- Integrate only completed, versioned service contracts.
- Define artifact handoff and scientifically valid conversions.
- Add end-to-end workflows and provenance continuity.
- Add deterministic replay and failure recovery.
- Avoid circular dependencies.

Exit: representative end-to-end workflows pass with complete provenance.

## Phase 4 — System hardening
- Security threat model and execution isolation.
- Resource accounting and limits.
- Performance and numerical stability.
- Reproducibility across supported environments.
- Backup, recovery, and operational diagnostics.
- Full regression and scientific reference validation.

Exit: system-level acceptance matrix passes.

## Phase 5 — Device and deployment decisions
Only after system completion, measure CPU, memory, GPU, storage, OS, and accelerator requirements. Define supported device profiles from evidence. Do not guess or promise compatibility in advance.

## Work-in-progress limits
- One active scientific service at a time.
- Shared-Core tasks only when they unblock that service.
- No speculative parallel service scaffolding beyond approved templates.
- Every task must have an owner, scope, acceptance criteria, affected paths, and verification plan.

## Completion rule
A service is not complete until its engine, runtime, Rulebook, data contracts, tests, scientific evidence, documentation, integration and freeze record are all accepted.
