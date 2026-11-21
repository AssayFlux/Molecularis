# Scientific integration gaps and insufficiencies

**Branch:** `CORE`  
**Purpose:** Running backlog for limitations intentionally deferred while scientific engines are being integrated. This document is not a validation certificate. Update it whenever an engine is added, changed, removed or reclassified.

## Integration policy

Integrate useful engines behind Molecularis-owned contracts first. Preserve engine identity, version, algorithm, parameters, input/output hashes where appropriate, and explicit runtime requirements. Keep optional dependencies optional unless their platform and redistribution case is proven. Do not silently substitute one algorithm for another. Do not claim that successful execution establishes scientific validity.

A gap may be deferred only when the integration remains bounded, honest about its limitations, and does not create unsafe data loss, incorrect coordinate/identity conversion, licence violations or uncontrolled resource use.

## Integration inventory

| Engine / library | Molecularis integration state | Deferred gaps |
|---|---|---|
| Biopython | Optional host PairwiseAligner adapter integrated; Android feasibility prototype exists | Exact file-level licence and wheel notices; device runtime/16 KB proof; parser differential corpus; FASTQ encoding metadata; structure identity preservation; broader alignment modes |
| Parasail | Source audit complete; not yet integrated | Fresh maintenance/security review; exact licence/citation notices; checked score-width/saturation; differential corpus; host build; Android NEON/JNI/16 KB proof |
| HTSlib / pysam | Optional host BAM/CRAM streaming and indexed-region adapter exists | Lossless record/header/tags/mate/base-modification model; reference/index provenance; decompression/time/resource limits; broader SAM/BAM/CRAM fixtures; native supply-chain and binary notices; Android feasibility |
| Biotite | Not integrated | Python >=3.12 host profile; Rust extension packaging; lossless structure contract; dependency/licence audit; differential mmCIF/BinaryCIF fixtures |
| RDKit | Optional host chemistry adapter exists | Broader stereochemistry/isotope/salt/tautomer/aromaticity corpus; graph/resource ceilings and isolation; exact transitive SBOM/notices; Android feasibility |
| AutoDock Vina | Optional host docking runner exists | Receptor/ligand preparation workflow; reproducibility across builds; redocking/cross-docking and enrichment benchmarks; resource isolation; binary provenance/licence inventory |
| OpenMM | Optional CPU runner for caller-prepared systems exists | Approved system preparation; force-field and ligand parameter provenance; biomolecular reference systems; energy/stability convergence checks; resource/cancellation controls; no general remote-worker exposure |
| Mol* | Viewer assets/prototype only | Full Molecularis data bridge; offline packaging/runtime; accessibility; large-structure performance; security review |
| SciPy | Host validation/reference use | No Android bundle; per-workflow pinning; reference tests for all dependent methods; environment isolation |
| ESM / AlphaFold | Not production-integrated | Exact model/weight licences; model provenance; supported runtime/hardware; memory/storage budgets; confidence calibration; benchmark datasets |
| HMMER / BLAST | Optional adapters/probes; not a unified service | Reproducible database packs; versioned search parameters; result provenance; native packaging/licence review; resource limits |
| NUPACK / NUAD | Not integrated | Current source and licence audit; thermodynamic dependency graph; model/data provenance; independent reference fixtures |
| GROMACS | Not integrated | Source/licence/build review; platform/runtime strategy; force-field and preparation governance; benchmark and output interoperability |
| Samtools / BCFtools | Available through HTSlib/pysam ecosystem, not exposed as complete Molecularis services | Tool-specific command/API contracts; exact bundled notices; reference concordance and normalization fixtures; safe subprocess isolation |

## First integration increment (2026-11-21)\n\n- Added `python/molecularis/alignment_biopython.py`, a lazy optional adapter returning Molecularis-owned primitive result data (engine/version, algorithm, mode, score, coordinates and scoring parameters).\n- Added `validation/requirements-bio.txt` pinning the isolated host reference profile to Biopython 1.88 and NumPy 1.26.2; no base dependency or Android package change.\n- Added optional adapter contract tests in `tests/test_alignment_biopython.py`. Tests have not been executed in this repository-editing session.\n- The adapter intentionally supports global/local affine-gap alignment only; it does not expose matrices, semi-global end-gap configuration, traceback rendering, CIGAR, read mapping or database indexing.\n\n## Cross-cutting gaps to close after integration

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
