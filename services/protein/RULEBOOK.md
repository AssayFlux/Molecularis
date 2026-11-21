# Protein Rulebook E — protein-core-v1

Status: executable engineering baseline; scientific review pending.

- PRO-001 Identity: exact canonical Protein v1 schema and deterministic SHA-256 identity.
- PRO-002 Sequence: non-empty uppercase canonical 20-amino-acid sequence; whitespace is normalized; ambiguity and rare residues are rejected in the artifact contract.
- PRO-003 Descriptors: values apply to unmodified linear peptides, average residue masses and free termini; pI uses the declared pKa approximation and bisection, not a universal experimental constant.
- PRO-004 Motifs: only caller-supplied, hash-pinned fixed-width literal motifs with '.' wildcard are scanned; no regular expressions or family/function inference.
- PRO-005 Design brief: human review is mandatory; no sequence generation or candidate ranking is performed.
- PRO-006 Provenance: model weights, motif packs, profile databases, licences, versions and run provenance must be retained and independently reviewed before scientific claims.

Rules are operational constraints, not evidence of experimental function, folding, safety or clinical validity.


## Agentics scientific rules

- Apply the universal lifecycle under this service's scientific authority.
- Pre-audit sequence/structure identity, residue mapping, assumptions, conditions, evidence versions and applicability.
- Distinguish prediction, simulation, constructed hypothesis and experimentally validated structure/function.
- Independently verify structural geometry and applicable biochemical/physical claims; a predictor cannot verify itself.
- Record uncertainty, alternatives, provenance, checkpoint/data licenses and limitations.
- Optional predictors and external engines require version/license review, isolated adapters and independent benchmarks.

Priority disciplines: Biochemistry, molecular biology, sequence evolution, structural biology, geometry, statistical mechanics, thermodynamics, probabilistic inference and structural uncertainty.
See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
