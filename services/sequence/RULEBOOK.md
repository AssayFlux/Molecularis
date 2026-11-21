# Sequence Rulebook

Status: SEQ-001–SEQ-005 implemented as executable v1 checks; independent scientific review pending.

Rulebook ID: sequence-core-v1, version 1.0.0.

| Rule | Requirement | Acceptance behavior |
|---|---|---|
| SEQ-001 | Typed record identity | Non-empty bounded identifier; supported sequence type; immutable canonical record |
| SEQ-002 | Alphabet admissibility | DNA/RNA IUPAC or declared extended protein alphabet only |
| SEQ-003 | Canonical identity | Uppercase, whitespace-free canonical JSON; deterministic SHA-256 |
| SEQ-004 | Artifact integrity | Stored schema/media type, digest and metadata must agree before execution |
| SEQ-005 | Explicit operation semantics | Preconditions enforced; genetic code and frame are explicit/defaulted by documented API; unsupported biology is not inferred |

## Evidence classes

- Established deterministic software behavior: alphabet validation, normalization, byte identity, statistics, complement/transcription and explicit-table translation.
- Heuristic/candidate outputs: ORF enumeration and genetic-code candidate inference.
- External adapter outputs: Biopython/Parasail alignments, BLASTP and HMMER profile search; retain tool version, parameters, reference/profile hashes and licensing evidence.
- Imported assertions: FASTA/GFF3/reference-pack annotations remain source assertions unless independently validated.
- Unknown: gene function, novelty, pathogenicity, clinical significance and biological context not established by these operations.

## Preconditions and postconditions

All sequence artifacts validate before persistence. Every operation accepts exactly one verified sequence artifact and emits a JSON report with input digest, operation ID, Rulebook version and limitations. Invalid inputs and unsupported transformations fail closed. No-hit and abstention are explicit; never relabel them as negative biological evidence.

## Known limits

The v1 runtime exposes validation, statistics, reverse complement, transcription and translation. Existing parsers, alignment, reference-pack, ORF, GFF3 and homology adapters remain available as separately tested Python APIs. They are not promoted to production capabilities until their own scientific acceptance criteria and external dependency contracts are reviewed.


## Agentics and shared scientific foundation rules

1. Apply **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn** without weakening this service's domain rules.
2. Before construction, audit objective, inputs, units, assumptions, constraints, evidence/source versions, applicability and resource/safety limits.
3. Use governing scientific laws, equations, mechanisms and algorithms with explicit assumptions and validity domains; distinguish empirical correlations from established laws.
4. Independently verify outputs using appropriate domain invariants, reference methods, statistical checks or experimental evidence. The proposer is never the sole verifier.
5. Preserve evidence class, uncertainty, limitations and provenance. A candidate is not automatically stable, experimentally realizable or functional.
6. External tools are optional registered adapters; verify exact versions, licenses, schemas, resource limits and verification strategy.

Priority foundations: Discrete mathematics, string/graph algorithms, information theory, probability/statistics, genetics, evolutionary models, sequence alignment and uncertainty in annotation.

See ../ai/AI_CONSTITUTION.md, ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
