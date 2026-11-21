# Molecularis release plan — v0.1.0 baseline and v0.1.1 next release

**Planning baseline:** `main` at `a799f6619c080ee1695784faf01e60fef6405504` (2026-11-18).
**Release policy:** version metadata may identify the v0.1.0 target, but no GitHub Release or immutable tag is to be published until every v0.1.0 acceptance gate below passes on the exact release commit.
**Product mode:** research-only. No clinical diagnosis, treatment, dosing, patient interpretation or clinical decision support is included.

## 1. Release intent

- **v0.1.0 — Basic working model:** a small, honest, installable Android research workbench. It proves the end-to-end application foundation, local data handling, a few real scientific workflows, result/provenance display and reproducible packaging. It does not claim that every registered capability is available from Android.
- **v0.1.1 — Integration, usability and scientific foundation:** close the remaining app-shell, workflow, navigation, accessibility, device and reproducibility gaps discovered during v0.1.0 testing.
- **Included in the same v0.1.1 release:** scientific rulebook and generation foundation — introduce the first executable, versioned scientific rulebooks and shared computational interfaces. This is an architecture and bounded-engine release, not a promise of universal biological prediction.

## 2. v0.1.0 — Basic working model

### Included scope

1. **Android application shell**
   - Native Kotlin/Jetpack Compose app; Home, Work and Settings.
   - Owner-approved Premium Minimal Monochrome V1 design authority (D-024); semantic decision colours only where needed for status.
   - Honest empty, loading, running, success, partial, failed and cancelled states for workflows that are actually enabled.
   - No simulated cloud account, fake progress, fabricated data or inert controls presented as functional.

2. **Local research workspace**
   - SAF-based user-selected file import/export.
   - Durable job state, cancellation/recovery behaviour where implemented, SHA-256 input identity and provenance.
   - Encrypted input handling and explicit Keystore-loss/recovery disclosure.
   - Clear privacy and research-only notices.

3. **Small set of real, bounded scientific workflows**
   - FASTA parsing and sequence quality/statistics.
   - FASTQ quality summary only with explicit Phred+33 or Phred+64 selection.
   - Basic sequence/protein utilities only where the Android dispatcher, input contract, result contract and tests are connected.
   - PDB/mmCIF structure viewing and SDF/MOL graph preview only as bounded visualization/inspection capabilities; no claim of de-novo protein folding or chemically complete 3D modelling.
   - Public database retrieval only where source, format, licence/terms, size limits, provenance and failure behaviour are documented.

4. **Engineering and reproducibility**
   - Python package and Android app version metadata set to 0.1.0.
   - Exact-head CI, Python tests/type/lint/governance checks, Android ARM64 APK build, JVM tests, native alignment/package checks and artifact SHA-256.
   - Reproducible build instructions, release notes, dependency inventory and explicit third-party notices.
   - Capability registry labels must distinguish source implementation, Android availability, validation evidence and external/device acceptance.

### Explicitly not included / not claimed

- Every one of the registered capabilities being runnable from Android.
- De-novo protein folding or validated structure prediction generated solely from first principles.
- Clinical PGx interpretation, patient-specific recommendations or clinical workflows; P0 remains NOT APPROVED.
- Validated molecular docking, biomolecular molecular dynamics, ADMET prediction or force-field coverage unless separately benchmarked and licensed.
- Full genome annotation, production-grade variant calling, comprehensive transcriptomics or exhaustive reference-database coverage.
- Independent scientific validation, regulatory clearance, security certification or broad device compatibility without the required evidence.
- Remote compute, cloud identity or cloud synchronization unless separately designed, secured and approved.

### v0.1.0 acceptance gates (all required before publishing)

