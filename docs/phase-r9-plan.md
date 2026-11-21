# R9 — Gene catalogue and precision-medicine research foundations

**Status:** In progress. Clinical/PGx decision support remains disabled.

## Scope
- Broad, expandable cross-domain gene catalogue with source/release metadata.
- Streaming ingestion of all 16 NCBI Gene gene_info columns from plain and gzip-compressed files.
- Search by GeneID, official symbol, synonyms, description, nomenclature and cross-references.
- Future: domain-specific annotation packs, comprehensive PGx gene/allele inventories, star-allele definitions, haplotype/diplotype translation, phenotype evidence, ancestry portability and guideline-version tracking.

## Current source
Implemented in `python/molecularis/catalog.py`. Catalogue ingestion does not elevate evidence status to validated.

## Limitations and gates
- NCBI Gene gene_info is not a PGx allele-definition source.
- No validated star-allele caller, diplotype translator or guideline implementation.
- No patient data or clinical recommendations.
- D-004 adviser checkpoint, P0 legal/ethics/regulatory requirements and qualified clinical review remain mandatory before any patient workflow.

## Exit evidence
Versioned source packs, checksums/licenses, taxonomy and nomenclature coverage reports, allele-definition concordance against approved reference datasets, ancestry/fairness analysis, independent review and provenance.


### R9 PGx foundation increment

Added a versioned JSON star-allele definition schema with mandatory source name/release/HTTPS URL/SHA-256/license/genome build, with the exact release required at import time, normalized literal small-variant keys, required/excluded variant sets and duplicate-definition checks. Added conservative matching for a caller-supplied, fully phased and explicitly complete haplotype; incomplete or unphased calls produce no-call statuses, and tied best definitions remain ambiguous. This is infrastructure only: no PharmVar/CPIC/PharmGKB source data has been imported or licensed, no gene inventory is claimed comprehensive, and there is no diplotype/phenotype translation or clinical recommendation.


### PGx definition foundation

Versioned allele-definition JSON ingestion now requires a pinned source release, source URL, SHA-256, license and genome build. Matching requires an explicitly complete and already phased haplotype. No authoritative PGx content is bundled; gene coverage is not comprehensive and diplotype/phenotype translation is not implemented.


### PharmVar source adapter

Added a parser for PharmVar's documented nine-column TSV haplotype/variant format. It verifies the original TSV byte-stream SHA-256, requires an exact pinned database release, preserves RefSeqGene/LRG/chromosome reference accessions and 1-based sequence coordinates, handles the explicit REFERENCE/*1 sentinel and matches only exact, complete, already phased variant sets. It does not remap locus coordinates to GRCh37/GRCh38, infer phase/CNV/hybrid alleles or translate diplotypes/phenotypes. No bulk PharmVar dataset has yet been downloaded or bundled.


### PharmVar TSV parser hardening — 2026-11-09

The nine-column importer now rejects duplicate/empty normalized header names, non-nine-column headers, and short/extra-width data rows instead of allowing DictReader to silently overwrite or discard fields. Added regression tests for malformed row widths, duplicate headers, ambiguous exact allele matches, phase/completeness abstention and reference-accession mismatch. This is parser integrity coverage only; it does not validate biological allele interpretation or supply authoritative PGx content.


### NCBI gene_info strict row/date validation — 2026-11-09

The streaming 16-column parser now requires exactly 16 tab-separated fields (not merely at least 16), preventing silent acceptance of schema drift or appended fields. Modification dates are parsed as real calendar dates rather than checked only for eight digits. Added regressions for extra columns and impossible dates. This remains source-file parser validation, not a complete NCBI release import or comprehensive catalogue coverage claim.
