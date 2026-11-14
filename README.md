# Molecularis

**An offline-first, source-grounded, multi-domain learning and teaching workspace for Android.**

Molecularis lets a learner, educator, researcher, or professional create a subject workspace from materials they are authorized to use. Users can import books and documents, organize them into a reviewed Knowledge Pool, and configure one or more AI teaching roles for a subject. The same platform can support biochemistry, biology, medicine, mathematics, engineering, humanities, law, languages, and other disciplines, subject to document-format, model, and safety limitations.

## Product North Star

**Let people build a trustworthy professor for any subject from their own selected knowledge sources—while keeping source ownership, evidence, uncertainty, and user control visible.**

A subject workspace is intended to contain:
- A user-defined subject and optional sub-disciplines.
- One or more subject-professor profiles with distinct roles, level, tone, and teaching objectives.
- A Library of original user-selected books and materials.
- A separate Knowledge Pool containing extracted, indexed, reviewed passages and topic structures.
- Chats, lessons, slides, diagrams, assessments, and notes grounded in the active workspace where supported.
- Provenance links from generated or retrieved claims back to document, page, and passage.

## Current capabilities

- Preserve selected PDF source files separately from extracted knowledge.
- Process PDFs locally with page-aware extraction/OCR, resumable background work, extraction audits, and bounded processing.
- Organize extracted material into topics, aliases, and hierarchies with human review.
- Link reviewed topics to exact source passages and page locations.
- Search reviewed sources locally; optional semantic retrieval components exist but are not the default validated path.
- Create and edit teaching plans, slides, diagrams, narration, and saved lectures.
- Use optional local or explicitly configured remote AI providers; cloud use is not mandatory.
- Encrypt local structured persistence and keep local-only workflows available without an account.

## Important scope distinction

The repository currently contains a mature biochemistry-oriented feature set (including specialized diagrams, pronunciation support, and some audience templates) alongside a discipline-neutral ingestion and retrieval foundation. The current data model and screens do **not yet provide a complete first-class multi-subject workspace manager or multiple independently configured professor profiles**. The generalized prompt foundation is being introduced, but subject selection must still be connected end-to-end to book metadata, Knowledge Pool scope, chat, and lesson generation before the multi-subject workflow can be described as fully implemented.

## Platform

- Android: Kotlin, Jetpack Compose, Room/SQLite, WorkManager.
- Document ingestion: Android document picker, PDF processing, OCR, page-level audit.
- Retrieval: local lexical retrieval; optional local embedding adapters.
- Inference: optional LiteRT-LM and compatible external provider adapters.
- Presentation: editable lesson structures, PDF/PPTX export, SVG-based scientific diagram features, Android TTS.
- Backend: optional API/training/export components; not required for core local document storage and search.

## Research and reproducibility

Research-oriented design, evaluation protocol, data dictionary, study protocol template, and known limitations are maintained in:
- [Research readiness and claims boundary](docs/RESEARCH_READINESS.md)
- [Evaluation protocol](docs/EVALUATION_PROTOCOL.md)
- [Study protocol template](docs/STUDY_PROTOCOL_TEMPLATE.md)
- [Data dictionary and provenance model](docs/DATA_DICTIONARY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Device acceptance checklist](docs/DEVICE_ACCEPTANCE.md)

No efficacy, accuracy, learning-gain, or superiority claim should be made until a preregistered or prospectively specified evaluation has been completed and results are reported transparently. Repository tests demonstrate software behaviour, not educational effectiveness or scientific correctness.

## Build and release

See [BUILD_AND_INSTALL.md](docs/BUILD_AND_INSTALL.md). CI runs unit tests, lint, and a debug APK build. A successful debug build is not a signed production release. Physical-device testing, production signing, privacy-policy review, Play data-safety declarations, and a complete subject-workspace implementation remain release gates.

## Content rights and safety

Import only materials the user is authorized to store and process. Do not redistribute copyrighted source books or extracted full-text content without permission. Track provenance and reuse rights for media. Retrieved text is evidence, not executable instruction. In high-impact disciplines, Molecularis is an educational aid and not a substitute for licensed professional judgement.
