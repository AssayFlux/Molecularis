# Genomics Runtime

Status: **implemented Python reference runtime integration; native C++/Rust and distributed execution are not implemented.**

The service registers five deterministic MSDE capabilities: `genomics.validate.v1`, `genomics.assembly-qc.v1`, `genomics.orf-scan.v1`, `genomics.annotation-validate.v1`, and `genomics.variant-qc.v1`.

Genome artifacts are immutable JSON payloads with media/schema identifiers, content digest, metadata integrity checks and parent lineage. Handlers enforce the shared execution byte/record/base budgets; individual algorithms impose additional hard limits. Results are stored by the shared Rulebook executor and linked to input artifacts.

VCF QC accepts a bounded text parameter and returns aggregate counts only. It verifies VCF contig names against the genome artifact, but deliberately does not claim REF-allele/reference-build validation. GFF3 input is bounded and every feature seqid must exist in the genome artifact.

BAM/CRAM and Samtools/BCFtools integrations remain optional local pysam/HTSlib adapters. CRAM requires an explicit local FASTA; network retrieval is never implicit. Host process execution is not part of the native MSDE handler path.


## Agentics scientific execution requirements

Validate genome/reference build, coordinate conventions, allele normalization, sample metadata, units and resource budgets before processing. Preserve dataset/source versions, tool versions, parameters, checksums, environment and lineage. Enforce data permissions/privacy and explicit missing-reference failures. AI output cannot bypass service policy. See ../ai/AI_CONSTITUTION.md.
