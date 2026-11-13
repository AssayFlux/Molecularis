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
- Schedule saved lessons for offline narration with WorkManager, foreground notifications, stop controls and visible completion/failure history.
- Schedule prepared teaching sessions, subject to Android background-execution and permission limits.
- Work offline after books, models, voice packs and other required assets are available.
- Optionally connect external AI providers; cloud use is never mandatory or silently enabled.

## Platform direction

- Android application: Kotlin + Jetpack Compose.
- Structured local data: Room / SQLite.
- Book and media files: app-private storage or user-selected document locations.
- Search: SQLite full-text retrieval with optional local semantic retrieval components.
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
- [Device acceptance and release checklist](docs/DEVICE_ACCEPTANCE.md)
- [Proposed architecture](docs/ARCHITECTURE.md)
- [Astronaut code and UI reuse record](docs/ASTRONAUT_REUSE.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## Development rule

All development is performed directly on the main branch. Keep changes small, tested and documented. Do not claim offline capability until it has been verified on a real Android device with the required local resources installed.

## Content and privacy

Import only books and materials you are authorized to store and process. Images found online are not automatically free to reuse; retain rights information and cache assets only when permitted. Local materials remain on-device by default. Optional API requests are explicit and should send only the minimum context needed.

## Current status

The Android foundation, encrypted local persistence, Library/Knowledge Pool separation, page-linked OCR passages, professor review flow, lesson planning, slide preview and PDF/PPTX exports are implemented. Knowledge Pool OCR uses foreground WorkManager with transactional per-page checkpoints and restart recovery; the current limits are 5,000 pages and 25 million extracted characters. Search is local lexical retrieval with optional local semantic components and still needs professor-curated relevance evaluation.

Teaching Studio supports editable saved lessons, audience levels, structured SVG diagrams with progressive reveal, diagram edit persistence, synchronized slide narration, Android audio-focus handling and a local biochemical pronunciation dictionary. Diagram templates are structural aids, not scientifically validated pathway models. Android TTS quality and offline availability depend on the installed device voice pack.

The Schedule screen stores saved-lesson sessions in encrypted Room and uses delayed WorkManager foreground playback, offline-voice selection, notification controls and completion/interruption/failure states. WorkManager timing is inexact and may be deferred by Doze or OEM policies; playback restarts from the beginning after process interruption. Audience and duration are stored as session metadata and do not guarantee a fixed runtime or automatic content regeneration.

The repository CI workflow runs unit tests, lint, builds a debug APK and uploads a 14-day artifact. Production signing, physical-device/OEM acceptance, airplane-mode verification, large-book performance profiling and professor review against licensed textbooks remain open. Local crash diagnostics are opt-in, stored on-device, omit user content and are never uploaded. Cloud authentication is not configured; cloud AI is optional and requires explicit setup.

**Release gate:** a successful CI debug build is not a production release. Complete the manual checks in [DEVICE_ACCEPTANCE.md](docs/DEVICE_ACCEPTANCE.md), provide licensed scientific references for professor review, and configure the production signing key as private CI secrets before signing a release.
