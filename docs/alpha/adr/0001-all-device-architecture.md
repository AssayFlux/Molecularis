# ADR-0001: Desktop-First Cross-Platform Application

- Status: Accepted product direction; UI framework selection remains open
- Date: 2026-11-21
- Decision owner: Project owner
- Context: The initial Alpha proposal incorrectly made a responsive website/PWA the primary client. The owner explicitly corrected the requirement: desktop application first for Linux, Microsoft Windows and macOS, plus Android and Apple mobile applications; no website-first strategy.

## Decision

Molecularis is an installed, desktop-first cross-platform scientific research application.

**Delivery order**
1. Linux, Windows and macOS desktop applications.
2. Android and Apple iOS/iPadOS applications using shared domain logic and contracts.
3. Optional web companion only after the installed application foundation, and only if justified by collaboration or institutional requirements.

The website/PWA is not the product's primary client and must not be used as a substitute for desktop or mobile application support.

## Architecture constraints

- Keep domain logic and scientific workflows independent of UI frameworks and OS lifecycle APIs.
- Prefer C++, Rust and Python for the scientific/core layers.
- Select a cross-platform UI/application framework only after a measured feasibility spike against all five OS families, accessibility, graphics/3D, native APIs, packaging/signing, updates, offline storage, mobile lifecycle and licensing.
- Preserve local-first desktop workflows; network availability is not required for ordinary local work.
- Share versioned project formats, schemas, provenance and numerical acceptance tests across platforms.
- Keep remote/HPC execution optional and explicitly authorized.
- Preserve valuable Android implementation and user data until migration parity is proven.

## Consequences

- Replace the previous web/PWA-first M1/M2 assumptions with desktop shell, project storage, local execution and packaging milestones.
- Re-sequence mobile as the next application target, not a browser fallback.
- Defer web companion and hosted-first architecture until after desktop/mobile foundations.
- Add Linux/Windows/macOS packaging, signing, update, graphics and filesystem validation to release gates.
- Framework choice remains an evidence-based open decision; this ADR does not prematurely select Qt, Tauri, Flutter or another framework.

## Alternatives considered

- Website/PWA first: rejected by explicit owner direction.
- Android-first: rejected as too narrow for the required desktop-first scope.
- Desktop-only: rejected because Android and Apple mobile applications are required.
- Separate unrelated codebases per OS: rejected because it duplicates domain logic and scientific contracts.

## Revisit when

A measured framework spike reveals a blocker, an important security/accessibility constraint emerges, or the project owner changes product direction.
