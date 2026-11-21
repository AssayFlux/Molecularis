# Molecularis Service Roadmap (A–N)

Version: 1.0  
Status: Approved execution order; service implementation has not started merely because this roadmap exists.

## Operating model

The roadmap contains fourteen independently completed service steps. Work proceeds strictly in order, one active service at a time. A later service may be researched, but its implementation does not begin until the previous service is accepted and frozen, unless the repository owner records an explicit sequencing exception in DECISION_LOG.md. Shared Core/MSDE work is allowed only when it unblocks the active step or closes a platform prerequisite.

**Platform gate before A:** establish the minimal Core service contract, MSDE artifact/provenance substrate, versioned schemas, capability registration, runtime lifecycle, resource budgets, and cross-language contract tests. The MSDE architecture is specified; its implementation is not yet complete. Do not start A until the platform gate is demonstrated by executable tests.

## The A–N sequence

| Step | Service | Primary responsibility | Why this position |
|---|---|---|---|
| A | Molecular | Canonical molecular entities, identifiers, bonds, atom/residue models, coordinate/unit conventions and molecular graph primitives | Shared domain foundation |
| B | Sequence | DNA/RNA/protein sequence representation, parsing, normalization, alignment, motifs and annotation | Fundamental linear biological data |
| C | Structure | Molecular/macromolecular structure representation, geometry, topology, coordinate transforms and structural validation | Builds on molecular primitives and sequence mapping |
| D | Chemistry | Chemical graphs, valence, stereochemistry, descriptors, transformations and reaction-level primitives | Supplies chemical correctness to downstream protein/ligand work |
| E | Protein | Protein-specific analysis, representation, embeddings/prediction adapters and structure-related workflows | Uses sequence, structure and chemistry foundations |
| F | Genomics | Reference assemblies, reads, alignments, variants, intervals and population-scale genomic operations | Uses sequence and shared data substrate |
| G | DNA/RNA | Nucleic-acid-specific folding, secondary/tertiary models, design and hybridization workflows | Builds on sequence, structure and molecular primitives |
| H | Simulation | Molecular simulation setup, numerical integration, force/energy interfaces, trajectories and reproducible execution | Requires stable molecular/structure/chemistry models |
| I | Kinetics | Reaction networks, rate laws, parameter estimation, ODE/stochastic kinetics and sensitivity analysis | Uses molecular and simulation foundations |
| J | Omics | Multi-omics data models, normalization, integration, differential and pathway-level analysis | Consumes sequence/genomics/protein and kinetics outputs |
| K | Phylogeny | Evolutionary models, tree inference, comparative analysis and support metrics | Uses sequence and genomics artifacts |
| L | Pharmacogenomics | Variant-to-function/evidence models, pharmacogenomic interpretation and traceable guideline/rule evaluation | Depends on genomics, omics and curated evidence |
| M | Cohorts | Cohort definitions, consent-aware metadata, aggregate analysis and privacy-preserving operations | Consumes validated domain artifacts under governance controls |
| N | Workflows | Cross-service DAGs, orchestration, scheduling, retries, provenance continuity and end-to-end reproducibility | Integrates the completed service portfolio |

Order is a dependency-aware implementation sequence, not a statement that later domains are less important or scientifically subordinate. If evidence requires reordering, record a decision-log entry before changing the sequence.

## Standard step lifecycle (mandatory for every letter)

1. **Discover:** inventory existing code, public imports, tests, schemas, data, dependencies, licenses, benchmarks and external-tool assumptions. Preserve useful work; do not rewrite blindly.
2. **Define:** freeze service scope, non-goals, terminology, scientific questions, input/output contracts, units, coordinate conventions, error model and acceptance thresholds.
3. **Design:** complete ENGINE, RUNTIME and RULEBOOK specifications; identify algorithms, invariants, language boundaries, resource limits and failure modes.
4. **Build:** implement Molecularis-owned algorithms and data structures. External packages may be optional adapters or independent references, never undisclosed mandatory substitutes.
5. **Contract:** publish versioned schemas and capability metadata; integrate with Core/MSDE using stable contracts and immutable artifact identities.
6. **Verify:** unit, property, golden-fixture, regression, integration, independent-reference, reproducibility, security and performance tests as applicable.
7. **Validate scientifically:** document dataset provenance, reference independence, operating range, uncertainty, limitations and evidence level. Software tests alone are insufficient.
8. **Document:** update service docs, API/schema references, examples, dependency/license records, benchmark reports and operational runbooks.
9. **Accept:** review every mandatory gate and unresolved limitation; no silent skips or untested claims.
10. **Freeze:** record completion commit, evidence, supported capability matrix, known limitations and protected paths. Then advance exactly one letter.

## Per-service acceptance gates

A service is not complete until all applicable gates pass:

- Engine: implemented operations, explicit algorithms, invariants, numerical behavior and non-goals.
- Runtime: lifecycle, configuration, isolation, bounded resources, cancellation, errors, observability and reproducibility.
- Rulebook: versioned, testable domain rules with IDs, applicability, rationale, constraints, generation/selection logic and acceptance tests.
- Contracts: versioned input/output/error schemas, units, nullability, precision and compatibility policy.
- Data: provenance, license, checksums, reference versions and immutable artifact lineage.
- Verification: mandatory tests execute in the intended dependency profile; no unexplained skips.
- Scientific evidence: appropriate independent references or benchmark evidence and explicit limitations.
- Integration: Core/MSDE compatibility and provenance-preserving handoff.
- Operations: installation, dependency profile, resource estimates, failure/recovery behavior and diagnostics.
- Freeze: status register and decision log updated, commit and test evidence recorded.

## Service-step work packet

At the start of each letter, create or update a service progress record containing:
- Step letter, service ID, owner and current status.
- Scope, non-goals, dependencies and prerequisite evidence.
- Existing implementation inventory and migration plan.
- Engine/runtime/Rulebook design decisions.
- Public contracts and schema versions.
- Work items with exact paths and acceptance criteria.
- Test matrix and scientific evidence plan.
- Risks, licenses, data governance and rollback plan.
- Completion checklist and freeze record.

## Rules for advancing

- Exactly one service may be in active implementation.
- Do not mark a service complete from a scaffold, registry entry, passing generic CI or successful import alone.
- Do not start the next letter with unresolved critical correctness, provenance, security or data-integrity issues in the current service.
- Preserve compatibility unless a versioned breaking-change plan is approved.
- Reuse shared primitives; do not duplicate domain semantics in Core.
- Record scope/order/dependency changes in DECISION_LOG.md.
- After N, perform system-wide integration, hardening, scale testing and release acceptance before device/deployment commitments.


## Shared Agentics scientific foundation

The scientific foundation is a shared platform prerequisite used by all services, not an additional A–N service and not a reason to create fourteen generic AI wrappers. It provides common contracts for quantities/units, scientific knowledge and evidence, provenance, mathematical/statistical computation, constraints, optimization, construction and independent verification. Each service retains its own domain rules and scientific acceptance thresholds.

During each service's discovery/design packet, map its actual needs to [Scientific Foundation](../services/ai/SCIENTIFIC_FOUNDATION.md) and [Scientific Tool Registry](../services/ai/SCIENTIFIC_TOOL_REGISTRY.md). Integrate only the capabilities needed by the active service, through versioned adapters and tests. Respect the approved service order and freeze gates; no service is scientifically accepted merely because a shared tool is available.
