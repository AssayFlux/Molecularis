# Research readiness, evidence, and publication boundary

## Purpose

This document separates implemented software behaviour from empirical claims. Molecularis is an evolving research prototype with a biochemistry-oriented legacy feature set and an initial multi-subject implementation. Any publication must describe the exact evaluated commit, configuration, corpus, model, and environment—not the roadmap.

## Current evidence in the repository

| Area | Evidence currently present | What it does not prove |
|---|---|---|
| Android build | GitHub Actions workflow for unit tests, emulator instrumentation, lint, and debug APK assembly | Production readiness or physical-device compatibility |
| Data persistence | Room/SQLite, SQLCipher integration, additive migrations | Complete migration correctness or resistance to every threat |
| Subject model | SubjectWorkspace and ProfessorProfile entities, active selectors, create/edit flows | Full lifecycle management, explicit cross-subject comparison, or complete isolation of every artifact |
| Subject isolation | Subject-filtered library, Knowledge Pool, chat retrieval, projects, lessons, schedules; overlapping-vocabulary Room instrumentation test | Populated legacy migration safety until migration tests pass; complete security assurance |
| Document ingestion | PDF import, page-aware extraction/OCR, resumable processing, extraction audits | OCR accuracy across languages, layouts, and devices |
| Knowledge organization | Topic hierarchy, aliases, human review, topic-passage links | Correctness or completeness of topic classification |
| Retrieval | Subject-filtered local lexical retrieval; optional embedding components for conversation attachments | Retrieval relevance, evidence recall, or superiority over baselines |
| AI prompting | Bounded prompt with subject and professor preferences; local and remote paths share constructed context | Model factuality, citation precision, or learning benefit |
| Provenance | Successful chat answers store provider/model, professor profile, prompt version/hash, source-set hash, retrieval config | Complete provenance for every lesson, diagram, slide, export, or schedule |
| Teaching outputs | Lesson outlines, slides, biochemical diagrams, narration, exports | Pedagogical validity, generality across disciplines, or learning gains |
| Privacy | Local-first architecture, encrypted database, explicit optional providers | Independent security audit or legal compliance certification |

## Remaining implementation gates

1. Add populated-database migration tests from supported prior schema versions and verify encrypted-copy row counts, FTS state, and all foreign keys.
2. Verify active subject/profile persistence across process death and physical-device restarts.
3. Complete workspace archive/delete and profile lifecycle management with safe data retention semantics.
4. Add explicit opt-in cross-subject comparison; never silently broaden retrieval.
5. Scope and version saved diagrams and all generated artifacts; attach complete source/model/prompt provenance.
6. Add EvaluationRun records and exportable machine-readable run manifests.
7. Make biochemical diagram tooling an optional domain pack and add independently validated non-biochemistry modules.
8. Add source rights metadata, retention controls, and user-facing confirmation for authorized processing.
9. Run device acceptance for low-memory, large corpus, offline, accessibility, localization, and encrypted migration conditions.

## Publication-quality study requirements

- Specify the research question, hypotheses, primary and secondary outcomes, comparator, inclusion/exclusion criteria, sample-size rationale, and analysis plan before data collection.
- Freeze the application commit, model/provider version, prompt version/hash, corpus manifest, retrieval configuration, and evaluation set.
- Separate development, validation, and held-out test data at source-document or source-family level, not merely by randomly splitting adjacent chunks.
- Use domain experts to create gold labels and adjudicate disagreements. Report expert roles, rubric, training, and agreement statistics.
- Evaluate ingestion, retrieval, evidence support, factual correctness, pedagogical quality, usability, accessibility, privacy, and performance as separate constructs.
- For learner outcomes, use a controlled or otherwise justified design, validated instruments, pre/post measurement, delayed retention where feasible, and appropriate statistical analysis.
- Obtain institutional ethics review/approval or a documented determination before collecting human-participant data. Consent, privacy, withdrawal, and data retention must be explicit.
- Report null, negative, and failure results. Do not cherry-pick successful prompts or examples.

## Governance and reproducibility

Supporting standards are documented in [RESEARCH_GOVERNANCE.md](RESEARCH_GOVERNANCE.md), [REPRODUCIBILITY.md](REPRODUCIBILITY.md), and [LIMITATIONS.md](LIMITATIONS.md). These are policies and plans, not proof that a study, audit, or validation has been completed.

## Claim language

Allowed when verified for the evaluated build:
- “The prototype implements page-aware PDF extraction and a human-reviewed source index.”
- “The app scopes library, conversation, and teaching records by an active subject workspace.”
- “The system records prompt and source-set digests for successful chat answers.”

Not justified without additional evidence:
- “Molecularis improves learning outcomes.”
- “Molecularis is scientifically accurate.”
- “Molecularis outperforms other AI tutors or RAG systems.”
- “Molecularis is secure/private by design” as an absolute guarantee.
- “Molecularis supports every subject.”
- “Professor profiles are separately trained AI models.”

## Minimum submission package

- Exact source commit and release artifact hash.
- Architecture and data-flow diagrams.
- Software and model inventory with licenses.
- Dataset/corpus manifest and rights statement.
- Evaluation protocol, annotation guide, and de-identified results.
- Statistical analysis and limitations.
- Threat model, privacy statement, and ethics determination.
- Reproducibility instructions and environment versions.
- A clear distinction between implemented, experimentally evaluated, and planned features.
