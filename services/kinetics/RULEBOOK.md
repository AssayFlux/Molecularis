# Kinetics Rulebook — kinetics-core-v1

Rules are executable contract checks; they do not constitute independent scientific validation.

- **KIN-001 — Identity:** network identifier is non-empty and bounded; species names are unique and bounded.
- **KIN-002 — State:** initial concentrations are finite and non-negative and align exactly with the species vector.
- **KIN-003 — Stoichiometry:** every reaction has non-empty reactant and product mappings, known species, integer coefficients 1–8 and finite non-negative rate constants.
- **KIN-004 — Canonical provenance:** artifact JSON is canonical, duplicate keys are rejected, and SHA-256 plus catalog metadata are verified on load.
- **KIN-005 — Numerical budget:** duration and step size are finite positive values, duration is an integer multiple of step size, and integration steps respect the caller/platform budget.
- **KIN-006 — Numerical state:** non-finite outputs or materially negative concentrations fail; tiny negative round-off is clamped to zero and reported by the solver's numerical contract.

Mass-action rates use (v_j=k_j\prod_i [X_i]^{\nu_{ij}}). Stoichiometric updates apply reactant consumption and product formation. Dimensional consistency is the caller's responsibility. The fixed-step RK4 approximation has no adaptive error estimate or stiffness handling.


## Agentics scientific rules

- Apply the universal lifecycle under kinetic domain authority.
- Pre-audit reaction network, rate laws, units, assumptions, initial conditions, parameter provenance and solver applicability.
- Distinguish deterministic rate equations, stochastic reaction models and empirical fitted relationships.
- Independently verify mass balance, invariants, limiting cases, parameter identifiability and numerical convergence where applicable.
- Record uncertainty, sensitivity, confidence/interval assumptions and model limitations.
- Preserve source, solver, parameter and artifact provenance.

Priority disciplines: Chemical kinetics, differential equations, stochastic processes, parameter estimation, sensitivity/identifiability, optimization, probability and uncertainty quantification.
See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
