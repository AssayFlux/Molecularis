# Current limitations and claims boundary

This document is intentionally conservative. It describes known constraints and must be updated when implementation or evidence changes.

## Product and architecture

- The current app contains substantial biochemistry-specific functionality. It is not yet a completed general-purpose multi-domain platform.
- First-class user-created subject workspaces and multiple independently managed professor profiles are not yet implemented end-to-end.
- Generalized prompt construction does not by itself guarantee that subject context is propagated through every screen, retrieval path, lesson workflow, and persisted conversation.
- Existing detected subject metadata is not equivalent to explicit workspace ownership or isolation.
- Cross-subject isolation has not been established until database, retrieval, chat, and UI integration tests demonstrate it.

## Ingestion and knowledge quality

- PDF processing relies on OCR and can lose formatting, equations, tables, diagrams, symbols, columns, footnotes, and reading order.
- Page-level extraction metrics are heuristic indicators of text usability, not measures of factual accuracy or completeness.
- Topic and heading detection are heuristic and require human review.
- Lexical retrieval can miss paraphrases and conceptually related passages; optional embedding primitives are not a validated default retrieval path.
- A retrieved passage can be irrelevant, outdated, incomplete, or contradictory. Page labels and provenance do not prove that a generated claim is supported.

## AI generation

- Outputs depend on model/provider versions, prompts, retrieval context, device/runtime behaviour, and network availability.
- A configured professor role is a prompt/configuration profile, not a separately trained or fine-tuned model.
- Generated explanations, diagrams, assessments, and summaries may contain errors, omissions, fabricated references, or unsupported claims.
- Source-grounding is only as strong as extraction, retrieval, evidence selection, and claim-level verification.
- No claim of clinical, legal, financial, or other professional competence is established.

## Platform and security

- Android device coverage, accessibility, localization, battery, memory, thermal behaviour, and large-corpus performance require broader physical-device testing.
- A successful CI debug build does not establish production readiness, secure signing, Play policy compliance, or security certification.
- Local encryption and app-lock implementation require threat-model review and device-level testing; they should not be represented as protection against every attacker or compromised device.
- Optional remote inference means that selected content may leave the device. The precise data flow and provider terms must be reviewed before sensitive use.
- Data export, deletion, backups, and derived-data cleanup need end-to-end verification.

## Research evidence

- Repository documentation, architecture diagrams, unit tests, and CI results are not a peer-reviewed evaluation.
- No educational effectiveness, learning gain, retention, transfer, usability superiority, or expert-quality claim should be made without suitable data.
- No benchmark performance claim should be made without a frozen dataset, documented gold labels, fair baselines, and reproducible analysis.
- No multi-domain generalization claim should be made until several independently defined domains are evaluated using comparable protocols.
- User satisfaction alone does not establish learning outcomes.

## How to update this document

For every resolved limitation, link the implementation commit, tests, acceptance evidence, and (where relevant) evaluation report. Do not delete unresolved limitations merely to make the project appear mature.
