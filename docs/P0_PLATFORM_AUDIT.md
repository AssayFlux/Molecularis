# P0 Platform Trust, Safety and Reliability Audit

**Snapshot:** 2026-11-23, branch `CORE`  
**Scope:** repository inventory, dependency declarations, current execution/data trust boundaries, recovery baseline and P0 residual risk.  
**Status:** baseline audit extended with scope-bound signed approval contracts; P0 remains **not passed** pending external identity, OS isolation, enforceable egress, resolved SBOM, institutional review and recovery operations. This document records repository evidence and actionable limits, not a security certification.

## Executive result

Molecularis is a Python-first, local scientific-computing reference platform with fourteen registered service verticals (A–N), a shared SQLite-WAL/content-addressed artifact store, a capability registry and an in-process Rulebook executor. The repository snapshot contains 445 tracked blobs, including source, tests, schemas, service documentation and CI configuration.

The current system is suitable for controlled engineering development with trusted, reviewed handlers and synthetic/public test fixtures. It is **not** an isolated multi-tenant execution environment, a production clinical platform, or a certified recovery/security system. Do not run untrusted generated code, arbitrary third-party tools, or restricted institutional data through it until the remaining P0 controls are implemented and independently reviewed.

## 1. Repository and service inventory

The A–N service set is:

| Key | Service | Primary concern |
|---|---|---|
| A | Molecular | molecular graphs, representation and validation |
| B | Sequence | sequence parsing, alignment and reference evidence |
| C | Structure | structural representation, geometry and quality |
| D | Chemistry | chemical graphs, properties and operations |
| E | Protein | protein sequence, motifs and model adapters |
| F | Genomics | reads, variants, annotation and genome QC |
| G | DNA/RNA | nucleic-acid sequence and structure operations |
| H | Simulation | molecular/physical simulation adapters |
| I | Kinetics | reaction networks and kinetic models |
| J | Omics | expression/matrix and multi-omics analysis |
| K | Phylogeny | alignments, trees and evolutionary inference |
| L | Pharmacogenomics | genotype/variant interpretation and PGx evidence |
| M | Cohorts | cohort aggregation and population analysis |
| N | Workflows | DAG validation, orchestration and artifact lineage |

Shared implementation entry points observed:

- `python/molecularis/platform/contracts.py`: budgets, capability, execution context and error contracts.
- `python/molecularis/platform/store.py`: SHA-256 object store, SQLite catalog, lineage, run evidence, audit and (in this P0 change) backup/restore.
- `python/molecularis/platform/runtime.py`: capability registry and in-process Rulebook DAG executor.
- `python/molecularis/platform/service.py`: local platform lifecycle and manifest loading.
- `python/molecularis/bootstrap.py`: A–N service registration.
- `python/molecularis/ai.py`: model-agnostic workflow planning and explicit approval gate.
- `tests/test_platform_*.py`, `tests/test_molecularis_ai.py`: focused platform and Agentics tests.

The repository also contains service-specific Python modules, JSON Schemas, service Rulebooks, benchmark smoke programs and optional adapters. The inventory does not imply every external executable/model is installed or active.

## 2. Dependency baseline

The root `pyproject.toml` declares Python `>=3.10`, no mandatory runtime dependencies, and setuptools `>=68` as the build requirement. CI currently exercises Python 3.11.

Declared optional scientific profiles:

| Profile | Declared packages | Scope |
|---|---|---|
| docking | `vina==1.2.7` | docking adapter |
| md | `openmm==8.6.1` | molecular dynamics |
| sequence | `biopython>=1.83,<2`, `biotite>=1.0,<2`, `parasail>=1.3.4,<2` | sequence/structure primitives |
| genomics | `pysam>=0.22,<1` | genomics/HTS |
| chemistry | `rdkit>=2023.9` | chemistry |

Development declarations include jsonschema, mypy, pytest, PyYAML, Ruff, types-PyYAML and tomli; `requirements-dev.txt` additionally declares pre-commit. These are declared ranges, not a report of the exact packages installed in a particular deployment.

`scripts/generate_source_sbom.py` produces a declared-dependency SPDX inventory. New `scripts/generate_environment_sbom.py` records installed Python distributions and observed `Requires-Dist` edges as SPDX 2.3; CI publishes it as the `molecularis-python-environment-sbom` artifact. This is a resolved Python-environment inventory, not a complete OS/native binary SBOM: package hashes, publisher attestations, file-level licenses, license-policy review and vulnerability scanning remain open. Do not infer that a dependency is installed merely because it appears in an optional extra.

