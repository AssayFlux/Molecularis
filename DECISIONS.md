# Molecularis — Decision Log
Open questions are not decisions. Record date, context, options, choice, consequences and approver. Changes to direction, scope, language, engine tier, license, data source or regulatory posture require an entry.

## Decision register
| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-000 | 2026-11-07 | Adopt owner master and living direction files | Approved — owner approved baseline in chat | Project owner |
| D-001 | 2026-11-07 | Project LICENSE | Approved — Apache-2.0 selected; canonical LICENSE text added at repository root | Project owner |
| D-002 | 2026-11-07 | Target jurisdictions and applicable privacy/medical-device laws | Approved strategic scope — global, including future clinical use; jurisdiction-specific clearance remains mandatory | Project owner; qualified advisers required for implementation |
| D-003 | 2026-11-07 | Research-paper framing and venue(s) | Approved — multiple papers over time; owner requests guidance at milestones | Project owner |
| D-004 | 2026-11-07 | Clinical advisory board/advisers | Approved — defer recruitment until software is more mature; P0 remains blocked pending qualified advisers | Project owner |
| D-005 | 2026-11-07 | Gene-scope breadth | Approved strategic direction — both a comprehensive PGx gene panel and a broad cross-domain gene catalogue; exact inventories and rollout are staged by evidence | Project owner |
| D-006 | 2026-11-07 | Target Android devices/minimum support matrix | Approved — Android 10+ (API 29), 64-bit ARM; low-end, mid-range and flagship test tiers | Project owner |
| D-007 | 2026-11-07 | Source-master archival | Resolved operationally — reconstructed from owner's complete chat-supplied master at docs/origin/MOLECULARIS_MASTER.md; not represented as a Git move | Owner instruction |
| D-008 | 2026-11-07 | Authorization to execute R1–R3 | Approved — proceed sequentially, subject to each phase's evidence, safety and exit gates; not a waiver or completion sign-off | Project owner |
| D-009 | 2026-11-08 | Parallel Track S implementation sequencing | Approved — begin independently implementable S1 preparation while R1–R10 continue; dependent rendering and S2–S5 gates remain | Project owner |
| D-018 | 2026-11-09 | Engineering language ownership and integration standard | Approved — owner-directed target stack and shared JSON Schema contract standard | Project owner |
| D-019 | 2026-11-09 | Sequential track execution order | Approved — R → S → I → P → G, two steps per track; supersedes D-009 parallel sequencing | Project owner |
| D-020 | 2026-11-09 | Close R host audit and proceed to S | Approved — close the R implementation/host-regression audit on exact-source CI #2126, consolidate documentation, then begin S. Does not waive or relabel open R device, external-science, licensing, security, accessibility or release evidence | Project owner |
| D-022 | 2026-11-11 | Start Track P and prepare P0 | Approved — start P engineering and P0 evidence preparation; formal P0 gate remains NOT APPROVED pending independent evidence and a separate owner gate decision | Project owner |
| D-023 | 2026-11-12 | Add Track U after Track G in sequential execution order | Approved — current order is R → S → I → P → G → U; supersedes D-019's five-track order while preserving its historical record and two-step gate | Project owner |
| D-025 | 2026-11-18 | Open engineering and institutional research-testing scope | Approved — owner declares institutional ethics approval obtained and authorizes patient-data research testing within its exact scope; approval record pending attachment; clinical deployment remains separate | Project owner |

## D-000 — Direction baseline (approved)
- Context: Owner supplied complete Molecularis master and instructed work to follow Parts 1–18 with approval gates.
- Options: (a) adopt master and derive living direction files; (b) implement without controlled baseline.
- Choice: (a), approved by the project owner in chat on 2026-11-07.
- Consequences: R0 is current workstream; no scientific claims or clinical features without evidence/gates. Master is historical source; NORTH_STAR/ROADMAP/DECISIONS become operational source of truth after approval.
- Approver: Project owner (explicit approval received 2026-11-07).

## Standing guidance and deferred checkpoints
- D-003: Guide the owner through paper framing, evidence readiness, authorship details and venue selection when R1–R3 evidence is available; this is a staged publication plan, not a manuscript approval.
- D-004: Revisit clinical-adviser recruitment after the research platform reaches the maturity checkpoint (target after R3), and before P0 or any PGx/clinical-scope work. P0 remains blocked until qualified advisers and all other prerequisites are satisfied.
- D-005: Maintain both the comprehensive, expandable PGx workstream and broad cross-domain gene catalogue. Inventory and implementation are evidence-led; catalogue inclusion does not imply implementation or validation.
- D-006: Android 10+ (API 29), arm64-v8a and low/mid/flagship test tiers are target requirements, not verified support claims. R1 must still establish actual device limits.

