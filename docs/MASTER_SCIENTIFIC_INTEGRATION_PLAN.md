# Molecularis — Master Scientific Integration Plan

**Status:** Planning baseline; implementation and acceptance are separate.  
**Date:** 2026-11-20  
**Target branch:** `main`

## 1. Purpose

This plan coordinates the proposed integration of desktop compute, structural biology, protein modelling, cheminformatics, molecular simulation, genomics, sequence design and workflow tooling into Molecularis. It is a roadmap, not evidence that any third-party engine is integrated, licensed, scientifically validated, or release-ready.

The Android application remains the research interface. A desktop Linux x86_64 compute host is the first reference target for workloads that exceed mobile resource limits. Existing Android, Python, C++/Rust, JNI and remote-node components should be extended through explicit contracts rather than replaced wholesale.

## 2. Current baseline and constraints

The repository already contains a bounded remote worker, an execution-envelope schema, structure prediction envelope validation, structure-quality observations, a deterministic structure-view payload and an OpenMM adapter. These are foundations, not complete end-to-end scientific products.

Known limitations to preserve in planning:
- The remote worker is not a general-purpose shell or arbitrary-code executor; keep it capability-bounded.
- Prediction envelope validation is not AlphaFold/ESMFold inference. Model weights, runtimes, data and licensing require separate decisions.
- The structure-quality module is not a calibrated MolProbity assessment.
- The OpenMM adapter expects a prepared system/topology/positions; complete preparation and force-field provenance remain work.
- The offline structure viewer is implemented, but physical-device and other acceptance evidence remains open.
- Track U and other existing track gates remain governed by the current roadmap and decision log.

## 3. Integration principles

1. **Contracts first:** versioned JSON Schemas for jobs, capabilities, inputs, outputs, errors and provenance.
2. **One scientific meaning:** shared definitions for sequences, residues, atoms, bonds, coordinates, units, identifiers and uncertainty.
3. **Adapters, not forks:** isolate third-party tools behind Molecularis-owned adapters; avoid wholesale embedding of large upstream applications.
4. **Reproducibility:** record engine/version, parameters, input hashes, reference-data versions, environment and execution host.
5. **Offline-first:** import/export and local execution work without mandatory cloud services; no silent downloads.
6. **Least privilege:** no arbitrary shell access, no implicit network access, bounded resources, explicit cancellation and auditable logs.
7. **Evidence-led claims:** distinguish catalogued, evaluated, licensed, adapted, integrated, tested, reference-validated and platform-verified states.
8. **No gate bypass:** this plan does not alter clinical, privacy, ethics, security, licensing, scientific or release approvals.

## 4. Target architecture

- **Android client:** project/workspace UI, input preparation, capability discovery, consent and data-transfer preview, job submission, progress, result inspection and export.
- **Desktop worker:** Linux x86_64 reference host first; authenticated and encrypted pairing; bounded job queue; capability manifests; isolated engine environments; resource quotas; cancellation and structured logs.
- **Shared contract layer:** job envelope, engine manifest, capability manifest, result envelope, provenance and error schemas.
- **Scientific core:** deterministic validation and data transformation; engine-specific computation stays behind adapters.
- **Engine environments:** independently pinned profiles for incompatible Python, PyTorch, JAX, CUDA and native dependency stacks.
- **Viewer layer:** offline-capable molecular/structure visualization consuming Molecularis-owned result payloads.
- **Governance layer:** third-party register, license evidence, security review, benchmark fixtures and acceptance records.

## 5. Proposed integration order

