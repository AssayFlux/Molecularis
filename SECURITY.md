# Security policy

## Supported versions

Security fixes are prioritized for the latest code on the default branch. No release-support or response-time guarantee is made until a formal release policy is published.

## Reporting a vulnerability

Please do not publish exploitable details in a public issue or pull request.

Use GitHub's **Report a vulnerability** flow in the repository's Security tab if private vulnerability reporting is enabled. If it is unavailable, contact the repository maintainers through a private channel listed on the maintainers' GitHub profile and ask for a secure disclosure route. Do not include secrets or user documents in the initial report.

Include, where safe:
- A concise description and affected version/commit.
- Preconditions and reproducible steps.
- Impact and realistic attack scenario.
- A minimal proof of concept that does not access another person's data.
- Suggested mitigation, if known.

Please allow maintainers reasonable time to investigate and coordinate a fix before public disclosure. No bug-bounty program or guaranteed SLA is currently offered.

## Security-sensitive areas

Pay particular attention to local document storage, exported files, Room migrations, app-lock/key handling, provider credentials, network requests, imported prompt/document content, logs, backups, and deletion of derived data.

Never submit API keys, signing keys, passwords, private documents, participant data, or production database files to the repository.
