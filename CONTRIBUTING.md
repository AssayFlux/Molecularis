# Contributing to Molecularis

Molecularis is governed by NORTH_STAR.md, ROADMAP.md and DECISIONS.md. For the all-device transition, read docs/alpha/MASTERPLAN.md and the documents indexed in docs/alpha/README.md.

## Rules
- Work on branch Alpha for the all-device transition. Do not commit directly to CORE.
- Follow the engineering integration standard and Alpha language strategy before substantial changes.
- Preferred core languages are C++, Rust and Python. TypeScript/JavaScript is required for the browser/PWA client. Do not add other languages or engines without a concrete need and decision record.
- Use versioned JSON Schema/OpenAPI contracts for cross-component messages; do not silently fork semantic definitions.
- Every substantial engineering update includes a Check section and a Next step.
- Preserve scientific domain logic, tests, provenance, schemas and user data when migrating away from Android.
- Android-native product development is retired. Do not add new Android-only capabilities. Keep legacy code only as migration/compatibility context until replacement parity is demonstrated.
- Never claim a capability is implemented, validated or device-verified without committed evidence.
- Do not add real patient data, secrets, model weights, private datasets or large generated binaries.
- Preserve the Apache-2.0 project license and review third-party code, data, models and tool licenses separately.
- Keep changes small, typed, tested and reproducible. Record provenance, limitations and upstream versions.
- Scientific outputs must state uncertainty, limitations and research-use status.
- Clinical decision support is out of scope. Do not add diagnosis, treatment or dosing features.
- Stop at milestone exit gates and report evidence and blockers.

The repository owner controls integration to CORE and releases. Creating Alpha does not authorize merging or publishing releases.
