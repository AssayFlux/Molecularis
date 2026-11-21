# Track S1 — Offline structure viewer contract

**Status (2026-11-10):** Android SAF import, hardened local WebView integration, JSON session export and bounded PNG snapshot export are implemented and exact-source CI verified. SVG export, persisted interactive-view state and physical-device/benchmark evidence remain open.

## Scope and non-goals

S1 provides offline display of validated user-selected PDB/mmCIF coordinate payloads, with reproducible preparation provenance. It does not invent bonds, protonation, secondary structure, confidence, quality grades or biological conclusions.

## Current implementation

- `python/molecularis/structure_view.py` builds deterministic `kinetics.structure-view.v1` payloads with Angstrom coordinates, finite-coordinate checks, unique atom serials, bounded annotations, atom ceiling (200,000), serialized-byte ceiling (32 MiB) and explicit limitations.
- `web/viewers/src/structure-viewer.html`, `structure-viewer.css` and `structure-viewer.js` implement a dependency-free Canvas 2D coordinate renderer. It supports drag rotation, wheel zoom, element/chain colouring, nearest-atom selection and an accessible first-500-atom list.
- The viewer validates payload schema, atom count, unique serials, finite coordinates, normalized element labels and the 32 MiB ceiling before rendering. Bounds calculation is iterative and does not spread large coordinate arrays onto the JavaScript call stack.
- The HTML Content Security Policy denies network connections and all default resources; only local script/style assets are permitted. There is no generic JavaScript/native bridge, filesystem access, eval hook, remote loader or telemetry.
- `android/app/src/main/java/org/assayflux/kinetics/StructureViewer.kt` connects SAF PDB/ENT/CIF/mmCIF import to the Python preparation/provenance path, loads byte-identical local assets through AndroidX WebViewAssetLoader, blocks network/file/content access and mixed content, constrains navigation, and exposes no generic JavaScript/native bridge.
- Android SAF exports deterministic session JSON and PNG snapshots; PNG capture is limited to 16 megapixels and cleans up the active WebView/bitmap lifecycle.
- `tests/test_structure_viewer_assets.py` checks web/Android asset parity, network-denial policy, bounded payload constants, bridge/eval absence, SAF contracts and PNG export bounds.
- The viewer is an original Molecularis implementation with no third-party runtime dependency; therefore there is no external viewer runtime license to approve.

## Remaining software work and exit evidence

1. Add SVG snapshot export and persist/restore interactive view state in the session format; retain explicit size ceilings and no arbitrary JavaScript/native bridge.
2. Add import/export failure-preserves-source and state round-trip tests.
3. Produce fixture screenshots, accessibility checks, memory/latency benchmarks and physical low-end arm64 device evidence.
4. Test supported Android System WebView versions and adaptive window sizes.

Android integration and automated package tests are implemented; physical-device evidence is not available here. Do not mark S1 fully exited until the remaining software work and device/evidence gates are addressed.
