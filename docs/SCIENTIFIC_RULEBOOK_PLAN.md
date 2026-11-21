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

## 6. Molecularis-owned rule authoring and scientific generation

The rulebook is part of the Molecularis-owned scientific framework. It must support every scientific domain in product scope and must not be limited to validating imported data.

### Rule authoring

Provide a governed authoring model for scientists and domain specialists to define:
- declarative constraints and invariants;
- equations, physical/chemical models and numerical methods;
- allowed ranges, units, boundary conditions and applicability domains;
- objective functions, scoring terms and optimization criteria;
- transformation and normalization procedures;
- uncertainty, confidence, abstention and failure semantics.

A rule is executable only when its inputs, outputs, units, assumptions, scope, tolerances, dependencies and failure behavior are specified. Rule authorship, technical implementation and independent scientific review must be distinguishable roles. Rules must be versioned, testable, attributable and reviewable; user-defined rules must not silently become globally trusted defaults.

### Rule execution and composition

Define a Molecularis-owned rule representation and execution contract that can be implemented across Python, Rust and C++ backends. Rules may compose into domain workflows, but composition must preserve units, coordinate/reference conventions, preconditions, postconditions and provenance. Execution must be deterministic where the method permits it and must record seeds and numerical environment where it does not.

### Candidate generation and optimization

Treat generation as a first-class scientific operation. A generator accepts a typed goal/specification and explicit constraints, constructs candidate scientific artifacts, evaluates feasibility and optionally optimizes a declared objective. Initial artifact families may include sequences, molecular graphs, conformations, 3D structures, topologies, simulation inputs and analysis workflows. A generator must report unsatisfied constraints, search limits, approximations and non-uniqueness rather than silently returning an apparently definitive answer.

### Independent validation

Generation and validation are separate interfaces and, where practical, separate implementations or methods. Validate generated outputs using independent invariants, reference implementations, benchmark fixtures, numerical diagnostics and experimental evidence when available. A successful rule check establishes only that the checked conditions passed within their declared scope; it does not establish experimental correctness, biological function or clinical validity.

### External engines and resources

Upstream projects may supply reusable algorithms, parsers, numerical kernels, inference engines, simulation engines or independent validators. Molecularis owns the surrounding contracts, rule semantics, workflow composition and provenance model. Keep upstream engines replaceable and optional. Track code licences, model/weight terms, parameter-set terms and dataset terms separately. A required reference genome, template, model weight, force-field parameter set or other resource must be declared per method; do not make a universal database dependency.

## 7. Implementation method

1. Inventory existing validators, generators, schemas and scientific methods.
2. Define Molecularis-owned scientific object, goal, constraint, rule and artifact contracts.
3. Define rule authoring, review, versioning, execution and composition semantics.
4. Define generation and optimization interfaces separately from validation interfaces.
5. Specify one versioned rulebook and generator contract per domain; map existing/upstream engines to those contracts.
6. Add positive, negative, boundary, infeasible-goal and malformed-input fixtures.
7. Compare generated and validated outputs with independent reference methods, benchmarks and experimental evidence where available.
8. Record tolerances and reasons; do not tune thresholds solely to make tests pass.
9. Add regression tests and a migration policy for schema/rule changes.
10. Obtain independent domain review before using rules for scientific claims.

## 8. Governance

Each rule requires an identifier, definition, rationale, units, scope, severity, method/version, test fixtures, known limitations, owner and review date. Breaking changes require schema versioning and a migration note. Rulebook completion is not clinical validation or regulatory clearance.
