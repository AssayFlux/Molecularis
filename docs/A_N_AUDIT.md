# A–N Service Repository Audit — Historical Baseline

> **Historical snapshot:** This audit describes source commit `24251ca6bf2daf6aef7fa815017a90fa0a38c0c9` on 2026-11-21. It is not the current service status. Later service implementation commits superseded its “scaffold/not implemented” and “do not start A” conclusions. Use [SERVICE_STATUS.md](SERVICE_STATUS.md) and the current service acceptance records for current implementation evidence. This historical audit is retained as a record of the earlier baseline, not as the authority for present status.

> **Superseded planning note:** The old source-root and C++/Rust interoperability recommendations below are historical observations from this snapshot, not current requirements. DEC-0014 establishes Python as the current implementation baseline and rejects speculative language ports. The later A–N service specifications and [SERVICE_STATUS.md](SERVICE_STATUS.md) are authoritative for current work.

Audit date: 2026-11-21  
Audited branch: `CORE`  
Audited source commit: `24251ca6bf2daf6aef7fa815017a90fa0a38c0c9`

## Executive result

All fourteen service directories and their four planning files exist. They are scaffolds, not completed service implementations. The service ENGINE/RUNTIME/RULEBOOK documents are generic templates; the manifests mark each service as `scaffold` / `not_implemented`. There are no service-local source, schema, data, benchmark, or test files beneath the service directories.

There is substantial reusable scientific code in the legacy `python/molecularis` package and corresponding root-level tests/validation scripts. That code is not yet migrated into service-owned boundaries or proven against each service's acceptance criteria. The platform status register correctly reports all A–N services as not started and says the platform gate must pass before A begins.

Latest CI on the audited source commit passed: core Python job, schema validation, capability registry validation, Ruff, compilation, tests, and optional chemistry/genomics/sequence profiles. This is repository CI evidence, not proof of scientific correctness or service completion.

## Cross-cutting findings

### Critical architecture and delivery gaps

1. **Service specifications are placeholders.** The Engine documents do not specify algorithms, inputs/outputs, invariants, units, failure modes or measurable service acceptance criteria. Runtime documents are generic lifecycle prompts. Rulebooks contain no operational, versioned domain rules.
2. **Implementation ownership is not established.** Service manifests point to `services/<id>/src/{cpp,python,rust}`, but existing Python implementations remain under `python/molecularis`; the service directories contain no source roots.
3. **No service-local verification boundary exists.** Tests remain in the single root `tests/` package. There are no per-service fixtures, conformance suites, benchmarks or acceptance records under the service directories.
4. **Platform gate is still open.** Native C++/Rust interoperability, crash recovery certification, process-level discovery, OS isolation and full scientific validation remain outstanding in `docs/SERVICE_STATUS.md` and `docs/WORK_BACKLOG.md`.
5. **External adapters are not native engines.** RDKit, pysam/HTSlib, OpenMM, GROMACS, ESM, Vina, Galaxy and similar integrations must be treated as optional adapters/references unless the corresponding Molecularis-native implementation is separately demonstrated.
6. **Existing CI is necessary but insufficient.** Current CI passes, but the workflow does not establish per-service scientific acceptance, independent reference coverage, performance envelopes, or native C++/Rust contracts.

### Priority code-level risks observed

- `python/molecularis/molecular.py` is named as though it were the foundational Molecular domain module, but it contains primer-property screening and SpCas9 NGG scanning. It does not implement canonical atoms, bonds, residues, molecular graphs, identifiers or coordinate/unit conventions required by service A.
- `python/molecularis/structure_prediction.py` explicitly validates a prediction envelope supplied by another service; it does not implement a prediction engine. It also reports model license status as not approved and calibration/node trust as not assessed.
- `python/molecularis/chemistry_rdkit.py` is an RDKit adapter, not an independent Molecularis-native chemistry engine.
- `python/molecularis/genomics_htslib.py` is a pysam/HTSlib adapter. The native parser modules are bounded utilities, not a complete SAM/BAM/CRAM/VCF implementation.
- `python/molecularis/workflows.py` is a bounded local FASTA/FASTQ QC workflow, not a cross-service DAG scheduler/orchestrator.
- `python/molecularis/virtual_cohort.py` produces synthetic aggregate data only. It is not a governed cohort system, consent/metadata model, privacy-preserving analysis engine or real-world cohort ingestion service.
- Several algorithms are explicitly exploratory or simplified (for example, grid-search Michaelis–Menten fitting and exploratory omics tests). Their limitations are documented in code and must remain visible in service claims.

## Service-by-service audit

