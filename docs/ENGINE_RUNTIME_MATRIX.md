# Molecularis — Engine Runtime Matrix

**Status:** Initial planning inventory; exact pins and support claims are pending reproducible builds.  
**Date:** 2026-11-20

| Runtime profile | Candidate workload | Platform direction | Isolation / constraints | Evidence still required |
|---|---|---|---|---|
| `base-python` | Shared validation, parsers, utilities | Linux x86_64 first; Android-hosted Python only where existing integration supports it | Locked dependencies; no implicit network | Exact Python/dependency pins, SBOM, tests |
| `chemistry-rdkit` | RDKit chemistry operations | Linux desktop; Android only through an explicitly supported native path | Native library isolation and version pinning | Build reproducibility, ABI compatibility, reference fixtures |
| `protein-esm` | ESM/ESMFold candidates | Linux x86_64; optional supported GPU | Separate PyTorch environment; model weights installed explicitly | Exact model/weight terms, CUDA matrix, benchmark |
| `protein-alphafold` | AlphaFold candidate | Linux x86_64 with suitable accelerator/storage | Separate JAX environment; large databases/weights; no default bundle | Exact upstream version, data/model licences, GPU and resource tests |
| `simulation-openmm` | OpenMM | Linux x86_64 CPU/GPU as verified | Separate environment; prepared-system input only until preparation pipeline is validated | Platform pins, force-field provenance, reference systems |
| `structure-tools` | Biotite and selected structure tools | Linux desktop; portable Python where feasible | Isolated dependencies; bounded file parsing | Format fixtures, parser limits, licence audit |
| `viewer-assets` | Offline structure/molecule viewer | Android WebView and desktop web runtime as appropriate | Static local assets, no remote runtime dependency | Offline packaging, asset notices, device/performance tests |
| `genomics-tools` | Selected genomics utilities | Linux desktop first | Separate profile for native tools and datasets | Exact tool/version matrix, data licences and benchmarks |

## Required manifest fields

Every runnable profile must declare:
- profile ID and semantic version;
- OS, architecture and ABI;
- language/runtime version;
- direct and transitive dependency lock and hashes;
- native library and accelerator requirements;
- engine and model/data identifiers;
- installation source and licence notices;
- CPU, RAM, disk, GPU and wall-time ceilings;
- network policy and filesystem access;
- health-check command (fixed, non-user-controlled);
- test suite and known limitations.

## Compatibility policy

Do not claim compatibility based only on package metadata or upstream documentation. Build the exact lock file in CI and on the reference host. Keep incompatible ML stacks separate. Record CPU-only fallback explicitly; never silently change precision, model, backend or numerical settings. Model weights and large reference datasets are opt-in installations with their own manifests and hashes.