## D-004 — Clinical adviser timing (approved)
- Date: 2026-11-07.
- Context: Decide when to recruit clinical advisers for Molecularis' possible future clinical/PGx work.
- Options considered: formal advisory board early; recruit one adviser first; defer advisers until software is more mature; remain research-only indefinitely.
- Choice: Defer all clinical adviser recruitment until the software is more mature (owner selected option 3).
- Consequences: Do not spend effort recruiting a clinical advisory board during the current R1 engineering-feasibility phase. Revisit adviser recruitment after the research platform reaches a meaningful maturity milestone (target review point: after R3), and before P0, PGx gene-set selection, patient-related workflows, clinical studies or any clinical-scope implementation. P0 remains blocked until qualified advisers and all other required legal, ethics, regulatory, QMS and evidence prerequisites are satisfied. This timing decision does not authorize patient data, clinical features or clinical claims; Research Mode remains the only public mode and Clinical Decision Support Mode remains disabled. If the project approaches a gated activity earlier than expected, pause and recruit/consult qualified advisers before proceeding.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-003 — Research-paper strategy (approved)
- Date: 2026-11-07.
- Context: Choose a publication strategy that is credible, evidence-led and manageable across Molecularis' broad scientific scope.
- Options considered: software/methods paper; bioinformatics application paper; broad multidisciplinary paper; multiple papers over time.
- Choice: Multiple papers over time (owner selected option 4).
- Consequences: The initial publication should focus on the platform/software/methods and be attempted only when R1–R3 provide sufficient reproducible implementation, validation and benchmark evidence. Later domain-specific papers may be developed separately when each domain has independently validated workflows and appropriate reference comparisons. Do not combine unsupported capabilities into broad claims or invent results. Venue selection, author order, affiliations, funding, competing interests and manuscript claims require later owner review against the venue's then-current requirements. The assistant should guide the owner through these decisions at relevant milestones; this does not replace owner approval or scientific peer review.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-002 — Target jurisdictions (approved strategic scope)
- Date: 2026-11-07.
- Context: Establish the intended geographic ambition for Molecularis, including the possibility of future clinical functionality.
- Options considered: India-first; India + US; India + EU/UK; global research-only; global including future clinical use.
- Choice: Global scope, including future clinical use (owner selected option 5).
- Consequences: The long-term product ambition is international, and future clinical use may be pursued. This is not a finding of legal compliance, regulatory clearance, market authorisation or permission to process patient data in any country. Research Mode remains the only public mode; Clinical Decision Support Mode remains disabled. Before any patient-data workflow, clinical feature, clinical study or market entry, identify each relevant jurisdiction and obtain qualified local privacy, health-data, medical-device/software, research-ethics and other applicable advice/approvals. P0 and all existing clinical, ethics, security and evidence gates remain mandatory. No single global approval is presumed.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-001 — Project license (approved)
- Date: 2026-11-07.
- Context: Select a project-level license that supports academic and commercial adoption while providing explicit patent terms.
- Options considered: MIT, Apache-2.0, GPL-3.0, AGPL-3.0 and proprietary licensing.
- Choice: Apache License 2.0 (Apache-2.0).
- Consequences: The project distributes its own original code under Apache-2.0; the canonical license text is now present at the repository root. Each third-party engine, dependency, model and data pack remains subject to separate license verification; this decision does not relicense third-party materials.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## D-006 — Android device target (approved)
- Date: 2026-11-07.
- Context: Set the Android OS/ABI target and physical-device test breadth for R1 and later support claims.
- Choice: Option 1 — Android 10+ (API 29), 64-bit ARM (arm64-v8a), with low-end, mid-range and flagship device test tiers.
- Consequences: This is the intended compatibility target and test strategy, not proof that all Android 10+ devices work. R1 must verify emulator and physical arm64 behaviour and establish evidence-based RAM, storage, performance and device support limits. CI/emulator success alone does not constitute physical-device validation. No R1 go/no-go or R2 authorization is implied.
- Approver: Project owner, explicit selection in chat on 2026-11-07.

## New decision template
- Date / ID:
- Context:
- Options:
- Choice:
- Consequences / roadmap impact:
- Approver:
- Evidence:


