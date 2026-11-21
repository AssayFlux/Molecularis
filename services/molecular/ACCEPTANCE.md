# Service A — Molecular v1 Acceptance Record

Status: v1 engineering implementation complete; CI green; independent scientific approval and formal contract freeze pending.

## Delivered implementation

- Canonical dependency-free atom/bond/residue/chain/molecule graph model.
- Structural invariants for identity, element symbols, formal charges, isotopes, bond references, duplicate edges, coordinate completeness and reciprocal hierarchy.
- Formula, atom/bond counts, net formal charge, adjacency, degree and connected-component operations.
- Strict JSON parsing: version/unit/frame enforcement, exact field sets, duplicate-key rejection and non-finite constant rejection.
- Canonical UTF-8 serialization and SHA-256 content identity.
- Immutable MSDE artifact ingestion/loading with metadata, parent lineage, content verification and byte budgets.
- Executable molecular.validate.v1 capability and molecular-structural-validation Rulebook, with persisted output artifact and run evidence.
- Versioned schemas for molecule documents, artifact references and validation reports.
- Water and glycine-backbone hierarchical fixtures.
- Unit, parser, schema, artifact, Rulebook and provenance tests.
- Reproducible linear-chain graph benchmark harness.

## Verification required

- [x] [CI run #148](https://github.com/AssayFlux/Molecularis/actions/runs/44883726169) is green on commit fb2afc2.
- [x] All 28 repository JSON Schemas, including all three Molecular schemas, pass validation in run #148.
- [x] 606 tests pass (12 skipped); Molecular Rulebook success/failure and artifact provenance tests are included.
- [x] Benchmark smoke passed on GitHub ubuntu-latest / Python 3.11.18: 1k atoms/999 bonds construction 0.00612 s, components 0.00049 s; 10k atoms/9,999 bonds construction 0.05971 s, components 0.00645 s. Single-run smoke measurements only; no performance threshold is asserted.
- [ ] Scientific reviewer confirms fixture provenance and approves MOL-001 through MOL-010.
- [ ] Public API and service manifest are reviewed and v1 contracts frozen.

## Scope boundaries

This is a foundational molecular graph service, not a complete chemistry engine. It does not infer valence, aromaticity, protonation, tautomerism, stereochemistry, implicit hydrogens, force fields, conformers or energetic properties. Existing RDKit functionality remains an optional Chemistry adapter. Python is the only implemented runtime; C++/Rust bindings are future work.

No clinical or experimental interpretation is implied by passing structural validation.
