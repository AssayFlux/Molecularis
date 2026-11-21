# Molecularis security and privacy threat model

**Status:** consolidated engineering threat model; not independently reviewed or certified.  
**Scope:** Android Research Mode, local import/storage/export, SQLite and WorkManager, Python/native runtimes, WebView, data packs, build supply chain and explicitly disabled optional remote boundaries.  
**Owner:** project owner must appoint a security role; see [Track G roles](track-g/roles-and-review-cadence.md).

## 1. Security objectives and invariants

- Preserve confidentiality and integrity of user-provided research files and derived outputs.
- Keep local workflows offline by default. User-initiated public-reference GET requests are enabled for allow-listed NCBI, UniProt and RCSB endpoints; no patient-data upload, telemetry or remote scientific processing is enabled.
- Treat user-selected files, SAF providers, data packs, metadata, URI values, parser inputs and all dependency artifacts as untrusted.
- Keep plaintext, keys, tokens and sensitive paths out of logs.
- Authenticate encrypted content; reject unknown versions and authentication failures without downgrade.
- Never load executable code or native libraries from data packs.
- Do not claim secure deletion on flash storage or deletion of copies previously exported.
- Keep patient/clinical data, human-subject workflows, individual clinical interpretation and Clinical Mode prohibited while P0 is NOT APPROVED.
- Treat a checksum as integrity evidence, not proof of publisher identity or redistribution rights.

## 2. Assets

| Asset ID | Asset | Confidentiality / integrity concern |
|---|---|---|
| A-01 | Imported sequence, structure, chemistry and other research files | Disclosure, tampering, malicious payload, loss |
| A-02 | Decrypted working buffers and temporary files | Residual plaintext after crash/cancel |
| A-03 | Keystore keys and encrypted chunks | Key compromise/loss, nonce/AAD misuse, rollback |
| A-04 | SQLite job, provenance and result metadata | Tampering, stale state, path/URI confusion |
| A-05 | Data-pack manifests and payloads | Substitution, malformed content, rollback, unlicensed redistribution |
| A-06 | Python, Rust, C++, Kotlin and WebView runtime | Memory safety, injection, parser abuse, bridge escalation |
| A-07 | Build inputs, toolchains, dependencies and artifacts | Supply-chain compromise, unreviewed licenses, provenance gaps |
| A-08 | CI credentials and future signing material | Repository/CI compromise and unauthorized release |
| A-09 | User-exported results | Unintended disclosure outside app-controlled storage |

## 3. Trust boundaries and attack surfaces

1. **SAF/document providers:** external content, MIME types, filenames, URI grants and provider behavior are untrusted and may change or be revoked.
2. **Import/parsing:** byte streams, metadata, formats, lengths, compression and parser state are attacker-controlled; enforce streaming and resource ceilings.
3. **Persistence:** WorkManager input, SQLite rows, encrypted file headers, chunk metadata, cache paths and migration state must be validated before filesystem access.
4. **Cryptographic boundary:** Android Keystore and AES-GCM protect app-private ciphertext; key invalidation, backup/restore and device compromise remain risks.
5. **Runtime boundary:** Python packages, Rust/C++ native code, WebView HTML/JS and bridge messages require constrained interfaces and bounded inputs.
6. **Data-pack boundary:** manifests and checksums can detect corruption but do not authenticate a publisher without a verified signature/trust root.
7. **Build/supply-chain boundary:** Gradle plugins, Maven artifacts, PyPI wheels, Cargo crates, NDK/CMake and downloaded tools are untrusted until pinned, hashed and reviewed.
8. **Export boundary:** SAF export intentionally sends user-selected content to an external provider/location; the app cannot control subsequent copies.
9. **Public-reference network boundary:** the Android manifest declares INTERNET for explicit public-reference retrieval. The current client permits HTTPS GET only to allow-listed NCBI, UniProt and RCSB hosts, rejects redirects and enforces timeouts/response caps. Only public search terms and accessions may cross this boundary; patient inputs, VCFs, sample identifiers and derived results must never be sent. Runtime traffic capture and merged-manifest verification remain open. Any additional provider or remote compute feature requires separate review.

## 4. Threat register

