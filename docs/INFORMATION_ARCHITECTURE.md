# Molecularis Information Architecture

## Product principle

Every top-level destination has one clear responsibility. Features should live where users expect them, and should not be duplicated across unrelated destinations. Keep source material, extracted knowledge, conversations, AI configuration, and authored lectures as distinct concepts.

## Primary navigation

1. **Home** — overview, recent activity, and shortcuts into the six work areas.
2. **Lectures** — the dedicated lecture-building studio (the existing Teaching Studio, promoted and refined).
3. **Chats** — study conversations and study tools available in the context of a conversation.
4. **Library** — imported source books and documents, arranged into shelves.
5. **Knowledge Pool** — extracted, source-linked knowledge and review workflows.
6. **AI Hub** — AI capabilities and AI configuration/workflows.
7. **Settings** — application preferences, grouped into clear categories.

Avoid a generic "More" bucket for core destinations. On compact devices, use a clearly labelled navigation drawer or adaptive navigation rail rather than hiding important areas in an ambiguous menu.

## Destination responsibilities

### Home
- Show a concise overview of books, extracted sources, conversations, and saved lectures.
- Provide direct actions for importing a book, starting a study chat, reviewing extracted knowledge, and creating a lecture.
- Keep metrics actionable; each metric opens its corresponding destination.

### AI Hub
All AI-related capabilities belong here:
- On-device model catalog, import, download, runtime readiness, and active model.
- Online AI providers, endpoints, model identifiers, credentials, and enable/disable controls.
- AI routing, model collaboration, and capability availability.
- Training and dataset preparation/validation workflows.
- Embeddings, semantic retrieval configuration, and vision model capabilities.
- AI diagnostics and clear explanations of which capabilities are actually available on the device.

Do not place AI provider/model controls in general app Settings. Settings may contain a link to AI Hub, but the configuration itself belongs in AI Hub.

Suggested headings: **Overview**, **On-device AI**, **Online AI**, **Models & downloads**, **Training & datasets**, **Retrieval & embeddings**, **Vision**, **Diagnostics**.

### Settings
All application preferences belong here. Present a settings landing page with category rows and concise descriptions, then focused subpages. Do not mix model/provider management into these pages.

Suggested categories and contents:
- **Customisation** — response style, teaching preferences, default audience and lesson preferences.
- **Appearance** — light/dark/system appearance, accent palette, typography, font size, shape, and background.
- **Voices** — narration voice, speech language, recognition language, pronunciation dictionary, speech rate, and installed voice/language availability.
- **Notifications** — reminders and notification preferences (only where implemented).
- **Privacy & security** — app lock, biometric unlock, local data and privacy explanations.
- **Storage & downloads** — cache, imported files, model storage overview, and safe cleanup controls.
- **Accessibility** — text scaling, contrast, motion, and screen-reader-friendly labels.
- **About & diagnostics** — version, licenses, diagnostics, and support information.

Each setting must have a clear label, plain-language explanation, current value, and an appropriate control. Destructive actions require confirmation. Avoid dumping every preference into one long undifferentiated screen.

### Library
Library is the source-material shelf:
- Every imported book/document appears here, with title, author when known, file type, page count, import date, and processing state.
- Organise books into user-visible shelves/collections (for example: Biochemistry, Molecular Biology, Metabolism, Reference).
- Support search, sorting, filtering, shelf creation/renaming, and moving a book between shelves.
- Book detail opens the source document and its metadata.
- Keep original source files intact when creating extracted knowledge.

Do not put extracted topics or generated summaries in the Library as if they were source books.

### Knowledge Pool
Knowledge Pool contains only information extracted or authored as structured knowledge:
- Knowledge sources linked back to their original Library book/document.
- Extracted topics, subtopics, concepts, definitions, pathways, and evidence passages.
- Review state, extraction quality, source page references, aliases, hierarchy, and merge/organisation tools.
- Search and filters by source, topic, subject, and review state.
- Clear review and approval actions before unverified extracted content is treated as trusted teaching evidence.

A Knowledge Pool item must preserve provenance: users should be able to trace a concept or passage back to the source book and page. The source book remains in Library.

### Chats
Chats is the study workspace for interactive learning:
- Conversation history, search, rename, archive, and delete.
- Study modes such as explain, quiz, flashcards, compare concepts, solve a problem, and exam revision (where implemented).
- Context controls to include approved Knowledge Pool sources and selected Library books.
- Relevant study tools available from the chat composer/tool drawer: attach a source, reference a topic, voice input/output, and study actions.
- Make source citations and evidence inspectable in the conversation.
- Keep AI provider/model configuration in AI Hub; Chats should expose only the model/capability selector needed to choose an available engine.

### Lectures (existing Teaching Studio)
Promote the existing Teaching Studio into a first-class **Lectures** destination and improve it as a complete authoring workflow:
- **My Lectures** — saved drafts, completed lectures, recent work, and search/filter.
- **Create Lecture** — title, subject/topic, audience, learning objectives, duration, teaching style, and source selection.
- **Build** — outline, sections, explanations, examples, diagrams, slide content, and speaker notes.
- **Sources & evidence** — select approved Knowledge Pool material and Library references; preserve citations.
- **Preview** — inspect the lecture as a learner/presenter, including slides and narration.
- **Export & present** — use existing supported PDF/PPTX/presentation and narration capabilities.
- **Save** — persist drafts and revisions; reopening a saved lecture restores its editable content.
- **Delete** — allow deletion from My Lectures with a confirmation step; explain whether exports remain on device.
- **Duplicate** — create a separate editable copy without changing the original.

A lecture is a durable authored artifact, not a transient chat response. Autosave or an explicit save state should make unsaved changes obvious. Deleting a lecture must not delete its source books or Knowledge Pool records.

## Cross-section rules

- Library = original source documents.
- Knowledge Pool = extracted and reviewed knowledge with provenance.
- Chats = interactive study and question-answering.
- Lectures = authored teaching deliverables.
- AI Hub = AI engines, providers, models, training, and AI capability configuration.
- Settings = app-wide preferences and device/app experience.

Use cross-links where helpful, but do not duplicate ownership. For example, a lecture may link to a book and a knowledge topic; it does not own or duplicate those source records.

## Quality and acceptance checklist

- Every major destination is reachable without hunting through a generic overflow menu.
- Every Settings preference is grouped under a descriptive category and focused subpage.
- AI-related configuration is consolidated in AI Hub.
- Library shelves contain source books/documents only.
- Knowledge Pool entries show source provenance and review status.
- Chat exposes study tools in context without becoming a second settings or AI administration screen.
- Lectures can be created, edited, previewed, saved, reopened, duplicated, and deleted with confirmation.
- Empty, loading, error, and success states are designed for every major workflow.
- Navigation and content remain usable on narrow Android screens, with scrollable content and accessible labels.
