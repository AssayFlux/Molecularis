# Verified Android and Material specifications

**Checked:** 2026-11-08 against Android Developers documentation. Re-check before every release.

## App-window size classes

Android currently defines width breakpoints as compact (<600dp), medium (600–<840dp), expanded (840–<1200dp), large (1200–<1600dp), and extra-large (≥1600dp). Height classes are compact (<480dp), medium (480–<900dp), and expanded (≥900dp). Classification is based on the app window, not the physical device; it changes with rotation, fold/unfold and multi-window.

Molecularis now evaluates live Compose window constraints. Navigation maps compact portrait windows to a bottom bar; all compact-height windows to a rail (including very wide short windows); medium/expanded windows to a rail; and large/extra-large windows (≥1200dp, non-compact height) to a permanent drawer. Readable content is capped at 840dp. JVM boundary tests cover the classifier, but device rendering is not verified.

Sources:
- https://developer.android.com/develop/ui/views/layout/use-window-size-classes
- https://developer.android.com/develop/adaptive-apps/guides/use-window-size-classes

## Adaptive navigation

Android documents `NavigationSuiteScaffold` in the Material 3 adaptive navigation suite. Molecularis currently uses stable Material 3 NavigationBar, NavigationRail and PermanentNavigationDrawer components with a window classifier, rather than NavigationSuiteScaffold. WindowManager fold posture/hinge support is not integrated. Do not describe the current shell as fold-aware.

Source:
- https://developer.android.com/develop/adaptive-apps/guides/build-adaptive-navigation

## Accessibility and touch targets

Android recommends interactive targets at least 48×48dp. This is a design target, not evidence of a TalkBack or WCAG pass. Status pills are non-interactive and expose state descriptions; navigation controls use Material components. Manual TalkBack, Switch Access, contrast, large-text and display-size checks remain outstanding.

Source:
- https://developer.android.com/guide/topics/ui/accessibility

## Edge-to-edge and predictive back

The app targets SDK 36. Edge-to-edge, system-bar/IME/cutout insets and predictive-back behavior must be verified on actual devices and navigation modes. No device pass is claimed.

Sources:
- https://developer.android.com/develop/ui/views/layout/edge-to-edge
- https://developer.android.com/design/ui/mobile/guides/patterns/predictive-back

## Not yet verified
- WindowManager fold features, hinge avoidance and tabletop/book posture.
- Exact Material 3 navigation dimensions and adaptive-icon safe-zone values.
- Splash screen, Play Store icon and feature graphic specifications.
- Target SDK / Play policy requirements at release time.
- Biometric, StrongBox, Play Integrity and notification permission behavior.
- Accessibility and performance budgets on a named low-end device.
