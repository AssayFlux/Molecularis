# Molecularis research workspace

This directory contains templates and, in future, versioned protocols, manifests, annotations, analysis code, and reports.

## Current contents

- [Manuscript template](MANUSCRIPT_TEMPLATE.md)
- [Annotation template](ANNOTATION_TEMPLATE.csv)

## Required discipline

1. Read [research governance](../docs/RESEARCH_GOVERNANCE.md), [evaluation protocol](../docs/EVALUATION_PROTOCOL.md), and [reproducibility standard](../docs/REPRODUCIBILITY.md).
2. Do not invent data, references, approvals, sample sizes, or results.
3. Freeze and identify the app commit, model/provider, prompt, corpus, retrieval configuration, and analysis plan for every reported run.
4. Keep held-out test data separate from prompt and threshold development.
5. Do not commit copyrighted books, private source text, personal data, identifiable participant data, API secrets, or restricted model files.
6. Record null results, failures, exclusions, missingness, and deviations.
7. Label templates and planned studies as such; never present them as completed experiments.

## Suggested future structure

```text
research/
  protocols/
  manifests/
  annotations/
  analysis/
  results/
  artifacts/
```

Only add raw data when consent, ethics, license, privacy, and repository-size constraints permit it.
