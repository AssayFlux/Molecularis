# Sequence Engine

Status: Python v1 implementation complete; independent scientific review and contract freeze pending.

## Ownership and scope

Sequence owns typed DNA, RNA and protein records, canonical identity, alphabet validation, parsing, deterministic transforms, sequence statistics, explicit-code translation, pairwise alignment and evidence-aware local reference triage. The canonical service artifact is a Molecularis-owned SequenceDocument, independent of optional parser/alignment packages.

Existing implementation modules are retained and mapped into this service:
- sequence.py: IUPAC alphabets, streaming FASTA/FASTQ, statistics, reverse complement, transcription, k-mers, Needleman-Wunsch and terminal quality trimming.
- genetic_code.py: explicit supported NCBI genetic-code tables and translation.
- sequence_reference.py and sequence_pack.py: bounded, provenance-checked local reference packs, exact matching and explicitly limited local alignment.
- alignment_biopython.py: optional Biopython pairwise-alignment adapter.
- gff3.py and gff3_transcripts.py: structural GFF3 import and CDS reconstruction; neither predicts function.
- orf.py, genome_orf.py, genetic_code_inference.py, blastp.py and hmmer_runner.py: bounded candidate screening and pinned external-tool adapters. These are not equivalent to validated gene annotation or calibrated homology inference.

## Canonical artifact

molecularis.sequence-record.v1 contains identifier, description, sequence_type (DNA, RNA or protein) and normalized sequence. Whitespace is removed and symbols uppercased. Canonical UTF-8 JSON bytes define SHA-256 identity. Sequence artifacts are immutable, content-addressed MSDE artifacts with parent lineage and verified metadata.

## Capabilities

- sequence.validate.v1: verify artifact integrity and alphabet.
- sequence.analyze.v1: deterministic nucleotide or amino-acid composition.
- sequence.reverse-complement.v1: IUPAC DNA reverse complement.
- sequence.transcribe.v1: DNA-to-RNA transcription.
- sequence.translate.v1: explicit NCBI genetic code, reading frame and optional complete-CDS checks.

Each operation executes through a versioned Rulebook against a stored artifact and emits a provenance-linked report. Existing parsers, alignment, reference search and annotation remain available through separately tested Python APIs; they are not conflated into a single opaque operation.

## Scientific boundaries

No gene/function prediction is implied by parsing, ORF enumeration, exact matches, local alignments or candidate code inference. A no-hit is not novelty evidence. Translation requires an explicit table and does not infer organism, transcript, strand, gene boundaries or reading frame. Biopython, Biotite and Parasail remain optional adapters/reference implementations, not mandatory runtime dependencies. No clinical interpretation is provided.


## Shared Agentics scientific foundation

This service participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn** where supported by its declared capabilities. Priority scientific foundations: Discrete mathematics, string/graph algorithms, information theory, probability/statistics, genetics, evolutionary models, sequence alignment and uncertainty in annotation.

Use shared scientific contracts for quantities/units, reference systems, evidence class, uncertainty and provenance. Keep service-specific scientific meanings, algorithms, constraints and validation logic owned here. Agentics may coordinate this engine but cannot override its domain Rulebook. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
