# Molecularis — Development Roadmap

This roadmap is outcome-based. Complete and validate one usable vertical slice at a time. Estimates are intentionally omitted until the first Android build and device constraints are known.

## Phase 0 — Product and engineering foundation

**Goal:** agree on scope and create a reliable Android project foundation.

- [x] Set Android minSdk 26 and targetSdk 35 (confirm supported device range through physical-device testing).
- [x] Inspect reusable Astronaut components and record license/dependency decisions.
- [x] Create Kotlin + Jetpack Compose Android project and Gradle wrapper.
- [x] Establish package structure, navigation shell, theme and settings.
- [x] Organize settings into separate appearance, chat/AI, speech/voice, privacy and account/security cards.
- [x] Add font-family, colour palette, dark appearance and custom background-image preferences.
- [x] Add a local PIN/password app lock using a salted PBKDF2 verifier encrypted by an Android Keystore AES-GCM key; optional strong biometric/device-credential unlock is available as a convenience. Physical-device security validation remains open.
- [ ] Configure a real account authentication provider and backend; local-only mode must remain usable without sign-in.
- [x] Add Room database, migrations and local repositories (automated migration coverage remains to be expanded).
- [x] Add GitHub Actions Android unit-test and lint workflow.
- [x] Document local build and install instructions in [BUILD_AND_INSTALL.md](BUILD_AND_INSTALL.md).

**Exit criteria:** clean debug APK build, app launches on a physical Android device, database initializes and CI runs.

## Phase 1 — Book library and ingestion

**Goal:** import a book and make its content usable offline.

- [x] Add SAF-based document picker and Library screen that preserves the original PDF before processing.
- [x] Add PDF page extraction through Android PDF rendering and on-device OCR; EPUB/DOCX remain deferred.
- [x] Add on-device OCR for PDF pages (currently used for all pages; direct text-layer extraction is a future improvement).
- [x] Raise the per-book PDF limit to 5,000 pages and stream OCR page-by-page into bounded Room batches.
- [x] Persist original book metadata in Room; extracted content is now created separately in Knowledge Pool.
- [x] Preserve PDF page numbers in extracted passage records (chapter-boundary detection remains open).
- [x] Normalize and chunk extracted text into page-aware passages.
- [ ] Move Knowledge Pool processing to resumable WorkManager jobs with cancellation/recovery. Current foreground processing now writes to a hidden staging book and atomically swaps passages only after successful full extraction; failed/cancelled re-analysis preserves the previous passage set and reviewed source. Abandoned staging rows left by process death are reclaimed after seven days; WorkManager persistence and resume remain open.
- [x] Add import progress/error feedback and clean up partially imported book rows/files on failure.
- [x] Add textbook deletion with Room cascade and local PDF file cleanup.
- [ ] Add duplicate detection and safe reimport/replace workflow.

**Current status:** Library stores the selected original PDF unchanged. Knowledge Pool now performs on-device page OCR after the professor explicitly starts processing, writes passages in bounded batches, detects conservative bibliographic metadata and possible chapter/topic headings, calculates a heuristic readiness score, and provides professor review/approval. The current 5,000-page and 25-million-character limits apply. Processing is foreground-only; resumable WorkManager processing, duplicate detection, progress recovery and direct PDF text-layer extraction remain open.

**Exit criteria:** a professor can import a permitted PDF, inspect extraction status and retrieve its extracted text while offline.

## Phase 2 — Topic organization and local knowledge base

**Goal:** turn book content into a browsable biochemistry knowledge library.

- [x] Detect likely chapter and section headings (heuristic; professor review remains required).
- [x] Organize topics into a hierarchy with aliases, duplicate detection, merge tools and cycle protection.
- [x] Provide professor review controls for source metadata and topic candidates, including manual topic creation and editing.
- [x] Keep the compatible SQLite FTS4 index with book/page filters; FTS5 is deferred until Android SQLite compatibility can be guaranteed.
- [x] Audit page coverage, empty/short pages and repeated OCR pages.
- [x] Retrieve page-labelled passages from professor-reviewed Knowledge Pool sources in offline chat prompts (lexical retrieval; scientific verification remains essential).
- [x] Link topic sections to exact OCR passage IDs and page locations using explicit provenance records.
- [ ] Wire optional local embeddings into ingestion and search after model/runtime/device validation (embedding primitives exist but are not part of the default path).
- [ ] Prepare professor-curated, source-cited evaluation datasets with validation and holdout splits; never auto-train on raw OCR.
- [ ] Keep fine-tuning optional and explicit; verify service security, dataset rights and evaluation before model use.
- [ ] Add a small curated biochemistry starter taxonomy, subordinate to the professor's books.

