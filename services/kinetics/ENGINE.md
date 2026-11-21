# Kinetics Engine

Status: Python v1 engineering implementation; independent scientific review deferred until A–N completion.

## Scope and implemented methods

- Canonical reaction-network documents with unique species, non-negative initial concentrations, integer stoichiometry and finite non-negative rate constants.
- Deterministic classical fourth-order Runge–Kutta (RK4) integration of caller-defined mass-action reaction networks.
- Existing Michaelis–Menten and competitive/uncompetitive/noncompetitive/mixed inhibition equations, log-grid least-squares fitting, linearized diagnostic transforms and seeded bootstrap utilities remain available.
- Existing closed-form one-compartment oral PK and Emax PD teaching models remain available as explicitly non-clinical reference primitives.

## Numerical contract

The ODE solver uses fixed step size, requires duration to be an integer multiple of the step, and enforces a caller-visible step ceiling. Trajectory output is downsampled to at most roughly 1,000 intervals plus endpoints. Negative concentrations beyond a small floating-point tolerance and non-finite states fail rather than being silently accepted. Rate-constant dimensions must be consistent with the reaction molecularity and caller-specified units; units are labels, not dimensional inference.

## Exclusions

No stiffness detection/adaptive error control, stochastic simulation, delay equations, spatial reaction-diffusion, automatic parameter fitting for arbitrary networks, thermodynamic feasibility, conservation-law proof, or experimental calibration. PK/PD functions are not dosing or clinical tools. Curve-fit diagnostics are exploratory.

## Acceptance

Canonical round-trip and digest; duplicate-key rejection; invalid stoichiometry rejection; first-order analytic decay concordance; mass conservation on a closed A→B conversion; deterministic artifact lifecycle and Rulebook execution; bounded integration; existing kinetic and PK/PD regression suite.
