# Architecture and Engineering Decision Log

## DEC-0014 — Python-first implementation; no speculative language ports

- **Status:** Accepted by the repository owner’s explicit direction on 2026-11-21.
- **Decision:** Python is the current implementation language and supported reference for Core/MSDE, all A–N services and Agentics. Do not create C++, Rust or other-language source roots, placeholders, bindings or duplicate algorithms as speculative scaffolding.
- **Rationale:** Keep engineering focused on completing and validating the existing Molecularis-native system rather than carrying forward unused language placeholders.
- **Exception:** An additional language may be proposed only for a concrete, measured capability/performance requirement, with an explicit architecture decision, benchmark evidence, maintenance/security/licensing review and a defined interoperability boundary.
- **Supersession:** This decision supersedes the language targets and source-root assumptions in DEC-0003 and DEC-0007. Those entries remain as historical decisions.

## DEC-0015 — Agentics Master Plan v2.1 is the sole roadmap authority

- **Status:** Accepted documentation authority, 2026-11-21.
- **Decision:** `docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md` v2.1 is the sole Agentics architecture and phase authority. The AI Constitution, Engine, Rulebook, Acceptance and Scientific Foundation Implementation Roadmap are subordinate specifications. Remove duplicate or obsolete phase sequences from the backlog and other planning documents.
- **Rationale:** Keep one consistent scientific knowledge-to-construction architecture and a single P0–P7 execution sequence.
- **Constraint:** A document update does not implement a capability or pass an engineering/scientific acceptance gate.


## DEC-0013 — Shared scientific foundation and governed tool ecosystem for Agentics

- **Status:** Accepted architectural direction; implementation remains gated by the Agentics roadmap.
- **Decision:** Agentics Molecularis uses one shared scientific foundation across A–N, spanning mathematics, physics, chemistry, biology, statistics, computer science, engineering and experimental methodology. Shared capabilities include typed scientific contracts, units/dimensions, knowledge/evidence/provenance, symbolic and numerical computation, statistics/uncertainty, optimization/constraints, graph/geometry, selected simulation adapters, construction and independent verification.
- **Tool policy:** The Scientific Tool Registry is a candidate catalogue, not an install manifest. Audit current Molecularis code and dependencies first; adopt only tools justified by a documented gap, with exact license/version review, isolated adapter, resource controls, provenance and independent tests. Optional external engines remain optional.
- **Governance:** The Agentics Master Plan remains the sole AI architectural authority. The AI Constitution and scientific foundation specifications are subordinate. Every A–N service retains its own scientific semantics, Rulebooks and acceptance thresholds. Pre-generation audit and independent post-generation verification are mandatory.
- **Constraints:** Do not claim listed tools are installed or scientifically validated. Do not train on data without explicit permission and leakage-resistant evaluation. Do not create parallel artifact stores, workflow runtimes or generic per-service AI wrappers. Preserve the approved service sequence and distinguish engineering completion from scientific acceptance.

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
