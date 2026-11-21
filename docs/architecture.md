# Architecture — Desktop-First Cross-Platform Target

**Status:** Target architecture; not a claim that the runtime is already implemented.  
**Authority:** NORTH_STAR.md, ROADMAP.md, DECISIONS.md and docs/alpha/MASTERPLAN.md.

## Product delivery order

1. **Desktop application first:** Linux, Microsoft Windows and macOS, with installable, signed/reproducible platform packages and native OS integration.
2. **Mobile applications:** Android and Apple iOS/iPadOS, sharing domain logic, contracts, project formats, provenance and design language.
3. **Optional web companion later:** only where it adds value for collaboration, institutional access or remote monitoring. It is not the initial product or the core runtime.

Do not describe a responsive website/PWA as the primary client. Core desktop workflows must work as an installed application and support local/offline research.

## Layered architecture

- **Cross-platform application UI:** choose after a documented feasibility spike. Evaluate Qt 6/C++ and other credible cross-platform options against all five target OS families. Criteria include accessibility, native look/feel, packaging, signing/updating, GPU/3D rendering, scientific visualization, offline storage, mobile lifecycle, platform APIs, test automation, contributor skills and license obligations. No framework is approved by this architecture note alone.
- **Domain/application layer:** platform-neutral workflows, projects, datasets, jobs, settings and permissions. No UI-framework or OS lifecycle dependency.
- **Scientific core:** C++ for measured performance-critical kernels; Rust for safe native services, parsing, validation and supervision; Python for scientific orchestration and ecosystem adapters.
- **Platform adapters:** filesystem, secure credential storage, notifications, background execution, hardware acceleration, accessibility and update/signing adapters for Linux, Windows, macOS, Android and iOS/iPadOS.
- **Compute services:** local process workers first where appropriate; optional paired Molecularis Node, hosted workers and institutional/HPC connectors for workloads beyond the current device.
- **Persistence:** versioned project format and local database with explicit migrations; optional shared PostgreSQL/object storage only when collaboration or hosted execution is enabled.
- **Contracts:** versioned JSON Schema/OpenAPI or equivalent language-neutral contracts, semantic versioning and compatibility tests.
- **Visualization:** reusable scientific visualization components; Mol* and other viewers are integrated behind stable interfaces and tested on every target graphics stack.

## Runtime and security boundaries

The UI is not a security boundary. Scientific engines and imported workflows are treated as untrusted. Use least-privilege worker processes, explicit file scopes, resource quotas, signed manifests where appropriate, cancellation, audit events and reproducible job manifests. Never expose arbitrary shell execution through a privileged control/API process. Remote compute is opt-in, authenticated, encrypted, cost-transparent and policy-aware.

## Data and portability

- Define portable project, dataset, artifact and provenance formats independent of OS and UI framework.
- Keep local project data user-controlled and exportable.
- Use atomic writes, checksums, backup/restore and tested schema migrations.
- Make sync/conflict behaviour explicit before introducing multi-device synchronization.
- Do not require cloud accounts or website availability for local desktop workflows.

## Migration

Preserve useful Android/Kotlin, Python, C++, Rust, schemas, tests, provenance and user data. Extract domain logic from Android lifecycle/UI dependencies. Build desktop vertical slices and prove parity before retiring legacy flows. Then implement mobile platform adapters and UI parity. See docs/alpha/MIGRATION_PLAN.md.

## Evidence boundary

A target architecture, framework spike, compiling package or green CI run does not prove complete platform support, security, scientific validity or release readiness. Every platform requires install/upgrade, accessibility, offline, filesystem, performance, graphics and recovery evidence. See docs/alpha/MASTERPLAN.md and docs/alpha/TEST_STRATEGY.md.
