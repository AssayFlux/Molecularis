# Molecularis — Product Vision

## North Star

Molecularis is a multi-domain, offline-first workspace where users build private subject libraries, curate source-grounded Knowledge Pools, and configure one or more AI professor roles to support learning and teaching.

Biochemistry is an important initial domain and has specialized capabilities, but it is not the product boundary.

## Users and jobs to be done

- Learners: understand a topic, revise from selected sources, and test their knowledge.
- Educators: prepare level-appropriate lessons, presentations, and assessments.
- Researchers: organize source collections, inspect evidence, and create traceable summaries.
- Professionals: maintain private domain-specific reference workspaces.

## Core workflow

1. Create a subject workspace and define scope, level, language, and intended use.
2. Add supported documents to that workspace's Library.
3. Process selected sources into a separate Knowledge Pool.
4. Inspect extraction quality, metadata, topic hierarchy, and source-page links.
5. Approve or reject sources and topic evidence.
6. Configure one or more professor roles with explicit scope and boundaries.
7. Chat, plan lessons, create learning materials, and inspect supporting evidence.
8. Save, export, reproduce, or delete outputs and their source associations.

## Product principles

- Subject identity is explicit and scoped; never assume biochemistry.
- One subject can have several professor roles with different pedagogical objectives.
- Source books remain separate from extracted/indexed knowledge.
- Human approval gates source-grounded generation where the workflow requires review.
- Citations must resolve to actual source passages and pages; never fabricate references.
- Provider/model use and network transfer must be visible and user-controlled.
- Retrieval, extraction, and generation are distinct operations and must be described accurately.
- User documents are untrusted content, not instructions to the AI or application.
- High-impact domains require additional expert review and domain-specific safety controls.
- Rights metadata and deletion semantics must be understandable.

## Current implementation boundary

Implemented foundation:
- PDF import, local preservation, checksum duplicate detection.
- Page-aware extraction/OCR, resumable processing, quality audits.
- Knowledge Pool metadata and topic review, aliases, topic-to-passage provenance.
- Local lexical search and optional semantic retrieval components.
- Teaching Studio, saved lessons, slide exports, diagrams, and narration features.

Not yet complete as an end-to-end multi-subject product:
- First-class subject/workspace entity and subject-scoped Library/Knowledge Pool.
- Subject selection during import and reliable migration of existing books.
- Multiple configurable professor profiles per subject.
- Subject-aware prompt composition and per-role memory/configuration.
- End-to-end isolation tests proving retrieval never crosses subject boundaries.
- Generic document support beyond the currently supported PDF workflow.
- Discipline-neutral teaching templates and assessments.
- Research-grade output provenance and exportable experiment records.

## Evaluation outcomes

The platform should be evaluated separately for:
- Ingestion fidelity and page mapping.
- Retrieval relevance and evidence recall.
- Citation correctness and claim support.
- Subject classification and cross-subject isolation.
- Expert-rated factual correctness and pedagogical quality.
- Learner comprehension and retention, using an appropriate controlled study.
- Latency, memory, energy, crash rate, and offline task completion.

Do not collapse these into one heuristic score. Report each metric with dataset, sample size, uncertainty, and failure cases.
