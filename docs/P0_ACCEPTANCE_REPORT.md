# P0 Platform Acceptance Report

**Report date:** 2026-11-26  
**Repository:** `AssayFlux/Molecularis`  
**Branch:** `CORE`  
**Status:** **NOT ACCEPTED — engineering controls partially implemented; deployment and institutional gates remain open.**

This report consolidates the P0 evidence and residuals. It is an engineering readiness record, not a security certification, legal opinion, scientific validation, or university approval. No restricted institutional data or model training is authorized by this report.

## Executive decision

P0 cannot honestly be marked complete yet. The repository now contains additional executable controls and regression tests for Galaxy egress authorization, Rulebook-to-OCI execution, one-use approval replay prevention, and one artifact-publication crash boundary. The remaining requirements include controls that can only be validated on the target university host or approved by the institution, as well as engineering work not yet implemented.

## Evidence-backed implementation status

| P0 area | Repository evidence | Status |
|---|---|---|
| Repository truth and Python dependency audit | SF0 audit; pip-audit in core and optional profiles; SPDX environment SBOM | Implemented for Python environments; native and legal review open |
| Cross-service typed handoff | `domain_integration.py`; sequence→protein and DNA/RNA→sequence fixtures | Representative contract tests exist; full real A–N workflow and scientific semantics remain open |
| Provenance continuity | ArtifactStore parent lineage; plan/input lineage; verifier/evidence references on handoffs | Partial; end-to-end replay/provenance acceptance open |
| Deterministic replay and cancellation | Rulebook run evidence, budget checks and failure records | Incomplete; no general replay engine, dependency invalidation or hard in-process cancellation |
| Threat model and classification | `docs/P0_PLATFORM_AUDIT.md`; `governance.py` | Baseline documented; institutional review and complete enforcement open |
| Egress enforcement | GalaxyClient requires explicit EgressPolicy, pins validated public DNS answers to TLS-verified connections; OCI tools run with network disabled | Partial; other process/network paths and host firewall enforcement open |
| OCI isolation | `OCIJSONHandler`; `MolecularisPlatform.bind_sandboxed()`; pinned image, network-none, read-only root, dropped caps, CPU/memory/PID/time limits and size-bounded output tmpfs | Adapter integrated with Rulebook API; real rootless runtime tests and image signature verification open |
| Approval and identity | Scope-bound approval payload; external verifier callback; SQLite atomic one-use ledger in ArtifactStore | Local replay prevention implemented; institutional identity, PKI, key custody and role authorization open |
| Backup and recovery | Verified backup/restore; corruption checks; injected post-blob/pre-catalog crash test | Partial; complete crash matrix, encrypted/signed off-host backups and witnessed restore drills open |
| Supply chain | Python pip-audit; SPDX 2.3 Python/native inventory metadata | Partial; OS/native vulnerability scans, binary hashes, publisher attestations and reviewed license report open |
| Data/model permissions | Governance metadata and source-permission contracts | Incomplete; source-specific legal/privacy/redistribution/training permission review required |
| Institutional acceptance | This report and operations runbook | Not signed; university security/privacy/system-owner review required |

## Exact CI evidence

The following GitHub Actions runs are tied to the exact commits shown:

