# Reproducibility and experiment record standard

**Purpose:** make each reported Molecularis result traceable to an exact build, dataset, model, configuration, and analysis. This document defines a target standard; it does not assert that existing experiments meet it.

## 1. Immutable run identity

Assign every evaluation a unique run ID. Record:
- Repository URL, branch, full commit SHA, release/tag, dirty working-tree state.
- Build workflow/run URL, build toolchain, JDK, Gradle, Android Gradle Plugin, Kotlin, SDK levels, dependency versions, and build variant.
- APK/AAB filename, byte size, SHA-256, signing status, and artifact location.
- Device manufacturer/model, Android version/API, RAM/storage, locale, language, battery/power conditions, and network state.
- Date/time in UTC and operator or automated runner identity (pseudonymous where appropriate).

Never identify an artifact only by a mutable filename such as `app-debug.apk`.

## 2. Corpus manifest

Each source record should include a stable source ID, bibliographic metadata, file format, byte size, SHA-256, language, acquisition date, rights basis, permitted use, and source version. Derived records should include extraction/OCR engine and version, page count, extraction timestamp, chunking parameters, passage IDs, and known extraction warnings.

Keep raw restricted source files outside public repositories. Publish a manifest with hashes and metadata only when permitted. Record corpus inclusion/exclusion rules and train/development/test partitions before evaluation.

## 3. Model and prompt manifest

Record exact provider and model identifiers, version or retrieval date, runtime/library version, local model artifact checksum when distributable, license, inference location (local/cloud), prompt-template version/hash, system policy version, generation parameters, context limit, and fallback behaviour.

If a provider does not expose a stable model version, state that limitation and record the request date and any provider metadata available. Do not imply bit-for-bit determinism when the provider is nondeterministic or changes the model behind an alias.

## 4. Retrieval manifest

Record:
- Retrieval implementation and commit.
- Lexical index and tokenizer configuration.
- Embedding model/version and vector dimensions, if used.
- Chunk size, overlap, page handling, filters, top-k, scoring, thresholds, reranker, and tie-breaking.
- Subject/workspace scope and explicit cross-subject settings.
- Source approval state and excluded source IDs.
- Query set version and gold-label version.

Report retrieval metrics separately from answer-generation metrics.

## 5. Evaluation data and annotation

Use stable IDs rather than names or personal identifiers. Preserve the annotation rubric, annotator qualifications, training procedure, independent ratings, adjudication, and inter-rater agreement. Keep a clear separation between development and held-out test data. Do not tune prompts or thresholds on the final test set.

For each answer, retain the query ID, retrieved passage IDs/ranks/scores, generated answer, cited evidence, model/run ID, latency, token/resource metrics where available, abstention/error status, and expert annotation. Avoid storing sensitive prompts or raw personal content in public artifacts.

## 6. Analysis and reporting

Version analysis scripts and dependencies. Report denominators, confidence intervals, effect sizes, missing data, exclusions, subgroup/subject results, and uncertainty. Preserve failed runs and negative/null results. Explain all post-hoc analyses. Do not compare systems under unequal corpora, models, time budgets, or access to tools without explicitly accounting for those differences.

## 7. Suggested repository layout

```text
research/
  README.md
  protocols/
  manifests/
  annotations/
  analysis/
  results/
  artifacts/
```

Only commit data and artifacts whose licenses, consent, privacy, and size permit redistribution. Keep generated private data and large model files out of Git.

## 8. Run record template

Create one machine-readable record per run (JSON/YAML/CSV) with fields equivalent to:

| Field | Description |
|---|---|
| run_id | Stable unique experiment identifier |
| protocol_version | Dated protocol and analysis plan |
| commit_sha | Full evaluated Git commit |
| artifact_sha256 | Exact APK/AAB digest |
| environment | CI and device configuration |
| corpus_manifest_sha256 | Corpus manifest digest |
| model_manifest | Provider/model/runtime details |
| prompt_hash | Prompt/template version or hash |
| retrieval_config | Index, chunking, filters, top-k, thresholds |
| dataset_version | Query and gold annotation versions |
| started_at_utc | Run start timestamp |
| deviations | Deviations and rationale |
| analysis_commit | Exact analysis code commit |

## 9. Publication package

Before submission, archive the protocol, run record, corpus manifest, annotation schema, analysis code, environment details, artifact checksum, and permitted aggregate results. Provide access restrictions and a contact route for data requests where raw data cannot be shared. Reproducibility does not require violating copyright, consent, or privacy.
