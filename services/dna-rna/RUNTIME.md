# DNA/RNA Runtime — G

Python v1 integrated with the local MSDE reference runtime. Start MolecularisPlatform, register_dna_rna_service, ingest NucleicAcidDocument via ingest_nucleic_acid and execute with dna_rna_rulebook. Reports identify source digest, operation, Rulebook version and checked rules; derived outputs retain MSDE input lineage. Serialization is sorted compact UTF-8 JSON and duplicate keys reject.

Artifact reads obey Budget.max_bytes. Translation is bounded by candidate budget. RNA folding is limited to 300 residues and caller budget may lower it. Cubic DP is synchronous; current in-process platform cannot preemptively cancel handlers or enforce OS-level CPU/memory isolation. Wall-clock budget is not a hard interrupt.

Malformed records raise ValueError/TypeError; wrong artifact contracts raise ValidationError; resource exhaustion raises ResourceLimitError; missing artifacts use platform typed errors. NUPACK/NUAD are not dependencies or invoked. Future adapters require explicit local installation, version/license record, pinned inputs, bounded process execution and output validation. No automatic model/database download. Shared platform owns lifecycle and shutdown.


## Agentics scientific execution requirements

Validate sequence alphabet, strand/direction conventions, chemical/thermodynamic parameters, units, conditions and resource budgets before execution. Preserve algorithm/model versions, parameters, data sources, environment and lineage. Optional folding/design tools must fail explicitly when unavailable. See ../ai/AI_CONSTITUTION.md.
