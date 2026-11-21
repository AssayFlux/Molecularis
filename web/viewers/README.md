# Offline structure viewer

This is a dependency-free, local coordinate viewer for validated
`kinetics.structure-view.v1` payloads. It uses Canvas 2D and native browser
events; it does not download scripts, fonts, data, or other resources.

## Integration contract

Load `structure-viewer.html` from an app-owned asset origin, then pass a
validated payload to:

```js
window.MolecularisStructureViewer.load(payload);
```

The viewer independently validates the schema subset, finite coordinates,
unique serials, atom/byte limits (200,000 atoms / 32 MiB), and limitations.
It supports drag rotation, wheel zoom, element/chain colouring, nearest-atom
selection, and a bounded accessible atom list.

## Scientific and security limits

This renderer displays coordinate points only. It intentionally does not
infer bonds, secondary structure, protonation, quality, confidence, or
biological meaning. It has no generic JavaScript/native bridge, filesystem
access, remote resource, telemetry, or network fallback. The embedding
application remains responsible for validating the canonical Python payload,
using a hardened local asset origin, and recording preparation provenance.

The viewer is an original Molecularis implementation with no third-party runtime
dependency. Validate on supported WebView versions and physical devices before
claiming release readiness. Canvas performance at the maximum atom limit is
not yet benchmarked.
