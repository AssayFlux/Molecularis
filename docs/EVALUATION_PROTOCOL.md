# Molecularis evaluation protocol (pre-study specification)

## 1. Objective

Evaluate the technical reliability and educational usefulness of a source-grounded, offline-first learning assistant. Treat this as a protocol template: populate and freeze the fields below before testing. Do not report results until data have actually been collected.

## 2. Research questions

- RQ1 — Ingestion: how accurately does the system preserve document text and page locations?
- RQ2 — Retrieval: how often does retrieval return the expert-identified evidence passages for a query?
- RQ3 — Grounding: are generated claims supported by retrieved passages, and are citations exact?
- RQ4 — Subject isolation: does a query retrieve only material from its active subject unless cross-subject search is explicitly requested?
- RQ5 — Teaching quality: how do qualified reviewers rate correctness, completeness, clarity, level fit, and pedagogical structure?
- RQ6 — Usability/performance: can target users complete core tasks, and what are latency, memory, battery, and failure characteristics?
- RQ7 — Learning outcomes: does use of the system change immediate comprehension or delayed retention relative to a suitable comparator?

## 3. Study registration fields

- Protocol version/date:
- Repository commit SHA:
- App version/build variant:
- Device model, Android version, RAM, storage:
- Model/provider name and exact version/hash:
- Prompt-template version/hash:
- Retrieval configuration (lexical/semantic weights, chunk size, overlap, top-k, filters):
- Corpus manifest version/hash:
- Study site and responsible investigator:
- Ethics committee / IRB review number or determination:
- Preregistration URL/identifier, if applicable:

## 4. Dataset construction

Create three disjoint source-level partitions:
- Development: may be used to tune chunking, prompts, retrieval, and interface.
- Validation: used to select among predeclared configurations.
- Held-out test: opened only after configuration freeze.

Do not split neighboring chunks from the same book across partitions. Prefer distinct books, editions, or source families to reduce leakage. Record title, author, edition, publisher, year, language, page count, file SHA-256, rights/permission basis, scan/digital origin, and exclusion reason. Keep copyrighted content private; publish metadata and permitted derived annotations only.

For each test query, annotate:
- Subject/workspace ID and scope.
- Query text, intended task, difficulty, and expected answer type.
- Relevant document IDs and exact page/passage IDs.
- Required facts and unacceptable errors.
- Whether answerable from the supplied corpus.
- Gold answer or scoring rubric.
- Annotator IDs/roles and adjudication notes.

## 5. Technical metrics

### Ingestion fidelity
- Character Error Rate (CER) and Word Error Rate (WER) against manually transcribed page samples.
- Page assignment accuracy: proportion of extracted passages mapped to the correct source page.
- Page coverage: pages with usable extracted text / total pages.
- Duplicate-page detection precision/recall against manually labelled duplicates.
- Processing time, peak memory, failure rate, recovery success, and battery consumption.

### Retrieval
For query q, let Rq be the retrieved top-k passages and Gq the gold relevant passages.
- Recall@k = |Rq ∩ Gq| / |Gq|.
- Precision@k = |Rq ∩ Gq| / k.
- MRR = mean reciprocal rank of the first relevant passage.
- nDCG@k using graded expert relevance labels.
Report macro averages and per-subject/per-language strata with confidence intervals.

### Evidence and citation quality
- Claim support rate: supported factual claims / all verifiable factual claims.
- Citation precision: citations that support the attached claim / citations emitted.
- Citation recall: supported claims with at least one valid citation / all claims judged supportable by the corpus.
- Citation resolution: citations resolving to the correct document and page.
- Abstention quality: correct abstentions on unanswerable queries and incorrect abstentions on answerable queries.
Use two independent expert annotators and adjudicate disagreements.

### Teaching quality
Rate each output on a predeclared ordinal rubric (e.g., 1–5): factual correctness, completeness, conceptual sequencing, clarity, learner-level fit, source alignment, uncertainty communication, and usefulness of examples/questions. Report item-level distributions, inter-rater agreement (weighted kappa or ICC as appropriate), and adjudication.

### Subject isolation
Create adversarial pairs with overlapping vocabulary across subjects. Measure:
- Cross-subject leakage rate = queries with any unauthorized foreign-subject passage in top-k / all test queries.
- Scope enforcement accuracy = correctly scoped queries / all test queries.
- Cross-subject opt-in correctness for explicitly requested comparisons.

### Usability and performance
Task completion, time on task, critical error rate, System Usability Scale (if appropriate), crashes, ANRs, p50/p95 latency, peak RAM, battery drain, and offline completion rate. Record device and OS strata.

## 6. Learner study design

Choose a design suited to the claim. A randomized parallel-group or counterbalanced crossover design may be appropriate; avoid assuming that one is automatically valid. Define:
- Population, recruitment, eligibility, sample-size/power calculation, and attrition assumptions.
- Comparator (e.g., usual study materials, conventional search, or another tool) and equalized time/resources.
- Primary outcome and validated assessment instrument.
- Secondary outcomes: delayed retention, transfer/application, learner confidence calibration, workload, usability.
- Intervention duration, training, allowed assistance, and adherence measures.
- Blinding of outcome assessors where feasible.
- Statistical model, covariates, missing-data strategy, multiplicity correction, effect sizes, and confidence intervals.

Do not claim a learning effect from satisfaction ratings or a small uncontrolled demonstration.

## 7. Bias, safety, and integrity

Predeclare prompt selection and stopping rules. Preserve failed runs and model errors. Avoid evaluating only handpicked questions. Record provider outages, rate limits, model updates, and manual interventions. For high-impact subject matter, have domain experts define unacceptable errors and review safety procedures. Do not expose participants to unreviewed high-risk advice.

## 8. Reproducibility package

Archive:
- Source commit and signed release artifact SHA-256.
- Build toolchain and dependency lock/version data.
- Device/environment matrix.
- Model files or immutable model identifiers and licensing terms.
- Prompt templates, retrieval settings, and configuration hashes.
- Corpus manifest and annotation schema.
- De-identified query set, gold labels, analysis scripts, and raw aggregate results where legally permitted.
- Deviations from protocol and a complete limitations statement.

## 9. Reporting

Report denominators, missingness, exclusions, confidence intervals, inter-rater agreement, per-subject performance, subgroup performance, negative results, and all protocol deviations. Separate technical performance from learning outcomes.
