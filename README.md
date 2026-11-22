<!-- Molecularis | AssayFlux -->

<p align="center">
  <img src="Assets/Molecularis%20Guilloche%20Logo.svg" alt="Molecularis — AssayFlux" width="360">
</p>

<p align="center">
  <strong>MOLECULAR SCIENCE · COMPUTATIONAL SYSTEMS · REPRODUCIBLE RESEARCH</strong>
</p>

<p align="center">
  <a href="https://github.com/AssayFlux/Molecularis/actions"><img src="https://img.shields.io/github/actions/workflow/status/AssayFlux/Molecularis/ci.yml?branch=CORE&style=flat-square&label=CI" alt="CI"></a>
  <a href="https://github.com/AssayFlux/Molecularis/blob/CORE/LICENSE"><img src="https://img.shields.io/github/license/AssayFlux/Molecularis?style=flat-square" alt="License"></a>
  <a href="https://github.com/AssayFlux/Molecularis/commits/CORE"><img src="https://img.shields.io/github/last-commit/AssayFlux/Molecularis/CORE?style=flat-square" alt="Last commit"></a>
  <a href="https://github.com/AssayFlux/Molecularis/issues"><img src="https://img.shields.io/github/issues/AssayFlux/Molecularis?style=flat-square" alt="Issues"></a>
</p>

---

## Molecularis

**Molecularis** is a native scientific computing platform by **AssayFlux**, designed to bring molecular and life-science computation into one coherent, extensible system.

Its architecture connects domain-specific services through shared data contracts, a capability registry, a Rulebook-driven workflow runtime and traceable scientific artifacts. An AI planning layer is being developed to translate research requests into validated workflows that use these services.

<table>
<tr>
<td width="50%" valign="top">

### The mission

Build a unified environment where researchers can compose scientific operations across domains without losing the context, provenance or reproducibility of their work.

</td>
<td width="50%" valign="top">

### The principle

**Engines compute. Rulebooks govern. Artifacts preserve evidence. AI coordinates.**

Scientific correctness must be established through domain validation—not inferred from successful software execution.

</td>
</tr>
</table>

## Universal scientific construction direction

**One approach governs all fourteen services:** Understand → Represent → Reason → Construct → Evaluate → Verify → Learn.

Agentics Molecularis is being developed to coordinate a shared Scientific Knowledge Engine, scientific reasoning and construction methods, domain-owned engines and independent verification. Molecularis is not intended to be limited to existing PDB records, X-ray structures, reference databases or pretrained predictors. Those are useful evidence sources and optional methods—not the boundary of what the system may construct.

Every result must distinguish observation, established knowledge, derivation, inference, prediction, simulation, construction, hypothesis and validation. A generated candidate is not automatically physically stable, experimentally realizable or functional. Each service retains its own scientific rules and acceptance criteria.

The governing architecture and phase gates are documented in [Agentics Molecularis Master Plan v2.1](docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md).

## At a glance

<table>
<tr>
<td width="25%" align="center" valign="top">

### 14

**Scientific services**

A–N domain architecture

</td>
<td width="25%" align="center" valign="top">

### 1

**Shared platform**

Core / MSDE foundation

</td>
<td width="25%" align="center" valign="top">

### Agentics

**Intelligence layer**

Goal-directed scientific orchestration

</td>
<td width="25%" align="center" valign="top">

### Rulebooks

**Execution model**

Declared, validated workflows

</td>
</tr>
</table>

## Scientific service cards

<table>
<tr>
<td width="50%" valign="top">

### A · Molecular

Molecular entities, representations, descriptors and molecular operations.

</td>
<td width="50%" valign="top">

### B · Sequence

Biological sequence parsing, transformation, alignment and analysis.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### C · Structure

Molecular structure representation, parsing and structural analysis.

</td>
<td width="50%" valign="top">

### D · Chemistry

Chemical representations, molecular graphs and chemistry operations.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### E · Protein

Protein sequence and protein-science analysis foundations.

</td>
<td width="50%" valign="top">

### F · Genomics

Read/alignment processing and variant-oriented genomics workflows.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### G · DNA/RNA

Nucleic-acid design, analysis and domain-specific rule packages.

</td>
<td width="50%" valign="top">

### H · Simulation

Molecular simulation execution and simulation-oriented workflows.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### I · Kinetics

Reaction networks, kinetic models and numerical integration.

</td>
<td width="50%" valign="top">

### J · Omics

