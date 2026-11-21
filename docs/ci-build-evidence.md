# CI build evidence — 2026-11-08


> **Historical record:** This document records evidence created before the product rebrand. References to Kinetics, the former repository name and historical source paths are retained where needed to preserve the accuracy of the dated evidence. The current product identity is Molecularis; see [the brand migration contract](brand-migration.md).

## Latest verified source revision

- Repository: [AssayFlux/Kinetics](https://github.com/AssayFlux/Kinetics)
- Source commit: `79a24eb00ec7beea30674a591361c2351beaa13d` — `Apply D-015 adaptive theme to local biometric lock screen`.
- Workflow: [run #2039 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42493028735).
- All five jobs passed: Python foundation/registry/tests; pinned host scientific-reference comparisons; pinned RDKit descriptor sanity fixtures; SPDX direct source-dependency inventory; Android ARM64 debug APK/AAB build, package checks and Android JVM unit-test task.
- Android build log: `BUILD SUCCESSFUL`; package-alignment and artifact-hash verification steps passed.
- APK: 69,792,811 bytes; SHA-256 `7029555e9640fd920f22a67890fe921473582affd2538e8aaddd61a261c9e44e`.
- AAB: 39,926,363 bytes; SHA-256 `dd6eb3cc6ddc97c9ed3036b4d6e0747c2e91ef2a6ee57f80eaa4e11e28b8cfa9`.
- Workflow artifact ZIP: 79,991,103 bytes; SHA-256 `4b6211b80b9a50a773bdb38c20ee6f7026e327255844f1eeffeb696bc613d8cd`. This is the ZIP digest, not the APK/AAB digest.
- The exact-source UI change applies the D-015 adaptive Light/Dark/System theme to the local biometric/device-credential app-lock screen. The screen explicitly distinguishes local device unlock from online account sign-in and does not handle biometric templates.

## Previous verification

- [Run #2038](https://github.com/AssayFlux/Kinetics/actions/runs/42486834053), commit `5471974`, passed the complete CI suite and produced an ARM64 debug APK/AAB.
- [Run #2033](https://github.com/AssayFlux/Kinetics/actions/runs/42484179938), commit `037befa`, passed 204 Python tests (4 skipped), pinned host reference comparisons, RDKit sanity fixtures, SPDX direct inventory, Android build/package checks and JVM unit-test task.

## Verification boundaries

- No emulator or physical-device installation/runtime evidence is recorded for run #2039.
- CI compilation does not prove real-device launch, Chaquopy/JNI runtime, SAF lifecycle, WorkManager process-death recovery, Keystore behavior, cold-start or peak-memory performance.
- Android JVM task success is not a substitute for instrumentation/UI tests.
- Debug artifacts are not production-signed release builds.
- Build and software/reference-fixture tests do not establish independent experimental scientific validity, complete dependency licensing or clinical suitability.
- Host reference comparisons establish agreement with selected pinned software fixtures only.

D-016 requires every substantial increment to be built, regression-tested and inspected. Record exact source SHA, workflow, toolchain, artifact hashes, test results and device details; unavailable evidence remains NOT RUN or BLOCKED.


## R-track imported FASTA analysis integration — 2026-11-09

### Exact-source CI evidence (integration revision before final audit patch)
- Source commit: `fc8b667951626447d951931bbfd1f901867405be`.
- Workflow: [run #2093 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42551582986).
- All five jobs passed: Python foundation/registry/tests; pinned host scientific-reference comparisons; pinned host RDKit descriptor sanity fixtures; Android ARM64 debug APK/AAB build, package checks and JVM unit tests; declared source dependency SPDX inventory.
- Android Gradle build: `BUILD SUCCESSFUL`; `:app:testDebugUnitTest` — `BUILD SUCCESSFUL`; APK ZIP alignment and native ELF alignment checks passed.
- APK: 69,875,191 bytes; SHA-256 `29db7d4014eeba7e6ab0ac57465c636f74cddbfe3b673a19c5e355c1b5e9387b`.
- AAB: 39,951,888 bytes; SHA-256 `24ce93b67a3eeb1946e1e2c51ef181032422a637cd6f595d9716eef737b8c607`.
- Workflow artifact ZIP: 80,045,596 bytes; SHA-256 `d79ef58563583f5c7f3ce0b45cbefa53f9a91c86b98b1076a8f22531d52b276c`; artifact ID `13645517097`. This digest is for the uploaded ZIP, not the APK/AAB.
- The successful build contains the imported FASTA WorkManager worker, schema-v4 durable analysis result, SHA-256 provenance, job-card inspection and SAF analysis JSON export.
- Follow-on exact-source audit commit: `2ea102719fc37354f18def85bb329a60a885ee2a`; [workflow run #2094 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42552040285). All five jobs passed, including Python foundation/registry/tests, pinned host scientific references, RDKit descriptor fixtures, SPDX inventory, and Android ARM64 APK/AAB build + JVM tests.
- Android build log: `BUILD SUCCESSFUL`; `:app:testDebugUnitTest` — `BUILD SUCCESSFUL`; APK ZIP/native ELF alignment and artifact verification passed.
- APK: 69,875,059 bytes; SHA-256 `d6b7bd05090519761bb1771b82c41f14b3c3ff2d834a1844d2ec0052babbb82b`.
- AAB: 39,951,809 bytes; SHA-256 `9c09035e9588e4af42554418c7f02e1efca2d84441f328b237f29c758c6c261f`.
- This confirms the result-digest revalidation, result-size guard and bounded preview on `2ea1027`. A later documentation/schema-only commit is being verified separately.

### Final R Step 2 audit changes (CI passed on `2ea1027`)
- Analysis export now requires current job state `succeeded` and exact equality between the current job digest and analysis-record digest.
- Worker checks non-empty record list and caps serialized output at 2,000,000 characters before persistence.
- Job-card preview is limited to 12,000 characters; full JSON is available via explicit export.

### Verification boundaries
- JVM test task is green for both `fc8b667` and `2ea1027`; no dedicated SQLite migration, analysis worker lifecycle, SAF provider failure, process-death or instrumentation test has yet been added for this vertical slice.
- No emulator or physical-device installation/runtime test is recorded. CI artifact existence is not device acceptance.
- No independent experimental validation or clinical suitability is implied.


### Exact-source private plaintext cleanup regression — 2026-11-09
Commit `c157bb5a09d9dcc17a8bc7a57b60129d58e4866a`, [workflow run #2100 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42553589465). All five CI jobs passed, including Android ARM64 debug APK/AAB packaging, APK/native alignment checks, Android JVM tests, Python foundation/registry tests, pinned scientific reference fixtures, RDKit sanity fixtures and SPDX inventory.
- Android JVM task: `:app:testDebugUnitTest` — BUILD SUCCESSFUL.
- APK: 69,875,783 bytes; SHA-256 `74275b4552fdab7e009bc067cbb27263e7296f860bb17b52257bbd20cbbd7462`.
- AAB: 39,953,164 bytes; SHA-256 `c89ad4bb971e9d76410592ba7d76655c7c029b63ce74c5895203edc0a1e7dc7b`.
- Artifact ZIP: 80,047,831 bytes; SHA-256 `c10568ef4d18f28ea9313b159e7b967103f29728661ce91b448e53c087107e0a`; artifact ID `13646870988`.
- New JVM regression tests verify temporary plaintext deletion after failed materialization, consumer exceptions and successful analysis.
- CI validates build/package/JVM and host checks only. It does not prove Android device runtime, secure erasure, database migration or end-to-end WorkManager/SAF lifecycle.


## Exact-source R-track audit baseline — 2026-11-09

- Source commit: `8c4128d5e448db51f2b48fec6c38ce6022fdb053`; [CI run #2101 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42554027490). All five jobs passed.
- Python CI collected 233 tests: 229 passed, 4 skipped (three optional RDKit adapter tests and one optional pysam test, unavailable in the base environment). The separate pinned RDKit descriptor sanity job passed.
- The Python suite executed R3/R4 sequence and research primitive tests, R5 structure/view tests, R6 core chemistry, R7 phylogenetics, R8 omics, R9 catalogue/variant reference and R10 registry/SBOM/configuration tests.
- Pinned host scientific-reference job passed the Michaelis–Menten/SciPy and genetic-code/Biopython comparison steps. These are bounded synthetic/software-reference checks, not independent experimental validation.
- Android ARM64 debug APK/AAB packaging, static package/ELF alignment and `:app:testDebugUnitTest` passed. APK: 69,875,151 bytes; SHA-256 `059abb9e3a299b5295b8f08772b976195d7be1cd7db46dce34faa7bcf486d2d9`. AAB: 39,952,539 bytes; SHA-256 `9c8e2ca3a81c4ef2b1fb041aefee99ace5cbfb3292574b815c6a87549210044e`. Artifact ZIP: 80,046,515 bytes; artifact ID `13646239880`.
- This evidence does not establish emulator/physical-device runtime, migration/WorkManager/SAF instrumentation, on-device Chaquopy, independent experimental validation, broad domain reference concordance, complete transitive licence/security review or release signing.


## Exact-source SQLite migration regression CI — 2026-11-09

- Source commit: `dd3269acfa79546b143e239948df4d95e938abc7`; [CI run #2104 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42556657894). All five jobs passed.
- Android arm64 debug APK/AAB build, package and ELF alignment checks, and `:app:testDebugUnitTest` all passed.
- Robolectric migration coverage now includes fresh schema v4 creation, v1→v4, v2→v4 and v3→v4 upgrades; v1/v2 fixtures assert a pre-existing job row survives and the v4 columns/table exist.
- APK: 69,875,719 bytes; SHA-256 `958098b0143b02bd68a6dadbbcd783afbd1fd7c8a5893f553bda5ba365f316e9`.
- AAB: 39,953,087 bytes; SHA-256 `773cc9cf5569d3eabb6c2665de79a4e0d8e0a47fba3f7b3f6c3c272552996e67`.
- Artifact ZIP: 80,047,943 bytes; SHA-256 `f9a0e18045a8a418691900868f4f78fd595a30798e2c95da29e82a00649ad7fc`; artifact ID `13647404333`; [download artifact](https://github.com/AssayFlux/Kinetics/actions/runs/42556657894/artifacts/13647404333).
- This closes the automated Robolectric migration checks for documented schema versions only. Device SQLite migration, interrupted transactions, WorkManager lifecycle, SAF providers and physical-device execution remain open.


## Exact-source R5 structural software comparison CI — 2026-11-09

- Source commit: `f1681ea5e2009f8bcbc33468689108affe57e56c`; [CI run #2105 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42557116117). All five jobs passed.
- Pinned host scientific-reference job executed the new Biopython 1.88 / NumPy comparison. Its fail-closed assertions passed for PDB atom metadata/coordinates, contact pairs and Horn-versus-Kabsch superposed RMSD. The result is in artifact `kinetics-host-reference-results-f1681ea5e2009f8bcbc33468689108affe57e56c`, artifact ID `13647457755`, ZIP SHA-256 `32c6f5de79373219c7409847679cc0c8359be722aa2d5d98fd6e9b505b9addaf`.
- Android ARM64 APK/AAB build, static alignment, artifact verification and JVM unit tests passed.
- APK: 69,875,851 bytes; SHA-256 `f3bb4c76f4cd36ab747efd77e0ba63b79feab2f74c521e4fd9959a298463270d`.
- AAB: 39,953,035 bytes; SHA-256 `bc20f28a3fdb2f4630b586ac8b51d5c6aef814b5fc84526c6759d6ad13a1f782`.
- Android artifact ZIP: 80,047,834 bytes; SHA-256 `41a206d20a983f0823fa79f03d6a5c114c7982bc209144d5de07a80beefd562b`; artifact ID `13648167099`.
- R5 evidence boundary: this is synthetic software concordance, not experimental reference-structure validation. mmCIF semantics, SASA/interactions, licensed real structures, large-structure benchmarks, viewer and device measurements remain open.


## Exact-source R-track audit baseline — 2026-11-09

- Source commit: `888e49bc7108a2609db97d76193a60d5eec175e0`.
- Workflow: [run #2126 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42560038764); all five jobs passed.
- Python: 242 collected; 238 passed; 4 skipped.
- Host scientific-reference comparisons, pinned RDKit descriptor sanity and declared-source SPDX inventory passed.
- Android arm64 debug build and package verification passed; `:app:testDebugUnitTest` completed successfully.
- APK: 69,891,771 bytes; SHA-256 `73e66bacb3d1e45e8928c52c10b3fed14e29aa71c8e09a8df73945ffef24aa06`.
- AAB: 39,953,771 bytes; SHA-256 `a851cdeaf921e8b8b40dd82184fb2ef8200bc7b660ab32c80da448cd22d5aadf`.
- Uploaded Android artifact ZIP: [artifact 13649560656](https://github.com/AssayFlux/Kinetics/actions/runs/42560038764/artifacts/13649560656), 80,049,058 bytes; SHA-256 `3c4b135979a4b1920a7afae3fc500c2aa7ebb35a3ef0af357fa867de9be60488`.
- This exact-source build verifies the import worker resource-lifecycle hardening. It does not establish physical-device runtime, WorkManager process-death recovery, SAF provider behavior, Chaquopy/JNI runtime, scientific validation or release signing.


## Exact-source I1–I5 combined software CI — 2026-11-11

- Source commit: `026032962de7b8315cfbeaaa0e0d6c39aa0d4ef4`.
- Workflow: [run #42967649660 — successful](https://github.com/AssayFlux/Kinetics/actions/runs/42967649660); all 9 jobs passed on the same source SHA.
- Python foundation/registry/tests: 498 collected; 489 passed; 9 skipped. Ruff and strict mypy completed successfully.
- Pinned host-side scientific-reference comparisons passed for the configured SciPy/PK-PD, genetic-code, structural, phylogenetic and omics fixtures. These are software-reference comparisons, not independent experimental validation.
- Pinned RDKit descriptor sanity and ADMET evaluation utility smoke checks passed on synthetic fixtures; no ADMET dataset was acquired and no predictive model was trained.
- AutoDock Vina 1.2.7 engine smoke and OpenMM 8.6.1 CPU synthetic harmonic replica smoke passed. These do not establish docking redocking/enrichment or biomolecular MD validity.
- Private Node docking-worker security tests and declared-source SPDX inventory passed. The worker remains disabled by default and has not been deployed; SPDX output is a declared-source inventory, not a complete transitive binary licence approval.
- Android arm64 debug build and `:app:testDebugUnitTest` passed; APK/package checks and 16 KB native ELF alignment checks passed.
- APK: 70,388,850 bytes; SHA-256 `b767656e1d39f1954da8b4d97d7409cb854ef41ce4ded0d17b62356ba42b81a0`.
- AAB: 40,252,958 bytes; SHA-256 `1edbb63f5fc8f0969c8137f9edc7b4f9b775b5cea5c6fa8499fb04e83bd03a80`.
- Android artifact ZIP: [artifact 13832212511](https://github.com/AssayFlux/Kinetics/actions/runs/42967649660/artifacts/13832212511), 80,652,760 bytes; SHA-256 `9ac654392a86fbc494c84bf2c44eed7e9f12c9301646f36c60035e3b5848f430`.
- Verification boundaries: no emulator/physical-device installation or runtime test; no approved secure-node deployment; no complete transitive engine/model/database/font licence review; no independent docking, biomolecular MD, ADMET, cohort or variant-effect validation; no production signing/release.
