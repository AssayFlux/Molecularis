# Molecularis — Session Log

## 2026-11-07 — Session 2: Align direction system with complete master
**Phase:** Track R / R0 Foundations  
**Objective:** Archive the owner-supplied master, reconcile roadmap/decision log, and prepare the R0 plan before implementation.

### Done
- Re-read NORTH_STAR.md, ROADMAP.md, DECISIONS.md and prior session entry.
- Reconstructed the complete 18-part master supplied by the owner in this conversation at docs/origin/KINETICS_MASTER.md as read-only history. This is a reconstruction, not a Git move; no root master file existed.
- Updated ROADMAP to reflect actual archive and R0 status.
- Updated DECISIONS: D-007 records archival reconstruction; all six owner decisions remain open.
- Added docs/phase-r0-plan.md.
- NORTH_STAR.md was not changed.

### Validated
- Prior main-branch tree and four living files were read before edits.
- No CI, tests, registry checker, app build, scientific validation, Android feasibility or device verification has been run or claimed.

### Not done
- R0 implementation: skeleton, registry, checker, reproduce-all, pre-commit and CI.
- No LICENSE selected or added.
- No Android/device or scientific work; no P0 or clinical functionality.

### Risks / blockers
- Direction baseline remains proposed until explicit owner approval.
- R0 exit requires actual green CI on empty skeleton.
- License, jurisdictions, paper framing, advisers, PGx gene set and target devices remain open.

### Next step
Present direction documents and open decisions for owner approval. After approval, execute R0 plan and stop at its CI-green exit gate.

### Gate status
WAITING FOR OWNER APPROVAL — direction baseline. R0 implementation has not started.


## 2026-11-07 — Session 3: R0 foundations implementation
**Phase:** Track R / R0 Foundations  
**Objective:** Implement the approved empty-skeleton foundation and verify its automated checks.

### Done
- Owner explicitly approved the NORTH_STAR / ROADMAP / DECISIONS baseline.
- Confirmed current `main` head before implementation.
- Prepared repository skeleton directories for Android, Python, Rust, C++, WebView assets, engines, data packs, domains, remote node, validation, benchmarks, paper and governance.
- Added an intentionally empty capability registry, evidence-job registry, registry checker and negative/positive checker tests.
- Added reproduce-all R0 stub, developer tooling configuration, pre-commit hooks, CI workflow, README and architecture / Android feasibility / third-party records.
- Preserved existing brand assets and historical master archive.
- No LICENSE selected; six owner decisions remain open; P0 remains blocked.

### Validation status
- Automated CI has been configured but its GitHub Actions result has not yet been inspected.
- No local test execution is claimed in this session.
- Android/native toolchain, APK/AAB, 16 KB alignment and package-size checks are explicitly blocked/not applicable in R0.
- No scientific validation, Android feasibility, device verification or clinical evidence is claimed.

### Not done / risks
- R0 is not complete until the actual Actions run is green and any failures are corrected.
- Native and Android checks are deferred to R1; the workflow reports this as a blocker rather than a pass.
- Project license, jurisdictions, paper framing/venue, advisers, initial PGx gene set and target devices remain open.

### Next step
Inspect the GitHub Actions run on `main`, fix any failures, record the actual run URL/result, then stop at the R0 exit gate for owner review.


## 2026-11-07 — Session 4: R0 validation and exit-gate review
**Phase:** Track R / R0 Foundations  
**Objective:** Validate the completed R0 scaffold in GitHub Actions, record evidence and stop at the owner gate.

### Done
- Added the repository metadata and governance entry points: LICENSE status placeholder (no license grant), CHANGELOG, SECURITY, PRIVACY, CONTRIBUTING and CITATION.cff.
- Added executable `scripts/reproduce-all` wrapper and expanded pre-commit checks for Ruff, Black and mypy.
- Strengthened registry checks so implemented tools require implementation metadata; validated tools require existing validation-record IDs; device verification requires a device log; clinical tools require the Part 12 gate/evidence; and public/paper claims may reference only validated tools.
- Kept the six open owner decisions unchanged.

