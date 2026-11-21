# Changelog

All notable project changes will be recorded here.

## v0.1.0 — basic working model (release target; not yet published)

- Added explicit immutable-baseline, branch, change-control and release-state governance; v0.1.0 remains a candidate until exact-commit acceptance and owner approval.
- Added a machine-readable candidate release manifest and CI checks for version alignment and Android capability-matrix consistency.
- Corrected the Android integration matrix: 36 of 68 catalogue capabilities are connected; 32 remain Python-only/not connected. The former 68/68 summary contradicted its own row-level table.
- Established `main` as the v0.1.0 baseline candidate and `v0.1.1` as the sole forward-development branch. Existing legacy branches are not authorized for further work.

- Set Python package and Android application metadata to version 0.1.0.
- Defined the bounded first-release scope: local research workspace, truthful Home/Work/Settings shell, supported FASTA/FASTQ workflows, bounded structure/chemistry viewing, provenance and reproducible ARM64 packaging.
- Explicitly exclude claims of complete Android dispatch for every registered tool, de-novo protein folding, clinically validated PGx, validated ADMET, general-purpose molecular dynamics and universal database coverage.
- Release remains blocked until the exact-head APK, tests, package checks, named-device workflow checks, accessibility/security/licensing review and owner acceptance are recorded. See [the release plan](docs/release-plan-v0.1.0-v0.1.1.md).

## Unreleased

- Closed the bounded Track G G0–G7 engineering foundation after exact-head CI workflow [#44108451571](https://github.com/AssayFlux/Kinetics/actions/runs/44108451571) passed 9/9 jobs on `31b1618c4e843d0ec90feb2ceae0d0e4fb1615b1`; Python 536 passed/9 skipped, Ruff/mypy/governance checks and Android arm64 APK/AAB/JVM checks passed. Overall G acceptance remains open for independent assurance, complete SBOM/licensing, device, owner and operational evidence.
- Started Track G G0–G7 engineering controls: canonical threat model and UI supplement, security verification matrix, source-level data-flow inventory, role/cadence model, requirements traceability, CAPA template, 68-tool capability claims matrix, dependency decision register, publication integrity and operational procedures.
- Added CI structural checks for governance registers and reproducible capability-claims matrix; Android CI archives Gradle/Cargo dependency reports and artifact hashes; the G verification increment adds build-environment, Cargo metadata and Android Python-wheel hash evidence. These remain raw inventories, not a complete SBOM or license clearance. These are engineering controls only; independent reviews and operating exercises remain open.
- Reworked the repository README into a concise project landing page with track status, scoped engineering-gate percentages, collapsible track details, navigation badges and the supplied animated brand/Molecularis logos.
- Consolidated legacy `Assets/` artwork into the lowercase `assets/` tree while preserving original Git blobs; corrected the JPEG extension of the former `Molecularis By AssayFlux©.png` file and updated active asset documentation.
- Updated the owner-approved sequential track order to **R → S → I → P → G → U** (D-023); Track U now follows Track G, with its pre-existing partial implementation retained and further work gated on G's two-step exit.
- Established the owner-approved direction baseline and R0 repository foundation.
- Added bounded Android SDF/MOL graph preview and host RDKit descriptor adapter; chemistry output remains exploratory.
- Added optional AutoDock Vina 1.2.7 host docking runner and a disabled-by-default authenticated Node worker.
- Added optional OpenMM 8.6.1 CPU replica runner with bounded DCD output; no biomolecular force field is bundled.
- Added PK/PD reference models, a SciPy ODE comparison, scaffold-aware ADMET evaluation metrics/applicability tools, metadata-only source inventory and synthetic aggregate cohort/effect simulations.
- These additions are research engineering foundations, not independently validated scientific or clinical capabilities.
