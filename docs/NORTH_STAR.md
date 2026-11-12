# Molecularis — North Star

## The destination

Molecularis is a personal, dependable biochemistry teaching assistant for the Android device. It helps a professor turn trusted biochemistry learning material into clear, memorable teaching—and, when asked, can teach a prepared lesson aloud with synchronized slides and scientific diagrams.

The product succeeds when a professor can move from **“I need to teach this topic”** to a coherent, accurate, engaging lesson with as little friction as possible, even without an internet connection.

## Who it serves

The primary user is a biochemistry professor teaching learners across MBBS, MD, DNB and PhD levels. The same scientific topic must be explainable at different depths: from foundational clinical understanding to advanced mechanisms and research-level nuance.

Students are the audience for lessons. The professor remains in control of source material, level, emphasis, duration and delivery.

## The core experience

1. **Build a trusted library.** Import textbooks, notes, lecture files and other materials supplied by the professor. Keep original files on-device and preserve useful structure such as chapters, pages, tables and figures.
2. **Understand and organize.** Extract text, recognize scanned pages when needed, and organize content into subjects, topics, subtopics and concepts. Make the local library searchable.
3. **Prepare to teach.** Given a topic, learner level and available time, create a logical teaching flow: prerequisites, learning objectives, explanation, mechanisms, clinical relevance, examples, misconceptions, recap and questions.
4. **Make science visible.** Build clear scientific diagrams from structured, reusable SVG elements. Reveal pathways and labels progressively as the explanation unfolds.
5. **Teach with voice and slides.** Let the professor present manually or ask Molecularis to deliver a prepared lesson using narration and synchronized slides. The professor can pause, resume, navigate and intervene.
6. **Improve the lesson.** Allow review and editing of teaching flows, slides, diagrams and narration before delivery.

## Product principles

- **Scientific understanding first.** Optimize for conceptual clarity, causal reasoning and useful explanation—not for producing long blocks of text.
- **Professor-directed.** The professor chooses the topic, level, time, source library and teaching intent. Generated material is editable and never presented as infallible.
- **Offline by default.** Core library, search, lesson preparation and playback should work locally wherever technically feasible. Network-dependent features must be explicit.
- **Trusted materials.** Use the professor's supplied sources as the foundation. Clearly distinguish source-grounded content from general model knowledge internally.
- **Right depth for the learner.** MBBS, postgraduate and doctoral explanations should differ in vocabulary, detail, assumptions and emphasis.
- **Visual and auditory teaching.** Slides, diagrams and narration are one coordinated lesson—not disconnected outputs.
- **Fast and dependable.** Import and indexing may take time, but everyday teaching workflows should be responsive, recoverable and predictable.
- **Privacy and ownership.** Keep books and personal teaching materials on-device by default. Never upload them to an external service without clear, informed permission.
- **Honest capability.** SQLite stores and retrieves knowledge; it does not generate explanations by itself. Local generation requires a compatible on-device model. If a model or offline voice is unavailable, say so plainly.
- **Respect rights.** Track provenance and reuse permissions for imported and externally sourced media. Do not assume that an image found online is free to reuse.

## The product boundary

Molecularis is not intended to be a generic chatbot, a replacement for the professor, a medical decision-support system, or an unreviewed textbook generator. It is a teaching workspace that helps a professor understand, structure, visualize and deliver biochemistry lessons.

It must not invent source quotations, fabricate references, conceal uncertainty, or silently send private material to a cloud provider.

## Experience standards

A successful lesson should:
- state clear learning objectives and establish prerequisites;
- explain mechanisms in a sequence that makes causal relationships understandable;
- define unfamiliar terms and explain important abbreviations;
- connect molecular mechanisms to physiology, pathology and clinical relevance when appropriate;
- use accurate, legible diagrams that reveal progressively;
- match its duration and depth to the professor's settings;
- finish with a concise synthesis and useful retrieval questions;
- remain editable and reviewable before autonomous delivery.

## Technical direction

- Native Android application using Kotlin and Jetpack Compose.
- Room/SQLite for structured local data, with full-text search as the dependable baseline.
- Original PDFs and media stored as files or document URIs, not as large database blobs.
- A modular content-ingestion pipeline for PDF text extraction, OCR, metadata and topic organization.
- A lesson domain model that separates content, slides, diagram states, narration and timing.
- A local AI provider abstraction; optional remote providers only with explicit user consent.
- Android text-to-speech as an initial voice path, with offline voice availability checked on the device.
- Background work for import, indexing and model downloads; foreground media playback for active lessons.
- Automated tests for ingestion, retrieval, lesson structure, diagram timelines and critical UI state.

Astronaut is the source project for reusable implementation and interface patterns. Molecularis may reuse its code and UI broadly, while adapting package identity, branding, navigation, data models and workflows to this teaching mission. Retain third-party notices and licence obligations for all reused components.

## First meaningful milestone

A professor can import a PDF, see its extracted content, search for a biochemistry topic, inspect relevant passages, generate and edit a structured teaching outline, and save that outline locally. This is the first end-to-end workflow on which later slides, diagrams, voice and autonomous teaching will build.

## Long-term measure of success

Molecularis becomes the professor's reliable teaching companion: a well-organized local knowledge library and a capable lesson studio that can prepare and deliver scientifically sound, level-appropriate biochemistry teaching—anytime, anywhere, with the professor in control.
