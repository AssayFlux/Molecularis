# Cohorts Rulebook M

Status: operational v1 engineering rules; independent privacy/scientific review pending.

| Rule | Requirement | Acceptance |
|---|---|---|
| COH-001 | Cohort identifiers, member IDs and visit IDs are bounded, non-empty and unique in their scope | Invalid/duplicate identifiers rejected |
| COH-002 | V1 data classification is synthetic_non_patient | Other classifications rejected |
| COH-003 | Attributes, measurements, provenance and visit timepoints are typed, finite and bounded | Invalid values, duplicate keys and non-finite numbers rejected |
| COH-004 | Descriptive summaries include explicit counts and missingness | Tests reconcile member, visit and observation totals |
| COH-005 | Stratified groups below minimum_cell_size are suppressed | No small group summary is emitted |
| COH-006 | Reports contain aggregates, not member-level rows or IDs | Output tests verify aggregate-only results |
| COH-007 | Overlap requires pseudonym IDs in a shared namespace and suppresses small intersections | Set/Jaccard fixtures and suppression tests pass |
| COH-008 | Canonical artifacts retain source, release, provenance and SHA-256 integrity | Round-trip and digest checks pass |

## Assumptions and exclusions
Member identifiers are caller-generated pseudonyms. The service cannot detect identifiers or free text that disclose identity. Minimum-cell suppression is not formal anonymization or differential privacy. Inclusion flags are supplied by the caller and are not eligibility determinations. Numeric summaries are descriptive, not inferential.
