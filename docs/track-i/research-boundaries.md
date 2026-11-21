# Track I — Research boundaries and evidence gates

**Status:** governance and implementation contract. No clinical capability is implied.

## I1 — Molecular descriptors

Descriptor calculations must state the chemical representation, canonicalization policy, protonation/tautomer assumptions, stereochemistry handling, aromaticity model, units and engine/version. Preserve raw input and parsed structure. Invalid valence, unsupported elements, ambiguous stereochemistry and parse warnings must be visible. Cross-engine agreement is not assumed; compare against pinned reference fixtures and report tolerances per descriptor.

## I2 — Docking

Remain gated until a supported engine, exact version, licence, reproducible installation, receptor/ligand preparation protocol, protonation policy, search-space definition, random seeds and independent redocking/cross-docking benchmarks are approved. Scores are not binding affinities or proof of activity.

## I3 — Molecular dynamics

Remain gated until engine and force-field licences, parameter provenance, hardware requirements, deterministic/reproducible protocol, equilibration, replicate strategy and independent validation are documented. A trajectory is not evidence of biological efficacy.

## I4 — ADMET / PK / PD / PBPK

Maintain a source-and-model inventory with applicability domain, training-data provenance, version, units, calibration, uncertainty and external validation. Out-of-domain inputs must trigger abstention. Predictions are research hypotheses and must not be used for treatment or dosing decisions.

## I5 — Variant and virtual-cohort research

Use public, appropriately licensed, non-patient datasets only during preparation. Define ancestry/population limitations, missingness, ascertainment, linkage/phasing assumptions, uncertainty and fairness checks. Do not infer an individual's clinical risk or recommend treatment.

## Hard boundary

Under D-025 (2026-11-18), the owner authorizes engineering and patient-data research testing within the institutional approval the owner declares has been obtained. The approval reference and scope remain pending attachment. Patient data must stay within the approved environment and out of GitHub/CI/logs. Clinical interpretation, diagnosis, treatment recommendations and clinical mode remain separate, disabled activities.


## I4 — ADMET / PK / PD / PBPK source inventory (preparation only)

Candidate public sources for future evidence mapping are recorded below. This is a discovery inventory, not an approved training set or validated model catalogue:

| Source | Candidate research use | Intake status |
|---|---|---|
| PubChem BioAssay | Assay metadata and bioactivity observations | License, assay quality, provenance and release review required |
| ChEMBL | Curated bioactivity records and target/compound links | Exact release and applicable terms review required |
| Tox21 | Public high-throughput toxicity screening records | Exact release, assay endpoint and reuse terms review required |
| FDA DILIrank | Published drug-induced liver injury classification resource | Version, source provenance and reuse terms review required |

No source has been downloaded, licensed, curated, or approved by this inventory. No ADMET/PK/PD/PBPK prediction model is selected. Before intake, record the exact release, original source URL, license text and review decision, SHA-256, endpoint definitions, units, assay context, exclusions, missingness, applicability domain and intended non-clinical use. Any future model requires leakage-controlled splits, external validation, calibration/uncertainty, out-of-domain abstention and bias review. No dosing, treatment or patient-level prediction is permitted.


Machine-readable I4 preparation: `data/admet-source-catalog.yaml` and `api/admet-source-catalog.schema.json` record PubChem BioAssay, ChEMBL and Tox21 as candidates only. The schema requires `verify_before_intake`, `patient_data: false`, and currently prohibits acquired data entries (`maxItems: 0`). Exact releases, license review and endpoint curation must precede any intake.


## I1 — implementation note (2026-11-09)

The optional host RDKit adapter records exact input-text SHA-256/UTF-8 length and
states its sanitization, canonical isomeric representation, protonation, tautomer,
aromaticity, stereochemistry, hydrogen and descriptor-unit assumptions. The input
is passed to the RDKit parser without preprocessing; protonation and tautomer states
are not corrected or inferred. This is provenance disclosure, not a validated
chemistry benchmark or evidence of biological activity. RDKit remains unbundled
from Android pending ABI, license, dependency and size review.


## I1 — molecular descriptor adapter hardening (2026-11-11)

