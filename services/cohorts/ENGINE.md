# Cohorts Engine M

Status: implemented v1 engineering slice; independent scientific, privacy and regulatory validation remain deferred.

## Scope
Molecularis owns canonical cohort artifacts, longitudinal visit records, aggregate summaries, categorical stratification and pseudonymous membership overlap. Existing synthetic cohort simulation primitives in `virtual_cohort.py` remain available and are not replaced.

## Data model
A CohortDocument contains unique pseudonymous member IDs, bounded categorical attributes, optional ordered visits and bounded numeric measurements. Inclusion is an explicit caller-provided boolean; the service does not decide eligibility. Source, release, classification and provenance are canonicalized and included in the artifact digest. V1 accepts only `synthetic_non_patient`.

## Operations
- Validate canonical artifact integrity and membership counts.
- Summarize included-member counts, categorical frequencies/missingness, visit counts and descriptive measurement summaries.
- Stratify by one categorical attribute, suppressing groups below a caller-selected minimum cell size (2–1000; default 5).
- Compare two cohorts by pseudonymous member-set intersection, union and Jaccard index; suppress small intersections.

## Algorithms
Categorical summaries use exact frequency counts. Numeric measurement summaries use arithmetic mean/minimum/maximum and explicit non-missing observation counts. Overlap uses set intersection/union and Jaccard = intersection/union (empty union returns 1.0). Stratification suppression is applied before group summaries are emitted. All operations are deterministic and bounded by document, field, visit and MSDE budgets.

## Boundaries
No individual-level rows or member IDs are returned in reports. Small-cell suppression is a disclosure-control heuristic, not differential privacy. Longitudinal data are descriptive only; no mixed models, hypothesis tests, survival analysis, causal inference, recruitment, consent adjudication, clinical eligibility or treatment interpretation is implemented. V1 rejects patient-classified data; callers remain responsible for ensuring the content itself contains no direct identifiers.


## Shared Agentics scientific foundation

Participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. Priority disciplines: Epidemiology, sampling theory, biostatistics, causal inference, experimental design, missing data, privacy-preserving analysis and measurement bias.

Use shared statistical, uncertainty, evidence and provenance contracts while retaining cohort-specific semantics and privacy authority. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
