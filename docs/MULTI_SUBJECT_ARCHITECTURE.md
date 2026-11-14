# Multi-subject and multi-professor architecture

## Current implementation boundary

Molecularis now has an initial first-class subject-workspace and professor-profile implementation. Room entities and a version-18 migration provide a default legacy workspace; the app exposes create/select/edit flows; and the principal library, Knowledge Pool, chat, projects, saved lessons, and scheduled lectures are scoped by subject ID.

The architecture is not yet a complete general-purpose multi-domain platform. Subject isolation still requires successful CI and populated-database migration validation. The biochemical diagram editor remains a specialist tool, cross-subject comparison is not yet a user-facing opt-in workflow, and not every generated artifact has complete provenance.

## Design decision

Molecularis should be a platform with a generic core and optional domain packs. Biochemistry-specific pronunciation, pathway diagrams, medical audience profiles, and domain taxonomies must not shape the global prompt or force every workspace into a biomedical workflow.

## Workspace model

A SubjectWorkspace is the top-level boundary for user-selected sources, Knowledge Pool records, conversations, professor profiles, projects, lessons, and scheduled teaching. The current entity includes a stable ID, name, description, optional discipline code, language tag, timestamps, and a default marker. Workspace lifecycle currently supports creation, selection, and editing; archival/deletion and data-transfer tooling remain planned.

Existing records are migrated into a default workspace named “My first subject.” The app does not infer that every legacy source is biochemistry.

## Professor profiles

A professor profile is a named configuration, not a separately trained model. Current fields include:
- Subject/workspace ID and display name.
- Pedagogical role.
- Learner level, tone, and teaching objectives.
- Custom instructions.
- Source-use policy and safety boundaries.
- Prompt-template version and timestamps.

The app supports creating, selecting, and editing profiles. Deletion, profile import/export, and a richer configuration editor remain planned. User-configured role labels and instructions are treated as preferences, not trusted system instructions.

Several profiles may share one subject's Knowledge Pool while maintaining distinct instructions. Do not claim that creating a profile fine-tunes or trains an AI model.

## Core request flow

1. User selects a workspace and professor profile.
2. The app presents only books, Knowledge Pool records, conversations, projects, lessons, and scheduled lectures belonging to that subject.
3. Retrieval joins passages to their source book and filters by the active subject before ranking or returning evidence.
4. The prompt is composed from generic system policy, the active subject label, selected professor preferences, learner context, and retrieved evidence.
5. Retrieved evidence is labelled with source, page, and passage information.
6. Local and configured remote chat receive the same constructed prompt/context; remote inference remains opt-in and may transmit prompt/source text to the configured provider.
7. Successful assistant messages record provider/model, profile ID, prompt version/hash, source-set hash when available, and retrieval configuration.
8. Scheduled lecture playback verifies that the scheduled row and saved lesson share the same subject ID.

## Domain packs

A domain pack may contribute specialized renderers, vocabulary, notation, templates, safety policy, and evaluation rubrics. It must be optional and versioned. The generic core must still operate if no domain pack is installed. The current biochemical diagram editor should be treated as a specialist module, not evidence of general diagram support.

## Database and migration

Room schema version 18 adds subject workspaces, professor profiles, and subject/provenance columns to existing records. Existing books, conversations, projects, lessons, and schedules are assigned to legacy-default. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for exact migration details.

The migration is additive and must be tested against populated databases from supported prior versions. The current instrumentation fixture tests DAO-level isolation for two subjects with overlapping vocabulary; it does not replace migration tests, physical-device testing, or security review.

## Acceptance tests

- Create two subjects and add at least two source documents to each.
- Verify library lists, FTS search, Knowledge Pool lists, and chat retrieval are scoped correctly.
- Verify two professor profiles in one subject have independent settings and can be selected/edited.
- Verify conversation switching does not leak history or professor configuration.
- Use identical query terms in both subjects and assert retrieval only returns active-subject passage IDs.
- Verify projects, saved lessons, and schedules remain scoped after subject switching and process restart.
- Verify scheduled playback refuses a lesson/lecture subject mismatch.
- Migrate a populated legacy database without loss or duplicate rows; verify encrypted copy and FTS indexes.
- Verify source deletion and replacement remove or invalidate derived records and cached retrieval data.
- Implement explicit cross-subject comparison only with visible consent and subject-labelled evidence.
