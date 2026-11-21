# Scientific integration gaps and insufficiencies

**Branch:** `CORE`  
**Purpose:** Running backlog for limitations intentionally deferred while scientific engines are being integrated. This document is not a validation certificate. Update it whenever an engine is added, changed, removed or reclassified.

## Integration policy

Integrate useful engines behind Molecularis-owned contracts first. Preserve engine identity, version, algorithm, parameters, input/output hashes where appropriate, and explicit runtime requirements. Keep optional dependencies optional unless their platform and redistribution case is proven. Do not silently substitute one algorithm for another. Do not claim that successful execution establishes scientific validity.

A gap may be deferred only when the integration remains bounded, honest about its limitations, and does not create unsafe data loss, incorrect coordinate/identity conversion, licence violations or uncontrolled resource use.

## Integration inventory

| Engine / library | Molecularis integration state | Deferred gaps |
|---|---|---|
| Biopython | Optional host PairwiseAligner adapter and Android feasibility prototype | File-level licence/notices; device runtime and 16 KB proof; parser differential corpus; FASTQ encoding metadata; full structure identity; broader alignment modes |
| Biotite | Optional host mmCIF adapter in `structure_biotite.py` | Python >=3.12 isolated profile; Rust packaging; BinaryCIF; author/label mapping; biological assemblies; annotation fidelity; differential fixtures |
| Parasail | New optional global/local affine-gap traceback adapter in `scientific_engines.py` | Python/native binding pin; score-width/saturation corpus; tie and gap convention comparisons; SIMD/NEON/16 KB proof; exact custom licence and citation notices |
| pysam | Optional host BAM/CRAM streaming and indexed-region adapter | Lossless tags/mates/header/base-modification model; reference/index provenance; decompression/time/resource limits; broader format fixtures |
| HTSlib | Exposed through the pysam adapter | Native binary provenance; bundled htscodecs/samtools/bcftools notices; format differential corpus; Android feasibility |
| BCFtools | Runtime discovery in engine registry; executable not invoked by Molecularis yet | Safe command contract; normalization/reference concordance; plugin and bundled-notice audit; isolated execution |
| Samtools | Runtime discovery in engine registry; executable not invoked by Molecularis yet | Safe command contract for view/sort/index/flagstat; header and sort semantics; bundled-notice audit; isolated execution |
| ESM | Isolated local-process prediction contract can carry model provenance | No ESM-specific loader; model/weight terms; accelerator/memory profile; embedding and confidence benchmarks |
| AlphaFold | Isolated local-process prediction contract and strict prediction-envelope validation | No bundled model/data; model/database terms; supported deployment profile; confidence calibration and benchmark datasets |
| Mol* | Offline Android viewer assets/prototype | Full Molecularis data bridge; offline runtime verification; accessibility; large-structure performance; security review |
| MolProbity | Runtime discovery only; no Molecularis validation adapter yet | Component-level source/licence review; command/API contract; validation method provenance; curated validation corpus |
| RDKit | Optional host chemistry adapter | Stereochemistry/isotope/salt/tautomer/aromaticity corpus; graph/resource ceilings; transitive SBOM/notices; Android feasibility |
| AutoDock Vina | Optional host docking runner | Preparation workflow; reproducibility across builds; redocking/cross-docking/enrichment benchmarks; isolation; binary provenance |
| OpenMM | Optional CPU runner for caller-prepared systems | Approved system preparation; force-field/ligand parameter provenance; reference systems; convergence; cancellation/resource controls |
| GROMACS | Runtime discovery only; no Molecularis execution adapter yet | Source/licence/build review; TPR/trajectory contracts; force-field governance; platform/runtime strategy; benchmark interoperability |
| SciPy | Host validation/reference use | Per-workflow pinning; no Android bundle; reference tests for all dependent methods; environment isolation |
| NUAD | Not integrated; upstream identity/source/licence not established in this pass | Resolve canonical upstream project and exact API; source/licence/dependency audit; thermodynamic model and design validation |
| NUPACK | Not integrated; no verified redistributable upstream source/API in this pass | Confirm access/licensing and supported API; thermodynamic model provenance; runtime profile; independent reference fixtures |
| Galaxy | Not integrated; source API reviewed, server not deployed | API client, auth/credential lifecycle, server operations, workflow mapping, job data controls and security review |

## First integration increment (2026-11-21)

- Added `python/molecularis/alignment_biopython.py`, a lazy optional adapter returning Molecularis-owned primitive result data (engine/version, algorithm, mode, score, coordinates and scoring parameters).\n- Added `validation/requirements-bio.txt` pinning the isolated host reference profile to Biopython 1.88 and NumPy 1.26.2; no base dependency or Android package change.\n- Added optional adapter contract tests in `tests/test_alignment_biopython.py`. Tests have not been executed in this repository-editing session.\n- The adapter intentionally supports global/local affine-gap alignment only; it does not expose matrices, semi-global end-gap configuration, traceback rendering, CIGAR, read mapping or database indexing.\n\n## Cross-cutting gaps to close after integration

