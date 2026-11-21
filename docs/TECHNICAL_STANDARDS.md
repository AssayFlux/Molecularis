# Technical Standards

## Language policy

Python is the current implementation language and supported reference for Molecularis services, Core/MSDE integration and Agentics orchestration. Do not create C++, Rust or other-language source trees, placeholders, bindings or duplicate implementations as speculative future scaffolding.

An additional language may be introduced only when a concrete, measured requirement cannot be met appropriately in the existing Python architecture. Such a proposal requires an explicit architecture decision, benchmark or capability evidence, maintenance/security/licensing review and a defined interoperability boundary. Until then, Python remains the implementation baseline.

## Interfaces

- Define versioned schemas and contracts at service boundaries.
- Specify units, coordinate conventions, numeric precision, nullability, error codes and determinism.
- Do not expose unstable internal objects as public interfaces.
- Prefer explicit serialization and documented API boundaries.
- Preserve compatibility or provide a versioned migration plan.

## Engineering quality

- Type-check and lint where practical.
- Use deterministic builds and pinned/recorded toolchains.
- Avoid hidden global state.
- Use structured errors and structured logs.
- Make resource ownership and cleanup explicit.
- Validate untrusted inputs and bound memory/CPU/disk consumption.
- Keep dependencies minimal and inventory all direct and transitive dependencies.

## Scientific computing

- State units and coordinate frames explicitly.
- Document numerical precision, tolerances, convergence criteria and random seeds.
- Use stable algorithms and test edge cases.
- Preserve raw inputs and provenance for derived artifacts.
- Never confuse prediction, simulation, heuristic scoring and experimental measurement.

## Scientific computing and Agentics standards

The Agentics scientific foundation is provider-neutral and uses the current Python implementation baseline. Shared contracts must represent quantities, dimensions, units, coordinate/reference systems, precision, uncertainty, assumptions, evidence classes, provenance and explicit error states. Use symbolic/numerical mathematics, statistical analysis, optimization, graph/geometry computation and simulation through narrow adapters with reproducible configurations.

Do not add a broad scientific dependency stack to the core runtime. First audit existing packages and service code; then choose the smallest justified dependency set. Optional domain executables, GPU/HPC solvers, model checkpoints and hosted services require isolated profiles, exact version/license records, resource and egress controls, and independent verification. Additional programming languages are not a roadmap milestone; they require a separate approved decision based on measured need.
