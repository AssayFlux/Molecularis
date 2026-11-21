# Track U — Completion audit and outstanding work


> **Historical record:** This dated audit/workplan predates the Molecularis rebrand. Former product names, source paths and repository URLs are retained where they document the state of the project at that time. Current identity and compatibility rules are in [brand-migration.md](../brand-migration.md).

**Audit date:** 2026-11-18  
**Repository:** `AssayFlux/Kinetics`  
**Target branch:** `main` only  
**Current engineering review baseline:** `83cd39d543e607876f8b499cff6b0cf94fc6b004` (49/68 catalogue routes reconciled, bounded HMMER, prediction-envelope, gene-catalogue and CA-comparison additions; exact-head CI pending)
**Audit and quality-report documentation commit:** `cb79b9110ff50a69b1b58d78a8b13e3c8843cf3b`  
**Status:** **ENGINEERING INTEGRATION IN PROGRESS — distinguish code work from external/device acceptance**  
**Design authority:** D-024, owner-supplied Premium Minimal Monochrome V1. Semantic decision colours may be used for status only; monochrome remains the visual authority.

This is an evidence-based gap register, not a completion claim. A source file existing does not prove a complete user journey, accessibility, security assurance, device compatibility or release readiness. Do not mark a row complete without the evidence named below.

## 1. Baseline and build evidence

