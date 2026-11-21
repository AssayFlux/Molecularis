# Pharmacogenomics Engine

Status: implemented v1 engineering slice; independent scientific review and clinical validation are not claimed.

## Scope
Molecularis owns canonical sample/haplotype artifacts, source-pinned star-allele definition ingestion, strict build matching, and deterministic matching of already-phased complete haplotypes. Existing `pgx.py`, `pharmvar.py`, and reference-bound variant normalization remain supported foundations.

## Supported operations
- Validate synthetic non-patient haplotype-call artifacts.
- Ingest bounded JSON star-allele definition packs with explicit source name, release, HTTPS URL, SHA-256 metadata, license identifier and genome build.
- Match each fully phased and completely called haplotype to the most specific compatible supplied star-allele definition; ties remain ambiguous and no-call states are preserved.
- Preserve definition-pack and sample artifact hashes and lineage through MSDE.

## Scientific boundary
This v1 is allele-definition matching only. It does not perform variant calling, phasing, copy-number inference, structural-variant analysis, transcript mapping, diplotype construction, phenotype translation, CPIC/DPWG guideline interpretation, drug selection, dose calculation, or clinical decision support. A no-match is not proof of reference genotype or absence of an allele. No population frequency assumptions are made.

## Input and output
Sample artifacts use `molecularis.pharmacogenomics-sample.v1`; definition artifacts use `molecularis.pharmacogenomics-definitions.v1`; operation reports use `molecularis.pharmacogenomics-report.v1`. Only `synthetic_non_patient` samples are accepted in v1. Genome build equality is mandatory. Coordinates are positive 1-based positions, and alleles are normalized literal A/C/G/T substitutions.

## Algorithms and assumptions
The matching algorithm requires exact genome-build agreement, exact variant identity and caller-supplied phase/completeness flags. Candidate definitions require all required variants and no excluded variants; the candidate with the largest required-variant set wins only if its star-allele name is unique. Ambiguity is returned, not resolved by ordering. This is a conservative matching heuristic, not a complete implementation of PharmVar or a clinical allele caller.

## Acceptance
See [ACCEPTANCE.md](ACCEPTANCE.md). CI tests cover canonicalization, duplicate-key rejection, digest integrity, definition release pinning, build mismatch, exact matching, ambiguity/no-call behavior and MSDE execution.
