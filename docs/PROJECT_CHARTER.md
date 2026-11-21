# Molecularis Project Charter

Version: 1.0  
Status: Governing project document  
Branch: CORE

## Mission
Build an independent, modular scientific computing system whose scientific engines, runtimes, data structures, and Rulebooks are owned and maintained by Molecularis.

## Product principles
1. Native-first: core scientific execution must be implemented by Molecularis.
2. Modular: each scientific service has explicit ownership, contracts, tests, data, engine, runtime, and Rulebook.
3. Evidence-led: scientific claims are supported by reproducible tests and documented evidence.
4. Reproducible: inputs, versions, parameters, environment, provenance, and outputs are traceable.
5. Safe by design: resource limits, input validation, secure execution, and failure isolation are built in.
6. Deliberate change: completed services are frozen and changed only through authorization.
7. Device-neutral until system completion: hardware support decisions follow measured system requirements.

## Non-goals
- Building a thin wrapper around another scientific engine and calling it Molecularis-native.
- Treating a directory, API, placeholder, or passing import test as a completed capability.
- Prematurely selecting end-user devices or optimizing for a single deployment target.
- Rewriting existing working code merely to fit a new layout before compatibility and migration plans exist.

## Ownership boundary
Molecularis owns its implementation and integration. Published methods may be independently implemented with attribution and license compliance. External software may be used for literature study, optional interoperability, or independent benchmarking, but must not be a mandatory execution dependency for a capability designated Molecularis-native.

## Success
The total system is complete only when all approved services meet their acceptance criteria, integrate through stable contracts, pass system-level scientific and engineering validation, and have a documented supported operating envelope.
