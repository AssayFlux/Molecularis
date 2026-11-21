# Biotite upstream audit

**Review date:** 2026-11-21  
**Molecularis target:** `CORE`  
**Disposition:** evaluated; do not add to the base dependency set or bundle in Android yet  
**Scope:** source, package metadata, licence and fit against the current Molecularis structure layer

## Upstream identity

- Repository: https://github.com/biotite-dev/biotite
- Reviewed branch: `main`
- Reviewed commit: `2effe8f30543602fc9ee58759a4e16066062b290` (2026-11-11)
- Licence declared in upstream `pyproject.toml`: BSD-3-Clause
- Licence text: upstream `LICENSE.rst`; source and binary redistribution require retaining/reproducing the copyright notice, conditions and disclaimer. The non-endorsement condition also applies.
- Upstream package metadata declares `license-files = ["LICENSE.rst", "THIRDPARTY.yml"]`. The third-party notice file was not successfully retrieved in this review; transitive/component notices remain an open gate.
- Upstream describes sequence/structure file IO, analysis, visualization and database interfaces. The reviewed structure source includes mmCIF and BinaryCIF file representations and conversion functions.

## Material technical findings

### Runtime and dependency fit

The reviewed upstream `pyproject.toml` declares:

- Python `>=3.12`
- NumPy `>=2.1`
- biotraj `>=1.0,<2.0`
- requests `>=2.12`
- msgpack `>=0.5.6`
- networkx `>=2.0`
- packaging `>=24.0`

The PDBx conversion source imports `biotite.rust.structure.io.pdbx`, so the distribution includes a native Rust component. The project also maintains Pixi environments with additional scientific and external-tool dependencies; those are not all mandatory runtime dependencies, but each optional feature still needs a scoped dependency and licence review.

Molecularis currently declares Python `>=3.10` and has no mandatory scientific Python dependencies. Adding the current Biotite main-line release to the base environment would therefore break the declared Python 3.10/3.11 compatibility and expand the dependency/native-build surface. Do not silently raise the global Python floor to accommodate one adapter.

### Useful capabilities

The inspected PDBx code provides more than the current Molecularis atom-site loop reader:

- CIF data blocks/categories/columns and explicit handling of missing/inapplicable values.
- BinaryCIF file support and PDBx conversion paths.
- Conversion between PDBx data and Biotite AtomArray/AtomArrayStack representations.
- Sequence extraction from polymer entity metadata.
- Structure annotations including chain, residue, insertion code, residue name, hetero flag, atom name and element.
- Structure conversion code references model counts, assemblies, unit cells, secondary-structure assignment, alternate-location filters and bond lists.

These are relevant gaps for Molecularis: its current shared Atom dataclass does not preserve insertion codes, model identity, occupancy, alternate-location identifiers, formal bonds, unit-cell/symmetry data or full residue/atom identity. The current mmCIF reader is intentionally a limited `_atom_site` loop parser, not a complete CIF dictionary/assembly implementation.

### Integration risks and constraints

- Biotite's AtomArray is a richer data model than Molecularis's current Atom dataclass. A lossy direct conversion would silently discard scientific identity fields.
- Molecularis must define canonical residue/atom identifiers and explicit mapping/round-trip rules before using Biotite objects as an interchange model.
- BinaryCIF and assembly support should be tested against pinned reference files, not inferred from the presence of APIs.
- Native Rust extension wheels/builds, architecture support, Python ABI, offline installation, binary footprint and supply-chain provenance have not been tested in Molecularis.
- No model weights or reference datasets are required for the basic parser integration, but external database fetch functionality must remain opt-in and must not introduce implicit network access.
- BSD-3-Clause is compatible in principle with the project direction, but the full third-party notice set and exact distributed wheel contents still need review. Do not treat the upstream top-level licence as clearance for every bundled component.

## Molecularis comparison

Current implementation and tests:

- `python/molecularis/structure.py`: PDB parsing, a limited mmCIF `_atom_site` loop parser, geometry and RMSD.
- `python/molecularis/structure_view.py`: bounded deterministic viewer payload with Angstrom coordinates and explicit limitations.
- `tests/test_structure.py`: small synthetic fixtures for PDB/mmCIF, RMSD, SASA and geometric interaction candidates.
- `docs/scientific-engine-decisions.md`: already records the limited parser scope and the Mol* viewer as a separate candidate.

The existing parser should remain available as a dependency-free, bounded import path. Biotite should be an optional, isolated parser/analysis engine behind a Molecularis-owned adapter. Never expose raw Biotite object structures as the stable public contract.

## Recommended integration design

1. **First define the lossless canonical structure contract.** Add explicit fields/identifiers for model number, atom serial, atom name, alternate location, residue name, chain/entity identifiers, residue sequence number, insertion code, element, occupancy, B-factor, hetero status, coordinates, coordinate units, bonds and source-format provenance. Define null/missing semantics and stable atom/residue keys.
2. **Create a Python 3.12+ optional engine profile**, not a base dependency. Pin a released Biotite version and its complete dependency graph; use a lock file and hashes. Do not use a floating `main` dependency.
3. **Implement an adapter that normalizes Biotite CIF/BinaryCIF/PDB input into the canonical contract.** Preserve all available identity and model fields; reject or explicitly report unsupported/lossy conversions. Keep the Molecularis parser as the minimal fallback.
4. **Add differential and round-trip fixtures.** Include multi-model structures, insertion codes, alternate locations, missing CIF values, non-polymer ligands, waters, anisotropic/occupancy fields where supported, assemblies and BinaryCIF. Compare atom counts, identifiers, coordinates, units and bonds against pinned expected values and an independent parser/reference.
5. **Add resource and security bounds** for input bytes, token/category counts, atom count, models, decompression, CPU/time and memory. Ensure no network access is required for local parsing.
6. **Complete licensing and platform review** for the exact release, Rust extension wheels, all transitive dependencies and notices before redistribution. Test offline install on supported Linux targets; Android bundling is a separate decision.
7. **Only then** promote the adapter through the project's evidence ladder. Parser agreement is software/reference validation, not biological interpretation or experimental validation.

## Decision

**Proceed to canonical structure-contract design and a Linux host-only proof of concept. Defer direct dependency integration and Android bundling.** The current upstream main branch's Python `>=3.12` requirement conflicts with Molecularis's `>=3.10` package contract, and the richer atom model requires a lossless mapping before an adapter can be scientifically safe.

This is an upstream source audit, not a claim that Biotite has been installed, executed, benchmarked or integrated in Molecularis. No scientific validation is claimed.
