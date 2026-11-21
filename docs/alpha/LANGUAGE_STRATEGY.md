# Alpha Language Strategy

C++, Rust and Python are Molecularis' preferred core languages. TypeScript/JavaScript remains necessary for the browser/PWA experience.

| Language | Ownership |
|---|---|
| C++17+ | Measured performance-critical numerical kernels, molecular geometry and native scientific library integration. |
| Rust | Safe parsers, format validation, local-node supervisor, worker lifecycle, capability enforcement and resource controls. |
| Python | Scientific orchestration, research APIs, reference implementations, workflow composition and ecosystem adapters. |
| TypeScript/JavaScript | Responsive web/PWA, browser state, visualization, offline shell and accessible UI. |
| SQL | Persistence and schema migrations. |

Use versioned JSON contracts for process boundaries. Use a stable C ABI for native libraries where appropriate. PyO3/maturin or pybind11 are options only when they reduce maintenance and have pinned ABI/toolchain support. Do not expose C++ exceptions, Rust panics or Python exceptions across boundaries. Define structured errors, cancellation and resource limits.

C++ and Rust implementations require profiling, safety, upstream compatibility or deployment justification. Python remains the default scientific composition and reference layer. Canonical semantics belong in schemas and rulebooks, not duplicated language-specific definitions.

Build expectations: CMake and sanitizers for C++; Cargo.lock, clippy and rustfmt for Rust; pyproject, pinned dependencies, Ruff, mypy and pytest for Python; strict TypeScript, lockfiles and browser tests for the web client. CI must test cross-language contracts.