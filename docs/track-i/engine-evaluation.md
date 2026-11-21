# Track I — engine and data-source evaluation

**Review date:** 2026-11-11  
**Scope:** research-only host execution candidates. This record is not legal advice or scientific validation.

## Docking — AutoDock Vina

**Selected host adapter:** AutoDock Vina 1.2.7, Python binding pinned as `vina==1.2.7`.

- Official project documentation identifies Apache License 2.0 for the source: https://autodock-vina.readthedocs.io/en/latest/
- Release tag: https://github.com/forlilab/AutoDock-Vina/releases/tag/v1.2.7
- Pinned source commit: `8eb40404f4f45608acb3b01427587ac049f27c1f`.
- PyPI lists the Python package as Apache-2.0, but reports no package provenance attestation for the 1.2.7 files: https://pypi.org/project/vina/1.2.7/.
- The bounded adapter accepts only caller-prepared PDBQT, hashes both inputs, hashes the installed Vina wrapper binary, fixes the CPU/seed/search-box protocol and stores each pose with a SHA-256.
- A 1IEP example receptor/ligand fixture is pinned to the upstream v1.2.7 source tree for a deterministic engine smoke check. This check is not redocking validation, decoy enrichment or evidence of binding affinity.
- `remote-node/` now contains a Node 22 worker with bearer authentication, loopback-only default binding, TLS-required remote binding, a single-job limit, request/result caps, timeout and an allow-listed Python child environment. Docking is disabled by default and requires explicit host configuration. The worker has not been deployed to a project compute node.

**Decision:** proceed with the pinned host adapter and CPU smoke check. Do not bundle into Android. Before a production compute service is exposed, verify the complete transitive binary/dependency licence inventory, package provenance, security posture, resource isolation and input/data rights.

## Molecular dynamics — OpenMM

**Selected host adapter:** OpenMM 8.6.1, pinned as `openmm==8.6.1`, CPU platform only.

- Official release: https://github.com/openmm/openmm/releases/tag/8.6.1
- Official license guide: https://docs.openmm.org/latest/userguide/library/01_introduction.html
- OpenMM documents the API, low-level API, Reference, CPU and application layers under MIT; CUDA, HIP and OpenCL platforms are LGPL. The project also includes separately licensed third-party components.
- The PyPI 8.6.1 distribution reports no provenance attestation: https://pypi.org/project/OpenMM/8.6.1/.
- The Molecularis adapter accepts already-constructed OpenMM System/Topology/position objects, refuses arbitrary XML input, uses the CPU platform, records engine-binary and protocol hashes, runs independent seeded replicas and emits bounded DCD artifacts.
- `python/molecularis/md_openmm.py` executes trusted, already-constructed OpenMM systems on the CPU platform, runs independently seeded replicas and emits bounded DCD artifacts with engine/protocol/input provenance.
- The CI smoke system is a synthetic two-particle harmonic bond. It verifies engine execution, serialization, replica creation, DCD output and schema only. It is not a biomolecular force-field benchmark.

**Decision:** proceed with CPU-only adapter and synthetic engine smoke. CUDA/HIP/OpenCL are excluded. Do not select or bundle a protein/ligand force field until the exact parameter release, source, redistribution terms, supported chemical domain and validation benchmarks are recorded. No NPT run is possible unless the supplied System has periodic boundary conditions.

## Alternative MD engine — GROMACS

GROMACS 2026.4 is an available alternative and identifies LGPL-2.1-or-later in its project citation metadata: https://gitlab.com/gromacs/gromacs. It is not selected for this increment because a second engine would duplicate integration and validation work before the OpenMM CPU adapter and force-field provenance gates are satisfied. Re-evaluate if production workload, platform or force-field support requires it.

## ADMET data candidates

| Source | Public evidence / known terms | Molecularis intake decision |
|---|---|---|
| ChEMBL | CC BY-SA 3.0; attribution and share-alike obligations apply. Commercially derived calculated properties may have additional terms. https://chembl.gitbook.io/chembl-interface-documentation/frequently-asked-questions/general-questions | Candidate only; pin release, exclude/segregate restricted calculated properties, preserve citations and review share-alike implications before intake |
| PubChem BioAssay | NCBI provides policy and depositor guidance, but the catalogue may contain depositor-submitted material with record-specific provenance. https://pubchem.ncbi.nlm.nih.gov/docs/policy-and-guidelines | Candidate only; verify record-level depositor rights and source terms; do not assume one blanket licence |
| Tox21 | Official programme makes public assay data downloadable with assay descriptions and protocols. https://tox21.gov/data-and-tools/ | Candidate only; public accessibility is not treated as a blanket reuse licence; obtain exact release and terms review |
| FDA DILIrank 2.0 | FDA describes 1,336 FDA-approved drugs and four DILI concern categories. https://www.fda.gov/science-research/liver-toxicity-knowledge-base-ltkb/drug-induced-liver-injury-rank-dilirank-20-dataset | Candidate only; preserve FDA label/literature provenance and ambiguity category; verify reuse terms and endpoint definitions |

The software now includes Bemis-Murcko scaffold-group splitting, binary ROC-AUC/average-precision/Brier/calibration summaries and Morgan/Tanimoto nearest-neighbour applicability-domain utilities. The pinned RDKit CI smoke uses synthetic molecules only. Acyclic molecules fall back to canonical-SMILES grouping, so related acyclic series may still cross partitions. These utilities do not train or select a model.

No dataset payload has been downloaded or ingested by this decision. No model is trained or selected. Public availability alone does not satisfy licence, endpoint, quality, leakage, applicability-domain, calibration, uncertainty or external-validation gates.

## Remaining gates

1. Complete SBOM and transitive licence/provenance review for pinned Vina and OpenMM distributions.
2. Establish a secured, resource-limited compute service and storage policy before remote execution.
3. Obtain independently curated redocking/cross-docking and decoy-enrichment benchmarks for docking.
4. Validate MD against an independently prepared molecular system, force-field-specific reference energies, timestep convergence, equilibration, replica stability and reproducibility.
5. Review each force-field and parameter source independently; engine licence does not grant parameter/data rights.
6. Approve exact data releases and source terms before ADMET intake; build leakage-resistant external validation and abstention before any predictive model.
7. Keep P0 and all patient/clinical use blocked.
