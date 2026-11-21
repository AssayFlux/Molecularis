# Architecture and Engineering Decision Log

Record decisions newest-first. Do not silently rewrite historical decisions; supersede them with a new entry.

## DEC-0009 — Authorized Sequence implementation before Molecular scientific freeze
- Status: Authorized by the repository owner in the 2026-11-21 project conversation.
- Decision: Begin B (Sequence) engineering while A (Molecular) remains implementation-complete but awaits independent scientific review and formal v1 freeze.
- Rationale: The owner explicitly directed work to proceed to Step B. This is a scoped sequencing exception, not retrospective acceptance of A.
- Constraints: A remains scientifically unaccepted; B must not claim A acceptance or platform acceptance. B must undergo its own independent scientific review and contract freeze before C. Preserve A's outstanding review as an explicit gate.

## DEC-0008 — Molecularis-native Scientific Data Engine
- Status: Accepted
- Decision: Establish MSDE as a shared Core subsystem for artifact identity/storage, native indexes, bounded query execution, provenance/evidence and Rulebook workflow support.
- Rationale: Scientific Rulebooks need repeated data retrieval, analysis, intermediate artifacts, independent checks, retry paths and auditable final acceptance across services.
- Consequence: Canonical data remains immutable and authoritative; indexes are derived/rebuildable; domain-specific scientific meaning remains in services; implementation proceeds through staged evidence gates.

## DEC-0001 — CORE-only development
- Status: Accepted. All changes are committed directly to CORE; no feature branches or pull requests. Verify HEAD and use non-force updates with expected SHA.

## DEC-0002 — Molecularis-native scientific execution
- Status: Accepted. External tools may be optional references or benchmarks, not mandatory hidden execution dependencies.

## DEC-0003 — Primary languages
- Status: Accepted. C++, Python and Rust are primary; other languages require documented justification.

## DEC-0004 — One service at a time
- Status: Accepted. Complete a service vertical slice before beginning the next, except necessary shared-Core work.

## DEC-0005 — Freeze completed services
- Status: Accepted. Freeze service implementation and documentation after successful completion; changes require authorization and change control.

## DEC-0006 — Device decisions after system completion
- Status: Accepted. Determine supported devices only after total-system build and measurement.

## DEC-0007 — Modular filesystem scaffold
- Status: Accepted. Establish 14 service directories with ENGINE, RUNTIME, RULEBOOK, service metadata, source roots, tests, schemas, data and benchmarks. Scaffolds do not imply implementation; existing Python modules remain in place until verified migration.
