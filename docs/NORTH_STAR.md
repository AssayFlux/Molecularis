# Molecularis — North Star

## The destination

Molecularis is a user-built, offline-first learning and teaching workspace. A person chooses a subject, adds books and other authorized materials, reviews the knowledge extracted from those sources, and creates one or more AI professor roles to help explain, teach, question, and organize that subject.

The intended experience is not a single preconfigured biochemistry tutor. It is a reusable framework for many subjects and many professor roles, with the active subject's sources, learning goals, and safety constraints made explicit.

## Who it serves

- Independent learners building a personal knowledge library.
- Educators preparing lessons and assessments from selected course materials.
- Researchers organizing domain-specific references and comparing source evidence.
- Professionals maintaining a private reference workspace.
- Study groups and institutions, where future collaboration and governance features are implemented.

## The core experience

1. **Create a subject workspace.** Name a subject, define its scope, add optional sub-disciplines, and choose the learner or professional level.
2. **Add sources.** Import books, notes, papers, and supported documents the user is authorized to process. Preserve original files separately from derived text.
3. **Build a Knowledge Pool.** Extract text, retain page boundaries, audit extraction quality, organize topics, and let the user correct metadata and topic structures.
4. **Review evidence.** Approve sources and topic links. Preserve exact source, page, passage, version, and processing provenance.
5. **Create professor roles.** Configure one or more roles (for example, foundational tutor, advanced lecturer, examiner, research-methods mentor) with domain, audience, objectives, and boundaries.
6. **Learn and create.** Use subject-scoped chat, lesson plans, slides, diagrams, quizzes, notes, and other supported study tools.
7. **Verify and improve.** Inspect evidence, correct mistakes, compare outputs against source material, and export reproducible evaluation records where consented.

## Product principles

- **User-defined domain:** no single academic discipline is the product's identity. Domain-specific features are modular extensions.
- **Evidence before confidence:** distinguish source-supported statements from general model knowledge; never fabricate citations.
- **Human review:** extracted topics and generated teaching content are candidates for review, not unquestionable truth.
- **Traceability:** retain document identity, checksum, page, passage, processing version, and approval state wherever possible.
- **Offline by default:** local library and search should not require cloud access. Network inference must be explicit.
- **Plural expertise:** multiple professor roles may coexist in one subject workspace without mixing their prompts or permissions.
- **User control:** the user owns workspace configuration and can remove sources and derived material.
- **Reproducibility:** record model/provider identity, prompt/template version, retrieval settings, source set, and timestamps for research-relevant outputs.
- **Safety by domain:** higher-risk disciplines require additional guardrails, disclaimers, and expert oversight.
- **Honest capability:** do not claim model training when the system has only extracted and indexed documents. Do not claim accuracy, learning gain, or clinical/legal competence without evaluation.

## Research integrity

Molecularis should be studied as a socio-technical system: document ingestion, retrieval, human review, AI generation, and learner interaction all affect outcomes. Research must report model/provider, version, hardware, corpus composition and rights, language, prompt and retrieval configuration, inclusion/exclusion criteria, missing data, failures, and human-review procedures. Educational outcomes require a suitable comparison design and validated measures. Software unit tests alone cannot establish educational benefit.

## Product boundary

Molecularis is a learning and knowledge-work aid. It is not an authority that replaces educators, domain experts, clinicians, lawyers, financial advisers, or institutional review. It must not silently upload private documents, train on user content without explicit informed consent, or present generated text as verified fact.

## Definition of success

A user can:
- Create multiple distinct subject workspaces.
- Add sources to the intended subject without accidental cross-contamination.
- Build and review a page-linked Knowledge Pool.
- Configure multiple professor roles for the same subject.
- Ask questions and create teaching material with visible evidence and uncertainty.
- Reproduce a prior output from its recorded source, model, prompt, and retrieval configuration.
- Export or delete their own data with understandable consequences.

These are target capabilities. Each must be marked implemented only after end-to-end tests and user-facing verification.
