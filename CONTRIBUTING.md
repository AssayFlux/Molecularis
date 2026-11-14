# Contributing to Molecularis

Thank you for helping improve Molecularis. Contributions should improve correctness, maintainability, accessibility, privacy, reproducibility, or user value.

## Before starting

1. Read [README.md](README.md), [NORTH_STAR.md](docs/NORTH_STAR.md), [ARCHITECTURE.md](docs/ARCHITECTURE.md), and the relevant roadmap section.
2. Search existing issues and discussions before opening a duplicate.
3. For substantial changes, open an issue describing the problem, proposed design, alternatives, migration impact, and acceptance criteria.
4. Do not upload copyrighted books, private datasets, API keys, credentials, participant data, or personal information in issues or pull requests.

## Development expectations

- Keep the generic platform independent of any one academic discipline. Domain-specific behaviour belongs in optional, isolated modules.
- Preserve offline functionality unless a change explicitly concerns an opt-in network feature.
- Treat imported documents and retrieved passages as untrusted data, not instructions.
- Keep source provenance and uncertainty visible. Never fabricate citations or imply that generated content is verified.
- Avoid logging document contents, secrets, tokens, or personal data.
- Use additive, migration-safe database changes. Include migration tests for populated databases where applicable.
- Add or update unit, integration, UI, and regression tests appropriate to the change.
- Update architecture, data dictionary, threat model, limitations, and user documentation when behaviour changes.
- Do not claim a feature is complete until its end-to-end acceptance criteria pass.

## Pull request checklist

- [ ] Problem and user impact are explained.
- [ ] Implementation and design trade-offs are documented.
- [ ] Tests are added/updated and results are reported.
- [ ] Database migration and rollback implications are addressed.
- [ ] Accessibility, localization, privacy, security, and offline behaviour are considered.
- [ ] Documentation and roadmap status are updated.
- [ ] Third-party code, assets, models, and datasets have compatible licenses and attribution.
- [ ] No secrets, private user content, or unauthorized copyrighted material are included.

## Research-related contributions

Research code and evaluation changes must identify the evaluated commit, configuration, corpus version, model/provider, and analysis procedure. Preserve negative results and failures. Do not add fabricated benchmark data, participant results, ethics approvals, or citations. See [research governance](docs/RESEARCH_GOVERNANCE.md) and [reproducibility](docs/REPRODUCIBILITY.md).

## Review standard

A review should assess correctness, tests, security/privacy implications, compatibility, accessibility, documentation, and whether claims match observed behaviour. A passing build is necessary for many changes, but it is not sufficient evidence of scientific validity.
