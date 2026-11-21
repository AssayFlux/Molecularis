# Molecularis — Scientific Engine Integration Matrix

**Status:** Planning matrix; entries are candidates, not approved integrations.  
**Date:** 2026-11-20

| Candidate | Intended Molecularis role | Proposed disposition | Key prerequisites / risks | Acceptance evidence |
|---|---|---|---|---|
| Biotite | Sequence and structural-biology data processing | Selective adapter | Pin compatible release; define canonical residue/atom mapping; licence and dependency review | PDB/mmCIF/sequence fixtures, round-trip and reference comparisons |
| Mol* | Offline molecular/structure visualization | Integrate viewer components selectively | WebView/offline packaging, asset licensing, payload limits and Android performance | Visual correctness, large-structure performance, accessibility and physical-device tests |
| MolProbity | Structure geometry validation | Adapt selected methods or wrap selected tools | Exact component licences, runtime compatibility, method provenance; do not embed legacy web application wholesale | Reference structures, agreement/disagreement analysis, documented thresholds |
| AlphaFold | Protein structure prediction | Separate optional Linux/GPU profile | Model and database licences, large weights/data, JAX/CUDA compatibility, compute/storage requirements | Reproducible model build, benchmark set, confidence calibration and independent review |
| ESM / ESMFold | Protein language-model features and optional folding | Separate optional profile | Model-weight terms, PyTorch/CUDA compatibility, model provenance and resource demands | Task-specific benchmarks, calibration and environment reproducibility |
| OpenMM | Molecular dynamics | Extend existing adapter | Prepared topology/system, force-field selection, ligand parameterization, unit and provenance controls | Reference energy/trajectory tests, stability checks and reproducible setup |
| RDKit | Cheminformatics | Continue/extend existing adapter | Version pinning, sanitization policy, stereochemistry and descriptor definitions | Known molecule fixtures, canonicalization and descriptor comparisons |
| Open Chemistry | Selected chemistry libraries/tools | Reuse only justified components | Component-by-component licence and dependency review; avoid importing full Qt/C++ application | Adapter tests and parity against known reference outputs |
| Genome-Wide Workbench | Genomics workflow/algorithm ideas | Selective reuse after audit | Identify exact modules and licences; map supported formats and algorithm scope | Curated sequence fixtures and independent reference comparisons |
| Galaxy | Workflow orchestration and provenance concepts | Reuse concepts; defer full server | Operational footprint, plugin ecosystem, security and administration burden | Workflow manifest and provenance prototype; deployment justification |
| ChemGraph | Chemistry calculation/workflow orchestration patterns | Optional isolated adapter | Clarify exact project/version and dependencies; isolate any agent/LLM execution from deterministic core | Deterministic adapter tests, safety boundary and scientific comparisons |
| nuad | Constrained DNA/RNA design | Optional specialist adapter | Exact licence and dependency review; clarify thermodynamic evaluation dependencies | Design constraint fixtures, independent evaluation and reproducibility |
| SciREPL | Scientific notebook/repl UX ideas | UX inspiration only initially | Safe execution model, kernel isolation, persistence and audit trail | UX prototype and threat-model review |

## Status vocabulary

Use the acceptance ladder from `not_assessed` through `platform_verified` defined in the master plan. Do not infer an engine’s status from its presence in this table or in the capability catalogue.

## Integration record required for every candidate

- Exact upstream repository, release/tag and commit.
- Component(s) to be used and whether code, model weights, datasets or documentation are included.
- Licence text, notices, attribution, patent/data/model terms and redistribution decision.
- Supported OS/ABI, language/runtime, accelerator and dependency lock.
- Molecularis capability IDs and input/output schemas.
- Resource, security and privacy boundaries.
- Reference fixtures, expected outputs, tolerances and benchmark methodology.
- Maintainer, upgrade policy, known limitations and removal plan.

## Important boundaries

The matrix does not grant permission to redistribute third-party code, models, weights or datasets. Project Apache-2.0 does not supersede upstream terms. A viewer is not a validator; a parser is not a predictor; envelope validation is not model inference; and a simulation adapter is not a complete system-preparation pipeline.
