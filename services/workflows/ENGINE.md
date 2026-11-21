# Workflows Engine N

Status: implemented v1 native orchestration slice; independent scientific validation of invoked capabilities remains owned by their services.

## Scope
Molecularis-native workflow contracts and orchestration over registered MSDE capabilities. A workflow is a bounded DAG of capability invocations with explicit named inputs, outputs, parameters, version and provenance. Existing FASTA/FASTQ QC helpers and Galaxy REST adapter are retained as independent utilities/connectors.

## Execution
Declare external inputs and operations; validate identifiers, references, uniqueness, operation count, parameters and acyclicity; resolve capabilities through ServiceRegistry; convert the graph to a Core Rulebook; execute through the deterministic topological executor. MSDE records input/output artifact lineage and run evidence.

## Determinism and failure
Canonical sorted-key JSON and stable topological ordering provide reproducibility. Core records failed runs and completed outputs. No implicit retries are performed because handlers may have side effects. Parallel execution, conditional branching, loops, scatter/gather and compensation transactions are not in v1.

## Boundaries
No scientific algorithm is silently delegated to Galaxy. The optional Galaxy adapter is separately operated. Workflow validation checks graph contracts and capability registration, not scientific correctness.


## Shared Agentics scientific foundation

Participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn** as the orchestration service. Priority disciplines: Computer science, graph algorithms, formal methods, constraint solving, scheduling/operations research, provenance, reproducibility, resource optimization and secure execution.

This service coordinates typed scientific work but does not own or redefine domain science. Use shared contracts, evidence classes, uncertainty and provenance while preserving each service's authority. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
