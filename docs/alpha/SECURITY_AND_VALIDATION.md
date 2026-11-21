# Alpha Security, Privacy and Scientific Validation

## Trust boundaries
Treat uploaded files, archives, notebooks, workflow definitions, model files, third-party engines and local-node requests as untrusted. Separate browser client, API/control plane, identity/project authorization, scheduler, isolated worker, artifact storage, Molecularis Node and external/institutional services.

## Required controls
- Project/tenant authorization on every object and job.
- Short-lived scoped credentials; no secrets in job payloads or logs.
- TLS in transit and encryption at rest where supported.
- Signed job manifests and versioned engine manifests.
- Worker isolation with CPU, memory, disk, process, time and network limits.
- No arbitrary shell execution in API/control-plane processes.
- Explicit filesystem mounts and read/write allowlists.
- Safe archive extraction, file type/size limits and path traversal prevention.
- Dependency pinning, SBOM, vulnerability review and license inventory.
- Audit events for access, sharing, compute placement, export and deletion.
- Local-node pairing, explicit capabilities, visible consent and revocation.
- Backup/restore and retention policy.
- No telemetry or external upload without transparent user control.

## Notebook and agent safety
Notebook kernels and ChemGraph agents run in isolated worker environments with quotas, timeouts, restricted network and explicit mounted data. Do not expose host secrets, unrestricted filesystem, Docker socket or privileged APIs. Browser execution is not a security boundary for native code.

## Scientific validation layers
1. Schema and contract validation.
2. Unit/integration tests and deterministic fixtures.
3. Reference comparisons against trusted methods/datasets.
4. Benchmark accuracy, calibration, uncertainty and performance.
5. Runtime/device/accelerator validation.
6. Independent domain expert review.
7. Owner release acceptance.

Each layer is recorded separately. CI green is not scientific validation.

## Provenance
Every job records immutable input checksums, project/dataset IDs, engine/container versions, model/database versions, parameters, units, seeds, environment, compute hardware, timestamps, logs, output checksums and warnings. Reports distinguish measured, predicted, inferred and user-supplied values.

## Medical and clinical boundaries
Current scope is research use. No diagnosis, treatment selection, dosing recommendation, clinical interpretation or clinical deployment is authorized. Any future change requires explicit owner decision, qualified clinical/scientific review, ethics/legal assessment, jurisdiction-specific regulatory analysis, privacy/security controls and prospective validation.