**Current status:** topic-to-passage provenance and topic review are implemented. The phase's source-processing and database changes passed Android unit tests and lint. Semantic embeddings, curated scientific evaluation and professor acceptance testing remain future work; keyword retrieval is not a substitute for scientific validation.

**Exit criteria:** topic search returns relevant passages from reviewed sources and the professor can correct topic organization. Retrieval relevance and scientific correctness still require evaluation against the professor's supplied textbooks.

## Phase 3 — Teaching flow engine

**Goal:** convert a selected topic into a useful lecture plan.

- [x] Define initial audience profiles: MBBS, MD / DNB and PhD.
- [x] Add an editable lesson structure with audience-specific minute budgets that sum to the selected duration.
- [x] Assemble matching local textbook passages into the lesson outline using keyword retrieval.
- [x] Add an editable template for objectives, prerequisites, explanation, mechanism, regulation, clinical connections, recap and questions (this is a scaffold, not AI-authored scientific teaching).
- [x] Connect Teaching Studio to the installed LiteRT-LM local model and gate generation on a successfully loaded model.
- [x] Reuse the optional external AI provider settings and encrypted API-key storage for chat; Teaching Studio's source-grounded draft currently uses the local model only.
- [x] Add outline editing, local save/update, reopen, delete, deterministic re-preparation and saved-lesson duplication.
- [x] Unit-test source quality gates and audience-specific time allocation.
- [ ] Evaluate with professor-reviewed sample topics and the supplied biochemistry textbooks.
- [x] Add a conservative OCR-usability gate for approved sources and lock local AI drafting unless eligible reviewed passage blocks are attached. This is not a scientific-accuracy score.

**Current status:** Teaching Studio now filters to professor-approved sources, screens extraction usability (page-text coverage >=35% and a heuristic score >=55/100), reports source usability, prefers approved topic/alias passage links and falls back to indexed lexical search. AI drafting is disabled when no eligible source passage is attached. Audience-specific section time budgets sum to the requested duration. Saved lessons can be updated in place or duplicated. The local LiteRT-LM model remains optional and is not bundled. The extraction score is not a scientific-accuracy score; generated content still requires professor review against the original books.

**Exit criteria:** a topic plus audience level produces an editable, coherent teaching flow grounded in the imported library. No API key is required for the local/search-based experience.

## Phase 4 — Slides and presentation player

**Goal:** make a prepared lesson presentable in a classroom.

- [x] Convert numbered lesson-outline sections into an initial local slide model (outline-derived; rich manual slide authoring remains open).
- [ ] Build multiple slide layouts and finish typography/accessibility rules across screen sizes.
- [x] Add an in-app slide preview with previous/next navigation and three selectable themes (full-screen presenter mode and timing remain open).
- [x] Add per-slide offline TTS playback (manual slide-by-slide narration; automatic timeline synchronization remains open).
- [x] Extract deterministic slide conversion into a testable component with unit tests.
- [x] Add offline PDF export with one landscape slide per page.
- [x] Add editable PPTX export using native PowerPoint text shapes and a unit-tested Open XML package.
- [ ] Add editable speaker notes and slide-to-lesson segment mapping.
- [ ] Validate PDF/PPTX rendering in Android document providers and common presentation viewers on physical devices.

**Current status:** the Teaching Studio now offers Classic, Midnight and Botanical themes, offline PDF export, and editable PPTX generation from the outline-derived slide model. Export actions use Android's document-creation flow, so the professor chooses where each file is saved. PPTX text remains editable in presentation software. The generated files have source-level/package tests, but viewer compatibility, typography on real devices, speaker notes, richer layouts and full-screen presenter controls still require validation and implementation. The generated slides remain a formatting of the professor-edited outline, not independently verified scientific content.

**Exit criteria:** a saved lesson can be presented offline and exported as usable PDF and editable PowerPoint files on validated Android devices.

## Phase 5 — Scientific SVG diagram engine

