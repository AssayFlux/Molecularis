# Agentics Molecularis — Scientific Tool Registry

**Purpose:** Catalog candidate computational tools and define how they may be integrated. This is not an installation manifest and does not imply that every listed tool is currently present, licensed, configured or validated.

## 1. Integration policy

1. Reuse existing Molecularis implementations before adding a dependency.
2. Prefer small, composable libraries for foundational computation.
3. Treat external executables, GPU models, datasets and commercial services as separately provisioned capabilities.
4. Verify the exact version, license, model/data terms, platform support and transitive dependencies before adoption.
5. Keep optional tools optional; a missing optional engine must produce an explicit capability-unavailable result, never a fake success.
6. Wrap every integrated tool in a Molecularis adapter with typed schemas, unit conventions, resource budgets, provenance and error mapping.
7. Do not import all scientific packages into the core AI runtime. Use extras, environment profiles or isolated workers where appropriate.
8. CI must use deterministic fixtures/mocks; live network, huge datasets and GPU hardware are not default test dependencies.

## 2. Foundational mathematics and numerical computation

| Capability | Candidate tools | Integration purpose |
|---|---|---|
| Array and matrix computing | NumPy | Core arrays, linear algebra and vectorized computation |
| Scientific algorithms | SciPy | Optimization, interpolation, integration, signal processing and statistics |
| Symbolic mathematics | SymPy | Algebra, symbolic differentiation/integration, equation manipulation |
| Units and dimensions | Pint; Astropy units where appropriate | Unit-safe quantities and dimensional analysis |
| Automatic differentiation | JAX; PyTorch autograd | Gradients and differentiable scientific models |
| ODE/PDE solvers | SciPy integrate; SUNDIALS; PETSc; Firedrake where justified | Differential-equation and multiphysics solving |
| Sparse linear algebra | SciPy sparse; PETSc | Large sparse systems |
| Geometry | Shapely; CGAL bindings where justified | Geometric operations and spatial validation |
| Graphs | NetworkX; igraph | Scientific networks and graph algorithms |
| Formal logic/constraints | Z3; SymPy logic | Constraint checks and formal reasoning |
| Optimization | CVXPY; CasADi; SciPy optimize; OR-Tools | Convex, nonlinear, symbolic and combinatorial optimization |

## 3. Statistics, uncertainty and data analysis

| Capability | Candidate tools | Integration purpose |
|---|---|---|
| Tabular data | pandas; Polars | Data ingestion and transformation |
| Classical statistics | statsmodels; SciPy stats | Regression, inference and diagnostics |
| Machine learning | scikit-learn | Classical predictive and preprocessing methods |
| Bayesian inference | PyMC; Stan | Bayesian models and posterior inference |
| Probabilistic programming | NumPyro; Pyro | Probabilistic models and inference |
| Survival analysis | lifelines | Time-to-event analysis |
| Causal inference | DoWhy; EconML (when justified) | Explicit causal estimands and sensitivity |
| Experimental design | statsmodels and specialist DoE libraries | Power, design and analysis |
| Visualization | Matplotlib; Plotly; Altair | Diagnostic and scientific plots |
| Large-scale analytics | DuckDB; Apache Arrow | Local analytical queries and columnar interchange |

## 4. Machine learning and scientific AI

| Capability | Candidate tools | Integration purpose |
|---|---|---|
| Deep learning | PyTorch | Model training and inference |
| Accelerated array computing | JAX | Differentiable and accelerator-based computation |
| Model interoperability | ONNX Runtime | Portable inference where supported |
| Model/dataset tracking | MLflow; DVC | Versioned experiments and data lineage |
| Model evaluation | scikit-learn metrics; domain benchmark harnesses | Reproducible evaluation and regression |
| Graph learning | PyTorch Geometric; DGL | Graph neural models when scientifically justified |
| Scientific ML | DeepXDE; NVIDIA Modulus (license/platform review required) | Physics-informed and operator-learning research |
| Hyperparameter optimization | Optuna | Reproducible search and experiment tracking |

LLM frameworks are orchestration aids only. They do not replace the Scientific Knowledge Engine, deterministic calculation or independent scientific verification.

## 5. Physics, chemistry and materials

