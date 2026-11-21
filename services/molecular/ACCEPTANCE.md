# Service A — Molecular v1 Acceptance Record

Status: implementation delivered; final CI verification and independent scientific approval pending.

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

- [ ] CI run for the implementation commit is green.
- [ ] All three Molecular schemas pass the repository schema validator.
- [ ] Molecular tests pass, including Rulebook success/failure and provenance checks.
- [ ] Benchmark harness runs at 1k and 10k atom scales; record machine/runtime details before setting performance thresholds.
- [ ] Scientific reviewer confirms fixture provenance and approves MOL-001 through MOL-010.
- [ ] Public API and service manifest are reviewed and v1 contracts frozen.

## Scope boundaries

This is a foundational molecular graph service, not a complete chemistry engine. It does not infer valence, aromaticity, protonation, tautomerism, stereochemistry, implicit hydrogens, force fields, conformers or energetic properties. Existing RDKit functionality remains an optional Chemistry adapter. Python is the only implemented runtime; C++/Rust bindings are future work.

No clinical or experimental interpretation is implied by passing structural validation.
