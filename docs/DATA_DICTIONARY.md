# Molecularis data dictionary and provenance model

## Purpose

This is the target conceptual model for the multi-subject architecture. It documents both existing repository concepts and required additions. Do not infer that every target entity is already implemented in Room.

| Entity | Key fields | Status in current repository |
|---|---|---|
| SubjectWorkspace | id, name, description, taxonomy, language, defaults, createdAt | Required; not yet first-class |
| ProfessorProfile | id, subjectId, name, role, instructions, audience, goals, boundaries, promptVersion | Required; not yet first-class |
| Book | id, subjectId, title, originalFileName, localPath, sourceUri, checksum, rightsBasis, importedAt | Existing book lacks subjectId and rights metadata |
| KnowledgeBook | id, bookId, detected metadata, subject, reviewState, extraction metrics | Existing; subject is detected metadata, not workspace ownership |
| Passage | id, bookId, pageNumber, chunkIndex, text, extractionVersion | Existing page-linked passage concept |
| Topic | id, knowledgeBookId, name, parentTopicId, confidence, evidence, approved | Existing; book/knowledge-book scoped |
| TopicPassageLink | topicId, passageId, pageNumber, linkType | Existing provenance link |
| Conversation | id, subjectId, professorProfileId, createdAt | Existing conversation lacks subject/profile scope |
| Message | id, conversationId, role, content, timestamp, status | Existing conversation message |
| Lesson | id, subjectId, professorProfileId, sourceSetHash, promptVersion, modelVersion, reviewState | Existing saved lesson lacks full provenance fields |
| EvaluationRun | id, subjectId, appCommit, modelVersion, configHash, datasetVersion, timestamp | Required; not yet implemented |

## Core invariants

1. Every source document belongs to exactly one subject workspace unless the user explicitly creates a shared-source relationship.
2. Every derived passage inherits the source's subject scope.
3. Every topic-to-passage link must point to a passage belonging to the same subject scope.
4. Every conversation has an explicit subject scope. A professor profile must belong to that same subject.
5. Retrieval queries are scoped by subject ID before ranking. Filtering after global retrieval is insufficient.
6. Cross-subject retrieval is a separate explicit user action and must label the source subject.
7. Deleting a source must remove or orphan its derived passages, topic links, cached vectors, and dependent citations according to a documented retention policy.
8. A source replacement creates a new checksum/version and must not silently rewrite the provenance of previously generated content.
9. Store model/provider, prompt template version, retrieval configuration, source-set hash, and generation timestamp for reproducibility.
10. Do not store API secrets in these entities; use secure platform storage.

## Suggested relational relationships

- SubjectWorkspace 1—N Book
- SubjectWorkspace 1—N ProfessorProfile
- SubjectWorkspace 1—N Conversation
- SubjectWorkspace 1—N Lesson
- Book 1—N Passage
- Book 1—0..1 KnowledgeBook processing record
- KnowledgeBook 1—N Topic
- Topic N—N Passage through TopicPassageLink
- ProfessorProfile 1—N Conversation and Lesson
- EvaluationRun N—1 SubjectWorkspace (or an explicitly declared multi-subject scope)

## Migration strategy

1. Add a default legacy workspace (e.g., "My first subject") and assign existing books and conversations to it.
2. Do not automatically label every existing book "Biochemistry"; preserve the detected metadata as metadata and ask the user to confirm the workspace subject.
3. Add nullable subject IDs first, backfill and verify counts, then enforce non-null constraints in a later migration.
4. Preserve existing foreign-key cascades and FTS triggers.
5. Add database-level indexes and constraints for workspace scope.
6. Add migration tests using populated databases from every supported schema version.
7. Add two-subject integration fixtures with similar terms and verify zero unauthorized leakage.
