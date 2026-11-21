# Pharmacogenomics Runtime

Status: implemented v1 local reference runtime.

## Lifecycle
1. Validate the typed sample document and its strict schema.
2. Validate and parse the caller-supplied, release-pinned definition pack before artifact publication.
3. Store both artifacts through MSDE with SHA-256 content identity and metadata.
4. At execution, verify artifact media type, schema identifier, digest, metadata and resource budget.
5. Require the exact named artifact inputs for the requested capability.
6. Match only calls marked both phase-confirmed and call-complete; preserve abstentions.
7. Emit a deterministic report containing input hashes, rulebook identity, operation-specific rule IDs and explicit limitations.

## Resource controls
- Definition packs: at most 2 MiB, 10,000 definitions and 1,000 variants per definition (parser defaults).
- Sample records: at most 500 haplotype calls and 20,000 total variants.
- Runtime artifact reads respect Core byte and candidate budgets.
- No network access, external tool execution, implicit database download or dynamic code loading occurs.

## Errors and reproducibility
Malformed input, duplicate JSON keys, invalid allele symbols, digest/metadata mismatch, genome-build mismatch and budget exhaustion fail closed. Matching is deterministic for fixed artifacts and parameters. Source provenance is supplied by the caller and is not independently authenticated by this runtime.

## Security and data handling
v1 rejects patient-classified data and is intended for synthetic non-patient engineering fixtures only. Do not place patient identifiers or protected health information in artifacts or metadata. The runtime is an in-process trusted handler and is not an OS-level sandbox.


## Agentics scientific execution requirements

Validate variant/build, allele nomenclature, diplotype/phenotype evidence, guideline version, population context, consent/privacy and intended-use boundaries before execution. Preserve source/guideline versions, software and rule versions, parameters and lineage. Consequential interpretation requires qualified human review. See ../ai/AI_CONSTITUTION.md.
