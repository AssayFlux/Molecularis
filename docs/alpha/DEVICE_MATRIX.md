# Molecularis Device and Platform Matrix

## Product principle

One installed application family, desktop-first. Linux, Windows and macOS are the first delivery targets. Android and Apple iOS/iPadOS are required mobile targets and follow on shared domain logic, contracts, project formats and design system. Website/PWA is not the first product.

| Target | Delivery priority | Application form | Core acceptance focus |
|---|---|---|---|
| Linux desktop | First wave | Installable native desktop package | Common distributions, filesystem, GPU/3D, packaging, updates, accessibility |
| Windows desktop | First wave | Signed desktop installer/package | Supported Windows versions, filesystem, GPU drivers, signing, updates, accessibility |
| macOS desktop | First wave | Signed/notarized application package | Supported macOS versions, Apple Silicon and Intel strategy, sandbox/permissions, notarization, updates |
| Android phone/tablet | Second wave | Installable Android application | Supported API/ABI matrix, touch, lifecycle, storage permissions, background work, battery, offline |
| Apple iPhone/iPad | Second wave | Installable iOS/iPadOS application | Supported OS/device matrix, sandbox/files, background lifecycle, signing, review constraints, offline |
| Workstation / lab PC | Desktop first wave plus compute adapters | Desktop application with optional local worker | Large datasets, CPU/GPU, isolation, scheduling, reproducibility |
| Institutional/HPC | Integration after core application | Explicit institution connector and scheduler adapter | Identity, queues, quotas, data residency, audit and policy |

## Desktop-first release gate

Before mobile expansion is declared ready, the desktop baseline must have reproducible builds and install/upgrade/uninstall tests on Linux, Windows and macOS; keyboard and assistive-technology accessibility; filesystem permission and large-file tests; offline operation; project backup/restore; graphics/3D validation; crash recovery; signed release/update paths; and documented supported hardware.

## Mobile release gate

Android and iOS/iPadOS require their own install, upgrade, lifecycle, storage permission, offline, notification/background-task, accessibility, performance, graphics and data migration evidence. Mobile is not satisfied by a responsive desktop UI running in a browser.

## Cross-device invariants

- Identical versioned project and scientific artifact formats.
- Stable scientific outputs within documented numerical tolerances.
- Explicit compute location and resource use.
- Clear sync/conflict and backup/restore status.
- Keyboard, pointer, touch, screen-reader, zoom/reflow and reduced-motion support as appropriate.
- No silent upload of private research files.

## Acceptance evidence

Record exact build SHA, hardware model, OS/version, architecture/ABI, graphics stack, app package version, test cases, commands, results, failures and reviewer. CI or an emulator alone is not physical-device validation.
