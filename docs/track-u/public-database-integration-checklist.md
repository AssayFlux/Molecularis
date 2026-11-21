# Public database integration — engineering checklist

**Owner:** Molecularis engineering
**Branch policy:** commit directly to `main`
**Status date:** 2026-11-18
**Current baseline:** `e89c475a2ad2fe4c5451926f077d5d1a9bb434a9`
**Overall status:** INTEGRATION IN PROGRESS — source paths exist; exact-head CI and device acceptance are not yet closed.

This checklist is an execution register. “Implemented” means code is present, not that a user journey or release has passed. Close an item only with the evidence listed.

## 1. Provider discovery and retrieval

| Item | Status | Acceptance evidence |
|---|---|---|
| NCBI Gene search | IMPLEMENTED IN SOURCE | Search, metadata display and malformed-query tests |
| NCBI Gene → linked nucleotide/protein discovery | IMPLEMENTED IN SOURCE | ELink result tests and real-provider smoke test using public accessions |
| NCBI Nucleotide FASTA | IMPLEMENTED IN SOURCE | Retrieval, checksum and QC integration tests |
| NCBI Protein FASTA | IMPLEMENTED IN SOURCE | Retrieval, checksum and QC integration tests |
| UniProtKB search and FASTA | IMPLEMENTED IN SOURCE | Search/retrieval tests and provenance checks |
| RCSB PDB mmCIF by entry ID | IMPLEMENTED IN SOURCE | Retrieval, checksum and viewer handoff tests |
| ENA / Ensembl / UCSC / PDBj / AlphaFold DB | NOT STARTED | Adapter, terms/licence review, fixtures and integration tests |
| PubChem / ChEBI / CCD | NOT STARTED | Structure/chemistry adapter and source-specific licensing review |
| GEO / SRA | NOT STARTED | Metadata-only discovery design, download bounds and terms review |
| RCSB text/ligand/organism search | OPEN | Search endpoint, pagination and result-selection tests |

## 2. Retrieval reliability and privacy

| Item | Status | Acceptance evidence |
|---|---|---|
| HTTPS host allow-list, bounded responses and timeouts | IMPLEMENTED IN SOURCE | Unit tests for host, redirect, timeout and response ceilings |
| Search terms/accessions only sent to providers | IMPLEMENTED IN SOURCE | Network instrumentation confirms no patient sequence, VCF, sample ID or private job metadata |
| SHA-256 and retrieval timestamp | IMPLEMENTED IN SOURCE | Hash reproducibility and timestamp tests |
| Encrypted app-private source payload storage | IMPLEMENTED IN SOURCE | AES-GCM tamper, Keystore loss, path traversal and restart tests |
| SQLite metadata / analysis JSON encryption | OPEN | Threat model, migration, key-loss and query design; do not claim encrypted at rest today |
| Explicit cancel and retry/backoff | OPEN | Cancellation propagation, bounded retry and user-visible state tests |
| ETag / Last-Modified / source release capture | OPEN | Provider-specific metadata tests |
| Licence / terms / attribution metadata | OPEN | Source registry review and user-visible attribution |
| Cache quota, eviction and clear-all | OPEN | Storage pressure and deletion tests |
| Background WorkManager retrieval | OPEN | Process-death, network constraint, retry and cancellation tests |

## 3. Parsing and scientific models

| Format / capability | Status | Acceptance evidence |
|---|---|---|
| FASTA retrieval and existing bounded QC | IMPLEMENTED IN SOURCE | Multi-record, invalid alphabet, empty and oversized fixtures |
| FASTQ | EXISTING WORKFLOW; PUBLIC PROVIDER PATH OPEN | Phred+33/+64 fixtures and strict length checks |
| GenBank / EMBL | OPEN | Feature/coordinate preservation fixtures |
| GFF3 / BED | OPEN | Explicit 1-based-inclusive vs 0-based-half-open tests |
| VCF | SEPARATE AGGREGATE-QC PATH | Header/assembly/coordinate/record-limit tests; never transmit externally |
| PDB / mmCIF | EXISTING PARSER HANDOFF | Chain/model/alternate-location/missing-residue and large-file fixtures |
| SDF / MOL | EXISTING GRAPH PREVIEW | Valence, bond order, charge, stereochemistry and conformer tests |
| Canonical typed models and parser versioning | OPEN | Schema version, round-trip and backwards-compatibility tests |

## 4. Engine dispatch and user journeys

- [x] Public search/retrieval controls are surfaced on Home.
- [x] NCBI/UniProt FASTA results use the existing on-device FASTA QC path.
- [x] RCSB mmCIF retrieval hands off to the existing structure parser/viewer.
- [x] Saved source payloads can be listed and deleted; FASTA can be re-analysed and structures reopened.
- [ ] Add saved-record detail view with full provenance, analysis history and explicit retention controls.
- [ ] Add typed engine registry dispatch with schema validation, resource limits, cancellation and engine/version provenance.
- [ ] Add direct sequence operations (translation, reverse complement, ORF, alignment, annotation) only where a real registered engine exists.
- [ ] Add structure chain/model/assembly controls and scientifically labelled measurements.
- [ ] Add chemistry SMILES/InChI/PubChem lookup and graph/conformer workflow only after parser and licence gates.
- [ ] Keep predicted vs experimental structure labels explicit; never imply a sequence itself supplies an observed 3D structure.

## 5. Verification and release

- [ ] Exact-main Android JVM tests pass.
- [ ] Exact-main arm64 APK and AAB build passes.
- [ ] 16 KiB native alignment and package integrity checks pass.
- [ ] APK/AAB SHA-256 hashes and build provenance are recorded.
- [ ] Public provider contract tests pass without relying on live API availability.
- [ ] UI tests cover search, result selection, retrieval, errors, offline mode, saved records, deletion and viewer handoff.
- [ ] Physical ARM64 device tests cover memory, large mmCIF, app background/restore and Keystore failure.
- [ ] Accessibility, font scaling, RTL, keyboard and screen-reader checks pass.
- [ ] Documentation and completion audit match the exact tested commit.
- [ ] No patient data appears in CI fixtures, logs, public API requests or telemetry.

## 6. Execution order

1. **Stabilise build:** keep main green; fix compile/test/package failures before adding new feature surface.
2. **Close current provider journeys:** add regression tests around NCBI Gene ELink, FASTA QC, saved record lifecycle and mmCIF viewer handoff.
3. **Harden storage/retrieval:** metadata protection decision, cancel/retry, cache quota, source release/licence provenance.
4. **Complete parser/model layer:** FASTQ/GenBank/EMBL/GFF3/BED/PDBx/mmCIF/SDF/VCF contracts and fixtures.
5. **Engine registry integration:** schema-checked dispatch, resource ceilings, cancellation, provenance and deterministic fixtures.
6. **Expand providers:** one source at a time after terms/licence/rate-limit review.
7. **Release acceptance:** exact-head CI, artifact hashes, device and accessibility evidence.

## Definition of done

A provider integration is done only when a user can search, inspect, select, retrieve, verify, parse, process with a real registered engine, understand provenance/limitations, save or discard deliberately, reopen offline and delete the record. Failure, cancellation, oversized input, malformed data, offline operation and Keystore loss must be safe and visible. CI success is not scientific validation or clinical approval.
