# R4 — Genomics and sequence analysis

**Status:** In progress. Source implementation and Android CI build evidence are not independent scientific validation or device verification.

## Scope
- FASTA/FASTQ parsing, including a streaming FASTA iterator and wrapped FASTQ sequence and quality lines.
- Sequence statistics, reverse complement, transcription, k-mer counting and global pairwise alignment.
- FASTQ quality summaries and explicit-offset terminal quality trimming.
- SAM and VCF text parsing with mandatory-field and scalar validation; SAM validation also checks CIGAR query consumption and permits missing QUAL when SEQ is present.
- Reference-checked minimal/left normalization for literal biallelic A/C/G/T small variants. A separate `ReferenceSequence` contract binds synthetic reference sequence bytes to assembly/accession/release/contig, 1-based-closed coordinates, retrieval timestamp and SHA-256; normalized output retains that provenance.
- Bounded lazy BAM core-field decoder for gzip/BGZF-compatible BAM streams; optional host-side pysam/HTSlib adapter for BAM/CRAM with explicit local reference for CRAM.
- Android Explore integration: bounded FASTA QC (record length, GC fraction and ambiguous-symbol count) and bounded FASTQ read-quality summary (explicit Phred+33/Phred+64, read/base counts, mean Phred and Q20/Q30 fractions) through the embedded Python adapter. These are local analysis cards, not yet the full SAF-import → durable job → result/provenance/export workflow.

## Current source
- Domain workflows: `python/molecularis/sequence.py`, `python/molecularis/genomics.py`, `python/molecularis/workflows.py`.
- Android bridge: `android/app/src/main/python/molecularis_probe.py` and `android/app/src/main/java/org/assayflux/molecularis/SequenceQcRunner.kt`.
- Explore UI: `android/app/src/main/java/org/assayflux/molecularis/MolecularisUi.kt`.
- Regression tests: `tests/test_research_primitives.py`, `tests/test_genomics.py`, `tests/test_fasta_workflow.py`.
- Exact Android CI evidence for the FASTA/FASTQ cards: [run #2033](https://github.com/AssayFlux/Kinetics/actions/runs/42484179938), source `037befa8e9d22099e250dd22d3c4d772a6457034`.

## Limitations
- FASTQ Phred offset is explicit user input; no encoding inference is performed.
- Android text-card inputs are capped at 1,000,000 characters; the Python workflow also caps reads and aggregate bases. The current UI does not provide a large-file streaming FASTQ import path.
- No adapter detection/trimming, sliding-window trimming, paired-read rescue, variant calling or clinical interpretation is performed by these QC cards.
- FASTA text convenience function materializes its returned records; use the iterator API for large inputs.
- BAM decoder exposes core SAM-like fields only and currently materializes each compressed BAM record block (bounded to 64 MiB); auxiliary tags are skipped. CRAM remains unsupported in Android and requires a reviewed htslib/CRAM engine.
- Terminal trimming is not adapter trimming or sliding-window quality trimming.
- VCF parsing does not yet normalize/decompose records automatically. The separate normalizer handles only reference-checked biallelic literal A/C/G/T small variants; symbolic alleles, breakends, multi-allelic decomposition, phasing and variant interpretation remain unsupported. The build-pinned wrapper currently accepts only explicitly classified synthetic non-patient fixtures; authoritative reference-pack intake, full assembly validation and scientific concordance remain open.
- Global alignment is not a high-throughput mapper.
- No clinical variant interpretation.

## Exit evidence
Independent fixtures and cross-tool concordance; malformed/large-file tests; deterministic provenance; measured runtime/memory; offline Android integration and device evidence; license review. No capability is marked validated until its evidence record is committed.


### Imported FASTA QC execution path — 2026-11-09 (R Step 1)

The Explore FASTA text-card remains a bounded convenience path. A second path now connects an already imported, authenticated FASTA research job to a WorkManager worker and durable analysis-result record. The worker applies 1 MB input bounds, uses the registered `analyze_fasta` Python adapter, persists result JSON with the exact source import digest and tool parameters, and exposes the saved result on the Home/Work job card. FASTQ is not automatically dispatched: explicit Phred offset selection remains mandatory. An analysis-result JSON export includes the tool identity, parameters, exact source SHA-256, result and scope note, while excluding private URI/path metadata. The latest integration commit still requires exact-source CI and device verification.


### R Step 2 CI boundary — 2026-11-09
The imported FASTA analysis worker and result/export UI compiled into the ARM64 APK/AAB and passed Android JVM unit tests at commit `fc8b667` (CI #2093). The follow-on result-integrity/preview patch `2ea1027` is awaiting exact-source CI. The build confirms packaging and compilation, not successful on-device Chaquopy invocation or scientific reference validation of FASTA QC.


### Exact-source audit CI — 2026-11-09
Commit `2ea102719fc37354f18def85bb329a60a885ee2a`, CI run #2094, passed all five jobs. ARM64 APK/AAB, package alignment, artifact hash checks and Android JVM unit tests passed. The digest revalidation and bounded result/preview guards are present in this exact-source build. No emulator/physical-device execution or on-device Chaquopy FASTA workflow is established by this CI result.


### Latest exact-source audit — 2026-11-09
CI #2101 passed the Python sequence/genomics regression suite and Android ARM64 packaging/JVM tests. This confirms host tests and compilation of the imported FASTA analysis path. It does not prove Android Chaquopy execution, large-file streaming on device, FASTQ durable import-to-export, BAM/CRAM Android support, external aligner/variant concordance or device performance. Those remain open.