| Phase | Scope | Exit evidence |
|---|---|---|
| P0 | Baseline audit, contracts, ownership and risk register | Exact source baseline, dependency inventory, approved ADRs and scoped acceptance criteria |
| P1 | Shared scientific data foundation | Schema tests, reference fixtures, unit/coordinate/identifier consistency |
| P2 | Desktop worker and Android interoperability | Paired host, offline package round-trip, auth, quotas, cancellation and audit tests |
| P3 | Structure biology and visualization | Biotite adapter, viewer integration, geometry cross-checks and device evidence |
| P4 | Protein intelligence and prediction | ESM/AlphaFold isolated profiles, model/data licence review, benchmark and uncertainty evidence |
| P5 | Cheminformatics | RDKit and selected Open Chemistry components behind stable molecule contracts |
| P6 | Molecular simulation | Prepared-system pipeline, parameter provenance, OpenMM reference comparisons and bounded execution |
| P7 | Genomics and nucleic-acid design | Validated sequence workflows, provenance and dependency/licence review |
| P8 | Workflow and notebook experience | Reproducible workflow manifests, safe execution model and audit trail |
| P9 | Cross-platform and release validation | Security, scientific, licence, performance, usability and platform acceptance reports |

The phases are dependency-ordered proposals, not commitments to fixed dates. Work may overlap only when the existing project sequencing decisions and dependencies permit it. The current project track order and two-step gates remain controlling; this plan does not silently reorder them.

## 6. End-to-end reference workflows

A. FASTA → sequence validation → optional ESM/AlphaFold job → prediction-result validation → structure viewer → provenance report.

B. PDB/mmCIF → structure parsing → geometry observations → independent validation comparison → viewer → reproducibility record.

C. Prepared molecular system → topology/force-field validation → bounded OpenMM simulation → trajectory/report → reproducibility record.

D. SMILES/SDF → molecule validation → RDKit descriptors/graph operations → selected calculator → molecule viewer → provenance.

E. FASTA/FASTQ → sequence QC → alignment/annotation/variant workflow where supported → result validation → provenance.

F. DNA/RNA design constraints → nuad adapter if selected and cleared → independent thermodynamic evaluation only where dependencies and rights permit → design report.

Each workflow must define valid inputs, rejected inputs, output schema, scientific references, resource bounds, failure modes and acceptance thresholds before being presented as supported.

## 7. Acceptance ladder

Use these explicit states in registers and reports:

`not_assessed → evaluated → license_cleared → adapter_developed → integrated → automated_tested → reference_validated → platform_verified`

A state may not be skipped. “Integrated” does not imply scientific validation; automated tests do not imply reference validation; host success does not imply Android/device support.

## 8. Security, privacy and safety requirements

- Pairing must use authenticated encrypted transport; non-loopback worker exposure requires TLS and strong identity handling.
- Provide a user-visible preview of data leaving Android before remote execution, including files, metadata, destination and retention.
- Do not transmit patient or other sensitive data unless the exact approved protocol, environment, consent/waiver and legal requirements authorize it.
- Keep patient data out of source control, issues, pull requests, CI, fixtures, logs and public artifacts.
- Encrypt imported payloads and review encryption coverage for job metadata, saved results, temporary files, backups and logs.
- Enforce per-engine allowlists, CPU/RAM/disk/time limits, queue limits, cancellation and output-size limits.
- Do not automatically fetch models, datasets, executables or reference packs.
- Review dependency vulnerabilities, SBOM, signatures/hashes and licence obligations before distribution.

## 9. Governance and deliverables

The companion documents define desktop architecture, engine integration, scientific rulebook, validation, runtime profiles, third-party register and milestones. Every engine proposal must have an owner, scope, upstream version, licence evidence, dependency profile, input/output contract, benchmark fixture, security review and explicit disposition.

## 10. Non-goals

This plan does not authorize clinical decision support, clinical deployment, patient-data processing outside existing approvals, automatic model downloads, arbitrary remote code execution, wholesale deployment of Galaxy, or bundling third-party weights/data without review.

## 11. Change control

Changes to execution order, engine tier, license posture, data source, regulatory posture or product scope require a recorded decision in `DECISIONS.md`. Implementation must follow the current roadmap and the project’s two-step build/audit discipline.
