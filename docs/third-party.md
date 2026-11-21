# Third-party software and data register

No third-party scientific engine, model or database is approved for product bundling. Chaquopy and its scientific package dependencies are configured only in the isolated R1 feasibility prototype; they are not production selections.

| Component | Version | Source | License | Use | Approval/status |
|---|---|---|---|---|---|
| pytest, PyYAML, Ruff, mypy, pre-commit | Ranges in requirements-dev.txt / hook revision in config | PyPI and pre-commit hook repository | Upstream terms require review before distribution | Development and CI only | Not bundled in app; audit required before release |

Before adoption, pin an exact version/revision; record canonical source and upstream license; assess redistribution, modification, attribution, patent and network obligations; flag GPL/AGPL or restrictive terms for explicit owner review; record data provenance, consent and update policy.

The project license decision is Apache-2.0 (D-001), and the canonical LICENSE text is present at the repository root. This does not approve any third-party component for product distribution.


## R1 candidates reviewed by desk research (not adopted)

| Candidate | Upstream licensing / status | Feasibility status | Decision |
|---|---|---|---|
| Chaquopy 17.2.0 | Upstream states 12.0.1+ is MIT/free-open-source; verify exact release artifact and transitive packages before distribution | Isolated R1 prototype; Python 3.11 / SDK / NDK and custom Biopython wheel build succeed; debug APK/AAB build and static 16 KB ELF inspection passed in CI | R1 candidate only; not selected for production |
| Biopython 1.88 | Upstream Biopython License Agreement applies to most files; some files are explicitly dual-licensed under that agreement or BSD-3-Clause; file-level audit required | Custom CPython 3.11 / arm64-v8a wheel built and packaged; APK/AAB static ELF 16 KB checks passed; Android runtime and file-level license audit pending | Not approved for production bundling; file-level license and ABI review required |
| SciPy (version TBD) | BSD-3-Clause | No compatible CPython 3.11 / arm64-v8a distribution found in Chaquopy indexes; custom build/alternative not yet evaluated | Not approved for bundling; required architecture candidate remains unresolved |
| Parasail v2.6.2 (candidate) | Battelle BSD-style license; source/binary notice retention and citation requirements; restrictions on Battelle name use | Candidate sequence-alignment engine; upstream describes C99 SIMD Smith–Waterman, Needleman–Wunsch and semi-global algorithms, CMake build and ARM cross-compilation; Android build not yet attempted | Evaluation only; no product bundling approval; pin/audit source and preserve license/citation obligations before adoption |
| Mol* 5.13.1 (candidate) | MIT license; preserve copyright and permission notice; audit bundled/transitive assets | Candidate offline macromolecular viewer; npm distribution and viewer bundle documented; local asset packaging/WebView worker and WebGL behavior not tested | Evaluation only; not bundled or approved |
| RDKit (candidate) | BSD-3-Clause upstream core license; audit bundled/transitive dependencies and contributed modules | Mature C++ cheminformatics toolkit; official build documentation describes CMake builds, but does not establish Android arm64 support; Boost/dependency and binary-size burden not measured | Alternative chemistry engine candidate; Android feasibility not established; not approved for bundling |

References:
- https://chaquo.com/chaquopy/documentation/
- https://chaquo.com/chaquopy/doc/current/versions.html
- https://chaquo.com/chaquopy/license/
- https://github.com/chaquo/chaquopy/blob/master/LICENSE.txt

No R1 candidate is approved for bundling by this entry. GPL/AGPL and other restrictive terms remain subject to explicit owner review. The project's own license is Apache-2.0 by owner decision D-001; the canonical LICENSE grant file is present.


Biopython references:
- Upstream license: https://github.com/biopython/biopython/blob/master/LICENSE.rst
- Upstream installation/build requirements: https://pypi.org/project/biopython/
- Chaquopy FAQ and Android wheel build guidance: https://chaquo.com/chaquopy/doc/current/faq.html and https://github.com/chaquo/chaquopy/tree/master/server/pypi



Parasail references:
- Upstream repository and build documentation: https://github.com/jeffdaily/parasail
- Pinned release tag: https://github.com/jeffdaily/parasail/tree/v2.6.2
- Exact upstream license text: https://github.com/jeffdaily/parasail/blob/v2.6.2/LICENSE.md
- Scientific citation: Daily J. (2016). Parasail: SIMD C library for global, semi-global, and local pairwise sequence alignments. BMC Bioinformatics 17:1–11. doi:10.1186/s12859-016-0930-z


Mol* references:
- https://github.com/molstar/molstar
- https://github.com/molstar/molstar/blob/master/LICENSE
- https://www.npmjs.com/package/molstar