## D-008 — Authorization to execute R1–R3 sequentially (approved)
- Date: 2026-11-07.
- Context: Owner explicitly approved “R1, R2 & R3” after clarification of the earlier ambiguous “R2 & R2” message.
- Choice: Proceed with the R1, R2 and R3 workstreams in sequence.
- Consequences: This is authorization to execute the approved roadmap phases, not a finding that any phase has passed its exit criteria. R1 remains in progress and currently has a documented Android build blocker at Chaquopy Biopython dependency resolution. R2 may begin only after R1 evidence is complete and the R1 go/no-go is documented; R3 may begin only after R2's exit evidence and approval. All scientific validation, third-party licensing, device verification, security, privacy, clinical and P0 gates remain in force. No clinical mode, patient-data workflow or clinical claim is authorized by this decision.
- Approver: Project owner, explicit approval in chat on 2026-11-07 (“Approved R1,R2&R3”).
- Evidence: Owner approval message in project conversation; phase completion evidence remains outstanding and must be recorded separately.


## D-009 — UI/UX master specification (2026-11-08)
- Context: Owner supplied `MOLECULARIS_UI_SPEC.md` and instructed parallel Track U and R0–R10 work.
- Choice: Adopt the UI specification as governing UI contract and execute U0 foundations now.
- Visual direction: NOT APPROVED. Three neutral proposals (Precision Lab, Field Notes, Dark Instrument) are studies only; owner selection is required before theme lock.
- Brand: Owner assets only. Existing `Assets/Brand Logo.svg` is preserved but not assumed to be approved app/brand master. Placeholders are development-only and block release.
- Security: Offline-only/no automatic cloud backup are conservative proposals; app lock/vault lock/panic wipe remain review items. Clinical mode remains disabled.
- Consequences: U0 records tokens, schema, asset contract, threat-model draft, verified platform facts and quality/device templates. Stop after presenting three working gallery directions for owner choice.
- Approver: Owner authorised execution; visual-direction and security-default sub-gates remain open.


## D-010 — Dark-first visual preference and theme-family scope (2026-11-08)
- Context: Owner supplied the AssayFlux animated organization logo and requested a futuristic dark design, with selectable light, dark and neon palette families and 20+ distinct fonts.
- Choice: Record dark-first/futuristic as the preferred direction; provide 4 light, 5 dark and 4 neon palette proposals and 26 distinct font-family candidates. Initial Compose shell defaults to dark and exposes Light/Dark/Neon selection.
- Not approved: No final palette, exact seed colour, font family bundle, app-logo treatment or design-system direction is locked. The U0 visual gate remains open for owner review.
- Brand constraint: Preserve the uploaded organization logo artwork; no recolouring, redraw, sampling or derivative app mark. Existing `Assets/Brand Logo.svg` remains unchanged.
- Consequences: Theme token generator, contrast/CVD audits, exact font licence audit, durable settings persistence and compact/medium/expanded gallery previews remain required. Font catalogue entries are candidates, not proof of redistribution rights.
- Approver: Owner supplied the direction in chat on 2026-11-08; final U0 visual choice is pending.
- Evidence: `design/tokens.json`, `design/typography-catalogue.yaml`, `docs/ui/theme-proposals.md`, `assets/design-previews/`.


## D-011 — Select Obsidian Cyan as the default UI direction (2026-11-08)
- Context: Owner requested a futuristic dark UI, light/dark/neon theme families, and then authorized us to complete the visual design using best judgement.
- Choice: Use Obsidian Cyan as the default dark-first direction: near-black/navy surfaces, cyan primary actions, electric-blue secondary accents and restrained mint status accents. Retain Light and Neon as selectable alternatives. This is an implementation choice under the owner's broad authorization, not a claim of measured superiority.
- Brand: Do not sample brand artwork for seed colours or alter the organization logo. The owner-provided astronaut background is used as supplied on the Home hero.
- Consequences: Palette contrast/CVD validation, token generation, gallery screenshots, adaptive layouts and owner visual review remain U0 work. Any contrast failure must be fixed in tokens, not by changing the logo.
- Approver: Owner authorized completion by best judgement in chat on 2026-11-08.


## D-012 — Responsive shell implementation strategy (2026-11-08)
- Context: The UI shell needs compact, medium, expanded and large-window navigation while preserving the current stable Material 3 dependency set.
- Choice: Implement live app-window classification in Compose and use Material 3 NavigationBar, NavigationRail and PermanentNavigationDrawer. Compact portrait uses bottom bar; medium/expanded and compact-height windows use rail; large/extra-large (≥1200dp) uses permanent drawer. Readable content is capped at 840dp.
- Deviation: NavigationSuiteScaffold and WindowManager fold-posture APIs are not yet integrated. This is temporary; no fold-aware or hinge-safe claim is permitted. Extend after adaptive-library compatibility and posture tests are verified.
- Evidence: WindowLayout.kt and WindowLayoutTest.kt; CI build/test pending. Device matrix remains NOT RUN.


