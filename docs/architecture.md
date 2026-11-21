# Architecture — Alpha All-Device Target

**Status:** Target architecture, not a claim of implemented runtime.  
**Authority:** NORTH_STAR.md, ROADMAP.md and DECISIONS.md.

## Product clients
- Responsive TypeScript web application/PWA is the primary client for phone, tablet, laptop and desktop.
- Optional desktop packaging reuses the same web client and API.
- Android/Kotlin is legacy migration context, not the product foundation.

## Scientific and platform language ownership
- Python: scientific orchestration, APIs, reference workflows and ecosystem adapters.
- Rust: safe parsers, validation, local-node supervisor, worker lifecycle and resource controls.
- C++17+: measured numerical kernels and native scientific libraries.
- TypeScript/JavaScript: browser/PWA UI, visualization and offline client behavior.
- SQL and versioned JSON Schema/OpenAPI: persistence and interface contracts.

## Runtime topology
- Web client handles presentation, lightweight validation and visualization.
- API/control plane manages identity, projects, artifacts, jobs, policy and provenance.
- Isolated workers execute approved scientific engines.
- Molecularis Node is an opt-in local connector for workstation files, CPU/GPU and native engines.
- Institutional/HPC connectors submit jobs through institution-approved schedulers.
- PostgreSQL is the shared metadata store; object storage holds large artifacts; SQLite may remain for local node metadata/cache.

## Contracts and boundaries
Use versioned schemas and explicit semantic versions for all cross-component messages. Prefer process/IPC boundaries for independently deployed services and a narrow stable C ABI for native libraries. Do not expose language exceptions/panics across boundaries. Every job has an immutable manifest, resource limits, cancellation and provenance.

## Scientific engines
Engines are optional, isolated profiles with exact versions, license/model/data review, resource profiles, validation datasets and documented limitations. A registry entry does not imply integration or validation.

## Security
The API is not an arbitrary code execution host. Uploaded data, notebooks, archives and engine inputs are untrusted. Workers have explicit mounts, least privilege, quotas, network policy and audit events. Local-node pairing is explicit and revocable.

## Migration
Preserve useful scientific code, tests, schemas, provenance and user data. Replace Android UI/lifecycle/storage incrementally only after parity and migration tests. See docs/alpha/MIGRATION_PLAN.md.

See docs/alpha/MASTERPLAN.md for the full architecture and milestone plan.
