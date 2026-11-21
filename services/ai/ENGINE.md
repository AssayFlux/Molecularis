# Agentics Molecularis — Intelligence and Orchestration Engine

**Product:** Agentics Molecularis  
**Parent platform:** Molecularis  
**Status:** Initial planner and approval-gated workflow execution implemented; provider, Sources, evidence composer and end-to-end acceptance pending.

## Mission

Translate research objectives into inspectable Workflow v1 plans; discover registered Molecularis capabilities; coordinate approved execution; verify artifact outputs; and compose answers whose scientific claims are traceable to immutable artifacts.

The governing design is **agents propose and coordinate; scientific engines compute; Rulebooks constrain and verify; artifacts preserve evidence; humans authorize consequential actions.**

The full architecture, phase gates and acceptance standard are in [Agentics Molecularis Master Plan](../../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md).

## Existing implementation to preserve

- `python/molecularis/ai.py`: provider-neutral callable planner contract, active capability catalog, strict Workflow v1 parsing, bounded operation count, persisted workflow artifact with input parents, and explicit approval gate.
- `python/molecularis/workflows_service.py`: WorkflowDocument, DAG validation, capability checks, ingestion and Rulebook execution.
- `python/molecularis/bootstrap.py`: fresh-runtime A–N service registration.
- Core/MSDE: artifact store, catalog, lineage, budgets, capability registry and run evidence.

Do not create a parallel workflow parser or duplicate registry/executor.

## Target runtime components

1. Request gateway and input validator.
2. Intent interpreter and entity-resolution coordinator.
3. Sources connectors and provenance/license manager.
4. Capability discovery and JSON-Schema tool adapter.
5. Workflow planner and strict plan validator.
6. Human approval manager.
7. Bounded execution orchestrator.
8. Scientific proposer adapters, including the separate Predictor service.
9. Domain Rulebook verifier and independent-check coordinator.
10. Artifact evidence ledger and claim-grounded answer composer.
11. Audit trace, evaluation harness and deployment policy.

## Request lifecycle

Receive → interpret → resolve/clarify → discover → plan → validate → explain/approve → execute → verify → compose → audit.

Each stage consumes and emits typed contracts or artifact references. A stage cannot bypass upstream authorization or downstream verification.

## Agent topology and autonomy

Begin with one orchestrator. Specialist agents are a later optimization, not a prerequisite. Any future specialist has an explicit role, tool allowlist, task contract, budget, timeout, termination condition and trace. Agents cannot authorize themselves or modify policy.

Autonomy levels:
- L0 Explain available capabilities and evidence.
- L1 Draft a plan; no scientific execution.
- L2 Execute a user-approved bounded workflow.
- L3 Run pre-authorized finite loops with stop conditions and budgets.
- L4 Autonomous consequential actions are out of scope and disabled.

## Provider adapter contract

Provider SDKs remain outside Core. A deployment adapter may use a hosted tool-calling model first and a local model later. It must return strict structured data, record provider/model/version and request metadata, enforce timeout/cost/context bounds, support cancellation where available, redact telemetry and fail closed on malformed output. Secrets are deployment-managed and never committed.

A deterministic mock adapter is mandatory for CI. No provider is reported as configured until a controlled integration test passes.

## Trust and security boundaries

- Model output, fetched text, file metadata, sequences, structure annotations and tool results are untrusted data.
- Never execute model-generated code or arbitrary shell/SQL.
- Only active registered capabilities may be proposed; policy independently authorizes each invocation.
- Validate every input/output against versioned schemas.
- Planning does not execute scientific operations.
- Execution requires explicit approval and bounded runtime policy.
- Network is denied by default; capability-specific egress requires allowlisting and user consent where user data leaves the environment.
- Failures, cancellations, partial outputs and retries remain explicit evidence.
- No model-generated value is scientific evidence.

## Evidence-grounded reporting

The answer composer must build claim records from artifact fields. Each claim includes supporting artifact IDs and field paths, source/method/model version, units, validation status, uncertainty and limitations. Missing or conflicting evidence must be stated as unknown or ambiguous. LLM-generated text may explain artifact-backed facts but cannot create numbers, coordinates, accessions, citations or confidence values.

## Scientific model boundary

LLMs are planners/reporters, not structure predictors or scientific validators. Scientific predictors are separate registered service adapters. Predicted and experimental artifact namespaces are distinct. Predictor provenance includes checkpoint hash, input hash, model version, seed/parameters, confidence outputs and verification evidence.

## Current limitations

- No configured production LLM provider is bundled.
- Sources and Predictor are not yet complete services.
- No complete artifact-grounded report composer or 50-query adversarial evaluation set.
- Real cross-service scientific artifact handoff remains to be demonstrated.
- OS-level isolation and recovery certification remain open.
- No multi-agent delegation, long-term memory or distributed execution is claimed.
- Scientific, clinical, experimental and institutional decisions remain outside Agentics authority.