**Goal:** explain biochemical mechanisms visually, step by step.

- [x] Define an initial structured diagram schema for nodes, labels, connections and reveal steps (compartments and reaction-specific semantics remain open).
- [x] Build a safe SVG generator from supported primitives with XML-escaped labels and bounded inputs.
- [x] Build SVG rendering with pinch zoom and two-axis pan in the isolated WebView preview (physical-device gesture validation remains open).
- [x] Add ordered reveal steps with progressive node/connection reveal; timed animation remains open.
- [x] Create reusable metabolic pathway, reaction mechanism, feedback regulation and molecular interaction templates with typed biochemical nodes and edges.
- [x] Add Wikimedia Commons image search restricted to HTTPS raster thumbnails with declared license metadata; cache bounded JPEG/PNG/WebP files locally with a JSON sidecar containing source, license, attribution and SHA-256.
- [ ] Link diagram steps to slide and narration segments (scheduled for Phase 6).

**Current status:** the diagram engine now has four reusable, typed templates (metabolic pathway, reaction mechanism, feedback regulation and molecular interaction), explicit node positions and biochemical roles, reaction/activation/inhibition/binding/transport edges, coordinate and topology validation, escaped SVG rendering, progressive reveal, and pinch-zoom/two-axis pan in a JavaScript-disabled WebView. Teaching Studio exposes editable component names and enzyme/reaction labels. Templates are structural teaching aids, not chemically validated reaction models; physical-device gesture checks, richer node/edge editing, domain-specific stoichiometry/compartments, and slide/narration synchronization remain open. Commons image search is optional; only results with declared license metadata are shown, and cached assets retain their attribution/license sidecar. Image insertion into diagram nodes and license-specific reuse review remain open.\n\n**Exit criteria:** at least one pathway can be generated from structured components and revealed in sync with its explanation.

## Phase 6 — Voice lecture and synchronization

**Goal:** let Molecularis deliver a prepared lecture aloud.

- [x] Reuse voice selection and preview in the app settings.
- [x] Reuse Android local-voice readiness checks and add long-script narration to the Teaching Studio (device voice-pack validation remains open).
- [ ] Add narration pacing, pauses, pronunciation dictionary and emphasis controls.
- [ ] Synchronize narration with slide changes and SVG reveal events.
- [x] Add manual per-slide narration using the installed Android TTS voice.\n- [ ] Add play, pause, resume, seek and stop controls.
- [ ] Add audio focus, interruption handling and headset/Bluetooth tests.
- [ ] Add optional local speech engine only after device and license evaluation.

**Current status:** the Teaching Studio can read its current outline aloud using an installed Android offline TTS voice, splitting long scripts into queued chunks. A presenter can manually request offline TTS for the current slide. Automatic narration timelines, pause/resume/seek, and diagram synchronization remain open.

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

## Large-book import update

The importer accepts PDFs up to 5,000 pages. OCR is performed sequentially and each page's chunks are written in batches of at most 250 passages, avoiding the previous design's full-book text and full-book passage lists in memory. Partial database rows and copied files are cleaned up on failure and cancellation. The import is still a foreground coroutine: keep Molecularis open during import. The 25-million-character ceiling is an additional safety bound, so 5,000 pages is a maximum page count, not a guarantee that every PDF of that size will fit every device. A 5,000-page real-world stress test is still required on representative Android hardware.

## First milestone status

The first vertical slice is implemented in the repository: **import one PDF → extract page text with on-device OCR → search local passages → prepare and edit a structured lesson outline → preview outline-derived slides → save and reopen the lesson → read the outline aloud with Android TTS.** The earlier baseline commit passed unit tests, lint and debug APK assembly. The 5,000-page importer, progressive lesson diagram and cancellation-safe cleanup commits have CI runs queued or in progress; do not treat those commits as verified until their workflows finish. A physical-device/offline acceptance test has not yet been performed. This remains a foundation; it is not yet an AI-generated lecture or a synchronized slide-and-voice presentation.

## Delivery discipline

- Work directly on the main branch only.
- Re-read the current main state before each change.
- Keep commits small and buildable.
- Add tests with each data or processing feature.
- Do not claim a feature is offline until it has been tested with airplane mode enabled and required local assets installed.
- Record device-dependent limitations rather than hiding them.
