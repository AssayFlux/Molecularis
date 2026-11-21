# Molecularis — North Star

**Status:** Owner-directed all-device product direction, updated 2026-11-21. This direction applies to branch Alpha.

## Mission

Build Molecularis as an all-device scientific research platform for phone, tablet, laptop, desktop and workstation. The primary experience is a responsive web application/PWA. Optional desktop packaging and secure local, hosted and institutional compute connectors provide device-appropriate execution.

Molecularis is not an Android project. Android/Kotlin is legacy implementation context and may be retained temporarily for migration, data compatibility or scientific logic extraction, but it is not the future product foundation.

## Preferred engineering languages

The owner's preferred core languages are C++, Rust and Python. C++ owns measured performance-critical scientific kernels. Rust owns safe parsers, validation, secure native services, resource controls and local-node supervision. Python owns scientific orchestration, research APIs, reference implementations and ecosystem adapters. TypeScript/JavaScript remains necessary for browser/PWA presentation and visualization. SQL and declarative schemas support persistence and contracts. Additional runtimes require a concrete need and recorded decision.

## Product principles

- All-device, responsive and accessible.
- Offline-capable where technically appropriate, with clear sync/conflict status.
- Compute-location transparent: users know where data and jobs run.
- Contract-first, modular and versioned.
- Evidence before claims; preserve provenance, uncertainty and limitations.
- Privacy, security and licensing by design.
- Research-use only; no clinical decision support without separate authorization and validation.

## Non-goals

- Android-only product roadmap.
- Browser execution of arbitrary native code.
- Unrestricted shell or arbitrary code execution in API processes.
- Blind copying of entire upstream platforms.
- Treating code availability as proof of model, dataset or redistribution rights.
- Clinical diagnosis, treatment or dosing recommendations under the current scope.