RDKit references:
- https://github.com/rdkit/rdkit
- https://github.com/rdkit/rdkit/blob/master/license.txt
- https://www.rdkit.org/docs/Install.html


## PGx data governance — source gate

No PharmVar, PharmGKB, CPIC or other PGx content is currently bundled. Before importing definitions or guideline content, record the exact release/download URL, retrieval date, SHA-256 checksum (required by the importer), genome build, schema mapping, attribution and redistribution terms. Review each source's current terms rather than assuming that publicly viewable content is freely redistributable. Keep allele-definition data distinct from clinical guideline recommendations; require independent curator review and release-specific concordance before marking any entry validated. No patient-level interpretation is enabled.


## Reproducible local build toolchain pins

- Gradle 8.13 binary distribution SHA-256: 20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78 (official Gradle checksum reference).
- Chaquopy 17.2.0 source commit: 1f63c93d8beaf7062fbe51888ab9235475df3bb8.
- Android Gradle Plugin 8.13.2; Kotlin 2.2.21; NDK 28.2.13676358; JDK 17; SDK platform 36; Build Tools 36.0.0; CMake 3.22.1.
- Biopython 1.88 and NumPy 1.26.2 are pinned in the prototype. The custom Biopython wheel build is source-pinned, but the downloaded NumPy wheel still needs an independently pinned checksum and a current 16 KB page-size compatibility review.
- These pins improve reproducibility; they do not constitute a full dependency lock, transitive license audit, SBOM or local build-success claim.
- Gradle checksum source: https://gradle.org/release-checksums/


## SBOM generation

Run `python scripts/generate_source_sbom.py --output sbom/source-dependencies.spdx.json` to create an SPDX 2.3 inventory of declared direct dependencies. This deliberately marks unresolved versions and license conclusions as NOASSERTION and does not include resolved transitive Gradle artifacts, downloaded wheel hashes, native binary contents or file-level license results. It is an engineering inventory only, not the final release SBOM. The release checklist still requires a fully resolved transitive SBOM.


## RDKit adapter status

An optional source adapter exists at python/molecularis/chemistry_rdkit.py. It imports RDKit lazily and reports the active engine version; it is not a bundled dependency and is not used by the Android app. Before adoption, pin an exact compatible release, capture the full transitive dependency graph, audit notices/licenses at file and binary level, evaluate Android arm64/16 KB compatibility and benchmark binary footprint. The core RDKit project license is BSD-3-Clause, but that does not settle the licenses of all bundled dependencies or contributed components.


## HTSlib/pysam adapter status

A lazy host-side adapter at python/molecularis/genomics_htslib.py supports streaming BAM/CRAM through pysam/HTSlib. CRAM requires a local reference FASTA; remote reference retrieval is not enabled. pysam/HTSlib is not an Android dependency. Before adoption, pin exact pysam/HTSlib releases, audit bundled htslib/zlib and platform-specific licenses, verify native arm64 and 16 KB compatibility, and measure binary footprint. No Android bundling approval is implied.


## PharmVar data source review