The optional host RDKit adapter now enforces input limits on encoded UTF-8 bytes rather than Python character count: 1 MiB for SMILES and 10 MiB for mol blocks. It rejects embedded NUL and invalid Unicode scalar input before parser invocation. Morgan similarity validates integer-only radius/bit parameters and applies the same per-input byte ceiling.

Descriptor schema version 2 adds formal charge, heavy-atom count, aromatic-atom count, aliphatic/aromatic ring counts and fraction Csp3, alongside molecular formula/weight, exact mass, Crippen LogP, TPSA, H-bond donors/acceptors, rotatable bonds and ring count. It also reports a transparent four-criterion Rule-of-Five heuristic (MW, Crippen LogP, HBD and HBA) with each threshold and pass/fail result; it is not an absorption, bioavailability, safety or efficacy prediction. Units and representation assumptions are explicit; raw input SHA-256 and exact UTF-8 byte length are retained. The pinned ethanol/benzene sanity fixtures now cover the added descriptors.

**Boundary:** RDKit remains host-only and is not bundled into Android. This increment does not establish descriptor accuracy beyond the named deterministic fixtures, chemical validity across all representations, bioactivity, ADMET, docking or clinical utility. License/transitive dependency review, Android ABI/size feasibility, wider curated chemical reference sets and device integration remain open.


## I-track engineering increments (2026-11-11)

- **I1:** Android accepts one bounded local SDF/MOL document for graph-only preview. Explicit-atom formula/mass and graph counts are reported with source SHA-256. This parser does not sanitize chemistry, infer implicit hydrogens, interpret stereochemistry/aromaticity or replace the separate host RDKit adapter.
- **I2:** `python/molecularis/docking_vina.py` provides a bounded AutoDock Vina 1.2.7 host runner for caller-prepared PDBQT, with input/protocol/engine/pose hashes and a strict result schema. `remote-node/` contains an authenticated, loopback-by-default Node worker that is disabled by default and exposes only docking. The pinned 1IEP job verifies engine execution and deterministic replay, not redocking accuracy or decoy enrichment. The separate job envelope remains non-executable until a secured node and dependency audit are approved.
- **I3:** `python/molecularis/md_openmm.py` provides an OpenMM 8.6.1 CPU-only runner for trusted, already-constructed System/Topology/positions. It executes seeded replicas, hashes the CPU engine/protocol/inputs and returns bounded DCD artifacts. CI uses a synthetic two-particle harmonic system only; no biomolecular force field is bundled or selected, and the Node worker explicitly reports MD disabled.
- **I4:** `python/molecularis/pkpd.py` supplies a single-dose first-order one-compartment oral PK equation (including the equal-rate continuous limit) and an Emax concentration-effect relationship. A pinned SciPy DOP853 ODE comparison independently checks the closed-form PK implementation. Added Bemis-Murcko scaffold-group splitting, ROC-AUC, average precision, Brier score, calibration-bin summaries and Morgan/Tanimoto applicability-domain utilities, with a pinned RDKit smoke check. The metadata-only source catalogue now includes PubChem BioAssay, ChEMBL, Tox21 and FDA DILIrank 2.0; all remain `verify_before_intake`, with zero acquired entries. No ADMET model is trained or selected.
- **I5:** `python/molecularis/virtual_cohort.py` provides seeded aggregate Hardy-Weinberg genotype counts and a separate caller-supplied additive-effect simulation with aggregate genotype-stratified trait summaries. No individual genotypes or phenotypes are returned; effect sizes are inputs, not learned or predicted; no ancestry, linkage, penetrance or clinical risk is modelled.

These are engineering primitives and engine smoke checks, not a scientific validation package. The I-track exit remains open pending exact-head CI, I1 physical-device verification and wider chemical reference sets, secure Node deployment and complete transitive engine dependency review, licensed biomolecular force-field parameters and independent I2/I3 redocking/MD benchmarks, curated I4 datasets/models with leakage-controlled external validation, and I5 public-cohort governance/fairness/independent validation. Patient-data research testing is owner-authorized within the declared institutional protocol; clinical interpretation and clinical deployment remain disabled.
