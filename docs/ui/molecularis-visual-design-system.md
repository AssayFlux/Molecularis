# Molecularis — active monochrome design system implementation guide

**Authority:** Owner V1 prompt, recorded as D-024 (2026-11-17).  
**Status:** Specification approved; native Compose implementation and evidence in progress.  
**Platform:** Existing Android Jetpack Compose application.  
**Full visual contract:** docs/ui/ui-spec.md. This file defines implementation rules and the status of supporting assets/tokens.

## 1. Design intent
A premium, minimal, monochromatic scientific workspace. Prioritise clarity, precision, usability, readable data, generous but disciplined whitespace and native Android interaction. Do not introduce decorative gradients, heavy shadows, oversized cards, excessive rounding, illustrations, arbitrary accent colours or unnecessary motion.

## 2. Semantic palette
Use only the exact Light and Dark values in docs/ui/ui-spec.md. Compose components consume semantic roles, never scattered raw hex values. Semantic green/amber/red/blue is reserved for status communication and must be paired with text/icon. System mode follows Android system appearance. Do not expose retired palettes as active theme choices.

## 3. Layout and component tokens
Use the 393 × 852 dp reference and responsive 360 × 800, 430 × 932 and tablet 600 dp+ layouts. Use the exact 4 dp spacing rhythm, content margins, type scale, radii and component dimensions from docs/ui/ui-spec.md. Use constraints/window classes, not absolute screen coordinates. Maintain minimum 48 × 48 dp interactive targets.

## 4. Typography and iconography
Use a highly readable sans-serif with system fallback. Respect system font scaling and Indic-script fallback. Tabular numerals are required for statistics. Do not bundle candidate fonts until licence, glyph coverage, offline behavior, file size and rendering are verified. Use one thin line-icon family with consistent 18/24/28 dp optical sizing; do not use text glyphs or emoji as production icons.

## 5. Asset contract
Owner-supplied logos and reference artwork must be preserved byte-for-byte. Do not redraw, recolour, crop destructively, sample colours from or place a duplicate wordmark over supplied brand artwork. Integrate only assets whose exact repository paths and intended roles are verified. Decorative cultural motifs from the superseded D-015 proposal are not enabled by this monochrome V1 unless separately re-authorised.

## 6. Screen composition and product truth
The actual application shell remains Home, Work, Explore and Settings, with adaptive navigation where appropriate. Home is a live research workspace, Work manages real imports/jobs, Explore describes registry capabilities and Settings controls actual preferences/security. Splash/onboarding, local lock, drawer, profile and appearance are separate flows only when implemented. Never invent cloud accounts, jobs, projects, metrics, ETAs, analysis results or executable scientific services. A capability is runnable only with a real Android dispatcher and result/provenance path.

## 7. Accessibility and quality
Measure contrast for every semantic foreground/background pair; target WCAG AA thresholds specified by the project accessibility contract. Verify large text, 200% font scale, TalkBack, focus order, keyboard/switch navigation, RTL, reduced motion, touch targets, dynamic resizing and empty/loading/error/recovery states. Do not claim accessibility conformance until evidence is committed.

## 8. Token and code ownership
Canonical source: design/tokens.json. Generator: scripts/gen_design_tokens.py. Generated outputs: android/designsystem/.../GeneratedTokens.kt and web/viewers/src/styles/molecularis-tokens.css. Never edit generated outputs manually. Compose UI primitives live in android/designsystem; app state and navigation remain in Kotlin app layer. Scientific logic remains outside Compose.

## 9. Required implementation sequence
1. Inventory UI source, assets, tokens, settings, navigation and tests.
2. Reconcile canonical tokens to V1 and make generation deterministic.
3. Implement reusable Compose primitives and a working component gallery.
4. Refine Home, Work, Explore, Settings, drawer, local lock and appearance against real app state.
5. Add search/onboarding only when real behavior is defined.
6. Add result/provenance and scientific viewers only when dispatcher/contract/dependency gates pass.
7. Add screenshot, contrast, accessibility, adaptive-window and regression tests.
8. Run exact-head CI and inspect the built artifact; record device checks separately.
9. Complete Step 2 audit, fix failures and repeat before reporting phase status.

## 10. Status honesty
This guide and the supplied prompt define intended behavior; they are not evidence of a running UI. Concept images are not screenshots. No screen, theme, font, icon library, contrast outcome, accessibility outcome or device support is complete without committed implementation and test evidence. See docs/track-u/implementation-plan.md and docs/ui/quality-report.md.

## Historical design authority
D-015 is retained in DECISIONS.md as historical direction. D-024 supersedes it only where the old visual system conflicts with the owner-supplied monochrome V1 prompt. Non-conflicting requirements (asset preservation, truthful workflows, native Compose, Research Mode and engineering/security constraints) remain active.