## D-009 — Parallel Track S implementation sequencing (approved)
- Date: 2026-11-08.
- Context: Owner explicitly directed completion of R1–R10 and commencement of Track S without another approval pause.
- Choice: Begin independently implementable S1 preparation in parallel with R1–R10. This supersedes the earlier sequencing prohibition only to the extent of non-dependent work.
- Consequences: Deterministic structure-view payload preparation and its contract/tests may proceed. Full WebView rendering remains dependent on R1 WebView/runtime feasibility and exact third-party license review. S2–S5 retain all scientific, model-license, node-security and benchmark gates. No phase is complete by this decision; no validation, clinical, patient-data or release gate is waived.
- Approver: Project owner, explicit instruction in chat on 2026-11-08.


## D-013 — Owner-supplied application UI reference designs (2026-11-08)
- Context: Owner added two visual reference assets to the repository: `Assets/App UI - Dashboard Design.jpg` and `Assets/App UI - Login Page Design.jpg`. The owner states these represent the design language they like and wants the Molecularis application UI to follow that language.
- Choice: Treat both images as first-class owner-supplied visual references for the Molecularis product UI. Apply their visual language consistently across dashboard, authentication/onboarding, navigation, cards, typography, spacing, colour, iconography and interaction patterns where the references provide evidence. Preserve the original image files unchanged. Scientific workflow clarity, accessibility, responsive behaviour, offline-first operation and existing brand-asset constraints remain mandatory.
- Boundary: Do not infer detailed visual properties from filenames or replace the reference designs with the existing generic theme proposals. The binary assets are present in the repository, but direct visual inspection is still required before extracting exact tokens or declaring a visual match. The final implementation must be reviewed against the images and validated with real screenshots across supported window classes.
- Approver: Owner explicitly confirmed this preference in project conversation on 2026-11-08.
- Evidence: The two repository assets listed above; visual comparison and screenshot evidence pending.


## D-014 — Light classic visual direction and calligraphic typography (2026-11-08)
- Context: Owner clarified that the dashboard reference's colours are placeholders only, selected a light classic interface, and requested designed calligraphic typography.
- Choice: Set the product's intended default visual direction to Light Classic. Preserve the reference's composition and component language (rounded hero region, prominent carousel, spacious cards, simple top controls and clear content hierarchy), but do not copy its pastel palette. Use a restrained classic scientific palette with light neutral surfaces, dark readable text and a controlled navy/teal accent system; exact colour tokens remain subject to contrast and screenshot validation.
- Typography proposal for implementation: Allura as a limited calligraphic brand signature/wordmark accent; Cormorant Garamond for selected editorial display headings; Inter for navigation, controls and body copy; JetBrains Mono for sequences, identifiers, code and scientific values. Do not use script typography for dense content, controls, labels, tables or scientific notation.
- Licensing and accessibility: These are font-family candidates, not approved bundled binaries. Verify exact upstream releases, licence texts, glyph coverage, weights, file size, rendering and contrast before packaging. Provide accessible sans-serif fallbacks. Do not claim visual completion until real app screenshots are reviewed against the owner's references.
- Supersedes: D-010/D-011 only for the default visual theme and typography direction; it does not remove the option to offer dark themes. D-013's owner-supplied layout references remain primary.
- Approver: Project owner, explicit selection/request in chat on 2026-11-08.
- Evidence: Owner dashboard reference image and chat instruction; login reference and screenshot comparison remain pending.


