# Molecularis — Third-Party Integration Register

**Status:** Initial candidate register; all licence and version dispositions require exact-source review.  
**Date:** 2026-11-20

| Project | Candidate use | Initial disposition | Review checklist |
|---|---|---|---|
| Biotite | Sequence/structure processing | Selective adapter | Exact release/commit, Apache or other applicable licence text, dependencies, format behaviour |
| Mol* | 3D molecular visualization | Selectively integrate viewer | Component and asset licences, notices, offline assets, WebView constraints |
| MolProbity | Structure validation methods/tools | Adapt selected methods or wrap selected tools | Component-specific licences, method provenance, legacy dependencies, redistribution |
| AlphaFold | Protein prediction | Optional isolated profile | Code, model weights, databases and data terms separately; compute/storage and export restrictions |
| ESM | Protein language models / ESMFold | Optional isolated profile | Code and weight terms, model card, dataset provenance, runtime and accelerator |
| OpenMM | Molecular dynamics | Extend existing adapter | Licence, plugins, force fields, parameter sources and supported hardware |
| RDKit | Cheminformatics | Existing optional adapter; extend after pinning | Release, licence, build provenance, native dependencies |
| Open Chemistry | Selected chemistry components | Component-level reuse only | Identify exact subproject, licence, dependencies; do not bundle full application by default |
| Genome-Wide Workbench | Genomics workflows/algorithms | Selective reuse after source audit | Exact repository/module, licence, format support and algorithm validation |
| Galaxy | Workflow orchestration | Concepts first; full deployment deferred | Server footprint, plugin licences, security, operations and justification |
| ChemGraph | Chemistry workflow/calculation patterns | Optional isolated evaluation | Resolve exact project/version; licence, deterministic boundary and agent isolation |
| nuad | DNA/RNA design | Optional specialist adapter | Licence, dependency terms, thermodynamic model separation and validation |
| SciREPL | Notebook/repl UX | UX inspiration initially | Execution isolation, kernel security, persistence, audit and data retention |

## Mandatory evidence per entry

- Canonical upstream URL, exact commit/tag and retrieval date.
- Licence file and applicable notices, patent, model, dataset and trademark terms.
- Exact files/modules used and modifications made.
- Dependency and transitive dependency inventory; SBOM.
- Whether binaries, weights, databases or datasets are redistributed, downloaded or user-supplied.
- Security review, vulnerability posture and network behaviour.
- Molecularis adapter owner, version policy, test suite and removal/upgrade plan.
- Legal review for ambiguous, custom, non-commercial, research-only or model/data terms.

## Decision rule

No third-party code, model weights, databases, reference data or assets may be bundled or redistributed until its exact terms are reviewed and recorded. Molecularis' Apache-2.0 project licence applies to Molecularis-authored material and does not relicense upstream components. A candidate listed here is not approved for use.


## Additional engines in the coordinated integration pass

- Parasail: `jeffdaily/parasail`, v2.6.2 source reviewed at `src/sw.c` and `src/nw.c`. Its custom Battelle licence and required citation/name restrictions must be preserved before redistribution. Molecularis wraps the Python/native API; it does not copy Parasail source.
- HTSlib, Samtools and BCFtools: source paths `sam.c`, `bam_sort.c` and `mpileup.c` reviewed. Preserve each upstream licence and bundled dependency notices separately; pysam remains the current Molecularis HTSlib integration seam.
- AlphaFold: `run_alphafold.py` reviewed. Code licence does not settle model-weight, database, or dataset terms; Molecularis uses only the isolated local-process contract until those are approved.
- RDKit: `SmilesParse.cpp` reviewed; per-file BSD notices remain applicable.
- OpenMM: `openmm/app/simulation.py` reviewed; wrapper/API use does not approve force fields or parameter sources.
- GROMACS: `md.cpp` reviewed; LGPL-2.1-or-later project terms and build/dependency notices require separate distribution review.
- SciPy: `scipy/stats/_stats_py.py` reviewed; the file contains historical upstream copyright/disclaimer material, so retain upstream notices with any redistributed binaries.
- Galaxy: workflow API implementation reviewed; server deployment and API use require separate operational/security approval.
- ESM, NUAD, NUPACK and MolProbity: exact source/API/licence was not established in this pass. Do not bundle, redistribute, or mark these as integrated until canonical upstream sources and terms are confirmed.
