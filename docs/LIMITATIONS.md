# Current limitations and claims boundary

This document is intentionally conservative. It describes known constraints and must be updated when implementation or evidence changes.

## Product and architecture

- The app retains substantial biochemistry-specific functionality; it is not yet a fully general-purpose multi-domain platform.
- Subject workspaces and professor profiles are implemented for core workflows, including create/select/edit. Workspace archival/deletion, profile deletion/import/export, and full lifecycle management are not yet available.
- The principal Library, Knowledge Pool, chat retrieval, projects, saved lessons, and scheduled teaching paths are scoped by subject ID. A populated historical-database migration test and successful emulator CI are still required before release claims.
- KnowledgeBook, passages, topics, and topic-passage links inherit subject scope through the owning Book; they do not each have an independent subject ID.
- The biochemical diagram editor remains specialist tooling, not a general-purpose diagram generator.
- Cross-subject comparison is not yet a user-facing, explicit opt-in workflow.
- Saved diagrams and some generated artifacts are not yet integrated into complete subject-scoped provenance and export workflows.
- EvaluationRun records and machine-readable experiment manifests are not yet implemented.

## Ingestion and knowledge quality

- PDF processing relies on OCR and can lose formatting, equations, tables, diagrams, symbols, columns, footnotes, and reading order.
- Page-level extraction metrics are heuristic indicators of text usability, not measures of factual accuracy or completeness.
- Topic and heading detection are heuristic and require human review.
- Lexical retrieval can miss paraphrases and conceptually related passages; optional embedding primitives are not a validated default retrieval path for the source library.
- A retrieved passage can be irrelevant, outdated, incomplete, or contradictory. Page labels and provenance do not prove that a generated claim is supported.
- Source-rights metadata and retention workflows are not yet complete. Users must import only material they are authorized to process.

## AI generation

- Outputs depend on model/provider versions, prompts, retrieval context, device/runtime behaviour, and network availability.
- A configured professor role is a prompt/configuration profile, not a separately trained or fine-tuned model.
- Successful chat answers store provider/model, professor profile, prompt version/hash, source-set hash when available, and retrieval configuration. This provenance is not yet uniformly attached to all generated artifacts.
- Remote inference may transmit the constructed prompt and selected source context to the configured provider. Users should not submit sensitive material without reviewing provider terms and data flows.
- Generated explanations, diagrams, assessments, and summaries may contain errors, omissions, fabricated references, or unsupported claims.
- No claim of clinical, legal, financial, or other professional competence is established.

## Platform and security

- Android device coverage, accessibility, localization, battery, memory, thermal behaviour, and large-corpus performance require broader physical-device testing.
- A successful CI debug build does not establish production readiness, secure signing, Play policy compliance, or security certification.
- The version-17-to-18 migration is additive, but populated legacy migration and encrypted-copy verification still need dedicated instrumentation tests.
- Local encryption and app-lock implementation require threat-model review and device-level testing; they should not be represented as protection against every attacker or compromised device.
- Data export, deletion, backups, and derived-data cleanup need end-to-end verification.

## Research evidence

- Repository documentation, architecture diagrams, unit tests, instrumentation tests, and CI results are not a peer-reviewed evaluation.
- No educational effectiveness, learning gain, retention, transfer, usability superiority, or expert-quality claim should be made without suitable data.
- No benchmark performance claim should be made without a frozen dataset, documented gold labels, fair baselines, and reproducible analysis.
- No multi-domain generalization claim should be made until several independently defined domains are evaluated using comparable protocols.
- User satisfaction alone does not establish learning outcomes.

## How to update this document

For every resolved limitation, link the implementation commit, tests, acceptance evidence, and (where relevant) evaluation report. Do not delete unresolved limitations merely to make the project appear mature.
