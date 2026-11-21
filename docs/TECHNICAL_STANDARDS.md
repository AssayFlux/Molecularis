# Technical Standards

## Language policy
Primary languages are C++, Python, and Rust. Other languages are allowed only with a written justification covering capability gap, maintenance cost, interoperability, security, licensing, and long-term support.

## Language boundaries
- C++: performance-sensitive numerical kernels, geometry, simulation and data-intensive algorithms when benchmarks justify it.
- Rust: memory-safe systems components, runtime services, concurrency, parsers and resource management.
- Python: orchestration, scientific interfaces, research-facing APIs and developer workflows.
These are defaults, not mandates. Avoid implementing the same algorithm multiple times without a measurable reason.

## Interfaces
- Define language-neutral contracts at service boundaries.
- Version schemas and public APIs.
- Specify units, coordinate conventions, numeric precision, nullability, error codes and determinism.
- Do not expose unstable internal structs as public interfaces.
- Prefer explicit serialization or a documented ABI/process boundary.

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

The Agentics scientific foundation is language- and provider-neutral. Shared contracts must represent quantities, dimensions, units, coordinate/reference systems, precision, uncertainty, assumptions, evidence classes, provenance and explicit error states. Use symbolic/numerical mathematics, statistical analysis, optimization, graph/geometry computation and simulation through narrow adapters with reproducible configurations.

Do not add a broad scientific dependency stack to the core runtime. First audit existing packages and service code; then choose the smallest justified dependency set. Optional domain executables, GPU/HPC solvers, model checkpoints and hosted services require isolated profiles, exact version/license records, resource and egress controls, and independent verification. Any language or package choice must follow the existing language policy and measured need.
