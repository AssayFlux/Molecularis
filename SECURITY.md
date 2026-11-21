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
