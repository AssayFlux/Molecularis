# Brand contract

**Status:** Owner-supplied visual references and legacy artwork are present under the case-sensitive root `Assets/`. The canonical `assets/brand/` input set is not present in the current repository tree. Final app-icon approval, brand usage rules and asset clearance remain open.

## Canonical asset contract

The intended canonical asset root is `assets/`, with owner-approved brand inputs under `assets/brand/` and design previews under `assets/design-previews/`. This layout is a target contract, not a completed migration. The current repository still contains the legacy root-level `Assets/` directory; it has **not** been consolidated into the lowercase canonical layout.

Do not move, rename, redraw, recolour or derive owner artwork without explicit authorization. Preserve existing binary Git blobs byte-for-byte. In particular, the organization logo is not automatically the Molecularis Android launcher icon.

## Required owner inputs

The Android release verification task expects the following files under `assets/brand/`:

- `app-logo.svg`
- `app-logo-foreground.svg`
- `app-logo-monochrome.svg`
- `brand-logo.svg`
- `brand-logo-light.svg`
- `brand-logo-dark.svg`
- `brand-usage.md`
- One approved app-logo background declaration (`app-logo-background.txt` or `app-logo-background.svg`)

These files are currently absent from the repository tree. Do not generate placeholder or substitute artwork to satisfy the release gate.

Still required from the owner: minimum size, clear space, forbidden changes, official hex colours, approved background use, confirmation of the final app-mark master and asset usage/clearance terms.

## Release gate

Release builds are intentionally blocked until the complete owner-approved asset set and usage documentation are supplied and verified. The Gradle `verifyOwnerBrandAssets` task is a fail-closed control; its failure in the current tree is an expected unresolved owner-input gate, not evidence that a debug build has failed.
