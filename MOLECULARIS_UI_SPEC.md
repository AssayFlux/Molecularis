# MOLECULARIS — UI/UX master specification index

**Current visual authority:** Owner-supplied Premium Minimal Monochrome Design System — V1 (D-024, 2026-11-17).  
**Platform:** Native Android Jetpack Compose.  
**Track:** U — User interface.

This file is an index, not a competing design specification. The 20-section owner prompt supplied on 2026-11-17 is the active visual contract. Its exact viewport, spacing, typography, light/dark colours, component measurements, interaction, safe-area, accessibility and responsive rules are transcribed in docs/ui/ui-spec.md. Product scope and real workflow behavior remain governed by NORTH_STAR.md, ROADMAP.md, the capability registry, architecture, privacy/security controls and phase gates.

## Active design at a glance
- Monochromatic light/dark foundation: the exact V1 hex values; semantic colours only for status.
- System, Light and Dark appearance.
- 393 × 852 dp reference viewport; responsive compact, standard, large and tablet layouts.
- 4 dp spacing system, restrained radii, precise component heights and native mobile behavior.
- Refined sans-serif typography, tabular statistics and system font scaling.
- Thin line icons, subtle separators, balanced whitespace and no decorative clutter.
- Actual MOLECULARIS workflows only: Home, Work, Explore, Settings, real local lock and supported research operations.

## Product truth
- Home counts and activity derive from persisted ResearchStore jobs.
- Work exposes actual import/job lifecycle and export/provenance actions.
- Explore is registry-backed; only capabilities with a real Android dispatcher and result path can run.
- Settings reflects actual persisted appearance, diagnostics and local app-lock behavior.
- Local biometric app lock is not cloud account authentication.
- No fabricated user identity, projects, jobs, metrics, ETAs, results or scientific services.

## Supersession
D-024 supersedes D-015 only where the older visual language conflicts with V1. D-015 remains historical evidence; its non-conflicting requirements remain active, including preservation of owner assets, native Compose, truthful workflows, Research Mode boundaries, and font/licence/accessibility review. Do not restore earlier neon/Obsidian Cyan palettes.

## Owner-approved screen blueprint (2026-11-18)
- The owner-supplied Login and Dashboard reference images are preserved at `Assets/App UI - Login Page Design.jpg` and `Assets/App UI - Dashboard Design.jpg`.
- Their structural requirements, account/authentication truth boundaries, service-carousel behavior, four dashboard panels and acceptance checklist are documented in `docs/ui/owner-blueprint-implementation.md`.
- D-024 remains the final visual authority; placeholder colours in the reference images do not supersede the monochrome system.

## Source and evidence
- Full active prompt and exact values: docs/ui/ui-spec.md.
- Design tokens: design/tokens.json.
- Generator: scripts/gen_design_tokens.py.
- Compose design system: android/designsystem.
- Screen and capability truth: docs/ui/screen-map.md and capabilities/registry.yaml.
- Device matrix: docs/ui/device-matrix.md.
- Quality evidence: docs/ui/quality-report.md.
- Track plan and two-step gate: docs/track-u/implementation-plan.md.

Concept images are references only. A screen is complete only when the real implementation, tests and required screenshot/device evidence exist.
