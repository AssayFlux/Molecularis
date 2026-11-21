# Simulation Runtime — H

Start MolecularisPlatform, register_simulation_service, ingest SimulationDocument and execute a Rulebook. Protocol artifacts are compact canonical JSON and immutable MSDE records. Loads verify schema, media type, content digest and metadata. Reports preserve source protocol digest and artifact lineage.

The GROMACS capability requires a protocol artifact with explicit local executable and TPR paths and lowercase SHA-256 pins, plus output_directory in Rulebook parameters. It invokes only fixed mdrun argv; arbitrary arguments and shell execution are disabled. Configured timeout is capped by platform wall-time budget; TPR and total outputs are capped by byte budget. Executable and paths are privileged operator configuration, not untrusted multi-tenant inputs.

OpenMM is invoked through run_openmm_dynamics with already constructed trusted OpenMM objects. The MSDE JSON protocol is not an object serializer. The adapter enforces CPU execution, replica/step/frame/atom limits and finite coordinates/energies. It returns DCD bytes encoded in a result envelope.

The local reference runtime is in-process. Its wall-time budget cannot preempt arbitrary Python handlers or guarantee OS-level isolation. Production execution requires a dedicated sandboxed worker with filesystem allow-lists, CPU/memory limits, process-group cancellation, scratch quotas and explicit artifact publication. External engine failures surface as runtime errors.


## Agentics scientific execution requirements

Validate model definition, units, coordinate frames, initial/boundary conditions, solver configuration, stability constraints and resource budgets before execution. Record solver/tool versions, parameters, precision, tolerances, random seeds, hardware/environment, logs and trajectory lineage. Bound CPU/GPU/memory/time and fail explicitly on solver or dependency failure. See ../ai/AI_CONSTITUTION.md.