- [ ] A clean checkout of the exact release commit builds the debug APK successfully; no cancelled or partial workflow counts.
- [ ] APK exists, is non-empty, installable and package-inspected; SHA-256, build environment and artifact are archived. AAB is required only if the release channel uses it.
- [ ] Android JVM tests and all required Python tests pass on the exact commit; skipped tests are explained.
- [ ] Native libraries pass the configured ELF / 16 KB alignment checks.
- [ ] Fresh install and upgrade path, SAF import/export, job cancellation/recovery, app relaunch and data integrity are exercised on at least one named ARM64 device and a supported emulator.
- [ ] The enabled FASTA and FASTQ workflows complete from user-selected file to persisted result and provenance, with malformed/oversized input rejection tested.
- [ ] Every visible action is functional or explicitly disabled with an explanation; registry-to-Android dispatcher parity is documented.
- [ ] Owner UI blueprint comparison, basic accessibility (contrast, touch targets, TalkBack labels and large text) and light/dark theme checks are recorded.
- [ ] Runtime permissions, merged manifest, backup/network behaviour, data deletion limits and third-party licenses/notices are reviewed.
- [ ] Release checklist is updated with evidence; owner explicitly accepts the release.

**Current disposition:** NOT RELEASED. The repository's Track U audit records U0–U3 partial, U4 bounded integration with device/science acceptance open, U5 partial/gated and U6 not passed. The release checklist also records NOT RELEASE READY. These are blocking evidence gaps, not paperwork to waive.

## 3. v0.1.1 — Scientific rulebook and computational generation plan

This workstream is part of the same v0.1.1 release as the integration/usability hardening scope above. The two workstreams are combined under one version number; there is no later v0.1.2 release in this roadmap.

### Architectural objective

Build a shared scientific execution substrate plus domain-specific, machine-readable rulebooks. Avoid one bespoke application for every molecule or analysis. Reuse common representations, units, geometry, numerical methods, provenance and validation, while keeping domain assumptions explicit.

### Shared scientific substrate

1. **Scientific object model:** typed atoms, bonds, residues, nucleotides, sequences, chains, molecules, reactions, compartments, coordinates, units and metadata.
2. **Rulebook format:** versioned machine-readable definitions with identifiers, scope, preconditions, constraints, equations, parameters, units, algorithms, dependencies, expected outputs, uncertainty, citations, licence and validation fixtures.
3. **Execution contract:** typed input/output envelopes, deterministic parameter capture, resource budgets, cancellation, logs, provenance, engine/version identity and structured failure/abstention.
4. **Data/reference layer:** downloadable or user-provided public datasets and reference packs with source release, checksum, schema, licence/terms, update policy and offline indexing. Do not bundle or redistribute data without rights review.
5. **Numerical and geometry layer:** vector/matrix operations, coordinate transforms, distance/angle/torsion calculations, optimization, statistics, numerical integration and unit-aware quantities.
6. **Validation layer:** curated synthetic fixtures, public benchmark datasets where licensed, independent reference comparisons, tolerances, regression tests and uncertainty reporting.
7. **Presentation layer:** 2D/3D viewers and scientific reports consume typed outputs; visualization must not imply stronger evidence than the underlying method.

### Initial rulebook families

| Rulebook family | Foundational rules and methods | First bounded generator/analysis |
|---|---|---|
| Chemical graph and organic chemistry | Elements, isotopes, valence, formal charge, bond order, aromaticity, stereochemistry, functional groups, reaction templates and atom/bond invariants | Validate/build small molecular graphs; canonicalize supported formats; calculate transparent descriptors |
| Nucleic acids | Nucleotide chemistry, strand direction, complementarity, codon tables, transcription/translation and sequence alphabet rules | Construct/validate sequence objects, reverse complements, translation and ORF reports |
| Protein chemistry | Amino-acid residue templates, peptide connectivity, backbone/side-chain atoms, bond geometry, torsion angles, stereochemistry and residue variants | Build chemically explicit peptide backbones/fragments and validate geometry; not claim native folding |
| Structural biology | PDB/mmCIF semantics, coordinate frames, atom/residue identity, contacts, geometry, secondary-structure annotations and quality metrics | Build structure objects, calculate geometric features and render validated coordinates |
| Biochemical reactions and enzymes | Stoichiometry, mass/charge balance where defined, reaction direction, Michaelis–Menten and kinetic models | Validate reaction equations and simulate bounded kinetic systems |
| Molecular interactions | Molecular representations, scoring assumptions, steric constraints, electrostatics and search/optimization methods | Transparent interaction feature calculations and benchmarked docking adapter; scores are not binding truth |
| Molecular dynamics | Force-field parameterization, energy functions, constraints, integration, ensembles and thermodynamic assumptions | Adapter-based simulation only with an explicitly supported, licensed/validated force field and reference system |
| Pathways and systems biology | Reaction networks, stoichiometric matrices, mass balance, ODEs, flux constraints and regulatory edges | Construct SBML-compatible pathway/network models and run small deterministic simulations |