Feature matrices, normalisation and exploratory multi-omics analysis.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### K · Phylogeny

Sequence-derived distance, tree construction and bootstrap support.

</td>
<td width="50%" valign="top">

### L · Pharmacogenomics

Allele-resource foundations and conservative genotype matching.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### M · Cohorts

Synthetic cohort operations, descriptive summaries and privacy-aware aggregation foundations.

</td>
<td width="50%" valign="top">

### N · Workflows

DAG orchestration, registered capabilities and reproducible workflow execution.

</td>
</tr>
</table>

Service registration and implementation do not, by themselves, establish scientific validity. Optional engines, models, reference datasets and their licenses must be checked in the target environment.

## Scientific Knowledge Engine

The initial P1 Scientific Knowledge Engine reference implementation is now part of the `CORE` branch. It provides typed scientific concepts, entities and relations; versioned knowledge packages; equations and laws with typed variables; ordered mechanisms with typed steps; evidence/provenance and source-permission records; SI dimensions and serializable quantities; coordinate references; deterministic queries; and persistence through the Core ArtifactStore with parent lineage.

- [Knowledge Engine contracts and usage](services/ai/KNOWLEDGE_ENGINE.md)
- [Scientific Knowledge Package schema](services/ai/schemas/scientific-knowledge-package-v1.schema.json)
- [Scientific Quantity schema](services/ai/schemas/scientific-quantity-v1.schema.json)
- [P1 acceptance evidence](services/ai/ACCEPTANCE.md)

