# Security policy

## Current status

Molecularis is an unreleased, research-only application under active development. The R, S and I software scopes have recorded engineering closure; Track P software verification is recorded on its exact implementation revision, while the owner-authorized research-testing scope is open under D-025; clinical deployment and independent security acceptance remain open. Track G's bounded research-only governance software foundation has passed exact-head automated checks (workflow #44098272029, 9/9 jobs); overall governance acceptance remains OPEN and Track U follows it under D-023. Physical-device validation, independent security assessment, qualified privacy/legal determinations, complete third-party clearance and production release authorization remain open. CI builds are unsigned debug artifacts, not a production release.

Never submit real patient, identifiable human-subject or clinical data to this repository, GitHub issues/PRs, test fixtures, CI logs or public attachments. Use synthetic data in CI. Owner-authorized patient-data research testing must remain within the declared institutional approval and the institution-approved environment.

## Reporting

For a suspected vulnerability in this public repository, use GitHub's private vulnerability reporting / Security Advisories feature if enabled for the repository. If it is unavailable, open a minimal public issue containing no exploit details, secrets or sensitive data and request a private reporting route. The private route has not yet been operationally tested and no staffed response SLA is claimed.

## Response

See [Track G operational controls](docs/track-g/operational-controls.md) and the [security verification matrix](docs/track-g/security-verification-matrix.md). Security ownership, private-channel testing, incident tabletop exercises and independent assessment remain open.

## Security commitments for future releases

- Local-first processing and no telemetry by default.
- No genomic or patient data in logs.
- Encryption at rest and authenticated encrypted remote transport before any approved sensitive workflow.
- Dependency and data-pack provenance, pinned versions and license review.
- Threat modelling, consent, access control, incident handling and independent review before sensitive-data features.

This policy is not a security certification, vulnerability-response SLA or authorization to process patient/clinical data.


## Institutional research-testing authorization

The project owner declares institutional ethics approval obtained and authorizes research testing within its scope (D-025, 2026-11-18). The approval reference and protocol copy remain pending attachment; this repository does not claim independent verification. The authorization does not replace device security review, clinical validation or regulatory clearance. Keep patient data out of GitHub, CI and public artifacts.
