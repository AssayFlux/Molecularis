# Alpha API and Job Contract Requirements

## API principles
- API is the control plane, not the scientific execution environment.
- Use OpenAPI for HTTP endpoints and JSON Schema for payloads/events.
- Version all public contracts and maintain compatibility tests.
- Enforce project-level authorization on every request and referenced object.
- Use idempotency keys for job submission, artifact creation and retry-safe operations.
- Use pagination, bounded filters, rate limits and explicit error envelopes.

## Resource groups
- Identity/session and organization membership.
- Projects/workspaces and access policies.
- Datasets and artifact metadata.
- Workflows and workflow versions.
- Engine registry and capability discovery.
- Jobs, events, logs and cancellation.
- Provenance, validation evidence and exports.
- Compute nodes, pairing and revocation.

## Job submission envelope
A job submission must identify project, workflow/engine, contract version, input artifact IDs, parameters, unit system, resource request, execution target preference, timeout, network policy, filesystem permissions and idempotency key. The server validates authorization, schemas, engine availability and quotas before scheduling.

## Job lifecycle
created → validated → queued → preparing → running → collecting → succeeded | failed | cancelled | expired

Every state transition is timestamped and audited. Workers report structured progress and diagnostics. Cancellation is cooperative first, then enforced by supervisor termination. Retries are bounded and create a new attempt linked to the original request.

## Error contract
Errors include stable code, safe message, retryability, correlation ID and optional field-level diagnostics. Never expose secrets, host paths or raw stack traces to untrusted clients.

## Streaming
Use authenticated server-sent events or WebSocket channels for job updates. Events are resumable by sequence/cursor and do not replace the durable job record.

## Compatibility and tests
Publish schema fixtures and test them from Python, Rust, C++ and TypeScript. Reject unknown required fields, invalid units, unsupported versions and unauthorized artifact references.