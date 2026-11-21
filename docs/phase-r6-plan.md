# R6 — Computational chemistry

**Status:** In progress. Graph descriptors and fingerprints are exploratory only.

## Scope
- Multi-record SDF V2000 parsing and conservative V3000 atom/bond parsing with coordinate, identifier and bond validation.
- Bounded graph descriptors, exact element/bond-order substructure matching and path fingerprints/Tanimoto similarity.
- Added an optional RDKit adapter for sanitized SMILES/molblock parsing, canonical isomeric SMILES, standard descriptors and Morgan radius-2 fingerprints/Tanimoto. RDKit is not bundled in Android; Android ABI, transitive dependencies, version pin, binary size and license notices remain unapproved. Protonation/tautomer workflows, conformers and Android production integration remain open.

## Current source
Implemented in `python/molecularis/chemistry.py`. Resource caps apply to substructure traversal and path fingerprints.

## Limitations
- V3000 support is limited to basic atom/bond graph records; stereochemical and other V3000 attributes are not interpreted. Robust SMILES is not implemented.
- No stereochemical interpretation or aromaticity model.
- Molecular formula and mass are based on explicit parsed atoms; implicit hydrogens are not inferred.
- Fingerprints are custom exploratory graph paths, not ECFP/Morgan fingerprints.

## Exit evidence
Reference SDF/SMILES corpus; concordance against an owner-approved engine; stereochemical and valence edge cases; deterministic descriptor/fingerprint definitions; adversarial resource-limit tests; license and Android ABI review.


## Representation and provenance contract (2026-11-09)

The optional RDKit adapter now returns a SHA-256 and UTF-8 byte count for the
exact supplied SMILES/molblock text, with no pre-parser text normalization. Results
also disclose canonical isomeric SMILES, RDKit sanitization/aromaticity, input
protonation and tautomer retention (no adjustment/canonicalization), stereochemistry
handling (unassigned centres are reported, not inferred), hydrogen handling and
units (Da and Å²). This improves auditability but does not resolve tautomer,
protonation, stereochemical or conformational ambiguity. The adapter remains
host-only; Android packaging and independent chemistry validation remain open.


## Host-side SDF graph concordance — 2026-11-09

The pinned RDKit sanity harness now also parses an explicit-atom cyclopropane V2000 fixture through both the local SDF parser and RDKit. It compares atom/bond counts, element and bond-order identity, coordinates, and graph cycle rank versus RDKit ring count. The result is fail-closed in CI and covered by the optional RDKit test.

This is a synthetic graph/parser check, not approval of RDKit for Android or proof of chemical validity. The local parser intentionally counts only explicit atoms and does not infer implicit hydrogens; stereochemistry, aromaticity, protonation, tautomerism and production engine/licensing decisions remain open.
