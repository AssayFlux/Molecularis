# Molecularis Future Architecture and Research Register

Status: forward-looking architecture. Nothing in this document is a claim that the capability is implemented.

## Target architecture

1. **Core contracts:** service identity, capability discovery, typed request/response/error envelopes, versioning, authorization and observability.
2. **MSDE:** immutable content-addressed artifact storage, manifests, catalog, journal/recovery, native indexes, bounded streaming/query execution and evidence ledger.
3. **Scientific services:** A–N domain engines, runtimes and Rulebooks with service-owned schemas and validation.
4. **Rulebook execution:** typed, versioned DAGs with preconditions, postconditions, budgets, method identity, retry policy, evidence requirements and explicit terminal states.
5. **Workflow integration:** cross-service artifact handoff, dependency invalidation, deterministic replay and auditable execution.
6. **Adapters:** optional external formats, import/export and independent reference tools, isolated behind explicit contracts.
7. **Interfaces:** API/CLI/SDK and future product clients; presentation layers remain outside scientific correctness boundaries.

## Future workstreams (not authorized as parallel service implementation)

### Data and scale
- Chunked and streaming artifact formats; compression and deduplication.
- Exact, ordered/range, interval, inverted, sequence candidate and spatial candidate indexes with exact verification.
- Query planning, snapshot isolation, pagination, resource budgets and explicit partial-result semantics.
- Sharding/replication only after single-node consistency and benchmark evidence.
- Backup, restore, corruption detection and disaster recovery.

### Scientific execution
- Deterministic and stochastic execution profiles.
- CPU/GPU acceleration only behind equivalent correctness tests and measured benefit.
- Plugin/adapter isolation and reproducible environment manifests.
- Reference-data registries with checksums, licenses and version lifecycle.
- Validation evidence levels, uncertainty reporting and calibration.

### Rulebook and planning
- Rulebook schema, static validation, dependency resolution and cycle detection.
- Preconditions/postconditions and typed artifact constraints.
- Planner that selects only registered, authorized capabilities.
- Bounded retry and repair loops; every change invalidates dependent evidence.
- AI-assisted proposal generation with deterministic validation and human approval where required.

### Security and governance
- Threat model, sandboxing, secret handling, signed artifacts and supply-chain controls.
- Dataset classification, consent/legal basis, retention and access controls.
- Dependency provenance, resolved release SBOM, vulnerability policy and license compliance.
- Audit logs and reproducible release attestations.

### Operations and deployment
- Resource profiles derived from representative workloads.
- Local workstation, server and cluster execution only after support matrices are tested.
- Metrics, structured logs, traces, health checks and operational runbooks.
- Versioned migrations and backward-compatibility policy.

## Research decision protocol

For every proposed technology or dependency, record: problem addressed, alternatives, scientific/engineering evidence, license, security, portability, maintenance cost, performance measurements, failure modes and exit strategy. Prototype behind a boundary; do not let a prototype become a mandatory dependency by accident.

## Explicit non-goals until evidence exists

- No promise of universal biological prediction or clinical-grade interpretation.
- No automatic cloud/GPU/cluster requirement.
- No unbounded agent loops or autonomous changes to scientific acceptance criteria.
- No replacement of experimental evidence with computational confidence.
- No distributed storage or vector database added merely for fashion.
