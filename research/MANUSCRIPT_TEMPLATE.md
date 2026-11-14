# Manuscript template — Molecularis

> This is a reporting scaffold, not a completed scientific paper. Replace every bracketed field with verified information. Do not invent sample sizes, results, model versions, ethics approvals, or citations. Follow the target journal's reporting checklist and discipline-specific standards.

## Proposed title

Molecularis: Design and Technical Evaluation of an Offline-First, Source-Grounded, Multi-Domain Learning Workspace

## Abstract

**Background:** [Problem and evidence gap.]

**Objective:** [Primary objective and research question.]

**Methods:** [Study design, exact app commit/version, devices, corpus, models, comparator, participants if applicable, measures, and analysis.]

**Results:** [Report only observed results, denominators, effect sizes, confidence intervals, and failures.]

**Conclusions:** [Conclusions bounded by the design and evidence; include limitations.]

**Keywords:** retrieval-augmented generation; mobile learning; offline-first; knowledge management; educational technology; provenance; human-in-the-loop.

## 1. Introduction

- Describe the educational/research problem and relevant literature.
- Explain limitations of current approaches using current, properly cited sources.
- State the intended contribution and distinguish technical novelty from product integration.
- State research questions and hypotheses.

## 2. System design and implementation

### 2.1 Intended users and use cases
[Define user roles and supported disciplines for the evaluated release.]

### 2.2 Architecture
[Describe Android app, local persistence, document ingestion, OCR, Knowledge Pool, retrieval, AI provider adapters, teaching outputs, and optional backend.]

### 2.3 Corpus ingestion and knowledge curation
[Formats, inclusion criteria, rights basis, extraction pipeline, chunking, topic organization, human approval, failure handling.]

### 2.4 Retrieval and generation
[Exact algorithm, chunk size/overlap, top-k, scoring, thresholds, prompt template, model/provider/version, context budget, abstention behaviour.]

### 2.5 Subject and professor configuration
[Describe what is implemented in the evaluated build. If first-class subject scoping or multiple profiles are not implemented, state this clearly and do not claim them.]

### 2.6 Privacy, security, and safety
[Data flow, local/cloud boundaries, encryption, secrets, threat model, deletion, consent, high-impact-domain boundaries.]

## 3. Methods

[Use the protocol in docs/EVALUATION_PROTOCOL.md. State the study design, corpus partitions, gold-standard creation, annotator qualifications, sample-size rationale, measures, analysis plan, ethics review, and deviations.]

## 4. Results

Report:
- Build/test status and device matrix.
- Ingestion fidelity and extraction failure cases.
- Retrieval relevance by subject and query type.
- Claim support and citation precision/recall.
- Expert teaching-quality ratings and agreement.
- Subject isolation tests, if implemented.
- Usability and device performance.
- Learner outcomes only if a suitable human-participant study was conducted.
- Negative, null, and unexpected findings.

## 5. Discussion

Interpret results against each research question. Compare only with fair, reproducible baselines. Discuss error patterns, applicability, limitations, and threats to validity.

## 6. Limitations

Discuss corpus representativeness, OCR and language limitations, model/provider variability, device coverage, evaluation sample size, expert-rating subjectivity, offline model availability, and unimplemented roadmap items.

## 7. Conclusion

Summarize what the evaluated build demonstrates and what remains unproven. Avoid broad efficacy claims unsupported by the design.

## Availability and declarations

- Source repository and immutable commit:
- Release artifact and SHA-256:
- Dataset/corpus availability and rights restrictions:
- Code and analysis scripts:
- Ethics approval/determination:
- Consent:
- Funding:
- Conflicts of interest:
- Author contributions:
- Acknowledgements:
