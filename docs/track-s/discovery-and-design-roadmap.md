# Track S — Protein, genome and sequence discovery roadmap

**Status (2026-11-11):** Track S is the active sequential engineering track under D-019/D-022. S1–S9 now have bounded software foundations, including ligand-site and apo-pocket geometry candidates (S3), conservative genetic-code candidate screening (S8), local execution/evidence adapters (S4/S6/S7/S9), and viewer export/state work (S1/S5). Exact-head CI and final source audit remain required. D-021 external scientific validation, licensed resources/models, secure inference and physical-device evidence are explicit carry-forward gates; no scientific acceptance is implied.

## Mission

Turn Molecularis into a research workbench that can investigate unfamiliar DNA/RNA/protein sequences, infer and explain candidate biological meaning, compare structures and families, and support constrained computational protein design. Outputs must remain reproducible, uncertainty-aware research hypotheses. A sequence annotation is not proof of function; a designed sequence is not proof of folding, activity, safety or manufacturability.

## Work packages

### S6 — Sequence intelligence and unknown-sequence triage
- Accept large FASTA/FASTQ and annotated genome/contig inputs with streaming, bounded-memory parsing, provenance and format validation. A bounded streaming wrapped-FASTQ iterator is now implemented; full end-to-end workflow integration remains.
- Detect likely coding regions, ORFs, splice-aware candidates where evidence permits, and report alternative hypotheses rather than one forced answer.
- Search local, version-pinned gene/protein reference packs; support remote search only through an explicitly configured, consented node/service.
- Provide similarity, domain, motif, conserved-region and family evidence with database/version, alignment coverage, identity, E-values or calibrated scores where applicable.
- Report unknown/no-hit sequences honestly; distinguish no database match from evidence of novelty.
- Exit evidence: curated positive/negative fixtures, reference concordance, reproducible search packs, memory/runtime bounds, calibrated thresholds and explicit false-positive/false-negative analysis.

### S7 — Genome annotation and gene discovery
- Support prokaryotic and eukaryotic workflows as distinct pipelines; do not present bacterial ORF finding as general eukaryotic gene prediction.
- Add contig QC, repeat/low-complexity handling, gene/transcript candidates, coding potential, functional annotation, pathway context and evidence provenance.
- Track genome assembly, coordinates, strand, transcript/isoform, genetic code, database release and coordinate conventions.
- Provide batch-level coverage, unresolved regions, conflicts and annotation confidence.
- Exit evidence: independently curated genomes across organism classes, gene-boundary and functional-annotation metrics, edge-case fixtures, resource benchmarks and versioned datasets.

### S8 — Translation tables and non-standard genetic-code investigation
- Treat “unknown genetic code” as a distinct scientific problem from merely unknown DNA sequence.
- Support explicit NCBI translation-table selection and per-record genetic-code metadata before attempting inference.
- Candidate-code investigation should combine codon usage, conserved homologs, coding-frame consistency, stop-codon depletion/reassignment, organelle/taxonomic context and transcript/protein evidence. The current bounded candidate helper uses coding-frame internal-stop evidence and optional complete-CDS start/terminal-stop evidence only; it is not yet a calibrated multi-evidence classifier.
- Never silently infer a non-standard code from one short sequence. Return ranked candidate tables, supporting/contradicting evidence, sample-size limits and an unresolved state.
- Exit evidence: organism-specific positive/negative reference sets, independent confirmation, confusion matrices, calibrated abstention thresholds and regression tests for ambiguous/low-coverage cases.

### S3 — Variant, interface and pocket candidate analysis
- Exact and bounded alignment-aware sequence-to-structure mapping, variant coordinate correspondence and inter-chain contact evidence are available with ambiguity/resource abstention.
- Explicit-ligand site screening reports nearby protein residues; an apo probe-grid screen reports coarse concavity candidates accessible to a small probe but not a large probe.
- Both pocket paths are geometry-only. Element-specific chemistry, waters/ions/metals, biological assemblies, insertion codes, alternate conformations and independent reference concordance remain limitations.

