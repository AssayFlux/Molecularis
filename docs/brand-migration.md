# Molecularis identity migration

This repository's product identity is **Molecularis**. New source namespaces, package metadata, UI component names, generated design tokens, viewer globals, documentation and asset paths use the Molecularis name.

## Compatibility retained intentionally

| Surface | New identity | Compatibility retained |
|---|---|---|
| Android source namespace | `org.assayflux.molecularis` | Android `applicationId` remains `org.assayflux.kinetics` so installed copies can update in place and retain app-private data. Changing it requires a separately planned app migration. |
| Python package | `molecularis` | `kinetics` is a thin import-compatibility package; the actual enzyme-kinetics implementation remains `molecularis.kinetics`. |
| Node worker configuration | `MOLECULARIS_*` | Existing `KINETICS_*` environment variables remain accepted as fallbacks. Molecularis variables take precedence. |
| Structure viewer API | `window.MolecularisStructureViewer` | `window.KineticsStructureViewer` aliases the same API for embedded clients. |
| CSS design tokens | `--molecularis-*` | `--kinetics-*` variables alias the new tokens. |
| Versioned scientific schemas | New source and product labels use Molecularis | Existing versioned identifiers such as `kinetics.structure-view.v1` remain stable protocol contracts; changing them requires explicit schema-version migration. |
| Persisted Android identifiers | Kept stable | The SQLite database filename, SharedPreferences key, WorkManager tags and cache prefixes remain unchanged so upgrades can find prior jobs, settings, work and files. Migrate them only with explicit copy/dual-read logic. |
| Scientific terminology | Unchanged | Enzyme kinetics, Michaelis–Menten models, kinetic transforms and the scientific `kinetics.py` module retain their correct domain meaning. |

## Historical material and artwork

The owner-supplied historical master and session records remain identifiable as archival source material. Legacy artwork blobs were preserved byte-for-byte while their active asset paths were renamed; their visible artwork still needs an owner-approved Molecularis master before release use. Do not present an unchanged Kinetics wordmark as a final Molecularis logo.

## Release checks

Run the repository CI workflow on the migration branch. Confirm Python package discovery, Android namespace/JNI linking, Chaquopy module imports, generated-token reproducibility, viewer tests, Node compatibility tests, and the existing capability-catalogue/schema contracts before merging.