PharmVar documents bulk database downloads containing per-gene haplotype TSV, FASTA and VCF files. Its TSV records are one row per haplotype/variant and coordinates are relative to the stated reference sequence; reference/*1 alleles use a special REFERENCE sentinel. The PharmVar data source is identified in HL7 terminology as CC BY-SA 4.0; retain attribution and ShareAlike terms in any separately distributed PharmVar data pack. Current PharmVar site version observed during this review: 6.2.29 (last updated 2026-09-22). Structural rearrangements and large deletions are not included in the downloadable allele definitions described on the download page. Recheck the live source release, terms and gene-specific change logs before each import.

- Native Rust toolchain: rustc/cargo 1.88.0 pinned by rust-toolchain.toml; android arm64 target pinned; Cargo.lock committed and local build uses --locked.

- Biopython 1.88 source is obtained from the immutable Git commit d7e4b8b19399668b09442a5b35765d9186b5f665, exported with git archive and built from a local recipe path instead of resolving a mutable PyPI sdist at build time. Biopython's PyPI metadata uses LicenseRef-Biopython-License-Agreement; include its upstream LICENSE/terms and review wheel redistribution before release.


## Biopython license notice

Biopython 1.88 is built from immutable source commit d7e4b8b19399668b09442a5b35765d9186b5f665. Its upstream LICENSE states the default license is the Biopython License Agreement, with some individual files dual-licensed under that agreement or BSD-3-Clause. The complete upstream LICENSE is reproduced in android/app/src/main/assets/third-party/BIOPYTHON-LICENSE.txt for the app's binary distribution notice. Individual file headers and all other runtime/transitive dependencies still require review.

- Biopython source pin: https://github.com/biopython/biopython/commit/d7e4b8b19399668b09442a5b35765d9186b5f665 (release 1.88). PyPI release page lists the sdist checksum, but the Android build uses the exact Git source commit rather than a mutable package index lookup.


## Host-only validation dependency inventory

The pinned NumPy/SciPy host comparison environment in
`validation/requirements-scipy.txt` is included in the generated declared
dependency SPDX inventory. These packages are validation-host tools only and
are not Android runtime dependencies. The CI workflow uploads the regenerated
direct-dependency inventory for each commit. License conclusions remain
`NOASSERTION` until exact upstream notices and all transitive artifacts are
reviewed; this artifact is not the release SBOM.


## S8 translation-table reference check

The pinned host-only Biopython 1.88 comparison in
`validation/requirements-biopython.txt` and
`validation/genetic_code_biopython_reference.py` checks all 64 codons and the
start/stop sets for the five explicitly implemented tables. Biopython is already
a pinned Android prototype dependency; the validation requirement shares that
version but does not approve any additional runtime dependency. The SPDX
generator records both usage contexts. This check is not evidence of organism
identification or genetic-code inference.


## Host-only RDKit validation pin

`validation/requirements-rdkit.txt` pins RDKit 2025.9.4 for the I1 descriptor
sanity job only. The core RDKit project license is BSD-3-Clause, but this host
wheel is not bundled in the Android app; transitive wheel components and their
notices still require a complete audit before any distribution or product use.


## Host Python versus embedded Python target

The Android build host is pinned to CPython 3.11.18 on the Ubuntu 26.04 runner.
The embedded Chaquopy runtime target remains the separately pinned
`3.11.17-0` distribution. The build host interpreter executes the wheel-builder
scripts; the Chaquopy target controls the Android Python runtime ABI. They are
recorded as separate SBOM entries and must not be conflated.


## Kotlin compiler artifact mirror fallback (build infrastructure only)

The Android settings add a content-filtered Maven Central mirror for the
`org.jetbrains.kotlin` group before Maven Central. It is a build-time fallback
for the Kotlin compiler artifacts whose Maven Central/GitHub delivery returned
HTTP 504 during CI. The filter prevents unrelated dependencies from resolving
through that mirror; Maven Central remains configured afterward. This does not
add a runtime application dependency. Mirror trust, checksum verification and
full transitive dependency auditing remain part of the R1 release gate.


The Gradle 8.13 build script now tries the official direct distribution CDN,
then the official services URL, then an Aliyun mirror for the same version.
Every downloaded archive must match the pre-recorded Gradle 8.13 SHA-256 before
extraction. The mirror is a transport fallback only; it cannot change the
accepted archive bytes.


## First successful arm64 debug package build — 2026-11-08

GitHub Actions run [#1904](https://github.com/AssayFlux/Molecularis/actions/runs/42465569625), commit `30d19ea2bec8a7ad0039eb48fa13ac6bfb6175ed`, produced both debug packages after checksum-verified Gradle 8.13 fallback retrieval:

- APK: 67,678,526 bytes; SHA-256 `0877bfe3331fc596dcaf440f8a659ddf5396c75484e172d2697bf2a7245269f6`.
- AAB: 38,860,218 bytes; SHA-256 `8ec29ece71ffbe3cef13ca3c25c759d4da958898cbdcde1e8ebad0c75b4db7cd`.
- Android JVM unit-test task, APK ZIP alignment, native ELF alignment and package size/integrity checks passed in CI. The APK contains arm64-v8a native libraries, including the embedded CPython 3.11 runtime and Molecularis native library.

This is debug build/package evidence only. No emulator or physical-device installation, offline-runtime, cold-start, memory, thermal or user-flow verification was performed. The build does not close the transitive/file-level license audit or approve Chaquopy, Biopython, SciPy, RDKit or any other engine for production distribution.


## Track G dependency decision register and CI evidence

The current component-by-component decision ledger is maintained at [`docs/track-g/dependency-decision-register.csv`](track-g/dependency-decision-register.csv). Empty artifact hashes, unassigned reviewers, candidate-only entries and NOT-APPROVED redistribution states are deliberate OPEN values; do not fill them with inferred approvals.

The Android CI build now archives:
- the resolved Gradle `debugRuntimeClasspath` dependency report;
- the Rust `cargo tree --locked --all-features` report and `Cargo.lock` SHA-256;
- SHA-256 hashes for cached Maven JAR/AAR/POM/module artifacts.

These files improve traceability but are not a complete SPDX/CycloneDX SBOM, do not yet inventory all Python/native/runtime artifacts, and do not establish license clearance. The source-dependency SPDX document remains a declared-source inventory. G2-01 and G2-02 therefore remain PARTIAL/OPEN until full resolved coverage, exact artifact/license review and redistribution decisions are evidenced.