### S9 — Protein family, domain and structure intelligence
- Protein physicochemical properties, signal peptides/transmembrane candidates, motifs, domains, family classification and evolutionary conservation.
- Connect sequence positions to structure residues and variants only with explicit mapping quality and missing-residue handling.
- Structure quality metrics, interfaces, pockets and residue environments must state model-vs-experimental provenance and applicability limits.
- Exit evidence: version-pinned reference families/structures, independent annotation comparisons, mapping tests and low-end device/node benchmarks.

### S10 — Constrained de novo protein design research
- Define a typed design brief: target function or binding objective, length, fold/family constraints, localization, expression host, disallowed motifs, stability/solubility goals and safety exclusions.
- Separate candidate generation from scoring, filtering and validation. Record model/weights/tokenizer versions, prompts/configuration, seeds, hardware/node, sampling settings and all filters.
- Candidate scoring may include sequence plausibility, predicted structure, confidence, aggregation/solubility heuristics, novelty and target-specific computational metrics; each score must disclose calibration and known blind spots.
- Compare candidates against known sequence/structure databases and flag similarity, patent/licensing and biosafety review needs before any downstream use.
- Require a human-reviewed experimental plan and wet-lab measurements before claiming function. No automated claim of a working protein.
- Exit evidence: model and dataset licenses approved; reproducible generation; independent held-out benchmarks; prospective experimental validation; failure analysis; compute/cost limits; biosafety review and owner approval.

## Shared architecture and quality requirements

1. Keep scientific algorithms in versioned Python/Rust domain modules, not Compose UI. Expose typed request/result schemas through the orchestrator and job/provenance store.
2. Large jobs must be cancellable, resumable where scientifically safe, resource-bounded and explicit about local-vs-node execution.
3. Every result carries input hash, tool and database versions, parameters, timestamps, random seeds, warnings, uncertainty, evidence links and limitations.
4. Unknown, unsupported, low-confidence and conflicting outcomes are first-class results; never fill missing evidence with fabricated annotations.
5. Reference packs require source, version/date, license, integrity hash, update policy and offline install/uninstall lifecycle.
6. Remote inference requires explicit user selection, consent, authenticated TLS, data-minimization, node threat model and a clear record of what left the device.
7. Do not bundle model weights, sequence databases or prediction engines until license, redistribution, privacy, ABI, memory, storage and performance reviews pass.
8. No clinical interpretation, patient workflow, autonomous wet-lab execution or unsafe biological design capability is implied. Applicable biosafety, legal and ethics review is a release gate.

## Execution order and dependencies

- S6 starts with reference-pack contracts, sequence evidence schemas and local small-scale baselines; it can use R4 parsers but must not imply exhaustive database coverage.
- S7 depends on R4 format/coordinate correctness and curated genome fixtures.
- S8 depends on S6/S7 reference metadata and independently curated organism-specific translation-table truth sets.
- S9 depends on R5 structure parsing/viewer provenance and validated residue mapping.
- S10 is planning and model/license feasibility only until compute architecture, model/data licenses, benchmark protocol and biosafety review are approved. Full generation and experimental claims are blocked until those gates pass.
- Track S begins only after the R-track implementation/host-audit gate and proceeds in its documented sequential order. No R or S exit gate is waived.

## Current honest baseline

- Existing source foundations include FASTA/FASTQ parsing, basic sequence operations, protein properties, limited PDB/mmCIF atom-site parsing, structure-analysis primitives and a deterministic structure-viewer payload contract.
- These foundations do **not** constitute production genome annotation, comprehensive unknown-gene discovery, non-standard genetic-code inference, advanced structure prediction or de novo protein design.
- S6–S8 now have bounded implementations and tests, while S9 has a conservative exact residue-mapping primitive. These remain in-progress research work packages until source, tests, reference evidence and exit gates are recorded individually; S10 remains feasibility-only and generation-gated.


## S implementation step 1 — initial execution boundary (2026-11-09)

The first S increment will harden the existing local evidence foundations before adding new inference claims:

1. **S1:** retain the strict deterministic structure-payload boundary, now with serialized UTF-8 byte and atom ceilings. Renderer selection, vendored viewer assets and WebView bridge remain gated on R1 WebView feasibility, exact-release/transitive license review and device tests. Do not introduce remote/CDN assets.
2. **S6:** harden local FASTA reference-pack manifest and byte verification, resource-limit validation, exact-match evidence and abstention. Similarity/homology search, E-values, domains and novelty inference remain unimplemented until licensed reference packs and independent calibration exist.
3. **S7:** preserve bounded six-frame ORF enumeration as a candidate generator only. Prokaryotic/eukaryotic gene annotation, transcript/splice models and annotation truth-set validation remain separate future work.
4. **S8:** explicit NCBI translation-table support remains caller-selected; no organism/genetic-code inference is authorized by these primitives.
5. **S9:** exact unique sequence-to-structure mapping remains conservative; alignment, insertion-code conversion, family/domain annotation and variant-effect claims remain out of scope until separately validated.
6. **S2–S5 and S10:** remain gated by their documented fixed-reference, model/license, node-security and biosafety requirements.

Every S increment must be tested against the exact commit. Host tests are regression evidence only; they do not close biological validation or device acceptance.


### S6 security hardening increment — bounded descriptor-based file access
- Reference FASTA and manifest files are opened as regular files through file descriptors; the final path component is opened with no-follow semantics where the host supports `O_NOFOLLOW`.
- FASTA hashing now enforces the byte ceiling while streaming, not only from the initial stat size. This prevents a file that grows after the preflight size check from causing unbounded hashing.
- Manifest reads remain capped at `max_manifest_bytes + 1` to detect overflow without loading an unbounded file.
- Added regression tests for manifest symlinks, oversized manifests and bounded FASTA hashing.
- Residual boundary: this protects local file ingestion on supported host filesystems; it does not establish a sandbox against privileged concurrent mutation, malicious kernel/filesystem behavior, or Android SAF document-provider semantics.


### S3 — Variant-to-structure coordinate mapping foundation
- Added `map_variant_to_structure`, which maps a protein substitution only when the structure chain has a unique, contiguous exact sequence match and the reference residue agrees with the query sequence.
- Ambiguous, gapped, missing or uncovered mappings abstain explicitly.
- The output records the query position, reference/alternate amino acids and corresponding structure residue number. It is coordinate correspondence only.
- No side-chain mutation modelling, stability/energy scoring, interface-effect prediction, pathogenicity or clinical interpretation is implemented.
- Apo-pocket analysis remains gated on complete atom chemistry and independent reference benchmarks. A bounded ligand-proximal site candidate screen is now available when the caller explicitly selects a ligand residue; it is contact evidence, not de novo pocket detection or an affinity predictor.


#### S3 interface-contact baseline
- Added bounded heavy-atom inter-chain contact counting with a spatial-neighbour index.
- Reports per-residue-pair atom-contact counts and minimum distances under a caller-selected cutoff.
- This is geometric contact evidence only; no interface energy, affinity, pocket, stability or functional effect is predicted. Pocket detection remains gated on ligand/solvent/chemical-component completeness and independent reference validation.


#### S5 deterministic offline session export foundation
- Added deterministic JSON export containing the validated structure-view payload and content-addressed preparation record.
- The export is byte-bounded and explicitly marks `render_state=not_rendered`; it does not pretend to contain PNG/SVG or viewer state.
- Image/session rendering and the structure benchmark matrix remain gated on a selected licensed renderer, fixed experimental reference structures, and device performance evidence.


#### S4 prediction evidence envelope and comparison boundary
- Added strict validation for externally supplied prediction envelopes, including sequence/model/node provenance, weights hash, license declaration, timezone-aware timestamp, structure payload and per-residue pLDDT consistency.
- Added exact-correspondence superposed CA RMSD comparison with source hashes.
- Validated envelopes remain `unverified_prediction`; no model execution, node authentication, confidence calibration, TM-score or predictive accuracy is claimed. Actual node/model execution remains gated.


#### S7 bounded contig QC foundation
- Added streaming contig summary statistics with N50/L50, total/longest/shortest lengths, canonical-base GC, ambiguous/N-base counts and short-contig counts.
- Enforced record/base budgets, unique identifiers and DNA IUPAC validation.
- This is assembly-summary QC only; gene/transcript annotation, contamination/completeness, eukaryotic splice models and functional annotation remain unimplemented pending reference datasets.