## D-015 — Owner-approved Molecularis Light Classic visual system (2026-11-08)
- Context: Owner reviewed the six-screen visual concept (splash, login, dashboard carousel, navigation drawer, profile and appearance) and explicitly approved it with “Love it” and directed that the new design be documented and implemented carefully.
- Choice: Adopt the visual system in `docs/ui/molecularis-visual-design-system.md` as the current product UI authority. Light Classic is the default: warm ivory/cream, deep maroon, restrained gold and peacock teal; retain a coherent Dark Classic and System appearance. Preserve the reference composition: rounded surfaces, prominent central horizontal workspace carousel with adjacent cards peeking, pagination, generous spacing and stacked real-data cards. Use culturally respectful, attributed motifs only after their dedicated evidence gates.
- Typography roles: Great Vibes (limited brand-script candidate only if no existing logo wordmark), Cormorant Garamond (display headings), IBM Plex Sans (functional UI/body), IBM Plex Mono (scientific data/code); Indic-script fallback must be verified. Font binaries remain subject to exact version/licence/glyph/size/offline verification before bundling.
- Constraints: Existing Compose architecture, capability registry, real-data-only UI, owner logo bytes, accessibility, privacy, security, offline-first policy, research-only public mode and all R/S/I/P gates remain in force. The generated showcase is concept art, not implementation or screenshot evidence.
- Supersedes: D-009's unresolved three-proposal visual gate; D-010/D-011's dark-futuristic/Obsidian-Cyan default and neon-first direction; D-014's Light Classic navy/teal palette and Allura/Inter/JetBrains Mono typography proposal where inconsistent with D-015. D-012 responsive shell strategy and D-013 owner layout references remain active where compatible. Earlier entries remain in the log for audit history, not as current UI instructions.
- Approver: Project owner, explicit visual approval and implementation instruction in chat on 2026-11-08.
- Evidence: Owner-approved concept review in project conversation; canonical specification at `docs/ui/molecularis-visual-design-system.md`. Implementation, screenshots, contrast and device validation remain open.

## UI decision supersession register
The following historical decisions are retained for auditability but are no longer active design instructions: D-009 (three-proposal visual gate), D-010 (dark-first preference), D-011 (Obsidian Cyan default), and D-014 (previous Light Classic palette/type proposal). D-015 is the current visual authority. D-012 adaptive navigation and D-013 owner layout-reference decisions remain active unless specifically contradicted by D-015.

## D-016 — Integrated build/test cycle and active UI direction reaffirmed
- Date: 2026-11-08.
- Context: Owner found that successful APK compilation had been mistaken for a working application: D-015 was not fully implemented, authentication/biometrics were absent, and several options were inert or informational.
- Choice: Approved. Implement substantial vertical slices, build arm64 APK/AAB, test affected systems and regression suite, inspect/install the exact artifact where hardware permits, fix failures, and repeat. Testing is part of every cycle, not deferred to the end. Record source commit and artifact SHA-256.
- Active design: D-015 Light Classic is the sole current UI authority, with Dark Classic and System. Earlier neon/Obsidian Cyan and pre-D-015 palette proposals are discontinued for active implementation and retained only as historical audit records.
- Authentication boundary: No fictitious cloud/account authentication. Local app-lock must be distinguished from account identity and have secure key lifecycle/recovery. Biometric unlock uses AndroidX BiometricPrompt, runtime capability/enrollment checks, explicit opt-in, credential fallback, lockout/error handling and Keystore-backed cryptographic operations where appropriate. Molecularis never stores biometric templates or passwords.
- Functionality: Every visible control executes a real action, navigates to an implemented screen, or is visibly disabled with an explanation. Research tools are launchable only with registry capability, input contract, dispatcher, result model/viewer and tests. No fake metrics, authentication success or scientific output.
- Evidence: Distinguish source implementation, automated tests, reference validation, CI build, emulator verification and physical-device verification. Build success alone is not a tested app. Missing hardware tests remain blockers.
- Consequences: ROADMAP contains the mandatory cycle. UI screen map, quality report, registry and session log must be updated with each cycle.
- Approver: Project owner, explicit instruction in chat on 2026-11-08.


## D-017 — Owner authorization for safe P-track public-data engineering preparation
- Date: 2026-11-09.
- Context: The owner explicitly reiterated permission to proceed with the P track. The existing P0 boundary distinguishes public, non-patient research preparation from patient-data, human-subject and clinical activities.
- Choice: Proceed immediately with P1 public-data-only engineering preparation in parallel with R/S/I work: catalogue/schema validation, synthetic fixtures, dataset provenance and reproducibility infrastructure, and non-clinical research tooling. Do not wait for P0 to build these safe foundations.
- Constraints: This authorization does not approve patient or human-subject data intake, clinical interpretation, genotype-to-phenotype recommendations, diagnosis/treatment/dosing, Clinical Mode, or claims of clinical validity/utility. P0 remains blocked until the existing legal, ethics, privacy, security, qualified-adviser, validation and owner-approval evidence is complete. D-004 adviser timing remains active; review after R3 and before any P0-gated activity.
- Approver: Project owner, explicit permission reiterated in chat on 2026-11-09.


