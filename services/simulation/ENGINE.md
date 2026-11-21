# Simulation Engine — H

Status: Python v1 engineering implementation.

Owns immutable simulation-protocol artifacts, force-field/input provenance, bounded orchestration and descriptive energy evidence. Consumes upstream Structure/Protein/Chemistry artifacts by digest; does not silently regenerate coordinates, bonds or ligand parameters.

Native Molecularis logic: strict NVT/NPT protocol contract; temperature, pressure, timestep, integration/equilibration steps, replicas, seed and reporting interval; canonical JSON and SHA-256 protocol identity; descriptive energy-series statistics and least-squares slope; MSDE artifact ingest/load integrity and lineage; three Rulebook capabilities.

Existing GROMACS adapter: explicit local executable and TPR SHA-256 pins, caller-declared force-field provenance, fresh output directory, fixed mdrun argv, bounded timeout/bytes and hashed output files.

Existing OpenMM adapter: trusted caller-constructed OpenMM System/Topology/positions, CPU NVT/NPT, independent replicas and derived random seeds, trajectory hash and engine build provenance. Direct API; untrusted artifact data is never deserialized into executable OpenMM objects.

Protocol validation checks contract consistency, not force-field correctness or thermodynamic suitability. Energy summaries do not infer equilibration, stability, ensemble convergence or physical validity. GROMACS TPR and force-field provenance are caller-supplied; TPR is not independently decoded. OpenMM is optional and requires local MD extra.

Exclusions: native force-field parameterization, ligand/protein preparation, protonation, solvent/ion placement, topology generation, minimization, enhanced sampling, free-energy calculation, alchemical transformations, reaction dynamics, GPU scheduler, distributed replicas, trajectory decoding and experimental validation.


## Shared Agentics scientific foundation

Participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. Priority disciplines: Numerical analysis, linear algebra, ODE/PDE solvers, classical/analytical mechanics, statistical mechanics, thermodynamics, stochastic processes, HPC and numerical error.

Use shared quantities, units, reference systems, uncertainty and provenance contracts while retaining simulation-specific numerical methods and physical models. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