### Generation versus prediction

The engine must label output class precisely:

- **Rule-based construction:** deterministic structures from explicit chemical/biological rules and supplied inputs.
- **Physics-based calculation/simulation:** results depend on parameterized models, boundary conditions and numerical approximations.
- **Statistical inference:** estimates derived from observed data and an explicit statistical model.
- **AI prediction:** model-generated outputs with model identity, training/data provenance where available, confidence/uncertainty and domain limits.
- **Database retrieval:** an existing record, never described as locally generated.

A rulebook alone cannot uniquely determine a protein's native fold or every biological outcome. Those tasks require additional evidence, trained models, physics-based computation or experimental data. Molecularis must not blur these categories.

### v0.1.1 staged implementation

- **Stage A — Rulebook schema and validator:** define JSON Schema/Pydantic-style typed contracts, versioning, citations, units, preconditions, dependency and test-fixture metadata.
- **Stage B — Shared chemistry kernel:** atom/bond graph, valence/charge checks, coordinate and geometry primitives, supported molecule serialization, unit tests against independently curated fixtures.
- **Stage C — Sequence and residue object model:** DNA/RNA/protein typed objects, codon tables, residue templates, peptide connectivity and provenance-preserving transformations.
- **Stage D — First generators:** deterministic small-molecule graph construction and peptide/backbone fragment construction; strict size/element/valence/geometry bounds.
- **Stage E — Structural analysis and visualization:** coordinate models, contacts, geometry, confidence/quality metadata and viewer contracts.
- **Stage F — Reaction/pathway model:** stoichiometric validation and small kinetic simulations.
- **Stage G — Prediction/simulation adapters:** integrate external/open-source engines only after ABI, license, data, benchmark, resource and device feasibility gates. AI model weights are separate governed artifacts, not silently downloaded.
- **Stage H — Benchmark and release:** independent reference concordance, reproducibility, performance/resource tests, licensing and documented scientific limitations.

### v0.1.1 exit criteria

- [ ] Rulebook schema is versioned, validated and documented with at least one executable rulebook in each delivered family.
- [ ] Shared scientific object model has explicit units, coordinate conventions, stable identifiers and serialization tests.
- [ ] Every generator produces deterministic, provenance-rich outputs for fixed inputs/parameters, or documents stochastic seeds.
- [ ] Chemical valence/charge and geometry checks reject invalid structures and explain why.
- [ ] Peptide construction fixtures agree with independent reference geometry within declared tolerances.
- [ ] Reaction stoichiometry and kinetic simulations pass analytic/reference comparisons.
- [ ] Every prediction/simulation adapter has source/license/model/force-field metadata, resource bounds and benchmark evidence.
- [ ] Visualizers display provenance, method class, quality/confidence and limitations.
- [ ] No clinical capability is enabled by this release.

## 4. Versioning and release discipline

- v0.1.0 is the first basic working research model.
- v0.1.1 combines integration/usability hardening with the first shared rulebook/generation substrate and bounded generators.
- Do not create or move release tags to a commit that has not passed its exact-head gates.
- Never mark a capability validated merely because code, a dataset, a model or a viewer exists.
