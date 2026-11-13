# Molecularis

**An offline-first Biochemistry Teaching Assistant for Android.**

Molecularis helps a biochemistry professor turn trusted books and teaching materials into clear, level-appropriate lectures — with slides, scientific diagrams and voice narration. It is designed for MBBS, MD, DNB and PhD teaching.

## North Star

**Make excellent biochemistry teaching available whenever and wherever students need it — even when the professor cannot be present.**

The professor selects the topic, student level and duration. Molecularis organizes the relevant knowledge, prepares a teaching flow, builds a visual presentation and can deliver the lesson with synchronized voice narration and step-by-step scientific diagrams.

## Core capabilities

- Preserve original permitted books in Library without modifying source files.
- Process selected books into a separate Knowledge Pool with page-linked passages, conservative metadata detection, chapter/topic candidates and quality indicators.
- Require professor review before reviewed Knowledge Pool sources are used to ground teaching generation.
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

The first vertical slice separates **Library source storage** from **Knowledge Pool processing**. Add an original PDF to Library, then explicitly process it in Knowledge Pool. Foreground WorkManager performs page-by-page OCR with durable checkpoints, audits extraction quality, and atomically replaces indexed passages only after successful processing. Topic sections now link to exact supporting passages and page numbers; the professor can edit topic hierarchy, aliases and merges before approval. Teaching Studio and offline textbook chat use only professor-reviewed Knowledge Pool sources. Extraction and heading analysis remain deterministic first passes, not model fine-tuning or a guarantee of scientific correctness.

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

An Android application foundation has been adapted from Astronaut and rebranded for Molecularis. The app includes the Compose interface, encrypted Room persistence, local retrieval, model management and Android voice components. Library preserves original PDFs up to the 5,000-page processing ceiling; Knowledge Pool performs page-by-page on-device OCR in bounded batches and stores page-aware passages, metadata candidates, chapter/topic candidates and a transparent readiness score. A 25-million-character safety ceiling also applies; processing remains foreground-only and needs device stress testing.

Offline chat and Teaching Studio retrieve matching passages only from professor-reviewed Knowledge Pool sources and include book/page/passage labels in the local model prompt. This is simple lexical retrieval, not a guarantee of completeness or scientific correctness. The Teaching Studio prepares an editable, level-aware outline with retrieved textbook passages. When a compatible LiteRT-LM model is loaded, it can optionally draft a longer explanation using those local excerpts; the excerpts are retained with the draft and professor verification is required. Lessons are saved in the encrypted local database. Numbered outline sections become a navigable slide preview, and the professor can manually narrate each slide with an installed Android TTS voice.

A validated biochemical diagram schema and XML-escaped SVG renderer are integrated into Teaching Studio as a progressive lesson-flow preview derived from the professor's outline. The diagram can reveal lesson sections step by step; it is not yet a biochemical reaction editor and does not fabricate pathway chemistry. Rich slide authoring and export, diagram pan/zoom and pathway templates, automatic narration timelines, background book ingestion and scheduled autonomous teaching remain open. Phase 1 ingestion and Knowledge Pool processing has passed Android unit tests and lint in GitHub Actions. Phase 2 is in progress: topic-to-passage provenance is being added and tested. Physical-device, offline-mode and professor acceptance testing have not yet been performed. Settings now has separate cards for appearance, font family, colour palette, custom background image, chat/AI behaviour, speech/voice and privacy. A fingerprint/strong-biometric app lock with device-credential fallback is implemented; cloud account sign-in remains unconfigured because the project has no authentication backend/provider yet. Physical-device, offline-mode and professor acceptance testing have not yet been performed.
