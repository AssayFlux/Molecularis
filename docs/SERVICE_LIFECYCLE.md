# Service Lifecycle and Completion Standard

## Required service package
Each service owns:
- ENGINE.md — scope, algorithms, data flow, invariants, APIs, limitations, acceptance criteria.
- RUNTIME.md — lifecycle, execution model, resources, isolation, errors, cancellation and reproducibility.
- RULEBOOK.md — formal domain rules, constraints, generation/construction procedures, validation and evidence levels.
- service.yaml — machine-readable identity, status, languages, contract versions and dependencies.
- src/cpp, src/python, src/rust — implementation roots; use only languages justified by the design.
- tests, schemas, data, benchmarks — service-owned verification and resources.
- CHANGELOG.md and COMPLETION_RECORD.md — history and freeze evidence.

## Stage gates
A. Discovery: define user/scientific problem, literature, known methods, novelty, risks and licensing.
B. Specification: define scope, exclusions, terminology, inputs, outputs and acceptance tests.
C. Architecture: define modules, dependency graph, language boundaries and data ownership.
D. Engine: implement algorithms with explicit numerical assumptions and error behavior.
E. Runtime: execute, manage resources, cancel, recover and record provenance.
F. Rulebook: make rules explicit, versioned, testable and traceable to evidence.
G. Data: define schemas, identifiers, units, serialization and artifact lifecycle.
H. Verification: unit, property, reference, regression, integration, performance and reproducibility tests.
I. Integration: connect to Core and previously completed services through versioned contracts.
J. Review: independent review of scientific correctness, engineering safety, licensing and completeness.
K. Freeze: publish completion record, tag service version in documentation, and protect paths.

## Rulebook quality
Every rule must include: stable ID, title, statement, rationale, applicability, inputs, constraints, severity, evidence class, validation method, test cases, exceptions, and version. Distinguish normative scientific constraints from heuristics and user-configurable preferences.

## Evidence levels
- E0: proposal or hypothesis; unimplemented.
- E1: implemented; unit tests only.
- E2: verified against controlled reference fixtures.
- E3: independently benchmarked against trusted published or independently implemented references.
- E4: validated on representative real-world datasets with documented limitations.
- E5: externally/experimentally validated where that is scientifically applicable.

Never imply that one evidence level proves a stronger one.

## Freeze and reopening
A frozen service changes only through explicit authorization and a recorded change request. A critical security or scientific defect may trigger expedited remediation, with complete audit trail and regression validation. A reopened service receives a new version and a new completion review.


## Agentics scientific lifecycle integration

Every service must identify which stages of **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn** it supports and document its domain-specific knowledge, equations, assumptions, constraints, units, construction methods and verification thresholds. Shared scientific types and tools may be reused, but domain semantics remain service-owned.

Any AI-proposed scientific operation must pass the pre-generation checks and independent post-generation checks defined in [AI Constitution](../services/ai/AI_CONSTITUTION.md). Service acceptance must record evidence class, uncertainty, applicability domain, provenance, limitations and reference-test evidence. Tool availability or successful execution alone is not scientific acceptance.