| Step | Service | Reusable code found | Audit conclusion | Main work still required |
|---|---|---|---|---|
| A | Molecular | `molecular.py` (primer/PAM utilities); shared scientific primitives | **Major scope mismatch; foundational Molecular service absent.** | Build canonical molecular entity/atom/bond/residue/graph models, identifiers, units, coordinate conventions, serialization and validation. Reclassify primer/PAM functions under DNA/RNA or sequence tooling. |
| B | Sequence | `sequence.py`, FASTA/FASTQ, alignment, ORF, genetic-code, motif and reference utilities | **Strongest reusable base; not accepted as a service.** | Formalize DNA/RNA/protein alphabets and record contracts, streaming and resource budgets, alignment algorithm suite, annotation semantics, reference packs and independent golden/property tests. |
| C | Structure | `structure.py`, Biotite adapter, alignment, pockets, quality, viewer and prediction-envelope modules | **Useful parsing/geometry base; incomplete structural domain.** | Complete topology/residue/chain models, mmCIF and alternate-location handling, units/transforms, validation, robust correspondence and independent structural reference tests. Prediction envelope validation is not prediction. |
| D | Chemistry | `chemistry.py`, `chemistry_rdkit.py`, docking utilities | **Partial utilities plus optional RDKit adapter; native chemistry not established.** | Native graph/valence/aromaticity/stereochemistry/charge/formula/SMILES scope, reaction transformations, canonicalization policy and independent chemistry fixtures. Clearly isolate RDKit-backed functions. |
| E | Protein | `protein.py`, ESM inference, protein design/motifs and structure-related modules | **Partial protein utilities and model adapters; no complete protein engine.** | Protein domain models, residue/sequence mapping, scoring/design contracts, model provenance/licensing, inference resource policy and independent validation/calibration. |
| F | Genomics | `genomics.py`, HTSlib adapter, VCF/SAM utilities, GFF3, annotation, genome QC and variant references | **Useful bounded genomics utilities; not a complete genomics service.** | Reference assembly/contig identity, standards-complete parsing, normalization/liftover policy, indexed access, variant annotation evidence, privacy controls and large-file tests. |
| G | DNA/RNA | Shared sequence/genetic-code/structure utilities; no dedicated DNA/RNA service module | **Service is a scaffold; domain ownership is missing.** | Nucleic-acid-specific thermodynamics, folding/design/hybridization models, duplex and modified-base representation, parameter provenance and independent NUPACK/NUAD-style references without treating adapters as native engines. |
| H | Simulation | GROMACS and OpenMM integration modules | **Adapters and execution hooks, not a Molecularis-native MD engine.** | Native simulation model/force-field contracts, units, integrators, constraints, energy/trajectory formats, deterministic execution, restart/recovery and validated physical benchmarks. |
| I | Kinetics | `kinetics.py`, PK/PD and SciPy reference utilities | **Useful basic models; exploratory fitting is not production-grade kinetics.** | Reaction-network representation, ODE/stochastic solvers, parameter identifiability, uncertainty, event handling, sensitivity analysis, units and benchmark/reference validation. |
| J | Omics | `omics.py` normalization, correlations, exploratory differential expression and growth models | **Useful statistical primitives; not a complete multi-omics platform.** | Explicit assay/data models, normalization assumptions, batch/covariate design, robust dispersion/uncertainty, multiple-testing policy, missingness and independent statistical references. |
| K | Phylogeny | `phylo.py` Newick and distance/tree utilities | **Partial tree utilities; inference breadth and evidence are incomplete.** | Formal tree/model representation, supported substitution models, scalable inference, support metrics, rooting/reconciliation policy and reference datasets. |
| L | Pharmacogenomics | `pgx.py`, PharmVar-related utilities and variant reference modules | **Partial evidence/data utilities; no validated interpretation service.** | Versioned guideline/evidence sources, allele nomenclature and star-allele calling validation, diplotype/phenotype rules, conflict resolution, ancestry limitations and traceable rule evaluation. No clinical claims without validation. |
| M | Cohorts | `virtual_cohort.py` synthetic-only cohort generators | **Manifest says scaffold; existing code is synthetic simulation only.** | Cohort definition/metadata contracts, consent and governance, de-identification/privacy threat model, aggregate query controls and auditable real-data boundaries. |
| N | Workflows | `workflows.py`, Galaxy connector and S4 process/engine utilities | **Local QC and connector utilities; cross-service orchestration absent.** | Typed DAG model, service discovery, scheduling, retries/idempotency, cancellation, artifact/provenance continuity, isolation, deterministic replay and end-to-end workflows. |

## Recommended disposition of existing code

- Preserve the existing modules and tests; do not delete or rewrite them during the audit.
- Inventory every public function, import, dependency, license, data source and test, then assign each reusable function to exactly one service.
- Move or wrap code only after the target service contracts are defined and compatibility tests exist.
- Mark adapter-backed functionality explicitly in capability metadata; do not advertise it as native.
- Reclassify misplaced functions (especially primer/PAM utilities currently in `molecular.py`).
- Add a service-local test/fixture/benchmark layout only as each service becomes active; keep the one-service-at-a-time rule.

## Execution order and gate — historical recommendation

The recommendation below applied to the historical audit source commit only. It has been superseded by subsequent service implementation work. Follow the current A–N state and next task in SERVICE_STATUS.md and WORK_BACKLOG.md; do not use this historical recommendation to infer that current service implementation has not started.

## Audit limits

This is a repository-wide static inventory and focused source review, including service manifests/specifications, representative domain modules, tests/validation layout and the latest CI run. It is not a line-by-line formal verification of every algorithm, nor does a passing test suite prove scientific validity. The function-level migration inventory, license/data provenance review, security review, numerical benchmarking and independent scientific validation remain explicit follow-up tasks.
