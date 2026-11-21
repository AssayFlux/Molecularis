# Alpha Operations and Compute Architecture

## Compute targets
1. Browser: UI, lightweight validation and visualization only.
2. Molecularis Node: opt-in local agent for filesystem, native engines and local CPU/GPU.
3. Hosted workers: isolated OCI/container execution for approved engine profiles.
4. Institutional/HPC: scheduler/API integration under institution policy.
5. Cloud: optional, cost-transparent, region-aware execution.

## Job lifecycle
Use a durable state machine: created → validated → queued → preparing → running → collecting → succeeded | failed | cancelled | expired. State transitions are server-authoritative and append-only in the audit stream. Retries are idempotent and bounded.

Each job has owner/project, engine manifest, contract version, input artifact references, resource request, timeout, execution target, permissions, cancellation token and provenance record.

## Molecularis Node
- Rust-first supervisor, signed updates and engine manifest verification.
- Pairing through explicit user approval and short-lived credentials.
- Capability allowlist: approved filesystem paths, engines, devices and resource classes only.
- No inbound public listener by default; use outbound authenticated connection where practical.
- Per-job isolated process/container where available.
- CPU, memory, disk, GPU and time quotas.
- Visible job activity, logs, cancellation and disconnect/revoke control.
- OS-specific packaging and auto-update only after signing, rollback and supply-chain controls.

## Operations
Provide structured logs, metrics, tracing, queue depth, worker health, resource use, job outcomes, artifact storage health and audit exports. Define SLOs only after measured workload baselines. Add backup/restore drills, disaster recovery, incident response and rollback before institutional production.

## Data placement and cost
Show users where input/output data reside and where computation occurs. Do not silently transfer large datasets. Provide quota/cost estimates for cloud jobs and institution-specific retention/data-residency policies.