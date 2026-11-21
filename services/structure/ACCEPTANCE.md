# Structure v1 Acceptance Record

Status: engineering implementation complete. University review, cross-reference testing and formal contract freeze are deferred until the full A–N build, as directed by the repository owner.

- [x] Existing Structure modules inventoried and retained.
- [x] Canonical immutable StructureDocument and strict JSON contract.
- [x] PDB and mmCIF ingestion through existing parsers.
- [x] MSDE artifact ingestion, digest/metadata verification and parent lineage.
- [x] Six deterministic capabilities and executable Rulebook.
- [x] Versioned artifact, record and operation-report schemas.
- [x] Unit/integration tests for parsing, canonical identity, integrity, budgets, geometry, contacts, SASA, interaction candidates and RMSD.
- [x] CI benchmark smoke added for bounded geometry workload.
- [x] CI run #158 passed: core 636 passed/12 skipped; optional sequence 639 passed/9 skipped, genomics 637 passed/11 skipped, chemistry 644 passed/4 skipped; 34 JSON Schemas and capability registry validated.
- [ ] University scientific review after completion of A–N.
- [ ] Independent PDB/mmCIF reference concordance, including quoted CIF tokens and alternate locations.
- [ ] Reference comparison for RMSD, contacts, SASA and interaction calculations.
- [ ] Performance and memory scaling study on representative macromolecular structures.
- [ ] Decide whether to extend v1 coordinate metadata before contract freeze.

This record certifies engineering implementation only, not independent scientific acceptance or production fitness.


## Agentics scientific acceptance

- [ ] Structural scope, coordinate conventions, units, assumptions and validity domain documented: Linear algebra, coordinate geometry, differential geometry/topology, mechanics, crystallography, numerical optimization, structural statistics and uncertainty.
- [ ] Pre-generation validation covers structure schema, units, frames, constraints and resource limits.
- [ ] Post-generation checks independently evaluate applicable geometry, topology, stereochemistry and physical criteria.
- [ ] Tolerances, uncertainty, limitations and evidence class are reported.
- [ ] Inputs, methods, versions, parameters and artifact lineage are reproducible.
- [ ] Optional tools have exact license/version and verification evidence.
- [ ] Engineering and scientific acceptance reported separately.

Shared requirements: ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_FOUNDATION.md.
