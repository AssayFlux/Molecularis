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
