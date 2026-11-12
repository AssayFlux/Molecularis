# Molecularis — Proposed Architecture

## Platform decision

Build Molecularis as a **native Android application using Kotlin and Jetpack Compose**. Use Room as the SQLite persistence layer. Keep the architecture modular, but begin with a small buildable application rather than creating many empty Gradle modules.

Astronaut is a useful reference implementation for Android-first offline AI patterns. Reuse selected patterns and code only after reviewing dependencies, license compatibility, security and device behavior. Do not copy the whole app or couple Molecularis to Astronaut's chat product.

## System overview

- Android UI: Jetpack Compose screens for library, topic browser, lecture builder, presentation player and settings.
- Domain layer: ingestion, topic organization, lesson planning, diagram sequencing and presentation orchestration.
- Data layer: Room/SQLite, local file storage, full-text search and repositories.
- AI provider layer: a local model adapter and optional remote API adapter behind one interface.
- Media layer: Android audio playback, text-to-speech, slide rendering and SVG rendering.
- Background work: WorkManager for imports, indexing, downloads and lesson preparation; a user-visible foreground media service for long-running lecture playback where Android policy requires it.

## Data and files

Use Room/SQLite for structured metadata and searchable extracted content. Do not put entire book PDFs or large image binaries into SQLite blobs. Keep original documents and media in app-private storage or user-selected Storage Access Framework locations, with persisted URI permission only when the user chooses to retain access.

Initial database entities:
- Book: title, author/editor if known, edition, file URI, import status and processing metadata.
- Document: file metadata, MIME type, checksum and extraction status.
- Chapter: book relationship, title, page range and hierarchy.
- Topic: normalized topic name, parent topic and aliases.
- ContentChunk: text, book/chapter/topic links, page range and chunk order.
- TopicChunk: many-to-many mapping between topics and content chunks.
- VisualAsset: local path/URI, topic, origin URL, license/permission note and attribution metadata.
- Lesson: topic, audience level, language, target duration, status and timestamps.
- LessonSegment: order, estimated duration, teaching purpose, narration text and slide association.
- Slide: lesson, order, title, body and visual layout data.
- Diagram: reusable SVG source, topic, components and reveal-step definitions.
- LectureSession: lesson, schedule, playback state, completion state and error details.
- ProviderConfig: provider identifier and non-secret settings; API secrets stored separately in Android Keystore-backed encrypted storage.

## Content pipeline

1. Import a user-selected PDF or other supported study material.
2. Extract text and page boundaries; use on-device OCR only for scanned pages.
3. Clean headers, footers, hyphenation and extraction artifacts without silently changing scientific meaning.
4. Detect headings, chapter hierarchy, tables and figure captions where practical.
5. Split content into coherent, overlapping chunks that preserve context.
6. Assign topic labels and aliases; allow professor correction and merging.
7. Index chunks for fast local search. Start with SQLite FTS5/Room-supported lexical search; add local embeddings and vector similarity only after a tested Android runtime is selected.
8. Keep processing resumable and show progress, failures and unsupported document cases.

## Teaching generation

The teaching engine should transform retrieved content into a lesson structure rather than paraphrase arbitrary chunks. A lesson plan can contain:
- Learning objectives and a short opening.
- Prerequisite concepts.
- Stepwise explanation of the mechanism or pathway.
- Important enzymes, substrates, products, cofactors and regulation.
- Relevant clinical or experimental connections appropriate to the selected level.
- Misconceptions and clarifying analogies.
- Recap and questions.

Use a provider interface so lesson generation can run through a compatible local model or an explicitly configured external API. If no generative model is installed, provide search, structured templates and clearly labeled limited generation rather than pretending a full AI model is present.

## Visual and SVG system

Represent a diagram as structured scientific components plus SVG output and ordered reveal steps. Components may include molecule labels, reaction arrows, enzyme labels, compartments, cofactors, energy markers and regulatory annotations.

The renderer should:
- Validate SVG input and reject scripts, external entities and unsafe embedded resources.
- Keep diagram elements addressable by stable IDs.
- Reveal components in a defined sequence.
- Synchronize each reveal step with a lesson segment or narration cue.
- Support zoom, pan, accessibility labels and static fallback.
- Keep imported images distinct from diagrams generated from SVG components.

For internet-sourced visuals, search for educational assets with reusable permissions where possible. Cache only when permitted and retain origin and rights metadata. Do not assume an image found online is free to reuse.

## Voice and presentation

Separate narration text from slide text. A lesson segment should define narration, estimated timing, slide transitions and diagram reveal events. The presentation player coordinates audio, slide display and diagram animation against one timeline.

Android text-to-speech can be the first voice adapter, but offline availability depends on the installed speech engine and language packs. Detect and communicate offline readiness. Add a bundled/local speech engine only after licensing, APK size, quality and device performance are evaluated.

Generate editable PowerPoint (.pptx) files as a planned export capability. Keep slide content in a provider-neutral model so the app can also render slides itself and export a PDF fallback. Validate the chosen PPTX library on Android before committing to it.

Scheduled lectures need clear user consent, visible notifications and Android-compliant foreground playback. Android battery optimization, exact-alarm permission, background execution limits and OEM restrictions mean the app must explain that scheduling reliability depends on device settings. Never claim unattended playback is guaranteed on every phone.

## Optional external AI

- External providers are disabled until configured and explicitly selected.
- Store API secrets using Android Keystore-backed encryption; never commit keys or place them in source code.
- Show the provider and whether a request will leave the device.
- Do not upload the professor's book library or full documents by default. Send only the minimum context the professor explicitly chooses.
- No silent cloud fallback when local inference fails.

## Security, privacy and content rights

- Keep books, extracted text, lesson drafts and API settings local by default.
- Allow the professor to delete an imported book and its derived text/index entries.
- Treat imported PDFs, images and SVG as untrusted input.
- Sanitize SVG and bound document, OCR, image and model processing resources.
- Respect book licenses and image reuse terms. Public availability is not permission to redistribute.
- Avoid storing student personal data unless a future feature truly requires it.

## Suggested initial package boundaries

Start in one Android app module with packages such as:
- app / navigation
- library / import / extraction
- knowledge / topics / search
- lesson / planning / generation
- diagrams / svg / animation
- presentation / slides / playback
- voice / providers
- settings / ai / privacy
- data / database / repositories

Extract Gradle modules only when boundaries are stable and tests justify the split.
