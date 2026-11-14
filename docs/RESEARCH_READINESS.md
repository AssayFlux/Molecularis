# Research readiness, evidence, and publication boundary

## Purpose

This document distinguishes what the repository currently demonstrates from what must be measured before a research paper can claim effectiveness. Molecularis is a multi-domain design direction with a substantial biochemistry-oriented implementation. A publication must describe the exact evaluated build, not the aspirational roadmap.

## Current evidence available in the repository

| Area | Evidence currently present | What it does not prove |
|---|---|---|
| Android build | GitHub Actions workflow for unit tests, lint, debug APK | Production readiness or physical-device compatibility |
| Data persistence | Room/SQLite, SQLCipher integration, migrations | Security against every threat or complete migration correctness |
| Document ingestion | PDF import, page-aware extraction/OCR, resumable processing, extraction audits | OCR accuracy across languages, layouts, and devices |
| Knowledge organization | Topic hierarchy, aliases, human review, topic-passage links | Correctness or completeness of topic classification |
| Retrieval | Local lexical retrieval; optional embedding components | Retrieval relevance, evidence recall, or superiority over baselines |
| AI prompting | Bounded conversation prompt; discipline-neutral system prompt foundation | Model factuality, citation precision, or subject-isolation in production |
| Teaching outputs | Lesson outlines, slides, diagrams, narration | Pedagogical validity or learning gains |
| Privacy | Local-first architecture, encrypted database, explicit optional providers | Independent security audit or legal compliance certification |

## Critical implementation gaps before claiming a multi-subject platform

1. Add a first-class Subject/Workspace entity with stable ID, display name, description, discipline taxonomy, language, audience defaults, and lifecycle.
2. Associate every book, processed Knowledge Pool record, passage, topic, conversation, professor profile, lesson, and evaluation run with a subject/workspace ID.
3. Make subject selection explicit at import and in all subject-scoped screens.
4. Support multiple professor profiles per subject, with independent role instructions, audience, teaching goals, tone, safety constraints, and prompt version.
5. Enforce subject isolation in database queries and retrieval. A query in subject A must never retrieve subject B material unless the user explicitly invokes cross-subject search.
6. Migrate existing data to a default legacy subject without data loss.
7. Replace discipline-specific assumptions in generic workflows; retain specialist features as optional modules.
8. Add end-to-end tests for two subjects with deliberately overlapping vocabulary and verify zero unintended cross-subject retrieval.
9. Add exportable provenance for each answer/lesson: source-set hash, document checksum, page/passage IDs, retrieval scores/configuration, provider/model version, prompt template version, timestamp, and user review state.
10. Add a clear source-rights and retention workflow. Users must confirm that they have authority to process each imported source.

## Publication-quality study requirements

- Specify the research question, hypotheses, primary and secondary outcomes, comparator, inclusion/exclusion criteria, sample-size rationale, and analysis plan before data collection.
- Use a frozen application commit, model/provider version, prompt version, corpus manifest, and evaluation set.
- Separate development, validation, and held-out test data at the source-document or source-family level, not merely by randomly splitting adjacent chunks.
- Use domain experts to create gold labels and adjudicate disagreements. Report expert credentials/roles and agreement statistics.
- Evaluate ingestion, retrieval, evidence support, factual correctness, pedagogical quality, usability, accessibility, privacy, and performance as separate constructs.
- For learner outcomes, use a controlled or otherwise justified design, validated instruments, pre/post measurement, delayed retention where feasible, and appropriate statistical analysis.
- Obtain institutional ethics review/approval or a documented determination before collecting human-participant data. Consent, privacy, withdrawal, and data retention must be explicit.
- Report null, negative, and failure results. Do not cherry-pick successful prompts or examples.

## Claim language

Allowed before empirical study:
- "The prototype implements page-aware PDF extraction and a human-reviewed source index."
- "The system is designed to support offline, source-grounded study workflows."
- "The repository includes unit tests for specified components."

Not justified without additional evidence:
- "Molecularis improves learning outcomes."
- "Molecularis is scientifically accurate."
- "Molecularis outperforms other AI tutors or RAG systems."
- "Molecularis is secure/private by design" as an absolute guarantee.
- "Molecularis supports every subject" or "multiple professors per subject" until end-to-end subject scoping and profile management ship and pass tests.

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