| Threat ID | Threat | Existing / intended control | Residual risk and verification |
|---|---|---|---|
| T-01 | Malformed or oversized import exhausts memory/CPU/storage | Streaming parsers, explicit byte/record caps, negative tests | Parser-specific fuzzing, CPU/memory profiling and device tests open |
| T-02 | URI traversal, provider substitution or revoked permission | SAF grants, UUID job IDs, canonical app-private path checks | Provider revocation, symlink/race and OEM provider tests open |
| T-03 | Ciphertext/chunk tampering or downgrade | AES-GCM authentication, job/chunk AAD, strict version checks | Key invalidation, nonce lifecycle and recovery tests open |
| T-04 | Process death/cancel leaves plaintext or inconsistent DB/files | WorkManager recovery and encrypted partial retention | Fault injection at every transition and orphan reconciliation open |
| T-05 | Data-pack substitution or rollback | Manifest checks, bounded copy, checksum, immutable installed versions | Publisher signature/trust-root policy and rollback tests open |
| T-06 | Sensitive content leaks through logs/errors | No-content logging rule and privacy requirements | Static scan plus runtime logcat review open |
| T-07 | WebView script/bridge injection | Offline assets, typed allow-list bridge and origin policy | Bridge fuzzing, CSP/origin tests and device review open |
| T-08 | Malicious dependency or compromised build input | Version pins, source inventory, CI and artifact hashes | Resolved transitive SBOM, artifact hashes/signatures and independent review incomplete |
| T-09 | Lost/stolen/rooted device exposes data | Keystore-backed encryption and app-private storage | Root/instrumentation/OS compromise, screenshot and lock behavior need device review |
| T-10 | Export sends confidential content to unintended destination | Explicit user-selected SAF action | Destination confirmation, partial-write and user disclosure tests open |
| T-11 | Backup/restore or key loss causes disclosure or irreversible loss | Source manifest sets allowBackup=false | Merged-manifest/OEM/Keystore invalidation tests open |
| T-12 | Unauthorized remote processing or data exfiltration | Explicit public-reference GET only; allow-listed HTTPS hosts, no redirects, bounded responses; private research inputs are not sent | Verify merged manifest, runtime traffic, DNS/redirect behavior and provider request contents; remote compute remains disabled |
| T-13 | Malicious intent/clipboard/overlay surface | Minimise exported components and sensitive clipboard use | Merged-manifest audit and interaction tests open |
| T-14 | Supply-chain license/security obligations missed | Candidate-only third-party register and source SPDX inventory | Exact resolved artifact and file-level review open |

## 5. Security control mapping

- **G1-01:** this document is the canonical cross-stack threat model. UI-specific cases are maintained in [the UI threat supplement](../governance/threat-model.md), not as a competing full threat model.
- **G1-02:** [security verification matrix](track-g/security-verification-matrix.md) records abuse cases, expected outcomes and evidence status.
- **G1-03:** [SECURITY.md](../SECURITY.md) defines current reporting guidance; operational response procedures are in [Track G operational controls](track-g/operational-controls.md). Private reporting route and triage ownership are not yet tested/assigned.
- **G1-04:** independent mobile/application security assessment and retest are mandatory before release.

## 6. Mandatory test scenarios

Test with synthetic/non-personal data only:
- malformed, oversized, truncated and adversarial parser inputs;
- URI revocation, path traversal, symlink/race and provider substitution;
- concurrent scheduling, cancellation, retry, process death and DB/file crash boundaries;
- Keystore invalidation, reinstall, restore and authentication failure;
- interrupted SAF export and destination-provider failure;
- WebView bridge wrong-origin, wrong-type, oversized and replayed messages;
- manifest permission/exported-component audit and runtime network capture;
- dependency substitution, stale artifact, data-pack rollback and checksum tampering.

Every result must record source commit, APK/AAB digest where applicable, test/tool version, device/API/ABI, input fixture digest, raw output, reviewer and limitations.

## 7. Explicit out-of-scope threats and limitations

Rooted or OS-compromised devices, malicious system providers, physical forensic extraction, coercion and compromise of the user's external export destination are not fully mitigated. Hardware-backed Keystore behavior varies by device. Secure deletion from flash storage cannot be guaranteed. These exclusions must be disclosed and reviewed rather than described as solved.

## 8. Independent assessment requirement

This is an engineering model, not an independent security assessment, penetration test, certification or risk acceptance. A qualified assessor must review the exact release artifact and source, report findings, verify remediation and document residual risk. No patient/clinical workflow may be enabled on the basis of this document.


## Public-reference network boundary update — 2026-11-18

The app now requests INTERNET permission for user-initiated public database retrieval. This is a deliberately limited network feature, not a general remote-compute channel. The current transport allow-list is NCBI E-utilities, UniProt REST and RCSB PDB file delivery. The client uses HTTPS GET, disables redirects and enforces response ceilings and timeouts. The UI discloses that imported patient data is never uploaded. The source-level control is not a substitute for merged-manifest inspection, runtime packet capture, provider endpoint verification or an independent security review. No patient or private research data may be included in provider requests.
