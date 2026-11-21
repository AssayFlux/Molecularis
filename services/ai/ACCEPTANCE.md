# Agentics Molecularis — Acceptance and Phase Gates

This file is the concise acceptance checklist. The authoritative detail and scope live in [AGENTICS_MOLECULARIS_MASTER_PLAN.md](../../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md).

## Existing implementation evidence

Implemented in the repository:
- Model-agnostic planner callable contract and live A–N capability catalog.
- Strict Workflow v1 parsing, DAG/capability validation and operation bounds.
- Exact external input declaration and artifact integrity checks.
- Persisted plan artifact with source input parent lineage.
- Explicit approval gate and execution through existing Molecularis workflow/runtime.
- A–N fresh-runtime bootstrap.

CI evidence previously recorded for the AI implementation: run [#44901363429](https://github.com/AssayFlux/Molecularis/actions/runs/44901363429), commit `2b6eced852fb049a81f6b087bb94e5e946047750`. This is engineering evidence for the then-current implementation, not evidence for the expanded roadmap or scientific acceptance.

## P0 — Hygiene and platform safety

- [ ] Reconcile status/docs against actual branch, commits and CI.
- [ ] Threat model and execution/network policy.
- [ ] OS-level sandbox with CPU/memory/time/disk/process/network limits.
- [ ] Timeout, cancellation and process-tree termination tests.
- [ ] Failed/intermediate run evidence.
- [ ] Artifact-store backup/restore, corruption and crash-boundary tests.
- [ ] CI green and documentation consistent.

**Gate:** all P0 engineering checks pass with linked commit and CI evidence.

## P1 — Sources service

- [ ] Audit and reuse existing source adapters.
- [ ] RCSB PDB, UniProt, AlphaFold DB, InterPro, PubChem and NCBI Entrez connectors.
- [ ] Offline cache, rate limits, retries, bounded downloads and checksums.
- [ ] Source/accession/release/retrieval/license/attribution metadata.
- [ ] Ranked resolver with explicit ambiguity.
- [ ] Recorded-fixture-only CI.
- [ ] Human hemoglobin alpha/beta candidate fixture and stable PDB artifact hash.

**Gate:** fixture resolution and retrieval are reproducible, provenance/license complete and offline CI green.

## P2 — Agentics orchestrator

- [ ] Provider-neutral hosted LLM adapter; deployment-managed credentials.
- [ ] Deterministic mock provider for CI.
- [ ] Capability JSON Schema → constrained tool definitions.
- [ ] Intent/entity/clarification contracts and Workflow v1 planning.
- [ ] Plan explanation, approval bound to plan/input hashes and revalidation at execution.
- [ ] Artifact-only Answer Composer with claim/field citations.
- [ ] Session/run trace, cancellation and bounded iteration controls.
- [ ] At least 50 grounded/adversarial evaluation cases.
- [ ] Prompt-injection, fabrication, privacy, license and unsupported-request tests.

**Gate:** all evaluation cases pass; zero fabricated/unsupported claims in the curated suite; approval/policy tests pass; every scientific report claim resolves to artifacts.

## P3 — Predictor service

- [ ] PredictorAdapter and canonical mmCIF/confidence outputs.
- [ ] Exact model code/weights/data license review.
- [ ] Model/checkpoint/input hashes, seed, parameters and runtime provenance.
- [ ] Predicted namespace distinct from experimental.
- [ ] Local MMseqs2 MSA; remote MSA only opt-in with egress consent.
- [ ] Geometry, clash, Ramachandran and confidence verification.
- [ ] Independent consensus/physics checks where justified.
- [ ] Post-training-cutoff benchmark with leakage-aware split and metrics.

**Gate:** reproducible benchmark and calibration report; provenance and licensing complete; prediction status always explicit.

## P4 — Data and training pipeline

- [ ] Versioned dataset snapshots, checksums and license ledger.
- [ ] Quality filters with documented thresholds.
- [ ] Sequence clustering and time/cluster splits.
- [ ] Synthetic labels kept separate from experimental.
- [ ] Reproducible PyTorch training/evaluation harness.
- [ ] Experiment and model registry artifacts.
- [ ] Manifest-based reproduction test within declared tolerance.

**Gate:** training run reproduced from manifest; leakage checks and license/privacy audit pass.

## P5 — Optional design (disabled until approved)

- [ ] Separate design risk assessment and policy.
- [ ] Design model adapters and candidate artifacts.
- [ ] Proposer → Verifier integration.
- [ ] Biosecurity screening, audit evidence and human-review record.
- [ ] Institutional approval and license review.

**Gate:** screening suite passes and human/institutional approval is recorded. No design release before gate.

## P6 — Generalize across A–N

- [ ] Service-specific proposer/verifier packages.
- [ ] Domain-owned Rulebook acceptance criteria and thresholds.
- [ ] Real cross-service typed artifact handoff and provenance continuity.
- [ ] Deterministic replay, failure propagation and recovery tests.
- [ ] Independent reference and reproducibility evidence per applicable domain.

**Gate:** each domain accepted against its own evidence standard; system integration report documents remaining limitations.

## Required phase report

1. Files changed.
2. Tests added and executed.
3. CI URL and exact commit.
4. Pass/fail/skip/not-tested summary.
5. Open risks and explicit non-claims.
6. Gate state: passed, failed or blocked.
7. Exact next phase (not started until gate passes).

University scientific review remains a separate acceptance activity. No engineering phase or green CI run is a substitute.