| Domain | Candidate tools | Integration purpose |
|---|---|---|
| Molecular dynamics | OpenMM; GROMACS; LAMMPS | Molecular and particle simulation |
| Quantum chemistry | Psi4; PySCF; NWChem | Electronic-structure calculations |
| Atomistic simulation | ASE | Unified atomistic workflow interface |
| Chemistry representations | RDKit; Open Babel | Molecular graphs, descriptors and format conversion |
| Quantum simulation | QuTiP | Quantum dynamics and open quantum systems |
| Finite element | FEniCSx; deal.II | PDE and continuum simulation |
| Multiphysics | MOOSE; OpenFOAM | Coupled physics and computational fluid dynamics |
| Materials workflows | AiiDA; pymatgen | Materials representations and provenance-aware workflows |
| Crystal structures | spglib; gemmi | Symmetry, crystallography and structure files |
| Thermodynamic property packages | CoolProp; domain-specific validated packages | Thermophysical properties within declared ranges |

## 6. Biology and Molecularis domain tools

| Domain | Candidate tools | Integration purpose |
|---|---|---|
| Sequence and annotation | Biopython; Biotite | Sequence parsing and biological data |
| Alignment | Parasail; MAFFT | Pairwise and multiple sequence alignment |
| Genomics | pysam; HTSlib; samtools; bcftools | BAM/CRAM/VCF/BCF operations |
| Protein models | ESM family; AlphaFold ecosystem | Optional sequence/structure predictions; exact checkpoint and license review |
| Structure validation | MolProbity | Domain validation of macromolecular structures |
| Molecular visualization | Mol* | Interactive structural inspection |
| DNA/RNA design | NUPACK; NUAD | Nucleic-acid analysis/design within model scope |
| Phylogenetics | IQ-TREE; MAFFT; scikit-bio | Evolutionary inference and sequence analysis |
| Single-cell/omics | Scanpy; AnnData; Bioconductor ecosystem | Omics representations and analysis |
| Workflow interoperability | Galaxy | External workflow integration with explicit data governance |

Existing Molecularis adapters and service implementations take precedence over creating duplicate wrappers.

## 7. Knowledge, data and reproducibility infrastructure

Candidate components include:
- JSON Schema or equivalent typed contracts for artifact validation.
- SQLite/PostgreSQL for transactional metadata and catalog records.
- Graph storage or typed graph packages when query needs justify them.
- Object/artifact storage with immutable content hashes.
- DVC or equivalent for dataset snapshots where appropriate.
- MLflow or equivalent for model experiment lineage.
- AiiDA or domain workflow systems for specialized scientific provenance.
- Standard scientific formats and parsers with checksums and versioned schemas.

Do not add a second artifact store or workflow executor where Molecularis Core already provides the capability.

## 8. Tool adapter contract

Every adapter must declare:
- Stable capability ID, domain, purpose and supported scientific claims.
- Tool name, exact version, executable/package identity and environment.
- License, data/checkpoint terms and attribution obligations.
- Input/output schemas, units, coordinate/reference conventions and format versions.
- Required and optional dependencies, hardware and resource envelope.
- Network/egress behavior and data disclosure requirements.
- Determinism, random seed support and reproducibility limitations.
- Failure modes, timeout/cancellation behavior and error mapping.
- Provenance fields, logs and output artifact types.
- Independent verification strategy and known limitations.
- Positive, negative, boundary and out-of-domain tests.

## 9. Adoption tiers

- **Tier 0 — Existing native capability:** already implemented in Molecularis; inspect and reuse.
- **Tier 1 — Foundational dependency:** small, broadly useful library adopted after compatibility and license review.
- **Tier 2 — Optional scientific adapter:** domain package or executable installed only in the relevant environment.
- **Tier 3 — Specialized infrastructure:** GPU/HPC, distributed solver, large external engine or institution-managed service; separate deployment and operational review.
- **Tier 4 — Research candidate:** experimental, unvalidated or license/maintenance uncertain; never treated as production authority.

## 10. Initial recommended baseline

Subject to repository dependency audit and license review, prioritize a modest foundational layer:
- NumPy, SciPy, SymPy, Pint.
- pandas or Polars (avoid duplicate use without a measured need).
- statsmodels and scikit-learn.
- NetworkX.
- PyTorch or JAX only where model/differentiable computation is needed; do not require both by default.
- CVXPY or SciPy optimization interfaces according to problem type.
- Matplotlib for reproducible diagnostics.

All other tools remain optional domain adapters. Exact versions, Python compatibility and licenses must be checked before changing dependency manifests.
