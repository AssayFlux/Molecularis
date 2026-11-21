# Architecture and Engineering Decision Log

Record decisions newest-first. Do not silently rewrite historical decisions; supersede them with a new entry.

## DEC-0001 — CORE-only development
- Status: Accepted
- Decision: All repository changes are committed directly to CORE. No feature branches or pull requests.
- Rationale: Single authoritative development line.
- Consequence: Verify HEAD and use non-force updates with expected SHA to avoid overwriting concurrent work.

## DEC-0002 — Molecularis-native scientific execution
- Status: Accepted
- Decision: Core scientific execution, runtimes, and Rulebooks are Molecularis-owned. External tools may be optional references or benchmarks, not mandatory hidden execution dependencies.
- Consequence: Independent implementations require scientific evidence, attribution and license review.

## DEC-0003 — Primary languages
- Status: Accepted
- Decision: C++, Python and Rust are primary; other languages require documented justification.
- Consequence: Language boundaries must be explicit and maintainable.

## DEC-0004 — One service at a time
- Status: Accepted
- Decision: Complete a service vertical slice before beginning the next scientific service, with only necessary shared-Core work allowed.
- Consequence: Use lifecycle gates and service completion records.

## DEC-0005 — Freeze completed services
- Status: Accepted
- Decision: Freeze service implementation and documentation after successful completion; changes require explicit authorization and change control.
- Consequence: Maintain protected-path records and regression requirements.

## DEC-0006 — Device decisions after system completion
- Status: Accepted
- Decision: Determine supported devices only after the total system has been built and measured.
- Consequence: Keep architecture device-neutral while recording resource requirements.

## DEC-0007 — Modular filesystem scaffold
- Status: Accepted
- Decision: Establish 14 service directories with ENGINE.md, RUNTIME.md, RULEBOOK.md, service.yaml, source roots, tests, schemas, data and benchmarks.
- Consequence: Directories and documents are scaffolds, not claims of implemented functionality. Existing Python modules remain in their original locations until verified migration.
