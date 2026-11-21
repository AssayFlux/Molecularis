# Architecture and Engineering Decision Log

Record decisions newest-first. Do not silently rewrite historical decisions; supersede them with a new entry.

## DEC-0012 — Universal Knowledge-to-Construction principle across A–N
- Status: Authorized by the repository owner on 2026-11-21.
- Decision: All fourteen Molecularis services follow the shared lifecycle **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. Agentics Molecularis coordinates this approach; a shared Scientific Knowledge Engine and reasoning/construction contracts support it; each service retains domain-specific scientific knowledge, algorithms, Rulebooks and verification criteria.
- Rationale: Molecularis must progress beyond retrieval and reproduction of known examples toward principled construction and evaluation of new candidates, including possibilities not present in current datasets.
- Constraints: This is not limited to molecular X-ray/PDB/structure prediction. External databases, observations and pretrained models are optional evidence/methods, not architectural prerequisites. Distinguish observed, established, derived, inferred, predicted, simulated, constructed, hypothesized and validated results. Mathematical validity, physical plausibility, experimental realizability and function are separate claims. Preserve human/institutional authority and independent domain verification. Implement the v2.0 roadmap sequentially with evidence gates; do not claim planned capabilities as implemented.


## DEC-0011 — Name and govern the Agentics Molecularis intelligence system
- Status: Authorized by the repository owner on 2026-11-21.
- Decision: The AI intelligence/orchestration layer is officially named **Agentics Molecularis**. Molecularis remains the parent scientific computing platform. The detailed roadmap is governed by `docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md`.
- Rationale: “Agentics” communicates goal-directed agent engineering: interpreting objectives, planning bounded work, coordinating tools and services, evaluating outcomes and preserving human authorization.
- Constraints: Agentics is not a scientific engine or source of truth. Existing AI planner, Workflow v1, Core/MSDE and A–N services must be reused. Execute the P0–P6 phases sequentially with explicit gates. Predictions remain distinct from experimental observations; reports must be artifact-grounded; no design capability before its separate safety gate.

## DEC-0010 — Defer university scientific review until A–N engineering completion
- Status: Authorized by the repository owner on 2026-11-21.
- Decision: Complete the A–N engineering implementation sequence first. Conduct university-level scientific review, reference comparisons, formal validation and service contract freezes after all fourteen services are engineered.
- Rationale: Centralized university review is the owner's chosen validation process.
- Constraints: Engineering completion must be reported separately from scientific acceptance. Preserve limitations, test evidence and provenance records; do not claim scientific validation or production readiness before the university review.

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
