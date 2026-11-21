# Omics Rulebook — omics-core-v1
- **OMI-001 — Canonical identity:** schema, identifier, feature IDs, sample IDs, assay type and units are explicit; SHA-256 identifies exact content.
- **OMI-002 — Matrix shape:** unique feature rows and ordered sample columns; rectangular matrices capped at 2,000,000 cells.
- **OMI-003 — Numeric domain:** values are finite and non-negative; raw-count matrices contain integer-valued entries.
- **OMI-004 — Scale honesty:** CPM/NB2 require raw counts; Welch requires normalized/log-expression values; diversity requires raw counts/abundance.
- **OMI-005 — CPM admissibility:** every sample library total must be positive.
- **OMI-006 — CLR admissibility:** pseudocount is finite and positive; transformed columns are centered.
- **OMI-007 — Differential design:** Welch groups are disjoint valid indices with at least two samples each; NB2 condition is binary and design estimable.
- **OMI-008 — Cross-omics alignment:** correlation requires identical ordered sample IDs; constant vectors are rejected.
- **OMI-009 — Evidence and limitations:** reports retain input digest, method, Rulebook and limitations; exploratory p-values are not clinical or causal evidence.