P1 engineering CI: [run #45046306359](https://github.com/AssayFlux/Molecularis/actions/runs/45045807328) — 769 passed, 12 skipped, 0 failed (including mechanism, law, quantity and artifact round-trip coverage). This is not a claim of comprehensive scientific knowledge or independent scientific validation. P0 platform safety, integration and recovery work remains open; model training is not yet authorized by the phase gates.

## Shared scientific reasoning and construction (P2)

The P2 reasoning foundation is implemented on the current development branch. It adds safe symbolic arithmetic and dimensional derivations, numerical root and linear-system solving, Simpson integration with error estimates, statistical summaries, Welch tests, regression, multiple-testing correction, explicit-prior Bayesian inference, power/sample-size planning, bootstrap and uncertainty propagation, sensitivity and probability calibration, graph topology and unit/frame-safe 3D geometry, bounded constraints/optimization, and construction task/candidate contracts with pre-publication auditing and an evidence-bearing independent-verifier contract.

- [P2 reasoning implementation](python/molecularis/reasoning.py)
- [P2 contract schema](services/ai/schemas/scientific-reasoning-v1.schema.json)
- [P2 tests](tests/test_reasoning.py)

The P2 examples exercise proposer/verifier separation in sequence and chemical-formula representation tasks. They are engineering fixtures, not evidence of chemical validity, molecular stability, experimental realizability or scientific acceptance. P2 engineering CI passed: [run #45047793858](https://github.com/AssayFlux/Molecularis/actions/runs/45047793858) — 792 passed, 12 skipped, 0 failed. P0 platform safety, integration and recovery gates remain open.

## Agentics Molecularis

<table>
<tr>
<td width="50%" valign="top">

### What it does

Agentics Molecularis is the intelligence and orchestration layer above the A–N services. It is intended to interpret a research objective, discover relevant capabilities, compose a Rulebook workflow and present evidence-backed results.

</td>
<td width="50%" valign="top">

### What it does not do

It does not replace scientific engines, execute arbitrary model-generated code or silently treat predictions as facts. Workflow execution is approval-gated; scientific interpretation remains subject to domain review.

</td>
</tr>
</table>

### Research-to-workflow lifecycle

| Stage | Responsibility |
|:---:|---|
| **01 · Understand** | Parse the research objective, constraints and supplied artifacts. |
| **02 · Discover** | Inspect the registered A–N capabilities. |
| **03 · Plan** | Generate a versioned workflow using declared operations. |
| **04 · Validate** | Check contracts, dependencies, artifact references and resource bounds. |
| **05 · Approve** | Require explicit human approval before execution. |
| **06 · Execute** | Delegate operations to service handlers through the Rulebook runtime. |
| **07 · Inspect** | Collect run state, output artifacts and provenance. |
| **08 · Report** | Present results, methods, limitations and unresolved questions. |

<details>
<summary><strong>AI implementation status and technical notes</strong></summary>

The model-agnostic planning and approval-gated execution framework is implemented in `python/molecularis/ai.py`. The A–N platform bootstrap is implemented in `python/molecularis/bootstrap.py`.

Still required for a complete AI product:

- A configured model-provider adapter and deployment credentials.
- Demonstrated artifact compatibility across real scientific service chains.
- Adversarial, prompt-injection and failure-mode testing.
- Evidence-rich report generation and independent AI safety evaluation.

No hosted model or provider credentials are bundled or assumed.

Read: [Agentics Master Plan](docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md) · [Engine](services/ai/ENGINE.md) · [Rulebook](services/ai/RULEBOOK.md) · [Acceptance](services/ai/ACCEPTANCE.md).

</details>

## Platform architecture cards

<table>
<tr>
<td width="50%" valign="top">

### Core / MSDE

Shared scientific data contracts, immutable artifact handling, metadata catalog and provenance foundations.

</td>
<td width="50%" valign="top">

### Capability Registry

Versioned discovery of service operations, schemas and capability metadata.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### Rulebook Runtime

Workflow validation, dependency ordering, execution policy and resource bounds.

</td>
<td width="50%" valign="top">

### Artifact Store

Content-addressed data, integrity checks and parent/lineage relationships.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### Workflow Engine

Operation dispatch, DAG execution and success/failure recording.

</td>
<td width="50%" valign="top">

### Service Runtime

Lifecycle management and bounded execution in the local reference platform.

</td>
</tr>
</table>

### Platform responsibility map

| Layer | Input | Responsibility | Output |
|---|---|---|---|
| AI planner | Research request | Capability selection and workflow proposal | Workflow plan |
| Validator | Workflow plan | Schema, capability and policy checks | Validated plan |
| Rulebook runtime | Approved plan | Dependency-aware execution | Run record |
| Domain services | Typed inputs | Scientific computation | Service results |
| Artifact store | Results and metadata | Integrity, storage and lineage | Traceable artifacts |
| Reporting | Run evidence | Summarise results and limitations | Research report |

## Repository structure

| Location | Responsibility |
|---|---|
| `CORE/` | Shared Core / MSDE architecture and implementation |
| `services/` | Domain service engines, Rulebooks, schemas and manifests |
| `services/ai/` | Agentics engine specification, Rulebook and acceptance gates |
| `python/molecularis/` | Platform runtime, AI planning and A–N bootstrap |
| `python/kinetics/` | Kinetics scientific implementation |
| `api/` · `schemas/` | Versioned API and data contracts |
| `capabilities/` | Capability inventory and registration metadata |
| `data/` · `validation/` | Reference metadata and validation assets |
| `remote-node/` | Remote execution component |
| `scripts/` · `tests/` | Engineering checks, fixtures and automated tests |
| `Assets/` | Project identity and visual assets |

## Engineering status

<table>
<tr>
<td width="50%" valign="top">

### Implemented foundations

- A–N service engineering implementations and registration path (A–N engineering complete; system/scientific acceptance remains separate).
- Core / MSDE local reference runtime.
- Content-addressed artifact storage and integrity checks.
- SQLite WAL metadata catalog.
- Capability registry and Rulebook DAG execution.
- Initial Agentics planning and approval gate.
- Automated engineering CI.

</td>
<td width="50%" valign="top">

### Remaining acceptance work

- Verified end-to-end scientific artifact handoff and provenance continuity across service boundaries.
- Typed artifact handoff and cross-service compatibility evidence.
- Configured AI provider and robust model integration.
- Runtime isolation, failure recovery, backup/restore and platform-wide hardening.
- Independent scientific validation at the university.
- Domain-specific benchmarking and reference-data verification.

</td>
</tr>
</table>

**Current engineering position:** A–N service engineering is recorded complete. Platform-wide integration, recovery/security acceptance and independent university scientific/privacy review remain open. Agentics currently has its initial planner and approval-gated workflow foundation; the shared Scientific Knowledge Engine and general construction/verifier system are roadmap work, not implemented capabilities.

**Latest observed CI:** [GitHub Actions run #44901363429](https://github.com/AssayFlux/Molecularis/actions/runs/44901363429) completed successfully on commit `2b6eced852fb049a81f6b087bb94e5e946047750`. This is engineering evidence, not independent scientific validation.

### Explicit non-claims

| Area | Current position |
|---|---|
| Scientific correctness | Requires independent domain validation. |
| Cross-service integration | Full real scientific chains still need demonstration. |
| Agentics provider | No configured hosted provider is included. |
| Production deployment | Local reference runtime; not certified as distributed production infrastructure. |
| Clinical use | No diagnostic or treatment capability is claimed. |
| External engines | Availability, licensing and versions depend on deployment configuration. |

## Getting started

**Requirements:** Python 3.10+

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e .
pytest
python scripts/check_registry.py
```

Use the repository's service specifications and engineering Rulebook when extending the platform.

## Agentics scientific foundation

Agentics Molecularis is intended to reason and construct through a shared scientific foundation—not through an LLM alone. Its scope includes mathematics, physics, chemistry, biology, statistics, computer science, engineering, materials science and experimental methodology. Shared capabilities include symbolic and numerical calculation, units and dimensional analysis, probability and statistics, uncertainty, optimization, graph/geometry computation, simulation adapters, scientific knowledge and independent verification.

All A–N services follow **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**, while retaining their own scientific rules and acceptance criteria. Existing data and models are evidence sources, not the boundary of possible construction. Every result must preserve assumptions, evidence class, uncertainty, applicability and provenance. Generated candidates are not automatically stable, experimentally realizable or functional.

| Foundation | Purpose |
|---|---|
| Mathematics and numerical methods | Derivation, calculation, solvers and error analysis |
| Physics and chemistry | Governing laws, mechanisms, energetics and simulation |
| Biology and domain sciences | Domain knowledge, biological constraints and interpretation |
| Statistics and uncertainty | Evidence appraisal, inference, experimental design and calibration |
| Computing and optimization | Algorithms, constraints, search, graph and geometric construction |
| Verification and provenance | Independent checks, traceability, reproducibility and limitations |

The candidate package/engine catalogue is not an installation list. Each integration requires a repository gap audit, version/license review, typed adapter, resource controls, provenance and independent tests. See [AI Constitution](services/ai/AI_CONSTITUTION.md), [Scientific Foundation](services/ai/SCIENTIFIC_FOUNDATION.md), [Scientific Tool Registry](services/ai/SCIENTIFIC_TOOL_REGISTRY.md) and [Implementation Roadmap](services/ai/IMPLEMENTATION_ROADMAP.md).

## Project documentation

- [P0 Platform Trust, Safety and Reliability Audit](docs/P0_PLATFORM_AUDIT.md)

<table>
<tr>
<td width="50%" valign="top">

**Direction and architecture**

- [North Star](docs/NORTH_STAR.md)
- [Master Development Plan](docs/MASTER_DEVELOPMENT_PLAN.md)
- [Agentics Molecularis Master Plan](docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md)
- [Future Architecture](docs/FUTURE_ARCHITECTURE.md)
- [MSDE Architecture](CORE/data-engine/README.md)

</td>
<td width="50%" valign="top">

**Execution and governance**

- [A–N Service Roadmap](docs/SERVICE_ROADMAP.md)
- [Master Engineering Rulebook](MASTER_ENGINEERING_RULEBOOK.md)
- [Service Status](docs/SERVICE_STATUS.md)
- [Work Backlog](docs/WORK_BACKLOG.md)
- [Continuous Work Protocol](docs/CONTINUOUS_WORK_PROTOCOL.md)
- [Scientific Validation Standard](docs/SCIENTIFIC_VALIDATION_STANDARD.md)
- [Security Policy](SECURITY.md)
- [AI Constitution](services/ai/AI_CONSTITUTION.md)
- [Agentics Engine](services/ai/ENGINE.md)
- [Agentics Rulebook](services/ai/RULEBOOK.md)
- [Agentics Acceptance](services/ai/ACCEPTANCE.md)
- [Scientific Tool Registry](services/ai/SCIENTIFIC_TOOL_REGISTRY.md)

</td>
</tr>
</table>

## Research collaboration

Molecularis is intended for collaborative development by researchers, computational scientists, software engineers and academic institutions.

Contributions should preserve service boundaries, versioned contracts, provenance and reproducibility. Implementations should include tests, schemas, resource constraints, dependency/license notes and a clear account of what has—and has not—been validated.

## License

See [LICENSE](LICENSE). Third-party libraries, scientific engines, pretrained models, datasets and reference resources may carry separate licenses and terms.

---

<p align="center">
  <strong>MOLECULARIS</strong><br>
  <sub>A scientific systems project by AssayFlux</sub><br>
  <sub>Every result should be traceable. Every workflow should be inspectable. Every claim should carry evidence.</sub>
</p>
