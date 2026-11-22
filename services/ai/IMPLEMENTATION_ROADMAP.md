# Agentics Molecularis — Scientific Foundation Implementation Roadmap

**Authority:** Subordinate to [Agentics Molecularis Master Plan](../../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md).  
**Purpose:** Turn the scientific foundation and tool catalog into a sequenced, testable implementation.

## 1. Target modular architecture

The following is a logical package boundary. Preserve current Core/MSDE, artifact, catalog, workflow and A–N service implementations; do not create parallel infrastructure.

```text
python/molecularis/
├── ai.py                         # Existing planner and approval-gated execution
├── bootstrap.py                  # Existing platform bootstrap
└── scientific/
    ├── contracts/                # Typed scientific artifacts and schemas
    ├── knowledge/                # SKE entities, relations, equations, evidence
    ├── units/                    # Quantities, dimensions, conversions
    ├── math/                     # Symbolic and numerical calculation adapters
    ├── statistics/               # Statistical inference and uncertainty
    ├── physics/                  # Physics model and solver adapters
    ├── chemistry/                # Chemistry model and tool adapters
    ├── biology/                  # Biological knowledge and computation adapters
    ├── geometry/                 # Spatial, graph and topology construction
    ├── optimization/              # Constraints, objectives and search
    ├── simulation/               # Simulation contracts and execution adapters
    ├── construction/             # Reconstruction/generalization/exploration
    ├── verification/             # Independent checks and domain Rulebooks
    ├── tools/                    # Registry, manifests and adapter loading
    ├── provenance/               # Bridges to existing artifact lineage
    └── evaluation/               # Benchmarks, uncertainty and regression suites
```

Create these modules incrementally when their contracts and tests are ready. Do not create empty package directories or placeholder modules merely to match this diagram.

## 2. Shared scientific contracts

Define versioned schemas for:
- Scientific objective and constraints.
- Quantity, unit, dimension and coordinate/reference system.
- Scientific concept, entity, relation and domain package.
- Equation/law/mechanism with variables, assumptions and validity domain.
- Evidence/source record and knowledge version.
- Derivation trace and computation record.
- Candidate, objective, constraint result and uncertainty.
- Simulation configuration and result.
- Verification check, threshold, evidence and decision state.
- Tool manifest, environment and resource declaration.
- Claim-to-artifact report mapping.

Contracts must be domain-extensible and must not erase domain-specific semantics.

## 3. Sequential implementation phases

### SF0 — Repository and dependency audit
- Inventory current scientific libraries, wrappers, service registrars and tests.
- Map existing A–N capabilities to the scientific discipline catalog.
- Identify duplicates, unsupported wrappers, version conflicts and license obligations.
- Record actual installed/optional/external status; do not infer it from documentation.
- Freeze a minimal dependency baseline.

**Gate:** evidence-backed inventory and dependency decision record.

### SF1 — Scientific type system and units
- Implement typed quantities, dimensions, unit conversion and validation.
- Define coordinate/reference conventions and numeric precision policy.
- Define scientific artifact envelopes and epistemic/evidence classes.
- Add schema validation, round-trip and invalid-unit tests.

**Gate:** invalid dimensions/units and malformed artifacts are rejected; provenance survives serialization.

### SF2 — Knowledge and evidence substrate
- Implement typed entities, concepts, relations and domain namespaces.
- Represent equations, laws, mechanisms, assumptions and applicability domains.
- Add source/license/provenance records, versioning and contradictory claims.
- Support deterministic query and package loading.
- Integrate with existing artifact store and lineage.

**Gate:** a versioned scientific knowledge package can be ingested, queried, serialized and traced without losing meaning.

### SF3 — Mathematical computation foundation
- Add symbolic expressions and derivation records.
- Add numerical linear algebra, integration, root finding and optimization adapters.
- Add dimensional analysis and unit-aware calculation.
- Record tolerances, precision, convergence and numerical error.
- Test known analytical solutions and failure/ill-conditioning cases.

**Gate:** reproducible calculations with explicit units, tolerances and error behavior.

### SF4 — Statistics and uncertainty
- Add descriptive/inferential statistics, distributions and estimation.
- Add hypothesis testing, regression and multiple-testing controls.
- Add Bayesian methods only with explicit priors/model assumptions.
- Add uncertainty propagation, calibration and sensitivity analysis.
- Add leakage-resistant benchmark and experiment-design contracts.

