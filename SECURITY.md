# Security policy

Molecularis is an actively developed scientific-computing engine. It is not approved for clinical use and does not claim independent security certification.

## Reporting

Report suspected vulnerabilities through GitHub's private vulnerability reporting / Security Advisories feature if enabled. If unavailable, open a minimal issue requesting a private reporting route; do not publish exploit details.

## Data handling

- Never commit patient data, identifiable human-subject data, credentials, access tokens or private datasets.
- Use synthetic or appropriately public fixtures in tests and CI.
- Do not place sensitive scientific inputs or outputs in logs, issues, pull requests or build artifacts.
- Treat uploaded files, external executables, model weights and reference databases as untrusted until validated and provenance-checked.

## Engineering expectations

- Pin and review dependencies and external runtime versions.
- Bound execution time, memory, file sizes and generated outputs.
- Verify hashes for externally supplied executables, models and data where supported.
- Avoid shell interpolation; use fixed argument arrays and isolated working directories.
- Preserve provenance and report validation status honestly.
- Do not enable licensed or restricted backends without confirming that the intended use and deployment are authorized.

This policy is not a security certification, response-time guarantee or authorization to process sensitive data.


## Agentics and model/tool security

- Treat user-supplied files, retrieved documents, datasets, model outputs and tool responses as untrusted input; content must never override system policy or service Rulebooks.
- Validate every proposed workflow against registered capability schemas, artifact integrity, authorization, resource budgets and applicable scientific constraints before execution.
- Bind human approval to the exact plan and input identities; invalidate approval if the plan, inputs, tool versions, data-egress scope or resource envelope changes.
- Do not execute model-generated source code or dynamically interpret untrusted Rulebook content.
- Keep provider credentials in deployment secret management; never store credentials in the repository, prompts, artifacts or logs.
- Require explicit data-egress policy for hosted models and external tools. Do not send restricted or sensitive data to a provider without authorization.
- Separate proposing from verification. Model confidence and self-review are not independent scientific evidence.
- Preserve audit records for model/provider identity, prompt/template version, tool calls, approvals, data access, execution parameters and resulting artifacts without logging sensitive payloads.
- Retrieval/index updates, curated knowledge changes, Rulebook changes and model-weight training are distinct operations with separate authorization and provenance.

These controls describe required safeguards; they do not claim that OS-level sandboxing, provider isolation or a complete threat model is already implemented.


## Execution approval contract (P0)

The legacy Boolean approval flag is not an authorization mechanism and is not accepted by the Agentics execution API. Integrations must obtain an `ExecutionApproval` from an institutional identity/approval service, sign the exact canonical bytes returned by `MolecularisAI.approval_payload`, and provide a verifier that authenticates the principal, validates the signature and atomically consumes the approval ID. The signed payload binds the exact workflow, inputs, active capability catalog, policy and resource budget. A local test verifier is not suitable for production. Until an institutional verifier and process isolation are deployed, execute only reviewed handlers with synthetic/public data in a controlled local environment.


## OCI sandbox operating boundary

`OCIContainerRunner` is opt-in and is not wired into the normal Rulebook handler dispatch. It requires a preloaded image referenced by immutable SHA-256 digest and a trusted Docker/Podman daemon. The runner supplies no network, a read-only root filesystem, no-new-privileges, all Linux capabilities dropped, non-root UID/GID, CPU/memory/PID/tmpfs/time limits and only explicit input/output bind mounts. Output mount disk quotas and daemon/rootless configuration must be enforced by the deployment operator. Do not expose a privileged container socket to untrusted users.


## Data classification and egress policy primitive (P0)

The `molecularis.governance` module provides a deny-by-default egress authorization contract. Missing, malformed or unknown data classifications resolve to `restricted`. A transfer requires an exact grant for HTTPS recipient hostname, declared purpose, classification and payload byte ceiling. Credentials in URLs, IP-literal destinations, private/reserved addresses and non-standard HTTPS ports are rejected.

This is a policy decision helper, **not a network firewall**. It does not inspect DNS resolution, redirects, proxy routing, provider SDK behavior or traffic from code that bypasses it. Until every outbound adapter and deployment network boundary enforces an approved policy, external egress remains prohibited for confidential/restricted data. See `python/molecularis/governance.py` and `tests/test_governance.py`.


### Galaxy outbound enforcement follow-up — 2026-11-26

`GalaxyClient` now requires an explicit `EgressPolicy` before sending any REST request or dataset download. The authorization check binds the configured recipient host, purpose, data classification and byte ceiling; absent policy fails closed before transport. Its default opener disables environment-derived HTTP proxies and rejects redirects. Tests cover missing grants, recipient mismatch, pre-transport denial, bounded requests and downloads.

This closes the application-level policy omission for the Galaxy HTTP client only. It is not a host firewall: DNS resolution is not pinned to an approved address, custom injected openers are trusted test/deployment dependencies, and other process/native-tool network traffic is outside this client. Do not treat it as complete platform-wide egress enforcement.
