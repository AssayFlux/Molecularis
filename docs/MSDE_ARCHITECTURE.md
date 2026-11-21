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