## 3. Data and execution flow

1. Inputs enter through callers/service APIs or explicit artifact ingestion.
2. The artifact store writes content-addressed blobs and catalog metadata/lineage.
3. The capability registry exposes declared operations and schema identifiers.
4. Rulebooks are checked for registered capabilities, dependency cycles and step bounds.
5. Reviewed Python handlers execute in the same process as the runtime.
6. Operation outputs are serialized as JSON artifacts; run evidence records success/failure and artifact IDs.
7. Agentics may propose a workflow, but workflow parsing/validation and an explicit approval flag are required before its execution method proceeds.

Important implementation limits:

- The executor checks elapsed wall time between handlers; it cannot preempt a running Python handler.
- Byte limits apply to artifact I/O and serialized operation outputs. They do not provide OS-enforced memory/CPU limits or a hard kill boundary.
- Capability schema identifiers are declarations; the current shared executor does not perform general JSON-Schema validation of every handler input/output.
- Handlers are trusted in-process Python code. The registry is not a sandbox.
- The Agentics approval flag is an application-level call contract, not an identity provider, signed authorization token or multi-user permission system.
- This P0 change binds execution inputs to the artifact identities recorded by the plan, preventing same-key input substitution after planning.

## 4. Threat model

### Assets

Scientific input/output artifacts; artifact catalog and lineage; run evidence; service capability registry; Rulebook definitions; model/provider credentials; restricted datasets; dependency and model supply chain; user/institutional approvals.

### Actors and trust boundaries

Potential actors include ordinary users, administrators, model providers, third-party tools, compromised dependencies and other local processes/users. Trust boundaries exist at file ingestion, workflow/model output, capability manifests, handler execution, external process/API adapters, the filesystem/catalog, CI and any future hosted deployment.

### Threat register

| Threat | Impact | Current control/evidence | Remaining P0 work |
|---|---|---|---|
| Malformed or oversized input | parser failure, resource exhaustion | bounded artifact ingest/read; schema/contract checks in selected services | uniform ingress limits and adversarial corpus |
| Forged artifact reference | false provenance or wrong data | P0 executor now rejects missing `art_*` references and verifies referenced content | typed artifact references across every service |
| Input substitution after AI planning | approved plan runs on different data | P0 execution compares supplied artifact IDs with persisted plan parents | bind approval to user identity, policy and versioned tool/data scope |
| Malicious model/retrieved content | prompt injection, unsafe tool proposal | model output is parsed as Workflow v1; only registered capabilities; explicit approval | adversarial prompt-injection evaluation and policy enforcement |
| Arbitrary handler/tool execution | code execution, host compromise | only repository-registered handlers are callable through registry | OS-level sandbox, process boundary, filesystem/network allowlist and hard termination |
| CPU/memory/disk exhaustion | service denial or host instability | operation count, output byte and between-handler wall-time checks | OS quotas, queue/fan-out limits, process monitoring and reliable kill |
| Artifact/catalog corruption | lost or misleading scientific records | SHA-256 verification, SQLite integrity, audit and P0 verified backup/restore | crash-boundary fault injection, scheduled backups, restore drills and retention policy |
| Backup theft or tampering | sensitive-data exposure or poisoned restore | backup catalog/object hashes and restore verification | encryption, access controls, signed manifests, off-host copies and key lifecycle |
| Dependency compromise | supply-chain execution | explicit dependency declarations, CI and optional profiles | resolved lock/SBOM, hash verification, vulnerability/license scanning and update policy |
| Sensitive data egress | privacy/legal breach | security policy forbids unauthorized data sharing; no hosted provider is configured by this layer | enforceable classification/egress controls at every adapter and deployment boundary |
| Unauthorized operations | data modification or disclosure | local capability allowlist and AI approval contract | authenticated principals, roles, tenant isolation and audit policy |

## 5. Data classification and default handling

Until an institution adopts a more specific classification scheme, use these labels:

- **Public:** explicitly public data with verified terms.
- **Internal:** non-public organizational data approved for the local deployment.
- **Confidential:** proprietary research, unpublished results or controlled model/data assets.
- **Restricted/regulated:** identifiable human-subject, patient, clinical, credential, export-controlled or otherwise regulated material.

