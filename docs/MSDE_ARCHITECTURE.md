# Molecularis Scientific Data Engine

This is the project-level entry point. Normative subsystem specifications live in CORE/data-engine/.

## Purpose
MSDE is the shared data substrate for large scientific datasets and Rulebook-driven multi-stage workflows. It manages artifact identity, immutable storage, native indexes, streaming queries, provenance, intermediate evidence and verification gates.

## Responsibility boundary
- Core/MSDE owns generic artifacts, storage, indexes, query execution, evidence envelopes, resource budgets and recovery.
- Scientific services own domain-specific parsing, normalization, scientific predicates, candidate generation and validators.
- Rulebooks own declared operation graphs, constraints, retry branches and acceptance criteria.
- Future AI components may propose plans but cannot certify scientific correctness or bypass policy.

## Key architecture choice
Use a portfolio of exact and specialized indexes. Keep canonical data immutable and authoritative; treat indexes as rebuildable accelerators. Start with content-addressed artifact storage, exact-key lookup and ordered range indexes. Add biological adapters only when service contracts and test datasets are ready.

## Protein structure example
A structure-generation Rulebook resolves and validates sequence evidence, creates candidate structures, runs independent geometry and quality checks, routes failures through bounded retry branches, revalidates affected outputs, and publishes only an artifact that passes mandatory gates.

Read the Engine, Runtime, Rulebook and Implementation Plan in CORE/data-engine/.


## Agentics scientific knowledge and evidence integration

Agentics consumes MSDE as the shared substrate for versioned scientific artifacts, source/evidence records, derivation traces, intermediate results, verification reports and immutable lineage. MSDE stores and indexes generic artifacts; the Scientific Knowledge Engine defines typed scientific concepts, equations, relationships, assumptions and evidence semantics; domain services own scientific meaning and acceptance.

Scientific artifacts should preserve quantity values and units, coordinate/reference conventions, epistemic class, uncertainty, applicable conditions, source/model/tool versions and parent lineage. Indexes remain derived/rebuildable and cannot become scientific authorities. AI-generated content is untrusted until validated by contracts, service Rulebooks and independent checks. No parallel AI artifact store or workflow executor is introduced.
