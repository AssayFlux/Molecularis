# Molecularis — North Star

**Status:** Owner-directed all-device product direction, updated 2026-11-21. This direction applies to branch Alpha.

## Mission

Build Molecularis as an all-device scientific research platform for phone, tablet, laptop, desktop and workstation. The primary experience is a responsive web application/PWA. Optional desktop packaging and secure local, hosted and institutional compute connectors provide device-appropriate execution.

Molecularis is not an Android project. Android/Kotlin is legacy implementation context and may be retained temporarily for migration, data compatibility or scientific logic extraction, but it is not the future product foundation.

## Preferred engineering languages

The owner's preferred core languages are C++, Rust and Python. C++ owns measured performance-critical scientific kernels. Rust owns safe parsers, validation, secure native services, resource controls and local-node supervision. Python owns scientific orchestration, research APIs, reference implementations and ecosystem adapters. TypeScript/JavaScript remains necessary for browser/PWA presentation and visualization. SQL and declarative schemas support persistence and contracts. Additional runtimes require a concrete need and recorded decision.

## Product principles

- All-device, responsive and accessible.
- Offline-capable where technically appropriate, with clear sync/conflict status.
- Compute-location transparent: users know where data and jobs run.
- Contract-first, modular and versioned.
- Evidence before claims; preserve provenance, uncertainty and limitations.
- Privacy, security and licensing by design.
- Research-use only; no clinical decision support without separate authorization and validation.

## Non-goals

- Android-only product roadmap.
- Browser execution of arbitrary native code.
- Unrestricted shell or arbitrary code execution in API processes.
- Blind copying of entire upstream platforms.
- Treating code availability as proof of model, dataset or redistribution rights.
- Clinical diagnosis, treatment or dosing recommendations under the current scope.


---

## Historical baseline (superseded on Alpha)

The following text is preserved for traceability. Its Android-native product direction is superseded by the all-device direction at the top of this file.

# Molecularis — North Star

**Status:** Owner-approved baseline  
**Last reviewed:** 2026-11-07  
**Authority:** Permanent direction. This file changes only with the project owner's explicit approval and a corresponding entry in `DECISIONS.md`.

## Mission

Build Molecularis as an offline-first, Android-native scientific workbench that makes validated bioinformatics, structural biology, chemistry, enzyme-kinetics, omics and (only through a separately gated path) precision-medicine research tools auditable, reproducible and useful on commodity Android devices, with an optional authenticated and encrypted Remote Compute Node for workloads that do not fit on-device.

## Research thesis

The project must demonstrate, by measurement rather than assumption, that:

1. Selected core analyses execute correctly and usefully on defined commodity Android devices.
2. A capability registry (tool → engine → data pack → domain) makes implementation, validation and device status auditable.
3. Every analysis records machine-readable provenance sufficient to reproduce and compare it.
4. A hybrid on-device / optional remote-node architecture gives users a practical path from phone to larger compute.

No thesis statement becomes a product or paper claim until supported by repository evidence.

## Six tracks

The current sequential execution order is **R → S → I → P → G → U** (D-023). Each track follows the two-step build-then-audit gate; dependencies and independent acceptance evidence remain mandatory.

- **R — Research platform:** Android shell, scientific runtime, registry, data packs, provenance, core tools, validation and release hardening.
- **S — Structure excellence:** structure ingestion/preparation, quality assessment, analysis, variant mapping, offline visualisation and benchmarks.
- **I — In-silico lab:** computational hypothesis generation for chemistry, docking, MD, ADMET and PK/PD, with explicit applicability limits and benchmark evidence.
- **P — Precision medicine:** pharmacogenomics first; research-only pipeline until clinical and regulatory gates are met.
- **G — Governance:** privacy, security, consent, licensing, quality practices, fairness and paper-evidence controls.
- **U — User interface:** accessible, secure and responsive user experience, design system, app shell, research workflows, scientific viewers, settings and usability evidence. Existing partial U0–U3 work is retained; further sequential U implementation follows G.

## Intended users

Primary users are scientists, bioinformaticians, structural biologists, computational chemists, students and research teams. Any future Clinical Decision Support Mode is for licensed clinicians and remains unavailable until all applicable governance, clinical-evidence and regulatory requirements are satisfied.

## Measurable goals

Targets below are acceptance criteria to be measured, not claims that have already been achieved.