- PR #76 was merged to `main` as merge commit `dea7bec731f3e6bdc3732899dd3feeed2703bbc3`.
- The merge contains the Step 1 monochrome design-system foundation and the compiler correction `FontWeight.Regular` → `FontWeight.Normal`.
- Exact-main workflow: [run 44208315663](https://github.com/AssayFlux/Kinetics/actions/runs/44208315663), commit `dea7bec731f3e6bdc3732899dd3feeed2703bbc3`.
- At audit time, the Python foundation/tests, Vina smoke, RDKit descriptor fixtures, SPDX inventory, host scientific reference comparisons, RDKit ADMET utility smoke, Node security tests and OpenMM CPU replica smoke jobs reported success.
- The Android arm64 debug APK/AAB job was still running at the audit time, at the build/package-alignment step. Therefore no APK/AAB success, package alignment, artifact hash or download artifact is claimed here.
- The earlier PR workflow `44208257346` is not a substitute for the exact-main build. Its artifacts are not evidence that the merged main commit produced an APK.

## 2. Work-package disposition

| Package | Disposition | What exists | Remaining closure work |
|---|---|---|---|
| U0 — design foundation | PARTIAL | D-024; V1 token source and generated Compose/CSS tokens; typography; reusable Compose primitives; component gallery source | Prove deterministic generation on exact main; audit every active component against owner dimensions; integrate verified owner assets without copying/moving originals; complete interactive gallery and visual regression screenshots |
| U1 — application shell | PARTIAL | Three destinations (Home, Work, Settings); compact drawer/bottom navigation and expanded rail; app bar; System-default Light/Dark preference; registry-backed Home carousel and service list; import/job entry points | Complete global search over real jobs/registry; onboarding for actual local setup; route every screen/action; verify process-death and navigation restoration; eliminate or explicitly label every planned/inert destination; complete screen-by-screen migration |
| U2 — security and privacy | PARTIAL / REVIEW REQUIRED | Device-local biometric prompt and credential fallback; foreground-return re-authentication; AES-GCM encrypted inputs; fail-closed Keystore-loss handling; read-only encrypted-orphan inventory; explicit Settings data inventory; analysis-work cancellation on job deletion | Lifecycle/device tests for prompt cancellation, lockout and credential fallback; merged-manifest/backup/network audit; Keystore fault injection; deletion/orphan cleanup regression; owner decision on FLAG_SECURE/Recents; decision on SQLite metadata/result encryption; independent mobile security/privacy review. See `u2-security-privacy.md` |
| U3 — workflows and results | PARTIAL | SAF import; WorkManager import/analysis lifecycle; encrypted input staging; FASTA QC; newly integrated FASTQ QC with explicit Phred+33/+64; digest-bound result persistence; structured FASTA/FASTQ result preview; provenance and SAF export | Embedded-runtime FASTQ fixtures; result schema validation; process-death/retry/cancel tests; export round trips; registry/dispatcher parity for every runnable action; broader durable detail/log/failure flows. See `u3-scientific-workflows-results.md` |
| U4 — scientific viewers | BOUNDED ANDROID STRUCTURE/CHEMISTRY INTEGRATION IMPLEMENTED; DEVICE/SCIENCE ACCEPTANCE OPEN | Service destinations route to hardened offline PDB/mmCIF interactive 3D coordinate viewer with session/PNG/SVG/state export and full-screen mode; SDF/MOL graph preview with full-screen mode; S3 ligand-site and apo-pocket candidate screens; no third-party viewer runtime dependency | Physical low-end ARM64 performance/memory, supported WebView matrix, accessibility/lifecycle/import-export tests and independent S1–S3 scientific concordance remain open. Alignment/tree/chart and full 3D chemistry viewers are not claimed. See docs/track-u/u4-scientific-viewers.md |
| U5 — genomics / PGx / in-silico screens | PARTIAL — AGGREGATE VCF QC INTEGRATED; PGx/IN-SILICO REMAIN GATED | The relevant genomics/variant service destinations include bounded aggregate-only VCF syntax/QC with institutional-authorization attestation, no sample/genotype output, no persistence/export; PGx and host-engine gate disclosures are explicit | P1 reference concordance/source terms/device validation; P2 licensed definitions and biological concordance; P3 licensed guideline evidence; I2 redocking/cross-docking; I3 force-field/biomolecular validation; I4 licensed datasets/model calibration. Owner-authorized research testing is open under D-025 within the declared institutional approval; no PGx interpretation or Android host-engine launcher. See docs/track-u/u5-genomics-pgx-research.md |
| U6 — quality and acceptance | NOT PASSED | Device matrix and quality-report documents; some source-level navigation and workflow tests | Run exact-head Kotlin/JVM/UI tests; token parity; screenshot comparisons; WCAG contrast measurement; touch-target bounds; TalkBack; 200% font scale; keyboard/switch access; reduced motion; RTL; landscape/split-screen/tablet; process death/rotation/offline; emulator and named physical-device checks; record results and hashes |

U2–U5 extension records: `u2-security-privacy.md`, `u3-scientific-workflows-results.md`, `u4-scientific-viewers.md` and `u5-genomics-pgx-research.md`. These describe concrete source additions and their still-open acceptance evidence; none waives external/device gates.\n\n## 3. Owner blueprint implementation (2026-11-18)\n\n- Added `docs/ui/owner-blueprint-implementation.md` and linked it from `KINETICS_UI_SPEC.md`; the two owner reference images remain in `Assets/` unchanged.\n- Replaced the old Home service catalogue with a horizontal carousel generated from the 68 individual capability entries plus Public Reference Databases. Domain cards are clickable and open a dedicated service destination.\n- Home now presents four summary panels for runtime readiness, research work, recent activity and local data/reference access.\n- Existing Public Database, FASTA/FASTQ, structure, chemistry, genetic-code and VCF workflows were moved into relevant service destinations where their current composables exist. Catalogue entries are shown with honest execution caveats; registration is not presented as proof of an Android dispatcher.\n- Replaced compact bottom navigation and expanded rail with the hamburger drawer. Added top-right profile entry with an explicit no-remote-account disclosure. Password reset, remote sign-in and user ID are not simulated because no identity backend exists.\n- Restored safe-drawing inset handling.\n- **Not yet accepted:** exact-head CI for the latest UI commit, screenshot comparison against both owner images, physical-device interaction/accessibility testing, login-screen visual alignment, real account backend, and complete per-capability Android dispatchers. Regression tests now cover one card per catalogue entry, ID-based routing, the five-indicator pager window, and the four dashboard panels. The current biometric screen remains a local device lock and is not a remote login form. The four unlabeled controls in the owner sketch are not assigned invented credential semantics; matching the login layout beyond the existing biometric unlock requires an owner-approved local credential design or a real identity backend.\n\n## 4. Screen-level gaps

The canonical screen inventory remains `docs/ui/screen-map.md`. The following are not complete merely because they appear in that map:

- Splash/onboarding and first-run local workspace setup.
- Global search, domain browser, tool search/favourites and a complete tool runner.
- Projects/data packs and complete job detail/log views.
- Dedicated sequence viewer/editor and alignment/tree viewers.
- Complete structure and chemistry viewers with validated offline lifecycle.
- Kinetics lab, charts studio and provenance detail viewer.
- Genomics/variant and PGx research screens, subject to P-track gates; clinical PGx interpretation and clinical deployment remain prohibited.
- In-silico job builder, subject to I-track engine gates.
- Complete security/privacy centre, data inventory and deletion controls.
- About/licence presentation and final owner-brand integration.
- Every empty/loading/running/success/partial/failure/cancelled/recovery-required state for each real workflow.

The Home/Work/Settings shell must remain truthful. Do not add fake user profiles, cloud login, demo jobs, fabricated progress, fabricated scientific results or controls with no real action.

## 4. Required exact-head closure evidence

The following evidence must be attached to the commit that is proposed for Track U engineering closure:

1. CI green on exact `main` commit, including Android arm64 debug APK/AAB build and JVM/package tests.
2. APK and AAB (where configured) verified as non-empty, package-aligned, and accompanied by SHA-256 hashes and build-environment record.
3. Generated token outputs reproducible from canonical token source with no diff.
4. Kotlin/Compose tests for navigation, all visible controls, theme persistence, workflow states and recovery.
5. Storage/security regression tests covering SAF, cancellation, resume, deletion, orphan cleanup, encrypted chunk integrity and Keystore-loss behavior.
6. Registry/dispatcher parity: each runnable card maps to a real input contract, dispatcher, result type and provenance path.
7. Contrast measurements for both themes; touch-target bounds; semantics/focus/TalkBack; 200% font scaling; reduced motion; RTL and keyboard/switch navigation.
8. Screenshot evidence for compact 360×800, baseline 393×852, large 430×932, tablet 600dp+, landscape and split-screen.
9. Named emulator and physical-device evidence, including performance and memory measurements on the agreed low-end ARM64 device.
10. Dependency, asset, font, icon and viewer provenance/licence/security review.
11. Updated quality report, screen map, implementation plan and session log reflecting the same exact commit and actual evidence.

A CI compile/build is not proof of UI acceptance, scientific validity, clinical safety or physical-device compatibility. Engine smoke checks are not scientific validation.

## 5. Cross-track carry-forward gates

- Track G independent/operational acceptance obligations remain OPEN as recorded in the implementation plan.
- D-025 authorizes research testing within the declared institutional approval; clinical PGx interpretation, patient-facing diagnosis, treatment or dosing must not be implemented or implied.
- U4 remains dependent on S1–S3 and viewer dependency/security review.
- U5 remains dependent on P1–P3 and I2–I4.
- No UI work may silently change the established Python/C++/Rust ownership boundaries or the JSON Schema engine envelope.

## 6. Closure rule

Track U may be described as **engineering-complete** only after U0–U6 engineering tasks have either passed their explicit acceptance criteria or are documented as externally blocked with an owner, dependency, evidence and non-claim. It may be described as **release-ready** only after all required independent, accessibility, security, scientific and physical-device approvals are separately satisfied.

**Current decision: Track U is OPEN.** The merged commit is a foundation milestone, not Track U completion.

## 6. Engineering work versus external acceptance

Engineering closure is not held open merely because a scientific or ethics approval is pending. Complete all work that can be completed safely in code: user journeys, local workflows, input bounds, deterministic outputs, persistence where appropriate, recovery, export, automated regression tests, UI states, accessibility semantics, build reproducibility and documentation.

The following are external/owner gates rather than ordinary coding tasks: ethics approval for a defined protocol; data-use permissions and licences; qualified clinical/PGx review; independent scientific concordance; owner risk decisions; physical-device testing where no device is attached to CI. The app must not imply that those approvals have been granted.

The presentation brief is docs/ethics-committee/engineering-evidence-brief.md. It records the supported research-only demo path, local data handling, explicit exclusions and evidence gaps without claiming ethics approval.


## 7. Public database retrieval integration — 2026-11-18

### Source implementation now present
- `PublicDatabaseClient.kt`: allow-listed HTTPS adapters for NCBI Gene/nuccore/protein, UniProtKB and RCSB PDB mmCIF-by-entry-ID.
- `PublicDatabaseCard.kt`: Home search and retrieval controls, sequence analysis dispatch, saved-record listing and deletion.
- `PublicRecordStore.kt`: encrypted app-private source payload cache using Android Keystore AES-GCM chunked files; SQLite metadata index.
- `StructureViewer.kt`: accepts fetched RCSB mmCIF, invokes the existing Python preparation/parser and opens the offline structure viewer.
- `KineticsUi.kt`: connects public structure retrieval to the existing Home structure viewer.
- `PublicDatabaseClientValidationTest.kt`: input-validation tests for unsupported databases, malformed accessions and malformed PDB IDs.

### Current truthful status
- NCBI nucleotide/protein and UniProt FASTA: retrieval, encrypted payload save and existing on-device FASTA QC are wired in source.
- RCSB PDB entry ID: mmCIF retrieval, encrypted payload save and existing parser/viewer handoff are wired in source.
- NCBI Gene: metadata search plus linked nucleotide/protein discovery through ELink; selected linked records use the existing FASTA retrieval and QC path.
- Saved records: visible and deletable; saved mmCIF can be reopened in the viewer and saved FASTA can be re-analysed. A richer saved-record detail/history browser remains open.
- Source payload encryption is implemented; SQLite metadata and analysis JSON remain plaintext within app-private storage.
- RCSB search is entry-ID based, not text/ligand/organism discovery.
- Provider retry/cancellation, release/licence metadata, cache quotas, physical-device behavior and scientific validation remain open.

### Required verification
- Run `2985` (`44229328602`) on commit `3dfc8b903f6928b65e673b2bb9a7ffb0586ff335`: arm64 APK/AAB build and 16 KiB native alignment checks PASSED; Android JVM unit-test compilation FAILED because `ResearchStoreMigrationTest.kt` passed `1L` where an `Int` byte-count argument is required. The test fixture was corrected at commit `2334b0703553e833adbf6a8de44c28826aebf05a`. The produced APK/AAB belongs to the older `3dfc` commit and is not the exact-main release candidate.\n- Earlier runs `2959` and `2971` failed on pre-fix commits: a Kotlin runtime-status type mismatch and governance identifier-range checks. Those source issues were corrected in subsequent main commits.\n- Latest exact-main CI run after the test correction is queued; do not claim release verification until its Android build, JVM tests, artifact inspection and hash capture all pass.
- Do not report APK availability until artifact enumeration confirms a non-empty APK and its SHA-256.
- An APK/AAB was produced by run 2985 on an older commit, but that run's JVM test stage failed and the artifact is not current-main evidence. No successful APK artifact has been verified for the latest main commit.
- Device tests must cover network failure, malformed response, large structure, Keystore loss, saved-record deletion, FASTA result persistence and actual 3D viewer opening.
- Track U remains OPEN. Public retrieval source integration is not equivalent to U-track completion or scientific validation.


## 8. Public database integration follow-through — 2026-11-18

- The integration checklist is committed at `docs/track-u/public-database-integration-checklist.md`; it separates implemented source paths from provider expansion, parser work, reliability and acceptance evidence.
- The public database rulebook status is reconciled with implementation: NCBI Gene ELink discovery, saved-record listing/deletion, FASTA re-analysis and mmCIF reopen are present in source. Metadata/analysis SQLite remains plaintext; raw payloads alone are encrypted.
- Workflow `44233607824` was created for `e89c475a2ad2fe4c5451926f077d5d1a9bb434a9`. Host-side scientific smoke/test jobs reported success; Android test/build was still running at audit refresh. No final Android conclusion or exact-head APK artifact is claimed.
- The earlier Android compiler failure was isolated to a test fixture passing a Long expression to a ByteArray size parameter. The fixture was corrected at `e89c475a2ad2fe4c5451926f077d5d1a9bb434a9`. This correction is not verified until exact-head JVM tests pass.
- Documentation commits trigger a new exact-head run. At refresh, workflow `44233969938` for `ca95e2816d93feffc29b487195d7b7c3fa445e8c` was pending.
- Track U and public database integration remain OPEN. Continue with exact-head CI, provider journey and encrypted-record lifecycle tests, retrieval cancellation/retry/cache management, typed parser/engine integration, then physical-device and accessibility acceptance.


## 9. Engineering follow-through — 2026-11-18 05:37 UTC

- Fixed the unresolved Compose biometric icon reference by using the available filled fingerprint vector. The earlier Android compile failure at `KineticsUi.kt:1398` is addressed in source at `2956ac803698c7d13212f036cab4112ea01b5139`.
- Corrected service dispatch so aggregate VCF QC and the U5 research gate appear only on the exact `genomics.sam_vcf` capability destination, not on every capability whose broad domain label happens to be Genomics or Variant. Source change: `d99ed33d5ac8bc633b2e867d0d89d55f5567d239`.
- Updated `tests/test_android_scientific_viewers.py` to assert the supported fingerprint icon reference and exact VCF service routing. Test change: `7fec05ca181790134b87e2704be77a651351ef83`.
- Exact-head workflow `44245420057` is queued for `7fec05ca181790134b87e2704be77a651351ef83`; it has not yet produced Android build or JVM test evidence.
- The 68-entry capability catalogue is not 68 runnable Android workflows. Current Android dispatchers are explicitly bounded to the implemented paths documented in `ServiceDetailScreen`; other entries are catalogue-backed service detail/status destinations and must not be represented as executable.
- Remaining coding work includes typed Android-to-engine dispatch for additional capabilities, complete public-database lifecycle/reliability, login/account architecture decision and implementation, and missing service-specific workflow UI. Device/visual/scientific acceptance remains a later testing phase.


## 10. Additional Android workflow integration — 2026-11-18

- Commit `92824712238e7dd54ddcab5e5ab8e8552e1d0014` adds local Android execution for protein descriptors, primer property screening and SpCas9 NGG PAM scanning.
- Commit `520d3b5777294871645a88f1566341ac8b1d1747` adds local Android execution for six-frame ORF candidate scanning, Michaelis–Menten rate calculation and Newick parsing.
- Android-connected workflows now total 14 including the public-reference-database service; the other 55 catalogue entries remain Python-source-only from the Android app's perspective.
- Added `docs/track-u/android-capability-integration-matrix.md` to map every catalogue entry to its Android integration state and to prevent source registration from being presented as mobile execution.
- Exact-head CI for `520d3b5777294871645a88f1566341ac8b1d1747` is queued at the time of this update. No build/test success is claimed until that run completes.
- Engineering integration is still open. The remaining work is enumerated in the matrix; scientific, device, accessibility and independent acceptance are later evidence gates.


## 11. Further Android workflow integration — 2026-11-18

- Commit `a136f133369cec91180b2d474dd03093008c9cb9` adds Android workflows for bounded global alignment, FASTA contig assembly QC, PDB SASA, distance-only interaction candidates, microbiome diversity indices and logistic growth.
- Commit `b1bb7fc8ea9909f3cea6ac071144791ed674e3d6` updates the Android-connected status allow-list and adds a regression assertion that these routes are reported correctly.
- The Android app now exposes 19 of 68 catalogue capabilities through dedicated local forms and typed/allow-listed Python bridge dispatch, plus the separate public-reference-database service: 20 Android workflows in total. The remaining 49 catalogue entries are not yet connected to Android.
- Updated `docs/track-u/android-capability-integration-matrix.md` with the new route mapping, source-to-Android distinction and remaining integration work.
- Exact-head CI has not yet completed for this source revision. These changes are not declared build-verified until CI passes.


## 12. Additional mobile scientific workflows — 2026-11-18

- Commit `3dce2837afd68b3deafbe0ffee634061c9b04d5f` adds local Android workflows for explicit NCBI genetic-code translation, enzyme inhibition rate calculation and UPGMA tree construction.
- Commit `58b35adb8d03ec1b0e65f825efa9596a1aae2898` corrects host-test input fixtures to use actual line breaks and adds explicit allow-list coverage for the new routes.
- The Android app now exposes 21 of 68 catalogue capabilities through dedicated Android forms and the local Python bridge. The separate public-reference-database service makes 22 Android workflows; 47 catalogue capabilities remain unconnected.
- The integration matrix has been refreshed with the exact capability-by-capability mapping.
- Latest exact-head CI is pending; no test or APK verification is claimed for these commits yet.


## 13. Additional omics and phylogenetic mobile workflows — 2026-11-18

- Commit `ce54dfbcd9f724ee857d8420a7aef52b17b48991` adds Android workflows for CPM/CLR omics normalisation, cross-omics Pearson correlation and Jukes–Cantor neighbour-joining from caller-supplied alignments.
- All three routes are explicitly allow-listed, have bounded matrix/sequence sizes and include limitations to prevent unsupported interpretation.
- The Android app now exposes 24 of 68 catalogue capabilities; 44 catalogue capabilities remain unconnected. Including the separate public-reference-database service, 25 Android workflows are available in source.
- Updated the integration matrix with these routes. Exact-head CI is pending and no APK verification is claimed yet.


## 14. Genome annotation mobile workflows — 2026-11-18

- Commit `617c1ef89e8714223739e61036a26c649bfcd335` adds Android workflows for GFF3 structural annotation validation and transcript CDS reconstruction from supplied contigs.
- The bridge applies 1 MB input bounds, 50,000-feature annotation bounds, 10,000-transcript reconstruction bounds and caller-selected genetic-code table metadata. It does not infer gene function or clinical effects.
- The Android app now exposes 26 of 68 catalogue capabilities; 42 remain unconnected. The separate public-reference-database service brings the source-level mobile workflow count to 27.
- Updated the capability integration matrix. Exact-head CI is pending.


## 15. Additional protein, genome and kinetics workflows — 2026-11-18

- Commit `e9a94daff65e799ab141097bc182986a97776fcb` adds a bounded Android protein motif scanner that hashes the caller-supplied motif pack and requires source/licence metadata; it does not download or independently verify the pack.
- Commit `c4640967d7c3ce0982a94372ac0ea06b2b92149f` adds a multi-contig prokaryotic ORF candidate scanner and paired Michaelis–Menten bootstrap intervals with a 100–500 replicate mobile limit.
- The Android app now exposes 29 of 68 catalogue capabilities; 39 remain unconnected. The separate public-reference-database service brings the source-level Android workflow count to 30.
- Updated the capability matrix. Exact-head CI is still pending.


## 16. Protein design governance and structure geometry — 2026-11-18

- Commit `74002543c0614e895c5750389fd36b4e5857a73c` adds Android validation of protein-design research briefs. The underlying engine explicitly blocks sequence generation until model, data, safety and review gates are approved.
- Commit `73dd399e9bf04bfff035245df32f1749e113da8e` corrects the PDB fixture and retains regression coverage for the bounded structure geometry screen.
- The Android app now exposes 31 of 68 catalogue capabilities; 37 remain unconnected. Including the separate public-reference-database service, 32 Android workflows are represented in source.
- Updated the integration matrix. Exact-head CI remains pending.


## 17. Structure mapping and phylogenetic support workflows — 2026-11-18

- Commit `09e0c5cfb467df24503159847b0783fe606b80e5` adds a bounded neighbour-joining alignment-site bootstrap and exact chain sequence mapping plus inter-chain contact geometry.
- Commit `e5f3f1dac828bb8b583a03997b75a736b776c346` adds alignment-based coordinate mapping with ambiguity abstention and amino-acid variant-to-coordinate mapping. These are coordinate tools only; they do not predict biological or clinical effects.
- The Android app now exposes 34 of 68 catalogue capabilities; 34 remain unconnected. Including the separate public-reference-database service, 35 Android workflows are represented in source.
- Updated the integration matrix. Exact-head CI remains queued behind the current Android build.


## 18. Current integration reconciliation — 2026-11-18

- Reviewed the live 68-entry capability catalogue against the Home/service-page routing, Kotlin runner allow-list, Python bridge dispatch and the dedicated FASTA, FASTQ, genetic-code inference, VCF QC, chemistry and structure workflows.
- The reconciled count is **43 of 68 catalogue capabilities connected to Android workflows; 25 remain unconnected**. The public reference-database retrieval service is additional to the 68-entry catalogue.
- Added the missing Kotlin allow-list entry for `kinetics.inhibition_rate`; its Python handler and UI form already existed. Added regression coverage requiring UI, Kotlin and Python route parity.
- Added six missing route rows to the integration matrix: exact/local FASTA reference search, local alignment reference search, Newick export alias and PDB geometry alias.
- Hardened mobile cross-omics input validation for non-empty rectangular feature matrices with at least three matched samples, and rejected malformed neighbour-joining sequence names/values before engine dispatch.
- Source-level integration is not a scientific validation claim. CI for the resulting commit is pending; no exact-head APK/build success is claimed in this addendum.


## 19. HMMER evidence workflows — 2026-11-18

- Added Android service-page routes for `protein.hmmscan_domain_evidence`, `protein.hmmscan_domtblout_evidence` and `protein.hmmer_domain_candidate_ranking`.
- The two parser IDs share the bounded pure-Python domtblout parser (20,000 lines, 16 KB per line and 10,000 domains). Profile name/version/licence/source/SHA metadata is mandatory but remains caller-supplied; the app does not execute HMMER or independently verify the underlying profile pack.
- The ranking route uses explicit caller thresholds for independent E-value, profile coverage, query coverage and alignment accuracy. Results remain candidate evidence and do not establish protein function or orthology.
- The reconciled catalogue count is now **46 of 68 connected; 22 remain unconnected**, plus the separate public reference-database service.
- Exact-head CI is pending. No APK success or scientific validation is claimed.


## 20. External structure-prediction envelope validation — 2026-11-18

- Added `structure.prediction_envelope_validation` to the dedicated Structure service page and the bounded Kotlin/Python allow-lists.
- The route validates sequence SHA-256 binding, model and node provenance fields, timestamp, structure-view payload, residue confidence vector and confidence summaries (5,000 residues / 1 MB viewer payload).
- It does **not** execute a prediction engine, verify model weights/licences, calibrate confidence, assess node trust or certify structural accuracy. Valid output remains `unverified_prediction`.
- The reconciled Android catalogue count is **47/68 connected; 21 remain unconnected**, plus Public Reference Databases as a separate service.
- Exact-head CI remains pending; no APK or device acceptance is claimed.


## 21. NCBI Gene snapshot composition report — 2026-11-18

- Added `genes.catalogue_coverage_report` as a dedicated Gene Reference Data service action.
- The bridge accepts up to 900 KB of gene_info TSV and 10,000 records, requires an explicit source-release label, and reports taxonomy/gene-type/release counts and missing annotation fields.
- The report intentionally returns no genome-wide coverage percentage: its scope is only the supplied snapshot. This is not a substitute for the in-app live NCBI Gene search/retrieval adapter.
- The reconciled Android catalogue count is **48/68 connected; 20 remain unconnected**, plus the separate public reference-database service.
- Exact-head CI remains pending; no APK/device acceptance is claimed.


## 22. Experimental structure coordinate comparison — 2026-11-18

- Added `structure.experimental_ca_comparison` to the Structure service page and the bounded local bridge.
- The action parses two caller-supplied PDB structures, requires at least three CA residues in each, enforces 900 KB combined input and 5,000 atoms per structure, and records SHA-256 hashes of both source texts.
- Comparison requires exact chain/residue/residue-name correspondence and reports superposed CA RMSD only. It does not perform alignment, calculate TM-score, validate biological function or certify experimental accuracy.
- The reconciled Android catalogue count is **49/68 connected; 19 remain unconnected**, plus the separate public reference-database service.
- Exact-head CI remains pending; no APK or device acceptance is claimed.


## 23. Android route completion for remaining catalogue entries — 2026-11-18

- Added Android service-page access and Kotlin/Python allow-list routing for all 20 entries missing from the strict UI + Kotlin + Python intersection. `genes.ncbi_catalogue` already had a UI route; its Kotlin and Python routes were added here.
- Implemented mobile bridges for local FASTA reference-pack ingestion/search, reference-bound and basic variant normalization, NCBI Gene snapshot ingestion, NB2 GLM, BGZF BAM core-field aggregation, PGx definition matching, PharmVar parsing/matching, deterministic structure viewer payload generation and structure-session export.
- Added dependency-aware adapters for BLASTP, HMMER hmmpress/hmmscan, RDKit, pysam/HTSlib, S4 prediction process, AUGUSTUS, Prodigal and generic pinned GFF3 annotation. These require separately installed Android-compatible binaries/libraries; they are not bundled in the current Android build. RDKit and pysam/HTSlib are also not installed in the current Chaquopy environment. Those routes must report missing dependencies rather than pretend to execute.
- The catalogue has **68/68 Android route registrations** across UI, Kotlin allow-list and Python dispatch. This is route coverage only—not proof that optional engines are packaged, executable out of the box, scientifically validated or clinically validated.
- Added regression tests for route parity and execution of the NB2, reference-normalization, viewer-payload and conservative PGx no-call paths.
- Exact-head CI/build is required before APK success is claimed.
