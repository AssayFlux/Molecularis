# Molecularis Design System

**Status:** Shared Compose primitives are being built for owner V1 monochrome UI (D-024); implementation and visual evidence remain in progress.

The Android design-system module compiles generated Compose semantic palettes and spacing/radius tokens from design/tokens.json using scripts/gen_design_tokens.py. MolecularisLightClassic and MolecularisDarkClassic are the active V1 palettes; other legacy palette entries are retained only as non-selectable historical/catalogue data until removed through the token audit.

Shared V1 primitives are in MolecularisComponents.kt: primary and secondary actions, outlined panels, text-labelled status, section headings and fields. These are foundational components, not evidence that every app screen has migrated to them.

The component gallery is a development surface, not production navigation. Responsive navigation currently uses Material 3 NavigationBar, NavigationRail and PermanentNavigationDrawer with a live window classifier and 840dp readable-content cap. Fold/hinge-aware behavior is not implemented or claimed.

Generated files must not be edited manually. Run the generator and CI reproducibility check after every token change. Contrast, screenshot, accessibility and device verification remain open.
