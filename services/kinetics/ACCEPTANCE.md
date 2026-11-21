# Kinetics I — Engineering Acceptance Record

Status: implementation CI-verified in run #44894304968. University scientific review, independent solver comparisons, kinetic benchmark/reference concordance and formal contract freeze are deferred until A–N engineering completion, as directed.

Acceptance scope: canonical reaction network artifact, MSDE lifecycle, mass-action RK4, curve equation capability, exploratory fit capability, executable KIN-001–KIN-006 rules, schemas, tests and benchmark smoke.

Not accepted as validated: stiffness handling, broad kinetic model coverage, experimental parameter accuracy, biochemical mechanism correctness, clinical PK/PD or production isolation.


## Agentics scientific acceptance

- [ ] Kinetic model scope, rate laws, units, assumptions and applicability documented: Chemical kinetics, differential equations, stochastic processes, parameter estimation, sensitivity/identifiability, optimization, probability and uncertainty quantification.
- [ ] Pre-generation checks validate species, reactions, parameters and initial conditions.
- [ ] Reference cases, mass-balance/invariant and numerical convergence tests pass.
- [ ] Parameter estimation records uncertainty, sensitivity and identifiability limits.
- [ ] Solver settings, versions, seeds and lineage are reproducible.
- [ ] Stochastic and deterministic model claims are clearly distinguished.
- [ ] Engineering and scientific acceptance reported separately.

Shared requirements: ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_FOUNDATION.md.
