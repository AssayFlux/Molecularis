# MSDE Core Rulebook

Version: 0.2.0. Status: normative Core rules; a tested subset is implemented in the local Python reference runtime.

Rule classes: MUST, SHOULD (default with recorded exception), MAY (optional).

## Identity and integrity
- MSDE-DATA-001 MUST assign each published artifact a stable logical ID and content digest.
- MSDE-DATA-002 MUST verify content digests at ingest and before trust-sensitive use.
- MSDE-DATA-003 MUST preserve raw inputs as immutable artifacts.
- MSDE-DATA-004 MUST record schema/type, byte length, encoding, provenance and lineage.
- MSDE-DATA-005 MUST reject path traversal and unsafe object references.

## Index correctness
- MSDE-IDX-001 MUST treat indexes as derived, rebuildable structures; canonical artifacts remain authoritative.
- MSDE-IDX-002 MUST bind every query to a consistent catalog/index snapshot.
- MSDE-IDX-003 MUST return explicit completeness status; truncated results MUST NOT be reported as complete.
- MSDE-IDX-004 MUST verify candidates against canonical values for exact queries.
- MSDE-IDX-005 MUST label approximate results and document recall/verification behavior.
- MSDE-IDX-006 MUST invalidate or rebuild indexes when source schema, extractor, normalization or index format changes.
- MSDE-IDX-007 SHOULD retain index build provenance and source snapshot identity.

## Bounded processing
- MSDE-RES-001 MUST bound memory, temporary storage, I/O, CPU, wall time, fan-out, queue depth and retries.
- MSDE-RES-002 MUST use streaming/chunking for payloads larger than configured in-memory threshold.
- MSDE-RES-003 MUST propagate cancellation and release temporary resources.
- MSDE-RES-004 MUST never silently drop records on backpressure or resource exhaustion.

## Transactions and recovery
- MSDE-TXN-001 MUST publish objects and index manifests atomically.
- MSDE-TXN-002 MUST recover safely after interruption at every write boundary.
- MSDE-TXN-003 MUST detect corruption and distinguish recoverable index damage from canonical data loss.
- MSDE-TXN-004 MUST prevent concurrent writers from publishing conflicting snapshots.

## Provenance and evidence
- MSDE-EVD-001 MUST record input digests, method/build versions, parameters, schema versions and output digests.
- MSDE-EVD-002 MUST preserve failed and superseded intermediate runs as immutable evidence. The current executor persists terminal failed-run evidence and successful outputs; partial-run evidence includes completed output artifact IDs.
- MSDE-EVD-003 MUST distinguish prediction, heuristic score, simulation, measurement and independent validation.
- MSDE-EVD-004 MUST record validator identity, outcome, threshold, tolerance and limitations.

## Rulebook execution and AI boundary
- MSDE-RBK-001 MUST validate operation DAGs for missing inputs, cycles, type mismatch and undeclared capabilities before execution.
- MSDE-RBK-002 MUST define preconditions, postconditions, budgets, retry limits and acceptance gates per operation.
- MSDE-RBK-003 MUST invalidate and rerun downstream checks when an upstream artifact changes.
- MSDE-AI-001 MUST treat AI output as an untrusted proposal until validated against contracts and policy.
- MSDE-AI-002 MUST NOT allow AI to bypass mandatory validators, change thresholds silently or forge evidence.
- MSDE-AI-003 MUST record model identity, proposal, policy decision and execution outcome.

## Acceptance
No rule is implemented until it has an automated test or documented reason why automation is impossible, plus review evidence.
