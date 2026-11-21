# Genomics Rulebook — genomics-core-v1

Status: **executable engineering rules GEN-001 through GEN-007; university scientific review deferred.**

| Rule | Invariant | Enforcement |
|---|---|---|
| GEN-001 | Genome identifiers, contig identifiers, DNA-IUPAC symbols and total size are bounded | GenomeDocument |
| GEN-002 | Genome artifacts have deterministic canonical JSON, SHA-256 identity and metadata integrity | ingest_genome/load_genome |
| GEN-003 | Assembly statistics are aggregate-only; GC denominator excludes ambiguous bases | summarize_contigs |
| GEN-004 | ORF scanning requires explicit translation table and is candidate enumeration only | scan_contig_orf_candidates |
| GEN-005 | Annotation features must parse as GFF3 v3 and reference genome contigs | parse_gff3 + handler |
| GEN-006 | VCF QC is bounded and does not emit sample IDs or genotype strings | summarize_vcf_qc |
| GEN-007 | Results preserve input artifact lineage and disclose interpretation limits | MSDE executor/report |

## Applicability and exclusions

Coordinates are 1-based inclusive in VCF/GFF3 reports; GFF3 is 1-based inclusive. ORF coordinates and strand follow the existing ORF engine contract. No rule establishes assembly completeness, biological correctness, gene function, variant effect, clinical significance or fitness for diagnosis. Caller-supplied parameters and reference builds must be explicit.