1. **Reproducibility:** every validated capability has a versioned validation record, benchmark/test vectors and provenance round-trip test; reproduce-all regenerates all committed paper tables and figures from a clean checkout.
2. **Registry integrity:** CI rejects missing tool/engine/pack/domain references, unsupported status claims, missing validation evidence, missing device logs and clinical-mode exposure without the required gate.
3. **Offline operation:** each capability designated Tier A passes an airplane-mode test on its declared supported device; network activity is limited to explicit public-reference retrieval, user-triggered pack downloads or a separately configured remote node. Public-reference requests must never contain patient data or private research inputs.
4. **Device evidence:** each device-verified capability has a dated test log identifying device model, SoC, RAM, Android version, app/build version and test outcome.
5. **Performance:** every benchmark records runtime and peak memory on named devices; battery/thermal measurements are included where practical. No performance claim without raw benchmark output.
6. **Privacy:** no telemetry by default; no genomic or patient data in logs; local data encrypted at rest; remote traffic authenticated and encrypted; consent and deletion behaviours tested before sensitive-data workflows.
7. **Fairness:** every relevant PGx/variant model or database records ancestry coverage and displays portability limitations; fairness analyses accompany validation.
8. **Release honesty:** README, store text and manuscripts derive claims from registry and benchmark evidence; no invented results, citations or validation.

## Non-goals

- A library, reader or archive of books, papers, tutorials or scraped documents; no bulk documentation corpus.
- Replacing a clinician, autonomously prescribing/dosing/diagnosing, or making emergency decisions.
- Presenting computational predictions as proof of efficacy, safety or clinical utility.
- Shipping Tier-C workloads on constrained Android devices merely to claim mobile capability.
- Runtime downloading of executable code.
- Adding programming languages, engines, databases, models or restrictive dependencies without the specified review and approval.
- Broad disease-treatment recommendations before a separately justified evidence and governance path.

## Operating modes

### Research Mode — default and only mode in public builds

For analysis, exploration, education and publication. Outputs include provenance, uncertainty, limitations and measured performance. Screens and reports state: **“Research use only. Not for diagnosis or treatment decisions.”**

### Clinical Decision Support Mode — future, gated, disabled

Only for evidence-linked decision support reviewed and signed off by a qualified clinician. It remains feature-flagged off in every public build until Part 12 requirements in the originating master specification are completed and approved. The app never autonomously prescribes, doses, diagnoses or makes emergency decisions. Patient-facing material is educational and directs users to discuss results with a clinician; it never gives start/stop or dosing instructions.

## Permanent guardrails

1. No autonomous prescribing, dosing, diagnosis or emergency decisions.
2. No clinical claims without matching validation and regulatory standing.
3. Public builds are Research Mode only.
4. No real patient data before the P0 gate has passed and applicable ethics/legal approvals are documented.
5. In-silico outputs are labelled predictions and accompanied by method, version, parameters, measured benchmark performance and applicability limits.
6. Every dependency, engine, model and data pack has a pinned version and verified license; restrictive licenses require owner approval.
7. No invented numbers, results, references, validations or study claims.
8. No capabilities aimed at designing or enhancing dangerous pathogens or toxins.
9. No bulk books, papers or document collections in the repository.
10. Direction changes require an owner-approved DECISIONS entry; changes to this file require explicit owner approval.
11. Genomic data remains local by default; no upload without explicit user configuration and consent.
12. Human data/participant work requires ethics review or documented exemption before it begins.

## Definition of done

### v0.1.0 alpha

R0–R3 complete and approved: empty-skeleton CI green; R1 feasibility go/no-go evidence accepted by owner; thin offline-capable Android shell and core infrastructure sufficient to import a file, run a cancellable job and inspect provenance; sequence tools, protein properties and enzyme-kinetics capabilities independently validated against published/textbook values and reference implementations; installs and works offline on real supported devices; research-use disclaimer visible. No clinical functionality.

### v1.0.0

Release-hardening track R10 complete: documented supported-device matrix; reproducible clean-checkout build and validation; all shipped capabilities accurately represented in registry; accessibility, low-end performance, crash, privacy and security checks passed; signed Android App Bundle and release artifacts; license register and data-safety/privacy materials match actual behaviour; no unresolved critical/high release-blocking defects; all public builds Research Mode only. Scope and quantitative thresholds must be approved in ROADMAP before the v1.0 gate.

### Clinical-grade release (not currently scheduled or authorised)

A distinct release, not an extension of v1.0 by implication. Requires intended-use statement and jurisdiction-specific legal/regulatory advice; QMS and software lifecycle controls; analytical validity, clinical validity and clinical utility evidence; accredited/validated genotype sources; clinical advisory board; ethics-approved prospective evaluation where required; risk management, usability, audit logs, role-based access, clinician sign-off, incident handling and post-release surveillance; regulatory authorisation/standing for each target jurisdiction as advised by qualified counsel. Clinical Decision Support Mode remains disabled until explicit owner approval after documented evidence review.

## Change control

NORTH_STAR changes only with explicit project-owner approval, a dated DECISIONS entry, and a corresponding ROADMAP update. If a task conflicts with this document, stop and ask rather than silently changing direction.
