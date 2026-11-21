# Omics Runtime
Python reference runtime backed by Core/MSDE. Start MolecularisPlatform, register the Omics service, ingest a validated OmicsDocument, then execute an operation-specific Rulebook against immutable artifact IDs.

All matrices are feature rows by ordered sample columns. The caller supplies feature/sample mapping, assay scale and units. Operations are deterministic for fixed inputs and parameters. Artifact loading checks schema, digest, metadata, byte and candidate budgets. There is no implicit conversion between raw counts and normalized/log values.

Example:
    doc = OmicsDocument("study", feature_ids, sample_ids, matrix,
                        assay_type="log_expression", value_unit="log2")
    artifact = ingest_omics(platform, doc)
    report = platform.execute(
        omics_rulebook("differential_welch",
                       parameters={"group_a": [0, 1, 2], "group_b": [3, 4, 5]}),
        {"omics_artifact_id": artifact.artifact_id})

The runtime is in-process and does not provide OS-level isolation or preemptive cancellation. Production deployment requires sandboxed workers and operational resource controls.


## Agentics scientific execution requirements

Validate assay/platform metadata, sample design, feature identifiers, normalization assumptions, units, missingness and resource budgets. Preserve dataset versions/checksums, preprocessing, software versions, parameters, seeds and lineage. Protect sensitive data and fail explicitly on incompatible batches or missing metadata. See ../ai/AI_CONSTITUTION.md.
