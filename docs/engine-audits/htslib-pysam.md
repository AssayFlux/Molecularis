# HTSlib and pysam engine audit

**Audit date:** 2026-11-21  
**Decision:** retain the existing Molecularis adapter as an optional host-side capability; do not add pysam/HTSlib to the dependency-free core or Android runtime. The adapter is an integration seam, not yet a release-approved engine.

## Upstream revisions inspected

- [pysam](https://github.com/pysam-developers/pysam): default branch `master`, inspected commit `6261249228ed2a8e8afb73f3fe4e936c1485b941` (committed 2026-11-03). Repository metadata declares MIT; `pyproject.toml` requires Python >=3.9 and builds with setuptools and Cython >=3,<4.
- [HTSlib](https://github.com/samtools/htslib): default branch `develop`, inspected commit `768d1f1b6e6e27d48792bb71332562b319116e55` (2026-11-19). Repository metadata reports `NOASSERTION`; the checked-in LICENSE explains the actual split licensing below.

These are moving branch snapshots, not approved release pins. A product build must select compatible immutable pysam and embedded HTSlib revisions and record source archive hashes.

## What the stack provides

HTSlib is the native C library for SAM, BAM, CRAM, VCF and BCF access. It supplies compressed I/O, indexed/random access, iterators, reference-based CRAM decoding and multithreaded I/O. pysam wraps HTSlib with Python/Cython APIs and also exposes samtools/bcftools functionality. The current pysam README states that its distribution wraps HTSlib 1.25, samtools 1.25 and bcftools 1.25.

This is a strong fit for the gap between Molecularis' bounded text SAM/VCF utilities and production-scale alignment/variant-file access. It is not a read mapper or variant caller: BAM/CRAM records describe alignments produced elsewhere. Do not present a pileup or file parser as read mapping, variant calling, or clinical interpretation.

## Licensing and supply-chain gates

- pysam's repository metadata and `COPYING` declare MIT.
- HTSlib's root distribution is MIT/Expat, but files under `cram/` use a modified three-clause BSD licence with non-endorsement wording. Preserve the correct notices for every redistributed binary/source component.
- HTSlib uses the htscodecs git submodule. Its exact revision and licence must be included in the resolved dependency inventory.
- pysam's own README identifies bundled samtools and bcftools sources. Their notices and any additional bundled third-party components must be audited independently; pysam's MIT declaration does not relicense these components.
- HTSlib's build documentation lists zlib as required, bzip2 and lzma as default compression dependencies, and libcurl/libdeflate/libcrypto as optional features. Disabling bzip2 or lzma can make some CRAM files unreadable. Network protocol support may be compiled in through libcurl; Molecularis must keep remote retrieval disabled unless a separately reviewed feature explicitly enables it.
- The repository-level SPDX metadata is insufficient for a binary redistribution decision. Generate a resolved transitive SBOM and inspect wheel contents/notices before distribution.

## Molecularis integration inspected

Existing adapter: `python/molecularis/genomics_htslib.py`.

- Imports pysam lazily, so the base package remains dependency-free.
- Streams `SamRecord` values from BAM/CRAM rather than loading the entire file.
- Supports full sequential reads and indexed region reads; converts the adapter's 1-based inclusive region coordinates to pysam's 0-based half-open fetch coordinates.
- Requires an explicit local FASTA for CRAM and does not enable implicit remote reference lookup.
- Converts decoded numeric qualities to Sanger/Phred+33 text for the existing `SamRecord` contract.
- Does not expose auxiliary tags, read groups, template/mate fields, base modifications, per-record reference IDs, binning, mapping-quality semantics, CIGAR operations as structured data, or reference/header provenance. The current `SamRecord` type is intentionally much narrower than a lossless alignment record.
- The adapter checks path suffixes and local file existence but does not itself impose file-size, record-count, elapsed-time, reference-size, or decompression limits. These are required at the job/worker boundary for untrusted inputs.
- No matching `tests/test_genomics_htslib.py` file was found in the inspected CORE tree. Do not infer runtime correctness from the adapter's presence.

## Recommended Molecularis design

1. Keep pysam optional and host-side initially. Do not add it to `project.dependencies`, Android Chaquopy, or the mobile APK.
2. Introduce a Molecularis-owned lossless alignment-record contract before expanding output fields. Preserve SAM flags, reference/mate coordinates, template length, CIGAR operations, MAPQ including the SAM value 255, sequence, missing-vs-present qualities, auxiliary tags with types, read-group identifiers, and source header/reference dictionary. Keep the current `SamRecord` as a deliberately lossy convenience view.
3. Add deterministic tiny SAM/BAM/CRAM fixtures and indexed-region fixtures. Test empty files, missing/corrupt indexes, truncated BGZF, absent sequence/qualities, unmapped/secondary/supplementary/duplicate/QC-fail records, CIGAR edge cases, long CIGAR encoding, tags, coordinate boundaries, reference mismatch, CRAM local-reference behavior, and remote-URL rejection.
4. Differentially compare parsed records and region membership against pinned samtools/HTSlib command-line outputs. Include known expected values; parser agreement alone is not biological validation.
5. Apply resource limits before and during processing: input bytes, records, regions, reference bytes, decompressed bytes, worker wall time and memory. Run native parsing in an isolated worker for untrusted uploads.
6. Keep reference FASTA/build identity and checksums in provenance. CRAM decoding must fail closed if the declared local reference is missing or inconsistent; never silently fetch a remote reference.
7. Only after host correctness and dependency notices are complete, evaluate Android arm64/16 KB page-size compatibility, JNI/NDK packaging, binary size and device runtime. No Android support is inferred from upstream portability.

## Adoption verdict

**Accept as an optional host engine candidate, not as a product dependency.** The existing adapter is directionally correct and already enforces an important safety property (explicit local CRAM reference), but the record model is lossy, there is no matching adapter test module in the inspected tree, resource controls are external, and the full bundled native licence/dependency closure is not yet established.

No tests, builds, benchmarks, Android device runs, or biological validation were performed as part of this source audit.

## Upstream references

- https://github.com/pysam-developers/pysam/tree/6261249228ed2a8e8afb73f3fe4e936c1485b941
- https://github.com/pysam-developers/pysam/blob/master/README.rst
- https://github.com/pysam-developers/pysam/blob/master/pyproject.toml
- https://github.com/pysam-developers/pysam/blob/master/COPYING
- https://github.com/samtools/htslib/tree/768d1f1b6e6e27d48792bb71332562b319116e55
- https://github.com/samtools/htslib/blob/develop/LICENSE
- https://github.com/samtools/htslib/blob/develop/INSTALL