- [Run #45866683899](https://github.com/AssayFlux/Molecularis/actions/runs/45866683899), commit `1c24557739844c9a0df23429850ce7864a7d5355`: Terminal Test Lab operation mapping and artifact-query correction; run passed.
- [Run #45867060800](https://github.com/AssayFlux/Molecularis/actions/runs/45867060800), commit `923c513130e3167ff3b60898577f1e4950552d53`: OCI Rulebook adapter and integration regression; core 840 passed/12 skipped, Chemistry 848/4, Genomics 841/11, Sequence 843/9 with 4 warnings; all jobs passed.
- [Run #45867255606](https://github.com/AssayFlux/Molecularis/actions/runs/45867255606), commit `b4f7a384be6c00a8b53a2d51768415ee6a24b07e`: atomic approval-consumption implementation and AI replay regression; all four jobs passed.
- [Run #45867647661](https://github.com/AssayFlux/Molecularis/actions/runs/45867647661), commit `739851f5964f551f5dc83f5edb2f9fa48edbf0fe`: crash-boundary fault-injection test; core 843 passed/12 skipped, Chemistry 851/4, Genomics 844/11, Sequence 846/9 with 4 warnings; all jobs passed.

A newer documentation-only HEAD may have a separate workflow pending. Do not treat a successful run on an earlier commit as proof that a later HEAD passed.

## Mandatory remaining closure work

### Engineering and deployment

1. Exercise OCIJSONHandler with rootless Docker and Podman on the target host; verify namespace, mount, UID/GID, seccomp/LSM and process-tree behavior.
2. Verify the size-bounded `/output` tmpfs hard limit on rootless Docker/Podman, including full-tmpfs behavior and bounded extraction to the host.
3. Pin and verify image publishers/signatures and approved digests before execution.
4. Map every outbound network path, verify the Galaxy DNS pinning behavior under adversarial DNS conditions, prevent remaining proxy/SDK bypasses and enforce an OS/network-level allowlist. Galaxy's client-level check alone is not sufficient.
5. Demonstrate multi-service execution with typed contracts, continuous provenance, deterministic replay, dependency invalidation, cancellation, timeout and injected failure evidence.
6. Expand crash injection across catalog transactions, WAL, object publication, backup publication, restore, disk-full and process/power-loss boundaries.
7. Add encrypted and signed off-host backup handling with institution-controlled keys, key rotation, restore verification and measured RPO/RTO.
8. Complete OS/native package and executable vulnerability scans, file/binary hashes, publisher provenance and a reviewed license/obligation report.
9. Verify data/model source terms, privacy restrictions, redistribution rights and explicit training permissions individually.

### Institutional decisions and signatures

The university/system owner must supply or approve:
- Identity provider and principal/role mapping.
- Cryptographic signing keys, custody, rotation, revocation and verifier implementation.
- Approved OCI runtime, image publisher/digest allowlist and host quota policy.
- Network egress gateway/firewall rules and DNS/proxy policy.
- Data classification owners and source-specific permissions.
- Backup encryption keys, retention, off-host destination, RPO/RTO and restore-drill witnesses.
- Security threat-model, privacy impact and incident-response review.
- Signed acceptance by authorized university security/privacy and system owners.

## Operating restrictions until acceptance

- Use synthetic or explicitly public data only.
- Keep restricted/confidential external transfers disabled.
- Do not run unreviewed or model-generated code in-process.
- Use only reviewed, digest-pinned OCI images with network disabled; deployment use still requires rootless-runtime verification and a hard output quota.
- Do not begin model training until data permissions, identity, isolation, provenance, rollback and institutional approval gates are accepted.
- Treat software CI as engineering evidence only, not scientific or institutional validation.

## Acceptance signatures

| Role | Name / organization | Decision | Date | Signature / reference |
|---|---|---|---|---|
| Platform engineering owner | Pending | Pending | Pending | Pending |
| University security owner | Pending | Pending | Pending | Pending |
| University privacy/data-protection owner | Pending | Pending | Pending | Pending |
| Scientific/domain reviewers | Pending | Pending | Pending | Pending |
| System/deployment owner | Pending | Pending | Pending | Pending |

**Final gate:** P0 remains **OPEN / NOT PASSED** until all mandatory engineering evidence is complete and authorized institutional owners sign the acceptance record.

- [Run #45868818928](https://github.com/AssayFlux/Molecularis/actions/runs/45868818928), exact tested code commit `d7e43682c1190e6b4adf534db367b6c0fd5f0308`: DNS-pinned Galaxy HTTPS transport and OCI tmpfs output/work mounts; core 845 passed/12 skipped, Chemistry 853/4, Genomics 846/11, Sequence 848/9 with 4 warnings; all four jobs passed. This includes unit tests for private/mixed DNS answer rejection, pinned-IP socket connection with original TLS hostname, OCI tmpfs quota command construction, bounded output extraction and container cleanup. Real network integration and rootless Docker/Podman execution remain deployment tests.
