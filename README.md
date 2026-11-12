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

The architecture is intentionally modular, but implementation will begin with a small, buildable Android app and grow through tested vertical slices.

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

The first milestone is deliberately small: **import one PDF, extract it, search a topic and save a structured teaching outline.**

## Project documentation

- [Product vision and North Star](docs/PRODUCT_VISION.md)
- [Development roadmap](docs/ROADMAP.md)
- [Proposed architecture](docs/ARCHITECTURE.md)

## Development rule

All development is performed directly on the main branch. Keep changes small, tested and documented. Do not claim offline capability until it has been verified on a real Android device with the required local resources installed.

## Content and privacy

Import only books and materials you are authorized to store and process. Images found online are not automatically free to reuse; retain rights information and cache assets only when permitted. Local materials remain on-device by default. Optional API requests are explicit and should send only the minimum context needed.

## Current status

Planning and architecture documentation. Android application implementation has not started yet.