**Gate:** reference statistical cases reproduce expected results and disclose assumptions/uncertainty.

### SF5 — Physics, chemistry and domain simulation adapters
- Prioritize tools against A–N needs and actual research use cases.
- Implement isolated adapters for selected solvers and packages.
- Validate boundary/initial conditions, units, parameters and supported ranges.
- Preserve input/output files, logs, executable/checkpoint identity and environment.
- Add independent physical/chemical invariants and reference cases.

**Gate:** each enabled adapter passes domain-specific positive, negative, boundary and reproducibility tests.

### SF6 — Construction and optimization
- Implement candidate and construction task contracts.
- Support reconstruction, generalization and bounded exploration.
- Add graph/geometry/sequence-specific construction primitives.
- Define objective functions, hard constraints, search budgets and stopping criteria.
- Keep proposal and verification implementations separate.

**Gate:** at least two distinct domains produce reproducible candidates that pass independent checks appropriate to their declared claims.

### SF7 — A–N integration
- Map each service to shared contracts and its own domain package.
- Preserve service-owned equations, rules, thresholds and acceptance criteria.
- Add cross-service artifact handoff and provenance continuity.
- Exercise real, typed workflows across multiple services.

**Gate:** every service demonstrates its supported lifecycle; cross-service handoffs preserve meaning and lineage.

### SF8 — Learning and model governance
- Implement approved data-source registry and ingestion policy.
- Add dataset manifests, licenses, deduplication and leakage checks.
- Establish baseline model evaluations before any fine-tuning.
- Add model registry, reproducible training manifests, regression tests and rollback.
- Treat retrieval/knowledge updates separately from model-weight updates.

**Gate:** an update is reproducible, permission-cleared, benchmarked and reversible.

### SF9 — Agentics orchestration
- Connect intent interpretation and planner to typed scientific knowledge and tool manifests.
- Build pre-generation auditor and post-generation independent verification coordinator.
- Bind approval to plan, inputs, tool versions, data egress and resource envelope.
- Generate artifact-grounded reports with explicit evidence classes.
- Add adversarial and out-of-domain evaluations.

**Gate:** every scientific workflow is auditable, policy-controlled and evaluated; unsupported claims fail the curated suite.

## 4. Initial priority by scientific return

1. Units, dimensions, typed quantities and reference systems.
2. Numerical and symbolic mathematics.
3. Statistics, uncertainty and experimental design.
4. Knowledge/evidence/provenance representation.
5. Constraint solving and optimization.
6. Graph, geometry and topology primitives.
7. Selected physics and chemistry simulation adapters.
8. Domain-specific A–N integration.
9. Model training and specialized AI.
10. Controlled discovery capabilities.

## 5. Dependency and tool adoption rules

- Scientific tool selection is driven by an identified service requirement and measurable gap.
- Avoid multiple libraries with overlapping responsibilities unless interoperability or performance requires them.
- Optional scientific engines belong in extras or isolated execution environments.
- GPU/HPC and licensed checkpoints require separate deployment and legal review.
- No dependency is added solely because it is popular or appears in this catalog.
- Pin and test versions; record SBOM/license data and security advisories.
- External engine failure must be explicit; do not silently substitute a method with different scientific semantics.

## 6. Required phase report

Every phase report must list exact files, implementation status, dependencies and licenses reviewed, tests and exact results, CI commit/run, benchmark evidence, scientific limitations, unresolved risks and gate state. A planned adapter is not an integrated adapter; an integrated adapter is not a validated scientific method.


## Alignment with the governing P0–P7 plan

This document is a subordinate implementation breakdown, not a second roadmap. The [Agentics Molecularis Master Plan](../../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md) v2.1 controls phase order and acceptance.

- **SF0** is the first repository/dependency audit task inside governing **P0**; P0 also includes cross-service integration, threat modelling, isolation, failure handling and artifact recovery.
- **SF1–SF2** implement the core of governing **P1** (typed scientific contracts and the Scientific Knowledge Engine).
- **SF3–SF5** provide mathematical, statistical and domain-computation foundations that support governing **P1/P2**.
- **SF6** maps to governing **P2** (shared construction, constraints, optimization and evaluation).
- **SF7** maps to governing **P3** (A–N integration).
- **SF8** maps to governing **P5** (permission-aware data/model governance).
- **SF9** maps to governing **P4** (Agentics orchestration); it must not jump ahead of P0–P3.