## D-018 — Owner-directed language ownership and integration contract
- Date: 2026-11-09.
- Context: The owner supplied an explicit engineering role, target stack ownership, integration-first workflow, interface-contract requirements, security rules and response/checklist requirements, and asked that they be documented and followed.
- Choice: Adopt `docs/ENGINEERING_INTEGRATION_STANDARD.md` as the mandatory engineering workflow and target ownership model: Python scientific analysis; C++ performance-critical core; Rust security; Kotlin Android; Swift iPhone; HTML/CSS/TypeScript with Three.js for offline 3D visualisation; Bash build/test/deploy automation only. Adopt JSON Schema as the semantic source of truth for cross-component engine messages, initially `api/engine-envelope-v1.schema.json`.
- Consequences: The standard is normative for new work. Existing code is not represented as conforming merely because it exists. Current Rust/C++ code is a smoke-test probe, Swift and TypeScript/Three.js sources are absent, and current Chaquopy/JNI edges must be migrated or explicitly mapped through reviewed, tested vertical slices. iOS minimum version/team experience remain TBD. No new clinical scope is authorized. No interface is silently changed by this documentation decision.
- Approver: Project owner, explicit instruction in chat on 2026-11-09.


## D-019 — Sequential track order and two-step gates (supersedes D-009)
- Date: 2026-11-09.
- Context: The owner explicitly reset execution order after earlier parallel-track instructions and requires a controlled base-first workflow.
- Choice: Work tracks strictly in this order: **R → S → I → P → G**. For each track, Step 1 builds the documented base; Step 2 audits, tests and completes/fixes remaining base work. Do not begin the next track until the current track's two-step gate has been honestly assessed and reported.
- Consequences: D-009's permission to develop S in parallel with R is superseded for current execution. Dependencies and safety gates remain. Report completion percentage only after the two-step gate and define the denominator; never claim full track completion if documented exit criteria remain unmet.
- Approver: Project owner, explicit instruction in chat on 2026-11-09.


## D-020 — R engineering audit closure and transition to S
- Context: The owner requested completion of the R-track audit, documentation consolidation, and transition to S.
- Evidence: Exact-source commit `888e49bc7108a2609db97d76193a60d5eec175e0`; CI #2126 passed all five jobs, including Android arm64 APK/AAB build, JVM tests, Python 238 passed/4 skipped, host scientific-reference comparisons, RDKit sanity and direct SPDX inventory.
- Choice: Close the R implementation/host-regression audit step, consolidate the repository documentation, and proceed to S as the next engineering track.
- Boundary: This is not a declaration that R1–R10 are all phase-accepted, scientifically validated, device-verified, fully licensed or release-ready. Open R evidence remains in the R audit and master roadmap as carry-forward obligations; dependent S work must respect those gaps.
- Approver: Project owner (explicit instruction in chat, 2026-11-09).


## D-022 — Owner authorization to start Track P and prepare P0
- Date: 2026-11-11.
- Context: The project owner explicitly stated: “I am approving, open p0 & build p track.”
- Choice: Start Track P in the prescribed R → S → I → P → G order. Begin P0 evidence preparation and continue the P1 public-data-only/synthetic engineering base. This authorizes project scope, engineering work and preparation.
- Boundary: D-022 does **not** assert that P0 has passed. The formal P0 gate remains NOT APPROVED until the intended-use and governance packet is complete; applicable jurisdiction-specific legal/regulatory advice, ethics/IRB determination, qualified independent clinical/scientific review, privacy/security/QMS evidence and independent validation plans are documented; unresolved risks are dispositioned; and the project owner records the formal gate decision. No patient/human-subject data or activity, individual genotype interpretation, diagnosis/treatment/dosing recommendation, Clinical Mode or clinical claim is enabled.
- Consequences: P0 preparation and permitted P1 public-data metadata/synthetic work are active. Candidate dataset entries remain unapproved until exact source terms and provenance are reviewed. No external approval, signature, adviser appointment or regulatory status is fabricated.
- Approver: Project owner, explicit approval in chat on 2026-11-11.


## D-023 — Add Track U after Track G in the sequential execution order
- Date: 2026-11-12.
- Context: The project owner explicitly instructed: “Add u track after G track in the order chain. Update all necessary documents.” The existing roadmap defines Track U as the User Interface track, with phases U0–U6.
- Choice: Set the current sequential engineering order to **R → S → I → P → G → U**. Track U follows Track G and must pass the same two-step rule: (1) build the documented base; (2) audit, test and fix the remaining base gaps.
- Supersession: This decision supersedes D-019 only as to the track list/order. D-019 remains a valid historical record of the earlier R → S → I → P → G order and its two-step execution model. D-009's parallel-track permission remains superseded. This decision does not reinstate parallel execution.
- Track U carry-forward: Existing U0–U3 source and documentation created before this decision are retained as pre-existing partial work; they are not erased or retroactively treated as fully accepted. Further sequential Track U implementation and its audit begin only after Track G's two-step gate has been assessed and reported. U4–U6 remain subject to their documented dependencies and exit criteria.
- Consequences and boundaries: Update current direction, roadmap, contribution guidance, documentation index and Track G sequencing references. Track dependencies, exact-head CI, device/accessibility/security evidence and all scientific/licensing/privacy/regulatory gates remain mandatory. This decision does not waive P0 or authorize patient data, human-subject activity, Clinical Mode or regulated deployment.
- Approver: Project owner, explicit instruction in chat on 2026-11-12.