1. **Canonical scientific data contracts:** stable sequence, alignment, read, variant, atom/residue, molecular graph, simulation system and result models that do not leak optional-engine objects.
2. **Provenance:** engine and version, algorithm, parameters, source/reference build, checksums, coordinate conventions, random seeds, environment and warnings.
3. **Validation:** deterministic unit fixtures, independent implementation comparisons, curated benchmark datasets, calibration and domain-specific acceptance criteria. Separate software correctness from scientific validity.
4. **Resource controls:** input bytes, decoded records/bases/atoms, CPU time, memory, thread count, output size, cancellation and decompression limits at the service boundary.
5. **Platform profiles:** Linux/macOS/Windows host support and Android/iOS only after native ABI, packaging, runtime, page-size, lifecycle and offline tests.
6. **Licensing and supply chain:** immutable source revisions, complete transitive source/binary notices, model/data terms, checksums, SBOM and update policy.
7. **Workflow integration:** consistent job lifecycle, progress, cancellation, persistence, export, audit/provenance and recovery.
8. **Privacy/security:** local-first processing, no patient/sample payloads in CI or logs, safe parsing of untrusted inputs, isolated native workers and explicit network behavior.
9. **Scientific boundaries:** research-only labels where appropriate; no clinical interpretation, affinity, toxicity, pathogenicity or biological mechanism claims from execution alone.

## Status vocabulary

- **Audited:** upstream source and relevant implementation paths inspected.
- **Integrated:** Molecularis-owned adapter or implementation is present in the repository.
- **Tested:** relevant tests were actually executed and passed in a named environment.
- **Reference-compared:** output was compared against a separately implemented or curated reference.
- **Benchmarked:** performance was measured on a named platform and workload.
- **Scientifically validated:** domain-specific evidence and acceptance criteria were met.

These states are independent. Never infer one from another. Update status only with recorded evidence.

## Current execution order

1. Complete host-side integration seams for sequence/alignment, genomics, chemistry, structure, docking and dynamics.
2. Integrate specialist engines only after their source, licence and runtime profiles are reviewed.
3. Unify contracts, provenance, job orchestration and resource controls across all integrations.
4. After the integration inventory is substantially complete, work through the deferred gaps above in priority order and record evidence for each closure.


## Biotite integration increment (2026-11-21)

- Reviewed upstream Biotite PDBx conversion implementation in `src/biotite/structure/io/pdbx/convert.py` and the `AtomArray` annotation model in `src/biotite/structure/atoms.py`. The upstream conversion path uses `CIFFile.read()`, `get_model_count()` and `get_structure()`; this adapter calls those APIs rather than reimplementing mmCIF parsing.
- Added `python/molecularis/structure_biotite.py`: lazy optional Biotite backend, bounded UTF-8 input, explicit model selection, atom-count bound, finite coordinate checks, input SHA-256, and Molecularis-owned primitive atom records. No Biotite/NumPy objects escape the adapter.
- Added `tests/test_structure_biotite.py` with optional dependency contract and input-bound tests. Tests were not executed in this repository-editing session.
- The adapter currently accepts text mmCIF only. BinaryCIF, biological assembly expansion, author/label identifier reconciliation and broader differential validation remain deferred.


## Coordinated integration increment (2026-11-21)

- Added `python/molecularis/scientific_engines.py` with a stable inventory for all 19 named projects (18 integration targets when pysam/HTSlib are counted as one paired stack), lazy runtime discovery (without importing model weights), and a Molecularis-owned Parasail global/local affine-gap traceback adapter.
- Added `tests/test_scientific_engines.py` for the 19-project inventory, discovery semantics, input ceilings and optional Parasail contract. These tests have not been executed in this repository-editing session.
- Source-level inspection in this pass covered Parasail's `src/sw.c` and `src/nw.c`; HTSlib's `sam.c`; Samtools' `bam_sort.c`; BCFtools' `mpileup.c`; AlphaFold's `run_alphafold.py`; RDKit's `SmilesParse.cpp`; OpenMM's `simulation.py`; GROMACS' `md.cpp`; SciPy's `stats/_stats_py.py`; and Galaxy's workflow API implementation. Existing audits cover Biopython, Biotite, pysam/HTSlib, RDKit, Vina, and OpenMM.
- ESM's expected `esm/pretrained.py` path and the guessed NUAD/NUPACK source paths did not resolve in the upstream repositories queried; MolProbity's canonical source/API was not established. These are explicitly not marked as integrated.
- The registry distinguishes integrated adapters, process-contract integrations, viewer assets, runtime discovery, and not-yet-integrated tools. A discovered executable or importable package is not evidence of a working workflow.
- The new Parasail adapter rejects inputs outside its configured alphabet, bounds alignment cells, checks saturation and returns traceback plus score. It does not claim parity with the existing Molecularis or Biopython aligners until differential tests are run.
- No model weights, reference databases, native binaries, or third-party source files were copied or bundled.
