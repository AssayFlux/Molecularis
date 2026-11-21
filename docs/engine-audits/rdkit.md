# RDKit upstream and adapter audit

**Review date:** 2026-11-21  
**Molecularis target:** `CORE`  
**Disposition:** retain the existing optional host adapter; do not bundle in Android or treat descriptor fixtures as scientific validation  
**Scope:** upstream source/licence, Molecularis adapter, pinned reference job and integration gaps

## Upstream identity and licence

- Repository: https://github.com/rdkit/rdkit
- Reviewed branch: `master`
- Reviewed upstream commit: `61b33d460cf4ced9cf5024a933f0e89f3316f410` (2026-11-20)
- Reviewed upstream licence: BSD 3-Clause, `license.txt`
- The licence requires retaining the source notice and reproducing the notice/conditions/disclaimer for binary distributions. The non-endorsement condition also applies.
- The reviewed CMake configuration uses C++20 and has many optional build components. It supports multiple wrapper/build configurations; that flexibility does not establish Android arm64 compatibility or a small redistributable runtime.
- The reviewed latest commit fixes an out-of-bounds read in MolPickler depickling and adds a regression test. Molecularis's adapter does not use RDKit pickle deserialization, so this specific change is not evidence of an exploitable path in the current adapter. It is a useful reminder that exact native release selection and security update monitoring matter.

## Current Molecularis integration

- Optional adapter: `python/molecularis/chemistry_rdkit.py`
- Host-only pin: `validation/requirements-rdkit.txt` declares `rdkit==2025.9.4`.
- Reference job: `validation/chemistry_reference.py`, using small fixed molecule fixtures and an explicit-atom cyclopropane SDF graph comparison.
- Existing register: `docs/third-party.md` records RDKit as a candidate, not approved for product bundling.
- The adapter imports RDKit lazily, reports the active version, applies bounded UTF-8 input checks, sanitizes molecules, reports canonical isomeric SMILES, descriptors, Morgan fingerprints, stereocentres and provenance hashes.
- The adapter deliberately does not infer protonation or tautomer states and labels its Rule-of-Five output as a heuristic physicochemical screen, not a prediction of ADMET, safety, efficacy or clinical suitability.

## What is already useful

The current design is directionally sound:

1. RDKit is optional and not imported by the base package.
2. The engine version is returned with results.
3. SMILES and mol-block input sizes are bounded before parser invocation.
4. Invalid parse results and non-finite descriptors are rejected.
5. Output records the input SHA-256, sanitization/canonicalization assumptions, units and known interpretation limits.
6. The reference fixture checks basic identity/formula/descriptors, fingerprint configuration and one small graph/coordinate comparison against RDKit.

This is a good starting adapter, not a complete chemistry platform.

## Gaps to close

### Scientific and representation gaps

- The fixture set is intentionally tiny (ethanol, benzene and a small synthetic graph comparison). It does not validate stereochemical edge cases, isotopes, salts/mixtures, aromaticity alternatives, charged tautomers, organometallics, query molecules, atom mapping, reaction semantics, conformer generation or 3D descriptors.
- The local graph parser and RDKit do not have identical chemistry semantics. In particular, the current fixture explicitly avoids asserting equality for implicit-hydrogen formula inference. Preserve this distinction; do not force false parity.
- Morgan fingerprints must carry the exact radius, bit length, chirality/features options, RDKit version and preprocessing policy. Similarity is representation-dependent and is not biological activity or binding affinity.
- Rule-of-Five pass/fail is not ADMET prediction. Do not use it to rank candidates as safe, effective or clinically suitable.
- Canonical SMILES is version/model-dependent. Persist source input and engine/version; do not replace original user input with canonical output.
- No validated protonation, tautomer, salt-stripping, stereochemical normalization or conformer workflow is present. These need explicit policy and reference fixtures before use.

### Input and runtime safety

- The 1 MB SMILES and 10 MB mol-block ceilings bound raw text size but do not alone bound molecular graph complexity or native parser CPU/memory. Add post-parse atom/bond/ring ceilings and worker-level CPU, memory, timeout and cancellation controls. Consider stricter format-specific limits before exposing this adapter to untrusted uploads.
- Do not expose RDKit binary pickle loading for untrusted content. The latest upstream security fix in MolPickler makes it especially important not to add a pickle pathway casually.
- Run untrusted parsing in a bounded worker process for production workloads. A Python exception boundary is not native-code isolation.
- Keep all network access disabled for this local parser/descriptor adapter.

### Packaging and licensing

- The current exact pin is a host validation dependency, not a release lock or proof of all wheel contents.
- Resolve and record the complete wheel/transitive dependency graph, hashes, notices and licence obligations for each supported platform.
- RDKit's BSD-3-Clause core licence does not automatically clear every optional/contributed component or external dependency.
- Android arm64, 16 KB page-size compatibility, JNI/runtime integration, native binary footprint and offline distribution remain untested and unapproved.

## Recommended next steps

1. Keep RDKit in the optional host-only profile; do not add it to base `pyproject.toml` dependencies.
2. Refresh the pinned release deliberately after reviewing release notes and security fixes. Do not pin an unreviewed development branch or silently upgrade based on the latest commit.
3. Expand deterministic fixtures for stereochemistry (specified/unspecified and tetrahedral/cis-trans), isotopes, formal charges, salts/mixtures, aromatic and aliphatic rings, valence/sanitization failures, isotopic mass, explicit/implicit hydrogen behavior and multi-fragment inputs.
4. Add adversarial/resource fixtures and post-parse ceilings for atoms, bonds, rings and descriptor runtime; test worker timeout and process termination.
5. Define a versioned Molecularis molecule/result schema with explicit atom/bond identity, stereochemistry, charge, isotope, conformer coordinates/units, fragment policy, sanitization state and provenance. Preserve original source text and hash.
6. Separate descriptor, fingerprint, substructure, conformer, reaction and property-prediction capabilities into distinct adapter contracts; do not let one generic “chemistry result” imply all are supported.
7. Complete transitive licence/SBOM and host platform verification. Evaluate Android only as a separate native feasibility project with measured APK/AAB size and device runtime evidence.

## Decision

**Retain the current optional RDKit adapter and host fixture job, then deepen molecule-schema and scientific edge-case coverage.** Do not replace the dependency-free chemistry core, make RDKit mandatory, or bundle it in Android. The current integration demonstrates selected RDKit operations on small fixtures; it does not establish broad chemical correctness, ADMET validity, Android support or release approval.

This is a source and adapter audit. It does not claim that a new RDKit version was installed, the upstream security fix was backported, benchmarks were run or the current validation job was executed during this review.
