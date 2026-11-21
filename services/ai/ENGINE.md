# Agentics Molecularis — Intelligence, Reasoning and Orchestration Engine

**Status:** Initial planner and approval-gated Workflow v1 execution implemented. Universal scientific knowledge, construction and verification architecture is the governing target.

Read the [Universal Scientific Reasoning & Construction Master Plan](../../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md).

## Mission

Translate research objectives into inspectable, reproducible workflows that use the shared scientific knowledge and reasoning foundation and coordinate all relevant Molecularis services A–N. The system should support the full lifecycle: understand, represent, reason, construct, evaluate, verify, classify and report.

## Permanent principle

**Understand → Represent → Reason → Construct → Evaluate → Verify → Learn.**

This applies to every service, not only Structure/Protein and not only work based on PDB, X-ray structures or pretrained predictors. External observations and models are evidence or optional methods; they are not the boundary of what Molecularis may construct.

## Authority boundaries

- Agentics interprets objectives, discovers capabilities, plans, coordinates approved execution and composes evidence-grounded reports.
- The Scientific Knowledge Engine stores typed, versioned scientific concepts, relations, equations, mechanisms, constraints, assumptions, evidence and applicability domains.
- Domain services own scientific meaning, algorithms, construction methods, thresholds and verification Rulebooks.
- Core/MSDE owns artifact identity, capability registry, workflow execution, budgets, provenance and lineage.
- LLMs are optional replaceable planners/reporters, not scientific authorities or substitutes for executable reasoning.
- Humans retain authority over consequential, clinical, experimental and institutionally governed decisions.

## Existing implementation to preserve

- `python/molecularis/ai.py`: provider-neutral callable planner, active capability catalog, strict Workflow v1 validation, bounded operations, persisted plan artifacts with input lineage and explicit approval.
- `python/molecularis/workflows_service.py`: DAG validation, capability resolution and Core Rulebook execution.
- `python/molecularis/bootstrap.py`: A–N registration.
- Core/MSDE artifact store, catalog, lineage, budgets and capability registry.

Do not create a parallel workflow parser, registry, artifact store or executor.

## Target components

1. Request and input validator.
2. Intent/task interpreter and ambiguity resolver.
3. Scientific Knowledge Engine and versioned knowledge packages.
4. Typed knowledge representation, units, equations and constraints.
5. Reasoning/derivation coordinator.
6. Construction strategy and candidate generator contracts.
7. Evaluation, optimization and uncertainty contracts.
8. Domain Proposer and independent Verifier adapters.
9. Capability/schema discovery and Workflow v1 planner.
10. Approval-gated bounded orchestrator.
11. Immutable evidence ledger and claim-grounded answer composer.
12. Audit, benchmark and adversarial evaluation harness.

These are logical modules; do not split them into processes without measured justification.

## Lifecycle

Receive → interpret/clarify → represent → retrieve relevant knowledge where needed → reason/formulate → plan → validate → explain/approve → execute → evaluate → independently verify → classify epistemic status → compose artifact-grounded report → audit.

## Construction modes

- Reconstruction from supplied observations or constraints.
- Generalization from established models with explicit assumptions.
- Exploration of a bounded candidate space for unobserved possibilities.

Every task declares objectives, constraints, method, budget, stopping criteria, uncertainty and verification plan. A constructed candidate is not automatically physically stable, experimentally realizable or functional.

## Evidence and reporting

Every claim maps to immutable artifact IDs and field paths. Record source/knowledge versions, equations, assumptions, methods, model/runtime versions, units, transformations, uncertainty and verification evidence. Report missing or conflicting evidence as unknown/ambiguous. Never invent scientific values, citations, laws or validation outcomes.

## Security and autonomy

Fetched text, model output and scientific annotations are untrusted data. Never execute generated code or shell. Tools are active registered capabilities only. Network is denied by default. Execution requires approval bound to the exact plan and inputs. Specialist agents remain deferred until a single orchestrator is safe and evaluated. L4 consequential autonomy is disabled.

## Current limitations

No complete SKE, universal construction framework, configured production LLM provider, evidence-grounded report composer, full real cross-service scientific handoff, 50+ adversarial evaluation suite, OS-level sandbox or recovery certification is claimed. The existing AI implementation is an initial engineering foundation, not a completed autonomous discovery system.


## Scientific foundation and tool integration

The shared AI scientific foundation spans mathematics, physics, chemistry, biology, statistics, computer science, engineering, materials science and experimental methodology. The discipline map and service-specific priorities are defined in [SCIENTIFIC_FOUNDATION.md](SCIENTIFIC_FOUNDATION.md); candidate packages and external engines are listed in [SCIENTIFIC_TOOL_REGISTRY.md](SCIENTIFIC_TOOL_REGISTRY.md).

### Logical module boundaries

- Scientific contracts and typed artifacts.
- Scientific knowledge and evidence packages.
- Units, dimensions and reference systems.
- Symbolic and numerical mathematics.
- Statistics, uncertainty and experimental design.
- Physics, chemistry and biology adapters.
- Graph, geometry, topology and optimization.
- Simulation and construction orchestration.
- Independent verification and evaluation.
- Tool registry, manifests and adapter loading.

These are logical boundaries, not empty directories to create in advance. Implement a module only when its contract, use case and tests are defined. Integrate with existing Core/MSDE artifact storage, provenance, capability registry and Rulebook runtime; do not create parallel stores or executors.

### Scientific tool integration contract

Every tool adapter declares stable capability ID, domain, exact tool/version, license and data terms, input/output schemas, units/reference conventions, dependencies, hardware/resource needs, network behavior, determinism, failure/cancellation behavior, provenance fields, verification strategy and known limitations. Optional executables and GPU/HPC engines run in appropriately isolated environments. Missing optional dependencies fail explicitly and never produce fabricated success.

### Mandatory generation gates

Before construction, run the pre-generation audit: objective and input validation, knowledge/version and source checks, unit/dimension validation, assumptions and boundary-condition checks, domain applicability, safety policy and resource feasibility. After construction, run independent domain verification and record evidence, uncertainty, limitations and decision state. The proposer is never the sole verifier.

See [AI_CONSTITUTION.md](AI_CONSTITUTION.md), [SCIENTIFIC_FOUNDATION.md](SCIENTIFIC_FOUNDATION.md), [SCIENTIFIC_TOOL_REGISTRY.md](SCIENTIFIC_TOOL_REGISTRY.md) and [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md).