## D-024 — Adopt the owner-supplied Premium Minimal Monochrome UI specification
- Date: 2026-11-17.
- Context: During Track U direction review, the project owner supplied the complete 20-section Premium Minimal Monochrome Design System — V1 and explicitly identified it as the required application UI prompt. This is a new, direct owner instruction for the active UI implementation.
- Choice: Supersede D-015 only for the active UI visual language and composition where they conflict. Adopt the owner's V1 monochrome specification: 393 × 852 dp reference viewport; responsive 360 × 800, 430 × 932 and 600 dp+ layouts; 4 dp spacing rhythm; supplied typography scale; exact light palette (#FAF9F6, #FFFFFF, #F2F1ED, #171717, #686868, #A3A3A3, #E5E3DE, #ECEAE6, #292929); exact dark palette (#121212, #1B1B1B, #242424, #F5F5F5, #A5A5A5, #686868, #333333, #292929, #E8E8E8); semantic status colours only; System/Light/Dark appearance; restrained component radii; application bar, drawer, button, input, card, list, icon, dialog, bottom-sheet, bottom-navigation and avatar measurements; safe-area, interaction, accessibility and responsive rules.
- Retained constraints: D-015 remains historical evidence and its non-conflicting requirements remain active: preserve owner-supplied artwork byte-for-byte; use native Jetpack Compose; retain real Molecularis workflows and Research Mode boundaries; do not invent accounts, jobs, metrics, results, scientific dispatchers or device support; keep typography/font licensing checks; do not enable unreviewed decorative assets. Existing scientific, privacy, security, licensing, architecture and phase gates are unchanged.
- Consequences: docs/ui/molecularis-visual-design-system.md, docs/ui/ui-spec.md, MOLECULARIS_UI_SPEC.md, tokens/generator, Compose primitives, screen implementations, screenshots, contrast/accessibility tests and roadmap evidence must be reconciled to V1. No claim of implementation or visual verification follows from this decision alone.
- Approver: Project owner, explicit instruction in chat on 2026-11-17.


## D-025 — Owner authorization for full engineering and institutional research testing

**Date:** 2026-11-18  
**Decision:** Open blanket engineering-development blockers, including the P0 development/testing blocker, and proceed with the complete MOLECULARIS implementation. The project owner declares that institutional ethics approval has been obtained and expressly authorizes testing with patient data within the scope of that approval.  
**Consequences:** Engineering may implement and test the full software system. Patient-data testing must remain within the exact institutional protocol, consent/waiver, approved environment and applicable law. Patient data must never be placed in source control, GitHub issues/PRs, CI, fixtures, logs or public artifacts. Clinical diagnosis, treatment/dosing recommendations, patient-facing clinical decision support and production clinical deployment are not implicitly approved by this engineering decision.  
**Approval record:** Institution, committee, approval/reference number, date, protocol version and conditions are pending attachment. The repository records the owner's declaration and does not claim independent verification.  
**Approver:** Project owner (explicit instruction in project conversation).


