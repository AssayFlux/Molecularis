# Molecularis — Scientific Rulebook Plan

**Status:** Design plan; rules and thresholds require domain review and evidence.  
**Date:** 2026-11-20

## 1. Purpose

Create a versioned, testable scientific rulebook that makes data interpretation consistent across Android, Python, C++/Rust components and desktop engines. The rulebook defines semantics and validation boundaries; it does not replace specialist scientific judgement or independent validation.

## 2. Canonical data concepts

Define schemas and shared terminology for:
- biological entities, sequences, alphabets, ambiguity symbols and sequence coordinates;
- proteins, chains, residues, atoms, alternate locations, insertion codes and model numbers;
- molecules, atoms, bonds, formal charges, isotopes, stereochemistry and conformers;
- coordinate frames, coordinate units, transforms and periodic boxes;
- physical quantities, dimensional units, temperature, pressure, energy and time;
- reference datasets, provenance, confidence/uncertainty and quality observations.

Identifiers must be stable and unambiguous. Preserve source identifiers and original values alongside normalized values; never silently discard alternate conformations, residue numbering or stereochemistry.

## 3. Rule classes

1. **Parsing rules:** accepted formats, encoding, malformed-file behaviour and resource ceilings.
2. **Normalization rules:** canonical representation and reversible transformations.
3. **Physical rules:** units, dimensions, coordinate conventions, boundary conditions and numerical tolerances.
4. **Scientific checks:** geometry, sequence consistency, stereochemistry, topology and domain-specific invariants.
5. **Quality observations:** measured quantities with method/version and evidence; avoid unsupported categorical grades.
6. **Provenance rules:** input hashes, source, engine, parameters, reference-data version and environment.
7. **Uncertainty rules:** distinguish measured, predicted, inferred, missing and not-assessed values.

## 4. Required result semantics

Every reported scientific value should carry:
- value and unit where applicable;
- method and method version;
- source/input reference;
- uncertainty or confidence where defined;
- validation state and applicable limitations.

Use explicit states such as `not_assessed`, `not_applicable`, `not_available`, `failed_validation` and `validated_within_scope`. Missing evidence must never be rendered as a passing score.

## 5. Domain rulebooks

- **Sequence:** alphabet validation, ambiguous symbols, lengths, gaps, coordinate mapping and sequence identity.
- **Structure:** chain/residue/atom identity, coordinate integrity, clashes, bond geometry, torsions, missing atoms and alternate locations.
- **Chemistry:** valence, aromaticity, formal charge, stereochemistry, sanitization and descriptor definitions.
- **Simulation:** units, topology, force-field provenance, constraints, integration settings, equilibration and energy diagnostics.
- **Genomics:** reference genome/build, coordinate conventions, strand, variant representation and annotation provenance.
- **Design:** explicit constraints, objective functions, thermodynamic model/version and feasibility semantics.

## 6. Implementation method

1. Inventory existing validators and schemas.
2. Define one versioned rule specification per domain.
3. Map existing implementations to rules; identify gaps and conflicting semantics.
4. Add positive, negative, boundary and malformed-input fixtures.
5. Compare outputs with independent reference tools/datasets.
6. Record tolerances and reasons; do not tune thresholds solely to make tests pass.
7. Add regression tests and a migration policy for schema/rule changes.
8. Obtain independent domain review before using rules for scientific claims.

## 7. Governance

Each rule requires an identifier, definition, rationale, units, scope, severity, method/version, test fixtures, known limitations, owner and review date. Breaking changes require schema versioning and a migration note. Rulebook completion is not clinical validation or regulatory clearance.
