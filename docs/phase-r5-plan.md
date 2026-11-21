# R5 — Structural biology

**Status:** In progress. Source implementation is not scientific validation or device verification.

## Scope
- PDB and mmCIF atom coordinate ingestion.
- Geometric contacts and coordinate RMSD, with optional rigid-body superposition.
- Added approximate Shrake–Rupley SASA and distance-only heavy-atom candidate screening for N...O hydrogen bonds, canonical Lys/Arg-Asp/Glu salt bridges and Cys SG disulfides. Future: mmCIF dictionary/assembly/symmetry semantics, residue mapping, secondary structure and structure quality checks.

## Current source
Implemented in `python/molecularis/structure.py`. The mmCIF reader currently supports atom-site loops and label/auth identifier fallbacks; the RMSD superposition uses a Horn-quaternion fit.

## Limitations
- mmCIF parser is not a full dictionary or biological assembly implementation.
- No symmetry expansion, missing-residue reconstruction or chemical component interpretation.
- SASA uses generic element radii and finite Fibonacci sampling; interaction screening does not include hydrogen geometry, protonation, solvent or energy calculations.
- Contact definitions and atom selections require explicit method metadata.

## Exit evidence
Reference structures and independently computed coordinate/contact/RMSD concordance; edge cases for alternate locations, chains, insertion codes and units; large-structure benchmarks; offline visualization and device resource measurements; dependency/license review.


## Host-side structural software reference comparison — 2026-11-09

Added `validation/structure_biopython_reference.py` to compare the local PDB parser's atom metadata/coordinates with pinned Biopython 1.88, contact-pair distances with an independent NumPy calculation, and Horn-quaternion superposed RMSD with an independent NumPy SVD/Kabsch fit. The scientific-reference CI job now runs this script, asserts every comparison passes and uploads its JSON record.

This is a deterministic synthetic software-concordance check only. It does not close the R5 exit gate: no experimental reference structures, full mmCIF semantics, biological assemblies, SASA/interaction chemistry concordance, large-structure benchmark, offline viewer or Android device measurements are claimed.


### Exact-source host reference CI — 2026-11-09

The structural parser/geometry comparison passed in the pinned scientific-reference job at commit `f1681ea5e2009f8bcbc33468689108affe57e56c`, CI run #2105. Biopython 1.88 parser metadata/coordinates, NumPy contact distances and independent SVD/Kabsch RMSD all passed their recorded tolerances. The host reference artifact is recorded in `docs/ci-build-evidence.md`.

This closes the new synthetic software-concordance check only. It does not meet R5's experimental structure, mmCIF, SASA/interaction, benchmark, viewer or device exit criteria.
