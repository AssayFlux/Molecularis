# Molecularis — Desktop Compute Architecture

**Status:** Proposed architecture; not an implementation or security approval.  
**Date:** 2026-11-20

## 1. Role of desktop compute

Android is the research control surface. Desktop compute is an optional, user-controlled execution host for resource-intensive workloads. The first reference host is Linux x86_64. Windows support should be evaluated per engine; WSL2 is a candidate compatibility route for Linux-only engines, not a universal guarantee. macOS can be assessed after the Linux reference path is stable.

## 2. Logical components

1. **Android job client:** constructs validated job envelopes, displays capability availability, previews data transfer, submits/cancels jobs and verifies returned artifacts.
2. **Pairing and identity:** explicit user pairing, host identity, revocation and key rotation. Do not rely on a shared static token as the final identity design.
3. **Desktop worker:** receives only declared capability jobs; validates schema and policy; queues jobs; starts a pinned engine profile; streams structured status; returns bounded outputs.
4. **Engine adapter:** translates Molecularis job contracts into one engine’s API/CLI and normalizes output.
5. **Environment manager:** selects an installed, pinned runtime profile. It must not silently install software or download weights.
6. **Artifact store:** content-addressed inputs/outputs, hash verification, retention controls and explicit cleanup.
7. **Audit/provenance:** records user, host, engine version, profile digest, parameters, input/output hashes, timestamps and terminal state.

## 3. Transport and trust

- Keep loopback-only operation as the safe local default.
- For LAN or other non-loopback access, require TLS, authenticated pairing and host identity verification.
- Design for certificate renewal, revocation, replay protection, request expiry and clock skew.
- Do not expose a generic command, arbitrary path, shell, Python snippet or unrestricted filesystem endpoint.
- Use capability identifiers and typed parameters; validate every request on the worker, not only in Android.
- Treat returned files and logs as untrusted inputs and enforce size/type limits.

## 4. Job lifecycle

`created → validated → queued → running → collecting → completed`

Terminal alternatives: `rejected`, `failed`, `cancelled`, `expired`.

Each transition must be persisted and observable. Cancellation must reach the engine process and clean up child processes and temporary files. A worker restart must not silently mark an unfinished job successful.

## 5. Resource governance

Each capability manifest declares maximum wall time, CPU threads, memory, disk, output bytes, queue slots and optional GPU requirements. Worker policy may lower but never exceed the declared ceiling. Prevent concurrent jobs from exhausting the host. Provide fair queueing, per-user quotas and clear “resource unavailable” errors.

## 6. Environment isolation

Use separate immutable/pinned profiles for stacks that conflict, for example:
- general Python/scientific utilities;
- PyTorch/ESM;
- JAX/AlphaFold;
- OpenMM simulation;
- chemistry/RDKit and native dependencies.

Exact versions, CUDA compatibility, GPU support and operating-system support must be established by reproducible environment builds and tests. Do not assume a single Python environment can host every engine.

## 7. Android ↔ desktop interoperability

The shared job envelope should include schema version, job ID, capability ID, input artifact references and hashes, typed parameters, requested resource bounds and policy/consent context. Results should include terminal state, output artifacts and hashes, engine/profile identity, provenance and structured diagnostics.

Provide offline package export/import as an early interoperability path. A package must be self-describing, bounded, integrity-checked and safe to inspect before import. Network pairing can follow once identity and threat-model review are complete.

## 8. Repository placement proposal

- `desktop/worker/` — worker service and packaging
- `desktop/profiles/` — profile definitions and lock files
- `desktop/engine-manifests/` — capability and runtime manifests
- `python/molecularis/adapters/` — Python-side engine adapters
- `api/` — versioned job, result, capability and provenance schemas
- `tests/integration/desktop/` — worker/client contract and lifecycle tests
- `docs/security/` — threat model, pairing, data-transfer and retention design

These are proposed paths; create them only when implementation begins and after checking repository conventions.

## 9. Required acceptance

- Authenticated pairing, revocation and TLS identity tests.
- Negative tests for unknown capabilities, malformed parameters, traversal, oversized files, replay and expired jobs.
- Resource-limit, cancellation, restart-recovery and concurrent-load tests.
- Offline package round-trip and hash-tamper tests.
- Data-transfer preview and explicit consent tests.
- SBOM, dependency and licence review.
- Linux reference-host validation followed by explicit Windows/macOS and Android interoperability evidence.
