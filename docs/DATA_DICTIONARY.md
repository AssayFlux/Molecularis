# Molecularis data dictionary and provenance model

## Purpose and implementation status

This document distinguishes entities already present in Room from concepts still planned. The active subject boundary is implemented for the primary learning workflows; this does not imply that every derived artifact or every specialist module is fully scoped.

| Entity | Key fields | Current status |
|---|---|---|
| SubjectWorkspace | id, name, description, disciplineCode, languageTag, timestamps, isDefault | Implemented in Room; create, select, edit |
| ProfessorProfile | id, subjectId, name, role, instructions, learnerLevel, tone, objectives, sourcePolicy, safetyBoundaries, promptVersion | Implemented in Room; create, select, edit; configuration only, not model training |
| Book | id, subjectId, title, localPath, sourceUri, checksum, importedAt | Implemented; import uses active subject |
| KnowledgeBook | id, bookId, detected metadata, reviewState, extraction metrics | Existing; workspace scope inherited through source Book |
| Passage | id, bookId, pageNumber, chunkIndex, text | Existing; workspace scope inherited through source Book |
| Topic | id, knowledgeBookId, name, parentTopicId, confidence, evidence, approved | Existing; scope inherited through KnowledgeBook/Book |
| TopicPassageLink | topicId, passageId, pageNumber, linkType | Existing; passage/book relationship provides scope |
| Conversation | id, subjectId, professorProfileId, workspaceProjectId, createdAt | Implemented; subject-filtered list and profile selection |
| Message | id, conversationId, role, content, status, provider/model, promptVersion/hash, sourceSetHash, retrievalConfig | Implemented; provenance fields populated for successful assistant answers |
| WorkspaceProject | id, subjectId, name, description, timestamps | Implemented; scoped to active subject |
| Lesson | id, subjectId, professorProfileId, promptVersion, outline, timestamps | Implemented; subject-filtered saved lessons; source/model provenance is incomplete |
| ScheduledLecture | id, lessonId, subjectId, schedule, status, workId | Implemented; scoped and validates lesson ownership before playback |
| SavedDiagram | id, title, template, diagramJson, updatedAt | Existing storage concept; not yet integrated into subject-scoped saved-output workflows |
| EvaluationRun | id, subjectId, appCommit, modelVersion, configHash, datasetVersion, timestamp | Planned; no first-class experiment-run table yet |

## Core invariants

1. Every imported source book has one subjectId.
2. Every derived passage is owned by a book; retrieval must join through the book and filter by its subjectId before ranking or returning results.
3. Knowledge Pool records are scoped through their source book. A detected KnowledgeBook.subject is metadata, not the workspace ID.
4. Every conversation has a subjectId; a selected professor profile must belong to the same subject.
5. Saved lessons, workspace projects, and scheduled lectures carry subjectId; scheduled playback verifies that the referenced lesson has the same subject.
6. Cross-subject retrieval is not currently offered as an implicit fallback. A future comparison workflow must be an explicit user action and label each source's subject.
7. Deleting a source must remove or orphan derived passages, topic links, cached vectors, and dependent citations according to a documented retention policy. Full derived-data deletion verification remains a release gate.
8. A source replacement creates a new checksum/version and must not silently rewrite the provenance of previously generated content.
9. Successful chat answers record provider/model, professor profile, prompt version and hash, source-set hash (when sources were retrieved), and retrieval configuration. This metadata is not yet uniformly attached to every generated artifact.
10. Do not store API secrets in these entities; use secure platform storage.

## Relational relationships

- SubjectWorkspace 1—N Book
- SubjectWorkspace 1—N ProfessorProfile
- SubjectWorkspace 1—N Conversation
- SubjectWorkspace 1—N WorkspaceProject
- SubjectWorkspace 1—N Lesson
- SubjectWorkspace 1—N ScheduledLecture
- Book 1—N Passage
- Book 1—0..1 KnowledgeBook processing record
- KnowledgeBook 1—N Topic
- Topic N—N Passage through TopicPassageLink
- ProfessorProfile 1—N Conversation and Lesson
- EvaluationRun N—1 SubjectWorkspace (planned)

## Migration 17 → 18

The additive Room migration:
1. Creates subject_workspaces and professor_profiles.
2. Creates a default legacy-default workspace and legacy-professor-default profile.
3. Adds subjectId to existing books, conversations, workspace projects, saved lessons, and scheduled lectures, defaulting existing rows to legacy-default.
4. Adds professorProfileId to conversations and saved lessons.
5. Adds provider/model, prompt version/hash, source-set hash, and retrieval configuration fields to messages.
6. Adds indexes for subject/profile lookups.

Existing content is preserved in the default workspace. The migration does not guess a discipline from old branding or detected book metadata. A populated-database migration test across supported historical versions remains required before release. New installs seed the same default workspace/profile in the Room creation callback.

## Validation requirements

- Two-subject fixture with overlapping vocabulary; library search and retrieval must return only the active subject.
- Conversation, professor, lesson, project, and schedule lists must remain scoped after switching subjects and restarting the app.
- Attempted profile/lesson mismatch must be rejected by application logic and covered by tests.
- Test migration from a populated version-17 database and verify row counts, foreign keys, FTS state, and encrypted-copy integrity.
- Verify source deletion and replacement across passages, topics, vector chunks, citations, and exports.
- Add explicit cross-subject comparison only with visible user consent and source subject labels.
