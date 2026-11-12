# Astronaut Reuse Review

Reviewed repository: https://github.com/AssayFlux/Astronaut

Astronaut is the owner's separate Android/Kotlin project and is licensed under MIT. Its license permits reuse subject to preserving the required copyright and license notice in copies or substantial portions. Any ported source must retain the applicable notice, and dependencies must be checked independently.

## Reuse candidates

| Astronaut area | Potential Molecularis use | Decision |
|---|---|---|
| Room database and migration patterns | Schema versioning, DAO/repository patterns and local persistence | Reuse patterns; design a new Molecularis schema |
| OfflineKnowledge document reader | SAF-based imports, PDF page handling, OCR and bounded extraction | Review and adapt the extraction approach; add page-aware PDF text extraction and larger-book processing limits |
| LocalRagIndex | Deterministic local BM25 retrieval and chunking | Strong candidate for a first retrieval prototype; prefer persistent SQLite FTS5 for the production library |
| PersistentHybridRag / LocalEmbeddings | Optional semantic retrieval | Defer until a compatible embedding model and device performance are validated |
| OfflineVoiceController | Local TTS voice discovery and offline speech readiness checks | Strong candidate for the voice adapter; test on supported Android versions and OEM speech engines |
| OpenAiCompatibleClient | Optional external model provider | Reuse the provider-boundary idea; re-check secret storage, request minimization and endpoint safety before porting |
| LiteRT-LM runtime adapter | Optional on-device generation | Evaluate after a small Android proof of concept and memory profiling |
| WorkManager usage | Background import, indexing and model downloads | Reuse the scheduling pattern, but use Android-compliant foreground media playback for active lectures |

## Do not copy blindly

- Astronaut is an AI messenger; Molecularis needs a teaching/lesson domain model and synchronized presentation timeline.
- Existing PDF OCR limits and extraction behavior are not automatically suitable for full textbooks. Benchmark large documents and preserve page/chapter boundaries.
- Android TTS being available does not guarantee that a selected voice works offline. Check each voice's network requirement and installed language pack.
- A catalog format or model file does not prove that an on-device runtime can execute it. Require a real runtime adapter and physical-device test.
- Do not copy application IDs, package names, branding, unrelated chat UI, model catalogs or backend assumptions.
- Do not copy any dependency without checking its current license, Android compatibility, maintenance status and APK impact.

## Reuse process

1. Keep Astronaut unchanged.
2. Port only a narrowly scoped component when Molecularis reaches the relevant roadmap phase.
3. Preserve MIT notices for reused source.
4. Adapt package names and interfaces to Molecularis domain contracts.
5. Add Molecularis-specific unit tests and physical-device tests.
6. Record the source file, original license and modifications in the relevant code header or third-party notices.

The goal is to reuse proven engineering work where it saves time, not to make Molecularis a fork of Astronaut.
