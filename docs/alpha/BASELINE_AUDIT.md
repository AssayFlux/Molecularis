# Alpha Baseline Audit — Initial Snapshot

**Date:** 2026-11-21  
**Branch:** Alpha  
**Base branch:** CORE  
**Base commit:** 741eb5808a99cce9131cc93557253a72c7e1819b  
**Audit scope:** Targeted remote GitHub inspection; not a full local clone or exhaustive source audit.

## Repository facts verified

- Repository: AssayFlux/Molecularis, public.
- Actual default branch at audit time: CORE.
- Alpha was created from CORE at commit 741eb5808a99cce9131cc93557253a72c7e1819b.
- The branch contains a Python project manifest: pyproject.toml, project name molecularis-workbench, version 0.1.0, Python >=3.10.
- Android application build is configured in android/app/build.gradle.kts with Kotlin, Jetpack Compose, Chaquopy, compileSdk 36, minSdk 29, arm64-v8a and C++17.
- Rust component exists at android/native-rust/Cargo.toml as a Rust 2021 static library.
- C++ native boundary exists under android/app/src/main/cpp/CMakeLists.txt and imports the Rust static library.
- Existing cross-component contract exists at api/engine-envelope-v1.schema.json; its schema ID and message identifiers still contain the legacy kinetics namespace. Treat these as stable protocol identifiers until explicit versioned migration is designed.
- Existing CI workflow is .github/workflows/ci.yml and was named “Molecularis validation and Android build”. Its original branch filters covered main and v0.1.1, not CORE or Alpha. Alpha changes it to include CORE and Alpha so the compatibility workflow can run on the new branch.
- A separate Alpha documentation integrity workflow and script were added to branch Alpha.

## Existing foundations to preserve and audit

- Python scientific package and tests.
- Rust static library and Cargo lock/dependency tree.
- C++17 JNI/native library and CMake configuration.
- Android/Kotlin/Compose shell, Chaquopy bridge, local storage and background-work semantics as migration sources.
- Versioned JSON Schema contracts, capability registry, scientific rulebooks, validation plans, provenance and governance records.
- Existing adapters and scientific domains: sequence/genomics, structure, chemistry/RDKit, docking/Vina, OpenMM, kinetics, omics and pharmacogenomics.

The presence of a file or adapter is not proof that a feature is complete, validated, secure or production-ready.

## Initial gaps and risks

1. No browser/PWA runtime has yet been established by this audit. Search for package.json returned no result, but this is not a complete proof that no web assets exist.
2. No OCI worker/container deployment was established by this audit. Search for Dockerfile returned no result, but this is not exhaustive.
3. Current CI is still an Android/legacy scientific validation workflow. It is retained as a compatibility gate during migration, not the target all-device CI architecture.
4. Existing schema IDs retain kinetics-era naming. Do not rename in place; define a versioned migration and compatibility strategy.
5. Android storage, Chaquopy, JNI, WorkManager, SAF and Keystore semantics require a per-capability migration ledger and data migration tests.
6. Upstream ZIP files are text snapshots, not Git repositories; exact upstream commits, versions and model/data licensing must be independently re-established.
7. Exact Alpha-head CI has not yet been observed as complete at the time this audit was written.

## Required M0 follow-up

- Enumerate all tracked paths and module ownership.
- Fetch and inspect full pyproject, Cargo, CMake, Gradle and workflow manifests.
- Run exact-Alpha Python, Rust, C++ and legacy Android checks.
- Inventory all existing schemas and contract tests.
- Inventory all engine adapters, dependencies, licenses, model/data references and external binaries.
- Produce Android-to-all-device component parity and user-data migration ledger.
- Threat-model local node, API, job scheduler, artifact service and notebook execution.
- Update this audit with exact command outputs, CI URLs, failures and reviewer.

## Evidence boundary

This is a targeted initial snapshot, not an independent security audit, scientific validation, full source audit, device test or release approval.
