# Track P — Public-data-only preparation boundary

**Status:** Track P started 2026-11-11 by owner authorization. P0 evidence preparation is active; the formal P0 gate remains NOT APPROVED. This file does not authorize patient or human-subject work.

## Permitted preparation

- Inventory public datasets and authoritative documentation with accession, release/version, licence, retrieval date and SHA-256.
- Design schemas, provenance records, synthetic fixtures and reproducibility scripts.
- Review published methods and document intended use, known bias, missingness and limitations.
- Draft non-clinical research questions and analysis plans without processing identifiable or patient-level data.

## Prohibited before P0 approval

- Importing, storing, transforming or analysing patient/clinical records.
- Human-subject recruitment, consent collection or intervention.
- Individual risk scores, diagnosis, treatment or dosing recommendations.
- Claims of clinical validity, clinical utility or regulatory compliance.
- Connecting clinical systems or enabling a Clinical Mode.

## P0 evidence required

A signed owner decision; jurisdiction-specific legal review; ethics/IRB determination and approval where applicable; qualified clinical/scientific advisers; privacy impact assessment and lawful basis; security threat model and access controls; data minimisation, retention/deletion and incident response; consent/data-use terms; dataset licences; intended-use statement; independent validation plan; and a documented stop/withdrawal process.

## Publication boundary

Public-data research still requires dataset licences, citation, provenance, bias analysis and reproducibility. Public availability does not automatically grant redistribution rights or remove ethical obligations. Any manuscript must distinguish exploratory computational findings from validated biological or clinical conclusions.


## Candidate public source inventory (not approved for intake)

The metadata-only `data/public-dataset-catalog.yaml` now separates candidate source discovery from acquired dataset records. Candidate sources include NCBI Gene, PharmVar, ClinVar and CPIC. Every candidate is explicitly marked `verify_before_intake` and `patient_data: false`; this is not a license approval, data download, or permission to use patient records.

Before adding an acquired entry, pin its exact release/accession, inspect and record the governing license and attribution requirements, retrieve only permitted non-patient content, compute SHA-256 over the exact bytes, document retrieval time and intended research use, and review known bias/limitations. P0 remains blocked. No genotype-to-phenotype interpretation, individual report, guideline recommendation or clinical workflow is implemented by this inventory.


## Engineering progress (2026-11-09)

The public non-patient catalogue now has an automated metadata gate in
`scripts/check_public_dataset_catalog.py`, wired into the Python CI job and covered
by synthetic tests. The gate checks source/licence URLs, unique IDs, non-patient
classification, exact SHA-256 shape, timezone-aware retrieval timestamps, and explicit
evidence before an entry can be marked approved for non-clinical research. It rejects
clinical decision-support and patient-stratification intended-use language.

This advances P-track public-data engineering preparation only. The acquired-entry
catalogue remains empty; no external dataset payload has been downloaded or accepted.
P0 and all patient/human-subject/clinical activities remain blocked.


## Synthetic reference and coordinate contract (2026-11-09)

`python/molecularis/variant_reference.py` adds an immutable reference-contig contract
for non-clinical synthetic fixtures. It binds a sequence to an explicit assembly,
accession, release, contig, 1-based-closed coordinate convention, timezone-aware
retrieval timestamp and SHA-256 over the exact uppercase ASCII sequence bytes.
Reference-checked literal biallelic normalization carries those fields into its
result provenance and explicitly records that interpretation was not performed.

Regression tests cover digest tampering, ambiguous coordinate conventions,
non-synthetic/patient classification, timezone-free timestamps, contig mismatch
and REF/reference disagreement. This is a software contract tested on synthetic
fixtures only; it is not an authoritative genome assembly, validated variant
normalizer, PGx matcher or clinical interpretation engine.


## Owner authorization and current execution state (2026-11-11)

D-022 records the project owner's authorization to start Track P, prepare P0, and build the permitted P1 base. This authorization opens engineering work; it is not a substitute for external legal, ethics, clinical, scientific or regulatory determinations. The P0 gate remains NOT APPROVED until the evidence packet is complete and the owner records a separate gate decision.

Execution: (1) P0 Step 1 prepares intended-use, governance, privacy, security, QMS, risk and validation evidence; (2) P1 Step 1 builds public-source metadata and synthetic reference/normalization contracts; (3) Step 2 audits, tests and fixes the base; (4) P2 interpretation and patient/clinical workflows remain disabled until P0 and their own gates pass.

See p0-evidence-packet.md and implementation-plan.md.
