# Pharmacogenomics Rulebook

Rulebook ID: `pharmacogenomics-core-v1`

Rules are operational constraints for the implemented research slice, not clinical practice guidelines.

| Rule | Requirement | Enforcement |
|---|---|---|
| PGX-001 | Sample data classification must be `synthetic_non_patient`. | Document constructor and schema |
| PGX-002 | Every variant uses a positive 1-based coordinate, literal distinct A/C/G/T alleles and the sample genome build. | `VariantKey` and document validation |
| PGX-003 | Sample and definition pack genome builds must match exactly. | Match operation |
| PGX-004 | A haplotype may be matched only when phase is confirmed. | Matcher returns `no_call_unphased` otherwise |
| PGX-005 | Incomplete calls must abstain. | Matcher returns `no_call_incomplete` otherwise |
| PGX-006 | Definition packs must be release-pinned and carry source, HTTPS URL, SHA-256 and license metadata; unresolved ties remain ambiguous. | Bounded parser and matcher |
| PGX-007 | Outputs must not claim phenotype, drug response, treatment or dosing interpretation. | Report contract, fixed limitations and operation scope |

## Matching semantics
Required variants must be a subset of observed variants; excluded variants must be absent. Among compatible definitions, the largest required-variant set is considered most specific. Equally specific definitions mapping to distinct star-allele labels produce `ambiguous`. The supplied definitions determine the universe of possible matches; incomplete packs can produce false no-match outcomes.

## Versioning
Rule changes require a new Rulebook version and tests. External definition packs must be versioned independently and carry their own release and licensing metadata.


## Agentics scientific rules

- Apply the universal lifecycle under pharmacogenomics domain authority.
- Pre-audit variant normalization, reference build, allele definitions, phenotype rules, source/guideline versions and population applicability.
- Separate observed genotype, inferred diplotype, predicted phenotype, guideline interpretation and clinical action.
- Resolve conflicting evidence explicitly; preserve ancestry/population limitations and uncertainty.
- AI cannot diagnose, prescribe or autonomously recommend treatment. Consequential interpretation requires qualified human/institutional review.
- Preserve evidence provenance, versioned rule evaluation and privacy controls.

Priority disciplines: Genetics, pharmacology, biostatistics, population variation, causal/evidence appraisal, guideline provenance, allele nomenclature and uncertainty.
See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
