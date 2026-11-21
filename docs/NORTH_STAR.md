# Molecularis North Star

## Mission

Build a trustworthy, modular, Molecularis-native scientific computing system that can represent, analyze, generate, simulate, validate and connect molecular and biological knowledge across scientific domains—with every result traceable, reproducible, bounded and honest about uncertainty.

## What success looks like

A researcher can express a scientific objective through explicit, versioned rules. Molecularis can plan the work, discover admissible native capabilities, execute bounded operations, preserve intermediate evidence, independently validate results and publish immutable artifacts with complete provenance. The same work can be replayed or audited later.

## Non-negotiable principles

1. **Scientific integrity over appearance.** Never claim a capability, accuracy, validation level or completion state without evidence.
2. **Native ownership.** Molecularis owns its domain models, core algorithms, runtime contracts, data substrate and Rulebooks. External tools are optional adapters, references or benchmarks unless a decision explicitly approves otherwise.
3. **One service at a time.** Complete and freeze each A–N service step before implementation of the next.
4. **Rules are executable contracts.** Rulebooks define admissibility, constraints, generation strategies, validation, evidence and acceptance—not informal prompts or untestable prose.
5. **Engine and Rulebook are separate.** Engines provide deterministic, composable capabilities; Rulebooks specify which capabilities to apply and how outputs are accepted.
6. **Evidence is first-class.** Inputs, methods, builds, parameters, data versions, random seeds, intermediate outputs, failures and validation results remain traceable.
7. **Bounded execution.** CPU, memory, GPU, disk, I/O, wall time, concurrency and candidate counts are explicit budgets.
8. **Fail visibly.** Incomplete, approximate, unsupported, uncertain or failed results must never masquerade as exact and complete results.
9. **Independent validation.** A method does not validate itself by repeating the same calculation. Use independent methods, implementations, datasets or experimental evidence when appropriate.
10. **AI is subordinate to policy.** AI may propose plans or parameters; it cannot bypass typed contracts, authorization, resource budgets, scientific validators or acceptance thresholds.
11. **Interoperability without lock-in.** Stable language-neutral contracts connect C++, Python and Rust; other languages need documented justification.
12. **Preserve before replacing.** Audit existing source, tests, assets, data and public interfaces before migration or deletion.
13. **Privacy and licensing by design.** Data use, model weights, reference databases and dependencies require provenance and terms review.
14. **Measured deployment.** Device and deployment targets follow total-system profiling, not speculation.

## Product boundary

Molecularis is the scientific engine and its supporting runtime/data/rule infrastructure. Interfaces and product applications may consume it through stable APIs, but must not become hidden dependencies of scientific execution.

## Long-term capabilities

- Native molecular and biological data models and generators.
- Rulebook-driven sequence, structure, chemistry, protein, genomics, nucleic-acid and simulation workflows.
- A scalable scientific data substrate with immutable artifacts, indexes, query planning and evidence lineage.
- Reproducible workflow execution with validation gates, retries and deterministic replay.
- Optional acceleration and AI-assisted planning behind verifiable policy boundaries.
- Research-grade diagnostics, benchmarks, auditability and extensibility.

## Definition of trust

A result is trustworthy only to the extent that its scope, inputs, methods, parameters, provenance, limitations and validation evidence are known. Molecularis must expose that evidence rather than collapse it into a single confidence label.


## Agentics scientific foundation

Agentics Molecularis coordinates a universal knowledge-to-construction lifecycle across every A–N service: **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. It is supported by a shared scientific knowledge/evidence substrate and reusable mathematical, statistical, unit-aware, optimization, geometry and simulation capabilities. Domain services remain authoritative for their scientific meanings, equations, constraints, Rulebooks and acceptance criteria.

The long-term ambition includes constructing candidates beyond known reference examples. This does not mean that generated candidates are automatically correct: mathematical validity, domain validity, physical plausibility, stability, experimental realizability and demonstrated function require distinct evidence. Pre-generation audit, independent post-generation verification, provenance and uncertainty are mandatory. See the [Agentics Master Plan](AGENTICS_MOLECULARIS_MASTER_PLAN.md) and [AI Constitution](../services/ai/AI_CONSTITUTION.md).
