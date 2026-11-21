# S2 — Structure quality metrics and badge policy

## Current implementation

`python/molecularis/structure_quality.py` reports atom/residue counts, supported/unknown element coverage, bounded nonbonded steric-overlap candidates and severe-overlap counts. A spatial cell index bounds candidate enumeration; callers can cap atom and candidate-pair counts.

The same module now exposes `backbone_torsion_angles`, a bounded N/CA/C backbone geometry calculation. It reports observed phi/psi angles in degrees only when the required adjacent backbone atoms exist and residue numbering is contiguous. Missing atoms, termini and numbering gaps remain unavailable; no coordinates are reconstructed and no Ramachandran outlier grade is assigned.

The report deliberately returns `quality_badge: not_assessed`. These metrics are not MolProbity clashscore and do not provide calibrated Ramachandran/rotamer, bond geometry, resolution/R-free or pLDDT/PAE measures. The shared Atom model does not preserve insertion codes, alternate locations, occupancy, hydrogen positions or bond topology. Unknown elements are counted and excluded rather than assigned guessed radii.

## Exit evidence still required

- Fixed experimental and predicted structure sets with trusted reference reports.
- Independent clashscore/Ramachandran/rotamer/geometry concordance and prespecified tolerances.
- Model-vs-experimental provenance and resolution/R-free/pLDDT/PAE ingestion.
- Calibrated badge thresholds, false-positive/false-negative review and uncertainty reporting.
- Large-structure memory/runtime benchmarks and low-end Android integration.
- User-visible explanations for every badge and missing metric.

Until those are complete, UI must show metrics as screening observations and use a neutral "not assessed" state rather than good/fair/poor.
