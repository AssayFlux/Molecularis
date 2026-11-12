# Molecularis — Product Vision

## North Star

**Make excellent biochemistry teaching available whenever and wherever students need it — whether the professor is present or Molecularis is delivering the lesson.**

Molecularis is a professor-led, Android-first biochemistry teaching assistant. It transforms the professor's selected books and teaching materials into an organized reusable offline knowledge base, then turns a topic into a clear teaching flow, visual presentation and spoken lecture.

The product is judged by one outcome: **does the student understand the biochemistry better after the session?**

## Who it serves

- The professor, who curates the library, chooses the topic, audience and duration, and controls the teaching style.
- MBBS students, who need clear foundations, mechanisms and clinically meaningful connections.
- MD and DNB students, who need deeper biochemical reasoning and clinical application.
- PhD students, who need mechanistic depth, molecular detail and links between concepts.

## Core experience

1. The professor imports books and study materials they are entitled to use.
2. Molecularis extracts and organizes the content into subjects, topics and subtopics.
3. The professor selects a topic, student level, language and time.
4. Molecularis creates a coherent lecture plan and speaking script.
5. It prepares slides and assembles scientific diagrams from reusable SVG components.
6. It can present the lesson with synchronized voice narration and progressive diagram reveals.
7. The professor can edit, save, replay, export or schedule a teaching session.

## Product principles

- **Professor-controlled:** the professor chooses the source library, topic, depth, duration and final teaching style.
- **Understanding before volume:** explain concepts in a logical sequence; do not dump extracted textbook paragraphs.
- **Offline-first:** imported materials, topic search, saved lessons and prepared presentations remain available without internet.
- **Optional AI connectivity:** a local model is the preferred offline generation path; external AI APIs are optional and explicitly enabled.
- **Visual explanation:** pathways and mechanisms should be built and revealed step by step, not merely shown as dense static images.
- **Honest capability:** show when a local model, offline voice, image or export capability is unavailable. Never silently switch to a cloud service.
- **Fast to use:** the professor should be able to move from topic selection to a usable teaching plan with minimal setup.
- **Respect content rights:** import only materials the user is authorized to process; retain image/source licensing metadata for asset management even when lecture slides do not display citations.

## Product boundaries

Molecularis is not intended to be:
- A general-purpose chatbot or a replacement for the professor.
- A literature review or citation-management system.
- A mandatory cloud service or account-based platform.
- A medical diagnosis or treatment decision system.
- A system that indiscriminately downloads or republishes copyrighted books, figures or images.

References need not clutter the lecture. Internally, however, the app should retain enough source and rights metadata to help the professor identify imported material and manage visual assets responsibly.

## Success measures

- A professor can import a supported book and find its content by topic.
- A selected topic produces a coherent, level-appropriate teaching flow.
- The same topic can be adapted for MBBS, MD, DNB and PhD audiences.
- A prepared lesson can be replayed offline with voice and slides.
- A scientific pathway can be revealed progressively in sync with narration.
- A scheduled session starts reliably when Android permits it and clearly reports any permission or battery restriction.
- The app remains useful without an API key or internet connection after required local models and assets are installed.

## First release definition

The first useful release is deliberately narrow: import a PDF, organize its text into searchable topic chunks, select a topic and student level, generate an editable teaching outline, and present it with slides and device-supported voice. Advanced local LLM inference, semantic retrieval, sophisticated SVG animation and unattended scheduled teaching follow in later milestones.
