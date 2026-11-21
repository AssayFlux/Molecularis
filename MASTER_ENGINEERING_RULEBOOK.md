# Molecularis Master Engineering Rulebook

Status: governing development policy; implementation is incremental.

## Ownership
- Molecularis-native engines, runtimes, data models, indexing and Rulebooks are the default.
- External scientific engines and runtimes are not mandatory execution dependencies. They may be research references or optional independent benchmarks.
- Implement published methods independently with proper attribution and license compliance.
- Do not claim scientific validity without documented evidence.

## Repository policy
- Develop and commit directly to CORE only.
- Preserve Git history and existing assets.
- No feature branches or pull requests.
- Review every change against scope and verify before commit.

## Languages
Primary languages: C++, Python and Rust. Other languages require documented technical justification. Define language boundaries and stable interfaces; avoid duplicate implementations without reason.

## Modular service lifecycle
Build one service at a time: specification, architecture, native engine, native runtime, Rulebook, data/contracts, integration, tests/benchmarks, documentation, completion review and freeze.

## Scientific data and evidence
- MSDE is the shared data substrate; canonical artifacts are immutable and indexes are derived/rebuildable.
- Every derived result records input identity, method/build, parameters, schema and Rulebook versions, and output identity.
- Exactness, completeness, approximation and uncertainty are explicit.
- Ingestion and query execution are bounded by resource budgets.
- Search, ranking, prediction and AI proposals never replace independent scientific validation.
- Preserve failed and intermediate outputs as traceable evidence where policy permits.

## AI-readiness
Future AI components may propose plans and parameter choices only through declared capabilities and typed contracts. Mandatory validators, resource limits, provenance and authorization cannot be bypassed. AI outputs are untrusted until checked.

## File protection
After service completion, freeze implementation and documentation. Changes require explicit authorization except controlled urgent security/scientific-correctness remediation, with impact analysis and regression tests.

## System sequencing
Complete and validate the total system before deciding supported devices or deployment profiles.

## Quality rules
No fake implementations, silent external-tool substitution or unverified accuracy claims. Keep provenance, reproducibility, licensing, security and scientific uncertainty explicit. Preserve assets and useful code during migration.
