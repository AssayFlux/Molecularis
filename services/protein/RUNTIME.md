# Protein Runtime E — v1

Protein service registers deterministic versioned operations on the shared MSDE platform. Canonical sequence artifacts are immutable, byte-bounded and SHA-256 verified on load. Parent lineage is retained by the platform. All motif-pack bytes are hash-verified by the existing scanner; caller metadata includes source, version and licence.

Limits: 5,000,000 canonical residues per artifact; 2 MiB motif pack; scanner defaults cap query length, motif count, comparisons and hits. Protein design briefs are bounded by their validator. ESM execution is an explicit separate local operation with verified model-directory digest, CPU/CUDA selection, batch and residue ceilings; PyTorch/Transformers are optional and weights are operator-supplied. No network access or implicit model download is permitted.

Errors fail closed on malformed contracts, artifact mismatch, unsupported residue symbols, missing optional runtime or exceeded resource ceilings. Runtime currently uses trusted in-process Python handlers; OS sandboxing and preemptive cancellation remain Core-level work.


## Agentics scientific execution requirements

Validate sequence/structure inputs, residue conventions, units, conditions, method applicability and resource budgets. Preserve model/checkpoint and tool versions, parameters, source artifacts, environment, random seeds and lineage. Optional predictors are not authoritative; unavailable tools fail explicitly. AI output is untrusted. See ../ai/AI_CONSTITUTION.md.
