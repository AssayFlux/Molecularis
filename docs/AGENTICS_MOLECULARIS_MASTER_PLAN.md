

## 14. Scientific foundation and computational tool ecosystem

Agentics requires a broad scientific foundation spanning mathematics, physics, chemistry, biology, statistics, computer science, engineering, materials science and experimental methodology. The discipline map, cross-cutting concepts and A–N alignment are specified in [SCIENTIFIC_FOUNDATION.md](../services/ai/SCIENTIFIC_FOUNDATION.md).

The candidate computational ecosystem is catalogued in [SCIENTIFIC_TOOL_REGISTRY.md](../services/ai/SCIENTIFIC_TOOL_REGISTRY.md). It includes symbolic/numerical mathematics, units, statistics, Bayesian inference, optimization, graph/geometry computation, scientific ML, physics/chemistry simulation, biological computation, visualization and reproducibility infrastructure. The registry is a selection catalogue, not an assertion that tools are installed or validated.

**Integration rule:** audit and reuse existing Molecularis capabilities first. Integrate tools through versioned adapters with typed schemas, units, provenance, resource limits, license/data-use review, failure behavior and independent verification. Foundational dependencies remain small; GPU/HPC, domain executables, checkpoints and external services are optional isolated capabilities. Never install the entire catalogue into the core runtime.

The mandatory build and operating requirements are defined in [AI_CONSTITUTION.md](../services/ai/AI_CONSTITUTION.md). The staged scientific foundation implementation is defined in [IMPLEMENTATION_ROADMAP.md](../services/ai/IMPLEMENTATION_ROADMAP.md). These documents are subordinate to this Master Plan and do not create a second AI roadmap.

### Scientific foundation implementation order

1. Repository/dependency and A–N capability audit.
2. Typed scientific artifacts, quantities, dimensions, units and reference systems.
3. Scientific knowledge/evidence substrate and provenance.
4. Symbolic and numerical mathematics.
5. Statistics, uncertainty, experimental design and causal reasoning.
6. Constraint solving, optimization, graph, geometry and topology.
7. Selected physics, chemistry and domain simulation adapters.
8. A–N construction and independent verification integration.
9. Governed knowledge acquisition, model evaluation and optional training.

A scientific discipline or package is not considered supported merely because it is listed. Support requires a declared scope, validated method, tests, provenance, limitations and appropriate domain acceptance.
