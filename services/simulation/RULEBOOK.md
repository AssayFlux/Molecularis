# Simulation Rulebook — H

Rulebook ID: simulation-core-v1; version 1.0.0. Engineering contract; independent scientific review deferred until A–N implementation completes.

| Rule | Constraint | Acceptance |
|---|---|---|
| SIM-001 | Protocol names exactly one supported engine (OpenMM or GROMACS) and ensemble (NVT/NPT). | Unknown values reject. |
| SIM-002 | Coordinates, topology and parameter-source identities are lowercase SHA-256; force-field name/version are explicit. | Missing or malformed provenance rejects. |
| SIM-003 | Temperature and timestep are finite, positive and bounded; timestep ≤4 fs; steps and replicas have hard ceilings. | Non-finite, bool-as-number and out-of-range values reject. |
| SIM-004 | NPT requires positive pressure; NVT must not specify pressure. | Ensemble/pressure contradictions reject. |
| SIM-005 | Canonical JSON is strict, duplicate-key rejecting and content-addressed; MSDE metadata must match. | Round-trip and tamper tests. |
| SIM-006 | GROMACS runs only hash-pinned executable and TPR with caller-supplied force-field manifest, fixed argv and bounded resources. | Hash mismatch, unsafe extra args, missing outputs and failed process reject. |
| SIM-007 | Energy analysis is descriptive only and accepts finite bounded samples. | Deterministic statistics; no equilibrium or stability claim. |

Capabilities: simulation.validate.v1, simulation.energy-analysis.v1 and simulation.gromacs-run.v1. Direct OpenMM adapter uses trusted object inputs and is not invoked through JSON artifact deserialization. Every report names the source protocol digest and limitations. Breaking schema or scientific semantics requires a new version and fixtures.


## Agentics scientific rules

- Apply the universal lifecycle within simulation domain authority.
- Pre-audit governing equations, assumptions, dimensions, initial/boundary conditions, parameter ranges and solver suitability.
- Record discretization, precision, tolerances, convergence and stability analysis; numerical convergence is not proof that the physical model is correct.
- Independently check conservation laws, invariants, reference cases and sensitivity where applicable.
- Distinguish simulated outcomes from observations and experimentally validated claims.
- Preserve full configuration, seeds, environment, solver version, uncertainty and provenance.

Priority disciplines: Numerical analysis, linear algebra, ODE/PDE solvers, classical/analytical mechanics, statistical mechanics, thermodynamics, stochastic processes, HPC and numerical error.
See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
