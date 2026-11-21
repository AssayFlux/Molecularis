# Phylogeny Runtime K

Status: implemented v1 using the shared local MSDE platform runtime.

## Lifecycle
1. Construct and validate immutable PhylogenyDocument.
2. Canonically serialize and ingest as an immutable artifact with digest, dimensions, alignment-method metadata and optional parent lineage.
3. Load only matching media/schema artifacts; verify digest and metadata before computation.
4. Execute one registered capability through a Rulebook operation.
5. Return a schema-versioned report with exact input digest, operation, operation-specific rules and limitations.

## Resource controls
- 3–500 taxa; at most 2,000,000 aligned sites and 5,000,000 total alignment cells.
- Artifact byte and candidate limits enforced by MSDE Budget.
- Bootstrap replicates are bounded by 1,000 and the active candidate budget.
- No external binary, remote service or network call is required.

## Reproducibility and errors
Canonical JSON and SHA-256 identify the input. Algorithms are deterministic for fixed inputs; bootstrap uses a caller-supplied integer seed. Invalid dimensions, alphabet, artifact metadata, saturated distances, inadequate sites and negative NJ limbs fail explicitly. Failed replicate counts are reported, never silently treated as successful.

The current MSDE handlers run in-process. These limits are application-level bounds, not an OS sandbox or preemptive CPU/memory isolation.
