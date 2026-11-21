# Molecularis — engineering evidence brief for ethics committee review

**Prepared:** 18 November 2026  
**Repository:** AssayFlux/Molecularis  
**Branch:** main  
**Review baseline:** ad0b1d7b0f0594489cf4623b74df022d80619659  
**Purpose:** explain the current research-software engineering boundary and support a transparent demonstration. This document is not an ethics approval, protocol, clinical validation or data-use authorization.

## 1. What the application is

Molecularis is an offline-first Android/Python research application. Its current native shell has four destinations: Home, Work, Explore and Settings. It is designed to support bounded, traceable research workflows and local inspection of scientific files. Research Mode only is in scope.

## 2. Demonstrable engineering surfaces

| Surface | Demonstration | Output / boundary |
|---|---|---|
| Work / import | Select a local FASTA or FASTQ document through Android's document picker | Local job lifecycle and import provenance; inputs are staged using app-managed encrypted storage |
| FASTA QC | Run the existing bounded FASTA analysis workflow | Sequence-level quality summary; not clinical interpretation |
| FASTQ QC | Select Phred+33 or Phred+64 explicitly, then run QC | Read/base quality metrics; encoding is never guessed |
| Structure viewer | Import a local PDB/ENT/CIF/mmCIF structure | Offline 2D atom/chain inspection; bounded JSON, PNG and SVG exports; not a validated 3D molecular viewer |
| Chemistry graph | Import local SDF/MOL | Explicit-atom formula/mass and graph counts; not RDKit sanitization, stereochemical interpretation or drug-likeness |
| VCF aggregate QC | Use only a synthetic or appropriately authorized public non-patient VCF; operator attestation is required | Basic VCF record-structure and aggregate counts plus source SHA-256; sample identifiers and genotype strings are not returned; not a full VCF specification validator; no reference concordance or variant interpretation |
| Settings | Demonstrate appearance selection, diagnostics and optional local biometric/device-credential lock | Device-local controls; not remote account authentication |

Only use synthetic or authorized public non-patient fixtures in a committee demonstration. Do not load patient, identifiable, clinical or human-subject data into the demo build.

## 3. Data handling and security facts

- Imported sequence/file inputs are encrypted in chunks using AES-256-GCM and stored in app-private no-backup storage.
- The Android app uses a local SQLite store for job/import/provenance metadata. This metadata is not separately encrypted.
- Analysis result JSON and parameters currently reside in app-private SQLite and are not separately encrypted.
- App preferences use private SharedPreferences and are not separately encrypted.
- Temporary plaintext analysis inputs are held in app-private cache and cleaned on normal completion; stale prefixed cache files older than 24 hours are cleaned at store startup.
- Optional local biometric/device-credential re-authentication is implemented. Physical-device lifecycle, lockout and recovery acceptance remains open.
- Job deletion requests cancellation of associated WorkManager analysis work and removes app-managed records/files where operations succeed. Flash-storage secure erasure and deletion of previously exported copies cannot be guaranteed.
- User-selected SAF exports leave Molecularis' storage boundary; Molecularis cannot guarantee deletion or access controls imposed by the destination provider.
- Screenshot/Recents suppression is not enabled pending owner-approved threat/privacy review.
- Runtime network, merged-manifest and backup/restore audits remain in the engineering acceptance register; do not claim a completed independent security certification.

## 4. Explicitly unavailable capabilities

- No patient-facing or clinical mode, diagnosis, treatment, dosing or clinical decision support.
- No PGx star-allele, diplotype, phenotype or guideline recommendation workflow in Android.
- No validated variant pathogenicity interpretation or reference-build concordance in the VCF QC screen.
- Docking/OpenMM/ADMET are not Android-runnable capabilities in this build. Their host-side adapters and smoke tests are not proof of scientific validity.
- No remote compute node, cloud identity, patient data upload or telemetry feature is claimed by this evidence brief.
- A local aggregate VCF QC result is not a clinical report and does not establish the origin or authorization of the input file. The checkbox is an operator attestation only.

## 5. Suggested live demonstration sequence

1. Start on Home and show the actual empty/recent-work state (do not create fake jobs).
2. Open Work, import a small synthetic FASTA, run QC and show the persisted job/result/provenance.
3. Import a synthetic FASTQ and explicitly choose the known fixture Phred offset before running QC.
4. Open Explore and import a small public example PDB/mmCIF file; demonstrate local viewing and a bounded export.
5. Import a small synthetic SDF/MOL fixture and explain the explicit-atom graph-only limits.
6. Open aggregate VCF QC, select a tiny synthetic VCF, tick the non-patient attestation and show only aggregate results.
7. Finish on Settings and show the local-data inventory and local-lock setting.

Keep fixtures small and have them available offline before the meeting. Avoid connecting the demo to live patient systems or personal data sources.

## 6. Questions the committee should decide separately

- What exact protocol, research question, population and data sources are proposed?
- Which data categories are permitted, and what lawful/ethical basis and access controls apply?
- Are public datasets genuinely authorized for the proposed use, and are their licences compatible?
- What retention, export, deletion, backup and incident-response policies are required?
- Who is accountable for data access, security operations and adverse-event/incident escalation?
- What additional independent scientific validation is required before any result is used in a publication or downstream decision?

## 7. Verification status

- Android arm64 APK/AAB build and JVM tests passed on commit 841aebd64605a167797fb42e8d49e2fa66557be5 (workflow #44216522668). This evidence is historical relative to the review baseline above.
- Python CI on commit 3300b97c84114cb3ba6eb31fa7655247956430e6 reported 538 passed, 2 failed and 9 skipped. The two failures were test-fixture escaping defects and have been corrected in ad0b1d7b0f0594489cf4623b74df022d80619659; exact-head CI is pending.
- Physical-device accessibility/performance, independent security review and scientific validation remain separate acceptance activities.

**Committee-facing statement:** Molecularis currently demonstrates bounded research-software engineering, not an ethics-approved human-subject study or a clinically validated system. The committee's review should determine the proposed study and governance conditions; software capability must not be represented as approval.