## D-026 — Desktop compute architecture and scientific-engine integration proposal
- Date: 2026-11-20.
- Status: **Proposed — owner decision pending.**
- Context: The project needs a controlled plan for integrating resource-intensive scientific engines and desktop compute without weakening the existing Android, scientific, privacy, security, licensing or release boundaries.
- Proposal: Use Android as the research interface and Linux x86_64 as the first reference desktop compute host. Extend the existing bounded remote-worker approach through versioned job/capability/result/provenance contracts, explicit authenticated pairing, TLS for non-loopback connections, isolated pinned engine profiles, resource quotas, cancellation, offline package import/export and user-visible data-transfer preview. Integrate third-party projects selectively through Molecularis-owned adapters rather than embedding complete upstream applications by default.
- Proposed integration domains: shared scientific data foundation; desktop interoperability; structural biology and visualization; optional protein-model profiles; cheminformatics; molecular simulation; genomics and nucleic-acid design; reproducible workflow and notebook experience; cross-platform and release validation.
- Consequences if approved: The companion planning documents under `docs/` become the working integration plan. Each engine remains a candidate until its exact upstream version, licence/model/data terms, runtime, adapter, scientific benchmark and security review are documented. The current approved track order and two-step build/audit gates remain controlling; this proposal does not reorder tracks or authorize parallel execution.
- Boundaries: This proposal does not enable remote compute, arbitrary command execution, automatic downloads, clinical functionality, patient-data processing beyond existing approvals, third-party redistribution or any engine's scientific acceptance. Existing privacy, ethics, security, licensing, scientific validation and release gates remain mandatory.
- Approval required: Project owner must explicitly approve or revise the architecture direction before implementation changes rely on this proposal.
- Evidence: `docs/MASTER_SCIENTIFIC_INTEGRATION_PLAN.md`, `docs/DESKTOP_COMPUTE_ARCHITECTURE.md`, `docs/SCIENTIFIC_ENGINE_INTEGRATION_MATRIX.md`, `docs/SCIENTIFIC_RULEBOOK_PLAN.md`, `docs/SCIENTIFIC_VALIDATION_PLAN.md`, `docs/ENGINE_RUNTIME_MATRIX.md`, `docs/THIRD_PARTY_INTEGRATION_REGISTER.md` and `docs/INTEGRATION_MILESTONES.md`.


---

## Alpha owner-directed decisions (2026-11-21)

| ID | Date | Topic | Status | Approver |
|---|---|---|---|---|
| D-026 | 2026-11-21 | Product direction: all-device platform | Approved by explicit owner instruction; Alpha is the working branch, not a brand | Project owner |
| D-027 | 2026-11-21 | Preferred core languages | Approved preference: C++, Rust and Python; TypeScript/JavaScript remains necessary for web/PWA client | Project owner |
| D-028 | 2026-11-21 | Android-native roadmap | Retired as product direction; preserve useful code and data during migration, do not build new Android-only product capabilities | Project owner |
| D-029 | 2026-11-21 | Alpha branch base | Created from current default branch CORE; no direct commits to CORE | Project owner direction; execution recorded by contributor |

## D-026 — All-device product direction

Molecularis becomes an all-device scientific research platform. Responsive web/PWA is the primary experience. Optional desktop packaging, a local compute connector, hosted workers and institutional/HPC connectors provide device-appropriate compute. Existing Android-specific work is audited and migrated rather than discarded. Preserve research-only and clinical-safety restrictions.

## D-027 — Preferred languages

C++, Rust and Python are preferred core languages. C++ is for measured numerical/performance kernels; Rust for safe parsers, validation and secure native services; Python for scientific orchestration and research integration. TypeScript/JavaScript is required for browser/PWA presentation and visualization. Use versioned contracts and stable ABI/IPC boundaries.

## D-028 — Android retirement and migration

No Android-native product roadmap. Existing Android/Kotlin work is migration context until equivalent cross-device capabilities and user-data migration are verified. Maintain a component parity ledger and preserve algorithms, tests, schemas, provenance and user data.

## D-029 — Alpha branch

Alpha was created from CORE, the repository's actual default branch at branch creation. It is the isolated implementation branch for the all-device transition. All Alpha changes remain separate from CORE until reviewed and merged by the repository owner.


## D-026 — Desktop-first cross-platform application direction (2026-11-21)
- Context: The initial Alpha plan incorrectly placed a responsive website/PWA first. The owner explicitly clarified: desktop application first for Linux, Microsoft Windows and macOS, and applications for Android and Apple mobile devices as well; no websites first.
- Choice: Adopt an installed, desktop-first cross-platform application. Deliver Linux/Windows/macOS desktop applications first, then Android and Apple iOS/iPadOS applications on shared domain logic, contracts, project formats and provenance. A web companion is deferred and optional, never the primary runtime.
- Framework: Not yet selected. Run a measured vertical-slice comparison across all five OS families, including accessibility, native integration, scientific visualization/GPU, offline storage, packaging/signing/updating, mobile lifecycle, testability and licensing. Record the result and owner decision before committing the framework.
- Consequences: Supersedes the web/PWA-first wording in Alpha planning docs. Re-sequence roadmap and backlog around desktop foundations, local scientific execution and desktop release engineering before mobile parity. Preserve Android scientific code and user data until migration parity is proven.
- Approver: Project owner, explicit instruction in project conversation on 2026-11-21.
