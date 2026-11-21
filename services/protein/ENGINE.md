# Protein Engine E — v1

Status: engineering implementation; university scientific review deferred until A–N completion.

## Canonical data
ProteinDocument stores a normalized canonical 20-residue amino-acid sequence, identifier and bounded description. Artifacts use deterministic JSON, SHA-256 identity, source lineage and integrity-checked metadata. Ambiguous/rare residues are rejected by this strict v1 artifact contract; standalone ESM inference retains its separately documented broader alphabet.

## Native capabilities
- Sequence validation and artifact integrity.
- Composition, average-residue molecular mass, mean hydropathy and theoretical pI using the documented Henderson–Hasselbalch approximation.
- Hash-pinned caller-supplied fixed-width motif scans with explicit wildcard semantics.
- Non-generative protein-design brief validation and mandatory human/release gates.

## Existing local workflows retained
ESM embeddings require operator-supplied, hash-verified local Transformers checkpoints; no download or remote code. HMMER parsers/rankers retain caller-supplied profile and threshold provenance. Structure prediction envelopes and exact sequence-to-structure mapping remain owned by Structure until cross-service integration.

## Exclusions
No native folding, de novo sequence generation, function/activity prediction, homology search, domain discovery, PTM prediction, disulfide inference, toxicity/clinical assessment or biological safety certification. ESM embeddings are representations, not calibrated functional predictions.


## Shared Agentics scientific foundation

Participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. Priority disciplines: Biochemistry, molecular biology, sequence evolution, structural biology, geometry, statistical mechanics, thermodynamics, probabilistic inference and structural uncertainty.

Use shared contracts for units, evidence, uncertainty and provenance while retaining protein-specific semantics and validators. Agentics cannot replace this service's scientific engine or Rulebook. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
