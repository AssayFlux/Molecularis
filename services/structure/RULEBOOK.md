# Structure Rulebook

Rulebook ID: `structure-core-v1`, version 1.0.0.

| Rule | Requirement | Acceptance behavior |
|---|---|---|
| STR-001 | Stable bounded structure identity | Non-empty identifier, bounded length, no control characters |
| STR-002 | Canonical atom records | Non-empty bounded atom array, required labels and unique serials |
| STR-003 | Finite coordinates | All Cartesian coordinates finite |
| STR-004 | Explicit coordinate convention | Right-handed Cartesian Angstroms only |
| STR-005 | Strict versioned serialization | Exact fields, schema ID, duplicate-key rejection and canonical SHA-256 |
| STR-006 | Artifact integrity and provenance | Stored media/schema, digest and metadata agree before execution |
| STR-007 | Bounded deterministic geometry | Operation-specific atom/sample limits and explicit parameters |

## Capabilities

- `structure.validate.v1`: artifact integrity and contract validation.
- `structure.geometry.v1`: atom/residue/chain counts and coordinate bounding box.
- `structure.contacts.v1`: inter-residue atom pairs within a distance cutoff.
- `structure.sasa.v1`: finite-resolution Shrake–Rupley area estimate.
- `structure.interactions.v1`: distance-only H-bond, salt-bridge and disulfide candidates.
- `structure.rmsd.v1`: raw or optimally superposed RMSD for two caller-matched coordinate arrays.

No operation implies chemical correctness, energetic stability, biological function or clinical interpretation. Imported coordinates preserve source assertions, not independent validation.


## Agentics scientific rules

- Apply **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn** without weakening domain rules.
- Pre-audit inputs, coordinate systems, units, assumptions, constraints, evidence versions and applicability.
- Apply structural/mechanical/crystallographic principles only within stated assumptions and validity domains.
- Independently verify geometry, topology, stereochemistry, clashes, physical plausibility and numerical tolerances as applicable; proposer is not sole verifier.
- Preserve evidence class, uncertainty, limitations and provenance. A valid coordinate model is not proof of stability or function.
- Optional tools require version/license review, typed adapters, resource limits and independent checks.

Priority disciplines: Linear algebra, coordinate geometry, differential geometry/topology, mechanics, crystallography, numerical optimization, structural statistics and uncertainty.
See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
