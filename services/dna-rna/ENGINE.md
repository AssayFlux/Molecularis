# DNA/RNA Engine — G

Status: Python v1 engineering implementation.

Owns canonical single-strand DNA/RNA artifacts and deterministic operations. Reuses B's sequence parser/genetic-code tables, A's molecular primitives and shared MSDE; does not duplicate FASTA/FASTQ, genome/variant or general alignment workflows.

Native operations: IUPAC-normalized typed DNA/RNA records; nucleotide composition and GC fraction; IUPAC DNA reverse complement; coding/sense DNA transcription and corresponding RNA-to-DNA alphabet conversion; explicit NCBI-table translation; bounded DNA oligo screen (length, GC, Wallace Tm, GC clamp); RNA secondary candidate by Nussinov maximum-pair DP with AU/GC/GU, minimum loop and deterministic traceback.

Artifact digest covers canonical JSON bytes; metadata is verified on load. Nussinov is O(n^3) time/O(n^2) memory, hard-limited to 300 nt. Wallace Tm is a rough heuristic only. Translation does not infer organism or gene boundaries.

Non-goals: no NUPACK thermodynamic ensemble/partition function, multi-strand complex design, hybridization free energy, NUAD automated design, kinetic folding, pseudoknots, tertiary folding, modified-base model, primer-pair specificity, wet-lab protocol or biosafety certification. Future adapters must be optional, pinned and provenance-bearing; native execution never silently delegates. University scientific comparisons and acceptance deferred until A–N engineering completes.


## Shared Agentics scientific foundation

Participates in **Understand → Represent → Reason → Construct → Evaluate → Verify → Learn**. Priority disciplines: Molecular biology, nucleic-acid chemistry, polymer physics, thermodynamics, statistical mechanics, sequence algorithms, folding and hybridization models.

Use shared unit, evidence, uncertainty and provenance contracts while retaining nucleic-acid-specific models and validators. See ../ai/SCIENTIFIC_FOUNDATION.md and ../ai/AI_CONSTITUTION.md.