#### S8 explicit genetic-code table identifier hardening
- Translation and ORF scanning now reject boolean, floating-point and string table identifiers instead of allowing Python's bool/int equality to select a table implicitly.
- The supported NCBI tables remain explicitly caller-selected for translation. A separate bounded candidate-ranking helper now screens supplied coding sequences for internal in-frame stops and optional complete-CDS start/terminal-stop consistency across supported tables. It abstains on insufficient records/codons or a small score margin. It does not incorporate taxonomic context, codon usage, homolog alignment or transcript evidence, and is not calibrated or a validated organism-specific assignment.


#### S6/S9 — Bounded caller-supplied protein motif evidence
- Added `python/molecularis/protein_motifs.py` for deterministic fixed-width motif matching against a caller-supplied, SHA-256-pinned JSON motif pack.
- Motifs support canonical amino-acid literals and a single-residue `.` wildcard; arbitrary regular expressions are intentionally unsupported.
- Enforces pack-byte, motif-count, query-residue, comparison and hit budgets; rejects duplicate JSON keys, duplicate motif IDs and invalid alphabets.
- Reports exact 1-based match coordinates and motif-pack provenance. A match does not infer family/function; a no-match does not establish novelty.
- This is a reusable motif-evidence primitive, not a curated motif database, motif-discovery engine, profile-HMM, homology search or calibrated classifier.


#### S3/S9 — Bounded alignment-aware coordinate mapping
- Added a semi-global linear-gap alignment mapper for a complete observed structure chain against a query-sequence subsequence.
- Query terminal overhangs are free; internal gaps are scored. Only identical aligned residue pairs are mapped.
- Counts optimal traceback paths (capped at two) and abstains on tied placements/tracebacks rather than choosing an arbitrary coordinate mapping.
- Enforces sequence, atom, residue and dynamic-programming cell budgets, plus caller-selected identity and structure-coverage thresholds.
- This is coordinate correspondence only, not a calibrated homology/family classifier, mutation model or functional predictor. Insertion codes and alternate locations remain unsupported by the current atom model.


## Owner scope decision D-021 — 2026-11-10

The owner approved deferring external biological/experimental validation, licensed reference/model resources and secure inference infrastructure, and physical-device verification as explicit carry-forward deliverables. Capabilities without implementation, license or validation remain disabled and must not be presented as scientifically established.

This decision does **not** waive missing software implementation. Full prokaryotic/eukaryotic annotation, homology/profile-HMM and family/domain workflows, and prediction-engine integration remain open engineering work. S10 generation remains disabled. Continue S; I remains blocked until the implementable S scope is completed and audited. See [the S-track evidence audit](audit-2026-11-09.md).


## S6 software increment — local alignment primitive (2026-11-10)

A bounded Smith–Waterman local aligner is now available for caller-supplied reference records. It reports descriptive score, identity, query/reference coverage and 1-based local coordinates under explicit dynamic-programming cell ceilings. It does not compute E-values or statistical significance and must not be presented as a calibrated homology/family classifier. Curated licensed reference packs and independent validation remain required.


The verified local FASTA-pack workflow now exposes the bounded local aligner directly after hash-pinned pack ingestion. GFF3 import returns its validated feature records as well as summary counts, enabling downstream processing while preserving the annotation-import-versus-prediction distinction.


## S4/S7/S9 software increments (2026-11-10)

- **S4:** a dependency-injected local prediction-engine protocol now connects an approved local worker to the existing strict envelope validator. No engine or weights are bundled; model/license, runtime and calibration gates remain open.
- **S7:** supplied GFF3 annotations can now be reconstructed into strand-aware spliced CDS sequences and translated with an explicit genetic code. This is not de novo eukaryotic gene prediction.
- **S9:** HMMER hmmscan domain-table output can be parsed into bounded provenance-bearing candidate profile-match evidence. A local HMMER binary and approved profile packs are still needed for live searches.


## 2026-11-11 — S3/S8 software boundary update

S3 now includes bounded explicit-ligand contact-site candidates and a coarse apo concavity candidate screen using probe accessibility. S8 now includes bounded, abstention-first candidate ranking from supplied coding-frame and optional complete-CDS evidence, with duplicate-evidence rejection and input/table bounds. These are source-level research hypotheses only; neither is a validated biological classifier. Exact-head CI and the S1–S10 audit are required before the S engineering gate can close.