### Validated
- GitHub Actions run 1373: [successful run](https://github.com/AssayFlux/Kinetics/actions/runs/42378594100) on commit `043cffe1c15dbf4361a7323e2febe42155334513`.
- Pre-commit configuration validation passed.
- Ruff lint passed.
- Mypy strict type-check passed.
- Registry validation passed for the intentionally empty R0 registry.
- Unit tests: **11 passed**.
- Reproduction stub ran and correctly reported that no evidence jobs are registered.
- Android artifact check explicitly reported BLOCKED / NOT APPLICABLE: no APK/AAB exists. Native/Android CI job explicitly reports the R1 blockers and does not claim native build success.

### Not done / risks
- No Android application/build, embedded Python, Rust/C++/Kotlin implementation, scientific capability, benchmark, device run, 16 KB alignment result or APK/AAB size result exists.
- No scientific validation, clinical evidence or patient-data workflow exists.
- Project license remains unselected; jurisdictions, paper framing/venue, clinical advisers, initial PGx genes and target devices remain open.
- First CI attempt failed on Ruff lint; issues were corrected, and the subsequent complete run 1373 passed.

### Gate status
**R0 implementation and automated acceptance checks are complete. Awaiting explicit owner acceptance of the R0 exit gate. R1 has not started.**


## 2026-11-07 — Session 5: Final R0 CI verification
**Phase:** Track R / R0 Foundations  
**Objective:** Verify the final R0 documentation/governance commit and leave an accurate owner-gate status.

### Validated
- Final R0 commit: `6746e124ed888afd1d284a6a52d0eb1432b33fe9`.
- GitHub Actions run 1375 on the final R0 commit: [successful run](https://github.com/AssayFlux/Kinetics/actions/runs/42378747002).
- Both workflow jobs completed successfully.
- Pre-commit configuration validation, Ruff lint, strict mypy, registry validation, all **11 tests**, reproduce-all wrapper and Android artifact gate-status check passed.
- The native/Android job passed only its explicit R0 blocker-reporting step. No native or Android build was performed or represented as passed.

### Current state
- R0 implementation and automated acceptance checks are complete.
- R0 exit gate is awaiting explicit owner acceptance. R1 has not started.
- Six owner decisions remain open; the LICENSE file is only a no-license-selected notice, not a license grant.
- No scientific capability, scientific validation, Android feasibility, device verification, patient-data workflow or clinical feature is claimed.

### Next step
Wait for the owner's explicit R0 exit-gate approval. On approval, begin R1 feasibility planning and stop again at its go/no-go gate.


## 2026-11-07 — Session 6: R1 Android feasibility started
**Phase:** Track R / R1 Android feasibility  
**Objective:** Start the R1 feasibility investigation and define evidence requirements without crossing the R1 go/no-go gate.

### Done
- Owner authorised R1 on 2026-11-07; R0 exit is treated as accepted.
- Read NORTH_STAR.md, ROADMAP.md, DECISIONS.md and the prior session log.
- Confirmed current main tree and existing R0 scaffolding.
- Added the R1 phase plan with experiments, evidence protocol, device constraints and exit criteria.
- Updated roadmap: R0 done; R1 in progress. R2 and R3 remain not started.
- NORTH_STAR status metadata now reflects the already-approved baseline; mission and scope are unchanged.

### Not done / validation status
- No Android project, APK/AAB, emulator or physical-device experiment has been run in this session.
- Embedded Python/Biopython, Rust FFI, C++ JNI, real engine, RDKit/alternative, offline viewer, 16 KB alignment, package size, cold-start and memory results are all untested.
- No scientific capability or clinical feature is implemented or validated.
- Target device decision D-006 remains open; six owner decisions remain open.

### Risks / blockers
- Physical-device evidence requires owner-selected or owner-provided arm64 target hardware. Emulator results cannot substitute for it.
- Candidate scientific engines and chemistry libraries require upstream support and license review; restrictive licenses require owner approval.
- R1 go/no-go must be reviewed and approved before R2. R3 depends on R2 and cannot start in parallel.

### Next step
Continue R1 experiments and record raw reproducible evidence in docs/android-feasibility.md. Stop at the R1 go/no-go gate.


## 2026-11-07 — Session 7: Owner decision D-001 — project license
**Phase:** Track R / R1 Android feasibility (in progress)
**Objective:** Record the owner's project-license selection and proceed to the next owner decision without changing R1 scope.

### Done
- Owner selected **Apache License 2.0 (Apache-2.0)** on 2026-11-07.
- Recorded D-001 as approved in DECISIONS.md, including the choice, rationale/options and third-party license caveat.
- Updated ROADMAP.md: five owner decisions remain open; canonical LICENSE grant text remains to be added as a repository task.

### Not done / validation status
- The canonical Apache-2.0 LICENSE file has not yet been added; the repository must not be described as carrying the license grant until that is committed.
- Third-party engines, dependencies, models and data packs still require individual license verification.
- No R1 feasibility result is changed by this governance decision.

### Next step
- Ask the owner to decide D-002: target jurisdictions.


## 2026-11-07 — Session 8: Owner decision D-002 — target jurisdictions
**Phase:** Track R / R1 Android feasibility (in progress)
**Objective:** Record the owner's geographic and long-term clinical ambition while retaining all jurisdiction-specific safety and regulatory gates.

### Done
- Owner selected option 5: global scope, including possible future clinical use.
- Recorded D-002 in DECISIONS.md as an approved strategic scope decision.
- Updated ROADMAP.md: four owner decisions remain open; jurisdiction-specific reviews and approvals remain mandatory.

### Constraints and interpretation
- This is a product ambition, not evidence of legal compliance, regulatory clearance, market authorisation or permission to process patient data anywhere.
- Research Mode remains the only public mode; Clinical Decision Support Mode remains disabled.
- Before patient-data workflows, clinical features/studies or market entry, identify each relevant jurisdiction and obtain qualified local privacy, health-data, medical-device/software, research-ethics and other applicable advice/approvals.
- P0 and all existing clinical, ethics, security and evidence gates remain mandatory. No global approval is presumed.

### Next step
- Ask the owner to decide D-003: research-paper framing and venue strategy.


## 2026-11-07 — Session 9: Owner decision D-003 — research-paper strategy
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's publication strategy and set evidence-based publication milestones without changing R1 scope.

### Done
- Owner selected option 4: multiple papers over time.
- Recorded D-003 as approved in DECISIONS.md.
- Updated ROADMAP.md with a staged publication strategy: platform/software-methods paper after adequate R1–R3 evidence, then separate domain papers only after independent validation.
- Recorded the owner's request for guidance at relevant milestones.

### Constraints and interpretation
- This is a publication strategy, not a claim that a paper is ready, submitted, accepted or peer reviewed.
- No unsupported capabilities, fabricated results or broad claims across unvalidated domains.
- Venue requirements, authorship, affiliations, funding, competing interests and manuscript claims require owner review when the evidence and candidate venue are known.
- R1 remains in progress; R2 remains gated on R1 evidence and explicit owner go/no-go approval.

### Next step
- Ask the owner to decide D-004: clinical advisers/advisory board.


## 2026-11-07 — Session 10: Owner decision D-004 — clinical adviser timing
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's decision to defer clinical-adviser recruitment while preserving the P0 and clinical-scope gates.

### Done
- Owner selected option 3: defer clinical advisers until the software is more mature.
- Recorded D-004 as approved in DECISIONS.md.
- Updated ROADMAP.md: revisit adviser recruitment at a maturity milestone, targeting after R3 and before P0/PGx work.

### Constraints and interpretation
- No clinical advisers are being represented as recruited or engaged.
- P0 remains blocked until qualified advisers and all other legal, ethics, regulatory, QMS and evidence prerequisites are satisfied.
- No patient-data workflows, clinical studies, PGx gene-set selection or clinical-scope implementation may begin ahead of the required gates.
- Research Mode remains the only public mode; Clinical Decision Support Mode remains disabled.

### Next step
- Ask the owner to decide D-005: initial PGx gene set.


## 2026-11-07 — Session 11: Owner decision D-005 — initial PGx panel breadth
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the intended initial PGx panel breadth without selecting genes or bypassing the deferred clinical-adviser gate.

### Done
- Owner selected option 2: target a broader initial panel of approximately 15–20 genes.
- Recorded D-005 as an approved strategic breadth decision in DECISIONS.md.
- Updated ROADMAP.md to reflect the 15–20-gene target while retaining evidence-based staging.

### Constraints and interpretation
- No individual PGx gene has been selected, validated, implemented or clinically endorsed by this decision.
- Exact gene selection is deferred until qualified clinical advisers are engaged after the D-004 maturity checkpoint and before P0/PGx implementation.
- Selection must consider guideline support, reference materials, caller/assay reliability, ancestry coverage, evidence quality, licensing and validation feasibility. Do not pad the panel to meet a numerical target; a smaller or staged panel may be proposed if evidence warrants.
- P0 remains blocked; Research Mode remains the only public mode. No patient-data or clinical use is authorized.

### Next step
- Ask the owner to decide D-006: target Android devices and minimum support matrix.


## 2026-11-07 — Session 12: Correct D-005 to owner-selected six-gene PGx scope
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Correct the PGx decision record to match the owner's explicit option 1 selection.

### Done
- Owner selected option 1: focused starter set of CYP2D6, CYP2C19, CYP2C9, VKORC1, TPMT and DPYD.
- Corrected D-005 in DECISIONS.md. The prior 15–20-gene entry did not match the owner's selection and is superseded by this correction.
- Updated ROADMAP.md and the P2 scope description to reflect the provisional six-gene research scope.

### Constraints and interpretation
- The six genes are a provisional planning scope, not a clinically approved panel, validated assay or implemented capability.
- Qualified advisers must review the list after the D-004 maturity checkpoint and before P0/PGx implementation. Review includes guideline support, reference data, locus/caller limitations (including CYP2D6 structural variation), ancestry coverage, licensing and validation feasibility.
- P0 remains blocked. No patient-data or clinical use is authorized.

### Next step
- Ask the owner to decide D-006: target Android devices and minimum support matrix.


## 2026-11-07 — Session 13: Android target approved; gene scope broadened and reopened
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's Android device target and capture the revised broad gene-scope direction without guessing its exact boundary.

### Done
- Owner approved D-006 option 1: Android 10+ (API 29), 64-bit ARM, with low-end, mid-range and flagship device test tiers.
- Updated DECISIONS.md and ROADMAP.md. This is a target matrix, not a verified compatibility claim.
- Owner clarified that the earlier six-gene PGx scope is too narrow and requested a large, broad gene scope.
- Reopened D-005 and superseded the six-gene list; exact scope boundary remains to be clarified.

### Constraints and interpretation
- Clarify whether “all types of gene” means a comprehensive PGx gene panel or a cross-domain gene catalogue spanning Kinetics' genomics and related scientific domains.
- Do not invent a gene count, freeze a list, or claim genes/callers are implemented or validated.
- PGx and all patient-related/clinical work remain subject to qualified advisers, P0, jurisdiction-specific legal/ethics/regulatory requirements and owner approval.
- R1 must test emulator and physical arm64 devices; the target does not establish support for every Android 10+ device.

### Next step
- Clarify the intended breadth of the gene catalogue before revising P2 or creating a gene inventory.


## 2026-11-07 — Session 14: Owner approves both gene-scope dimensions
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Resolve D-005 scope direction for both comprehensive PGx and cross-domain gene coverage.

### Done
- Owner explicitly selected both: (1) a comprehensive, expandable PGx gene panel and (2) a broad cross-domain gene catalogue spanning genomics and relevant Kinetics domains.
- Updated D-005 in DECISIONS.md and the gene strategy/P2 descriptions in ROADMAP.md.
- Defined PGx as a specialised workstream within the wider catalogue, with distinct evidence, reference, caller/assay, interpretation and validation requirements.

### Constraints and interpretation
- The previous six-gene list is not the agreed scope limit.
- No fixed gene count or exhaustive coverage claim is implied. Inventory and implementation waves must be evidence-led.
- Listing a gene does not imply that analysis, caller, assay or interpretation is implemented or validated.
- PGx remains research-only and gated by qualified advisers, P0, jurisdiction-specific legal/ethics/regulatory requirements and owner approval. No patient-data or clinical work is authorized.

### Next step
- Develop the gene-catalogue taxonomy and prioritisation framework as a planned work item after the current R1 feasibility gate; do not interrupt R1 or start R2 before its go/no-go approval.


## 2026-11-07 — Session 15: Direction-file reconciliation and R1 continuation
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Continue repository hygiene and keep the phase gate accurate while awaiting an unambiguous owner approval statement.

### Done
- Reconciled DECISIONS.md after D-001 through D-007 were resolved: replaced the obsolete “Open decisions” section with standing guidance and removed the superseded D-005 clarification-pending text.
- Corrected docs/android-feasibility.md to reflect the approved D-006 Android target and to avoid describing the target matrix as verified device support.
- Clarified that the first Android CI build failed on the missing host-Python prerequisite and that the later workflow result must be checked before any build-success claim.

### Gate and approval status
- The owner's message “R2 & R2 both approved” is ambiguous. A clarification was requested (R1 + R2 or R2 + R3); “Carry on” did not resolve which pair was intended. No new phase approval has been recorded from that exchange.
- R1 remains in progress. R2 remains gated on complete R1 evidence and an explicit R1 go/no-go decision. R3 depends on R2 and must not start early.
- D-001 through D-007 remain recorded as resolved/approved according to their respective scopes. The Apache-2.0 LICENSE grant text is still not installed; the current LICENSE file remains a non-grant placeholder.

### Next step
- Verify the latest Android workflow's terminal status and job steps; continue R1 experiments and record only reproducible evidence. Ask the owner to state the intended approval pair explicitly before changing phase gates.


### R1 CI evidence update — workflow run 1384
- Inspected GitHub Actions run 1384: [workflow run](https://github.com/AssayFlux/Kinetics/actions/runs/42379811746), commit `3bd4e152faf4007e44cd3fc0de63e5a26ecf065e`.
- Python foundation/registry/tests job completed successfully, including Ruff, mypy, registry validation, unit tests and reproduce-all stub.
- Android job successfully provisioned Python 3.11 and Android SDK/NDK. Gradle then failed at `:app:installDebugPythonRequirements`: pip could not find a matching `biopython` distribution in the configured PyPI/Chaquopy indexes.
- APK compilation did not complete; APK alignment, size reporting and artifact upload were skipped. No APK/AAB or Android runtime result is claimed.
- Updated docs/android-feasibility.md with this concrete blocker. Next R1 action: investigate a supported Chaquopy-compatible Biopython distribution/build strategy or a justified alternative, including license and ABI review; then rerun the build.


## 2026-11-07 — Session 16: Owner authorizes R1–R3 execution sequence
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Record the owner's explicit authorization to proceed through R1, R2 and R3 while preserving all phase exit gates.

### Owner approval
- Owner explicitly stated: “Approved R1,R2&R3” on 2026-11-07.
- Interpreted as authorization to execute R1, R2 and R3 sequentially. This resolves the earlier ambiguous “R2 & R2” wording.
- Recorded as D-008 in DECISIONS.md and reflected in ROADMAP.md.

### Gate status (unchanged)
- R1 remains in progress; run 1384's Android build is blocked at Chaquopy Biopython dependency resolution. No APK build/runtime success is claimed.
- R2 remains not started until R1 evidence is complete and the R1 go/no-go is documented.
- R3 remains not started until R2 exit evidence and approval.
- D-008 is execution authorization, not phase acceptance and not a waiver of scientific validation, licensing, physical-device, security, privacy, clinical or P0 gates.

### Next step
- Continue R1 by resolving the Biopython packaging blocker, rerunning Android build, then completing the embedded Python/native/device evidence matrix. Start R2 only after the documented R1 gate passes.


### R1 Biopython packaging investigation — 2026-11-07
- Rechecked the current Android Gradle configuration: Chaquopy 17.2.0, Python 3.11, arm64-v8a, and unpinned `biopython`, `numpy`, `scipy` pip installs.
- Reviewed current Chaquopy FAQ, package-index listing, wheel-build instructions and version-17 pip behavior. The no-matching-distribution error indicates there is no compatible Android distribution available through the configured indexes. Chaquopy documents custom Android-wheel builds for packages not already supported; version 17's normal index installs are binary-only.
- Biopython upstream source builds require Python headers and a C compiler. A normal sdist install cannot be assumed to work in Chaquopy's app build task. Next experiment: inspect exact Android wheel availability, then build a reproducible CPython 3.11 arm64 wheel with Chaquopy's documented toolchain if needed; verify extension linkage, 16 KB ELF alignment, license notices and representative runtime test vectors.
- Biopython licensing is not accurately summarized as BSD-3-Clause for the whole distribution: upstream identifies the Biopython License Agreement for most files and BSD-3-Clause dual licensing for some files. Added a third-party register note; no adoption/bundling approval is implied.
- Updated `docs/android-feasibility.md` and `docs/third-party.md` with the findings and candidate path. No dependency was removed, no build success is claimed, and no production technology choice was made.


### R1 custom Biopython wheel CI experiment — 2026-11-07
- Added `android/biopython-wheel/meta.yaml` pinned to Biopython 1.88.
- Updated the Android Gradle pip configuration to consume a local Android wheel and pin Biopython 1.88 and NumPy 1.26.2.
- Updated the Android CI job to check out Chaquopy 17.2.0, download its CPython 3.11.17 Android target and the Chaquopy NumPy 1.26.2 arm64 wheel, then cross-build Biopython for arm64-v8a using the documented Chaquopy wheel builder.
- CI prints the generated wheel SHA-256 and proceeds to APK/AAB build and 16 KB APK alignment check only if the wheel build succeeds.
- Updated the R1 evidence matrix and third-party register. This is an experiment, not a validated package: the CI run, APK build, emulator import/tests, ELF inspection and physical-device tests are still pending.
- Biopython 1.88 is pinned to a current upstream release; upstream PyPI metadata identifies NumPy as a required dependency and a Biopython-specific license expression. The custom recipe includes NumPy 1.26.2 as a host dependency for the cross-build. No production bundling approval is implied.


### R1 build pipeline correction — 2026-11-07
- Confirmed from the Chaquopy 17.2.0 tag that its Python 3.11 target is 3.11.17-0 and its legacy Android wheel builder uses NDK r27.3.13750724 internally, installing it from ANDROID_HOME if needed. Removed misleading environment overrides which pointed at the app-build NDK rather than the wheel builder's own configured toolchain.
- Confirmed Biopython 1.88 declares NumPy as a required dependency and uses setuptools 74.1+ with native C extension modules. The pinned Chaquopy wheel recipe uses NumPy 1.26.2 as the host/runtime requirement input.
- Added an explicit R1 risk: Chaquopy's Python 3.11 NumPy 1.26.2 Android wheel in the index dates from 2023, before the 16 KB compatibility era. It must be ELF-inspected and runtime-tested; if it fails 16 KB validation, the stack must be rebuilt or moved to a compatible newer Python/package path.
- This correction does not establish wheel-build success, APK/AAB success, or 16 KB compatibility.


### R1 first custom-wheel CI attempt — 2026-11-07
- Latest CI run 42382373740 passed the Python foundation job (Ruff, mypy, registry validation, unit tests and reproduction stub).
- Android job provisioned Java, Python, Android SDK/NDK, installed wheel-builder dependencies, checked out the pinned Chaquopy 17.2.0 source and downloaded its CPython 3.11.17 target plus Biopython 1.88 source.
- The first custom wheel build failed before Biopython compilation: Chaquopy's wheel builder created a libpython.so alias for both libpython3.so and libpython3.11.so; the second ln -s failed because the alias already existed. This is a toolchain alias collision, not a Biopython compiler failure.
- Added an assertion-checked, CI-local patch changing that alias creation to ln -sf, so the version-specific alias takes precedence. This does not modify the pinned upstream repository or claim wheel success; rerun required.
- Aligned the prototype app minSdk to API 29, matching D-006 Android 10+ target rather than leaving an accidental API 24 app floor.


### R1 Biopython wheel build attempt 2 — 2026-11-07
- The SONAME alias patch allowed the second CI attempt to progress through Biopython 1.88 C-extension compilation for aarch64 Android.
- Link failed because Chaquopy's compiler-wrapper.py removed the workspace-local Chaquopy host-library path from the compiler command as outside its allowlisted safe directories. Consequently ld.lld could not resolve -lpython3.11. The compile command was using Chaquopy's Android clang wrapper and the expected 16 KB max-page-size linker flag.
- Patched the pinned CI checkout's compiler-wrapper safe roots to include only GITHUB_WORKSPACE, in addition to its existing safe root. This allows the generated host headers/libraries under the repository's build directory while continuing to reject arbitrary host paths. Both toolchain patches are asserted and scoped to the pinned Chaquopy 17.2.0 build checkout.
- The custom wheel has not yet completed. APK/AAB, runtime, ELF, emulator and physical-device evidence remain outstanding.


### R1 Biopython wheel success / SciPy package blocker — 2026-11-07
- Latest custom-wheel CI attempt successfully built Biopython 1.88 for CPython 3.11 / Android arm64-v8a. Wheel SHA-256: cdf569ea13eb9314e43afeb9bbd3dbdbf95616d138f775a2e12e4cb7ba0cecbf.
- Gradle then consumed the generated local Biopython wheel and downloaded NumPy 1.26.2 successfully. It stopped at SciPy: no matching distribution exists on the configured PyPI/Chaquopy indexes for this Android target. APK compilation did not start.
- Removed SciPy from the mandatory Android pip install only for the next isolated Biopython/NumPy feasibility build. Updated the runtime probe to test SciPy if present and explicitly report it unavailable if absent; an ABI/import error is not swallowed. SciPy remains a required architecture candidate and unresolved R1 item, not silently dropped.
- Added SciPy to the third-party register with BSD-3-Clause upstream licensing noted as a candidate; exact version, Android packaging and redistribution review remain open.
- R1 remains in progress. No APK/AAB, app runtime, emulator, physical-device, 16 KB or performance result is claimed.


### R1 Gradle build attempt after SciPy isolation — 2026-11-07
- CI run 1451 passed the Python foundation job.
- The Android job successfully built the pinned Biopython 1.88 arm64 wheel, installed it from local find-links, and resolved/installed NumPy 1.26.2 plus Chaquopy OpenBLAS/libcxx/libgfortran runtime wheels. SciPy was the only package-resolution blocker and is now kept as a separate unresolved R1 candidate rather than blocking the Biopython/NumPy APK probe.
- Gradle progressed through Python source packaging, proxy generation, resource processing and stopped at Kotlin compilation due to Java target 1.8 vs Kotlin target 17 mismatch.
- Updated app Gradle configuration to set Java source/target compatibility and Kotlin compiler JVM target to 17. Rerun required. No APK/AAB, zipalign, ELF, runtime or device result is yet available.


## 2026-11-07 — Session 15: R1 arm64 build and static 16 KB package evidence
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Complete the first successful Android arm64 packaging experiment and inspect the actual APK/AAB native ELF payloads.

### Done
- Fixed the Java/Kotlin JVM target mismatch by setting both toolchains to Java 17.
- CI run 1454 succeeded on commit `87a5b6f0fcae54de6858bc32d7472379ba09ccc7`: Python foundations and Android arm64 build jobs both green.
- Built and uploaded arm64 debug APK (65,388,299 bytes) and AAB (37,573,255 bytes).
- APK ZIP alignment check passed with `zipalign -c -P 16 -v 4`.
- Downloaded and independently inspected both build artifacts. All 22 native shared libraries in each archive were ELF64 little-endian AArch64; every PT_LOAD segment had 16 KB alignment (`p_align=0x4000`).
- Recorded APK SHA-256 `a6cd53256acfa8d408ef3fddbf8da37c98367f9dbcd082fe9c68ebcb4d53152b`, AAB SHA-256 `def0e546c518f721d839b2c4238df1a95bca75db269ca3206645e3a8c0b46dda`, and workflow artifact digest in `docs/android-feasibility.md`.
- Added a repeatable CI ELF alignment checker and extended the app probe to exercise Bio.PDB parsing alongside SeqIO and NumPy; the latter is packaged but has not run on Android.

### Validated
- Workflow: https://github.com/AssayFlux/Kinetics/actions/runs/42383161737
- Python foundation job passed Ruff, mypy, registry validation, reproduction stub and 11 unit tests.
- Android arm64 Gradle APK/AAB build, Biopython/NumPy installation, ZIP alignment and artifact upload passed.
- Static ELF inspection passed for all native libraries in APK and AAB.

### Not done / blockers
- No Android emulator or physical arm64 device runtime test; no claim that Python/Biopython/NumPy imports or app startup work on-device.
- No 16 KB emulator/device runtime test.
- SciPy Android packaging remains unresolved.
- Rust FFI, C++ JNI, actual scientific engine, RDKit/alternative, offline viewer, SAF/background/cancellation, cold-start and peak RSS remain open.
- Biopython file-level license audit and distribution approval remain open.
- R1 exit gate is not met; R2 must remain gated.

### Next step
Run the expanded Python/Biopython probe on an arm64 Android device/emulator; continue remaining R1 experiments and record owner go/no-go only after the complete evidence matrix.


## 2026-11-07 — Session 16: Expand R1 native and scientific-engine probes
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Extend the arm64 feasibility app beyond packaging into native-language and real algorithm probes.

### Done
- Added a minimal Rust static library under android/native-rust exporting a C ABI numeric function.
- Added C++17 JNI shared-library source and Kotlin bridge (NativeProbe); the app screen now calls both Rust and C++ functions with the expected 3² + 4² = 25 result.
- Wired CMake/NDK into the Android Gradle build and added CI steps to cross-compile Rust for aarch64-linux-android before the arm64 APK build.
- Added Bio.PDB structure parsing and Bio.Align.PairwiseAligner global-alignment test vector to the Python runtime probe. The known vector ACGT vs ACCT with match=2, mismatch=-1, gap-open=-5 and gap-extension=-1 yields score 5.0 on the host Biopython test.
- Evaluated Parasail v2.6.2 as a possible standalone sequence-alignment engine. Its upstream Battelle BSD-style license has source/binary notice retention and citation obligations plus restrictions on Battelle name use; recorded it as an unapproved evaluation candidate in docs/third-party.md.

### Pending validation
- CI run for the integrated Rust/C++/Python probe and native ELF gate must complete successfully.
- No on-device invocation or emulator/physical-device result exists yet.
- Parasail has not been cross-built or adopted. Biopython PairwiseAligner is a real algorithm smoke test but does not replace the separate engine/RDKit evaluation required by the phase plan.

### Remaining R1 blockers
- SciPy Android packaging or a documented and owner-approved compute boundary.
- Rust/C++ native runtime and 16 KB-device verification.
- One domain-appropriate scientific engine decision and measured Android test.
- RDKit or alternative assessment; offline molecular viewer.
- SAF import, background execution, cancellation, cold-start and peak RSS.
- Physical arm64 test devices covering the approved low/mid/flagship tiers.
- Biopython file-level license audit and all dependency redistribution reviews.

### Gate
R1 remains IN PROGRESS. No R1 go/no-go has been issued and R2 remains blocked.


## 2026-11-07 — Session 17: R1 Rust/C++ arm64 build and ELF validation passed
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Validate that the Rust and C++17 native prototypes build, link and satisfy static 16 KB ELF alignment checks in the packaged arm64 artifacts.

### Validated
- CI run 1471: https://github.com/AssayFlux/Kinetics/actions/runs/42384355517 — both jobs succeeded on commit 2683a4f2212f3337593a1ac0ff0d59cc4105f986.
- Rust static library cross-compilation for aarch64-linux-android passed.
- Gradle/CMake compiled and linked the C++17 JNI shared library with the Rust static library.
- Packaged libkinetics_native.so exports both Kotlin JNI entry points and kinetics_rust_sum_squares.
- APK: 65,405,092 bytes; SHA-256 fca08d6ba9b0b0cecb63f93d9f6c0cdeb7d115253cb80a227fd009ea57cabf09.
- AAB: 37,577,400 bytes; SHA-256 1c27e74a9501e32c2381ca387f4de88c2a2373d7da38efd28ca59ed563db1509.
- Workflow artifact archive: 75,471,020 bytes; digest sha256:38f0f76879623d2a243c69dbce0208d9fb2fe646c4370ca2936adef6786e6143.
- Both APK and AAB contain 23 native ELF libraries; all are ELF64 little-endian AArch64 with every PT_LOAD segment aligned to at least 16 KB. The CI checker and zipalign check passed.

### Not done / blockers
- Native Rust/C++ JNI calls have not yet been executed on an Android emulator or physical device.
- The Python/Biopython/NumPy/PairwiseAligner/PDB runtime probe has not yet been executed on Android.
- No 16 KB page-size emulator/device runtime test, physical-device matrix, cold-start or peak-memory measurement.
- SciPy, independent scientific engine, RDKit/alternative, offline viewer, SAF/background/cancellation and license audit remain open.
- R1 exit gate remains unmet; R2 remains blocked.


## 2026-11-07 — Session 18: Prepare physical-device validation handoff
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Make the remaining owner-device tests reproducible and collectable without overstating CI evidence.

### Done
- Added KineticsR1 Logcat output for native JNI and Python runtime reports, including stack traces on failure.
- Added a device runbook to docs/android-feasibility.md with install/launch commands, model/API/ABI/page-size capture, logcat and memory commands, expected test outputs, and five-repeat measurement guidance.
- Recorded that 4 KB Android devices validate the baseline only; a 16 KB runtime test remains separately required.

### Blocked pending device access
- No Android phone has been connected to ADB in this environment. The APK is build-validated but not device-runtime validated.
- Owner needs to connect a representative Android 10+ arm64 device and provide its model/SoC/RAM/API/page-size and run logs. A separate 16 KB emulator/device test is also required.


## 2026-11-08 — Session 19: R1 integrated arm64 build evidence rechecked
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Reconcile the current CI result and maintain an accurate phase gate before further runtime experiments.

### Validated
- Inspected the latest workflow run 1481: https://github.com/AssayFlux/Kinetics/actions/runs/42384785011, commit `a7c3fd885f408bfcd46d487d58f96358129b03b2`.
- Both Python foundation and Android arm64 jobs passed.
- Android CI passed Rust arm64 cross-compilation, Chaquopy 17.2.0 preparation, Biopython 1.88 custom arm64 wheel build, APK/AAB packaging, APK ZIP alignment, static ELF alignment and artifact upload.
- APK: 63 MiB; AAB: 36 MiB. Artifact ID 13579510157; uploaded artifact digest `sha256:1c545a16edbea1453652d7c7321af4610764ad897ec39f04fdf5b66908db45fc`.
- Static ELF checker reports 16,384-byte minimum PT_LOAD alignment for every inspected native library in APK and AAB. This is static package evidence only.
- Updated docs/android-feasibility.md to record run 1481 and explicitly distinguish static build validation from runtime/device validation.

### Not validated / still open
- No Android emulator has been booted by CI and no APK runtime smoke test has run.
- No arm64 physical phone is connected; the owner has not yet supplied the previously requested exact model. Physical-device launch/runtime, low/mid/flagship coverage, cold-start and peak RSS remain blocked.
- Python/Biopython/NumPy and Rust/C++ JNI calls are compiled/packaged but not yet confirmed executing on Android.
- No 16 KB kernel runtime test; ZIP/ELF alignment is not a substitute.
- SciPy packaging, independent domain engine, RDKit/alternative, offline molecular viewer, SAF/background/cancellation, and dependency license/redistribution review remain open.

### Phase gate
- R1 remains IN PROGRESS; no R1 go/no-go is recorded.
- Owner authorization D-008 permits execution of R1, R2 and R3 sequentially, but does not waive the R1 exit gate. R2 remains not started until complete R1 evidence and explicit R1 go/no-go approval. R3 remains dependent on R2 exit evidence and approval.
- No patient data or clinical feature work is authorized; P0 remains blocked.

### Next action
- Continue R1 runtime validation using a 16 KB Android emulator and collect physical-device identity/logs from the owner. Resolve or explicitly scope the remaining scientific/runtime and licensing items before requesting R1 go/no-go.


## 2026-11-08 — Session 20: Owner-directed local Android build workflow and R1–R3 plans
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Apply the owner's instruction to keep APK builds and Android runtime testing out of GitHub Actions, while preparing gated R1–R3 execution plans.

### Done
- Owner explicitly directed: do not build APKs in GitHub Actions and do not run GitHub-hosted Android testing; build locally first and defer device testing.
- Removed the Android arm64 APK/AAB build and Android emulator job from `.github/workflows/ci.yml`. Host-side Python, registry, lint, type and unit-test checks remain.
- Rewrote the R1 phase plan to distinguish historical CI build evidence from the required future local build and owner-device evidence.
- Added detailed, explicitly gated R2 and R3 phase plans. These are plans only; neither phase has started.
- Corrected the third-party register's malformed literal newline separators.
- Updated ROADMAP to reflect the local-build route and explicit R1/R2/R3 gates.

### Evidence and validation boundary
- Historical CI runs 1471 and 1481 remain recorded as successful cross-build/static-package evidence. No fresh local APK build is claimed.
- The previously running Android emulator job is no longer part of the workflow and may have been cancelled by the workflow change; no emulator pass is claimed.
- Python host-side CI is retained. Its next result must be checked after these documentation/workflow commits.
- No Android runtime, physical-device, SciPy, standalone scientific engine, RDKit/alternative, offline viewer or performance pass is claimed.

### Not done / blockers
- R1 remains in progress; local APK build and remaining feasibility evidence are outstanding.
- R2 remains not started until the R1 evidence matrix and explicit owner go/no-go are complete.
- R3 remains not started until R2 exit evidence and approval.
- Canonical Apache-2.0 LICENSE grant file remains outstanding.
- No patient-data or clinical work is authorized; P0 remains blocked.

### Next step
Continue R1 source-side feasibility work and prepare a reproducible local build route. Keep GitHub Actions free of APK/AAB build and Android runtime test jobs. Stop at the R1 owner go/no-go before starting R2.


## 2026-11-08 — Session 21: Local Android build handoff and license file completion
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Make the owner-directed local build reproducible and close the previously approved project-license file task.

### Done
- Added `scripts/build_android_local.sh`, a local-only Linux/WSL2 arm64 debug APK/AAB build procedure using the pinned Rust, Chaquopy, Biopython and NumPy feasibility inputs.
- Added `docs/local-android-build.md` with prerequisites, commands, expected outputs and explicit static-build/runtime evidence boundaries.
- Added a host-side `bash -n` check for the local build script; this does not build an APK or run Android.
- Added the canonical Apache License 2.0 text to the root `LICENSE`, following owner decision D-001 and the Apache Software Foundation's official license text.
- Updated README, DECISIONS, ROADMAP and third-party register to reflect the Apache-2.0 grant file and local Android build workflow.
- Corrected the malformed literal newline sequences in the third-party candidate table.

### Validation boundary
- GitHub Actions remains source-validation-only. Latest workflow run is pending at the time of this log entry; record its final outcome separately.
- The local build script has not been executed on the owner's machine. No fresh local APK/AAB, runtime or device pass is claimed.
- Historical run 1471/1481 build evidence remains static and historical only.

### Remaining gates
- R1 remains IN PROGRESS; SciPy, real scientific engine, RDKit/alternative, offline viewer, app runtime, SAF/lifecycle, performance and local APK build evidence remain open.
- R2 and R3 remain NOT STARTED; their plans are prepared but their predecessor gates have not passed.
- P0 remains blocked; no patient data or clinical features are authorized.


## 2026-11-08 — Session 22: Host-only CI verification after workflow change
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Verify the source-only CI workflow after removing GitHub-hosted Android builds and tests.

### Validated
- Workflow run 42428857132 on commit `aeaeee1b2f8075ce944cf1092f3d0d14c676aa70` completed successfully: https://github.com/AssayFlux/Kinetics/actions/runs/42428857132
- Ruff passed; mypy passed with no issues in 7 source files; registry validation passed; all 11 unit tests passed.
- Reproduction stub ran and correctly reported no registered evidence jobs.
- The local Android build script passed `bash -n` syntax validation.
- No APK/AAB build or Android emulator/runtime test ran in GitHub Actions.

### Remaining status
- R1 remains IN PROGRESS; the local build and remaining Android/scientific feasibility evidence are not yet available.
- R2 and R3 remain NOT STARTED pending predecessor gates.


## 2026-11-08 — Session 23: Final source-only CI rerun
**Phase:** Track R / R1 Android feasibility (in progress)  
**Objective:** Verify the final Android artifact-gate wording and local build-script prerequisite corrections.

### Validated
- Workflow run 42428935274 completed successfully on commit `6580e4b254aafa09da4543b490b7af4b457d9637`: https://github.com/AssayFlux/Kinetics/actions/runs/42428935274
- Pre-commit configuration, Ruff, mypy, registry validation, all 11 unit tests, reproduction stub, local-only Android artifact gate and `bash -n scripts/build_android_local.sh` passed.
- This run did not build APK/AAB files and did not run Android emulators or devices.

### Gate
R1 remains IN PROGRESS. Host-side source CI success does not close Android build/runtime/scientific feasibility criteria. R2/R3 remain gated and not started.


## 2026-11-08 — Session 14: Research platform R1–R10 execution mandate
**Phase:** Track R / R1 (in progress; R2–R10 remain dependency-gated)  
**Objective:** Begin a careful, evidence-led execution pass across the Research Platform track without weakening owner-approved phase gates.

### Owner instruction
- Owner instructed: complete Research Platform R1 through R10 carefully; no shortcuts or unsupported completion claims.
- Existing build policy remains: no APK/AAB builds or Android emulator tests in GitHub Actions; local build first, physical-device testing deferred by owner.
- Existing sequential phase gates remain binding. R2 requires R1 evidence and explicit go/no-go; R3 requires R2 exit approval; later work packages retain their listed dependencies and governance gates.

### Repository audit and corrections
- Re-read ROADMAP, NORTH_STAR, DECISIONS, R1/R2/R3 plans, local Android build guide, third-party register and Android feasibility record.
- Confirmed R1 is still incomplete; R2/R3 are planned but not started.
- Corrected ROADMAP's stale statement that the Apache-2.0 LICENSE file remained to be added.
- Corrected ROADMAP R10 wording so it does not imply GitHub Actions APK builds, which the owner explicitly prohibited.
- Corrected stale Android feasibility chronology that incorrectly said no APK/AAB had ever been produced after historical CI runs 1471/1481.

### Commits
- `4f3a86a4bfc2587e7fb815a1a3fd29111538e503` — reconcile Research Platform roadmap and release-channel/build policy.
- `eb587564a0e921e6184ac1d2180c1b1f9bbb0b35` — reconcile Android feasibility chronology and local-only build policy.

### Validation and limitations
- Documentation edits only; no application source changes or new tests were performed in this session.
- No fresh local APK/AAB build, Android runtime/device test, scientific validation or R1 go/no-go is claimed.
- R1's documented technical and owner-device blockers remain open. R2–R10 are not marked complete or started ahead of their dependency gates.

### Next work
- Perform a source-level R1 audit of Android Gradle configuration, Python probe, Rust FFI, C++ JNI, native alignment checker and local build script; fix verified defects and add host-side tests where possible.
- Continue engine, offline viewer, lifecycle, security and licensing investigations with pinned evidence.
- Update phase and roadmap status only when each exit criterion has supporting evidence.


## Session 15 — R1 source audit and ELF checker hardening (2026-11-08)

### Owner instruction
- Owner approved continuation and reiterated the requirement to complete Research Platform R1–R10 carefully, without unsupported completion claims.
- Continue in dependency order. R1 remains the active phase; R2 and R3 remain gated by their documented exit criteria and owner reviews. R4–R10 remain downstream roadmap packages.
- Preserve the owner directive: no APK/AAB builds or Android emulator/device tests in GitHub Actions; local APK build and physical-device testing remain owner-controlled.

### Work completed
- Audited the R1 Android project layout, Gradle configuration, Kotlin probes, Python runtime probe, Rust FFI, C++ JNI and ELF checker.
- Found that the prior ELF checker only compared minimum PT_LOAD p_align with 16 KB. It did not verify ELF program-header bounds/entry sizes, alignment power-of-two, or p_offset/p_vaddr congruence.
- Hardened scripts/check_android_elf_alignment.py to validate ELF64 little-endian version 1, AArch64, program-header table bounds and sizes, PT_LOAD presence, each load segment's 16 KB minimum alignment, power-of-two alignment and p_offset/p_vaddr congruence.
- Added tests/test_android_elf_alignment.py with synthetic valid and invalid ELF fixtures.
- Corrected escaped byte literals after the first CI test run exposed the fixture-signature error. The failed run is retained as a test-driven correction, not hidden.

### Verification
- Host-only CI run 42429935581 passed on commit e1560a3f74165a770438000a650a83019a01432d.
- Ruff passed; mypy passed with 8 source files; registry validation passed; all 15 unit tests passed; reproduction stub, local Android build-script syntax check and owner-directed Android artifact gate passed.
- No APK/AAB was built, no emulator/device test was run, and no Android runtime result is claimed.

### Remaining R1 blockers
- Owner local build and build-log/artifact evidence.
- Android runtime execution of Python/Biopython/NumPy and Rust/C++ JNI probes.
- SciPy architecture decision/experiment; separate scientific engine evaluation; RDKit/alternative; offline structure viewer.
- SAF import, background execution, cancellation/resume, cold-start and peak-memory evidence.
- Complete dependency/source-file license audit and explicit owner R1 go/no-go.


## Session 16 — Integrated R1–R10 implementation delivery (2026-11-08)

### Owner direction
- Owner corrected the execution approach: implement Research Platform R1–R10 as one integrated delivery; prepare the first local Android build before the later testing campaign.
- Do not stop at R1 or R2 to ask permission to start downstream implementation.
- GitHub Actions must not build APK/AAB or run Android emulator/device tests. The first Android build is local. Later testing is a separate owner-directed stage.
- This changes implementation sequencing, not scientific validation, licensing, clinical, privacy, security or release exit criteria.

### Source implementation added
- Python research package now includes sequence/FASTA/FASTQ parsing, statistics, reverse complement, transcription, k-mers and global alignment; protein composition/mass/hydropathy/pI estimate; Michaelis–Menten and inhibition models plus exploratory log-grid fitting; PDB coordinate parsing, contacts and unaligned RMSD; SDF V2000 parsing and exploratory graph fingerprints/Tanimoto; Newick parsing and patristic distances; SAM/VCF text parsing and FASTQ quality summary; CPM/CLR, correlation, fold change and Shannon/Simpson diversity.
- Added streaming NCBI Gene gene_info ingestion with taxon, GeneID, symbols, synonyms, source and release provenance. Catalogue imports cannot confer validated status.
- Configured the Python package layout and public exports.
- Capability registry now lists initial source-implemented tools with evidence_level=none; no tool is marked validated/device-verified.
- Android shell now provides Research Mode, SAF document import, SQLite job/provenance metadata, WorkManager background streaming/hash import, cancellation and resumable partial-file checkpoints.
- Added Android Keystore AES-256-GCM helper and a data-only pack manager with manifest/source/license/size/SHA-256 checks.
- Added R10 release-hardening checklist and integrated R1–R10 implementation inventory; updated roadmap and R2/R3 plans to reflect the owner's integrated-delivery instruction.

### Explicitly not claimed
- No tests were intentionally run in this implementation pass and no APK/AAB was built. GitHub source CI may be triggered by repository pushes; no Android build/device job was added.
- Android compile/runtime behavior, local APK build, native FFI/JNI execution, 16 KB runtime support, dependency redistribution, scientific concordance, memory/performance, security review and release readiness remain unverified.
- Remaining substantial code scope includes BAM/CRAM, robust VCF normalization, mmCIF and advanced structure metrics, production chemistry/SMILES/stereochemistry, broader phylogenetic inference/search, differential-expression inference, multi-omics workflows, broad gene-domain annotations/data-pack rollout and full R10 accessibility/performance/crash/security/release automation.
- R1–R10 are in progress, not complete. The implementation inventory is documented at docs/research-platform-implementation.md and release requirements at docs/release-hardening.md.


### Continued integrated implementation
- Added Android Keystore AES-256-GCM helper, data-pack manifest/checksum/size/license validation, and hardened pack ID/version path handling.
- Extended SAF import worker with partial-file checkpointing, resumable continuation, SHA-256 continuity, 512 MiB cap, and cancel/resume controls in the app shell.
- Added SAM/VCF text parsing, FASTQ quality summaries, NCBI Gene catalogue ingestion, primer screening, SpCas9 NGG PAM scanning, UPGMA clustering, logistic growth and cross-omics correlation.
- Added an R10 release-hardening checklist and refreshed the integrated implementation inventory.
- These additions are source implementation only; no test/build/Android runtime result is claimed.


## Session 17 — Moto G54 5G target recorded; Android build-source defect corrected (2026-11-08)

### Owner input
- Owner supplied Motorola Moto G54 5G as the available physical test handset.
- Recorded it as the first planned R1 physical-device target in `docs/android-feasibility.md` and `docs/phase-r1-plan.md`. Exact device properties must be collected from the connected phone; no model-spec assumptions or compatibility claim are made.
- Build-first / test-later remains the active owner directive. GitHub Actions remains host-source-validation only; APK/AAB build and device tests are local and later.

### Source audit correction
- Audited `android/app/build.gradle.kts` and found a literal escaped newline joining the WorkManager dependency and JUnit test dependency, which makes the Kotlin DSL source malformed.
- Corrected the declaration into two actual Gradle lines in commit `1cce915dc8386e0ca7d819b896edba2a73bb4127`.
- This is a source-level correction only. No Gradle build or APK/AAB build was run here, so the correction is not yet build-verified.

### Current phase state
- R1 remains in progress: local build and later Moto G54 5G runtime evidence remain outstanding; SciPy, domain scientific engine, RDKit/alternative, offline molecular viewer, lifecycle/SAF and licensing questions remain open.
- R2/R3 source implementation is underway as part of the owner-authorized integrated R1–R10 delivery; their integration tests, device verification and exit approvals remain incomplete.
- No clinical/patient workflows are enabled. No phase is marked complete by this session.


## Session 18 — R2 import durability and R3 regression baseline (2026-11-08)

### R2 source hardening
- Changed resumable import staging from cache storage to app-private `noBackupFilesDir/research-imports`, so Android cache eviction does not silently destroy a checkpoint and imported material is excluded from normal app backup.
- Resume now re-reads and hashes the source prefix and compares it with the retained partial file before appending. If the source changed, the stale partial is discarded and the user must restart the import rather than receiving a hash for a mixed-version file.
- WorkManager import now rejects unsafe job IDs and reports durable checkpoint state. MainActivity now requires a persistable SAF read grant before enqueueing background/resumable work; it no longer silently ignores a missing grant.
- Enabled SQLite foreign-key enforcement for job/provenance references.
- These are source changes only; Android compilation, WorkManager process-death behavior and device runtime remain unverified.

### R3 regression coverage
- Added `tests/test_research_primitives.py` covering FASTA/FASTQ parsing and malformed records, IUPAC reverse complement/transcription, sequence statistics and k-mer counts, Needleman–Wunsch output consistency/memory cap, peptide mass/pI/unsupported residues, Michaelis–Menten and four inhibition rate equations, and synthetic parameter-region recovery for the log-grid fit.
- Tests are regression/unit tests only. They do not constitute independent scientific validation, reference concordance, statistical uncertainty analysis or device performance evidence.
- The first test runs exposed three incorrect test expectations (k-mer window count, peptide mass threshold and error-message match); each was corrected against the current algorithm output. No underlying algorithm change was made for those expectation mismatches.
- The attempt to lint the entire scientific package surfaced 90 existing style violations across the package; broad automated rewriting was not applied. CI retains Ruff/mypy checks on scripts and tests; scientific package formatting/type cleanup remains an explicit debt item. The test module marks the currently untyped research package import as ignored for mypy.

### Host validation
- Host-only CI run 1594 passed on commit `71bb2474dec3f94f3868d5ac9ad4cf441fc25f1b`: pre-commit config, editable package install, Ruff for scripts/tests, mypy for scripts/tests, registry check, all 28 tests, reproduction stub, owner-directed local Android artifact gate and local build-script shell syntax.
- CI run: https://github.com/AssayFlux/Kinetics/actions/runs/42431967869
- No APK/AAB build, Android runtime, emulator, Moto G54 5G, scientific engine, SciPy, RDKit or viewer test was run.

### Phase status
- R1 remains IN PROGRESS. Local APK build and later owner device campaign remain outstanding; Moto G54 5G is the selected first handset, not a verified device.
- R2 remains implementation in progress; required integration tests, migration/recovery, encryption-at-rest integration, provenance export and real-device workflow remain incomplete.
- R3 remains implementation in progress; independent reference validation, confidence intervals/residual diagnostics, units/model identifiability, validation records and device benchmarks remain incomplete.
- No R1/R2/R3 phase is marked complete; no clinical/patient capability is enabled.


## Session 19 — integrated R1–R10 implementation increment (2026-11-08)

### Owner direction followed
- Continued implementation directly on `main`; no branch was created.
- Kept GitHub Actions from automatically running checks on pushes or pull requests. The existing host validation workflow is now manual-dispatch only. No APK/AAB or Android emulator/device job was added.
- No tests were run and no APK/AAB was built in this session, in accordance with build-first / test-later.

### Source changes committed
- **R1:** pinned Android NDK 28.2.13676358 in Gradle to match the local build script; added an in-app manual probe for embedded Python/Biopython/NumPy/SciPy reporting and C++ JNI/Rust FFI smoke calls. This is a probe path, not evidence that the Android runtime has passed.
- **R2:** upgraded SQLite schema to v2 with a migration and transactional final import/provenance update. SAF imports are staged as independently authenticated AES-256-GCM chunks using an Android Keystore key, including resumable source-prefix verification and recovery from an incomplete final record. Final imported data remains encrypted in app-private no-backup storage. Added a chunked decrypt-to-temporary-file helper and removed legacy plaintext staging before new imports. Export/analysis integration, key-loss recovery, migration tests and device verification remain open.
- **R3:** added finite-value guards, residual mean/sample dispersion, R-squared and assumption-qualified Gaussian least-squares AIC/BIC to the exploratory Michaelis–Menten fit. Added warned Lineweaver–Burk, Eadie–Hofstee and Hanes–Woolf coordinate transforms. Confidence intervals, identifiability and independent reference validation remain open.
- **R4:** strengthened SAM mandatory-field, CIGAR, sequence/quality and optional-tag validation; strengthened VCF header, column-count, position and QUAL validation.
- **R5:** added a Horn-quaternion rigid-body RMSD superposition path and finite-coordinate checks. mmCIF and advanced structure metrics remain open.
- **R6:** strengthened SDF V2000 atom/bond parsing; added graph descriptors, bounded exact element/bond-order substructure matching, and hard limits for path-fingerprint traversal/features. Production stereochemistry/aromaticity/tautomer handling and an approved chemistry engine remain open.
- **R7:** added quoted Newick labels, finite/non-negative branch-length checks and finite UPGMA distance validation.
- **R8:** added finite-value validation throughout exploratory omics primitives and made Simpson diversity explicitly Gini–Simpson (1 - sum of squared relative abundances). Differential-expression inference and broader multi-omics remain open.
- **R9:** expanded NCBI Gene ingestion to all 16 gene_info columns and added streaming from plain or gzip-compressed files. This is a broad expandable catalogue import, not a claim of exhaustive domain annotation or a validated PGx panel.
- **R10:** registry checks now require implementation paths to exist inside the repository; periodic one-second UI polling was replaced with WorkManager LiveData observation. Full accessibility, performance, crash, threat-model, licensing and release hardening remain open.
- Updated the integrated implementation inventory and roadmap to reflect these source changes without marking any phase complete.

### Verification state
- All changes above are source commits only. No tests, lint, type checks, Gradle build, APK/AAB build, Android runtime probe, Moto G54 5G install, scientific reference comparison or device benchmark was run.
- The previous 28-test host result remains the historical baseline for the earlier source revision only; it does not verify these new commits.
- R1–R10 remain in progress. The remaining scope includes Android build/runtime evidence, full export and recovery integration, BAM/CRAM, VCF normalization, mmCIF/advanced structure metrics, production chemistry and approved engines, broader phylogenetic inference/search/viewers, statistically sound differential expression, PGx allele/diplotype implementation and data packs, and full R10 release hardening.
- Clinical mode remains disabled; no patient workflow or patient data is enabled.


### R4 continuation — wrapped FASTQ and terminal quality trimming
- FASTQ parser now accepts wrapped sequence and quality lines, validates separator identifiers and exact total quality length, and rejects invalid quality characters.
- Added explicit terminal low-quality trimming with Phred-offset validation, minimum-length rejection and limitations (no adapter or sliding-window trimming).
- Added regression cases to the source tree; they were not executed under the test-later instruction.

- R2 follow-up: AES-GCM chunk AAD now binds every chunk to its job ID and ordinal, preventing cross-job substitution/reordering; authenticated materialization verifies the recorded whole-file SHA-256 before publishing a temporary plaintext file. The chunk format is versioned separately. This remains uncompiled and untested.


### R5, R8 and R9 continuation
- **R5:** added an mmCIF `_atom_site` loop parser that maps coordinate records into the shared atom model, handles label/auth identifier fallbacks and alternate locations, and rejects incomplete/non-finite coordinate rows. It is not a full mmCIF dictionary, symmetry or biological-assembly implementation.
- **R8:** added two-group Welch unequal-variance tests for pre-normalized/log-scale feature matrices, Student-t two-sided p-values, and Benjamini–Hochberg q-values across the supplied feature family. The API rejects malformed sample designs and duplicate feature IDs. It does not model raw-count distributions, covariates, batches, paired/repeated measures or study design; results remain exploratory.
- **R9:** added bounded provenance-preserving catalogue search over GeneID, official symbol, synonyms, descriptions, nomenclature and cross-references, with optional taxonomy filtering. It does not supply PGx star alleles, haplotypes, diplotypes or clinical recommendations.
- Added regression-test source for the new R5/R8/R9 paths; tests remain deliberately unexecuted during this build-first pass.
- Updated the integrated implementation inventory and roadmap. R1–R10 remain in progress; source additions are not validation or device support evidence.


### R2, R6 and R7 continuation; R1 probe improvement
- **R2:** decrypted analysis materialization is now restricted to the app-private cache. Added a callback helper which removes the temporary plaintext file in a `finally` block. This narrows accidental plaintext exposure; crash/power-loss cleanup and a complete SAF export pipeline still need implementation and verification.
- **R6:** added a multi-record SDF V2000 iterator which reports record-number context on malformed records. This does not add stereochemical or production chemistry semantics.
- **R7:** added neighbour-joining distance-tree inference. It validates the matrix and rejects negative inferred limbs rather than silently clipping or changing branch lengths.
- **R1/R2:** extended the manual on-device runtime probe to check Android Keystore AES-GCM round-trip and rejection of mismatched authenticated metadata, in addition to the existing embedded-Python and C++/Rust smoke probes.
- Added source-level regression cases and updated the implementation inventory/roadmap. No tests or Android build/runtime commands were run in this pass.


### R4–R10 controlled delivery plans
- Added individual phase plans for R4 genomics, R5 structural biology, R6 computational chemistry, R7 phylogenetics, R8 omics, R9 gene catalogue/PGx foundations and R10 hardening.
- Each plan distinguishes source implementation from scientific validation and device verification, records current limitations, and defines evidence-based exit criteria. R9 explicitly retains the P0/adviser gate; R10 records local-only APK/AAB and device verification.


### R2 decryption resource boundary
- Decryption now rejects empty authenticated chunks and caps materialized plaintext at the same 512 MiB limit as import, before writing beyond the cap.
- The helper checks the output channel's current position before each plaintext write. This is source-only and has not been exercised on Android.


### R9 large-catalogue search memory bound
- Gene catalogue search now retains at most the requested result limit in exact and partial result buckets rather than accumulating every partial match from a full streamed NCBI catalogue. This avoids turning a streaming import into an unbounded search-result memory allocation.
- No tests were run; all new tests remain queued for the later validation phase.


### R10 accessibility increment
- Added Compose semantics descriptions for the research workbench heading, Research Mode notice and merged research-job/state summaries. This improves screen-reader context but is not a full WCAG/accessibility audit.
- R10 remains in progress; no device accessibility test was run.


### R2 encrypted-container format versioning
- Added an explicit `KDAT` magic plus format-version byte to the encrypted container. Import resume validates the header and resets incompatible legacy/torn staging data before re-reading the source; finalized-file materialization rejects unknown formats.
- Chunk ordinal and job ID remain authenticated as AES-GCM AAD. The metadata now identifies the corresponding chunked-v2 format unambiguously.
- This is not a migration path for previously finalized v1 encrypted imports; those require an explicit recovery/migration design. No Android build or test was run.


### R1/R2 versioned-container runtime probe
- Extended the manual Android runtime probe to create a KDAT v2 encrypted file, append an authenticated chunk, decrypt it through the production reader, verify SHA-256 and byte-for-byte output, and remove the temporary probe files.
- This is a future on-device check only; the probe has not been built or executed.


## Session 20 — integrated R2/R4 source hardening (2026-11-08)

### R2
- Added startup cleanup for stale plaintext analysis-cache files: only the app's uniquely-prefixed files older than 24 hours are eligible. Normal callback cleanup remains in place.
- Empty imported files are rejected rather than recorded as successful research inputs.
- Hardened data-pack installation against direct-constructor manifest bypass and dot-segment path values. The installer hashes the exact bytes copied to its temporary file, verifies the declared size and SHA-256 before finalization, uses a unique temporary file and refuses to replace an installed version.
- These are source changes only. Filesystem atomicity, cross-instance concurrency, process-death recovery, Android compilation and device execution remain unverified.

### R4
- Added `iter_fasta_records`, a lazy iterator over FASTA line iterables, while retaining `parse_fasta` as a convenience materializer.
- Added `normalize_small_variant` for reference-checked minimal/left normalization of biallelic literal A/C/G/T small variants. Symbolic alleles, breakends, multiallelic decomposition and interpretation remain explicitly unsupported.
- Exported both APIs, added regression-test source, updated the capability registry and phase documentation.
- No tests or Android build were run. R4 remains in progress pending tests, reference concordance, BAM/CRAM and large-file/device evidence.


### R1 embedded-package integration follow-up (2026-11-08)
- Corrected the Chaquopy source-set configuration to use its documented `chaquopy.sourceSets` DSL and include the repository `python/` directory. The Android app will therefore package the actual `kinetics` modules rather than only the isolated probe module.
- Extended the future on-device Python probe to import `kinetics`, run FASTA parsing and exercise the reference-checked variant normalizer.
- Updated the static Android config guard and R1 documentation. This was a source-level integration correction; no Gradle build or Android runtime probe was executed. Chaquopy 17.2 documentation specifies `chaquopy.sourceSets` for additional Python source directories. <https://chaquo.com/chaquopy/doc/current/android.html>


### R3 uncertainty increment
- Added a seeded paired nonparametric bootstrap helper for Michaelis–Menten parameter percentile intervals, with fixed search bounds and explicit assumptions/limitations. Added the helper to the public package exports and capability registry, plus a deterministic regression-test case.
- No tests were executed. The intervals are exploratory and remain subject to reference validation, identifiability assessment and scientific review.


### R4 SAM semantics follow-up
- Corrected SAM handling so SEQ may be present while QUAL is `*`, as allowed for missing quality data; QUAL must remain `*` when SEQ is unavailable. Present QUAL values still require matching length and printable characters.
- Added CIGAR query-consuming operation validation against SEQ length, plus regression-test source for both cases. No tests were run.


### R6 V3000 source increment
- Added conservative V3000 atom/bond graph parsing with counts, unique atom/bond identifiers, coordinate finiteness, bond references and duplicate-edge validation. The existing multi-record SDF iterator now dispatches both V2000 and supported V3000 records.
- Added a basic V3000 regression fixture and updated R6 registry/plan. Stereochemistry and additional V3000 atom/bond attributes remain uninterpreted; this is not production cheminformatics. No tests were run.


### R5 approximate SASA source increment
- Added deterministic Shrake–Rupley solvent-accessible surface area using generic element van der Waals radii and Fibonacci sphere sampling, with atom-count, probe-radius and point-resolution limits.
- Exported the API, added regression-test source for single-atom area, occlusion and invalid inputs, and updated the R5 capability registry/plan. It omits hydrogens, atom-specific radii, residue-level relative accessibility and biological assemblies. No tests were run; reference concordance remains required.


### R7 Newick export increment
- Added deterministic Newick serialization with safe quoting of labels containing whitespace or delimiters, finite/non-negative branch-length validation and cycle rejection.
- Exported the API, added a quoted-label/branch-length round-trip regression case and updated the R7 capability registry/plan. No tests were run; tree inference remains distance-based and needs reference concordance/bootstrap/model-based methods.


### R2 SAF export and schema migration increment
- Added a two-pass LocalCrypto.decryptChunkedFileToStream: first pass authenticates every AES-GCM chunk and verifies recorded SHA-256 without writing plaintext; second pass authenticates again while streaming to the caller-owned output stream.
- Added ResearchStore.exportStoredInput for completed imports only and a Compose SAF CreateDocument action. Export uses the user's selected destination and does not materialize a plaintext cache file.
- Added SQLite schema version 3 migration for export metadata and a provenance timestamp index.
- No Android compilation or tests were run. SAF provider failure/partial-file behavior, migration fixtures, process death, key loss and export cancellation still need dedicated verification.


### R8 NB2 count GLM source increment
- Added an exploratory NB2 log-link GLM for raw integer counts, with size-factor normalization, per-feature moment dispersion, IRLS, numeric covariates, Wald statistics and BH correction.
- Design rank deficiencies and insufficient residual degrees of freedom are rejected. Regression-test source covers a condition effect, a balanced numeric batch covariate, fractional-count rejection and confounding rejection.
- This is not equivalent to DESeq2/edgeR: no empirical-Bayes dispersion shrinkage, small-sample calibration, repeated-measures model or robust outlier procedure. No tests or reference simulations were run.


### R4 BAM core decoder increment
- Added a lazy gzip/BGZF-compatible BAM decoder for reference dictionary and core alignment fields (query name, flags, reference, position, MAPQ, CIGAR, sequence and qualities). It bounds header/record blocks, validates record lengths, CIGAR operation codes, sequence packing, qualities and reference IDs.
- Exported the iterator and added a synthetic binary-record fixture. Auxiliary tags are skipped; CRAM is not implemented; no indexed region access or large-file benchmarks are claimed. No tests were run.


### R9 PGx definition foundation increment
- Added a provenance-gated JSON definition pack parser and typed VariantKey / StarAlleleDefinition / AlleleMatch models, with pinned source release, HTTPS source, license and genome build metadata.
- Added conservative matching for already phased, explicitly complete haplotypes only; incomplete/unphased inputs no-call and tied best definitions remain ambiguous. No phasing, CNV, structural variant, diplotype, phenotype or clinical interpretation is inferred.
- Added regression-test source and registry/docs updates. No authoritative PGx datasets were imported because licensing/release review is still required. No tests were run.


### R7 Jukes-Cantor model-distance increment
- Added Jukes-Cantor 1969 nucleotide distance with pairwise deletion, minimum-site guard and explicit saturation rejection, plus neighbour joining from aligned DNA sequences using those corrected distances.
- Exported both APIs, added regression-test source and updated capability registry/phase docs. This is model-corrected distance inference, not ML/Bayesian tree search; no rate heterogeneity, bootstrap or independent reference concordance. No tests were run.


### R5 interaction candidate increment
- Added distance-only heavy-atom screening for N...O hydrogen-bond candidates, canonical Lys/Arg–Asp/Glu salt-bridge candidates and Cys/CYX SG disulfide candidates, with explicit geometric ranges and caveats.
- Exported the API, added regression-test source and updated R5 registry/plan. Hydrogen-bond directionality, protonation, solvent, energetic scoring, alternate conformations and structural validation remain absent. No tests were run.


### R10 build reproducibility and governance increment
- Pinned Gradle 8.13 binary SHA-256 in wrapper properties and local build script; pinned Chaquopy 17.2.0 to its immutable source commit. The local script now downloads and verifies Gradle rather than relying on an arbitrary host-installed Gradle.
- Extended the Android static guard to check wrapper checksum and local build source pins. Updated dependency register with toolchain versions and explicitly noted that the NumPy wheel checksum and complete transitive dependency/license inventory remain open.

- Added initial security/privacy threat model, accessibility verification protocol and explicit NOT RELEASE READY checklist. These are plans and controls, not independent review or passed audit evidence.

- Hardened PGx pack import to require the expected release identifier and a 64-hex source checksum; VariantKey normalizes REF/ALT to uppercase and rejects non-integer positions.


### R10 SBOM source inventory increment
- Added a standard-library SPDX 2.3 generator for directly declared Android Gradle, Chaquopy Python, development Python and Rust dependencies. Unresolved/BOM-managed versions and license conclusions are marked NOASSERTION; the generator's annotation explicitly says it is not a resolved transitive release SBOM.
- Updated release checklist and documentation so the static inventory cannot be mistaken for the final release SBOM.


### R6 optional RDKit adapter increment
- Added a lazy optional RDKit backend for sanitized SMILES/molblock parsing, canonical isomeric SMILES, formula/molecular-weight/LogP/TPSA/H-bond descriptors, chiral-centre reporting, Morgan fingerprints and Tanimoto similarity.
- The adapter reports the active RDKit version and fails clearly when unavailable. It is not bundled in Android and has no product approval; exact release pin, transitive licenses, Android ABI/16 KB support and binary-size evaluation remain open. Added optional regression-test source guarded by importorskip; no tests were run.


### R4 optional HTSlib adapter increment
- Added a lazy pysam/HTSlib streaming adapter for BAM and CRAM, with indexed region reads, coordinate conversion and explicit local FASTA requirement for CRAM. No remote reference fallback is enabled.
- Exported the API, registered the optional engine, documented the license/ABI review gate and added optional BAM adapter regression-test source. pysam/HTSlib is not bundled in Android; no CRAM/HTSlib tests were run.


### R3 independent numerical reference harness
- Expanded Michaelis–Menten output with local Jacobian covariance approximations, standard errors, leverage, standardized residuals, Cook's distance, Durbin–Watson, residual sign runs, condition-number and search-bound warnings. These are descriptive approximations, not validated inferential statistics.
- Added a reproducible host validation harness comparing noise-free and seeded Gaussian-noise synthetic fits with SciPy curve_fit, recording SciPy/NumPy versions and explicit tolerances. The harness was not executed; no validation pass is claimed. Experimental reference datasets remain required.


### R2 explicit local deletion flow
- Added a user-confirmed delete action for terminal imports. It removes the finalized encrypted KDAT, encrypted partial staging, legacy plaintext staging (if present), provenance row and job row. Canonical directory checks constrain deletions to app-private research storage.
- The UI explicitly warns that exported copies cannot be recalled and flash-storage secure erasure is not guaranteed. No Android build/tests were run.


### R9 PharmVar TSV source adapter increment
- Added a release- and byte-checksum-pinned importer for PharmVar's documented nine-column TSV haplotype/variant format. It preserves the source reference accession/coordinate system, handles the REFERENCE sentinel and matches only exact complete already-phased haplotype variant sets.
- Added parser/matcher test source and exported APIs. No live bulk PharmVar dataset was downloaded or bundled; no CYP2D6 CNV/hybrid, structural variation, phasing, diplotype or phenotype translation is claimed. Current PharmVar version and license are documented with source links; terms/release must be rechecked at every import. No tests were run.

- Pinned Python host version to 3.11.17, Rust toolchain to 1.88.0 with arm64 Android target, committed Cargo.lock and changed local native build to cargo --locked. Extended static Android guard to verify the Python/Rust pins.

- Replaced Biopython's mutable PyPI source fetch with a pinned immutable Biopython 1.88 Git commit, `git archive` source export and local Chaquopy recipe path. Added commit pin to static Android config guard.

- Added the full Biopython upstream LICENSE text to Android assets and represented its custom license identifier/extracted text in SPDX; the SPDX package records the exact source commit. Static privacy guard now checks no INTERNET permission, backup disabled and cleartext disabled.


### R8 NB2 edge-case increment
- Added an explicit all-zero-feature path to the exploratory NB2 GLM. Such features are retained with p=1 for transparent multiple-testing accounting, neutral coefficient placeholders, and a clear non-estimable warning; no artificial model fit is attempted.
- Added regression-test source only. No tests or Android build were run.


## 2026-11-08 — Integrated R1–R10 completion continuation: R7 bootstrap increment
**Phase:** Track R / integrated implementation continuation
**Objective:** Close a bounded remaining R7 capability gap without misrepresenting validation or bypassing the owner’s build-first/test-later instruction.

### Done
- Added seeded nonparametric alignment-site bootstrap support for the Jukes–Cantor + neighbour-joining workflow.
- The API reports requested, successful and failed replicates; failed/saturated/invalid NJ replicates are not silently repaired and are excluded from the support denominator with explicit warnings.
- Added split extraction, deterministic seed handling, input bounds and a public package export.
- Added regression-test source for deterministic results, output bounds and invalid inputs.
- Registered the source capability as implemented with no validation evidence.
- Corrected R5 implementation documentation to reflect already-present approximate Shrake–Rupley SASA and distance-only interaction-candidate screening; secondary-structure assignment and reference validation remain open.
- Updated R7 roadmap and implementation status to include JC+NJ and the new bootstrap primitive.
- Opened draft PR #73: https://github.com/AssayFlux/Kinetics/pull/73

### Not done / validation status
- No tests, lint, type checks or scientific reference comparisons were run, in accordance with build-first/test-later.
- No APK/AAB build or Android device/emulator test was run.
- This bootstrap is distance-based exploratory support, not ML/Bayesian inference, rate heterogeneity, model selection or a validated phylogenetic pipeline.
- R1–R10 are not complete. Outstanding platform gates include local Android build/runtime evidence, end-to-end scientific dispatch integration, key-loss recovery and device verification, independent reference validation, full BAM/CRAM Android integration, full mmCIF/secondary structure, production chemistry engine and licensing, ML/Bayesian phylogenetics, calibrated count-aware inference, comprehensive versioned gene/PGx packs, and R10 security/accessibility/performance/release evidence.

### Next step
Continue integrated implementation only where correctness can be supported by source, pinned reference data and explicit licensing. Preserve unvalidated capabilities as implemented-but-unvalidated; do not claim R1–R10 complete until their exit evidence exists.


## 2026-11-08 — R2 Keystore key-loss preservation increment (direct main)
**Phase:** Track R / R2 storage recovery
**Objective:** Prevent silent key regeneration and make completed encrypted records visibly recoverable when the Android Keystore alias is definitely absent.

### Done
- Added a tri-state Android Keystore alias probe: present, definitely absent, or unavailable/unknown. An unavailable Keystore is not treated as key loss.
- On startup, definite alias absence moves completed encrypted records and retained `.encpart` partial imports into `recovery_required`; partial ciphertext is preserved and not offered for unsafe resume.
- Preserved encrypted files and provenance; no replacement key is generated and no ciphertext is deleted automatically.
- Exposed the recovery-required state in the research job list and made it ineligible for ordinary resume/export actions.
- Updated the R2 roadmap and implementation notes.

### Limits / validation status
- This is safe failure-state handling, not cryptographic recovery. If the original Android Keystore key is permanently lost, AES-GCM ciphertext cannot be decrypted; only restoring the original key/device backup can recover it.
- Partial-import key-loss recovery, orphan reconciliation, interrupted SAF export cleanup and migration fixtures remain open.
- No tests, lint, Gradle build, APK/AAB build, runtime probe or Android device/emulator validation were run, per owner instruction.

### Current gate
R2 remains in progress. The source change is committed directly to `main`; Android compilation and on-device verification are still required before calling this behavior complete.


## 2026-11-08 — Session 15: Local build host guard and SAF export cleanup
**Phase:** Track R / integrated R1–R10 implementation  
**Objective:** Prepare an honest local-build handoff and harden the SAF export failure path.

### Done
- Confirmed current `main` at `e3993decda7c433f7017dc94fc79c194b978728d` before this work.
- Added an early host check to `scripts/build_android_local.sh`. Termux/Android, non-Linux and non-x86_64 hosts now stop before toolchain downloads or cache mutation with an actionable error.
- Updated `docs/local-android-build.md`: current pinned build route requires Linux x86_64 or x86_64 WSL2; Termux on an Android/aarch64 phone is not supported as the build host. Termux may still be used after the APK exists for transfer, installation and log collection.
- Hardened the SAF export flow: use truncate mode; on export failure, attempt provider-level deletion of the incomplete SAF document and accurately report whether deletion succeeded or manual cleanup is required.
- Updated the R2 plan to describe the provider-dependent cleanup behavior and its limitations.

### Not validated
- No APK/AAB was built.
- No Termux command, Android runtime probe, SAF provider, emulator or physical-device test was run.
- No tests or static checks were run under the owner-directed test-later policy.
- SAF deletion remains provider-dependent; no universal rollback is claimed.
- Track R1–R10 remain in progress; no phase or Track R exit is claimed.

### Next
Continue R1–R10 source integration and close the remaining code-level gaps. Once the owner has a supported Linux x86_64 build host, run the pinned local build script; use the resulting APK for the owner-directed device-test campaign.


## 2026-11-08 — Integrated R-track build and regression evidence
**Scope:** R0–R10 integrated implementation campaign; CI build-first authorization.

### Verified
- Latest successful GitHub Actions run: [#1650](https://github.com/AssayFlux/Kinetics/actions/runs/42450892141), source commit `b5a591aa2b0545188409eacc0eb76043b4143fb8`.
- Python foundation job passed: pre-commit configuration, Ruff, production-code mypy, registry validation, Android configuration guardrails, pytest, reproduction stub and build-script syntax.
- Android arm64 build job passed: pinned Linux x86_64/JDK 17/Python 3.11.17/Android SDK 36/NDK 28.2.13676358/Rust target; custom Biopython arm64 wheel packaging; APK/AAB build; static ELF/APK alignment checks; Android JVM unit tests; artifact verification.
- APK SHA-256: `10896f91f622e979a1155c19263f825ccf5ee15e386d39ea1a56f28dd34c6056`, size 66,786,657 bytes.
- AAB SHA-256: `21aa978efcb65ad1e6040a398d1faf7fe1bc6c06d895fe12603860130d4a6ffa`, size 38,153,856 bytes.
- Uploaded artifact archive SHA-256: `9c32298574d2d7081274daaee5ae63828103cf47adbfbd19b0bc7d0db476867d`.
- Build log explicitly states no emulator or physical-device test was run.

### Boundaries / remaining
- CI green is not R1–R10 completion. R1 runtime/engine feasibility; R2 SAF, migration, crash and Keystore verification; R3 independent scientific validation; R4–R9 reference concordance, broader engines/data coverage and benchmarks; R10 transitive SBOM/licensing, security/accessibility review, device/performance tests and signing remain gated.
- R0 remains done by owner acceptance; this campaign adds regression evidence without reopening its historical gate.
- No clinical/patient workflow, validated scientific capability, device support or release claim is made.



## 2026-11-08 — UI/UX master specification and U0 foundations
**Phase:** Track U / U0 in parallel with R0–R10  
**Objective:** Adopt UI/UX contract, create U0 foundations and repair Compose build blocker.

### Done
- Added root `KINETICS_UI_SPEC.md` as the governing specification index.
- Added three unapproved token directions, settings schema, owner brand asset checklist/placeholders, token generator, fail-closed brand script and design-system skeleton.
- Added screen map, verified Android specs, device matrix, quality-report template, component catalogue placeholder and STRIDE threat-model draft.
- Fixed Kotlin unmatched closing brace reported at `MainActivity.kt:272`.

### Verified
- Official Android window classes and edge-to-edge guidance are recorded in `docs/ui/verified-specs.md`.
- Python foundation checks passed in run #1660 before the UI changes.

### Not validated
- The Kotlin fix still requires a fresh successful Android build.
- No gallery screenshot, responsive layout, TalkBack, contrast, 200% font, device matrix, Macrobenchmark or usability result is claimed.
- No visual direction or brand assets are approved. U0 remains in progress and must stop at owner choice.

### Next
Run Python/registry checks and Android build on the consolidated source. Complete exact full-text transcription of the owner spec and gallery screenshots before asking owner to choose.

## 2026-11-08 — Dark-first futuristic theme and typography proposals
**Phase:** Track U / U0, parallel with R0–R10  
**Owner direction:** Dark-first futuristic scientific workbench; selectable light, dark and neon theme families.

### Done
- Inspected the owner-supplied AssayFlux animated logo GIF (1024×1024, 26 frames). Existing repository brand SVG was left unchanged; no redraw, recolour or inferred seed colours.
- Added 13 palette proposals to `design/tokens.json`: 4 light, 5 dark and 4 neon combinations.
- Added three palette preview SVGs under `assets/design-previews/`.
- Added 26 distinct font-family candidates in `design/typography-catalogue.yaml`, spanning professional UI, futuristic, stylish, certificate/serif, monospace and accessibility roles.
- Extended settings schema with theme-family and font-family entries.
- Added a dark-default Light/Dark/Neon selector to the Compose shell. Selection survives activity recreation; durable settings persistence is not yet wired.
- Added `docs/ui/theme-proposals.md`, recorded owner preference in `DECISIONS.md`, updated Track U roadmap, and documented the animated logo asset boundary.

### Build evidence / limits
- Run #1700 Android arm64 APK/AAB build and package checks succeeded; Python foundation job failed only on a line-length lint error in `scripts/gen_brand_assets.py`.
- Fixed the lint line in commit `9ead9f15a23e28117abb3b999f3fa93a05a15c7d`.
- Run #1701 (older source snapshot) still had the pre-fix lint failure; Android build step was still running when this entry was written.
- Consolidated run #1712 is queued and is expected to validate the updated source; its result is not yet known.
- No emulator, physical-device, screenshot, contrast, TalkBack, 200% font-scale, CVD, performance or usability pass is claimed.
- Candidate font files are not bundled; exact version/licence, language, size and accessibility checks remain.
- Palette previews are proposals; contrast and colour-vision checks remain.
- Theme selector currently uses inline Compose colours. Token-to-Compose/CSS generation and migration to generated tokens remain unfinished.

### Gate
Owner has specified dark-first/futuristic as the intended direction. Exact default dark palette and the complete design-system/gallery approval remain open. U0 is not complete.


## 2026-11-08 — Owner artwork integration and CI repair
**Phase:** Track U / U0 in parallel with R0–R10

- Located the user's named assets in the Kinetics repository under `Assets/`.
- Inspected `Assets/Kinetics.png`: the bytes are JPEG despite the .png suffix. Preserved the original and copied its exact Git blob to `android/app/src/main/res/drawable-nodpi/kinetics_background.jpg`; Compose Home hero now displays it with a restrained dark overlay (light family uses a lighter overlay).
- Copied the exact owner organization-logo SVG blob from `Assets/Brand Logo.svg` to `assets/brand/brand-logo.svg`. No edit, conversion, recolouring or optimization. Updated brand instructions; official colours, clear space, variants and usage rules remain unconfirmed. App-logo placeholders still block release builds.
- Owner authorized the implementation team to choose a visual direction. Recorded Obsidian Cyan as the default dark direction in D-011; Light and Neon remain selectable alternatives.
- Fixed mypy's optional CairoSVG import error using a targeted missing-import ignore; the import remains optional and is only loaded when raster generation is requested.
- Run #1717 Python foundation job passed: Ruff checks, mypy (24 source files), registry validation, and pytest (111 passed, 3 skipped).
- Android APK/AAB build for run #1717 remained in progress at log time. It predates the final Home-background Compose integration and brand master copy. Run #1721 is queued for the current source; final debug APK availability is not yet established.
- No device, emulator, screenshot, TalkBack, contrast/CVD, font-scale, performance or usability test is claimed.


## 2026-11-08 — Responsive shell implementation
- Added live app-window navigation modes: bottom bar for compact portrait windows, rail for medium/expanded and compact-height windows, permanent drawer for large windows.
- Added an 840dp maximum readable content width and JVM tests for navigation breakpoint boundaries.
- Replaced inert status chips with non-interactive state labels carrying TalkBack content descriptions.
- Official Android window breakpoints and accessibility touch-target guidance recorded in docs/ui/verified-specs.md.
- Device screenshots, TalkBack, contrast, 200% font scale, fold posture, performance and usability remain untested. No accessibility or device-responsiveness pass claimed.


## 2026-11-08 — Session: Parallel R1–R10 closure and Track S1 start
**Phase:** Track R integration + Track S1 preparation  
**Objective:** Continue R1–R10 implementation while beginning independently implementable S1 work under the owner's explicit parallel-work authorization.

### Done
- Re-read ROADMAP, DECISIONS, SESSION_LOG, capability registry, current UI quality report, device matrix, third-party register and research implementation inventory.
- Confirmed R1–R10 are still recorded in progress; did not convert source implementation or a successful debug build into phase-completion claims.
- Added `python/kinetics/structure_view.py`: deterministic bounded structure-view payload preparation with explicit Angstrom units, finite-coordinate and annotation checks, duplicate serial rejection, atom ceiling and limitations.
- Added `tests/test_structure_view.py` for deterministic serialization and negative input cases.
- Registered `structure.viewer_payload` with evidence_level none.
- Added versioned `api/structure-view-payload.schema.json` and `docs/track-s/structure-viewer-contract.md`.
- Updated ROADMAP and DECISIONS with D-009: S1 preparation may proceed in parallel; WebView renderer and dependent S work remain gated by their dependencies.

### Not done / gates retained
- New Track S1 code has not yet been run through CI; no S1 renderer or third-party viewer bundle is present.
- R1 device/runtime, native engine, transitive license and performance evidence remain open.
- R2 interruption/migration/SAF/security device tests remain open.
- R3–R9 independent scientific validation and missing engine/data scope remain open.
- R10 complete SBOM, security review, UI accessibility/device matrix and release hardening remain open.
- Clinical/patient workflows remain disabled; no clinical claims are authorized.

### Next
- Run CI on the S1 preparation commit and fix any regressions.
- Continue the highest-risk R1/R2 integration and independent scientific validation work across R3–R9.
- Progress S1 viewer licensing and offline WebView integration only after confirming exact upstream assets and R1 runtime constraints.
- Update the phase evidence and quality reports from actual test/device outputs only.


## 2026-11-08 — Session: Verified debug build and expanded Track S discovery scope
**Phase:** Track R1–R10 integration + Track S1/S6–S10 planning and bounded preparation  
**Objective:** Verify the integrated Android artifact, correct stale project status, and define the owner's requested unknown-sequence/genome/protein-design scope without implying it is already implemented.

### Verified
- GitHub Actions run #1792 completed successfully on `2f426d4b70a10c3ddf4c5acbd9fd961937effb1a`.
- Python job passed Ruff lint/format, mypy across 26 production files, registry checks, reproducible token generation, Android guardrails and 119 tests (3 optional-dependency tests skipped).
- Android job passed arm64 debug APK/AAB build, package alignment, artifact verification and `testDebugUnitTest`; the Gradle task completed successfully.
- Artifact uploaded: [run #1792 artifact](https://github.com/AssayFlux/Kinetics/actions/runs/42460656392/artifacts/13610030667), 78,043,152-byte archive, SHA-256 `99a79072f6275ae9e69649222b2108452dd304d2d11445017df2a38e41ed6bd4`.
- APK SHA-256: `21e29a2c78ba58ddd5601d67859dbb966f340c1ab0927a6c798f4cc50fe29324`; AAB SHA-256: `0b4bdbf87e3ec9c8dfcc0444f8dcbfab5d9b5922772f26e4c0dee2375bef04a5`.
- Artifact is an unsigned debug build, expires 2026-11-22; CI did not run emulator or physical-device verification.

### Track S planning added
- Added `docs/track-s/discovery-and-design-roadmap.md` covering S6 unknown-sequence/protein-family intelligence, S7 genome annotation, S8 non-standard genetic-code investigation, S9 protein domain/structure intelligence and S10 constrained de novo protein design research.
- Extended the Track S roadmap table with explicit dependencies and evidence gates. S10 remains feasibility/planning only until model/data licenses, compute security, biosafety review and experimental validation gates pass.
- Updated README with the verified run/artifact and correct Track S parallel-work status; removed the stale run #1650 and stale NO-SOURCE JVM test claim.
- Owner-supplied files are present under `Assets/`; `Assets/Kinetics.png` is actually JPEG-encoded despite its extension. Preserve originals and respect the exact-blob brand master; do not infer official brand colours or convert the animated logo without an approved use case.

### Still open
- APK installation, launch, SAF import/export, encrypted-storage lifecycle, runtime probes, screenshots, TalkBack, 200% font scale, accessibility, fold posture, performance and low-end device tests.
- R1–R10 phase exit evidence, independent scientific reference validation, complete transitive SBOM/license review, security review and owner gates.
- Track S6–S10 are plans, not implemented capabilities; no unknown-code inference, production genome annotation or de novo protein design claim is made.
- No clinical/patient workflow or scientific validation claim is authorized.

### Next
- Continue R1/R2 runtime-critical and licensing/security evidence while improving R3–R9 reference validation.
- Start S6 schema/reference-pack foundations and S1 viewer licensing/bridge only within approved dependencies.
- Keep S10 model selection and generation blocked until its explicit gates are met.


## 2026-11-08 — Session: Parallel R/S/I/P execution and publication-readiness foundation
**Phase:** R1–R10 + S1/S6–S10 + I1–I5 preparation + P0-gated public-data preparation + G5 paper evidence  
**Objective:** Follow the owner instruction to progress all four tracks concurrently without bypassing dependencies; establish a reproducible publication evidence process before making scientific claims.

### Committed
- `docs/parallel-track-execution.md`: explicit parallel lanes, dependencies, evidence vocabulary, P0 restriction and publication gates.
- `paper/manuscript-skeleton.md`: software-methods manuscript structure with results reserved for measured evidence.
- `paper/claim-evidence-ledger.csv`: claim-to-evidence tracking template.
- `validation/RESULT-MANIFEST.md`: required metadata for immutable benchmark results, including dataset/license/version, method, uncertainty, outcomes, resources, provenance and independent review.
- Updated `ROADMAP.md` to link the parallel execution and paper-readiness documents.

### Track boundaries
- R1–R10 continue; no phase exit criteria are marked complete by this documentation increment.
- S work proceeds only where R4/R5, reference-data, renderer and model/license dependencies permit. S10 remains feasibility-only behind model/data, compute and biosafety gates.
- I1 begins with R6 descriptor correctness and public reference fixtures; I2/I3 engine execution remains gated on secure node and license review; I4/I5 remain research-only design and data/license review until independently validated.
- P0 remains blocked. Only public-data, non-patient schema/source inventory and test preparation are allowed; no patient interpretation, clinical output or Clinical Mode.
- Paper 1 is a candidate after R1–R3 exit evidence and independent reference validation. CI green or unit tests alone are not scientific evidence.

### Open evidence
- Android physical-device runtime, SAF/encryption lifecycle and accessibility/performance matrix.
- Independent reference suites and held-out benchmarks for R3–R9 and any I/S capability.
- Complete transitive SBOM/license inventory, model/database/asset licenses, security and node threat-model review.
- Qualified adviser/legal/ethics gate packet for P0; no patient data.
- Manuscript results, figures and claims remain empty until generated from reproducible validation records.


## 2026-11-08 — I1 chemistry reference-sanity increment
**Phase:** Track I / I1, parallel with R/S/P work

### Committed
- Added `validation/chemistry-reference-fixtures.json` with small-molecule identity and descriptor sanity expectations for ethanol and benzene.
- Added `validation/chemistry_reference.py`, which runs the fixtures through the optional RDKit adapter, records the active RDKit version, checks formulas/graph counts/basic descriptors within explicit tolerances, and emits machine-readable JSON.
- Extended `tests/test_chemistry.py` with an optional-dependency integration test for the runner. The test skips when RDKit is not installed.

### Boundaries
- These fixtures are engineering sanity checks, not an independently curated chemical benchmark or ADMET validation.
- RDKit is not yet pinned in a reproducible validation environment and is not bundled in the Android app.
- No ligand preparation, protonation/tautomer handling, biological activity, ADMET, PK/PD, docking or clinical prediction is validated.
- CI outcome for these commits is pending; no test pass is claimed until the workflow completes.

### Next
- Pin and review the host RDKit distribution/license, execute the fixture job in a controlled environment, and add independent reference materials before increasing I1 evidence status.
- Continue S6 sequence evidence implementation and R1/R2 runtime/security closure; keep P0 blocked.


## 2026-11-08 — S6 sequence evidence contract increment
**Phase:** Track S / S6 foundations, parallel with R and I work

### Committed
- Added `api/sequence-annotation-evidence.schema.json` (JSON Schema 2020-12) for sequence annotation outputs.
- The contract requires a query sequence SHA-256, sequence type/alphabet, versioned and licensed reference-pack provenance with content hashes, per-hit identity/coverage/score, explicit annotation status, confidence calibration status, abstention reasons and limitations.
- Novelty status is constrained to `not_established`; a no-hit result cannot be represented as proof of novelty.
- Added `tests/test_sequence_evidence_schema.py` to guard the provenance and abstention requirements.

### Limits
- This is an output contract, not a sequence-search implementation.
- No local protein family/domain database, calibrated threshold, annotation result, genome annotation or genetic-code inference is claimed.
- Test/CI status for this increment is pending.

### Next
- Implement bounded local reference-pack indexing and exact/similarity search with deterministic fixtures, explicit licensing, version/hash provenance and negative controls.
- Keep unknown/no-hit cases in abstention unless supported evidence meets calibrated criteria.


## 2026-11-08 — S6 bounded exact-reference triage implementation
**Phase:** Track S / S6 implementation foundation

### Committed
- Added `python/kinetics/sequence_reference.py` with deterministic exact full-length local reference matching for DNA, RNA and protein inputs.
- Added strict reference-pack metadata validation (name, version, license, source URI and lowercase SHA-256), unique reference identifiers, alphabet validation, and hard record/residue ceilings.
- Results include normalized query SHA-256, algorithm/parameters, pack provenance, exact-match identity/coverage, explicit no-hit abstention reasons and limitations.
- Novelty remains `not_established` for both hits and no-hits; no homology, family, domain, function or clinical inference is attempted.
- Added regression tests for positive matches, no-hit abstention, provenance, resource limits, invalid hashes, duplicate IDs and protein alphabet handling.
- Registered the primitive with `evidence_level: none`.

### Limits
- Exact full-length matching only; no BLAST-like local alignment, profile-HMM, gene caller, domain annotation or calibrated confidence.
- Pack provenance fields are supplied by the caller and are not independently verified by this code.
- No real reference dataset is bundled; synthetic fixtures are engineering tests only.
- CI is pending for this increment.

### Next
- Add content-addressed reference-pack ingestion and deterministic index persistence with licensing manifest validation.
- Add independently sourced positive/negative sequence fixtures before assigning validation evidence.
- Continue R1/R2 runtime/recovery closure, R3 reference comparisons and P0-gated public-data inventory.


## 2026-11-08 — S6 verified local reference-pack ingestion and P-track catalogue foundation
**Phase:** Track S / S6 and Track P / public-data-only preparation

### Committed
- Added `python/kinetics/sequence_pack.py` to load local FASTA reference packs from a strict JSON manifest.
- The loader verifies the manifest SHA-256 against the actual FASTA bytes, hashes the same open file descriptor again after parsing, and rejects content changes during ingestion.
- Added bounded manifest and FASTA byte reads, regular-file/symlink checks, record and residue limits, duplicate-ID rejection, and DNA/RNA/protein alphabet validation.
- Added `api/local-reference-pack.schema.json`, loader regression tests, and a registry capability with `evidence_level: none`.
- Added an intentionally empty public non-patient dataset catalogue, its strict schema, and intake rules requiring explicit license review, version/accession, retrieval time, SHA-256 and a false patient-data flag.

### Limits and gates
- Manifest license strings are provenance metadata, not a legal determination; each exact dataset/license/use still requires human review.
- No reference dataset payloads are bundled or downloaded. Synthetic fixtures only.
- The local loader is FASTA-only; no archive extraction, network fetching, similarity search, homology, gene function or novelty inference.
- P0 remains blocked. The P catalogue is metadata-only; no patient data, interpretation, clinical feature or Clinical Mode is authorized.
- S6 remains `evidence_level: none` until independent positive/negative reference validation and calibrated methods exist.

### Next
- Integrate loader-backed exact search, then add independently sourced reference fixtures and negative controls.
- Continue R1/R2 runtime, lifecycle, recovery and licensing evidence; R3 independent numerical comparisons; I1 pinned RDKit validation; S7–S9 only where data/engine dependencies permit.


## 2026-11-08 — R3 pinned synthetic SciPy comparison in CI
**Phase:** Track R3, host-side numerical validation foundation

### Committed
- Added `validation/requirements-scipy.txt` with exact NumPy/SciPy versions for the host-only comparison environment; the dependency file records BSD-3-Clause license identifiers.
- Added a dedicated CI job that runs the deterministic Michaelis–Menten comparison against `scipy.optimize.curve_fit` and uploads the machine-readable JSON result artifact.
- Updated validation documentation and R3 roadmap status to distinguish synthetic numerical comparison from experimental validation.

### Limits
- This does not bundle NumPy/SciPy into Android and does not establish mobile feasibility.
- Synthetic data and SciPy's independent numerical implementation are not experimental ground truth.
- No independent wet-lab dataset, calibrated uncertainty, or R3 exit gate is claimed; registry evidence remains none.


## 2026-11-08 — S6 loader-backed local exact-search integration
- Changed the verified pack loader to return its declared sequence type alongside the immutable metadata and parsed records.
- Added `search_local_fasta_reference`, which verifies the on-disk manifest and payload before passing records into the exact-only DNA/RNA/protein triage primitive.
- Added an end-to-end regression test asserting content-hash provenance and that exact hits still do not establish novelty.
- Similarity search, homology/family/domain annotation and calibrated thresholds remain unimplemented; evidence level remains none.


## 2026-11-08 — R1 declared dependency inventory and R2 cancellation-state safeguard
- Extended the SPDX source inventory generator to include host-only validation requirements while labelling them as non-Android runtime dependencies.
- Added a CI job to generate and retain the declared direct-dependency SPDX inventory for each commit, plus a regression test for SciPy/NumPy inventory coverage.
- Updated the third-party register to distinguish host validation dependencies from Android runtime packages and retain `NOASSERTION` where exact license conclusions/transitive artifacts remain unaudited.
- In R2, changed user cancellation to persist `cancelled` after requesting WorkManager cancellation, avoiding a permanently active `cancel_requested` state when a queued worker never starts. Added a detailed SAF/encryption/recovery device verification matrix; none of those device scenarios is claimed passed.
- R1 remains open pending full resolved/transitive dependency and binary/file-level license audit, engine decisions and physical-device runtime/performance evidence.


## 2026-11-08 — S8 explicit genetic-code translation foundation
- Added `python/kinetics/genetic_code.py` with explicit NCBI translation tables 1, 2, 4, 5 and 11, including table-specific start and stop codons.
- Added frame selection, RNA-to-DNA codon normalization, optional explicit trailing-partial-codon trimming, and strict CDS start/stop/internal-stop validation.
- Added tests for alternative mitochondrial tables, bacterial/plastid table 11, alternative initiator handling and invalid/ambiguous inputs.
- Registered the capability at `evidence_level: none`; no genetic-code inference, organism identification, gene finding or biological function claim is made.


## 2026-11-08 — S8 independent codon-table reference comparison
- Added a host-only Biopython 1.88 reference requirement and `validation/genetic_code_biopython_reference.py`.
- The comparison checks all 64 codons plus start/stop codon sets for each implemented table (1, 2, 4, 5 and 11), and emits a machine-readable result.
- Extended CI to upload both the synthetic SciPy kinetic comparison and genetic-code table comparison records.
- Updated the SPDX generator so host-only requirements are inventoried while shared Android/host dependencies (Biopython 1.88) retain both contexts rather than being misclassified as host-only.
- This checks implementation transcription against Biopython; it does not prove biological truth or infer any organism's genetic code. S8 evidence remains none.


## 2026-11-08 — I1 pinned RDKit host-side sanity validation
- Added `validation/requirements-rdkit.txt` pinning RDKit 2025.9.4 for host-only fixture execution.
- Added a separate CI job that runs the ethanol/benzene descriptor sanity harness and uploads a machine-readable JSON record.
- The dependency inventory generator includes the RDKit validation pin as host-only; it is not bundled in Android.
- This is a descriptor/parser sanity check against RDKit, not an independent chemical benchmark, ADMET, biological-activity, docking, PK/PD or clinical validation.


## 2026-11-08 — CI evidence checkpoint (run #1870)
- Python foundation, registry, Ruff/mypy and unit-test job completed successfully on commit `1a416f00d55975e7021ea6b454348d2f9af3740a`.
- Pinned host-side scientific reference job completed successfully: deterministic Michaelis–Menten comparison against SciPy and exhaustive 64-codon/start/stop comparison against Biopython 1.88. Uploaded artifact: [host reference results](https://github.com/AssayFlux/Kinetics/actions/runs/42464525641/artifacts/13610754008).
- Direct-dependency SPDX inventory job completed successfully.
- Android arm64 job failed before build execution because setup-python could not download the pinned Python 3.11.17 build host (HTTP 504 from the hosted toolchain download). This is an infrastructure/setup failure, not a compile or test failure; no APK/AAB artifact was produced in that run.
- Changed the Android build runner from `ubuntu-latest` to `ubuntu-24.04` to stabilize the pinned host environment. Awaiting the subsequent workflow run before claiming a build result.
- Scientific reference job success is limited to synthetic numerical agreement and codon-table transcription conformance; no experimental truth, biological validation or S8 genetic-code inference is established.


## 2026-11-08 — S7 bounded six-frame ORF candidate scanner
- Added `python/kinetics/orf.py` to enumerate complete start-to-stop ORF candidates on both strands and all three frames using an explicitly selected NCBI genetic code.
- Retains nested starts, reports 0-based half-open coordinates on the supplied sequence, maps reverse-strand intervals back to input coordinates, and enforces a maximum ORF count.
- Added regression tests for forward/reverse coordinates, nested ORFs, alternative-table stop behavior, ambiguity rejection and resource limits.
- Registered as implemented with `evidence_level: none`.
- This is a heuristic candidate enumerator only. It is not a prokaryotic gene caller or eukaryotic annotation pipeline; it does not model promoters, RBS, introns, splice sites, transcripts, operons, gene function or genetic-code inference.


## 2026-11-08 — CI checkpoint #1877 and Gradle distribution fallback
- Python foundation completed successfully: Ruff checks, strict mypy, registry validation and `148 passed, 4 skipped` tests.
- Pinned SciPy/NumPy and Biopython reference job passed and uploaded both synthetic kinetic and five-table codon comparison records.
- Pinned RDKit 2025.9.4 ethanol/benzene descriptor sanity job passed and uploaded its JSON record.
- Declared direct-dependency SPDX inventory generation passed.
- Android build host setup reached Python 3.11.17, JDK 17, Rust 1.88.0 and Android NDK 28.2.13676358, but Gradle distribution retrieval returned repeated HTTP 504 responses before compilation began; no APK/AAB was produced.
- Added a checksum-verified direct `downloads.gradle.org` distribution URL with `services.gradle.org` fallback. This is a network-resilience change, not evidence of a successful build; the next CI run must verify it.


## 2026-11-08 — CI checkpoint #1885 (S7 included)
- Python foundation completed successfully on commit `6312f74528f1c4aefe2f033de76611352f0a10b2`: Ruff passed, strict mypy reported no issues in 30 source files, and `153 passed, 4 skipped` tests.
- Pinned SciPy/Biopython reference comparisons, RDKit descriptor sanity fixtures, and direct-dependency SPDX generation all completed successfully.
- The newly added six-frame ORF scanner and its strand/coordinate/table-specific tests are included in the passing Python suite.
- Android build was still running when this checkpoint was recorded; no build success is claimed here.


## 2026-11-08 — R1 mirror fallback after repeated Gradle CDN gateway failures
- CI run #1899 passed Python foundation (`159 passed, 4 skipped`), strict mypy (30 source files), SciPy/Biopython, RDKit and SPDX jobs.
- Android setup succeeded with the separately pinned host CPython 3.11.18, JDK 17, Android SDK/NDK and Rust toolchain.
- Gradle 8.13 retrieval still failed because both official distribution endpoints returned HTTP 504 before compilation. No APK/AAB was produced.
- Added an Aliyun Gradle distribution mirror as a final transport fallback. The build script accepts the downloaded archive only if its SHA-256 matches the pre-recorded Gradle 8.13 digest; no alternate Gradle version or unverified bytes are accepted.
- Added a content-filtered Kotlin Maven mirror for compiler artifacts. Mirror integrity and transitive dependency review remain open; this is build infrastructure only.
- Awaiting a new CI run to verify both mirror paths. R1 remains open.


## 2026-11-08 — R1 first successful reproducible arm64 debug build (CI run #1904)
- GitHub Actions run [#1904](https://github.com/AssayFlux/Kinetics/actions/runs/42465569625) completed successfully on commit `30d19ea2bec8a7ad0039eb48fa13ac6bfb6175ed`.
- Built the arm64 debug APK (67,678,526 bytes; SHA-256 `0877bfe3331fc596dcaf440f8a659ddf5396c75484e172d2697bf2a7245269f6`) and debug AAB (38,860,218 bytes; SHA-256 `8ec29ece71ffbe3cef13ca3c25c759d4da958898cbdcde1e8ebad0c75b4db7cd`). Both artifacts passed the repository artifact size/integrity checker.
- Android Gradle build and JVM unit-test task completed successfully. APK ZIP alignment and native ELF alignment checks completed in the build lane; pinned Python foundation, registry checks, Ruff, strict mypy, 159 passed / 4 skipped Python tests, SciPy/Biopython reference comparisons, RDKit descriptor sanity fixtures and SPDX inventory jobs also passed.
- Gradle retrieval succeeded through the checksum-pinned multi-source fallback after prior HTTP 504 failures. This is the first successful build evidence for this integrated source state.
- Boundaries: no emulator or physical-device install/runtime test was run; no cold-start, memory, thermal or offline runtime evidence exists. The declared SPDX inventory is not a complete resolved transitive/file-level license audit. R1 remains in progress and no production engine/bundling decision is made by this build.
- The generated debug APK/AAB are available as workflow artifact `13611129700` (14-day retention) and were separately extracted for owner download in this conversation.


## 2026-11-08 — R2 non-destructive encrypted orphan inventory
- Added `EncryptedOrphanScanner` to identify finalized `.kdat` files without a matching database storage reference and `.encpart` files whose job is missing or already has finalized storage.
- Scanner ignores symbolic links and non-regular files, reports path/type/size/modified time, and never deletes, renames, decrypts or otherwise modifies ciphertext.
- Added `ResearchStore.encryptedOrphanInventory()` to compare app-private encrypted directories with durable job rows. The inventory is a review aid, not automatic cleanup or cryptographic recovery.
- Added JVM tests covering unreferenced finalized files, missing-job partials, stale partials for completed jobs, active partial preservation, symlink exclusion and proof that reported files remain intact.
- This advances the R2-14 implementation path only. Real app database integration, device inspection and the full R2 recovery matrix remain unverified; R2 stays in progress.


## 2026-11-08 — S9 conservative exact sequence-to-structure mapping
- Added `map_exact_chain_sequence` for mapping a supplied protein sequence to a selected structure chain only when the observed standard-residue sequence has one unique contiguous exact occurrence.
- Preserves query positions and structure residue numbers; repeated matches and no-hit cases abstain explicitly. Non-standard residues are rejected rather than silently coerced.
- Added tests for unique mapping, repeated-match abstention, no-match, unsupported residue and invalid query/chain inputs.
- Limitations: no alignment, gaps, missing/disordered residue repair, insertion-code handling, variant-effect analysis, homology or function inference. S9 remains in progress pending residue-number semantics, reference fixtures and independent validation.


## 2026-11-08 — I4 and P public-source inventory preparation
- Added a metadata-only candidate source inventory for NCBI Gene, PharmVar, ClinVar and CPIC. Candidate rows are explicitly marked `verify_before_intake` and `patient_data: false`; the schema rejects unreviewed candidates being represented as license-approved entries.
- Kept `entries: []`: no dataset payload has been retrieved, no hash or retrieval date has been fabricated, and no license approval is claimed.
- Added I4 discovery notes for PubChem BioAssay, ChEMBL, Tox21 and FDA DILIrank as candidate research sources only. Exact releases, endpoint quality, license terms and applicability must be reviewed before intake. No ADMET/PK/PD/PBPK model was selected or evaluated.
- P0 remains blocked. No patient data, genotype interpretation, clinical recommendation, treatment/dosing output or clinical feature was enabled.


## 2026-11-08 — S9 / I4 / P source-preparation checkpoint
- S9 exact chain-sequence mapping implementation and tests are committed; mapping only occurs for a unique contiguous exact match of canonical residues and preserves structure residue numbering. Alignment, insertion codes, missing residues and variant/function interpretation remain unsupported.
- I4 now has a candidate source inventory (PubChem BioAssay, ChEMBL, Tox21, FDA DILIrank) with explicit pre-intake review requirements; no dataset or model is approved, ingested or evaluated.
- P metadata catalogue separates candidate discovery (NCBI Gene, PharmVar, ClinVar, CPIC) from acquired entries. Candidate schema requires `verify_before_intake` and `patient_data: false`; acquired entries remain empty. Added a YAML/schema regression test.
- P0 remains blocked. No patient data, clinical interpretation or recommendations are enabled.


## 2026-11-08 — R9 source-snapshot catalogue coverage reporting
- Added `gene_catalogue_coverage_report` for bounded summaries by taxonomy, gene type and source release, plus missing-annotation counts.
- The report explicitly returns null completeness percentage/denominator because an expected gene universe must be independently defined; it does not claim genome-wide completeness or clinical coverage.
- Added tests for multi-taxonomy counts, missing denominator semantics and entry bounds; registered the source capability with evidence_level none.


## 2026-11-08 — I4 machine-readable candidate catalogue
- Added metadata-only candidate source records for PubChem BioAssay, ChEMBL and Tox21 with endpoint-specific review requirements.
- Added a strict schema requiring license status verify_before_intake, patient_data false and zero acquired entries. No data bytes, model weights, release IDs, license approvals or prediction results are claimed.
- Added YAML/schema regression test. I4 remains preparation-only pending exact release, license, endpoint and validation review.


## 2026-11-08 — S9 bounded residue mapping hardening
- Added configurable limits for query sequence length (default 1,000,000 residues) and observed structure-chain residues (default 100,000).
- The structure residue cap is enforced while consuming the atom iterable, preventing unbounded materialization of a chain. Invalid/non-positive limits fail explicitly.
- Added regression tests for query and structure caps. Exact unique mapping and abstention semantics are unchanged.
- Automated CI run #1943 passed immediately before this hardening on commit `06c48d24a429`; the new commits are awaiting their own CI validation. S9 remains in progress.


## 2026-11-08 — S9 streaming and atom-count bound
- Hardened exact chain mapping to consume the supplied atom iterable incrementally instead of materializing all atoms for the selected chain.
- Added a global input atom cap (default 2,000,000), in addition to the query residue cap (1,000,000) and structure-chain residue cap (100,000). Exceeding any configured limit fails explicitly.
- Added regression coverage for streaming atom limits and invalid limit values. The current mapping remains exact-only and intentionally abstains on numbering gaps, non-standard residues, repeated matches and no-hit cases.
- CI run #1949 was queued for these changes at the time of this log update; no pass is claimed until it completes.


## 2026-11-08 — Owner UI reference assets recorded
- Confirmed repository assets `Assets/App UI - Dashboard Design.jpg` and `Assets/App UI - Login Page Design.jpg` are the owner's visual references for the preferred Kinetics UI design language.
- Recorded D-013: preserve both source images and align dashboard/authentication plus shared UI patterns to their visual language without compromising accessibility, responsive layouts, scientific clarity or brand constraints.
- Detailed visual extraction and screenshot comparison remain pending; no claim of having visually inspected or matched the images is made in this checkpoint.


## 2026-11-08 — Owner UI master prompt captured additively
- Audited the current README, root UI-spec index, living UI specification, verified Android UI constraints, decision log, roadmap, token source and brand-asset contract before reconciling the new prompt.
- Confirmed the app stack is native Android/Jetpack Compose; no framework change is appropriate. Existing repository masters, decisions, capability boundaries, Android accessibility baselines and release gates remain authoritative where they overlap.
- Added `docs/ui/owner-master-prompt-addendum.md` to capture only additive requirements: delicate visual treatment, motif manifest/pool and deterministic daily picker proposal, theme contrast automation, reduced-motion behavior, cultural respect, expanded screen-state requirements and corresponding test/README expectations.
- Linked the addendum from README. No screens, tokens, fonts, logos or existing UI were replaced. Motif system and detailed visual implementation remain subject to reconciliation with the full master and Track U gates.
- Owner's prompt proposes alternate font families; no typography change was made because existing approved repository decisions/catalogue take precedence. No font binaries were bundled.


## 2026-11-08 — Owner approved new Kinetics visual system (D-015)
**Objective:** Replace conflicting old UI instructions with the owner's newly approved six-screen visual direction while preserving historical decision auditability and all non-UI project gates.

### Recorded
- Owner explicitly approved the generated six-screen concept (splash, login, dashboard carousel, navigation drawer, profile/settings, appearance) and directed that the new design be documented and implemented carefully.
- Added canonical `docs/ui/kinetics-visual-design-system.md` with Light Classic/Dark Classic palettes, typography roles, screen composition, motif provenance and deterministic picker requirements, accessibility, engineering constraints, implementation sequence and acceptance checklist.
- D-015 added to `DECISIONS.md`; prior D-009 visual proposal gate, D-010/D-011 dark-first/Obsidian Cyan default and D-014 palette/typography proposal marked superseded for active UI direction. Historical records retained intentionally for auditability. D-012 responsive navigation and D-013 owner reference layout remain active where compatible.
- `docs/ui/ui-spec.md`, root `KINETICS_UI_SPEC.md`, `design/tokens.json`, README and this session log updated to point to the new authority. Previous additive UI prompt is marked historical/superseded.

### Not claimed
- No app screen implementation, font binary bundling, motif assets, contrast pass, accessibility pass, screenshot test or device verification is claimed by this documentation change.
- Generated concept art is not a screenshot of the running app. Actual logos remain byte-for-byte preserved; UI must use real registry-backed capabilities and actual app state only.

### Next
Audit current Compose screens, token generator, settings persistence and asset inventory; implement Light Classic semantic tokens and shared Compose components, then refine real screens in dependency order. Continue R1–R10, S, I and P implementation in parallel where dependencies permit; preserve all scientific, licensing, privacy, security, ethics and publication gates.


## 2026-11-08 — Session 18: D-015 CI repair and S7 resource hardening
**Phase:** Integrated R1–R10 with parallel S/I/P preparation  
**Objective:** Restore deterministic design-token generation, align the active theme metadata with D-015, and bound ORF candidate scanning.

### Done
- Committed generated Compose and WebView token outputs for Light Classic and Dark Classic so the generator's reproducibility check can compare the checked-in files against its output.
- Repaired the malformed typography catalogue selection-policy line and removed the duplicate display-serif entry.
- Aligned design token metadata with the approved Light Classic default and Dark/System appearance; other catalogue palettes are not active UI selections.
- Added explicit S7 ORF scan limits: maximum genome bases, maximum simultaneously open starts per frame, and maximum emitted ORFs. Included the effective limits in result provenance.
- Added regression tests for over-limit sequence length, open-start accumulation and invalid resource limits.

### Validation status
- Previous latest CI run #1982 failed because generated token outputs were not committed and Android compilation could not resolve the new palette symbols. The generated output commits address the first defect and supply the missing symbols; a later CI run must verify both.
- CI run #1983 was started before the WebView CSS output was committed and failed the reproducibility step on that earlier commit; it is not evidence for the complete fix.
- Newer CI runs are queued/pending at this log update. No passing build or test result is claimed for the latest changes.
- S7 remains an ORF candidate enumerator, not a prokaryotic/eukaryotic gene annotation pipeline. No gene function, organism identity or genetic code is inferred.

### Remaining
- Verify the latest complete CI run including token reproducibility, Python tests, Kotlin compilation, APK/AAB package checks and Android JVM tests.
- Continue the approved R/S/I/P tracks against their roadmap dependencies and gates.


## 2026-11-08 — Session 19: Bound exact-reference search and correct S6 evidence claims
**Phase:** Track S / R1–R10 integration  
**Objective:** Prevent unbounded query allocation and make roadmap claims match the actual reference-search implementation.

### Done
- Added a configurable 5,000,000-residue default query ceiling to exact full-length reference search.
- Made all exact-search resource budgets require positive integers; booleans and fractional values are rejected.
- Included the query ceiling in the returned search parameters for reproducibility.
- Added regression tests for oversized queries and invalid integer budgets.
- Corrected the S6 roadmap statement: the current primitive accepts caller-supplied pack metadata and does not independently verify reference-pack bytes, license, or release. Similarity/homology search and novelty inference remain unimplemented.

### Validation
- The source and tests are committed. CI run #1993 is pending at this log update; no new test pass is claimed.
- Exact-only matching remains a conservative triage primitive; no gene/protein function, family, clinical interpretation, or novelty conclusion is produced.

## Session 20 — 2026-11-08
- Confirmed CI run #1999 passed all five jobs: Python foundation/tests, SPDX inventory, RDKit descriptor sanity fixtures, pinned scientific-reference comparisons, and Android ARM64 debug APK/AAB build/package checks.
- S9: hardened sequence-to-structure mapping resource limits to require positive integers (reject booleans and floats); replaced repeated full substring slicing with early-stop string search that also detects overlapping repeated exact matches; added regression tests for invalid caps and overlap ambiguity.
- Commits: `eaa532e` (implementation), `aef4501` (tests). CI for these commits is pending.
- Remaining S9 gates: alignment/gap handling, insertion-code-aware residue identity, licensed domain/family references, curated independent structure mappings and benchmark concordance.
- R/S/I/P remain active. No device-runtime, independent biological/chemical validation, dataset license approval, P0 clearance or paper submission readiness is inferred from CI.

## Session 21 — 2026-11-08
- S9: exact sequence-to-structure matching now rejects boolean/floating-point resource limits and stops after detecting a second occurrence while still detecting overlaps; added regression coverage.
- I1: added incremental SDF stream ingestion that buffers one record at a time and enforces positive-integer maximum record count, per-record character budget and aggregate character budget; preserves explicit V2000/V3000 subset limitations. Added stream, limit and invalid-budget tests.
- Commits: `eaa532e`, `aef4501` (S9); `9f26dc0`, `ea94516`, `e448d30` (I1).
- CI run #1999 passed before these changes. CI for current commits is pending; no passing status claimed yet.
- I1 remains exploratory: descriptor reference fixtures are host-side sanity checks, not an independently curated chemistry benchmark or validated biological/ADMET model. P0 remains blocked.

## 2026-11-08 — Session 22: Owner-directed integrated implementation and verification cycle
**Phase:** Track R1–R10 + S/I/P parallel work; UI/authentication delivery correction  
**Objective:** Correct the delivery process and active product plan after owner review found the APK still used old UI, lacked login/biometric flows and exposed incomplete options.

### Done
- Re-inspected Android entry point, Compose shell, app dependencies, manifest, UI screen map, canonical D-015 design system, UI spec, roadmap and decision log.
- Confirmed concrete gaps: no login/onboarding/profile screen; no biometric dependency or BiometricPrompt flow; dashboard still uses the old generic K mark and background hero; theme state is activity-session-only; Explore is informational rather than a tool dispatcher; only Home/Work/Explore/Settings are active destinations.
- Confirmed Work currently connects SAF import, background job management, cancel/resume, encrypted export and delete flows; this is not proof of full app functionality.
- Recorded D-016 and made build → automated test → artifact inspection → fix → repeat mandatory.
- Reaffirmed D-015 as the only active design. Earlier neon/Obsidian Cyan and pre-D-015 proposals are discontinued for active UI work and retained only as historical records.
- Expanded UI specification and screen map with authentication, biometric unlock, durable appearance, working-control and evidence requirements.

### Validated
- Repository source inspection confirmed the gaps above. No Android build, automated test, install, biometric prompt, emulator or physical-device verification was run as part of this documentation update.
- Latest known CI run #2009 on commit 9d2b0b012853d0092cee54841957c83331576abc was pending at inspection; verify before the next implementation commit.

### Not done / blockers
- D-015 screens are not fully implemented.
- Local app-lock trust model, secure recovery and BiometricPrompt integration are not implemented.
- No real device/emulator evidence for UI, login, biometric, accessibility, performance or complete app actions.
- Research modules still need registry-to-dispatcher-to-result-viewer integration.
- Existing debug APK is not the new-design/authenticated build and must not be represented as such.

### Next cycle
1. Verify workflow #2009 before pushing new changes.
2. Implement local app-lock and biometric capability handling with secure recovery semantics and tests.
3. Replace old dashboard composition with D-015 and integrate actual supplied logo assets.
4. Persist appearance settings and make exposed controls functional or explicitly unavailable.
5. Add UI/action/instrumentation coverage, build arm64 artifact, run regression suite, inspect screenshots and install/run on emulator/device when available.
6. Repeat the same cycle for remaining R/S/I/P workstreams while preserving scientific, licensing, privacy and ethics gates.

## 2026-11-08 — Session 23: Regression repair and D-015 dashboard increment
**Phase:** R/S/I/P parallel programme; Android UI and build verification  
**Objective:** Resolve CI regressions, advance the approved Light Classic dashboard, and keep implementation evidence synchronized.

### Done
- Corrected the streamed SDF parser to preserve blank molfile header lines and normalize line endings as actual newline characters.
- Corrected exact protein-chain matching to enumerate every overlapping occurrence instead of truncating the ambiguity report.
- Added a D-015 horizontal workspace carousel with three real-data panels: import entry, job counts/navigation, and device runtime diagnostics. The carousel uses actual job counts and runtime output; no placeholder metrics or fabricated activity were added.
- Updated the UI screen map: biometric prompt/capability source is present, Light/Dark/System preference persistence is present, and dashboard carousel source is present. Brand integration, secure recovery review, screenshot inspection and device verification remain open.
- Updated this session record and linked all work to the active masterplan and D-016 test cycle.

### Validated
- CI run #2023 exposed the initial regressions: 190 passed, 4 skipped, 2 failed.
- After the first fixes, CI run #2023 reported 191 passed, 4 skipped, 1 failed; the remaining failure identified the escaped-newline defect.
- CI run #2024 on source commit `b7bcf4c` reports Python foundation tests successful (196 collected; all passed), pinned scientific reference comparisons successful, RDKit descriptor sanity fixtures successful, and SPDX source inventory successful.
- The Android arm64 APK/AAB job in run #2024 was still in progress at the time of this entry.
- D-015 carousel source is committed in `99eba82`; current queued CI run #2026 includes the carousel and UI screen-map update. No build/test result is claimed for that UI commit yet.

### Not done / blockers
- No physical-device or emulator installation/runtime evidence is available.
- Android UI screenshot/accessibility checks remain outstanding; current CI builds and runs JVM unit tests, not instrumentation UI tests.
- Owner-supplied logo integration, audited typeface packaging, splash/onboarding/profile screens, and full D-015 screen completion remain open.
- Explore is still informational; registry-to-dispatcher-to-result-viewer integration remains open.
- Biometric unlock is a device-local app gate, not a cloud identity or biometric-bound data-encryption key. Recovery and device-level verification remain required.

### Next cycle
1. Complete the queued arm64 build and JVM tests for the carousel source.
2. Fix any Kotlin/Compose build or runtime defects and repeat the complete CI cycle.
3. Integrate the supplied owner brand asset without altering its artwork; verify layout, contrast and typography against the approved design references.
4. Add registry-backed capability browsing and connect only tools with real input contracts, dispatchers and result viewers.
5. Continue R1–R10 and S/I/P work in parallel, retaining explicit validation, licensing, privacy, biosafety and publication gates.


## 2026-11-08 — Session 24: Registry catalogue integration and Android compile repair
**Objective:** Continue the integrated R/S/I/P programme, correct the Explore catalogue integration and align the active UI implementation with D-015.

### Implemented in source
- Connected Explore to the generated capability catalogue derived from `capabilities/registry.yaml`. The screen is a registry-backed catalogue only; it does not yet dispatch research tools or imply that every listed capability is runnable.
- Corrected the Kotlin declaration defect that blocked Android compilation (`@Composable private private data class` on a data class).
- Removed the generic K badge from the hero and moved its visual treatment toward D-015's maroon/gold Light Classic and deep-plum Dark Classic language. This is an incremental style correction, not completion of the owner-reference redesign.
- Corrected the design-token metadata's stale `selected_direction` value to `kinetics_light_classic`, consistent with D-015.

### Build evidence at session start
- CI run [#2028](https://github.com/AssayFlux/Kinetics/actions/runs/42480571753), commit `d9d693040bf6ad83fdc01aca363dce7e3b5fb521`, failed during Android Kotlin compilation at the invalid `CapabilityEntry` declaration. Python, registry, scientific fixture, RDKit sanity and SPDX jobs passed; Android JVM and artifact packaging did not run.
- Previous run [#2027](https://github.com/AssayFlux/Kinetics/actions/runs/42479673744), commit `c3b047914d2ed729062cb2415591aaee1cc6a564`, built an arm64 debug APK/AAB and passed package checks. Those artifacts predate the current Explore changes and are not current-build evidence.
- No emulator or physical-device installation/runtime verification is claimed.

### UI design analysis and remaining work
- Current authority remains D-015 in `docs/ui/kinetics-visual-design-system.md`; the supplied reference assets are `Assets/App UI - Dashboard Design.jpg` and `Assets/App UI - Login Page Design.jpg`. They are source references, not proof of implementation.
- The active app still lacks the complete owner-directed splash/login/onboarding/profile flow and full brand-asset integration. The present biometric screen is a device-local app lock, not account authentication.
- Explore remains catalogue-only. A tool becomes launchable only after a real input contract, dispatcher, typed result, viewer, provenance and tests are connected.
- The S/I/P scientific, licensing, data, safety and governance gates remain active; no unsupported clinical or biological claims are introduced.

### Next verification
- Run CI on this correction; only report an APK/AAB after the exact new commit builds and artifact checks pass.
- Continue the next end-to-end research workflow and the D-015 screen implementation; test each increment rather than accumulating unverified work.


## 2026-11-08 — Session 25: FASTQ Android integration, build repair and document reconciliation

**Phase:** R4 vertical slice; D-015 UI implementation; R/S/I/P parallel delivery  
**Objective:** Follow D-016 document-first planning, connect bounded FASTQ quality analysis to Android Explore, verify the exact source, and reconcile the roadmap/UI/evidence records before the next implementation increment.

### Direction and documents reviewed before this increment
- Read `NORTH_STAR.md`, `ROADMAP.md`, `DECISIONS.md`, the latest session history and `docs/origin/KINETICS_MASTER.md`.
- Read the parallel-track execution protocol, integrated research-platform inventory, architecture boundary, R1–R4 phase plans, S discovery roadmap, I research boundaries, P public-data-only preparation, D-015 visual system, screen map and D-016 build/test requirements.
- Reconfirmed: R/S/I/P may proceed concurrently only where dependencies permit; scientific, license, security, P0, biosafety and device gates remain binding. Compose is presentation-only; domain algorithms remain in Python/Rust/C++. D-015 is the sole active UI authority.

### Implemented and verified
- Bounded FASTQ quality workflow uses the existing wrapped FASTQ parser and quality-summary primitive.
- Requires explicit Phred+33 or Phred+64 selection; encoding is never inferred.
- Enforces character, read-count and total-base limits; reports read/base totals, mean Phred, Q20/Q30 fractions and a compact per-read preview.
- Connected through Chaquopy to a native Compose Explore card beside FASTA QC.
- Added regression tests for multi-read summaries, explicit encoding, invalid quality lengths and resource limits.
- Corrected the FASTQ sample/fixture line-ending defect after run #2032 failed the Python test job.

### Exact-source verification
- Commit: `037befa8e9d22099e250dd22d3c4d772a6457034`.
- CI: [run #2033 — success](https://github.com/AssayFlux/Kinetics/actions/runs/42484179938).
- Python: 204 passed, 4 skipped.
- Pinned scientific-reference comparisons, RDKit descriptor sanity fixtures and SPDX direct inventory: passed.
- ARM64 debug APK/AAB build, static package alignment and Android JVM unit-test task: passed.
- APK SHA-256: `c902baada3c912e8ae5a166173e96e731c555b43ec2236031a8456c489ea990e`; size 69,793,535 bytes.
- AAB SHA-256: `f224d81850d1cb2858233ef9f82f7ed96969fc40712a96144e5b7757382c4f4d`; size 39,922,964 bytes.
- Uploaded workflow ZIP SHA-256: `20c8e277605afab518f1f7cbb33fbabb71b8da3b9dfed504aab91f3b95caa22a`. This is not the APK/AAB digest.
- Docs-only follow-up commit `ecc1d50` synchronizes the R1/R4 plans, UI screen map and CI evidence with this result.

### Not done / evidence boundaries
- No emulator or physical-device install/runtime evidence; Chaquopy runtime behavior on the target handset remains unverified.
- The FASTA/FASTQ cards are not yet SAF-backed streaming import, durable cancellable jobs, provenance persistence, result viewer or export workflows.
- The supplied dashboard/login reference JPGs and brand assets are present in the repository, but the running app has not been visually compared against them. D-015 implementation remains incomplete.
- No independent wet-lab/experimental validation is claimed. Host software reference comparisons are not experimental truth.
- R1–R10, S, I and P remain open according to their separate exit gates; P0 remains blocked.

### Next increment
- Continue document-first review before every code change. Prioritise the D-015 dashboard/login and owner-brand integration only after source/assets/theme/navigation architecture are audited; use actual app state and preserve original artwork.
- Continue R/S/I/P work in dependency-safe parallel slices, each with tests, exact-source CI and updated registry/evidence records.


## 2026-11-08 — Session 26: D-015 local lock screen and exact-source verification

**Phase:** Track U / D-015; integrated R/S/I/P programme continues  
**Objective:** Apply the approved adaptive visual system to the device-local lock screen, verify the exact source and reconcile evidence before the next UI increment.

### Direction and documents reviewed before implementation
- Re-read `NORTH_STAR.md`, `ROADMAP.md`, `DECISIONS.md`, prior session history, D-015 visual authority, UI screen map, R2 implementation/exit requirements, CI evidence and the affected Compose/activity/theme sources.
- Reconfirmed D-016: every substantial increment must build and test; CI does not replace emulator or physical-device execution.
- Reconfirmed that local biometric/device-credential app lock is not account authentication; no cloud account or biometric-template storage may be implied.

### Implemented
- Applied the selected Light Classic, Dark Classic or System-resolved palette and the current Kinetics typography system to the local biometric lock screen.
- Added clear local-device-security and fallback explanation, an explicit retry action, responsive scrolling and accessible error presentation.
- Preserved AndroidX BiometricPrompt behavior and its device-credential fallback; the UI does not receive or store biometric templates.
- The lock screen remains a local app gate, not a cloud identity or account sign-in implementation.

### Exact-source verification
- Commit: `79a24eb00ec7beea30674a591361c2351beaa13d`.
- CI: [run #2039 — success](https://github.com/AssayFlux/Kinetics/actions/runs/42493028735); all five jobs passed.
- Android ARM64 debug APK/AAB build, package-alignment checks, artifact-hash verification and Android JVM unit-test task passed.
- Python/registry tests, pinned host scientific-reference comparisons, pinned RDKit sanity fixtures and SPDX direct dependency inventory passed.
- APK: 69,792,811 bytes; SHA-256 `7029555e9640fd920f22a67890fe921473582affd2538e8aaddd61a261c9e44e`.
- AAB: 39,926,363 bytes; SHA-256 `dd6eb3cc6ddc97c9ed3036b4d6e0747c2e91ef2a6ee57f80eaa4e11e28b8cfa9`.
- Artifact ZIP: 79,991,103 bytes; SHA-256 `4b6211b80b9a50a773bdb38c20ee6f7026e327255844f1eeffeb696bc613d8cd`.

### Not done / evidence boundaries
- No emulator or physical-device installation/runtime test has been performed for this revision.
- No screenshot comparison against the owner-supplied dashboard/login JPGs or full D-015 six-screen implementation is claimed.
- Original brand integration, profile/onboarding/account identity, secure key-recovery review, accessibility instrumentation and full R2 end-to-end lifecycle remain open.
- Debug APK/AAB artifacts are not production-signed releases; scientific reference-fixture agreement is not experimental validation.
- R1–R10, S and I retain their individual gates; P0 remains blocked.

### Next increment
- Remove the unreferenced pre-D-015 hero composable and its obsolete image/gradient dependencies only after confirming the dashboard call graph, then refine the live-data D-015 dashboard carousel without inventing jobs, metrics or branding.
- Rebuild and test the exact next commit before accepting it as a baseline.


## 2026-11-09 — Session 27: P-track public-data engineering preparation

**Phase:** Track P / P1 safe public-data-only preparation  
**Objective:** Act on the owner's explicit P-track permission without misrepresenting it as approval for patient-data or clinical activity.

### Direction and documents reviewed
- Re-read the current roadmap, decision log, session history, P-track public-data boundary, public dataset catalogue/schema, dataset-intake policy and CI workflow.
- Reconfirmed D-004: qualified clinical-adviser engagement is revisited after R3 and is required before P0-gated activity.
- Reconfirmed P0 remains a separate legal, ethics, privacy, security, qualified-adviser and owner-evidence gate.

### Implemented
- Added `scripts/check_public_dataset_catalog.py` to validate non-patient source metadata, unique identifiers, HTTPS references, content hash shape, timezone-aware retrieval timestamps, and licence-review evidence for research-approved entries.
- Added conservative intended-use checks to reject clinical decision-support, diagnosis, treatment/dosing recommendation and patient-stratification language.
- Extended the public dataset JSON Schema so `approved_for_research` entries require reviewer, review timestamp, approved scope and evidence URL.
- Added synthetic tests for valid catalogue, patient-data rejection, duplicate IDs, missing hash/timezone, missing licence-review evidence and prohibited intended-use language.
- Wired the catalogue validator into the Python CI job.
- Updated P1 roadmap status to distinguish safe public-data engineering preparation from P0-gated patient/clinical activity; updated README and decision log with owner authorization D-017.

### Scope and evidence boundary
- The acquired dataset catalogue remains empty; no external dataset payloads were downloaded.
- Candidate sources remain `verify_before_intake`; no licence approval is inferred.
- No patient data, human subjects, genotype-to-phenotype interpretation, clinical recommendations or Clinical Mode are implemented.
- This increment advances P1 preparation only; it does not pass P0 or P1's scientific validation exit gate.
- Exact-source CI is pending at commit time; no passing build or test is claimed yet.

### Next increment
- Obtain green exact-source CI for this metadata gate.
- Add versioned non-patient synthetic genotype/variant fixtures and build/coordinate/allele-normalization contracts without clinical interpretation.
- Keep external datasets out of the repository until exact release, licence and intended-use reviews are documented.


## 2026-11-09 — Session 28: Build-pinned synthetic reference contract (P1/R4)

**Objective:** Continue P-track public-data preparation and strengthen R4's reference identity/coordinate provenance without admitting external or patient data.

### Documents and code reviewed
- Re-read the North Star, roadmap, decision log, session history, P-track preparation and catalogue policy, R4 plan, public dataset schema, registry, Python CI workflow and affected genomics parser/tests.
- Confirmed that the existing R4 small-variant normalizer checks REF against a supplied sequence but did not bind that sequence to a named assembly/release/contig, coordinate convention or digest.

### Implemented
- Added immutable `ReferenceSequence` metadata with assembly, accession, release, contig, 1-based-closed coordinates, retrieval timestamp, explicit synthetic non-patient classification and SHA-256 verification over uppercase ASCII sequence bytes.
- Added `normalize_against_reference`, which verifies reference identity and contig before calling the existing literal biallelic normalizer and carries reference metadata into the output.
- Explicitly records `interpretation_performed: false`; no transcript mapping, phasing, pathogenicity, PGx matching or clinical interpretation is performed.
- Added synthetic regression tests for successful left normalization/provenance, digest tampering, invalid coordinate conventions, patient classification, malformed sequence/timestamp, contig mismatch and REF mismatch.
- Registered the capability with evidence level `none`, exported the public API and updated P/R4 documentation.

### Evidence boundary
- Exact-source CI is pending; no test/build success is claimed in this log.
- The fixture is synthetic and does not represent GRCh37, GRCh38, T2T or any authoritative assembly.
- External reference-pack acquisition, licence review, full assembly/contig validation, independent normalizer concordance, Android integration and clinical interpretation remain unimplemented.

### Next
- Resolve any exact-source CI findings.
- Extend non-clinical synthetic VCF fixtures to validate build/contig/coordinate/allele provenance end to end.
- Continue R/S/I/P dependency-safe vertical slices; do not claim a track complete until all its exit evidence exists.


## 2026-11-09 — Session 29: I1 chemistry representation provenance

**Objective:** Improve the auditability of the existing optional RDKit descriptor adapter without implying Android readiness or biological/ADMET validity.

### Documents and sources reviewed
- Re-read the North Star, roadmap, decision log, latest session log, I-track research boundaries, R6 plan, RDKit adapter, chemistry tests, pinned RDKit reference fixture/script and CI workflow.
- Confirmed RDKit is host-only and that existing outputs reported engine/version and canonical isomeric SMILES but did not hash the exact supplied input or fully expose representation assumptions.

### Implemented
- Added SHA-256 over exact UTF-8 input text and byte count for SMILES and molblock analysis; no pre-parser text normalization is applied.
- Added explicit representation assumptions for sanitization, canonicalization, protonation, tautomer handling, aromaticity, stereochemistry, hydrogen handling and descriptor units.
- Added regression assertions for input hash/length and key chemical-state assumptions.
- Updated I1/R6 documentation and roadmap evidence description.

### Evidence boundary
- Pinned host RDKit reference fixture remains a basic sanity comparison, not an independent chemistry benchmark.
- Exact-source CI for the P1/R4 and I1 changes remains pending; no green result is claimed here.
- RDKit is not packaged in Android; no ADMET, biological activity, docking, PK/PD or clinical claim is made.


## 2026-11-09 — Session 30: S1 structure payload boundary hardening

**Objective:** Harden the offline viewer data boundary while renderer and WebView dependencies remain under license/security review.

### Documents and code reviewed
- Re-read the North Star, roadmap, decision log, latest session log, S1 viewer contract, S-track discovery roadmap, payload JSON Schema, structure payload implementation/tests and Android/CI constraints.
- Confirmed S1 currently produces a bounded coordinate payload but the serializer only checked the schema version and could serialize internally inconsistent payloads.

### Implemented
- Added strict payload validation before serialization: exact top-level and atom fields, supported source format, Angstrom units, atom-count consistency and bounds, non-empty limitation text, unique non-negative integer atom serials, non-negative residue numbers, bounded text annotations, normalized element labels and finite numeric XYZ coordinates.
- Added regression tests for mismatched counts, non-finite coordinates, duplicate serials, unexpected top-level fields and invalid metadata types.
- Updated S1 roadmap and viewer contract.

### Evidence boundary
- This is a validated serialization boundary in source/tests only; no Mol*/3Dmol.js renderer, offline bundle, WebView bridge, license approval or device rendering is claimed.
- Exact-source CI remains pending; no green result is claimed.


## 2026-11-09 — Session 31: Repair exact-source CI failures

**Objective:** Resolve the two independently observed failures in CI #2079 before continuing feature integration.

### Repository review
- Re-read NORTH_STAR, ROADMAP, DECISIONS, the latest session log, the parallel-track protocol, integrated R1–R10 inventory, R2 plan, S1 viewer contract, I1 chemistry plan and P1 public-data boundary.
- Confirmed D-016 requires fixing and rerunning the exact source, and that software tests do not establish scientific validation or device verification.

### Failure evidence
- CI #2079 Python job failed Ruff E501 at `scripts/check_public_dataset_catalog.py:163`.
- CI #2079 Android build produced the arm64 debug APK/AAB, but its JVM test task failed: `ImportProvenanceSummaryFormatterTest.untrustedInputNameCannotInjectAdditionalSummaryLines` (15 tests, 1 failure).

### Corrective changes
- Wrapped the public-catalogue status output to satisfy the configured 100-character Ruff limit without changing validation semantics.
- Changed provenance input-name sanitization to collapse consecutive control characters into one separator and trim boundary whitespace. This prevents CRLF input from creating doubled spaces while preserving a single-line display value.

### Verification boundary
- Fixes are committed for exact-source CI rerun. Do not mark the run green until the new workflow completes.
- Android build output from #2079 is not a verified APK because the same run's required JVM test failed.
- No emulator or physical-device installation/runtime verification is claimed.


## 2026-11-09 — Session 32: Regenerate the Android capability catalogue

- Exact-source CI #2080 passed Ruff, mypy and registry validation, then failed the generated Android capability catalogue reproducibility check.
- Root cause: the R4 reference-bound normalization capability was added to the canonical registry, but its generated Android asset was not regenerated.
- Updated `android/app/src/main/assets/capability-catalog.json` with the missing registry entry. The entry remains `implemented` with `evidence_level: none`; no validation claim was added.
- CI #2080 Android arm64 build and host-side scientific/chemistry comparison jobs were still running/successful at inspection time; final workflow status must be rechecked.
- Exact-source CI rerun required to accept this asset fix. No device verification is claimed.


## 2026-11-09 — Session 33: Harden human-readable provenance against metadata line injection

**Objective:** Ensure imported filenames and persisted metadata cannot forge additional claims or sections in the exported human-readable provenance summary.

### Reviewed
- Re-read the North Star, roadmap, decisions, latest session log, R2 import/provenance plan, Android formatter and its JVM tests.
- Confirmed the summary already sanitized input names, but other persisted scalar fields and the parameter text were rendered without the same single-line boundary.

### Implemented
- Apply the existing control-character and newline sanitizer to the job identifier, state, tool identifier, tool version and parameter JSON before rendering.
- Added a regression case attempting to inject clinical approval, validation, reviewer and interpretation lines through those fields.
- Kept the summary explicitly scoped to import/encryption/hash provenance; this does not create scientific or clinical evidence.

### Verification
- Exact-source Android JVM test and full CI rerun are required; no pass is claimed at commit time.
- No emulator or physical-device test is claimed.

### Next
- Run the new formatter regression through exact-source CI, then continue closing the R2 import-to-analysis-to-result/export lifecycle.


## 2026-11-09 — Session 34: Close remaining provenance hash line-injection path

**Objective:** Complete the single-line trust boundary for every string rendered by the human-readable import provenance summary.

### Reviewed
- Re-read NORTH_STAR, ROADMAP, DECISIONS, the latest session history, the R2 provenance/export plan, the formatter and its JVM regression suite.
- Inspected the formatter field by field after Session 33. The persisted input SHA-256 field was still rendered without the single-line sanitizer, unlike the job ID, state, tool metadata and parameter JSON.

### Implemented
- Apply the same control-character/newline sanitizer to the persisted input hash before rendering.
- Add a regression test that attempts to inject a forged clinical-status line through the hash field.
- Keep numeric byte counts and timestamps typed; no user-controlled display strings are introduced from them.

### Verification boundary
- Exact-source Android JVM and full CI results are pending. This source change is not yet accepted as a verified baseline.
- This is presentation/provenance integrity hardening only; it does not validate the import bytes, create scientific results or establish clinical evidence.
- No emulator or physical-device verification is claimed.

### Next
- Require the exact-source CI run to pass, then resume the R2 import → durable analysis job → result/provenance → SAF export integration.

## 2026-11-09 — Session 35: R-track two-step base cycle — CI regression correction

**Owner-directed sequence:** complete R in two explicit steps before starting S; then S, I, P and G in order.

### Step 1 — Build documented R base
- Keep R1–R10 as the base scope defined in ROADMAP; integrate rather than presenting isolated modules as a finished workbench.
- R2 import provenance hardening now sanitizes input name, job metadata, parameter JSON and input SHA-256 in the human-readable summary.
- CI exposed a contradictory regression assertion: the test both prohibited the sanitized phrase anywhere and expected that same phrase in the sanitized field. Corrected the negative assertion to reject only a newline-prefixed forged section.

### Verification boundary
- The current exact-source CI run failed at this contradictory JVM assertion; the ARM64 packaging step completed before the JVM test task failed. No successful tested build is claimed.
- The correction must pass the exact-source Android JVM suite and full CI before R Step 1 is accepted.
- No emulator or physical-device verification is claimed.

### Next
- Finish the R Step 1 integration base across import → typed analysis → durable result/provenance → export, then perform R Step 2 full audit and regression closure. Do not start S until R has passed its two-step gate.


## 2026-11-09 — Session 36: R Step 1 — connect authenticated imported FASTA to durable QC result

### Implemented
- Added a WorkManager analysis worker for completed FASTA imports only. It decrypts/authenticates the already stored KDAT input into the existing short-lived private cache helper, enforces 1 MB byte and character bounds, runs the registered local FASTA QC adapter, and removes the plaintext cache in the existing `withStoredInput` finally block.
- Added schema v4 `analysis_results` storage with foreign-key cleanup, exact source SHA-256, tool/version, parameters, result JSON and timestamp. Result persistence is transactional and only accepts succeeded imports with a recorded digest.
- Added a job-level Run FASTA QC action and saved-result inspection on Home/Work cards. Analysis is unique WorkManager work tagged separately for refresh.
- FASTQ is intentionally not auto-analysed: the user must explicitly choose Phred+33 or Phred+64; this worker only accepts FASTA extensions.

### Verification boundary
- CI for commit `45a54b6` is still running at the time of this entry. This new integration slice is not yet compiled or tested.
- No emulator/physical-device verification is claimed. No analysis export or full R-track exit is claimed yet.


### R Step 1 integration correction — 2026-11-09
- Source review after the first integration commit found two wiring defects before CI: a missing comma in the recent-jobs SQL projection and the Work screen not forwarding the new analysis callback. Both are corrected in the next commit.
- This is exactly why the two-step plan includes a dedicated audit/repair pass; no acceptance is claimed until exact-source CI passes.


### R Step 1 documentation sync — 2026-11-09
- Updated the R2 and R4 phase plans and roadmap to describe the new authenticated imported-FASTA → WorkManager → bounded QC → SHA-256-linked durable result → job-card inspection path.
- Remaining work is explicitly retained for R Step 2; no R-track completion percentage or acceptance is recorded until the exact-source audit and tests close.


### R Step 1 — analysis result export added — 2026-11-09
- Added a portable versioned analysis-result JSON envelope containing the method/tool identity, parameters, exact imported-input SHA-256, timestamp and result payload; source URI/private paths remain excluded.
- Added a user-mediated SAF JSON export action on the saved result view, with best-effort partial-document cleanup and explicit warning when the provider cannot delete.
- Exact-source CI is required for this additional slice; it is not yet verified.


### R Step 1 audit correction — analysis export callback wiring — 2026-11-09
- Source review caught the Work-screen job-card call missing the new analysis-export callback. Home already passed it correctly. Fixed the Work-screen call before accepting this increment.


### R Step 1 — documentation update for analysis export — 2026-11-09
- Updated the R2/R4 phase plans and ROADMAP to include the versioned SAF analysis-result export, source digest binding and privacy exclusions.
- R Step 1 remains unaccepted pending exact-source CI; R Step 2 will audit the complete R base and close migration, persistence, export and UI regressions.


### R Step 2 audit — reject oversized imports before plaintext materialization — 2026-11-09
- The first worker version checked the 1 MB cap after authenticated decryption to cache. The audit moved the committed byte-count gate ahead of decryption so a 512 MB stored import is rejected without creating a large plaintext cache file.
- Analysis persistence now validates the imported digest format before recording a result. Exact-source CI and tests remain pending.


### R Step 2 audit — result integrity and bounded UI preview — 2026-11-09
- Analysis JSON export now joins the current job and only emits a result if the job is still succeeded and its current SHA-256 exactly matches the digest bound to that analysis record.
- Worker validates both record_count and a non-empty records array and rejects results above the 2 MB persistence cap before storage.
- Job-card result preview is capped at 12,000 characters; the complete version remains available through the explicit SAF JSON export action, avoiding multi-megabyte Compose text rendering.
- CI for the preceding integration revision passed the arm64 APK/AAB build, Android JVM unit tests and artifact verification; this latest audit patch now requires its own CI run.


## 2026-11-09 — R Step 2: exact-source integration verification and final audit patch

### Verified revision
- Commit `fc8b667951626447d951931bbfd1f901867405be`, CI run #2093: all five workflow jobs passed.
- ARM64 debug APK and AAB built; APK ZIP/native ELF alignment checks passed; Android JVM unit tests passed; artifacts and hashes recorded in `docs/ci-build-evidence.md`.
- APK SHA-256: `29db7d4014eeba7e6ab0ac57465c636f74cddbfe3b673a19c5e355c1b5e9387b`.
- AAB SHA-256: `24ce93b67a3eeb1946e1e2c51ef181032422a637cd6f595d9716eef737b8c607`.

### Follow-on audit commit
- Commit `2ea102719fc37354f18def85bb329a60a885ee2a`: require current job SHA-256 equality when exporting analysis, reject malformed/empty/oversized QC results before storage, and cap Compose preview to 12,000 characters.
- Exact-source CI run #2094 is pending. Step 2 cannot be accepted until that run succeeds.
- Still not tested: SQLite migration/recovery under Android runtime, WorkManager interruption/retry, SAF provider cleanup on actual providers, full instrumentation/UI flow, emulator/physical device launch, Chaquopy execution on device and performance.
- No R-track completion claim is made from this base vertical slice.


## 2026-11-09 — Owner engineering integration standard
- Inspected NORTH_STAR, ROADMAP, DECISIONS, SESSION_LOG, architecture, contribution rules, language inventory, Gradle/CMake/Cargo/Python build configuration and existing JSON Schemas.
- Added `docs/ENGINEERING_INTEGRATION_STANDARD.md` with project profile, explicit target language ownership, current implementation gaps, integration-first workflow, boundary ABI rules, security/testing rules, required change record, Check/Next step format and R→S→I→P→G two-step sequencing.
- Added `api/engine-envelope-v1.schema.json` as the initial shared semantic contract for request/result/error messages. JSON Schema is the chosen contract source; operation-specific payload schemas and cross-language validators must be added with each operation.
- Linked the standard from architecture and CONTRIBUTING; recorded owner direction as D-018; added it to ROADMAP.
- Known gaps are stated, not hidden: current Rust/C++ is a probe, Swift/TypeScript/Three.js are absent, and no full cross-language contract validator exists yet. Team size, iOS minimum version and web graphics support remain TBD.
- No application interface or runtime behavior was changed in this documentation/schema increment.


### R Step 2 exact-source CI completion — 2026-11-09
- Commit `2ea102719fc37354f18def85bb329a60a885ee2a`, workflow #2094: all five jobs passed.
- ARM64 APK SHA-256 `d6b7bd05090519761bb1771b82c41f14b3c3ff2d834a1844d2ec0052babbb82b` (69,875,059 bytes); AAB SHA-256 `9c09035e9588e4af42554418c7f02e1efca2d84441f328b237f29c758c6c261f` (39,951,809 bytes).
- Android Gradle build, APK/native alignment checks, JVM unit tests and artifact verification all passed. Host Python, reference comparisons, RDKit sanity and SPDX jobs passed.
- This closes exact-source CI for the R2/R4 imported FASTA integration slice, not the entire R track. Device/runtime and dedicated migration/worker/SAF instrumentation checks remain open.


### Shared envelope contract test — 2026-11-09
- Added a Python contract test for `api/engine-envelope-v1.schema.json`: Draft 2020-12 schema self-check, valid request/result/error examples, and rejection of invalid version, digest, kind/payload combinations and malformed timestamp.
- Added `jsonschema[format]` as a development/test-only dependency in both project development dependency declarations. It is not an Android/iOS runtime dependency.
- Cross-language runtime validation remains to be implemented in each adapter as its corresponding operation is migrated; the Python test does not claim Kotlin/Rust/C++/Swift validation is already wired.


### D-019 execution-order correction — 2026-11-09
- Recorded the owner's current strict R → S → I → P → G sequence and two-step-per-track gate.
- Explicitly superseded D-009's earlier parallel S-track permission for current execution; no S/I/P/G work is to be started while R remains open.


### R Step 2 security cleanup regression — 2026-11-09
- Audit found that `withStoredInput` entered its cleanup `finally` only after successful decryption/materialization. A failed authenticated decrypt could therefore leave a partially written plaintext cache file.
- Extracted `withPrivateTemporaryFile` so cleanup encloses materialization as well as consumer execution; added JVM regression tests for partial materialization failure, consumer exception and success.
- This is a source-level security hardening change. Exact-source Android/JVM CI is required; it does not establish crash-proof secure erasure or device runtime behavior.


### R2 private plaintext cleanup exact-source CI — 2026-11-09
- Commit `c157bb5a09d9dcc17a8bc7a57b60129d58e4866a` passed all five jobs in CI run #2100, including Android ARM64 APK/AAB packaging and JVM tests.
- Regression tests for cleanup after failed materialization, consumer exception and success are included in that exact-source run.
- Artifact hashes and verification boundaries are recorded in `docs/ci-build-evidence.md`; this does not close device/runtime or migration gates.


## 2026-11-09 — Session 37: R-track evidence audit and stale test-status correction

### Reviewed
- Re-read the R1–R10 phase plans, current roadmap, engineering integration standard, CI evidence and latest exact-source workflow/job logs.
- Inspected the Python CI log for workflow #2101 at commit `8c4128d5e448db51f2b48fec6c38ce6022fdb053`: pytest collected 233 items and completed with 229 passed / 4 skipped.
- Confirmed R3/R4 research and sequence tests, R5 structure/view tests, R6 core chemistry tests, R7 phylogenetics tests, R8 omics tests and R9 catalogue/variant tests executed. Optional RDKit adapter tests (3) and pysam test (1) were skipped because those dependencies are not installed in the general test environment. The separate pinned RDKit sanity job passed.
- Confirmed the pinned host scientific-reference job's SciPy Michaelis–Menten and Biopython genetic-code comparison steps passed.
- Confirmed all five jobs in CI #2101 passed, including Android ARM64 APK/AAB packaging, static alignment and `:app:testDebugUnitTest`.

### Implemented documentation corrections
- Removed stale claims in R3/R7/R8 plans that regression tests or the SciPy comparison had not run.
- Updated R4 exact-source audit notes; recorded the run, test count, artifact hashes and verification boundaries in `docs/ci-build-evidence.md`.
- Updated ROADMAP with actual test evidence and remaining R-track blockers.

### Verification boundary
- APK SHA-256: `059abb9e3a299b5295b8f08772b976195d7be1cd7db46dce34faa7bcf486d2d9`; AAB SHA-256: `9c8e2ca3a81c4ef2b1fb041aefee99ace5cbfb3292574b815c6a87549210044e`.
- No emulator/physical-device install, Android SQLite migration/WorkManager/SAF instrumentation, Chaquopy on-device execution, independent experimental validation, comprehensive domain reference concordance, full transitive licence/security audit or release signing is claimed.
- R remains open; no S/I/P/G implementation was started. Continue R Step 2 against concrete gaps and do not pass the track gate prematurely.


## 2026-11-09 — Session 38: Expand SQLite migration regression coverage

### Reviewed
- Re-read the current R2 plan, roadmap, ResearchStore schema migration implementation and Robolectric migration test suite.
- Confirmed the existing suite exercised fresh schema creation and v3→v4 only, while the production upgrade path contains sequential v1→v2, v2→v3 and v3→v4 steps.

### Implemented
- Added synthetic legacy database fixtures for schema v1 and v2.
- Asserted both historical schemas upgrade through v4, preserve an existing job row and expose the expected storage_path, exported_at and analysis_results schema.
- Kept the existing fresh-install, v3→v4, digest-binding and cascade-delete cases.

### Verification boundary
- The new tests are committed as source only after the exact-source Android/JVM CI run passes.
- Robolectric migration tests do not replace Android device/runtime migration, interrupted-transaction or process-death verification. No R2/R-track exit is claimed.

### Next
- Run the exact-source CI suite, inspect the Android test result, then continue R Step 2 against WorkManager interruption/retry and SAF provider lifecycle gaps.


## 2026-11-09 — Session 39: Add independent structural software reference harness

### Reviewed
- Re-read the R5 scope, current PDB/mmCIF parser, contact and Horn-quaternion RMSD implementations, pinned host validation dependencies and scientific-reference CI workflow.
- Confirmed existing R5 tests covered deterministic geometry and parser edge cases but no independent parser/geometry comparison was executed in CI.

### Implemented
- Added a deterministic synthetic PDB reference harness comparing atom metadata/coordinates with Biopython 1.88.
- Added independent NumPy contact-distance and SVD/Kabsch RMSD calculations and explicit tolerances.
- Wired the script into the pinned scientific-reference CI job, added a fail-closed overall-pass assertion and uploaded the JSON evidence artifact.
- Documented the precise scope and limitations in the R5 plan and validation README.

### Verification boundary
- Exact-source CI must pass before this comparison is counted as executed.
- The fixture is synthetic and does not satisfy the R5 experimental reference-structure, mmCIF, SASA, interaction, benchmark or device exit criteria.

### Next
- Validate the exact-source run and continue R5 with real, licensed reference structures and explicit coordinate/contact tolerances.


## 2026-11-09 — Session 40: Verify legacy SQLite migration coverage

### Verification
- Exact-source commit `dd3269acfa79546b143e239948df4d95e938abc7`, workflow #2104, completed successfully across all five CI jobs.
- Android ARM64 debug APK/AAB packaging, static alignment checks, artifact verification and `:app:testDebugUnitTest` passed.
- The Robolectric suite now includes fresh-install, v1→v4, v2→v4 and v3→v4 migration coverage; v1/v2 fixtures verify retained job data and expected v4 schema.
- APK SHA-256: `958098b0143b02bd68a6dadbbcd783afbd1fd7c8a5893f553bda5ba365f316e9`; AAB SHA-256: `773cc9cf5569d3eabb6c2665de79a4e0d8e0a47fba3f7b3f6c3c272552996e67`.
- Artifact ZIP SHA-256: `f9a0e18045a8a418691900868f4f78fd595a30798e2c95da29e82a00649ad7fc`; artifact ID `13647404333`.

### Evidence boundary
- Automated Robolectric migration tests are now green for the documented schema versions.
- No device SQLite migration, transaction interruption, process-death, WorkManager retry/resume, SAF provider or on-device Chaquopy execution is claimed. R2 and R remain open.


## 2026-11-09 — Session 41: Cross-check SDF graph parsing against RDKit

### Reviewed
- Re-read R6 scope, local V2000/V3000 parser, graph descriptor tests, optional RDKit adapter, pinned RDKit host fixtures and third-party approval boundaries.
- Confirmed the existing RDKit reference fixture tested adapter descriptor outputs but did not compare the local SDF graph parser with an independent cheminformatics parser.

### Implemented
- Added a deterministic explicit-atom cyclopropane V2000 fixture.
- Compared local and RDKit atom/bond counts, element identities, bond orders, coordinates and cycle rank/ring count.
- Added explicit tolerance and documented why implicit-hydrogen formula equality is not asserted.
- Made the reference script fail closed and extended the optional RDKit regression test.

### Verification boundary
- Exact-source CI must pass before this new comparison is counted as executed.
- Synthetic graph concordance does not establish stereochemical/tautomer/protonation correctness, chemical benchmark performance or Android RDKit feasibility/licensing.

### Next
- Validate the exact-source RDKit host job and continue R6 against an owner-approved reference corpus and engine/license feasibility decision.


## 2026-11-09 — Session 42: Add independent phylogenetic NJ reference harness

### Reviewed
- Re-read the R7 phylogenetics scope, neighbour-joining implementation, Newick/tree-distance tests and pinned Biopython reference environment.
- Confirmed existing tests checked selected additive three-taxon distances but did not compare the local NJ implementation with an independent tree-construction package in CI.

### Implemented
- Added a deterministic four-taxon additive distance matrix with unequal terminal branches.
- Added a Biopython 1.88 NJ reference tree and compared all six patristic pair distances against Kinetics with a 1e-8 tolerance.
- Added fail-closed output and CI artifact upload alongside the existing scientific-reference records.
- Documented the synthetic-only evidence boundary in the R7 plan and validation README.

### Verification boundary
- Exact-source CI must pass before this check is counted as executed.
- This does not establish published phylogeny concordance, model-based inference, evolutionary interpretation, search/viewer functionality or device performance.

### Next
- Validate the exact-source run, then extend R7 with a frozen licensed reference alignment/tree set and documented topology/branch tolerances.


## 2026-11-09 — Session 43: Add independent NB2 likelihood reference harness

### Reviewed
- Re-read the R8 differential-expression implementation, normalization/dispersion method, current NB2 tests and pinned SciPy validation environment.
- Confirmed the current regression suite exercised synthetic behavior but did not compare the IRLS estimates and Wald statistics with an independent optimizer.

### Implemented
- Added a deterministic raw-count comparison fixture with explicit median-of-ratios size factors and per-feature moment dispersions.
- Added an independent SciPy NB2 log-likelihood optimizer and Fisher-information standard-error/Wald calculation.
- Compared condition coefficients, standard errors and p-values with explicit tolerances; wired a fail-closed script and JSON artifact into host reference CI.
- Documented the synthetic-only boundary in the R8 plan and validation README.

### Verification boundary
- Exact-source CI must pass before this comparison is counted as executed.
- This does not validate dispersion moderation, repeated-measures models, outlier handling, null calibration, power, FDR control or biological truth.

### Next
- Validate the exact-source comparison and continue R8 with null simulations, power/FDR calibration and an independently reviewed reference dataset.


## 2026-11-09 — Session 44: Verify R5 structural software reference comparison

### Verification
- Exact-source commit `f1681ea5e2009f8bcbc33468689108affe57e56c`, workflow #2105, passed all five CI jobs.
- The pinned host scientific-reference job executed the new Biopython/NumPy structural comparison and its fail-closed overall-pass assertion.
- PDB atom metadata/coordinates, contact-pair distances and superposed RMSD agreed with independent references within recorded tolerances.
- Android ARM64 build, static alignment and JVM unit tests passed. APK SHA-256: `f3bb4c76f4cd36ab747efd77e0ba63b79feab2f74c521e4fd9959a298463270d`; AAB SHA-256: `bc20f28a3fdb2f4630b586ac8b51d5c6aef814b5fc84526c6759d6ad13a1f782`.

### Evidence boundary
- This is synthetic software concordance, not experimental structure validation. Real licensed structures, mmCIF semantics, SASA/interaction concordance, viewer and device benchmarks remain open.
- R5 and the overall R track remain in progress; no S/I/P/G track work is started.


## 2026-11-09 — Session 45: Correct R3 diagnostics inventory

### Reviewed
- Audited `fit_michaelis_menten`, `bootstrap_michaelis_menten` and their regression tests against the R3 exit criteria and roadmap statements.

### Corrected
- Updated the R3 plan to accurately record existing Gaussian-iid AIC/BIC, standardized residuals, leverage, Cook's distance, Durbin–Watson, residual sign runs, local Jacobian covariance/standard errors and identifiability condition-number output.
- Kept the critical distinction: these are implemented, regression-tested descriptive diagnostics, not independently validated model-selection or uncertainty methods.

### Still open
- Independent experimental/reference datasets, unit validation, predeclared identifiability thresholds, uncertainty coverage simulations, broader model comparisons and Android device/runtime evidence.


## 2026-11-09 — Session 46: Correct R1 feasibility and privacy status

### Reviewed
- Re-read the R1 exit criteria, Android feasibility record, current CI workflow and privacy statement against the current repository source and CI history.
- Found stale text that described the application as a minimal feasibility shell and stated SciPy was absent without distinguishing host validation from Android runtime availability.

### Corrected
- Updated `docs/android-feasibility.md` to identify the current Android app/build lane, latest exact-source CI #2111 state, and explicit device/runtime boundaries.
- Clarified that host-only SciPy comparisons do not prove Android SciPy packaging.
- Updated `PRIVACY.md` to describe the current Research Mode prototype while retaining the explicit absence of an independent privacy assessment, patient workflow, account service, telemetry and remote compute.
- Updated the roadmap's R4 evidence wording to include the migration and imported-FASTA regression baseline without claiming on-device completion.

### Verification boundary
- CI #2111 was still running its Android arm64 build/package/JVM job when this record was prepared. Its other four jobs had passed. No final pass is recorded here.
- No emulator/physical-device test, Moto G54 5G execution, independent privacy review or release approval is claimed.

### Next
- Confirm CI #2111's Android job outcome; continue R-track gaps only. R1–R10 remain open until their individual exit evidence and owner gates are satisfied.


## 2026-11-09 — Session 47: Add imported FASTA worker guard tests

### Reviewed
- Re-read the imported FASTA worker and its dispatch bounds before expanding the Android test surface.
- Confirmed the worker rejects invalid job identifiers before store access, checks the committed byte count before materializing plaintext, and rejects FASTQ before starting the embedded Python runtime.

### Implemented
- Added the pinned WorkManager testing dependency for JVM/Robolectric tests.
- Added tests for missing/malformed IDs, unknown jobs, an oversized committed input rejected before plaintext materialization, and FASTQ rejection pending an explicit Phred offset.
- Updated the R2 plan and roadmap with the exact coverage and its limitations.

### Verification boundary
- Tests are newly authored and are not counted as passing until the exact-source Android CI job completes.
- They do not establish WorkManager process-death/retry/cancellation semantics, on-device Chaquopy execution or SAF provider behavior.

### Next
- Verify exact-source CI, then extend deterministic lifecycle coverage where it can be meaningfully exercised without pretending a JVM test is a device test.


## 2026-11-09 — Session 48: Harden PharmVar TSV ingestion

### Implemented
- PharmVar TSV header validation now rejects empty or duplicate normalized column names and requires exactly the documented nine columns.
- Each data row must contain exactly nine fields; short and extra-field rows fail closed.
- Added tests for ambiguous exact allele matches, phase/completeness abstention and reference-accession mismatch.

### Verification boundary
- The tests are newly authored; exact-source CI is pending. No biological validation, licensed reference dataset import or clinical PGx capability is claimed.

### Next
- Confirm CI and continue the R9/R10 validation gates. R remains open.


## 2026-11-09 — Session 49: Expand phylogenetic edge-case coverage

- Added two-taxon neighbour-joining distance preservation, asymmetric/non-zero diagonal rejection and deterministic tie-resolution regression tests.
- Updated the R7 plan/roadmap to distinguish these deterministic software tests from missing published biological tree references and scale benchmarks.
- Tests await exact-source CI; R7 remains exploratory and R remains open.


## 2026-11-09 — Session 50: Reconcile superseded parallel-track instructions

### Audit finding
- The current decision log correctly records D-019 as superseding D-009 parallel sequencing, but the top-level ROADMAP sequencing gate and historical parallel execution protocol still instructed parallel S/R/I/P work.
- Those stale instructions contradicted the owner's latest explicit order and could cause an assistant or contributor to start S before the R gate.

### Corrected
- Replaced the active ROADMAP sequencing gate with D-019's strict R → S → I → P → G order and two-step-per-track rule.
- Reworded the former parallel permission as historical/superseded.
- Marked docs/parallel-track-execution.md as archived historical guidance and explicitly prohibited using its parallel lanes as current instructions.

### Verification boundary
- Documentation consistency correction only; no phase completion or exit approval is implied.


## 2026-11-09 — Session 51: Diagnose and repair first worker/PharmVar test failures

### Exact-source findings
- CI #2114 failed two new Android worker tests because their fixtures updated state/hash/byte count but omitted storage_path; the production query correctly classifies those rows as not fully committed. Fixed the fixtures to seed the metadata required to reach the byte-limit and FASTQ preflight checks without attempting decryption.
- CI #2117's Python job reported 235 passed, 4 skipped and one failed. The implementation correctly raised the duplicate-normalized-header error; the test expected the later nine-column error. Corrected the assertion to expect the actual duplicate-header rejection.

### Verification boundary
- These are test-fixture/assertion corrections, not production behavior changes.
- Corrected exact-source CI #2121 and later are required before counting these tests as passed.
- No device runtime, Keystore or encrypted-import end-to-end result is claimed.


## 2026-11-09 — Session 51: Reconcile R1/R7/R8 status against current implementation

- Updated R1 feasibility status to the exact current CI #2122 source/run and removed stale parallel-track authorization language; D-019 is the active sequencing decision.
- Corrected R7 plan scope to include implemented JC69 distance estimation and seeded site-column bootstrap, while retaining the explicit absence of likelihood/Bayesian inference and a viewer.
- Corrected R8 plan scope to include the exploratory NB2 count GLM and numeric covariates, while documenting missing dispersion moderation, repeated-measures and robust inference.
- Updated the Android feasibility record to distinguish passed host/Python/RDKit/SPDX jobs from the still-running Android job.
- No phase exit is declared. R1 device/runtime feasibility and scientific validation remain open.


## 2026-11-09 — Session 52: Harden NCBI Gene catalogue parsing

- Changed gene_info row-width validation to require exactly 16 fields; extra fields are no longer silently discarded.
- Validated modification dates as real YYYYMMDD calendar dates.
- Added regression tests for appended columns and impossible dates.
- Exact-source CI required before counting the tests as passed. No comprehensive NCBI release import or PGx clinical validation is implied.


## 2026-11-09 — Session 53: Close encrypted import worker resources reliably

- Moved import staging-directory creation, legacy plaintext cleanup and initial state update into the worker's guarded execution block.
- Added a finally block that closes the SQLite helper after success, cancellation and all failure returns, including failed legacy plaintext cleanup.
- Exact-source Android CI is required; no process-death or physical-device lifecycle claim is made.


## 2026-11-09 — Session 54: Begin sequential Track S implementation step 1
**Phase:** Track S / Step 1 — documented base implementation  
**Objective:** Start S after the R host-audit closure and documentation consolidation, following D-019 and owner decision D-020.

### Done
- Reviewed the S roadmap, offline structure-viewer contract and unknown-sequence evidence contract before changing code.
- Inspected the existing S1 structure-payload validator, S6 local exact-reference and FASTA pack loader, S7 bounded ORF enumeration, S8 explicit translation tables and S9 conservative sequence-to-structure mapping.
- Hardened S6 local FASTA pack resource-limit validation: byte, manifest, record and residue limits must be positive integers; booleans and floats are rejected.
- Added regression coverage for all four resource-limit parameters.
- Kept S1 rendering gated on R1 WebView feasibility, exact viewer/transitive-license review and device evidence. No unsupported homology, novelty, gene-function or genetic-code inference is introduced.

### Validation boundary
- Exact-source CI for this increment is required before treating the new tests as passed.
- Existing S tests and host reference fixtures remain regression/conformance evidence, not independent biological validation.
- R device, external-science, licensing and release evidence remains carried forward; no R validation claim is implied.

### Next step
Run exact-source CI, inspect the S6 changes and continue the S1/S6–S9 documented base work without crossing S2–S5/S10 gates.


## 2026-11-09 — Session 55: S6 reference-pack file-boundary hardening
- Opened FASTA and manifest inputs through regular-file descriptors, using no-follow flags where supported.
- Enforced FASTA byte ceilings during streaming hash, closing the growth-after-stat resource-boundary gap.
- Added tests for manifest symlinks, oversized manifests and streaming byte limits.
- Exact-source CI is required before this increment is considered regression-tested.


## 2026-11-09 — Session 56: S1 structure-payload byte ceiling
- Added a 32 MiB default serialized UTF-8 payload ceiling to the deterministic structure-view preparation/validation/serialization boundary, in addition to the 200,000-atom ceiling.
- Added regression tests for oversized payloads and invalid byte-limit types/values.
- Updated the S1 contract and S roadmap. This remains payload preparation only; no renderer or WebView bridge is claimed.
- Exact-source CI required.


## 2026-11-09 — Session 57: S2 bounded structure geometry metrics
- Added a conservative S2 geometry report: atom/residue counts, assessed/unknown element counts, spatially indexed steric-overlap candidates and severe-overlap count.
- Added explicit atom and candidate-pair ceilings and strict parameter validation.
- The report always returns `quality_badge=not_assessed`; it does not claim MolProbity, Ramachandran, rotamer, resolution/R-free or pLDDT/PAE quality.
- Added synthetic regression fixtures and a dedicated S2 contract documenting the evidence still required for a calibrated quality badge.
- Exact-source CI required.


## 2026-11-09 — Session 58: S3 conservative variant coordinate mapping
- Added protein substitution-to-structure mapping over the existing exact, unique, contiguous chain correspondence primitive.
- Enforced reference-residue agreement and explicit abstention for ambiguous, noncontiguous, missing or uncovered structure mappings.
- Output is coordinate correspondence only; no mutation effect, stability, pathogenicity or clinical interpretation is claimed.
- Added positive, abstention and invalid-input regression tests; exact-source CI required.


## 2026-11-09 — Session 59: S3 inter-chain contact evidence
- Added a bounded spatial-neighbour implementation for heavy-atom contacts between two selected chains.
- Reports residue-pair contact counts and minimum distances; hydrogen atoms are excluded.
- Explicitly avoids affinity, energy, pocket or functional-effect claims.
- Added synthetic contact and resource-limit regression fixtures; exact-source CI required.


## 2026-11-09 — Session 60: S5 deterministic session export foundation
- Added a byte-bounded, deterministic JSON structure-session export containing the validated coordinate payload and preparation provenance.
- Export explicitly records `render_state=not_rendered` and discloses the absence of PNG/SVG/interactive viewer state.
- Added determinism, provenance and export-size regression tests; exact-source CI required.


## 2026-11-09 — Session 61: S4 prediction evidence and comparison boundary
- Added strict provenance/confidence envelope validation for externally supplied structure-prediction results.
- Added exact residue-key superposed CA RMSD comparison for predicted versus experimental coordinates.
- Outputs remain unverified; no prediction model, node transport/authentication, license approval, confidence calibration or biological accuracy claim is implemented.
- Added synthetic regression tests and documented S4 external dependencies.


## 2026-11-09 — Session 62: S7 bounded contig assembly QC
- Added streaming contig-level assembly summary metrics: N50/L50, length distribution endpoints, GC, ambiguity and N counts.
- Added unique-ID, IUPAC DNA and record/base resource-limit checks.
- Explicitly does not claim assembly completeness, contamination screening or gene annotation.
- Added synthetic regression tests; exact-source CI required.


## 2026-11-09 — Session 63: S8 genetic-code selector validation
- Hardened genetic-code and ORF entry points to accept only integer NCBI table identifiers, explicitly rejecting booleans/floats/strings.
- Added regression cases for both APIs. No genetic-code inference is implemented.
- Exact-source CI required.


## 2026-11-09 — Session 64: S1 Android viewer handoff, S5 SAF export and S7 bounded candidate work

### Done
- Integrated Android SAF PDB/ENT/CIF/mmCIF import with bounded 16 MiB reads, strict UTF-8 decoding and the Python structure parser/provenance path.
- Integrated the dependency-free renderer through a packaged local WebView asset origin with network, file/content access and mixed-content restrictions; navigation is constrained and no generic JavaScript bridge is exposed.
- Added Android SAF JSON session export through `CreateDocument`; it exports the validated payload and provenance and explicitly remains `not_rendered`.
- Added the S7 six-frame ORF candidate-evaluation ceiling (1,000,000 total) and a nested-start regression test; documented the 24 explicitly supported S8 translation tables and exclusion of context-dependent table 31.
- Corrected the S audit matrix to distinguish completed Android integration from still-open physical-device, PNG/SVG and persisted-view-state work.

### Validation and limits
- CI #2200 and #2201 passed all five jobs on their exact commits.
- CI #2202 passed Python foundation/registry/tests, scientific-reference, RDKit and SPDX jobs; Android arm64 packaging remained in progress at this log update.
- CI #2204 on the audit/test commit was pending; the nested-start test is not counted as CI-verified until that exact run passes.
- No physical Android device, screenshots, accessibility audit, memory/latency benchmark, PNG/SVG renderer, biological annotation truth set, licensed prediction model or wet-lab validation is available here.

### Next step
- Verify CI #2202 Android packaging and CI #2204 exact-source regression suite; continue closing implementable S1–S10 software gaps while retaining external validation gates.


## 2026-11-10 — Owner decision D-021 and S5 PNG increment

### Owner-approved scope
- Owner approved deferring independent biological/experimental validation, curated truth sets/calibration, licensed reference datasets and prediction models/weights/secure inference infrastructure, and physical-device verification as explicit carry-forward deliverables.
- All unvalidated capabilities remain disabled and labelled unverified.
- This approval does not waive missing software implementation. S4 prediction-engine integration, S6 homology/profile-HMM workflows, S7 prokaryotic/eukaryotic genome annotation, and S9 family/domain workflows remain open. S10 candidate generation remains disabled.
- Track I remains blocked until the implementable S software scope is completed and audited.

### S5 implementation
- Added Android SAF PNG snapshot export with a 16-megapixel pixel-count bound.
- Added active WebView reference refresh and cleanup for viewer replacement/disposal, plus a source-contract regression test.
- Commit `e1afc18` added the export; `39e6eaf` tightened lifecycle handling and test coverage.
- CI for `39e6eaf` was queued at this log update; no pass is claimed until exact-source CI completes.

### Deferred validation
- Device screenshots, import/export on physical hardware, accessibility, memory/latency benchmarks, experimental structure concordance, licensed biological reference packs, model licensing and wet-lab evidence remain explicitly deferred.


## 2026-11-10 — Owner decision D-022: full S software implementation authorization

- Owner explicitly authorized full implementation of the remaining S-track software scope, including S4, S6, S7 and S9, and completion of the S1–S10 software audit.
- Continue implementing without asking for repeated permission for ordinary repository code, tests, documentation, capability registration and integration work.
- D-022 does not waive D-021's external gates: licensed model/data acquisition, independent biological/experimental validation, physical-device verification and any required secure inference infrastructure must remain honestly tracked until actually available and verified.
- Unvalidated capabilities stay disabled or clearly marked unverified. Do not fabricate model weights, reference packs, test results, external credentials or device evidence.
- Track I remains blocked until the implementable S software scope is complete and the exact-source audit passes.


## 2026-11-10 — Session 65: S4/S6/S7/S9 local execution and evidence pipelines

### Implemented
- S4: hash-pinned local prediction-process protocol with bounded JSON I/O, executable and weights SHA-256 verification, provenance matching and strict prediction-envelope validation.
- S6: local HMMER profile pressing/search against a complete source-plus-four-index pressed pack; bounded local BLASTP against hash-manifested protein databases; existing FASTA packs, exact search, Smith–Waterman and motif scanning remain integrated.
- S7: genome-wide aggregate-budget ORF candidate scanning; pinned Prodigal prokaryotic and AUGUSTUS eukaryotic runners; generic local GFF3 annotator protocol; supplied GFF3 transcript/CDS reconstruction and coordinate validation.
- S9: bounded HMMER domain-evidence parsing and caller-thresholded candidate ranking/abstention. No functional assignment is made.
- Regenerated the Android capability catalogue from the canonical registry and updated the S-track audit/roadmap.

### Exact-source verification
- CI #2275, run `42738823000`, exact commit `a05339e8fb2afbd0d12093972dcff81c68399b9b`: **5/5 jobs passed**.
- Python strict typing, Ruff, registry/catalogue reproducibility and the full unit-test suite passed.
- Android arm64 APK/AAB packaging, alignment, JVM tests and artifact/hash checks passed.
- Scientific reference fixtures, RDKit sanity fixtures and SPDX inventory passed.

### Boundaries and remaining work
- S4 model/runtime/weights and secure inference infrastructure remain external D-021 gates.
- S6 BLAST+/HMMER binaries and curated/licensed local reference databases are caller-supplied; homology evidence is not calibrated or a functional verdict.
- S7 Prodigal/AUGUSTUS binaries and species models are caller-supplied; syntax/coordinate checks do not establish biological accuracy.
- S9 profile databases and independent family/domain concordance remain external gates.
- S1/S5 SVG export and persisted interactive view state, S3 pocket candidates and S8 translation-table inference remain software gaps; S2 calibration and physical-device evidence also remain open. Track S is **not closed** and Track I remains blocked.


## 2026-11-11 — Session 66: Reconcile current S1–S10 source audit

### Reviewed
- Re-read NORTH_STAR, ROADMAP, DECISIONS, SESSION_LOG, the S discovery roadmap, the integrated research-platform inventory and the S implementation audit.
- Inspected default-branch head `ec3178e09192011d9b96d5a355a07dbd731a2d35`, its S5 source-contract test diff, and source-search results for S1/S5 viewer state/export, S2 geometry, S3 pocket analysis, S4 prediction protocol, S6–S9 workflows and S10 design boundary.

### Confirmed
- S1 now has SAF structure import, offline renderer integration, provenance, JSON session export and bounded PNG/SVG export; viewer state is serializable.
- S5 now includes SVG snapshot export and persisted interactive viewer-state serialization. This supersedes the earlier Session 65 statement that SVG/state remained absent.
- S4/S6/S7/S9 software adapters are present as recorded in the current roadmap and Session 65.
- S2 remains limited to bounded clash/torsion metrics without calibrated quality classification.
- S3 pocket-candidate analysis and S8 organism-specific candidate genetic-code inference remain software gaps.
- S10 generation remains disabled; only non-generative brief validation is implemented.

### Verification boundary
- CI #2275 passed all five jobs on exact commit `a05339e8fb2afbd0d12093972dcff81c68399b9b`.
- Current reviewed head `ec3178e09192011d9b96d5a355a07dbd731a2d35` is later than that CI checkpoint. No exact-head passing CI was established in this session.
- No repository test suite or Android build was executed in this session; no physical-device or independent biological validation is claimed.

### Disposition / next step
- Track S remains open and Track I remains blocked.
- Next implement S3 pocket-candidate analysis and S8 candidate genetic-code inference as bounded, provenance-bearing, abstention-first software; do not claim biological validity without independent truth sets.
- Reconcile the capability registry, generated Android catalogue, tests, roadmap, README and session log after those increments, then verify exact-head CI before any S exit decision.


## 2026-11-11 — Session 67: S3 ligand-site candidates and S8 genetic-code candidate ranking

- Added `python/kinetics/structure_pockets.py` with explicit-ligand, bounded spatial-index screening of nearby canonical protein residues. The result is labelled ligand-proximal geometric site candidates only; it does not detect apo cavities or estimate affinity/function.
- Added `tests/test_structure_pockets.py` for contact aggregation, missing-ligand abstention, non-finite coordinates and resource-limit rejection.
- Added `python/kinetics/genetic_code_inference.py` with bounded ranking across supported NCBI tables from supplied coding-frame internal-stop evidence and optional complete-CDS start/terminal-stop evidence. It enforces record/base limits and abstains for insufficient evidence or a small best-vs-runner-up margin.
- Added `tests/test_genetic_code_inference.py` for candidate ranking, low-evidence/tie abstention, malformed inputs and limits.
- Registered both capabilities in `capabilities/registry.yaml`; updated README, ROADMAP, S-track audit, discovery roadmap and evidence contract.
- Source/test commits: `a81802e7793400533953590491d59cb738466af1`, `0896335ea4334daa6fa7144e7bfbc010d350c6d7`, `5caf102efa314aa6fbe79c2417272697515d245b`, `806cde0ced16f2285b4c39300b87ce366bd5834b`, `e43a2b328de4c5a260671958f079bc33f285e591`, `cb07ad0b451455999c76e81637b92aa228d7d020`, `b9ef7468bba0bec8ce5f66634588c713ec197877`.
- Documentation commits: `02348f4559ac914075eaccecc74c510e30827dbc`, `a19988ae00668e3dfa8e35a20fc606e3af80c890`, `5845bb7506f419bec1c2d97d337843bda4ee9840`, `3d5ee4b5f5ac9d0cf705e2f03a34e533efe08c75`, `3ca26a89fea51f07b578b7b700c6b9b7b9208c52`.
- No local Python/Android test runner is exposed in this session. Exact-head CI must be inspected before reporting these tests as passed. Biological validation, calibrated code assignment, apo-pocket detection and complete chemical-component handling remain open. Track S is not closed; Track I remains blocked.


### Session 67 follow-up — conservative-input review

- Tightened S3 selection so a canonical amino-acid residue cannot be passed as the ligand selector; the selected ligand must be an explicitly identified noncanonical residue in the parsed atom stream.
- Tightened S8 evidence independence: duplicate record IDs and identical normalized coding sequences are rejected rather than counted repeatedly, and at least two supported tables are required for comparative ranking.
- Added regression tests for the S3 protein-as-ligand rejection and S8 duplicate-sequence/single-candidate rejection.
- Follow-up commits: `fdaf37e40c6e76fb5523e40dd1c210bfc436e21e`, `d08cd5e0f3262696cf405c57ac722b37a5265830`, `aaae933eccad6c0106c43d1c8b5b6a94f0cd695a`, `0836788b4a5bd942017a9e2949534214bdd9cde9`, `2b1b21e5536272ccb5929f18228c87e59be9dc21`, `d4538a94f4002bc4db6e298d600212a6884e8167`.
- Exact-head CI is required before treating the new tests as passed. S3 remains limited to ligand-bound geometric site candidates; S8 remains a heuristic candidate ranking only.

- Exposed both new candidate functions from the public `kinetics` package API and changed their tests to import through that public surface, covering package-level integration.
- Public API/test commits: `38139c9e41ef874e5afe6dca0253cbe44f98fdb3`, `8580ac459560d69e0c701ec208f7c1c9d7259854`, `16d962b5c0169e28dfb6705ca5f94ed706cdb0d5`.

- First GitHub Actions validation reached Ruff successfully but mypy identified eight strict-typing errors in the new dictionary accumulators/ranking keys. Replaced unsafe object conversions with explicit typed casts in the two implementation modules. This is a code fix, not a passing-test claim; the latest exact-head workflow must rerun.
- Strict-typing fix commits: `cfc8e2c01be0df9053ac2e086554f66d07587c01`, `3e82b0d06d5b2c1641491b32532f1e71ed1ff681`.

- Updated the README S8 row to distinguish the new heuristic candidate-ranking software from the still-open organism-specific truth-set and calibration gates.


## 2026-11-11 — Session 68: S3 apo-site screening and S8 candidate-boundary hardening

### S3
- Added `python/kinetics/apo_pockets.py`: bounded probe-grid candidate screening using small- and large-probe accessibility, spatial buckets, protein-model-bound filtering and hard atom/grid/distance/component ceilings.
- Exposed `apo_pocket_candidates` through the public Python API, registered `structure.apo_pocket_candidates`, and regenerated the Android capability catalogue.
- Added a synthetic open-cavity fixture, single-atom abstention, and grid/distance-budget tests. The result is coarse concavity evidence only; it does not estimate affinity, ligandability, function or druggability.

### S8
- Bounded candidate-table iterable materialization to the supported table count, bounded raw per-record sequence size before normalization, and rejected complete-CDS records that cannot contain distinct start and terminal codons.
- Corrected the tied-score fixture to use distinct normalized coding sequences, so it tests a real score tie without violating the independent-evidence rule.
- Added tests for infinite table iterables and complete-CDS minimum length.

### Integration and verification
- Fixed stale Android catalogue after adding S3/S8 registry entries.
- Added a true S3 candidate-pair overflow test.
- Updated README, ROADMAP, S discovery roadmap and S implementation audit.
- The previous workflow failed at catalogue reproducibility before unit tests. The exact-head CI for the final documentation/source commit must pass before any test or APK pass is claimed.
- Current disposition: S3/S8 software work is implemented but not yet CI-verified. Track S remains open; Track I remains blocked until exact-source CI and final S1–S10 audit pass. D-021 external validation/resource/device items remain deferred, not completed.


## 2026-11-11 — Session 69: final Track S software exit audit

- Re-polled exact-head workflow run 42954316831 for `77ddd0f934eb8712818af1cdf8c297140d35289b`: all jobs succeeded, including Python foundation/registry/tests, scientific reference, RDKit, SPDX and Android arm64 build/package tests.
- Python suite: 440 passed, 4 skipped (optional RDKit/pysam dependency coverage unavailable in the Python job). Ruff, strict mypy, registry/catalogue reproducibility, scientific-reference and SPDX checks passed.
- Android arm64 debug APK/AAB build, package alignment, JVM test task, artifact/hash verification and upload all passed. GitHub Actions artifact bundle is available from run 42954316831.
- Completed S1–S10 software-scope reconciliation in `docs/track-s/audit-2026-11-09.md` and updated roadmap/README. S3 apo-concavity candidate screening and S8 candidate ranking are part of this exact-head result.
- **Decision: Track S software scope CLOSED; Track I is the next engineering track.** D-021 independent scientific/experimental validation, licensed resources/models, secure inference infrastructure and physical-device verification remain explicit carry-forward obligations. S2 has no calibrated quality grade; S3/S8 outputs are heuristic candidates; S10 generation remains disabled. No scientific, clinical or release readiness is claimed.


## 2026-11-11 — Session 70: I1 chemistry descriptor hardening
**Phase:** Track I / I1
**Objective:** Start I in roadmap order by hardening the existing host-only RDKit chemistry adapter and its pinned reference checks.

- Added strict UTF-8 byte ceilings (1 MiB SMILES, 10 MiB mol block), embedded-NUL rejection and invalid-Unicode rejection before RDKit parser calls.
- Hardened Morgan Tanimoto parameter validation against booleans/non-integers and applied input byte limits to both operands.
- Versioned the descriptor output schema to v2; added formal charge, heavy/aromatic atom counts, aliphatic/aromatic ring counts and fraction Csp3, with explicit units/assumptions and finite-number checks.
- Expanded ethanol/benzene pinned sanity fixtures and validation assertions; added optional RDKit tests for extended descriptors and adversarial input bounds.
- RDKit remains a host-only optional dependency; Android integration is not claimed. Docking, MD and ADMET remain behind their documented engine/license/data/validation gates.
- Exact-head CI for the final I1 source revision is pending. No tests are claimed passed in this session until that workflow completes.


### I1 follow-up — Rule-of-Five heuristic

- Added an explicit four-criterion Rule-of-Five physicochemical screen to the RDKit descriptor payload, including observed values, thresholds and per-criterion pass/fail.
- The payload explicitly states this is not an absorption, bioavailability, safety, efficacy or clinical-suitability prediction.
- Added optional RDKit unit coverage and pinned ethanol/benzene reference-run assertions for the screen.
- The earlier exact-head workflow attempt exposed one test-name lint violation and the then-current descriptor code exposed an unavailable RDKit API call; both were corrected. A fresh exact-head workflow is required before claiming the fixes pass.


## 2026-11-11 — Session 71: I-track engineering foundations
**Phase:** Track I / I1–I5
**Objective:** Advance all software work that can be responsibly completed without claiming external engine, data, licensing or scientific-validation gates.

- I1: added an Android SAF SDF/MOL import and graph-only preview card, Chaquopy runner and Python bridge. Input is bounded to 16 MiB, strict UTF-8 and NUL checks are applied, one molecule record is required, and source SHA-256 is reported. Added regression tests for the Python graph core and Android integration contract.
- I2/I3: added `api/insilico-job.schema.json` with strict docking and MD request variants. It records source hashes, preparation, search-box/protocol, force-field and seed metadata. Both variants hard-code execution disabled and licence review pending; no docking or MD engine is executed.
- I4: added `python/kinetics/pkpd.py` with a first-order single-dose one-compartment oral PK reference equation and Emax relationship, explicit units, bounded series and strong non-clinical limitations. Added unit tests and package exports. No ADMET model or dose recommendation is claimed.
- I5: added seeded synthetic aggregate Hardy-Weinberg genotype-count generation, a strict JSON result schema and tests. No individual-level data, ancestry labels, phenotype or variant-effect prediction is produced.
- Added strict schema tests for I2/I3 and I5; updated roadmap and research boundaries.

**Validation:** The preceding I1-only combined source revision `e5888232cd0f58c48c3a000aca260f31b551937b` passed its exact-head workflow, including Python tests, pinned RDKit and scientific-reference checks, SPDX generation, arm64 APK/AAB build, JVM tests and artifact verification. This does not validate the later I1–I5 changes in this session. The combined I1–I5 source revision requires a fresh exact-head CI run; no pass is claimed until it completes.

**Remaining external gates:** approved docking/MD engines and licences, secure compute, independent redocking and MD reference benchmarks, licensed/curated ADMET datasets and externally validated models, population/fairness-reviewed public cohorts and variant-effect validation, physical-device verification, and all relevant scientific acceptance evidence. P0 remains blocked; no patient or clinical workflows are enabled.

- Follow-up: added `api/insilico-result.schema.json` for docking poses and replicated MD energy/trajectory outputs. Both require input/protocol/build hashes and `validation_status: not_independently_validated`; regression tests reject a fabricated validated status.


## 2026-11-11 — Session 72: I-track engine adapters and private worker
**Phase:** Track I / I1–I5
**Owner authorization:** The owner explicitly authorized all I-track implementation and gave permission to complete the track. This authorizes engineering work; it does not substitute for source-specific licence terms, secure-node deployment, experimental evidence or independent scientific validation.

- **I2 docking:** added python/kinetics/docking_vina.py, pinned AutoDock Vina 1.2.7, bounded prepared-PDBQT inputs, seeded search, score components, per-pose output, and SHA-256 provenance for inputs, engine binary, protocol and poses. Added an upstream-pinned 1IEP fixture and a deterministic Vina engine smoke workflow. This is engine smoke only, not redocking/cross-docking or decoy-enrichment validation.
- **I2 Node:** added remote-node/server.mjs, Node 22 package/tests, a schema-validated Python worker entry point and execution request schema. The worker defaults to loopback and disabled, requires a long bearer token when enabled, requires TLS for non-loopback binding, limits concurrency/body/output/time and passes an allow-listed environment to Python. It has not been deployed to a project node. MD remains disabled at this service boundary.
- **I3 MD:** added python/kinetics/md_openmm.py, pinned OpenMM 8.6.1 CPU execution, trusted preconstructed System/Topology boundary, independent seeded replicas, DCD artifacts, finite-state checks and engine/protocol/input provenance. CI smoke uses a synthetic two-particle harmonic system only; no biomolecular force field is selected or claimed validated.
- **I4 PK/PD:** added the continuous equal-rate limit to the one-compartment oral PK equation and a pinned SciPy DOP853 numerical ODE comparison covering equal and unequal absorption/elimination rates. Expanded the metadata-only ADMET candidate inventory to FDA DILIrank 2.0 and added an automated validator; acquired data entries remain empty.
- **I5:** added synthetic additive genotype-to-trait effect simulation with caller-supplied effects and aggregate genotype-stratified summaries only. Added a strict schema and tests. This is not a variant-effect prediction model.
- Updated engine selection/licence notes, source catalogue, research boundaries, roadmap and README.

**Validation evidence:** On source revision e7b314df67ae83fec2164a6911c78311b54784f2, the Vina 1.2.7 engine smoke, OpenMM 8.6.1 CPU synthetic replica smoke, pinned RDKit reference, SciPy scientific references, SPDX inventory and Android APK/AAB + JVM build all passed. The Python job on that same revision failed at mypy due two integration annotations; these were corrected. A subsequent Node worker CI run exposed one test expectation (case-sensitive error text) and lint exposed formatting/exception chaining issues; these were corrected. The latest exact-head workflow must pass before the combined I1–I5 revision can be called CI-green.

**Remaining gates:** private Node worker deployment and host hardening; complete Vina/OpenMM transitive binary SBOM/provenance review; biomolecular force-field parameter selection and licence review; independent redocking/cross-docking/decoy enrichment; biomolecular MD convergence, energy and ensemble benchmarks; approved ADMET dataset releases and leakage-controlled external model validation; governed public cohorts, population/fairness and independent variant-effect validation; I1 physical-device and wider chemical reference verification. No patient data, clinical mode or dosing recommendations are enabled.


## 2026-11-11 — Session 72: I1–I5 engine integration and verification audit

- Re-audited the latest source and documentation after the I1–I5 foundations were expanded.
- I1: Android SAF SDF/MOL graph preview and host RDKit descriptor adapter remain separate by design; the exact I1 integration checkpoint `bbaabc52f7a81f1578cd3a871679330316591e18` passed Python, pinned RDKit, scientific-reference, SPDX, Android arm64 APK/AAB, JVM and artifact/hash jobs (workflow `42962948259`). This does not establish physical-device validation or Android RDKit support.
- I2: added pinned AutoDock Vina 1.2.7 host execution for caller-prepared PDBQT, bounded inputs/protocol, engine/input/pose hashes, strict result envelope, pinned 1IEP deterministic engine smoke and a disabled-by-default authenticated Node 22 docking worker. Smoke execution is not redocking RMSD, cross-docking or decoy enrichment. Worker deployment, complete transitive SBOM/provenance review and secure-node approval remain open.
- I3: added OpenMM 8.6.1 CPU-only execution for trusted constructed System/Topology/positions, independently seeded replicas, bounded DCD outputs and engine/input/protocol hashes. CI smoke uses a synthetic harmonic two-particle system only; no biomolecular force-field parameter set is selected or validated. Secure deployment and independent stability/energy convergence remain open.
- I4: added a pinned SciPy DOP853 ODE comparison for the closed-form one-compartment oral PK implementation; metadata-only ADMET sources remain unacquired and unapproved. No trained ADMET model, parameter fitting, dose guidance or PBPK validation is claimed.
- I5: added caller-supplied additive-effect simulation with aggregate genotype-stratified trait summaries; effects are inputs, not learned predictions. No individual records, ancestry, linkage, penetrance or clinical risk are produced.
- Updated README, ROADMAP and research-boundaries documentation to reflect the expanded software foundation and remaining gates.

**Verification status:** the combined I1–I5 workflow attempts following the I2/I3 additions were cancelled by subsequent rapid pushes before the final source revision could complete. The earlier I1 integration workflow passed, and the dedicated Vina/OpenMM smoke jobs have reported passing in intermediate revisions; neither result is an exact-head pass for the final combined source. A fresh stable-head workflow is required before claiming combined Python/lint/type/registry, Android, engine-smoke and artifact verification.

**I-track exit remains OPEN.** Remaining acceptance work: stable exact-head CI; physical Android device install/runtime and import checks; complete transitive engine SBOM/provenance and approved secure Node deployment; independently prepared docking redocking/cross-docking and decoy-enrichment benchmarks; licensed biomolecular force-field/parameter sources and independent MD stability/energy checks; curated licensed ADMET datasets and leakage-controlled external model validation; and public-cohort governance, fairness and independent variant-effect validation. P0 and all patient/clinical workflows remain blocked.


- **I4 evaluation increment:** added Bemis-Murcko scaffold-group splitting, binary ROC-AUC/average-precision/Brier/confusion-matrix/sensitivity/specificity and calibration summaries, plus Morgan/Tanimoto nearest-neighbour applicability-domain analysis. Inputs are bounded and RDKit version is recorded in structure-based outputs. A pinned RDKit CI smoke validates schemas and synthetic examples only; no ADMET data or predictive model is present.
- **I3 provenance increment:** MD outputs now include canonical coordinate and topology hashes, serialized System hash, CPU plugin/core binary hash, separate deterministic integrator and velocity seeds, and finite final-state checks. These strengthen reproducibility but do not replace force-field source verification or scientific MD validation.


## 2026-11-11 — Session 73: I1–I5 exact-head combined CI checkpoint

- Re-polled `main` and confirmed exact source SHA `026032962de7b8315cfbeaaa0e0d6c39aa0d4ef4` matched successful workflow [#42967649660](https://github.com/AssayFlux/Kinetics/actions/runs/42967649660).
- All 9 jobs passed: Python foundation/registry/tests; Android arm64 debug APK/AAB build and package tests; pinned RDKit descriptor fixtures; SPDX inventory; Vina engine smoke; private Node docking-worker security tests; OpenMM CPU replica smoke; ADMET utility smoke; pinned host scientific-reference comparisons.
- Python suite: 498 collected, 489 passed, 9 skipped; Ruff and strict mypy passed.
- Android `:app:testDebugUnitTest`, package verification and 16 KB native ELF alignment checks passed. APK 70,388,850 bytes (SHA-256 `b767656e1d39f1954da8b4d97d7409cb854ef41ce4ded0d17b62356ba42b81a0`); AAB 40,252,958 bytes (SHA-256 `1edbb63f5fc8f0969c8137f9edc7b4f9b775b5cea5c6fa8499fb04e83bd03a80`).
- Downloadable debug build artifact: [13832212511](https://github.com/AssayFlux/Kinetics/actions/runs/42967649660/artifacts/13832212511).
- Updated README, roadmap and CI evidence to distinguish this combined software-CI pass from I-track exit acceptance.
- **Disposition:** combined I1–I5 software CI checkpoint passed; I-track exit remains open pending remaining software integration/review and carry-forward device, licence, secure-node and independent scientific-validation gates. P0 and patient/clinical workflows remain blocked.


## 2026-11-11 — Session 74: I-track software closure audit

**Phase:** Track I / I1–I5 software exit audit  
**Objective:** Audit the latest exact main revision, close the implemented I-track software scope, and keep real scientific/device/licensing acceptance explicitly open.

### Audit and evidence
- Confirmed exact main SHA `aabe37808a5494acb2171b6ed71d2661b4dd2453` and exact-head GitHub Actions [workflow #42970328048](https://github.com/AssayFlux/Kinetics/actions/runs/42970328048).
- All **9/9 jobs passed**. Python suite: **490 passed, 9 skipped**; Ruff and strict mypy passed.
- Android arm64 debug APK/AAB packaging, package checks, JVM tests and 16 KB native alignment checks passed. Artifact bundle: [13832813087](https://github.com/AssayFlux/Kinetics/actions/runs/42970328048/artifacts/13832813087), 80,653,407 bytes.
- Pinned RDKit descriptor references, Vina engine smoke, OpenMM synthetic CPU replica smoke, ADMET utility smoke, host scientific-reference comparisons, Node docking-worker security tests and declared source SPDX inventory all passed.
- Reviewed I1–I5 implementation modules, request/result schemas, worker boundary, component tests and Android chemistry integration. The current software contracts and automated integration checks support closing the documented I1–I5 software scope.
- Corrected stale README/roadmap checkpoint references and added `docs/track-i-audit-2026-11-11.md`.

### Disposition
**I1–I5 software implementation and integration audit: CLOSED.**  
**Real scientific, physical-device, licensing, dataset/model, secure-node and owner acceptance: OPEN.**

This is not scientific validation or production readiness. Vina/OpenMM/ADMET smoke tests are not independent biological benchmarks; APK/AAB CI is not a physical-device run; source SPDX is not complete transitive binary/model/data licence approval.

### Next
Track P is next under R → S → I → P → G, but is not marked started in this session. P0 remains blocked; only public-data metadata and synthetic/non-patient preparation may proceed before P0. No patient data, clinical interpretation or Clinical Mode is enabled.


## 2026-11-11 — Session 75: Track P owner authorization and P0 preparation start

**Phase:** Track P / Step 1 — documented base  
**Objective:** Record owner authorization, open P-track engineering, and prepare P0 evidence without misrepresenting external approvals.

### Inspected
- Re-polled main: source SHA 3ce74d14f0e79f6c147f437db6e3bd28d44ef097.
- Exact-head GitHub Actions workflow [#42972264169](https://github.com/AssayFlux/Kinetics/actions/runs/42972264169) completed successfully; all 9/9 jobs passed (Python foundation/registry/tests, Android arm64 APK/AAB and package tests, RDKit, SPDX, Vina smoke, OpenMM smoke, ADMET utility smoke, Node worker security and host reference comparisons).
- Read ROADMAP, README, DECISIONS, public-data-only boundary, public dataset catalogue and documentation index.
- Confirmed candidate public-source catalogue remains metadata-only with entries: []; candidate sources are not approved for intake.
- Confirmed existing synthetic reference-build/contig/coordinate/digest contract and normalization tests are preparation foundations, not validated clinical interpretation.

### Owner decision
- Owner explicitly approved: “open p0 & build p track”.
- Recorded D-022: Track P starts; P0 evidence preparation and P1 public-data/synthetic base may proceed.
- Owner authorization is not external legal advice, ethics/IRB determination, clinical/scientific review, regulatory clearance or formal P0 gate passage.

### Changes prepared
- Added docs/track-p/p0-evidence-packet.md as a DRAFT evidence register, intended-use boundary, initial risk register and P0 exit checklist.
- Added docs/track-p/implementation-plan.md for P0/P1 Step 1 and Step 2, stack ownership, data boundary and phase exit criteria.
- Updated ROADMAP, README, DECISIONS, public-data boundary and docs index to show Track P started and P0 preparation active.

### Disposition and open work
- Track P Step 1: in progress; this commit establishes the documented base, not a completed P-track implementation.
- P0: formal gate remains BLOCKED / NOT APPROVED. External determinations/reviews and formal evidence are pending.
- P1: public metadata and synthetic-only work may proceed. Acquired dataset entries remain empty; no patient data or individual genotype interpretation.
- No patient/human-subject data, clinical recommendation, Clinical Mode, clinical validity claim or regulatory compliance claim is enabled.
- Exact-head CI for the new documentation commit must be checked separately. No tests are claimed for this documentation-only increment beyond the previously cited exact-head run.


## 2026-11-11 — Session 76: P1 public-catalogue contract alignment

**Phase:** Track P / P1 — public-data metadata foundation  
**Objective:** Close a schema/checker mismatch found during the P1 audit.

### Finding
The Python catalogue checker required a dataset licence URL and canonical kebab-case identifiers, while the JSON Schema did not fully enforce those same constraints. This allowed the declarative contract to be weaker than the runtime gate.

### Change
- Made dataset-entry license_url mandatory in the JSON Schema.
- Added canonical kebab-case patterns for acquired dataset IDs and candidate source IDs.
- Reworked catalogue tests to validate the committed YAML against JSON Schema Draft 2020-12 with URI/date-time format checks.
- Added negative schema cases for missing licence URL, patient_data=true, unknown properties and noncanonical candidate IDs.

### Verification
- Tests added; not yet executed in this environment. Exact-head CI is required before claiming a pass.
- This increment changes metadata validation only. It does not download or approve data and does not enable patient data or interpretation.


## 2026-11-11 — Session 77: P1 CI failure triage

- Exact-main workflow 42973850678 failed in the Python job's strict mypy step; all eight other jobs passed.
- Failure: `python/kinetics/genotype_qc.py:143` converted an untyped parser field with `int(object)`.
- Fix: explicitly validate chromosome text and positive integer position before constructing the aggregate record; this also fails closed on malformed parser output rather than coercing it.
- Fix is committed for exact-head CI verification; no test pass is claimed until that workflow completes.


## 2026-11-11 — Session 78: P1 synthetic genotype-QC audit hardening

**Phase:** Track P / P1 — Step 2 audit, test and fix  
**Base:** `28f26eeb3d1a617811111f5afede303eb024d672`

### Audit findings
- The first aggregate-only synthetic VCF QC implementation bounded input bytes, variant/sample counts, validated literal REF/ALT alleles and allele indexes, required one GT FORMAT field, rejected mixed phase separators, treated partial calls as missing, and emitted no sample identifiers or genotypes.
- The P1 plan explicitly requires unsupported ploidy to fail closed. The initial parser accepted haploid and polyploid calls without a chromosome/ploidy contract; that was an implementation gap.
- The exact-head CI workflow #42996550617 is still independently validating the preceding coordinate-type fix; this increment does not claim that run has completed.

### Changes
- Tightened synthetic genotype parsing to accept only diploid GT calls (including fully/partially missing diploid calls) and reject haploid/polyploid calls with an explicit error.
- Added negative fixtures for haploid, triploid and higher-ploidy calls.
- Updated P1 roadmap and implementation-plan status to reflect the actual QC foundation and remaining independent/exact-head gates.

### Boundaries
- This is synthetic-fixture software verification only. It is not an authoritative VCF implementation, genome build, PGx allele caller, clinical interpretation or scientific validation.
- Public dataset acquired entries remain empty; no patient/human-subject data or clinical workflow is enabled.
- P0 remains DRAFT / NOT APPROVED. P2–P7 remain not started pending their documented dependencies and approvals.

### Validation
- Tests are committed for CI; no local execution is claimed. The new exact-head workflow must pass before this increment is treated as verified.


## 2026-11-11 — Session 79: P0 internal control drafts and CI evidence reconciliation

### Verified evidence
- Exact-source workflow #42996550617 on 28f26eeb3d1a617811111f5afede303eb024d672 completed successfully: all 9 jobs passed.
- The Android job built arm64 debug APK/AAB, passed package alignment and JVM unit tests, and uploaded artifacts. CI explicitly did not run an emulator or physical device.
- Artifact measurements: APK 70,389,746 bytes, SHA-256 64de505b3636d12d2e7b85683413021dc44cf1fe1eb6aa9c9e6b0d5ebd84112c; AAB 40,259,732 bytes, SHA-256 30db5ec820e6b9f0465db176d552b10bb1a4f77098771b425a7bae3999ba380e.
- Exact-head workflow #42997277628 on 9532d2056d4e0eb7ffda7cd5d6c256ff7aadb71b: Python job passed 507 tests with 9 optional-dependency skips; full workflow still running at this log entry.

### P0 preparation
- Added docs/track-p/p0-controls-draft.md with engineering drafts for intended use, data governance, threat model, quality lifecycle, staged validation and stop-work/incident response.
- Linked the draft from the P0 evidence packet and documentation index.
- Corrected the escaped line break in the decision register so D-020 and D-022 are distinct rows.
- The new drafts do not represent legal/privacy advice, ethics determination, independent clinical/scientific review, QMS certification or formal P0 approval.

### Current gate status
- P0 remains BLOCKED / NOT APPROVED; external determinations and competent review remain outstanding.
- P1 remains in progress until the exact-head workflow for the synthetic ploidy guard completes and the remaining audit/reference requirements are assessed.
- P2–P7 remain not started; patient data, human-subject activity, individual PGx interpretation and Clinical Mode remain disabled.


## 2026-11-11 — Session 81: P2–P7 research-only foundations

### Starting evidence
- Commit e9faf7165ceeb2ee9af9ed08d663c32d0be10cda exact-head workflow #42998496868 passed 9/9 jobs.
- Python: 509 passed, 9 skipped.
- Android arm64 debug APK: 70,389,586 bytes; SHA-256 636476de0eab15b767815499d4220219f8953ff6e04f21dbb3f42b8903c76789.
- Android arm64 debug AAB: 40,260,318 bytes; SHA-256 a0cee244440b16f7af6ab9a55be4a1e3ad976f62520e41057269b7b99abe334b.
- JVM tests and package alignment passed; no physical-device runtime performed.

### Added
- Synthetic PGx and PharmVar regression tests for release/digest metadata, exact haplotype matching, accession/build mismatch, ambiguous definitions and abstention.
- P3 research-only guideline evidence schema; clinical decision support is prohibited by schema.
- P4 curation record schema; uncertain outcome and mandatory second review; autonomous final classification and clinical use prohibited.
- P6 risk/control and jurisdiction-review schemas; patient-data and Clinical Mode authorization hard-false.
- P5 ethics/adviser protocol template and P2–P7 workplan.
- Updated roadmap and documentation navigation.

### Gate status
- P0 remains BLOCKED / NOT APPROVED; external determinations and competent reviews are outstanding.
- P1 remains in progress pending independent reference concordance, source-term review, fuzz/resource audit and device workflow validation.
- P2–P7 are now in progress as research-only software foundations/templates, not completed operational or clinical phases.
- No public dataset payload has been acquired or approved. No patient/human-subject data, individual clinical interpretation, recommendations, Clinical Mode, prospective study or regulated deployment is enabled.
- Exact-head CI for the new commit is required before this increment is accepted.


## 2026-11-11 — Session 82: Track P exact-head audit and evidence reconciliation

**Phase:** Track P / Step 2 — audit, test and fix  
**Base:** aee8f1e3a73dfa5136ca2472877bd541727453db

### Verified
- Exact-head GitHub Actions workflow [#43002587271](https://github.com/AssayFlux/Kinetics/actions/runs/43002587271) completed successfully: all 9/9 jobs passed.
- Python: 522 passed, 9 skipped (optional RDKit/pysam unavailable in the Python foundation job); Ruff lint and strict mypy passed.
- Android arm64 debug APK: 70,389,802 bytes; SHA-256 `4cd8ce2e1f5e6874e39d589e853fdb801c9322c56461a19703653d031f5f9fb5`.
- Android arm64 debug AAB: 40,260,451 bytes; SHA-256 `90ce8bbfac2e6a17faf385bcffcee1ddcc179bde1ecc625ef93a5b25ff66bdc1`.
- 16 KB package alignment and Android JVM unit tests passed. CI explicitly did not run an emulator or physical-device test.
- Pinned host-side reference comparisons, OpenMM replica smoke, Vina engine smoke, RDKit descriptor and ADMET utility smoke, source SPDX inventory, and private Node worker security tests passed. These are not independent biological/clinical validation.
- Android artifacts were uploaded as workflow artifact `kinetics-android-arm64-debug-aee8f1e3a73dfa5136ca2472877bd541727453db` (artifact ID 13847730191).

### Fixes and audit
- Corrected lint defects in the new P-track schema/PharmVar tests; this exact-head run now passes the complete workflow.
- Reviewed P0 evidence packet, P0 control drafts, P1 boundary/implementation plan, P2–P7 workplan and decision register. Documents consistently preserve the NOT APPROVED gate and identify external evidence owners/requirements.

### Gate status
- P1/P2/P3/P4/P5/P6/P7 research-only engineering foundations and preparation now have exact-head software CI evidence for this increment. This does not mean their independent validation, licensing, human curation, ethics, risk-control verification or regulatory tasks are complete.
- P0 remains BLOCKED / NOT APPROVED. Required competent legal/regulatory and ethics determinations, qualified independent scientific/clinical review, approved privacy/security/QMS evidence, independent validation protocol, risk acceptance and formal P0 gate decision are not present in the repository.
- P1 authoritative reference concordance, exact-source terms review, fuzz/resource audit and device workflow validation remain open. No acquired public dataset is approved.
- No patient/human-subject data, individual PGx clinical interpretation, diagnosis/treatment/dosing recommendation, Clinical Mode, prospective study or regulated deployment is authorized.
- Debug APK/AAB build and CI success do not establish device runtime, scientific validity, clinical safety, regulatory clearance or production readiness.

### Disposition
Track P remains IN PROGRESS. The software audit increment is verified; external and operational exit criteria remain open. Do not mark P0–P7 or the overall Track P closed until their required evidence and approvals are actually recorded.


## 2026-11-12 — Track P parser resource-bound audit increment

- Audited the P1 synthetic VCF ingestion and P2 PGx definition/PharmVar parsing boundaries.
- Added default byte/record/variant ceilings to PGx JSON and PharmVar TSV parsers, plus fail-closed type/limit validation and synthetic regression tests.
- Updated the P2 workplan and roadmap to record the engineering increment and explicitly leave exact-head CI pending.
- No authoritative public data was downloaded or approved. No patient/human-subject data, individual clinical interpretation, clinical recommendation or Clinical Mode was enabled.
- P0 remains BLOCKED / NOT APPROVED. Independent reference concordance, exact-source terms review, fuzz/security assessment, operational curation/ethics, privacy/QMS, qualified jurisdiction advice and P7 regulatory/prospective evidence remain open.


## 2026-11-12 — P4/P6/P7 evidence-contract hardening

- P4 accepted-for-research curation records now require completed second review with reviewer role, timestamp and evidence URL; pending and escalated states remain explicit.
- P6 residual-risk acceptance now requires an accountable role, timestamp and evidence URL.
- P7 jurisdiction statuses indicating received advice or pending owner disposition now require advice evidence and a product-classification field.
- Added synthetic schema tests. These contracts do not constitute human curation, risk sign-off, legal advice or regulatory classification.
- Exact-head CI remains pending; all affected checks must pass before this increment is verified. P0 remains NOT APPROVED and clinical/patient workflows remain disabled.


- Additional P1/P2 audit: confirmed VCF record/sample limits are applied during parsing; added boolean-coordinate rejection for PharmVar typed records with negative tests. Exact-head CI and independent reference comparison remain pending.


## 2026-11-12 — Repository-wide documentation and structure audit

- Audited the complete GitHub recursive tree at `dafc3cad56bc6b9b9b49cc30f9e5f65bbd655c47`: 356 tracked files across 55 non-root directories; tree response was not truncated. Reviewed canonical direction files, README, docs index, architecture/integration standard, validation, security, licensing, CI evidence, Track P documents, citation metadata and session history.
- Added `docs/research-grade-readiness-audit-2026-11-12.md` with inventory, status/documentation drift, naming/layout issues, research-grade evidence requirements and a staged reorganisation plan.
- Updated `docs/README.md`, root README and ROADMAP to link the audit, align P2–P7 software-preparation status, and clearly state that latest parser/schema hardening still needs exact-head CI. Earlier green workflows are historical, not current-head verification.
- Identified case-distinct `Assets/` and `assets/` trees and a very large append-only session log. No mass moves or deletes were made: asset consolidation requires full reference/hash audit; historical session entries are preserved.
- No local build, test suite, Ruff, mypy, device test, independent scientific validation or external review was run as part of this documentation audit.
- Current status: documentation navigation and readiness audit improved; research-grade scientific validation and release readiness are not established. P0 remains BLOCKED / NOT APPROVED; patient/clinical workflows remain disabled.


## 2026-11-12 — D-023 adds Track U after Track G

- Owner directed that Track U be added after Track G in the sequential execution chain and that all governing documents be updated.
- Added D-023: current order is **R → S → I → P → G → U**, with the existing two-step base-build then audit/test/fix gate applied to every track.
- D-023 supersedes D-019 only as to the current track list/order. D-019 remains historical evidence for the earlier five-track order; the superseded parallel-track permission in D-009 remains inactive.
- Existing partial U0–U3 source and documentation are retained as pre-existing work, not erased or retroactively accepted. Further Track U implementation and its audit follow G's two-step gate; U4–U6 retain their documented dependencies and exit criteria.
- Updated NORTH_STAR, ROADMAP, README, CONTRIBUTING, engineering integration standard, docs index, archived parallel-work protocol, Track G plan/register and CHANGELOG to align with D-023.
- No track status, scientific validation, physical-device verification, license clearance, external approval or P0 status is changed by this sequencing decision. Patient/clinical workflows remain disabled.


## 2026-11-12 — README redesign and asset-root consolidation

- Rebuilt the root README as a concise project landing page: supplied organization/Kinetics GIFs, compact project snapshot, D-023 track order, scoped engineering-gate status, collapsible track details, coloured navigation badges and owner-supplied UI reference images.
- Defined the displayed percentages narrowly as documented engineering-gate closure; did not claim scientific, clinical, legal, regulatory or release compliance. P0 remains NOT APPROVED.
- Audited the two case-sensitive root directories. `Assets/Brand Logo.svg` and `assets/brand/brand-logo.svg` were the same Git blob; the remaining legacy assets were moved into `assets/brand/` and `assets/design-previews/` by reusing their original Git blob SHAs.
- Renamed the former `Assets/Kinetics.png` path to `assets/brand/kinetics-background.jpg` because its bytes are JPEG; no conversion or recompression was performed. The original Android background blob remains identical.
- Updated active brand and UI documentation. Historical decision/session records retain old path strings where they accurately describe past events.
- Consolidation commit: `300d2446b931bce947e870932077c666700cffb1`. README and documentation edits follow in this session.


## 2026-11-12 — Track G implementation increment 1
**Phase:** Track G / G0–G7 engineering controls  
**Objective:** Convert the initial governance plan into traceable repository controls while preserving external acceptance gates.

### Implemented
- Expanded the G0–G7 control/evidence register and requirements traceability.
- Added role/accountability and review-cadence model; unassigned roles are explicitly marked rather than invented.
- Consolidated the application-wide security threat model and retained UI-specific threats as a scoped supplement.
- Added a 16-case security verification matrix; device/fuzz/independent review results remain open.
- Added source-level data-flow and information-asset inventory based on the inspected Android manifest, build configuration and policies.
- Added dependency decision register and CI capture of resolved Gradle/Cargo dependency reports plus Maven artifact hashes; the checked-in SPDX generator remains a declared-source inventory, not a full release SBOM. Updated the third-party inventory and release checklist to state this limitation explicitly.
- Generated a 68-tool capability claims matrix with conservative wording; current registry entries do not become scientifically validated by implementation.
- Added publication integrity protocol, operational incident/rollback/access/recovery procedures, and an empty CAPA register.
- Added governance structural checker, capability matrix generator and pytest coverage; wired both checks into CI.
- Updated README, roadmap, documentation index, SECURITY.md and changelog to reflect active G work and corrected the stale R1–R10 security status.

### Validation status
- Repository writes were accepted by GitHub and the generated claims matrix contains 130 capability rows.
- Exact-head CI for the latest G revision is pending at the time of this entry. Earlier intermediate runs were cancelled as newer commits superseded them; they are not treated as test passes.
- No local execution, independent security review, legal/privacy determination, device audit, ethics decision, tabletop exercise, access review or recovery drill is claimed.

### Open / blockers
- Verify CI on the final exact head; fix all failures and rerun.
- Resolve Gradle/Cargo/Python/native dependency graph and exact artifact/license coverage; no third-party bundle approval is implied.
- Appoint qualified security, scientific, privacy, quality, data and release role-holders.
- Complete independent mobile security assessment and retest.
- Complete jurisdiction-specific privacy/legal review and applicable ethics determinations.
- Run synthetic-only incident, backup/recovery and access-review exercises; record evidence and CAPA.
- Establish independent scientific protocols/truth sets, subgroup/missingness reports and claim-level validation.
- Complete authorship/COI declarations and a reproducible literature/novelty review before any paper submission.

### Gate status
**G0–G7 engineering implementation is IN PROGRESS. Track G is not accepted or closed. P0 remains BLOCKED / NOT APPROVED. Track U remains gated after G under D-023.**


### Audit correction — capability matrix scope
The first generated claims CSV incorrectly included entries outside the registry's `tools` collection (including UI screen catalogue records). The generator reads only `tools`; the matrix and test expectation have been corrected to **68 tool capabilities**. UI screen entries are not mislabelled as executable tool capabilities. The exact-head CI must confirm the regenerated CSV matches the generator.


## 2026-11-17 — Track P bounded software-scope closure audit

### Work performed
- Re-read the current Track P implementation plan, P0 evidence packet, P0 controls draft, P2–P7 workplan, public-data boundary, dataset catalogue, schemas, source modules and tests.
- Confirmed the main baseline was `7967ccb0288ea1d5b82af18f8ab8d886d18d4733`.
- Inspected exact-head workflow [#44078534173](https://github.com/AssayFlux/Kinetics/actions/runs/44078534173): 9/9 jobs passed. Python: 534 passed, 9 skipped; Ruff and strict mypy passed. Android arm64 APK/AAB build, package alignment and JVM tests passed.
- Recorded the distinction between bounded software implementation closure and the still-open external/scientific/operational acceptance gates.

### Disposition
**P1–P7 bounded research-only software foundation: CLOSED.** P0 and the full Precision Medicine track: **OPEN / BLOCKED**. The public dataset catalogue remains metadata-only with no acquired entries. No independent PGx concordance, licensed source corpus, ethics determination, qualified clinical review, legal/regulatory advice, privacy/security/QMS approval, operational curator evidence or physical-device runtime acceptance is recorded. No patient data, human-subject activity, individual interpretation, clinical recommendations or Clinical Mode are authorized.

### No fabricated closure
The owner’s authorization starts engineering work; it does not substitute for competent external determinations or a formal P0 gate decision. This audit does not claim scientific or clinical validation and does not waive any carry-forward obligation.


## 2026-11-17 — Track G governance engineering verification

- Audited current `main` at `622ffc1705fda3161478b710fe2f5a4af65c6287`, including G0–G7 plans/registers, source threat model, privacy/security policies, CI, claims generator, checker, tests, dependency register and operational templates.
- Baseline exact-head workflow [#44098272029](https://github.com/AssayFlux/Kinetics/actions/runs/44098272029) passed 9/9 jobs. Python governance checker and claims-matrix reproducibility check passed; Ruff/mypy passed; pytest reported 534 passed and 9 skipped. Android arm64 debug APK/AAB build, package alignment and JVM tests passed.
- Strengthened governance structural validation for all 16 security test IDs, eight data-flow IDs, exact G requirement rows, explicit unassigned specialist roles and the five not-run tabletop templates.
- Added regression tests for security/data-flow inventory completeness and for not misrepresenting tabletop templates as completed exercises.
- Extended Android CI dependency evidence capture to include Gradle build environment, Cargo metadata and Python wheel hashes alongside existing runtime graph, Cargo tree and artifact hashes.
- Reconciled the roadmap into G0–G7 and updated implementation plan, control register, traceability and SECURITY.md with exact-head evidence and remaining limitations.
- **Disposition:** G0–G7 bounded research-only software foundation implemented/automated-check verified. Overall Track G remains OPEN pending owner policy acceptance, qualified role appointments, full SBOM and license review, independent security/privacy/scientific/legal reviews, merged-manifest/device verification, operational tabletop/access/recovery exercises and publication author/literature evidence. No external approval or exercise is fabricated. Track U remains gated on G's two-step assessment under D-023.


## 2026-11-17 — Track U start: owner V1 design and Step 1 base
**Phase:** Track U / Step 1 — documented base implementation
**Baseline:** main commit e6c98e0b506223aed65b00d1c39f0916ef2a0446
**Branch:** track-u-step1-base

### Gate assessment
- Track G bounded G0–G7 engineering foundation was reported CLOSED on exact main commit 31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1; workflow 44108451571 passed 9/9 jobs.
- Overall Track G acceptance remains OPEN for independent reviews, complete resolved SBOM/licensing, device verification, named specialist appointments, owner policy/risk acceptance and operational exercises. These remain carry-forward obligations; none is waived by starting U.
- This satisfies the D-023 sequencing prerequisite to start Track U engineering.

### Owner design direction
- Added D-024 adopting the owner's complete Premium Minimal Monochrome Design System — V1 as the active UI visual authority, superseding D-015 only where visual direction conflicts.
- Preserved non-conflicting constraints: original assets byte-for-byte, real KINETICS workflows, native Compose, Research Mode only, no fabricated accounts/jobs/results, and all existing security/privacy/licensing gates.

### Step 1 base work committed on this branch
- Added docs/track-u/implementation-plan.md with U0–U6 scope, product truth, integration contracts, two-step gate and evidence requirements.
- Updated KINETICS_UI_SPEC.md, docs/ui/ui-spec.md, docs/ui/kinetics-visual-design-system.md and docs/android-ui-ux-spec.md to the V1 authority.
- Migrated canonical active Light/Dark token values and shared spacing/radius values in design/tokens.json; regenerated GeneratedTokens.kt and kinetics-tokens.css.
- Added shared Compose V1 primitives in android/designsystem/.../KineticsComponents.kt.
- Updated screen map, device matrix, design-system README, UI quality report, docs index, roadmap and root README status.

### Not verified / not done
- No CI run, Kotlin compile, APK/AAB build or automated test result has yet been inspected for this branch.
- No running-app screenshots, visual reference comparison, contrast measurements, TalkBack/200% font-scale/RTL checks or emulator/physical-device tests are claimed.
- Existing Home/Work/Explore/Settings source has not yet been fully migrated to the new primitives and V1 component measurements.
- Search/onboarding, full destination map, security/privacy surfaces, durable result viewers and U4–U6 remain incomplete or dependency-gated.
- No Track U completion percentage is reported before Step 1 and Step 2 are both assessed.

### Next
Continue U0 token/component integration into actual screens, run exact-branch CI, inspect failures and fix them; then proceed through U1–U3 real workflow integration before Step 2 audit. Keep U4/U5 blocked until their S/P/I dependencies and licence/performance gates pass.


## 2026-11-17 — Track U implementation continuation
**Branch:** track-u-step1-base  
**PR:** #76  
**Latest source head at entry:** fe5d464367130f7dc14644e1f83b0852754e9665

### Additional implementation
- Corrected generated component catalogue so the deterministic design-token check no longer sees stale palette/spacing/radius documentation.
- Replaced the old serif/display typography mapping with the owner's refined sans-serif V1 scale; scientific text uses tabular monospace.
- Rebuilt the development component gallery around the shared V1 controls and compact flat grouping.
- Replaced text-glyph navigation symbols with one outlined Material icon family and fixed the remaining stale glyph reference.
- Added the standard Material Icons Core dependency; no new viewer/scientific runtime dependency was introduced.

### Verification status
- Workflow 44123373855 failed only because docs/ui/component-catalogue.md was stale after token generation; Android build was still in progress when that run was superseded.
- On the corrected catalogue head 0f7e145a518aa6057a2941f123d48bd1eea8da5e, the Python foundation/registry/tests job passed; other host-side scientific smoke/security/SPDX jobs passed. Android arm64 APK/AAB job was still running at last inspection.
- Exact latest head fe5d464367130f7dc14644e1f83b0852754e9665 has a new pull-request workflow run queued/pending. No result is claimed for that head yet.
- No UI screenshot, contrast, TalkBack, 200% font-scale, RTL, emulator or physical-device evidence is claimed.

### Remaining track work
- App bar and navigation drawer still need full integration and exact dimension verification across compact/standard/large/tablet windows.
- Search/onboarding and all settings/security/privacy surfaces need implementation against actual supported app behavior.
- Review local biometric lifecycle/recovery, encrypted settings/data inventory/deletion disclosures, and decide FLAG_SECURE/Recents behavior only with documented threat/privacy review.
- Finish durable result/provenance views and verify all workflow states with actual ResearchStore/WorkManager paths.
- U4 viewers remain blocked on S1–S3 interfaces, dependency licence/security review and low-end-device performance evidence.
- U5 remains blocked on P1–P3 and I2–I4; no clinical interpretation is permitted while P0 is blocked.
- U6 needs actual screenshot/contrast/accessibility/window/device evidence; CI compilation alone is insufficient.
- Step 2 exact-head integration audit has not run. Track U remains OPEN.


## 2026-11-17 — Track U application shell continuation
**Branch:** track-u-step1-base  
**PR:** #76  
**Source changes:** e08d2699c290dc42bb8c0ff1946823d8d4a8ee02 and 778747d7b6f0e797f6124ec54b81e5ef80186af2

### Implemented
- Added the V1 56dp application bar with a real menu action and current destination context.
- Replaced the compact-width permanent drawer with a gesture-enabled modal drawer, constrained to a maximum 340dp width, with grouped brand header, real Home/Work/Explore/Settings destinations and selection/close behavior.
- Retained adaptive navigation rail for expanded windows and bottom navigation for compact windows; all routes continue to use existing app screens.
- Updated the UI quality report to distinguish implemented source behavior from unrun visual/device acceptance.

### Exact-head verification
- Workflow 44124996311 on prior source head 49f169f497058bfe02fd9f66c712b11b19eafc86: Python foundation/registry/tests, token reproducibility, SPDX inventory, scientific reference comparisons, RDKit descriptor sanity, OpenMM replica smoke, ADMET utility smoke and private Node security tests passed. Pinned Vina smoke and Android arm64 APK/AAB build were still running at last inspection.
- New source commits have triggered additional PR workflows. Kotlin compilation, APK/AAB build, JVM tests and UI behavior are not yet claimed for the latest source head.
- No screenshot, contrast, TalkBack, 200% font-scale, RTL, keyboard/switch navigation, emulator or physical-device evidence is claimed.

### Remaining
- App shell still needs exact-head build validation and visual inspection against the 393×852dp reference, plus compact/standard/large/tablet checks.
- Search/onboarding, security/privacy surfaces and full result/provenance presentation remain open.
- U4/U5 remain dependency-gated; U6 evidence remains outstanding. Step 2 audit has not run. Track U remains OPEN.


## 2026-11-18 — Public scientific database retrieval and local integration

- Added Home search/retrieval for NCBI Gene metadata, NCBI Nucleotide, NCBI Protein, UniProtKB and RCSB PDB entry IDs.
- Added allow-listed HTTPS GET transport for NCBI E-utilities, UniProt REST and RCSB PDB; no redirects, strict UTF-8 decoding, connection/read timeouts and response-size ceilings.
- Public query validation rejects FASTA/VCF payloads and long sequence-like search terms. The UI instructs users not to enter patient/sample identifiers or raw sequences. Imported research files and derived results are not sent to providers.
- Added encrypted app-private public-record payload storage using the existing Android Keystore AES-GCM chunk format, SHA-256 verification, SQLite metadata, saved-record listing, deletion, authenticated reopen, FASTA reanalysis and RCSB structure reopen.
- Connected fetched FASTA to the existing embedded Python FASTA QC adapter. Connected fetched RCSB mmCIF to the existing Python structure preparation/parser and offline viewer. No new folding model or experimental structure generator was introduced.
- Updated the public-data rulebook, U-track implementation plan, completion audit, U3/U4 notes, UI specification, privacy notice, Android Settings inventory, threat model, data-flow inventory (DF-09), security verification matrix, governance checker/tests, P0 controls and architecture defaults.
- Documented the storage limitation: raw public payloads are Keystore-encrypted; SQLite source metadata and analysis JSON remain unencrypted at rest. Provider release/licence metadata, cache quotas, explicit network cancellation/retry, RCSB text search and NCBI Gene-to-RefSeq linking remain open.
- CI exposed an existing Kotlin runtime-card type mismatch (nullable Boolean passed where RuntimeStatusCard expects String) and governance inventory ID range assumptions. Runtime statuses now map to explicit labels; governance traceability remains G-REQ-001..008 and data flows DF-01..09.
- Earlier CI runs 2959 and 2971 failed on pre-fix commits. Exact latest-main build/test verification remains pending; no APK is declared successful or available until the latest run produces and verifies its artifact.


## 2026-11-18 — NCBI Gene sequence linking

- Added NCBI ELink-based discovery from a Gene ID to linked nucleotide or protein records, followed by ESummary metadata and the existing accession-based FASTA retrieval.
- Home now exposes "Find nucleotide" and "Find protein" actions on NCBI Gene results.
- Added validation tests for numeric Gene IDs and supported linked databases, plus static integration assertions.
- This closes the previous metadata-only Gene search gap at source level; exact-head CI and provider-response/device tests remain pending.


## 2026-11-18 — Android package and JVM test verification

- CI run 2985 (44229328602) on commit 3dfc8b903f6928b65e673b2bb9a7ffb0586ff335 successfully built arm64 debug APK and AAB and passed package/native 16 KiB alignment verification.
- The same run's Android JVM test stage exposed a test-fixture compile error in ResearchStoreMigrationTest.kt: a Long literal was passed where the current completeImport contract expects an Int. Corrected the fixture from 1L to 1 at commit 2334b0703553e833adbf6a8de44c28826aebf05a.
- The generated APK/AAB from 3dfc is not treated as a release candidate because the JVM test stage failed and later source changes are present on main. Exact-current-main build plus JVM tests and artifact hash verification remain required.


## 2026-11-21 — Molecularis identity migration

- Rebranded product metadata, Android source namespace, Kotlin UI/design-system identifiers, Python package namespace, Node worker package/configuration, generated CSS tokens, viewer global API, documentation and active asset paths to Molecularis.
- Kept the Android applicationId and versioned scientific schema identifiers stable for compatibility; added Python, Node, viewer and CSS aliases for existing integrations.
- Retained enzyme-kinetics terminology and the scientific Michaelis–Menten implementation as domain concepts. The historical owner-supplied master and prior session entries remain archival evidence.
