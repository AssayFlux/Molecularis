# DNA/RNA Rulebook — G

Rulebook ID: dna-rna-core-v1; version 1.0.0; executable engineering rules, scientific review pending.

| Rule | Constraint | Acceptance |
|---|---|---|
| DRNA-001 | Record exactly DNA or RNA, non-empty, uppercase, valid declared IUPAC alphabet. | Invalid symbols and empty records reject. |
| DRNA-002 | Exact canonical JSON fields; duplicate keys reject; SHA-256 covers canonical bytes. | Stable round-trip bytes and digest. |
| DRNA-003 | Artifact metadata, media type, schema and content digest agree. | Tampering/wrong type rejects. |
| DRNA-004 | Strand semantics explicit: transcription treats DNA as coding/sense; reverse transcription preserves corresponding orientation. | No silent template-strand claim. |
| DRNA-005 | Translation uses explicit NCBI table/frame; no organism/gene inference. | Unsupported tables and invalid CDS fail closed. |
| DRNA-006 | Primer screen accepts canonical A/C/G/T 15–40 nt and reports Wallace limitations. | Not nearest-neighbour thermodynamics or specificity. |
| DRNA-007 | RNA fold accepts canonical A/C/G/U, AU/GC/GU non-crossing pairs, minimum loop and hard ceiling. | Deterministic Nussinov; ambiguous and over-budget inputs reject. |

Operations: validate, statistics, reverse_complement, transcribe, reverse_transcribe, translate, primer_screen, fold_rna. Each is an MSDE capability with source digest and rule IDs. Wallace Tm is heuristic; Nussinov is maximum-pair approximation, not calibrated free energy. No function, binding affinity or experimental success is inferred. Breaking contracts require new schema/capability versions; changed scientific semantics require new Rulebook version and fixtures. External adapter evidence stays separate.
