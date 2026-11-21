# Structure Engine

Status: Python v1 engineering implementation complete; university review is deferred until the full A–N build.

## Responsibility and reused implementation

Structure owns macromolecular coordinate representation, PDB/mmCIF ingestion, geometric summaries, contact screening, approximate solvent-accessible surface area (SASA), distance-based interaction candidates and RMSD comparison. Coordinates are right-handed Cartesian Angstroms.

Existing Molecularis modules are retained: `structure.py` provides parsers, raw and Horn-quaternion superposed RMSD, distance contacts, deterministic Shrake–Rupley SASA and geometric interaction candidates. Existing pocket, quality, prediction, visualization and Biotite adapters remain available separately; optional packages are not hidden runtime dependencies.

## Canonical artifact and capabilities

`molecularis.structure-record.v1` stores identifier, source format, model number, coordinate convention and ordered atom records. Canonical JSON bytes define SHA-256 identity. MSDE artifacts are immutable, lineage-aware and metadata-verified.

Capabilities: validate, geometry, contacts, sasa, interactions and rmsd. RMSD consumes two artifacts and requires caller-matched atom order; it does not infer atom correspondence.

## Limits

PDB parsing handles fixed-column ATOM and optional HETATM records and selects blank/A alternate locations. mmCIF parsing reads atom_site loops and label/auth fallbacks; it is not a complete CIF grammar/dictionary interpreter. Current records omit occupancy, B-factor, insertion code, anisotropic displacement, assembly operators, symmetry and ensembles. Contacts/interactions are geometric candidates, not validated bonds or energies. SASA uses generic radii and finite Fibonacci sampling without adding hydrogens. No missing-atom reconstruction, loop modelling, folding, force field, docking, electron-density refinement or biological assembly inference is claimed.