Unknown classification defaults to **Restricted**. CI fixtures must be synthetic or appropriately public. No external model, hosted service or tool may receive confidential/restricted data without documented permission, a reviewed data-processing basis and explicit egress authorization. Access to a dataset is not permission to train model weights on it.

## 6. P0 engineering changes in this delivery

The following code changes are included in this P0 step and were verified by [CI #44909367708](https://github.com/AssayFlux/Molecularis/actions/runs/44909367708), commit `62e55cb` (core 758 passed/12 skipped; optional Chemistry 766/4, Genomics 759/11, Sequence 761/9 with 4 existing warnings):

1. **Artifact-store backup:** SQLite's backup API creates a consistent catalog snapshot; only catalog-referenced objects are copied; catalog and object hashes are verified; the backup is atomically published to a new destination and does not overwrite an existing backup.
2. **Restore:** validates manifest/catalog consistency, SQLite integrity, every object digest and a post-restore artifact audit; restores only to a new directory and refuses damaged backup content.
3. **Audit expansion:** reports missing/corrupt catalog artifacts, dangling lineage, orphan objects and leftover temporary files. Audit remains non-destructive.
4. **Execution integrity:** Rulebook execution now rejects an input string that looks like an artifact ID but does not exist, and verifies artifact content before treating it as provenance.
5. **Approval/input binding:** Agentics execution verifies that the supplied artifact identities are exactly those attached as parents to the persisted plan. Replacing an input while retaining the same input key is rejected.
6. **Regression tests:** round-trip backup/restore, lineage/run preservation, refusal to overwrite, tampered catalog/object rejection, corrupt-source backup rejection, missing artifact rejection and AI input substitution rejection.

These additions do **not** provide backup encryption/signing, OS sandboxing, hard cancellation, distributed recovery or security certification.

## 7. P0 hardening additions — 2026-11-23\n\nThe Agentics execution API no longer accepts a Boolean `approved=True` as authorization. It now requires an `ExecutionApproval` envelope and a caller-supplied external `approval_verifier`. The canonical bytes returned by `MolecularisAI.approval_payload` bind: one-execution scope, unique approval ID, principal ID, exact workflow artifact and hash, sorted input artifact IDs, current capability catalog fingerprint, execution budget fingerprint, execution policy fingerprint and execution-context parameters. The approval envelope has a JSON Schema. The verifier must authenticate the principal, verify a signature over these exact bytes and atomically consume the approval ID to prevent replay. Core cannot authenticate institutional users or guarantee one-use semantics without that external verifier; tests use a synthetic verifier only.\n\nThis closes the prior application-level Boolean approval weakness at the API contract level. It does not implement institutional identity, key management, cryptographic signing, role-based access control or a complete sandbox policy. An opt-in `OCIContainerRunner` now provides a narrow Docker/Podman execution path for digest-pinned images: network disabled, read-only root, dropped Linux capabilities, no-new-privileges, non-root UID/GID, bounded memory/CPU/PIDs/tmpfs and wall-time timeout, explicit read-only input and read-write output mounts, no shell interpolation, and no implicit image pulls. The ordinary Rulebook executor remains in-process; no capability is automatically moved into a container. Container daemon trust, host filesystem permissions, output-volume disk quotas, image provenance/signature policy and real daemon adversarial tests remain open.\n\n## 8. Operating rules until P0 passes

- Run only reviewed repository handlers in a controlled local environment.
- Do not execute model-generated code, arbitrary scripts, shell strings or unreviewed plugin/tool binaries.
- Use synthetic/public fixtures in CI and development.
- Keep confidential/restricted data out of external providers and logs.
- Use a local filesystem with reliable atomic rename and SQLite locking; do not use network filesystems as a supported store.
- Create backups to a separate protected destination. Verify a restore before relying on a backup. Backups are currently neither encrypted nor signed.
- Preserve source artifacts and provenance; never auto-delete orphans based only on an audit report.
- Treat passing CI as engineering evidence only, not scientific validation or operational certification.

## 9. P0 exit checklist

- [ ] Repository/dependency inventory reviewed by maintainers; exact deployed package versions, licenses and data permissions recorded.
- [ ] Representative A–N cross-service artifact handoffs tested with typed contracts and continuous provenance.
- [x] Core approval payload binds principal, nonce, exact plan, inputs, capability catalog, policy and resource budget.\n- [ ] External identity provider, signature verification and atomic replay prevention are integrated and adversarially tested.
- [ ] Threat model and data classification reviewed by the institution.
- [ ] Enforceable data-egress policy and secret handling implemented for every external adapter.
- [ ] OS-level isolation, resource quotas, process termination and filesystem/network policy implemented and adversarially tested.
- [ ] Crash-boundary fault injection and recovery matrix completed; backup/restore drill and retention policy reviewed.
- [ ] CI and optional scientific profiles pass; resolved SBOM, license and vulnerability review completed.
- [ ] Platform acceptance record updated with evidence and explicit residual risks.

**P0 is not complete until every mandatory exit item is supported by reproducible evidence and reviewed.** University scientific validation remains a separate later gate.


## 10. P0 engineering hardening verification — 2026-11-23

GitHub Actions [run #45088241792](https://github.com/AssayFlux/Molecularis/actions/runs/45088241792) on exact commit `2c9ae812ec7ecf213ca8fbc4303132e5e34b43a3`: core 817 passed/12 skipped; Genomics 818/11; Chemistry 825/4; Sequence 820/9 (4 existing warnings); 69 JSON schemas validated; installed-environment SPDX 2.3 inventory generated (43 Python distributions); Ruff, compilation and benchmark smoke steps passed.

The passing CI run includes signed/scope-bound approval contract tests, the opt-in OCI sandbox command-contract tests, the all-pairs synthetic A–N handoff envelope matrix, environment SBOM generation/structure tests, all core regression tests and optional scientific profiles. The SBOM is a Python installed-distribution inventory, not a native OS image SBOM or a license/security attestation. Passing CI does not close institutional, deployment or scientific review gates.


## 10. Consolidated P0 hardening — 2026-11-26

This delivery adds the following repository-level controls:

1. **Fail-closed classification and egress grants:** `python/molecularis/governance.py` defines Public/Internal/Confidential/Restricted labels; missing or malformed labels default to Restricted. Outbound authorization requires an exact HTTPS host, purpose, classification and byte-ceiling grant. URL credentials, IP-literal destinations and non-standard ports are rejected. This is a reusable policy primitive, not a firewall; no claim is made that every adapter currently invokes it or that DNS/redirect/proxy egress is constrained.
2. **Known-vulnerability audit in CI:** CI exports each installed environment with `pip freeze --exclude-editable` and runs `pip-audit --strict` against that resolved requirements snapshot. The main job and each optional scientific profile are scanned. This detects known Python package advisories in those environments; it does not audit OS/native packages, repository source, model/data assets or legal compliance.
3. **Expanded environment SBOM:** SPDX 2.3 output now includes installed Python distributions and dpkg/rpm native package inventories when available, observed Python dependency edges, package URLs, host platform metadata and unreviewed license metadata hints. License declarations/conclusions remain `NOASSERTION`; publisher identity, package provenance, binary hashes, OS vulnerability scanning and legal review remain open.
4. **Regression tests:** tests cover classification fail-closed behavior, exact egress grant matching, byte limits and unsafe URL destinations; SBOM tests cover Python/native inventory structure and preserve explicit non-claims.


The first dependency-audit execution identified **PYSEC-2026-1845** in the resolved development dependency `pytest 8.4.2` (the advisory reported `9.0.3` as the fix). The project and development requirements were raised to `pytest>=9.0.3,<10`. The subsequent resolved-environment CI scan passed on commit `564db597902e5e5a036f191c2228f8e160fe87a5`; all audited Python dependency graphs were clean after the upgrade.

### P0 status after this delivery

The repository now has stronger engineering primitives and an automated Python vulnerability audit. P0 is still **NOT PASSED**. The following require deployment/institutional resources or further integration: connect egress checks to every provider/tool/network adapter and enforce network policy; institutional identity, cryptographic signature verification and atomic replay prevention; integrate OCI isolation into normal capability execution and test a real rootless runtime; enforce output-volume quotas and process-tree termination; verify typed semantic handoffs/provenance across representative real A–N chains; run crash-boundary fault injection and signed/encrypted off-host backup/restore drills; inventory and scan OS/native executables and model/data assets; review dependency licenses and source-specific data permissions; complete university security/privacy/threat-model review and sign a platform acceptance record.

The latest P0 additions are code and CI changes, not evidence of production security, scientific validation, or authorization to process restricted data/train models.


### Exact-HEAD P0 engineering CI evidence — 2026-11-26

GitHub Actions [run #45846604545](https://github.com/AssayFlux/Molecularis/actions/runs/45846604545) passed on `CORE` commit `564db597902e5e5a036f191c2228f8e160fe87a5`:

- Core Python suite: **828 passed, 12 skipped**.
- Chemistry profile: **836 passed, 4 skipped**.
- Genomics profile: **829 passed, 11 skipped**.
- Sequence profile: **831 passed, 9 skipped, 4 warnings**.
- Resolved Python dependency audit: passed in core and all three optional scientific profiles, with no known vulnerabilities reported.
- SPDX 2.3 Python/native environment inventory generated and uploaded as workflow artifact `molecularis-python-environment-sbom` (75,790 bytes; SHA-256 `0a6da8aed7ecef4a8217c0e69d566e987897125a8a495225af391db8b66487eb`).
- Registry/schema validation, Ruff E9/F, Python compilation and all benchmark smoke steps passed.

This is exact-commit engineering CI evidence. It does not replace source-level license review, OS/native vulnerability scanning, container-runtime adversarial tests, recovery drills or institutional approval. The four existing Sequence-profile warnings remain recorded rather than silently treated as failures or ignored.

## 10. OCI timeout cleanup follow-up — 2026-11-26

The opt-in `OCIContainerRunner` now starts the local Docker/Podman client in a new process session. When its wall-time budget expires, the runner attempts to terminate the client process group with SIGTERM, escalates to SIGKILL if the client does not exit, and then attempts daemon-side removal of the container ID recorded in the cidfile. The client process group is therefore handled more deliberately than the prior `subprocess.run(timeout=...)` path.

This remains best-effort cleanup, not proof of complete process-tree or container termination: daemon responsiveness, cidfile creation races, runtime-specific behavior and host-level process supervision require real rootless Docker/Podman adversarial tests. The runner still is not integrated into ordinary in-process Rulebook handler execution. Output bind-mount disk usage is not hard-quota enforced. These P0 items remain open.


## 11. Galaxy adapter egress enforcement follow-up — 2026-11-26

The Galaxy REST client now requires an explicit EgressPolicy for every outbound API request and dataset download. Authorization is performed before transport and binds the configured host, purpose (galaxy_workflow by default), classification (Restricted by default) and request/transfer byte ceiling. Missing policy fails closed. The default opener disables environment-derived HTTP proxies and refuses redirects. Regression tests cover absent policy, recipient mismatch before transport, approved requests, response/download ceilings and redirect rejection.

**Scope and residual risk:** this is enforcement at the Galaxy application adapter only. DNS answers are not pinned or revalidated against private/reserved address ranges, custom injected openers are trusted, and native executables or future adapters can still make independent network connections. This does not replace an OS/container network namespace, firewall or institutional egress gateway. Platform-wide egress remains OPEN; confidential/restricted outbound transfers remain prohibited unless the institution approves and enforces the complete path.


## 12. OCI Rulebook execution adapter — 2026-11-26

The platform now exposes `MolecularisPlatform.bind_sandboxed()` to bind a registered capability to `OCIJSONHandler`. During ordinary Rulebook execution, the handler serializes a versioned `molecularis.oci-handler-request.v1` envelope containing capability ID, typed input values, parameters, run identity, service identity, engine/schema/rulebook versions and execution budget into `/input/request.json`. A digest-pinned image is invoked through the OCI runner with network disabled, read-only root, dropped capabilities, non-root UID/GID, CPU/memory/PID/time bounds and explicit mounts. The tool must write a JSON object to `/output/result.json`; non-zero exit, malformed/non-object JSON, symlink output and aggregate output exceeding the configured accepted-byte ceiling fail closed. A Rulebook integration regression test exercises this binding path.

**Limits not closed by this code:** aggregate output size is checked after the container exits, not enforced as a write-time filesystem quota. The host bind mount can consume disk before the post-run check. No production capability has been switched to this handler by default; image publisher/signature verification and approved image inventory remain open. Rootless Docker/Podman execution, daemon isolation and process-tree cleanup still need adversarial tests on the actual university host. The default Python handlers remain trusted in-process code unless explicitly rebound through the sandbox adapter. P0 remains NOT PASSED.
