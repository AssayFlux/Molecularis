# Molecularis Alpha Baseline Audit

**Snapshot date:** 2026-11-21  
**Repository:** `AssayFlux/Molecularis`  
**Development branch:** `Alpha`  
**Integration branch / repository default:** `CORE`  
**Original Alpha base:** `741eb5808a99cce9131cc93557253a72c7e1819b`  
**Alpha head at this snapshot:** `a9d65b7d7b0b366f219f6eb510fd75d4f852fea7`  
**CORE head at this snapshot:** `bf72241dff0d0adef2f6f7c243a2619871cba62d`  
**Current merge base:** `b038ef1065dd163108bd591e5e3a7e4c0d7b438d`

## 1. Audit scope and evidence boundary

This is a targeted remote repository inspection and branch comparison, not a full local clone, exhaustive source review, independent security assessment, scientific validation, device test or release approval. File presence and CI configuration do not prove a capability is implemented or production-ready.

## 2. Repository and branch facts

- Repository is public and its default branch is `CORE`.
- Both `Alpha` and `CORE` exist.
- Alpha was originally created from CORE commit `741eb5808a99cce9131cc93557253a72c7e1819b`.
- At this snapshot, Alpha and CORE have diverged: Alpha is 5 commits ahead and CORE is 3 commits ahead of merge base `b038ef1065dd163108bd591e5e3a7e4c0d7b438d`.
- The branches must be integrated through a reviewed merge/PR. Do not force-reset either branch or assume Alpha can replace CORE wholesale.
- No open pull requests were present when this snapshot was taken.
- Alpha documentation-integrity workflow passed on Alpha head: [run 44853634887](https://github.com/AssayFlux/Molecularis/actions/runs/44853634887).
- The main Molecularis validation/Android-build workflow for Alpha head was pending at snapshot time: [run 44853634860](https://github.com/AssayFlux/Molecularis/actions/runs/44853634860). Do not infer success from a pending run.

## 3. Existing implementation foundations observed

The repository contains established Android/Kotlin/Compose and Gradle build material, a Python scientific package and tests, Rust and C++ native components, Node utilities, versioned JSON Schema contracts, capability catalogues, scientific rulebooks, validation plans, provenance/governance records and scientific adapters.

Observed scientific areas include sequence/genomics, protein and macromolecular structure, chemistry/RDKit, docking/Vina, molecular dynamics/OpenMM, enzyme kinetics, omics and pharmacogenomics. Each capability still requires implementation-level and evidence-level verification.

The existing Android stack is migration source material. It must not be deleted until user data, domain logic, contracts, tests, security properties and replacement parity have been assessed.

## 4. Alpha target direction

Alpha defines the intended upscale direction for Molecularis:

- Responsive web application/PWA is the primary client across phone, tablet and desktop.
- Optional desktop packaging must share the same product UI and domain logic.
- Molecularis Node is an explicitly paired, least-privilege local compute connector.
- Hosted workers and institutional/HPC connectors provide policy-controlled execution.
- Browser code is not a trusted sandbox for arbitrary scientific code.
- Preferred scientific/core languages are C++, Rust and Python. TypeScript/JavaScript supports the browser client; SQL and declarative schemas support persistence/contracts.
- Heavy workloads are durable jobs with resource limits, cancellation, logs, artifacts and provenance.
- Research-only posture remains in force. Clinical decision support, clinical claims and deployment remain disabled unless separately authorized, independently validated and legally cleared.

See `docs/alpha/MASTERPLAN.md`, `DEVICE_MATRIX.md`, `LANGUAGE_STRATEGY.md`, `DATA_MODEL.md`, `API_AND_JOB_CONTRACTS.md`, `OPERATIONS_AND_COMPUTE.md` and `SECURITY_AND_VALIDATION.md`.

## 5. Compatibility and migration constraints

- Preserve versioned schema IDs and public API/protocol identifiers until a versioned migration, compatibility tests and deprecation policy exist.
- Treat persisted Android identifiers, user databases, files, preferences, keys and background-job semantics as migration-critical data/contracts.
- Extract domain logic from Android lifecycle/UI dependencies before reuse.
- Maintain the existing Android build/test workflow as a temporary compatibility gate while the cross-device client and compute topology are built.
- Do not conflate scientific terms (for example enzyme kinetics) with obsolete product branding.
- Reassess legacy aliases only after usage inventory and a documented removal window.

## 6. Initial gaps and required M0 work

1. Complete a tracked-file/module inventory with owners, entry points, generated files, build systems and tests.
2. Run exact-head CI for Alpha and CORE and retain run URLs, failures and artifacts.
3. Inspect Python, Rust, C++, Gradle, CMake, Node and workflow manifests at exact commits.
4. Inventory schemas, APIs, capability identifiers, adapters and contract tests.
5. Inventory upstream source versions, licenses, model weights, datasets, binaries and redistribution rights.
6. Produce a capability-by-capability Android-to-all-device parity and user-data migration ledger.
7. Threat-model identity, API, local node, worker isolation, scheduler, artifact service, notebook execution and update/signing.
8. Establish the browser/PWA, API/control-plane, durable job, artifact, local-node and worker implementation baselines before claiming they exist.
9. Map legacy R/S/I/P/G/U work and evidence into the new milestones; retain historical records and explicitly mark superseded plans.
10. Add independent scientific, privacy, security, accessibility, licensing and operational acceptance evidence at the relevant gates.

## 7. Release and claim restrictions

A passing build is not scientific validation, device support, security clearance or release approval. Every scientific capability must declare supported inputs, units/conventions, method and dependency versions, provenance, limitations, reference comparisons and domain review. The platform remains research-use only. No clinical or patient-facing claim is authorized by this plan.

## 8. Audit update protocol

Update this file when branch heads, merge base, workflow evidence, implementation inventory or milestone status changes. Record exact commit SHAs and links. Distinguish **planned**, **implemented**, **tested**, **independently validated** and **released** states. Never convert a target into a completion claim.
