# Molecularis — Scientific Validation Plan

**Status:** Validation framework proposal; no new scientific acceptance is claimed.  
**Date:** 2026-11-20

## 1. Validation layers

1. **Contract validation:** schema correctness, required fields, version compatibility and rejection behaviour.
2. **Unit/integration testing:** deterministic component behaviour, error paths and resource limits.
3. **Reference validation:** comparison against trusted reference datasets/tools with documented versions and tolerances.
4. **Benchmark validation:** task-specific accuracy, calibration, throughput, memory and reproducibility.
5. **Platform validation:** exact Android devices, desktop OS/CPU/GPU combinations and offline behaviour.
6. **Independent review:** domain expert assessment of methods, datasets, limitations and claims.

A pass at one layer does not imply a pass at another.

## 2. Test design

For every workflow, define:
- intended use and explicit non-goals;
- input domain, supported formats and excluded cases;
- reference set and inclusion/exclusion rationale;
- ground truth/reference method and version;
- primary and secondary metrics;
- acceptance thresholds set before evaluation;
- uncertainty, failure and missing-data treatment;
- hardware/runtime profile;
- reproducibility package and report owner.

Use held-out evaluation data where model tuning or threshold selection could otherwise leak into the test set.

## 3. Workflow validation suites

### A. Protein prediction
Validate sequence handling, model/environment identity, output parsing, residue mapping, confidence-field semantics, coordinate integrity and task-specific accuracy. Compare on a curated benchmark with explicit data leakage controls. Calibrate confidence separately from raw model scores. Prediction envelope validation alone is not prediction validation.

### B. Structure quality
Use curated structures and independent geometry references. Compare individual observations and distributions; document disagreements and limitations. Do not label current bounded clash/torsion observations as MolProbity-equivalent without method-level evidence.

### C. Molecular dynamics
Verify topology, atom ordering, units, force-field assignment, ligand parameters, constraints and initial conditions. Test energy behaviour and reference systems; define equilibration and stability criteria. Record all force-field and parameter sources.

### D. Cheminformatics
Use known molecule fixtures spanning charges, aromaticity, stereochemistry, salts, isotopes and edge cases. Validate sanitization, canonicalization and descriptor definitions against pinned reference implementations.

### E. Genomics
Use versioned reference genomes and curated truth sets. Test coordinate conventions, strand handling, normalization, variant representation and annotation provenance.

### F. Nucleic-acid design
Test constraint satisfaction and reproducibility. Thermodynamic claims require a separately reviewed model, parameter set and independent comparison.

## 4. Reproducibility packet

Every reference-validation run should archive:
- protocol and test-set manifest;
- input and reference hashes;
- source commit and build identity;
- engine/model/runtime/profile versions;
- parameter/configuration files;
- hardware and accelerator details;
- raw outputs, normalized outputs and logs;
- metric implementation/version and tolerances;
- deviations, exclusions and failure analysis;
- signed review/approval record where required.

Do not put patient data or restricted datasets in public repository artifacts.

## 5. Reporting

Publish results with denominators, confidence intervals where appropriate, subgroup/task breakdowns, failure rates and known limitations. Separate exploratory results from pre-registered acceptance tests. Never fabricate benchmark values or use a single successful example as evidence of general validity.

## 6. Exit criteria

A workflow may be called reference-validated only when its protocol, reference set, metrics, thresholds and results are reviewed and reproducible. Platform verification additionally requires the named hardware/software matrix and recorded test artifacts. Clinical or regulated claims require separate governance and approvals.
