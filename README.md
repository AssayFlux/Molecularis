# Molecularis

**An offline-first Android workspace for document-grounded learning and knowledge work.**

Molecularis combines local document ingestion, human-reviewed knowledge organization, source-aware retrieval, and AI-assisted teaching workflows. It is evolving from a biochemistry-oriented prototype toward a configurable, multi-subject learning workspace.

> **Research status:** active software project and research prototype. This repository is not a completed study or a validated educational intervention. Read [current limitations](docs/LIMITATIONS.md) and [research readiness](docs/RESEARCH_READINESS.md) before making claims.

## North Star

Let people build a trustworthy learning workspace from sources they are authorized to use—while keeping evidence, provenance, uncertainty, privacy, and user control visible.

A subject workspace is intended to contain:
- User-defined subject scope and learning context.
- Multiple configurable professor/teaching profiles (configuration profiles, not separately trained models).
- Original source files and a separately managed, human-reviewed Knowledge Pool.
- Page- and passage-level provenance.
- Subject-scoped conversations, lessons, projects, and scheduled teaching.
- Reproducible records of model, prompt, retrieval, source-set, and generation configuration.

See [North Star](docs/NORTH_STAR.md), [Product Vision](docs/PRODUCT_VISION.md), and [Roadmap](docs/ROADMAP.md).

## Current implementation

The Android app currently includes:
- Kotlin and Jetpack Compose application architecture.
- Local PDF library and page-aware OCR/extraction workflow.
- Resumable background processing with WorkManager and bounded database writes.
- Human-reviewed Knowledge Pool topics, aliases, and topic-to-passage provenance.
- First-class subject workspace and professor profile records, with create/select/edit flows.
- Subject-scoped library, Knowledge Pool, chat, projects, saved lessons, and scheduled lectures.
- Subject-filtered lexical retrieval for imported source passages.
- Chat prompts composed from the active subject and selected professor configuration.
- Shared constructed prompt/context for local and configured remote chat inference.
- Per-answer metadata for provider/model, professor profile, prompt version/hash, retrieved source-set hash, and retrieval configuration.
- Teaching Studio lesson outlines, slides, narration, and export; biochemical pathway diagrams remain a specialist feature.
- Optional local or explicitly configured remote AI providers.

### Integration boundaries

The current subject-workspace integration is an initial implementation, not yet a complete general-purpose multi-domain platform:
- Existing records migrate into a default workspace named **My first subject**. New imports belong to the currently active subject.
- Existing Knowledge Pool records inherit scope through their source book; topic and passage records are reached through that book.
- Subject isolation is enforced in the principal library, chat, Knowledge Pool, project, lesson, and schedule paths. Instrumented tests are included; CI and migration validation must pass before treating the integration as release-ready.
- Workspace/profile deletion and archival are not yet provided. Professor-profile configuration is not model fine-tuning or training.
- The biochemical diagram editor remains biochemical-specific; other domains need their own validated optional domain packs.
- Cross-subject comparison is not implemented as a user-facing opt-in retrieval workflow.
- EvaluationRun records, full lesson source-set/model provenance, and automated research artifact manifests remain planned.

## Architecture and product documentation

| Document | Purpose |
|---|---|
| [Architecture](docs/ARCHITECTURE.md) | Application structure and data flow |
| [Information architecture](docs/INFORMATION_ARCHITECTURE.md) | Navigation and information model |
| [North Star](docs/NORTH_STAR.md) | Product destination and principles |
| [Product vision](docs/PRODUCT_VISION.md) | Intended user experience and boundaries |
| [Roadmap](docs/ROADMAP.md) | Phases, acceptance criteria, and gaps |
| [Multi-subject architecture](docs/MULTI_SUBJECT_ARCHITECTURE.md) | Implemented boundary and remaining design |
| [Data dictionary](docs/DATA_DICTIONARY.md) | Entities, invariants, and migration plan |
| [Build and install](docs/BUILD_AND_INSTALL.md) | Local development and Android build instructions |
| [Device acceptance](docs/DEVICE_ACCEPTANCE.md) | Physical-device validation checklist |
| [Astronaut reuse record](docs/ASTRONAUT_REUSE.md) | Reuse, attribution, and license decisions |

## Research and reproducibility

Research-oriented documents are maintained separately from product claims:
- [Research readiness and claims boundary](docs/RESEARCH_READINESS.md)
- [Current limitations](docs/LIMITATIONS.md)
- [Research governance, ethics, and integrity](docs/RESEARCH_GOVERNANCE.md)
- [Evaluation protocol](docs/EVALUATION_PROTOCOL.md)
- [Reproducibility standard](docs/REPRODUCIBILITY.md)
- [Human-participant study protocol template](docs/STUDY_PROTOCOL_TEMPLATE.md)
- [Manuscript template](research/MANUSCRIPT_TEMPLATE.md)
- [Annotation template](research/ANNOTATION_TEMPLATE.csv)
- [Research workspace guide](research/README.md)

The intended first paper should make a bounded system-design and technical-evaluation contribution. Educational effectiveness requires a separate, appropriately designed study. No accuracy, learning-gain, retention, safety, superiority, or generalization claim should be made without supporting evidence from a documented protocol.

## Build, test, and CI

See [BUILD_AND_INSTALL.md](docs/BUILD_AND_INSTALL.md). GitHub Actions runs Android unit tests, subject-isolation instrumentation tests on an emulator, lint, and debug APK assembly. A debug APK is not a signed production release. CI success does not establish physical-device compatibility, scientific correctness, security certification, or educational benefit.

## Contributing and security

- [Contributing guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy](SECURITY.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
- [Software citation metadata](CITATION.cff)

Contributions should include tests, migration considerations, documentation updates, and evidence for any capability claims. Do not commit secrets, private documents, participant data, unauthorized copyrighted material, or restricted model files.

## Content rights, privacy, and safety

Import only materials you are authorized to store and process. A user's access to a file does not automatically permit redistribution of the file or extracted text. Remote inference may transmit selected content to a configured provider; review provider terms and data flows before using sensitive material. Retrieved text is evidence to inspect, not executable instruction or guaranteed truth. In high-impact disciplines, Molecularis is an educational aid and not a substitute for qualified professional judgement.

## License

See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Third-party models, datasets, documents, and assets may have separate terms.
