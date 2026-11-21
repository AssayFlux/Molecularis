"""Local-first immutable artifact store with SQLite catalog and indexed labels.

The catalog is authoritative for visibility. Blobs are published before catalog rows,
so a crash can leave an unreferenced blob but cannot expose a catalog row to missing
content. Orphans are safe to collect after an explicit audit.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable, Iterator, Any
import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
import time
import uuid

from .contracts import (
    ArtifactNotFound, Budget, IntegrityError, QueryResult, ResourceLimitError,
    ValidationError,
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    digest: str
    size_bytes: int
    media_type: str
    schema_id: str
    created_at: float
    metadata: dict[str, Any]
    parents: tuple[str, ...]


class ArtifactStore:
    """Single-writer local artifact store; concurrent readers use SQLite snapshots."""

    FORMAT_VERSION = 1

    def __init__(self, root: str | Path, *, busy_timeout_ms: int = 10_000) -> None:
        self.root = Path(root).expanduser().resolve()
        self.blob_root = self.root / "objects" / "sha256"
        self.tmp_root = self.root / "tmp"
        self.db_path = self.root / "catalog.sqlite3"
        self.blob_root.mkdir(parents=True, exist_ok=True)
        self.tmp_root.mkdir(parents=True, exist_ok=True)
        self._busy_timeout_ms = busy_timeout_ms
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=self._busy_timeout_ms / 1000)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute(f"PRAGMA busy_timeout={int(self._busy_timeout_ms)}")
        return conn

    @contextmanager
    def _session(self) -> Iterator[sqlite3.Connection]:
        conn = self._connect()
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _initialize(self) -> None:
        with self._session() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=FULL")
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS platform_meta (
                    key TEXT PRIMARY KEY, value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    digest TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL CHECK(size_bytes >= 0),
                    media_type TEXT NOT NULL,
                    schema_id TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    metadata_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_artifacts_digest ON artifacts(digest);
                CREATE TABLE IF NOT EXISTS lineage (
                    artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
                    parent_id TEXT NOT NULL,
                    ordinal INTEGER NOT NULL,
                    PRIMARY KEY(artifact_id, ordinal)
                );
                CREATE INDEX IF NOT EXISTS idx_lineage_parent ON lineage(parent_id);
                CREATE TABLE IF NOT EXISTS labels (
                    artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
                    key TEXT NOT NULL,
                    value_json TEXT NOT NULL,
                    value_text TEXT NOT NULL,
                    value_number REAL,
                    PRIMARY KEY(artifact_id, key)
                );
                CREATE INDEX IF NOT EXISTS idx_labels_exact ON labels(key, value_json, artifact_id);
                CREATE INDEX IF NOT EXISTS idx_labels_range ON labels(key, value_number, artifact_id);
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    service_id TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    status TEXT NOT NULL,
                    started_at REAL NOT NULL,
                    finished_at REAL,
                    inputs_json TEXT NOT NULL,
                    outputs_json TEXT NOT NULL,
                    evidence_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS journal (
                    tx_id TEXT PRIMARY KEY,
                    state TEXT NOT NULL,
                    artifact_id TEXT NOT NULL,
                    digest TEXT NOT NULL,
                    created_at REAL NOT NULL
                );
            """)
            row = conn.execute("SELECT value FROM platform_meta WHERE key='format_version'").fetchone()
            if row is None:
                conn.execute(
                    "INSERT INTO platform_meta(key,value) VALUES('format_version',?)",
                    (str(self.FORMAT_VERSION),),
                )
            elif int(row["value"]) != self.FORMAT_VERSION:
                raise IntegrityError("unsupported catalog format version",
                                     details={"found": row["value"], "supported": self.FORMAT_VERSION})

    def _blob_path(self, digest: str) -> Path:
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValidationError("invalid SHA-256 digest")
        return self.blob_root / digest[:2] / digest[2:]

    def ingest(
        self,
        chunks: bytes | Iterable[bytes] | BinaryIO,
        *,
        media_type: str = "application/octet-stream",
        schema_id: str = "urn:molecularis:artifact:raw:1",
        metadata: dict[str, Any] | None = None,
        parents: Iterable[str] = (),
        budget: Budget | None = None,
    ) -> Artifact:
        budget = budget or Budget()
        metadata = dict(metadata or {})
        if any(not isinstance(key, str) for key in metadata):
            raise ValidationError("metadata keys must be strings")
        _canonical(metadata)
        parent_ids = tuple(parents)
        if not media_type or not schema_id:
            raise ValidationError("media_type and schema_id are required")
        if isinstance(chunks, bytes):
            iterator: Iterator[bytes] = iter((chunks,))
        elif hasattr(chunks, "read"):
            def read_chunks() -> Iterator[bytes]:
                while True:
                    part = chunks.read(budget.chunk_bytes)  # type: ignore[union-attr]
                    if not part:
                        break
                    yield part
            iterator = read_chunks()
        else:
            iterator = iter(chunks)

        digest = hashlib.sha256()
        size = 0
        fd, temp_name = tempfile.mkstemp(prefix="ingest-", dir=self.tmp_root)
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "wb") as stream:
                for part in iterator:
                    if not isinstance(part, bytes):
                        raise ValidationError("artifact stream must yield bytes")
                    size += len(part)
                    if size > budget.max_bytes:
                        raise ResourceLimitError("artifact exceeds byte budget",
                                                 details={"limit": budget.max_bytes, "observed": size})
                    digest.update(part)
                    stream.write(part)
                stream.flush()
                os.fsync(stream.fileno())
            hex_digest = digest.hexdigest()
            destination = self._blob_path(hex_digest)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if destination.stat().st_size != size:
                    raise IntegrityError("existing content-addressed object has unexpected size")
                temp_path.unlink()
            else:
                os.replace(temp_path, destination)
                try:
                    dir_fd = os.open(destination.parent, os.O_RDONLY)
                    try:
                        os.fsync(dir_fd)
                    finally:
                        os.close(dir_fd)
                except OSError:
                    pass

            artifact_id = "art_" + uuid.uuid4().hex
            created_at = time.time()
            tx_id = uuid.uuid4().hex
            with self._session() as conn:
                conn.execute("BEGIN IMMEDIATE")
                for parent_id in parent_ids:
                    if conn.execute("SELECT 1 FROM artifacts WHERE artifact_id=?", (parent_id,)).fetchone() is None:
                        raise ArtifactNotFound("parent artifact does not exist", details={"parent_id": parent_id})
                conn.execute("INSERT INTO journal VALUES(?,?,?,?,?)",
                             (tx_id, "prepared", artifact_id, hex_digest, created_at))
                conn.execute(
                    "INSERT INTO artifacts VALUES(?,?,?,?,?,?,?)",
                    (artifact_id, hex_digest, size, media_type, schema_id, created_at,
                     _canonical(metadata).decode("utf-8")),
                )
                conn.executemany("INSERT INTO lineage VALUES(?,?,?)",
                                 [(artifact_id, parent, i) for i, parent in enumerate(parent_ids)])
                for key, value in sorted(metadata.items()):
                    encoded = _canonical(value).decode("utf-8")
                    number = float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None
                    conn.execute("INSERT INTO labels VALUES(?,?,?,?,?)",
                                 (artifact_id, str(key), encoded, str(value), number))
                conn.execute("UPDATE journal SET state='committed' WHERE tx_id=?", (tx_id,))
            return Artifact(artifact_id, hex_digest, size, media_type, schema_id,
                            created_at, metadata, parent_ids)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def get(self, artifact_id: str, *, verify: bool = True) -> Artifact:
        with self._session() as conn:
            row = conn.execute("SELECT * FROM artifacts WHERE artifact_id=?", (artifact_id,)).fetchone()
            if row is None:
                raise ArtifactNotFound("artifact not found", details={"artifact_id": artifact_id})
            parents = tuple(r["parent_id"] for r in conn.execute(
                "SELECT parent_id FROM lineage WHERE artifact_id=? ORDER BY ordinal", (artifact_id,)))
        artifact = Artifact(row["artifact_id"], row["digest"], row["size_bytes"],
                            row["media_type"], row["schema_id"], row["created_at"],
                            json.loads(row["metadata_json"]), parents)
        if verify:
            path = self._blob_path(artifact.digest)
            if not path.is_file() or path.stat().st_size != artifact.size_bytes:
                raise IntegrityError("artifact object is missing or has wrong size")
            hasher = hashlib.sha256()
            with path.open("rb") as stream:
                for part in iter(lambda: stream.read(1_048_576), b""):
                    hasher.update(part)
            if hasher.hexdigest() != artifact.digest:
                raise IntegrityError("artifact digest verification failed")
        return artifact

    def read(self, artifact_id: str, *, budget: Budget | None = None) -> Iterator[bytes]:
        artifact = self.get(artifact_id)
        budget = budget or Budget()
        if artifact.size_bytes > budget.max_bytes:
            raise ResourceLimitError("artifact exceeds read byte budget")
        path = self._blob_path(artifact.digest)
        with path.open("rb") as stream:
            while True:
                part = stream.read(budget.chunk_bytes)
                if not part:
                    break
                yield part

    def find_exact(self, key: str, value: Any, *, limit: int = 1000, offset: int = 0,
                   snapshot_id: str | None = None, budget: Budget | None = None) -> QueryResult:
        return self._query_label(key, value, None, limit=limit, offset=offset, snapshot_id=snapshot_id, budget=budget)

    def find_range(self, key: str, *, minimum: float | None = None, maximum: float | None = None,
                   limit: int = 1000, offset: int = 0, snapshot_id: str | None = None,
                   budget: Budget | None = None) -> QueryResult:
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValidationError("minimum cannot exceed maximum")
        return self._query_label(key, None, (minimum, maximum), limit=limit, offset=offset,
                                 snapshot_id=snapshot_id, budget=budget)

    def _query_label(self, key: str, exact: Any, bounds: tuple[float | None, float | None] | None, *,
                     limit: int, offset: int, snapshot_id: str | None, budget: Budget | None) -> QueryResult:
        budget = budget or Budget()
        if not key or limit <= 0 or offset < 0:
            raise ValidationError("key and positive limit are required; offset cannot be negative")
        page_size = min(limit, budget.max_results, budget.max_candidates)
        clauses = ["l.key=?"]
        args: list[Any] = [key]
        if bounds is None:
            clauses.append("l.value_json=?")
            args.append(_canonical(exact).decode("utf-8"))
            order = "l.artifact_id"
        else:
            low, high = bounds
            if low is not None:
                clauses.append("l.value_number>=?")
                args.append(low)
            if high is not None:
                clauses.append("l.value_number<=?")
                args.append(high)
            clauses.append("l.value_number IS NOT NULL")
            order = "l.value_number, l.artifact_id"
        started = time.monotonic()
        with self._session() as conn:
            conn.execute("BEGIN")
            current = int(conn.execute("SELECT COALESCE(MAX(rowid),0) FROM artifacts").fetchone()[0])
            if snapshot_id is None:
                snapshot = current
            else:
                try:
                    snapshot = int(snapshot_id)
                except (TypeError, ValueError) as exc:
                    raise ValidationError("snapshot_id must be a catalog snapshot integer") from exc
                if snapshot < 0 or snapshot > current:
                    raise ValidationError("snapshot_id is outside available catalog history")
            where = " AND ".join(["a.rowid<=?"] + clauses)
            rows = conn.execute(
                f"SELECT l.artifact_id FROM labels l JOIN artifacts a ON a.artifact_id=l.artifact_id "
                f"WHERE {where} ORDER BY {order} LIMIT ? OFFSET ?",
                (snapshot, *args, page_size + 1, offset),
            ).fetchall()
        has_more = len(rows) > page_size
        selected = rows[:page_size]
        if time.monotonic() - started > budget.max_wall_seconds:
            return QueryResult((), str(snapshot), len(selected), False, True, offset)
        next_offset = offset + len(selected) if has_more else None
        return QueryResult(tuple({"artifact_id": row["artifact_id"]} for row in selected),
                           str(snapshot), len(selected), not has_more, True, next_offset)

    def record_run(self, *, run_id: str, service_id: str, operation: str, status: str,
                   inputs: list[str], outputs: list[str], evidence: dict[str, Any],
                   started_at: float | None = None, finished_at: float | None = None) -> None:
        if not all((run_id, service_id, operation, status)):
            raise ValidationError("run identity and status fields must be non-empty")
        with self._session() as conn:
            conn.execute("INSERT INTO runs VALUES(?,?,?,?,?,?,?,?,?)",
                         (run_id, service_id, operation, status, started_at or time.time(),
                          finished_at or time.time(), _canonical(inputs).decode(),
                          _canonical(outputs).decode(), _canonical(evidence).decode()))

    def get_run(self, run_id: str) -> dict[str, Any]:
        with self._session() as conn:
            row = conn.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            raise ArtifactNotFound("run evidence not found", details={"run_id": run_id})
        return {"run_id": row["run_id"], "service_id": row["service_id"],
                "operation": row["operation"], "status": row["status"],
                "started_at": row["started_at"], "finished_at": row["finished_at"],
                "inputs": json.loads(row["inputs_json"]), "outputs": json.loads(row["outputs_json"]),
                "evidence": json.loads(row["evidence_json"])}

    @staticmethod
    def _file_sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for part in iter(lambda: stream.read(1_048_576), b""):
                digest.update(part)
        return digest.hexdigest()

    def backup(self, destination: str | Path) -> dict[str, Any]:
        """Create a verified, non-overwriting, self-contained local backup.

        The SQLite backup API captures a consistent catalog snapshot. Only blobs
        referenced by that snapshot are copied. The destination is atomically
        published after the catalog and every object have been verified.
        """
        target = Path(destination).expanduser().resolve()
        if target == self.root or self.root in target.parents:
            raise ValidationError("backup destination cannot be inside the live store")
        if target.exists():
            raise ValidationError("backup destination already exists")
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=f".{target.name}.backup-", dir=target.parent))
        try:
            db_target = staging / "catalog.sqlite3"
            source = sqlite3.connect(self.db_path)
            replica = sqlite3.connect(db_target)
            try:
                source.backup(replica)
                integrity = replica.execute("PRAGMA integrity_check").fetchone()
                if integrity is None or integrity[0] != "ok":
                    raise IntegrityError("SQLite backup failed integrity_check")
                rows = replica.execute(
                    "SELECT digest, size_bytes FROM artifacts ORDER BY digest"
                ).fetchall()
            finally:
                replica.close()
                source.close()

            objects: dict[str, int] = {}
            for digest, size in rows:
                objects[digest] = int(size)
            for digest, expected_size in objects.items():
                source_path = self._blob_path(digest)
                if not source_path.is_file() or source_path.stat().st_size != expected_size:
                    raise IntegrityError("cannot back up a missing or incorrectly sized object",
                                         details={"digest": digest})
                if self._file_sha256(source_path) != digest:
                    raise IntegrityError("cannot back up a corrupt object",
                                         details={"digest": digest})
                object_target = staging / "objects" / "sha256" / digest[:2] / digest[2:]
                object_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source_path, object_target)
                if self._file_sha256(object_target) != digest:
                    raise IntegrityError("backup object verification failed",
                                         details={"digest": digest})

            count_connection = sqlite3.connect(db_target)
            try:
                artifact_count = int(count_connection.execute(
                    "SELECT COUNT(*) FROM artifacts"
                ).fetchone()[0])
            finally:
                count_connection.close()
            manifest = {
                "format_version": self.FORMAT_VERSION,
                "created_at": time.time(),
                "catalog_sha256": self._file_sha256(db_target),
                "artifact_count": artifact_count,
                "objects": [{"digest": digest, "size_bytes": size}
                            for digest, size in sorted(objects.items())],
            }
            manifest_path = staging / "backup-manifest.json"
            manifest_path.write_text(
                json.dumps(manifest, sort_keys=True, indent=2, allow_nan=False) + "\n",
                encoding="utf-8",
            )
            with manifest_path.open("rb") as stream:
                os.fsync(stream.fileno())
            os.replace(staging, target)
            return manifest
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise

    @classmethod
    def restore(cls, backup_dir: str | Path, destination: str | Path) -> "ArtifactStore":
        """Restore a verified backup into a new, non-existing store directory."""
        source = Path(backup_dir).expanduser().resolve()
        target = Path(destination).expanduser().resolve()
        if (not source.is_dir() or target.exists() or target == source
                or source in target.parents):
            raise ValidationError("backup must exist and restore destination must be a new directory outside the backup")
        manifest_path = source / "backup-manifest.json"
        db_source = source / "catalog.sqlite3"
        if not manifest_path.is_file() or not db_source.is_file():
            raise IntegrityError("backup is missing its manifest or catalog")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise IntegrityError("backup manifest is unreadable") from exc
        if not isinstance(manifest, dict) or manifest.get("format_version") != cls.FORMAT_VERSION:
            raise IntegrityError("unsupported backup format")
        if cls._file_sha256(db_source) != manifest.get("catalog_sha256"):
            raise IntegrityError("backup catalog digest mismatch")

        try:
            conn = sqlite3.connect(f"file:{db_source}?mode=ro", uri=True)
            try:
                check = conn.execute("PRAGMA integrity_check").fetchone()
                if check is None or check[0] != "ok":
                    raise IntegrityError("backup catalog failed integrity_check")
                rows = conn.execute("SELECT digest, size_bytes FROM artifacts").fetchall()
            finally:
                conn.close()
            expected = {digest: int(size) for digest, size in rows}
            if any(not isinstance(digest, str) or len(digest) != 64
                   or any(char not in "0123456789abcdef" for char in digest)
                   for digest in expected):
                raise IntegrityError("backup catalog contains an invalid object digest")
            objects = manifest.get("objects")
            if not isinstance(objects, list) or any(not isinstance(item, dict) for item in objects):
                raise IntegrityError("backup manifest object list is invalid")
            listed = {item["digest"]: int(item["size_bytes"]) for item in objects}
            if expected != listed or len(listed) != len(objects):
                raise IntegrityError("backup manifest does not match catalog object references")
            if int(manifest.get("artifact_count", -1)) != len(rows):
                raise IntegrityError("backup manifest artifact count does not match catalog")

            target.parent.mkdir(parents=True, exist_ok=True)
            staging = Path(tempfile.mkdtemp(prefix=f".{target.name}.restore-", dir=target.parent))
            try:
                shutil.copyfile(db_source, staging / "catalog.sqlite3")
                for digest, size in expected.items():
                    source_object = source / "objects" / "sha256" / digest[:2] / digest[2:]
                    if (not source_object.is_file() or source_object.stat().st_size != size
                            or cls._file_sha256(source_object) != digest):
                        raise IntegrityError("backup contains a missing or corrupt object",
                                             details={"digest": digest})
                    object_target = staging / "objects" / "sha256" / digest[:2] / digest[2:]
                    object_target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source_object, object_target)
                os.replace(staging, target)
            except Exception:
                shutil.rmtree(staging, ignore_errors=True)
                raise
        except Exception:
            raise

        restored = cls(target)
        report = restored.audit()
        if report["failures"] or report["orphan_digests"]:
            shutil.rmtree(target, ignore_errors=True)
            raise IntegrityError("restored store failed its post-restore audit",
                                 details={"audit": report})
        return restored

    def audit(self) -> dict[str, Any]:
        """Verify all catalog references and report unreferenced blobs without deleting them."""
        with self._session() as conn:
            rows = conn.execute("SELECT artifact_id FROM artifacts ORDER BY artifact_id").fetchall()
        valid = 0
        failures: list[str] = []
        referenced: set[str] = set()
        for row in rows:
            try:
                artifact = self.get(row["artifact_id"])
                valid += 1
                referenced.add(artifact.digest)
            except (ArtifactNotFound, IntegrityError):
                failures.append(row["artifact_id"])
        with self._session() as conn:
            dangling_parents = conn.execute(
                "SELECT l.artifact_id, l.parent_id FROM lineage l "
                "LEFT JOIN artifacts p ON p.artifact_id=l.parent_id "
                "WHERE p.artifact_id IS NULL ORDER BY l.artifact_id, l.parent_id"
            ).fetchall()
        all_blobs = {p.parent.name + p.name for p in self.blob_root.glob("*/*") if p.is_file()}
        temp_files = sorted(p.name for p in self.tmp_root.iterdir() if p.is_file())
        return {
            "catalog_artifacts": len(rows),
            "verified": valid,
            "failures": failures,
            "dangling_lineage": [
                {"artifact_id": row["artifact_id"], "parent_id": row["parent_id"]}
                for row in dangling_parents
            ],
            "orphan_digests": sorted(all_blobs - referenced),
            "temporary_files": temp_files,
            "ok": not failures and not dangling_parents,
        }
