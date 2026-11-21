# Molecularis — North Star

**Status:** Owner-directed product direction, updated 2026-11-21. This direction applies to Alpha and is to be integrated into CORE through reviewed PRs.

## Mission

Build Molecularis as a **desktop-first, cross-platform scientific research application** for Linux, Microsoft Windows and macOS, with a coherent native-app experience on Android and Apple mobile devices (iOS/iPadOS). The primary deliverable is an installed application—not a website. The desktop application is the first product target; mobile applications follow on the same domain model, contracts, design system and scientific capabilities. A web interface may be added later as a companion or institutional access surface, but it is not the first product or the architectural centre.

Molecularis helps researchers create, inspect, execute, compare and reproduce scientific workflows across personal computers, mobile devices, local compute nodes and institutionally governed compute. It remains research-use only unless separate evidence, owner authorization and applicable legal/regulatory clearance establish otherwise.

## Product principles

- Desktop first: Linux, Windows and macOS are first-class targets.
- Mobile next: Android and iOS/iPadOS are first-class application targets, not browser-only fallbacks.
- One coherent product: shared domain logic, scientific contracts, project formats, provenance and design system; platform-specific adapters only where required.
- Offline-capable and local-first where technically appropriate, with explicit sync, backup and conflict semantics.
- Compute-location transparent: users know where files and jobs run.
- Contract-first, modular, versioned and reproducible.
- Evidence before claims; preserve provenance, uncertainty and limitations.
- Privacy, security, accessibility and licensing by design.
- No assumption that a web stack or PWA is the primary product runtime.

## Preferred engineering languages

The owner's preferred core languages are C++, Rust and Python.
- C++ owns measured performance-critical scientific kernels and mature native scientific-library interfaces.
- Rust owns safe parsers, validation, secure native services, cross-platform process supervision and resource controls.
- Python owns scientific orchestration, research APIs, reference implementations and ecosystem adapters.
- UI technology must be selected through a desktop-first cross-platform feasibility spike covering Linux, Windows, macOS, Android and iOS/iPadOS. Prefer a solution that keeps C++, Rust and Python as the scientific/core languages and avoids duplicating product logic. Do not silently assume React/PWA or select a framework without evaluating accessibility, native integration, packaging, update/signing, GPU/3D visualization, offline storage, mobile lifecycle and licensing.
- SQL and declarative schemas support persistence and contracts. Additional runtimes require a concrete need and recorded decision.

## Product architecture principles

- Installed desktop app is the first user-facing runtime; desktop workflows must not depend on a network connection or a hosted website for core local research.
- Shared scientific core and stable language-neutral contracts sit below platform-specific UI and OS adapters.
- Local scientific execution is preferred when feasible; optional Molecularis Node/worker services extend CPU/GPU and memory capacity with explicit pairing and permissions.
- Hosted and institutional/HPC compute are optional, policy-controlled execution targets, never mandatory for ordinary local work.
- A future web companion may consume the same APIs/contracts but must not force the installed apps to become thin website wrappers.
- Existing Android/Kotlin work is migration source material. Preserve valuable algorithms, data, schemas and tests; retire old UI only after parity and user-data migration are demonstrated.

## Non-goals

- Website-first or PWA-first product strategy.
- Android-only or desktop-only architecture.
- Browser execution of arbitrary native code.
- Unrestricted shell or arbitrary code execution in API processes.
- Blind copying of entire upstream platforms.
- Treating code availability as proof of model, dataset or redistribution rights.
- Clinical diagnosis, treatment or dosing recommendations under the current scope.

## Research and release guardrails

Every shipped scientific capability requires declared inputs, units/conventions, method and dependency versions, provenance, limitations, validation evidence and supported-platform evidence. Public builds remain research-use only. Clinical Decision Support Mode remains disabled unless separately authorized and independently validated under applicable governance.

## Change control

This North Star reflects the owner's explicit correction on 2026-11-21: desktop application first across Linux, Windows and macOS; Android and Apple mobile apps also required; no website-first strategy. Record consequential architecture and roadmap changes in DECISIONS.md. Historical Android-first source material remains preserved below this active direction for traceability and is not current product authority.
