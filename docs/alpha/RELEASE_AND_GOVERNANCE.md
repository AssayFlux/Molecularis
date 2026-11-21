# Alpha Release and Governance

## Release channels
- Development: internal installable desktop builds for Linux, Windows and macOS.
- Preview: opt-in desktop research preview after minimum security, privacy and data-integrity gates.
- Mobile preview/stable: Android and iOS/iPadOS only after platform-specific lifecycle, permissions, signing and data-integrity gates.
- Stable: supported desktop platform matrix, operational readiness, validated scientific vertical slices and rollback plan.
- Web companion: deferred; not a prerequisite for desktop or mobile release.
- Institutional: tenant isolation, SSO/integration policy, data residency, audit export, backup/restore, support and incident procedures.

## Required release evidence
- Exact commit SHA and reproducible build instructions.
- SBOM, dependency and license inventory.
- Security and privacy review appropriate to the release scope.
- Supported OS/device/hardware matrix and accessibility results for each installed application target.
- Scientific validation reports for every advertised capability.
- Install/upgrade/uninstall, data migration, backup/restore and rollback evidence on each supported OS.
- Operator runbook, monitoring, incident contacts and known limitations.
- Owner approval and release notes.

## Governance
Changes to product direction, languages, data sources, engines, licensing, privacy/clinical posture and release policy require DECISIONS.md updates. Scientific claims must link to evidence. Third-party code, models, datasets, fonts and containers have separate license/terms reviews.

## No clinical claims
The platform remains research-use only. No clinical diagnosis, treatment, dosing or decision-support release is permitted under the current scope.