# Genomics Engine

Status: **implemented engineering baseline v1; scientific review deferred until A–N engineering completion.**

## Ownership and scope

Genomics owns assembly artifacts, contig-level quality summaries, explicit genetic-code ORF candidate scans, GFF3 annotation validation, aggregate VCF QC, and provenance-aware host adapters. Sequence owns general sequence parsing/alignment; Genomics composes it for genome-scale records. DNA/RNA owns molecular sequence design and transcription workflows.

## Native implementation

- Canonical DNA-IUPAC genome document with stable serialization, SHA-256 identity and MSDE artifact lineage.
- Bounded contig statistics (N50/L50, GC over canonical bases, N/ambiguity burden).
- Six-frame complete ORF candidate enumeration with explicit caller-selected NCBI table and aggregate work ceiling.
- GFF3 v3 syntax/hierarchy validation plus genome-contig membership.
- Aggregate VCF QC with sample identifiers/genotype values omitted from results.
- Existing SAM parser, BAM core decoder, optional pysam/HTSlib BAM/CRAM reader, Samtools/BCFtools allow-list, reference normalization, genotype QC, Prodigal/AUGUSTUS and GFF3 transcript reconstruction remain available as separately scoped modules.

## Explicit exclusions

No native read aligner, variant caller, genome assembler, gene caller, phasing engine, structural-variant caller, pathogenicity predictor, contamination estimator, clinical interpretation or population inference is claimed. External executables and model/database packs are not bundled or downloaded. Optional adapters are not equivalent to native Molecularis engines.
