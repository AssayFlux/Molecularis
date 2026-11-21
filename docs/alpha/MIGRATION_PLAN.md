> **HISTORICAL / SUPERSEDED FOR EXECUTION (2026-11-21):** This document is retained as source history and technical evidence. Do not use it as an active roadmap or implementation authority. The current repository-first plan is [docs/MASTER_PLAN.md](../MASTER_PLAN.md) for files in `docs/`, or [Master Plan](../MASTER_PLAN.md) for files in `docs/alpha/`. Current exact inventory: [REPOSITORY_BASELINE.md](../REPOSITORY_BASELINE.md); capability mapping: [CAPABILITY_STATUS.md](../CAPABILITY_STATUS.md). Reconcile any still-useful details into the current plan before implementation. No completion or validation claim is implied by this historical document.

---


# Molecularis Cross-Platform Application Migration Plan

## Rule

Migrate by capability and preserve scientific logic, contracts, evidence and user data. The target is an installed desktop-first application for Linux, Windows and macOS, followed by Android and Apple iOS/iPadOS applications. A website/PWA is not the first replacement target.

## Target migration sequence

1. Extract platform-neutral domain and scientific logic from Android/Kotlin UI and lifecycle dependencies.
2. Inventory and version project files, databases, settings, caches, artifacts, credentials and background jobs.
3. Build the desktop application shell and shared domain layer; prove install, offline, project create/open/save/export, local scientific job execution and provenance on Linux, Windows and macOS.
4. Reuse existing C++, Rust and Python foundations behind stable contracts; replace JNI/Chaquopy only where a measured cross-platform boundary is better.
5. Port user-facing capabilities in vertical slices and compare deterministic outputs with the legacy implementation.
6. Add Android and iOS/iPadOS application adapters and UX, preserving shared project formats and scientific semantics.
7. Add optional remote/local-node/HPC integrations only with explicit permissions, threat models and resource policies.
8. Consider a web companion after installed-app milestones; it must use shared contracts and must not become a prerequisite for desktop use.
9. Remove legacy Android-only code only after migration, parity, export/restore and rollback evidence plus owner approval.

## Legacy area mapping

| Legacy area | Action | Target |
|---|---|---|
| Kotlin/Jetpack Compose screens | Retain as reference; replace incrementally | Shared cross-platform application UI |
| Android navigation/state | Extract domain state; replace UI navigation | Platform-neutral application/domain layer |
| Android storage and SQLite | Inventory, migrate and retain compatibility reader | Portable project format + local database |
| WorkManager jobs | Preserve semantics and migration mapping | Cross-platform local job supervisor/queue |
| Chaquopy/Python bridge | Audit and extract | Python scientific runtime/service boundary |
| JNI/C++ | Retain if useful; benchmark | Shared native C++ library/API |
| Rust utilities | Retain and harden | Cross-platform native libraries/services |
| WebView visualizations | Evaluate and isolate | Reusable visualization component in installed app |
| Offline behavior | Preserve and test | Local-first projects, cache and explicit optional sync |
| Android packaging/signing | Keep until mobile migration is validated | Desktop packages plus Android/iOS signing pipelines |

## Data migration requirements

For every legacy store, record schema/version, owner, sensitivity, encryption, backup behaviour and target. Provide export/import, checksums, atomicity, rollback and corruption-recovery tests. Do not silently upload user data. Preserve identifiers required for upgrades until a documented compatibility window has passed.

## Framework selection gate

Before committing to a UI framework, build a small vertical slice on Linux, Windows, macOS, Android and iOS/iPadOS. Score native packaging, accessibility, 3D/GPU visualization, filesystem access, offline storage, background tasks, secure credential storage, update/signing, test automation, performance, contributor skills and licensing. Record measured results and owner decision in DECISIONS.md.

## Completion

A component is migrated only when behavior, scientific outputs, data round-trip, permissions, accessibility, platform tests and rollback are demonstrated. A compiling UI shell alone is not migration completion. Clinical restrictions remain unchanged.
