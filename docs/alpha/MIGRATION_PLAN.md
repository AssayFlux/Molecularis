# Android-to-All-Device Migration Plan

## Rule
Do not delete or rewrite legacy Android code until its purpose, dependencies, user data and replacement path are known. Android is no longer the product roadmap, but the repository contains useful scientific and engineering foundations.

| Legacy area | Action | Target |
|---|---|---|
| Kotlin/Jetpack Compose screens | Replace incrementally | Responsive web/PWA UI |
| Android navigation/state | Replace | Web application routing/state |
| Android storage and SQLite | Migrate/retain selectively | Project API + object storage; local encrypted cache/node metadata |
| WorkManager jobs | Replace semantics, not blindly code | Durable job service and local-node queue |
| Chaquopy/Python bridge | Audit and extract | Python service/worker packages |
| JNI/C++ | Retain if useful; benchmark | C ABI/native worker or local node |
| Rust utilities | Retain and harden | Cross-platform native libraries/services |
| WebView visualizations | Evaluate/reuse | Browser-native visualization modules |
| Offline behavior | Preserve intent | PWA cache, local node queue, explicit sync |
| Android packaging/signing | Retire after migration | Optional desktop/node packaging and web deployment |

## Migration stages
1. Inventory modules, entry points, tests, storage schemas and dependencies.
2. Map every user-facing capability to a web/PWA replacement or documented retirement.
3. Extract domain logic from Android lifecycle and UI dependencies.
4. Define API/schema contracts before replacing cross-component calls.
5. Migrate local user data with export, checksum, import and rollback tests.
6. Implement responsive workflows in vertical slices.
7. Run parity tests against legacy deterministic outputs.
8. Keep a compatibility reader until migration completion is demonstrated.
9. Remove Android-only build targets only after owner approval and archived evidence.

For each component record path/module, behavior, dependencies, formats, tests, risk, classification, replacement path, migration status, parity evidence and removal approval.

Never put real patient data, credentials or private datasets in fixtures. Clinical restrictions remain unchanged.