# Multi-subject and multi-professor architecture

## Design decision

Molecularis should be a platform with a generic core and optional domain packs. Biochemistry-specific pronunciation, pathway diagrams, medical audience profiles, and domain taxonomies remain useful modules, but must not shape the global prompt or force every workspace into a biomedical workflow.

## Workspace model

A SubjectWorkspace is the top-level boundary for user-selected sources, Knowledge Pool records, conversations, professor profiles, lessons, and evaluation records. Users can create as many workspaces as local storage and device performance permit. Each workspace has a name, description, optional taxonomy/discipline code, language, intended learner levels, and domain-specific safety profile.

## Professor profiles

A professor profile is a named configuration, not a separately trained model. It can define:
- Display name and pedagogical role.
- Subject/workspace ID.
- Learner level and prerequisites.
- Teaching objectives and preferred structure.
- Tone, language, response length, and assessment style.
- Source-use policy and citation format.
- Explicit safety boundaries.
- Prompt-template version and creation/update timestamps.

Several profiles may share one subject's Knowledge Pool while maintaining distinct instructions. Do not claim that creating a profile fine-tunes or trains an AI model.

## Core request flow

1. User selects a workspace and professor profile.
2. The app validates that the profile belongs to the active workspace.
3. Retrieval is executed with a mandatory workspace filter.
4. The system constructs a prompt from the generic base policy, domain profile, professor profile, learner level, and retrieved evidence.
5. Retrieved evidence is labelled with source ID, title, page, passage ID, and retrieval score.
6. The model generates a response or abstains when evidence is inadequate.
7. The app stores provenance metadata with the result.
8. The user can inspect citations, correct the answer, and flag unsupported claims.

## Domain packs

A domain pack may contribute specialized renderers, vocabulary, notation, templates, safety policy, and evaluation rubrics. It must be optional and versioned. The generic core must still operate if no domain pack is installed.

## Database migration

Follow the additive migration plan in DATA_DICTIONARY.md. Migrate existing content to a user-confirmed legacy workspace. Never silently infer a user's academic discipline from the app's former branding or from a book title.

## Required acceptance tests

- Create two subjects and add at least two source documents to each.
- Verify library lists and Knowledge Pool lists are scoped correctly.
- Verify two professor profiles in one subject have separate settings.
- Verify conversation switching does not leak history or professor configuration.
- Use identical query terms in both subjects and assert retrieval only returns active-subject passage IDs.
- Explicitly request cross-subject comparison and verify sources are labelled by subject.
- Delete a source and assert that its derived passages, vector rows, and links are removed or marked unavailable.
- Reopen the app and verify selected workspace/profile persistence.
- Migrate a populated legacy database without loss or duplicate rows.
