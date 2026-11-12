# Molecularis — Development Roadmap

This roadmap is outcome-based. Complete and validate one usable vertical slice at a time. Estimates are intentionally omitted until the first Android build and device constraints are known.

## Phase 0 — Product and engineering foundation

**Goal:** agree on scope and create a reliable Android project foundation.

- [ ] Confirm minimum Android version and target device range.
- [ ] Inspect reusable Astronaut components and record license/dependency decisions.
- [ ] Create Kotlin + Jetpack Compose Android project and Gradle wrapper.
- [ ] Establish package structure, navigation shell, theme and settings.
- [ ] Add Room database, migrations and repository tests.
- [ ] Add GitHub Actions build and unit-test workflow.
- [ ] Document local build and install instructions.

**Exit criteria:** clean debug APK build, app launches on a physical Android device, database initializes and CI runs.

## Phase 1 — Book library and ingestion

**Goal:** import a book and make its content usable offline.

- [ ] Add SAF-based document picker and library screen.
- [ ] Support PDF text extraction first; add EPUB/DOCX only after library and licensing review.
- [ ] Detect scanned PDFs and add on-device OCR as a separate processing path.
- [ ] Persist book/document metadata and processing state in Room.
- [ ] Preserve page numbers and chapter boundaries where available.
- [ ] Clean and chunk extracted text without losing scientific notation.
- [ ] Add resumable background processing and progress/error UI.
- [ ] Add delete/reimport behavior and derived-data cleanup.

**Exit criteria:** a professor can import a permitted PDF, inspect extraction status and retrieve its extracted text while offline.

## Phase 2 — Topic organization and local knowledge base

**Goal:** turn book content into a browsable biochemistry knowledge library.

- [ ] Detect headings, chapters and likely topic/subtopic labels.
- [ ] Build a topic tree with aliases and duplicate-topic merging.
- [ ] Add professor review/edit tools for topic assignments.
- [ ] Add SQLite FTS5 keyword search and filters.
- [ ] Link topic pages to relevant content chunks and page locations.
- [ ] Add optional local embeddings only after runtime and device tests.
- [ ] Add a small curated biochemistry topic taxonomy as a starter, not as a replacement for the professor's books.

**Exit criteria:** topic search returns relevant passages from imported material and the professor can correct the organization.

## Phase 3 — Teaching flow engine

**Goal:** convert a selected topic into a useful lecture plan.

- [ ] Define audience profiles: MBBS, MD, DNB and PhD.
- [ ] Define lesson structure and time-budgeting rules.
- [ ] Build retrieval-to-lesson context assembly.
- [ ] Create prompt/templates for objectives, prerequisites, explanation, mechanism, regulation, clinical connections, recap and questions.
- [ ] Add local-model provider interface and capability checks.
- [ ] Add optional external AI provider settings and secure key storage.
- [ ] Add edit, regenerate, save and duplicate lesson workflows.
- [ ] Test with professor-reviewed sample topics and different audience levels.

**Exit criteria:** a topic plus audience level produces an editable, coherent teaching flow grounded in the imported library. No API key is required for the local/search-based experience.

## Phase 4 — Slides and presentation player

**Goal:** make a prepared lesson presentable in a classroom.

- [ ] Convert lesson segments into slide data.
- [ ] Build slide themes, layouts and readable typography.
- [ ] Create an in-app slide player with presenter controls.
- [ ] Add PDF export as the first dependable offline export.
- [ ] Implement and validate editable PPTX export on Android.
- [ ] Add speaker notes and slide-to-lesson segment mapping.

**Exit criteria:** a saved lesson can be presented offline and exported as a usable presentation file.

## Phase 5 — Scientific SVG diagram engine

**Goal:** explain biochemical mechanisms visually, step by step.

- [ ] Define structured diagram schema for nodes, labels, arrows, compartments and reactions.
- [ ] Build a safe SVG generator from those components.
- [ ] Build SVG rendering, zoom and pan.
- [ ] Add ordered reveal steps and animation timing.
- [ ] Create first reusable templates: metabolic pathway, reaction mechanism, feedback regulation and molecular interaction.
- [ ] Add curated online image search and permitted local caching with rights metadata.
- [ ] Link diagram steps to slide and narration segments.

**Exit criteria:** at least one pathway can be generated from structured components and revealed in sync with its explanation.

## Phase 6 — Voice lecture and synchronization

**Goal:** let Molecularis deliver a prepared lecture aloud.

- [ ] Add voice selection and preview.
- [ ] Add text-to-speech adapter and offline voice readiness check.
- [ ] Add narration pacing, pauses, pronunciation dictionary and emphasis controls.
- [ ] Synchronize narration with slide changes and SVG reveal events.
- [ ] Add play, pause, resume, seek and stop controls.
- [ ] Add audio focus, interruption handling and headset/Bluetooth tests.
- [ ] Add optional local speech engine only after device and license evaluation.

**Exit criteria:** a prepared lesson plays with understandable voice, slides and diagram steps synchronized, including offline operation on a validated device/voice pack.

## Phase 7 — Autonomous and scheduled teaching

**Goal:** allow a professor to schedule a topic, duration and audience and have the app run the prepared session.

- [ ] Add lecture scheduler with date/time, topic, audience, duration and language.
- [ ] Require lesson generation and media readiness before scheduling.
- [ ] Add preflight checks for storage, voice pack, battery and required permissions.
- [ ] Use Android-compliant scheduling and foreground media playback.
- [ ] Add visible notifications, start/stop controls and recovery after process interruption.
- [ ] Record completion, interruption and failure state.
- [ ] Test across Android versions and representative OEM battery policies.

**Exit criteria:** a scheduled, prepared lecture starts and completes on validated devices when required permissions and system conditions are met; failures are visible and recoverable.

## Phase 8 — Quality, performance and release

**Goal:** make Molecularis dependable for real teaching.

- [ ] Test extraction on representative high-quality and scanned textbooks.
- [ ] Professor-review factual clarity and level adaptation across MBBS, MD, DNB and PhD.
- [ ] Test scientific notation, equations, subscripts, Greek letters and pathway labels.
- [ ] Profile large books, indexing, model memory, battery and thermal behavior.
- [ ] Test airplane-mode workflows and network-disabled API behavior.
- [ ] Audit permissions, local data deletion, SVG sanitization and API secret storage.
- [ ] Add accessibility, font scaling and landscape presentation support.
- [ ] Prepare signed release, backup/export guidance and crash diagnostics with privacy controls.

**Exit criteria:** documented device matrix, passing automated tests, professor acceptance of sample lectures and a reproducible release build.

## Recommended first milestone

Do not begin with autonomous teaching or a large local model. First build this thin vertical slice:

**Import one PDF → extract text → search for one topic → display relevant passages → create a structured lecture outline → save it.**

This validates the core data pipeline before adding generation, voice, slides and diagrams.

## Delivery discipline

- Work directly on the main branch only.
- Re-read the current main state before each change.
- Keep commits small and buildable.
- Add tests with each data or processing feature.
- Do not claim a feature is offline until it has been tested with airplane mode enabled and required local assets installed.
- Record device-dependent limitations rather than hiding them.