The implementation baseline is Python. Do not create speculative C++, Rust or other-language packages. Candidate scientific tools remain optional until the audit proves a need and license/version/security/verification requirements are satisfied.


## Implementation status — 2026-11-22

### SF1 — Scientific type system and units: engineering complete

Implemented in `python/molecularis/knowledge.py`:
- Canonical SI dimension algebra, finite typed quantities and quantity JSON round-trip serialization.
- Built-in base/common units, safe compound-unit parsing, conversion and incompatible-dimension rejection.
- Coordinate reference metadata.
- Versioned scientific package serialization and JSON Schema contracts.
- Positive/negative unit and round-trip tests.

### SF2 — Knowledge and evidence substrate: engineering complete

Implemented in `python/molecularis/knowledge.py` and integrated with Core ArtifactStore:
- Concepts, entities, relations and domain namespaces.
- Equation and law records with typed variables, assumptions, applicability and source references; ordered mechanism steps with typed entity and evidence references.
- Evidence classes/statuses, uncertainty, source/license/permission metadata and explicit contradiction links.
- Immutable package identity/version and deterministic query interfaces.
- ArtifactStore persistence, caller-supplied parent lineage and verified artifact loading.
- A–N domain ownership map.

**Verification:** GitHub Actions [run #45045807328](https://github.com/AssayFlux/Molecularis/actions/runs/45045807328), tested commit `819eb1fff6785fa49530ab5bf8b30e5280111712`: 769 passed, 12 skipped, 0 failed; schema validation, Ruff, compilation, benchmark smoke tests and optional Chemistry/Genomics/Sequence profiles passed.

**Boundary:** SF1–SF2 establish a knowledge representation substrate, not a symbolic math engine, general reasoning system, comprehensive ontology, scientific truth oracle or trained model. P2 has now implemented reference-level SF3 (symbolic/numerical mathematics), SF4 (statistics and uncertainty), and SF6 (constraints, optimization and construction contracts); see the P2 implementation record below. SF5 domain solver adapters, SF7 A–N integration, SF8 learning/model governance and SF9 Agentics orchestration remain future work. P0 platform safety/integration/recovery gates remain open and must be addressed before progression into P3/P4 or model training.


## P2 implementation record — shared reasoning and construction

**Implementation branch:** agentics/p2-reasoning-construction

Implemented in python/molecularis/reasoning.py and exported from python/molecularis/__init__.py:

- Safe arithmetic expression AST; no Python eval/exec, function calls, attribute access, indexing or arbitrary code execution.
- Deterministic derivation trace construction with explicit variables, assumptions, source references and P1 SI-dimension inference.
- Bisection root solver with bracket checks, finite values, tolerance, iteration budget, residual and termination state.
- Descriptive statistics, Pearson correlation, seeded percentile bootstrap, first-order independent uncertainty propagation, deterministic-seed Monte Carlo, local sensitivity and binary probability calibration.
- Hard/soft constraints, weighted multi-objective bounded grid search, deterministic enumeration and explicit no-feasible/budget-exhausted states.
- Reconstruction/generalization/exploration task contracts, bounded candidate contracts and pre-publication constraint audit.
- Versioned contract schema at services/ai/schemas/scientific-reasoning-v1.schema.json.
- Two contract-level proposer/verifier fixtures: sequence alphabet checking and chemical-formula element-count consistency.

**Scientific boundary:** the expression language is intentionally small and is not a general CAS; bisection requires a continuous function with a sign-changing bracket; grid search is for bounded low-dimensional reference problems and does not guarantee a global optimum beyond enumerated grid points; uncertainty routines rely on stated independence/distribution/local-linearity assumptions; calibration metrics require representative labelled binary outcomes. The two domain fixtures establish engineering separation only, not physical/chemical validity or experimental confirmation.

**Gate state: ENGINEERING PASSED.** GitHub Actions [run #45047445495](https://github.com/AssayFlux/Molecularis/actions/runs/45047445495) on tested commit `b55efdaaae8e276c17c22b272fec94b0131f316e`: 788 passed, 12 skipped, 0 failed; 67 JSON schemas validated; Ruff, compilation, benchmark smoke tests and Chemistry/Genomics/Sequence optional profiles passed. P0 remains open; this P2 implementation does not certify platform isolation, full cross-service integration, recovery or production readiness.
