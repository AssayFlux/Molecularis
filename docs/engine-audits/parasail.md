# Parasail upstream and integration audit

**Review date:** 2026-11-21  
**Target:** Molecularis `CORE`  
**Upstream:** https://github.com/jeffdaily/parasail  
**Reviewed release:** `v2.6.2`, commit `600fb26151ff19899ee39a214972dcf2b9b11ed7` (2023-03-10)  
**Disposition:** retain as an evaluation candidate; do not integrate or bundle before a fresh maintenance/security review and architecture-specific proof

## Licence

The exact release's `LICENSE.md` is a Battelle BSD-style grant. It permits source and binary redistribution subject to retention/reproduction of notices and disclaimer, but has additional conditions beyond ordinary BSD-3-Clause:

- The Battelle Memorial Institute/Battelle name cannot be used without express written consent.
- Redistributions and publications based on work using the software must include the specified 2016 Daily et al. Parasail citation.

These conditions must be carried into source distributions, binary notices, app legal screens/docs as applicable, and scientific publication guidance. Do not label this simply “BSD-3-Clause” or use Battelle's name as an endorsement. Audit the complete pinned source distribution and contributed SIMD/SSW/SIMDe components for their own notices before redistribution.

## Technical findings from v2.6.2 source and README

- C99 SIMD library implementing Smith–Waterman local, Needleman–Wunsch global and configurable semi-global pairwise alignment.
- Algorithm families include diagonal, blocked, striped and prefix-scan approaches.
- Result variants trade performance for richer output: score/end locations; alignment statistics; or traceback suitable for SAM CIGAR retrieval.
- SIMD instruction families documented include SSE2, SSE4.1, AVX2, AltiVec and NEON. Runtime CPU dispatch chooses an available implementation when built/configured correctly.
- Upstream describes no required external dependencies and documents CMake, autotools and ARM cross-compilation.
- CMake probes compiler/CPU capabilities and has optional OpenMP. Android builds must explicitly control target architecture and compiler flags; never compile host x86 instructions into an arm64 artifact.
- The README states there is no automated test suite at this release; `make check` builds additional test programs such as ISA reporting. This is a material validation gap for adopting it as a scientific engine.
- The release tag is from March 2023. This audit did not establish a current maintenance/security cadence or whether newer branches/releases contain fixes; a 2023 tag must not be adopted without a fresh upstream activity and vulnerability review.

## Molecularis fit

- The current `needleman_wunsch` implementation in `python/molecularis/sequence.py` is a bounded, dependency-free, full-matrix global aligner with a single linear gap penalty and deterministic single traceback. It is valuable as a transparent reference implementation for small sequences, not a high-throughput engine.
- Biopython PairwiseAligner is already used as a host/Android feasibility reference and supports richer scoring modes, but is not itself a high-throughput read mapper.
- `docs/phase-r1-plan.md` requires a real scientific sequence engine to be built and tested; it explicitly says the Biopython smoke test alone does not complete that criterion.
- Parasail could fill the SIMD pairwise alignment engine role. It does not provide indexed reference mapping, seed chaining, read mapping, variant calling, or BAM/CRAM infrastructure.

## Integration risks and required contract

1. **Scoring semantics:** Parasail documents that gap-open penalty alone is applied when opening a gap; gap-extension applies to subsequent extension. Ensure Molecularis's adapter exposes the same convention and maps the selected semi-global end-gap policy exactly.
2. **Integer lane saturation:** SIMD implementations commonly have 8/16/32/64-bit score lanes and saturation detection. Use a checked dispatcher or conservative width selection; never silently accept a saturated score. Validate long sequences, extreme scoring matrices and gap penalties against an independent 64-bit/reference implementation.
3. **Alphabet/matrix:** validate sequence alphabet and substitution-matrix dimensions/symbol mapping before calling native functions. Explicitly define ambiguity symbols, wildcard handling, protein matrices, case normalization and strand behavior.
4. **Traceback:** score-only routines are not interchangeable with traceback routines. CIGAR conversion must be checked for orientation, soft clips, terminal gaps and coordinate conventions before using in SAM/BAM output.
5. **Memory and limits:** bound sequence lengths, result/traceback allocation, batch size, thread count and CPU time. Treat native errors/null results and cancellation explicitly.
6. **Runtime dispatch:** verify the exact NEON/ARM64 path on real target hardware. A successful host x86 build or ARM cross-compile is not runtime evidence.
7. **Android integration:** build an arm64-v8a shared/static library with NDK and the required 16 KB page-size alignment, inspect every packaged ELF, test JNI invocation and compare results on physical devices. Cross-compilation alone is insufficient.
8. **Licensing and provenance:** pin immutable commit, hash source archive, retain exact license and third-party notices, add citation requirements to output provenance and publications, and track security updates.

## Recommended evaluation plan

- First establish the exact current upstream status and review any release newer than v2.6.2 before selecting a pin.
- Build a host-only adapter proof with one explicit algorithm/scoring contract and no implicit defaults.
- Create a differential corpus comparing Parasail with Biopython PairwiseAligner and Molecularis Needleman–Wunsch for supported common cases: global/local/semi-global, linear/affine gaps, terminal gap variants, nucleotide/protein matrices, ambiguity handling, tie scores, empty/short/long inputs, and traceback/CIGAR.
- Add score-width/saturation tests and test all available 64-bit or non-SIMD fallback paths against arbitrary-precision/reference DP.
- Benchmark only after correctness gates pass; measure throughput, latency, memory, CPU architecture and thread count on representative sequence lengths. No performance claim is made in this audit.
- Then cross-compile arm64 Android, inspect ELF/16 KB alignment and notices, and execute JNI/runtime tests on emulator and physical ARM64 hardware.

## Decision

**Parasail is the best candidate in this set for a dedicated SIMD pairwise-alignment engine, but it is not yet accepted.** Keep Molecularis's transparent Needleman–Wunsch implementation for small reference fixtures and Biopython PairwiseAligner as a mature comparison implementation. Evaluate Parasail behind a Molecularis-owned adapter only after source freshness, licensing, score-saturation, differential correctness and Android ABI/runtime gates pass.

This is a source audit, not an integration or benchmark. No Parasail binary was built or run in this review, and no performance, Android compatibility or scientific validation claim is made.
