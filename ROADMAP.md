# Molecularis — Alpha Roadmap

**Status:** Owner-directed target roadmap for branch Alpha. Milestones are plans, not completion claims.  
**Updated:** 2026-11-21  
**Base:** Alpha created from repository default branch CORE.

## Product direction

Molecularis is an all-device scientific research platform. Responsive web/PWA is the primary interface. Optional desktop packaging, local Molecularis Node, hosted workers and institutional/HPC connectors provide compute. Android-native development is retired as the product direction; useful existing code and data must be audited and migrated safely.

## Current baseline

The current CORE README identifies an Android/Kotlin/Compose application with Python 3.10+, C++17, Rust, Node.js, SQLite, WebView, JSON Schema contracts and scientific foundations in sequence, structure, chemistry/RDKit, docking/Vina, OpenMM, kinetics, omics, pharmacogenomics and governance. The architecture document says its boundaries are intended design, not proof of a complete runtime.

Existing roadmap tracks R/S/I/P/G/U, rulebooks, validation plans, integration register and engineering standard contain reusable work and constraints. Their evidence and current status must be audited at the Alpha base SHA. Preserve research-only and clinical-safety restrictions.

## Milestones

| ID | Milestone | Exit evidence |
|---|---|---|
| M0 | Baseline and branch audit | Base SHA, inventory, build/test/CI baseline, risk register, migration ledger |
| M1 | Cross-device client foundation | Responsive app shell, design tokens, accessibility baseline, PWA install/offline shell |
| M2 | Control plane and identity | Auth, projects/workspaces, API contracts, authorization and audit events |
| M3 | Data and artifact platform | Upload/download, checksums, object storage, metadata, versioning and export |
| M4 | Jobs and orchestration | Durable job state machine, queue, events, cancellation, retries, resource policy |
| M5 | Molecularis Node | Pairing, signed manifests, capability allowlist, local files/CPU/GPU, revocation |
| M6 | Scientific data model | Canonical entities, units, coordinate frames, schemas, provenance and rulebooks |
| M7 | Structure experience | Mol* viewer, structure artifacts, deterministic rendering payloads and validation |
| M8 | Sequence/genomics | Biotite and GWW selective adapters, reproducible sequence workflows |
| M9 | Protein models | ESM and AlphaFold isolated profiles, model/data terms and benchmark gates |
| M10 | Structure validation | MolProbity methods/adapters in audited isolated worker |
| M11 | Chemistry | Open Chemistry components and ChemGraph workflows with reviewable inputs |
| M12 | Molecular dynamics | OpenMM setup, force-field provenance, simulation, analysis and benchmark gates |
| M13 | Notebooks and workflow federation | SciREPL-inspired notebooks and Galaxy API/federation |
| M14 | DNA/RNA nanostructure | NUAD workflows and separate NUPACK license/integration review |
| M15 | Institutional readiness | HPC connectors, deployment, monitoring, backup/restore, security and independent validation |

## Delivery sequence

M0–M6 establish platform and shared contracts. M7–M12 deliver scientific vertical slices in dependency order. M13–M14 add notebook/workflow and specialized design capabilities. M15 prepares institution-scale operations and release acceptance.

The sequence may be adjusted only through DECISIONS.md with explicit rationale. Parallel work is allowed only when dependencies and shared files are controlled.

## Definition of done

A milestone is done only when code, tests, schemas, docs, exact-head CI, security review (where relevant), scientific evidence (where relevant), supported-device evidence and owner acceptance are recorded. A passing build is not proof of scientific validity, device support or release readiness.

## Historical work

Previous R/S/I/P/G/U tracks and their detailed plans are retained as historical/evidence sources until the Alpha baseline audit classifies each artifact as current, superseded, historical or needs-review. Do not delete evidence or silently carry forward old completion claims.
