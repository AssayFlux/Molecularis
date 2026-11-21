# U3 — Scientific workflows and result presentation

**Disposition:** PARTIAL — two real sequence workflows are now reachable from persisted Work jobs; the broader workflow inventory and acceptance remain OPEN.
**Scope:** Research Mode only. A successful parser/QC run is not independent scientific validation and is not clinical interpretation.

## Existing integrated workflow retained

- SAF imports are staged and stored using the existing encrypted, hash-verified import path.
- WorkManager owns long-running import and analysis execution.
- FASTA QC operates only on a completed import whose stored bytes are authenticated and whose SHA-256 is recorded.
- FASTA result JSON is stored against the exact input digest with tool ID, tool version, parameters and creation timestamp.
- Import provenance and analysis exports omit source URI and private storage paths.
- Work cards retain cancel/resume/delete/export actions and distinguish failure/recovery states.

## Added in this work package

### FASTQ quality summary

- A new ImportedFastqAnalysisWorker accepts FASTQ/FQ inputs and gzip-compressed .fastq.gz/.fq.gz inputs from completed, hash-verified imports.
- Input is bounded to 1,000,000 bytes and 1,000,000 decoded characters before Python analysis.
- Phred offset is required as an explicit WorkManager input and restricted to 33 or 64. It is never guessed.
- The Work UI asks the user to choose Phred+33 or Phred+64 before queuing the analysis.
- The worker calls the existing molecularis_probe.analyze_fastq Python adapter and verifies that the returned result records the selected offset and at least one read.
- The persisted result records sequence.fastq.quality_summary, version 1, the imported SHA-256 binding and explicit offset/size parameters.
- Worker guard tests cover missing/malformed job IDs, invalid Phred offsets, missing jobs, wrong input type, oversized input without materializing plaintext, and preservation of the queued/import state when analysis preflight fails. FASTA and FASTQ analysis failures now update the explanatory message without rewriting the import job's durable state.

### Result detail

- Saved analysis records now expose method ID, method version, parameters and saved timestamp in the Work job model.
- The result panel presents record count, total bases, selected Phred offset, mean quality, Q20/Q30 fractions, a bounded first-five record preview and method limitations where present.
- The complete result remains available through the explicit SAF JSON export action.
- The UI labels the displayed values as a bounded research QC result and surfaces method limitations; it does not infer biological function or clinical meaning.

## Current limitations

- Analysis result JSON and method parameters are stored in app-private SQLite in plaintext; U2 discloses this limitation. No encryption-at-rest claim is made for this table.
- The result panel currently supports the persisted FASTA/FASTQ summary structures. Other registry tools are not automatically exposed as runnable.
- Progress granularity for the bounded analysis workers is not yet streamed into the UI; WorkManager lifecycle and terminal success/failure remain the source of truth.
- Retry/resume policy for analysis work is not yet a dedicated user-facing workflow.
- Full result/provenance cross-linking, result schema validation, process-death tests, export round trips and every failure/partial state remain to be verified.
- FASTQ parsing/quality summaries do not perform adapter detection, trimming, paired-read rescue, variant interpretation or clinical interpretation.

## Required closure evidence

1. Exact-main Android arm64 APK/AAB build and JVM tests including both worker suites.
2. Valid and invalid FASTQ fixture tests through the embedded Android Python runtime for both supported offsets.
3. Result persistence and digest mismatch tests for FASTQ as well as FASTA.
4. Process-death/restart and WorkManager retry/cancel tests.
5. SAF result/provenance export round-trip tests, including provider partial-write failures.
6. Registry/dispatcher parity audit for every visible runnable control.
7. UI screenshot, accessibility and physical-device review for the result panel and Phred selection dialog.

**Decision:** U3 remains PARTIAL. The new FASTQ workflow is a concrete integration, not a claim that every scientific engine has a complete mobile UI.


## Import lifecycle correction — 2026-11-18

The import worker now atomically claims and finalizes the durable job state. Cancellation is committed before WorkManager cancellation, and finalization refuses a job no longer marked running. Resume transitions are explicit; WorkManager process recreation may reclaim a running job and continue from its authenticated encrypted partial. Automated store and worker regression tests were added. Exact-head CI and forced process-death/device testing remain outstanding.


### Gzip-compressed sequence inputs — 2026-11-18

- The encrypted-import FASTA/FASTQ workers now detect gzip by filename suffix and decompress on-device.
- Expanded content remains bounded to 1,000,000 bytes and 1,000,000 decoded characters before parsing; malformed UTF-8 and NUL bytes are rejected.
- Provenance records the compression handling mode and expanded-size limit. Automated CI continues to use synthetic sequence fixtures only.


## Public reference sequence retrieval — 2026-11-18

- Home exposes NCBI Nucleotide, NCBI Protein and UniProtKB search; NCBI Gene search exposes linked nucleotide/protein discovery through ELink; the linked records then use the FASTA retrieval path.
- Selected NCBI nucleotide/protein or UniProtKB records are fetched directly as FASTA inside the app.
- Retrieved payload bytes are SHA-256 checked and stored as Android Keystore AES-GCM chunked files in app-private no-backup storage. The SQLite record index stores source, accession, format, endpoint, retrieval time, byte count and digest; the index and result JSON are not encrypted at rest.
- Retrieved FASTA is dispatched to the existing embedded Python `molecularis_probe.analyze_fasta` adapter and the bounded local FASTA QC result is retained with the record.
- Saved public records are listed and deletable from Home. A full saved-record detail/browser screen, WorkManager background execution, explicit cancel/retry, cache quotas, source release/licence fields and NCBI Gene-to-RefSeq linking remain open.
- This is sequence QC integration, not full sequence annotation/alignment/ORF/translation integration. Exact-head CI and Android device verification remain required.


### Saved public FASTA record reuse — 2026-11-18

- Public FASTA records are reopened from the encrypted KDAT cache using authenticated decryption and SHA-256 verification.
- The existing local FASTA QC adapter can be run again against the saved record; the latest JSON result is updated in the public-record index.
- Public records larger than the current FASTA QC ceiling may still be retained, but QC can fail with an explicit limit message. Retrieval/storage success is not misreported as QC success.
