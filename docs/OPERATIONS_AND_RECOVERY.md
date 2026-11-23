# Molecularis operations, backup and recovery runbook

**Status:** engineering procedure for controlled local development. This is not a production, regulated-data or institutional approval.

## Operating boundary

- Use only reviewed repository handlers and preloaded, digest-pinned tool images.
- Until institutional identity/authorization, real sandbox integration and egress controls are deployed, use synthetic or explicitly public data only.
- The local ArtifactStore is single-writer. Use a local filesystem with SQLite locking and atomic rename; do not treat network filesystems or multi-host shared writes as supported.
- Keep backup destinations outside the live store, on a separately protected volume. Current backups are not encrypted or signed.
- Do not rely on an audit report to delete orphaned data automatically.

## Routine integrity check

```python
from molecularis.platform import ArtifactStore

store = ArtifactStore("/srv/molecularis/store")
report = store.audit()
if not report["ok"]:
    raise RuntimeError(f"ArtifactStore integrity failures: {report}")
if report["orphan_digests"] or report["temporary_files"]:
    raise RuntimeError(f"Review orphan/temp objects before cleanup: {report}")
```

Audit is read-only. Preserve the report with the deployment's change/incident record, without including sensitive payloads.

## Create a verified backup

```python
from molecularis.platform import ArtifactStore

store = ArtifactStore("/srv/molecularis/store")
manifest = store.backup("/srv/molecularis-backups/backup-YYYYMMDD-HHMMSS")
print(manifest)
```

The destination must not exist and must be outside the live store. Backup verifies the SQLite snapshot and copied object digests before atomically publishing the directory. Restrict backup directory access and encrypt the storage volume using institution-managed keys until application-level encryption/key management is delivered.

## Restore drill

Restore only into a new, empty destination. Never overwrite the live store during a drill.

```python
from molecularis.platform import ArtifactStore

restored = ArtifactStore.restore(
    "/srv/molecularis-backups/backup-YYYYMMDD-HHMMSS",
    "/srv/molecularis-restore-drills/restore-YYYYMMDD-HHMMSS",
)
report = restored.audit()
assert report["ok"] and not report["orphan_digests"]
```

After restore, verify a representative set of artifact IDs, source/parent lineage, run records, and domain-level loaders. Record backup timestamp, catalog/object counts, restore duration, audit report, selected artifact checks and operator. Do not promote a restored store until application-level checks and the institution's recovery objectives are met.

## Incident / corruption response

1. Stop new writes and isolate the affected deployment from external tools/providers.
2. Preserve the live directory, logs, backup manifest and audit output as read-only evidence.
3. Do not delete or repair catalog rows/blobs manually.
4. Restore the latest known-good backup into a new directory.
5. Run store audit and representative service-level artifact/lineage checks.
6. Record missing work since the backup, data-loss window, root cause and recovery duration.
7. Obtain operator approval before switching the application to the restored store.
8. Keep the damaged store and evidence under the institution's retention policy.

## Required deployment-specific values (must be supplied by operator)

- Named data owner and system owner.
- Data classification and approved dataset permissions.
- Backup frequency, retention, encryption and off-host copy policy.
- Recovery Point Objective (RPO) and Recovery Time Objective (RTO).
- Key custody/rotation and restore authorization.
- Container runtime version, rootless/daemon configuration, image allowlist/signature verification and host output-volume quota.
- External egress allowlist, secrets provider and identity/approval verifier.
- Incident contact and escalation path.

## Open validation evidence

The repository tests exercise backup/restore round-trip and tamper detection. A deployment owner must still run and sign a scheduled restore drill, crash-boundary fault injection, retention review, encryption/key-management review, RPO/RTO measurement and a real rootless-container adversarial test. These are not marked complete by CI.
