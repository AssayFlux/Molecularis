# Molecularis Master Engineering Rulebook

Status: governing development policy; implementation is incremental.

## Ownership
- Molecularis-native engines, runtimes, data models, and Rulebooks are the default.
- External scientific engines and runtimes are not mandatory execution dependencies. They may be used as research references or optional independent benchmarks.
- Implement published methods independently with proper attribution and license compliance.
- Do not claim scientific validity without documented evidence.

## Repository policy
- Develop and commit directly to `CORE` only.
- Preserve Git history and existing assets.
- No feature branches or pull requests.
- Every change must be reviewed against its scope and verified before commit.

## Languages
- Primary: C++, Python, Rust.
- Other languages may be adopted only where a documented technical requirement justifies them.
- Define language boundaries and stable interfaces; avoid duplicate implementations without a clear reason.

## Modular service lifecycle
Build one service at a time: specification → architecture → native engine → native runtime → Rulebook → data/contracts → integration → tests/benchmarks → documentation → completion review → freeze.

A service is not complete merely because files or APIs exist. Its required behavior, runtime, Rulebook, validation, tests, and integration must work.

## File protection
After a service passes its completion review, record its version and freeze its implementation and documentation. Do not modify protected files without explicit authorization, except controlled remediation of urgent security or scientific-correctness defects. Every authorized change requires impact analysis, regression tests, and updated records.

## System sequencing
Complete and validate the total system before deciding supported devices or deployment profiles. Do not prematurely constrain architecture to a device class.

## Quality rules
- No fake implementations, silent external-tool substitution, or unverified accuracy claims.
- Keep provenance, reproducibility, licensing, security, and scientific uncertainty explicit.
- Avoid unnecessary dependencies, duplicated ownership, circular imports, and undocumented contracts.
- Preserve existing assets and useful working code during migration.
