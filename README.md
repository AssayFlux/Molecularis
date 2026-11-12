# Molecularis

**An offline-first Biochemistry Teaching Assistant for Android.**

Molecularis helps a biochemistry professor turn trusted books and teaching materials into clear, level-appropriate lectures — with slides, scientific diagrams and voice narration. It is designed for MBBS, MD, DNB and PhD teaching.

## North Star

**Make excellent biochemistry teaching available whenever and wherever students need it — even when the professor cannot be present.**

The professor selects the topic, student level and duration. Molecularis organizes the relevant knowledge, prepares a teaching flow, builds a visual presentation and can deliver the lesson with synchronized voice narration and step-by-step scientific diagrams.

## Core capabilities

- Import permitted books and study materials into a local library.
- Extract, organize and search content by subject, topic and subtopic.
- Generate teaching flows adapted for MBBS, MD, DNB and PhD levels.
- Build slides and export presentations.
- Assemble scientific diagrams from reusable SVG components and reveal them progressively.
- Deliver lectures using voice narration synchronized with slides and diagrams.
- Schedule prepared teaching sessions, subject to Android background-execution and permission limits.
- Work offline after books, models, voice packs and other required assets are available.
- Optionally connect external AI providers; cloud use is never mandatory or silently enabled.

## Platform direction

- Android application: Kotlin + Jetpack Compose.
- Structured local data: Room / SQLite.
- Book and media files: app-private storage or user-selected document locations.
- Search: SQLite full-text search first; optional local semantic retrieval later.
- AI: local model adapter plus optional external API adapter.
- Voice and playback: Android media/TTS adapters, with offline readiness checks.
- Visuals: structured scientific diagrams rendered as safe SVG.

The Android application now starts from the reusable Astronaut Kotlin/Compose foundation, including its interface, local data layer, offline AI adapters, knowledge retrieval, model management and voice components. These are being adapted into a biochemistry teaching workspace; not every imported capability is yet verified or complete.

## Roadmap

1. **Foundation:** Android project, navigation, database and CI.
2. **Book library:** import PDFs, extract text and preserve page structure.
3. **Knowledge base:** topic hierarchy, chunking and offline search.
4. **Teaching engine:** level-aware lesson planning and optional AI providers.
5. **Slides:** in-app presentation and export.
6. **SVG diagrams:** reusable biochemical components and progressive reveals.
7. **Voice:** narration synchronized with slides and diagrams.
8. **Autonomous teaching:** schedule, preflight and play prepared lectures.
9. **Release quality:** scientific review, device testing, privacy and performance.

The first vertical slice is implemented in code: **import a PDF, extract page text on-device, search passages, prepare and edit a structured teaching outline, save and reopen it, and read it aloud using an installed offline Android voice.** CI and physical-device acceptance are still pending.

## Project documentation

- [North Star — product destination and principles](docs/NORTH_STAR.md)
- [Product vision and requirements](docs/PRODUCT_VISION.md)
- [Development roadmap](docs/ROADMAP.md)
- [Android build and installation guide](docs/BUILD_AND_INSTALL.md)
- [Proposed architecture](docs/ARCHITECTURE.md)
- [Astronaut code and UI reuse record](docs/ASTRONAUT_REUSE.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## Development rule

All development is performed directly on the main branch. Keep changes small, tested and documented. Do not claim offline capability until it has been verified on a real Android device with the required local resources installed.

## Content and privacy

Import only books and materials you are authorized to store and process. Images found online are not automatically free to reuse; retain rights information and cache assets only when permitted. Local materials remain on-device by default. Optional API requests are explicit and should send only the minimum context needed.

## Current status

An Android application foundation has been adapted from Astronaut and rebranded for Molecularis. The app includes the Compose interface, encrypted Room persistence, local retrieval, model management and Android voice components. The textbook library supports PDF import up to 5,000 pages per book, page-by-page on-device OCR, bounded passage batching, page-aware storage, keyword search and deletion. A 25-million-character safety ceiling also applies; large imports remain foreground-only and need device stress testing.

Offline chat now retrieves matching passages from imported textbooks and includes book/page/passage labels in the local model prompt so answers can cite their source. This is simple lexical retrieval, not a guarantee of completeness or scientific correctness. The Teaching Studio prepares an editable, level-aware outline with retrieved textbook passages. When a compatible LiteRT-LM model is loaded, it can optionally draft a longer explanation using those local excerpts; the excerpts are retained with the draft and professor verification is required. Lessons are saved in the encrypted local database. Numbered outline sections become a navigable slide preview, and the professor can manually narrate each slide with an installed Android TTS voice.

A validated biochemical diagram schema and XML-escaped SVG renderer are integrated into Teaching Studio as a progressive lesson-flow preview derived from the professor's outline. The diagram can reveal lesson sections step by step; it is not yet a biochemical reaction editor and does not fabricate pathway chemistry. Rich slide authoring and export, diagram pan/zoom and pathway templates, automatic narration timelines, background book ingestion and scheduled autonomous teaching remain open. The latest importer, diagram and cleanup changes are awaiting CI verification. Physical-device, offline-mode and professor acceptance testing have not yet been performed.
