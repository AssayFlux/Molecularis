# Track S — Unknown-sequence evidence contract

**Status:** design contract; not a claim that the annotation pipeline is implemented or validated.

## Required input provenance

Every analysis records input SHA-256, format, sequence identifier, length, alphabet, ambiguity count, topology if known, organism/taxon if supplied, source and licence, software/version, database-pack identifiers and hashes, and run timestamp.

## Ordered analysis stages

1. Parse and validate FASTA/FASTQ without silently discarding malformed records.
2. Classify molecule type as nucleotide, protein, ambiguous or unsupported; preserve uncertainty.
3. Run local exact/near-exact similarity search only against explicitly selected, versioned reference packs.
4. Run translated ORF discovery only when the input and selected genetic-code table support it; record all candidate ORFs and strand/frame.
5. Attach gene, protein-family, motif and domain annotations with source accession, coordinates, method, score, thresholds and database version.
6. Reconcile conflicting annotations; retain conflicts rather than selecting an unsupported single answer.
7. Emit an abstention state when evidence is insufficient, references are absent, or competing hypotheses cannot be resolved.

## Output states

- `annotated_with_evidence`: one or more evidence-backed annotations are present; does not prove biological function.
- `multiple_hypotheses`: competing annotations remain.
- `no_supported_match`: selected references did not support a match; does not imply novelty.
- `insufficient_input`: input quality/length/type prevents interpretation.
- `unsupported_scope`: required method or reference pack is unavailable.

## Mandatory annotation fields

`subject_id`, `subject_sha256`, `feature_type`, `start`, `end`, `strand`, `frame`, `genetic_code_table`, `reference_accession`, `reference_version`, `reference_sha256`, `method`, `software_version`, `score`, `e_value`, `identity`, `coverage`, `thresholds`, `evidence_class`, `limitations`.

Coordinates must declare 0/1-based convention and half-open/closed intervals. Null means unknown; it must not be replaced with a guessed value.

## Validation design

Use frozen positive and negative fixtures, taxonomically diverse holdouts, decoys, partial/truncated sequences, low-complexity inputs, ambiguous bases, reverse-complement cases, short ORFs, alternate genetic-code controls and conflicting-reference cases. Report sensitivity, precision, false discovery rate, coverage/abstention rate and stratified confidence intervals. Freeze thresholds before holdout evaluation.

## Novelty and function

The interface must never label a sequence “novel gene/protein” solely because a local search found no hit. Novelty requires a defined search universe and independent review. Functional claims require external experimental evidence and appropriate controls.


## Explicit genetic-code translation (S8 foundation)

`python/molecularis/genetic_code.py` supports explicit translation tables 1, 2, 4,
5 and 11 for canonical DNA/RNA sequences. The caller must select the table.
CDS mode checks table-specific start/terminal-stop codons and rejects internal
in-frame stops. Alternative initiators are represented as methionine only in
CDS mode. Ambiguous bases are rejected rather than guessed.

This primitive does **not** infer the organism's genetic code, locate genes,
identify reading frames/strands, establish gene function, or support every NCBI
translation table. A short unknown sequence or a no-hit is not evidence of a
novel genetic code. Candidate inference now has a bounded, abstention-first software screen over supplied coding-sequence records. It ranks supported tables using internal-stop and optional complete-CDS start/terminal-stop evidence only. It is not an organism-code assignment; organism-specific
positive/negative truth sets, independent comparisons, calibrated confusion
matrices and abstention criteria are available. The host-only
`validation/genetic_code_biopython_reference.py` comparison exhaustively checks
the five implemented tables against Biopython 1.88; it is a transcription
conformance check, not biological validation or inference.
