# Biopython upstream and integration audit

**Review date:** 2026-11-21  
**Target:** Molecularis `CORE`  
**Upstream:** https://github.com/biopython/biopython  
**Reviewed upstream commit:** `3c32ad9b14d1d52a468d072c1288376f60071d19` (2026-11-16)  
**Disposition:** retain as an isolated prototype/reference engine; complete runtime, file-level licence and scientific contract gates before product adoption

## Licence and packaging

Biopython's `LICENSE` is not a blanket BSD-3-Clause grant. It contains the Biopython License Agreement and a BSD-3-Clause text, and says some files are explicitly dual licensed at the file level. The reviewed `pyproject.toml` identifies the project licence as `LicenseRef-Biopython-License-Agreement`, includes `LICENSE.rst`, and requires NumPy. Before redistribution, audit the exact source files and compiled extensions included in the Molecularis wheel against their headers and licence declarations. Preserve the complete applicable notice text. Do not infer that every module is BSD-3-Clause simply because the BSD text is present in the root licence file.

The current upstream package metadata requires Python `>=3.10`, depends on NumPy, and builds a number of C extension modules. Upstream README reports support/testing across CPython 3.10–3.14 and PyPy 3.10. This is compatible with Molecularis's Python floor at the interpreter level, but not a reason to add Biopython to the base dependency set: Molecularis deliberately has no mandatory runtime dependencies, and its Android custom wheel is a separate ABI/build artifact.

## Useful upstream capabilities inspected

- `Bio.SeqIO` FASTA and FASTQ parsers/writers, including a mature format registry.
- FASTQ support distinguishes Sanger PHRED+33, old Solexa+64 and Illumina PHRED+64; these are not interchangeable encodings.
- `Bio.Align.PairwiseAligner` supports configurable pairwise alignment and compiled alignment core modules.
- `Bio.PDB.PDBParser` and `Bio.PDB.MMCIFParser` provide richer structural parsing than a simple atom-site loop.
- The mmCIF parser exposes author-vs-label chain and residue numbering choices. Its default parser can be permissive; permissive mode may catch construction exceptions and omit problematic atoms/residues. A strict parser mode and explicit warning/error capture are necessary when omissions would alter scientific results.

## Molecularis integration found

- The dependency-free API lives in `python/molecularis/sequence.py`; it provides streaming FASTA/FASTQ record iterators, IUPAC reverse complement/transcription, k-mer counts, basic statistics and a small linear-gap Needleman–Wunsch implementation.
- The local Needleman–Wunsch implementation is a simple educational/reference implementation: it allocates full score and traceback matrices and is bounded by `max_cells`; it supports one linear gap penalty and returns one deterministic optimal traceback. It is not a high-throughput mapper or affine-gap aligner.
- `python/molecularis/genomics.py` handles SAM/VCF text and FASTQ quality utilities. The Molecularis FASTQ parser currently assumes printable Sanger-style quality characters during parsing; trimming accepts an explicit PHRED offset of 33 or 64. The file format/encoding must therefore be selected explicitly by the caller; do not infer encoding from characters.
- `android/app/src/main/python/molecularis_probe.py` imports Biopython `SeqIO`, `Bio.PDB.PDBParser` and `Bio.Align.PairwiseAligner` in the R1 feasibility probe. Its fixed global alignment vector (ACGT vs ACCT; match 2, mismatch -1, gap open -5, extension -1) expects score 5.0.
- `docs/third-party.md` records Biopython 1.88 and NumPy 1.26.2 in an isolated Android Python 3.11/arm64 prototype. The custom wheel was historically built and packaged, but on-device imports/runtime, current 16 KB runtime behavior, complete wheel notices and file-level licensing remain open.
- `docs/scientific-engine-decisions.md` explicitly labels PairwiseAligner a prototype/reference candidate, not a high-throughput mapper.

## Findings and risks

1. **Do not replace Molecularis's public sequence records with SeqRecord.** Keep Molecularis-owned stable contracts and translate at the adapter boundary. This avoids coupling the API to optional dependency versions and BioPython's mutable metadata semantics.
2. **FASTQ semantics need explicit format metadata.** Sanger PHRED+33, Illumina PHRED+64 and legacy Solexa+64 require different decoders. The raw quality string and declared encoding should be retained in provenance; a wrong offset can produce plausible but materially wrong quality scores.
3. **Parser permissiveness must not hide data loss.** For PDB/mmCIF, use strict construction where appropriate, capture warnings and compare parsed atom/residue counts. Never silently accept a permissive parser result as complete.
4. **Author and label numbering are not interchangeable.** Preserve both chain/residue namespaces, insertion codes and model identity in a canonical Molecularis structure contract before mapping.
5. **Pairwise alignment is not read mapping.** PairwiseAligner is suitable for reference alignments and algorithm comparisons, not a substitute for BWA/minimap2-class indexed mapping or BAM/CRAM processing.
6. **Algorithm settings are part of the result.** Persist global/local/semi-global mode, substitution matrix, gap-open/extension penalties, end-gap policy, strand policy, ambiguity handling, algorithm and exact engine version.
7. **Android wheel success is not runtime proof.** A packaged custom wheel does not establish import success, numerical correctness, memory behavior, ABI compatibility on target devices, offline behavior or complete notices.
8. **No clinical or biological interpretation follows from parser/alignment execution.** Exact match, alignment score, percent identity and a parser's chosen atom mapping must not be elevated into homology, pathogenicity or functional claims without separately validated methods.

## Recommended work

- Keep Biopython optional and isolated; do not add it to base `pyproject.toml` dependencies.
- Finish the exact Biopython 1.88 + NumPy Android wheel file-level licence and transitive notice review; regenerate a resolved SBOM with artifact hashes. Keep this separate from the newer upstream main branch.
- Run the existing R1 import/SeqIO/PDB/PairwiseAligner probe on emulator and physical arm64 device and record exact artifact, OS/API, page size, RSS/startup and logs. Current docs correctly mark this as not yet done.
- Add differential fixtures for FASTA headers/blank/comment lines, wrapped FASTQ, all three FASTQ encodings, max/min quality boundaries, ambiguous bases, empty records, malformed separators and large streaming files.
- Compare Molecularis and Biopython alignments using independently specified global/local/semi-global vectors, affine and linear gaps, terminal-gap settings, ties, empty/ambiguous sequences, nucleotide/protein matrices and long sequences. Compare score and alignment properties, not only a single expected traceback where multiple optima exist.
- For PDB/mmCIF, compare strict parser output against pinned reference structures covering multiple models, insertion codes, alternate locations, auth/label chain and residue IDs, waters, ligands and missing values. Assert no silent atom loss.
- Preserve a dependency-free Molecularis fallback and expose engine choice/version in provenance.

## Decision

**Biopython is the preferred mature Python reference/parser layer for SequenceIO, PDB/mmCIF and pairwise-alignment comparison, but remains a prototype rather than a production-approved dependency.** Continue with explicit adapters and reference fixtures. Do not add it to the base package, assume file-level BSD licensing, or claim Android runtime support from packaging evidence alone.

This is a source/documentation audit. It does not claim that the Android runtime probe, tests, device runs or benchmarks were executed during this review.
