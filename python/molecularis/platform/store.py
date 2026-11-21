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
import sqlite3
import tempfile
import time
import uuid

from .contracts import (
    ArtifactNotFound, Budget, IntegrityError, QueryResult, ResourceLimitError,
    ValidationError,
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


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

    def find_exact(self, key: str, value: Any, *, limit: int = 1000,
                   budget: Budget | None = None) -> QueryResult:
        return self._query_label(key, value, None, limit=limit, budget=budget)

    def find_range(self, key: str, *, minimum: float | None = None,
                   maximum: float | None = None, limit: int = 1000,
                   budget: Budget | None = None) -> QueryResult:
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValidationError("minimum cannot exceed maximum")
        return self._query_label(key, None, (minimum, maximum), limit=limit, budget=budget)

    def _query_label(self, key: str, exact: Any, bounds: tuple[float | None, float | None] | None,
                     *, limit: int, budget: Budget | None) -> QueryResult:
        budget = budget or Budget()
        if limit <= 0:
            raise ValidationError("limit must be positive")
        effective_limit = min(limit, budget.max_results)
        clauses = ["key=?"]
        args: list[Any] = [key]
        if bounds is None:
            clauses.append("value_json=?")
            args.append(_canonical(exact).decode("utf-8"))
            order = "artifact_id"
        else:
            low, high = bounds
            if low is not None:
                clauses.append("value_number>=?")
                args.append(low)
            if high is not None:
                clauses.append("value_number<=?")
                args.append(high)
            clauses.append("value_number IS NOT NULL")
            order = "value_number, artifact_id"
        where = " AND ".join(clauses)
        started = time.monotonic()
        with self._session() as conn:
            conn.execute("BEGIN")
            snapshot = conn.execute("SELECT COALESCE(MAX(rowid),0) AS s FROM artifacts").fetchone()["s"]
            rows = conn.execute(
                f"SELECT artifact_id FROM labels WHERE {where} ORDER BY {order} LIMIT ?",
                (*args, budget.max_candidates + 1),
            ).fetchall()
        candidates = len(rows)
        if candidates > budget.max_candidates:
            rows = rows[:budget.max_candidates]
        if time.monotonic() - started > budget.max_wall_seconds:
            return QueryResult((), str(snapshot), min(candidates, budget.max_candidates),
                               False, True, None)
        complete = candidates <= budget.max_candidates and len(rows) <= effective_limit
        selected = rows[:effective_limit]
        next_offset = None if complete else effective_limit
        items = tuple({"artifact_id": row["artifact_id"]} for row in selected)
        return QueryResult(items, str(snapshot), min(candidates, budget.max_candidates),
                           complete, True, next_offset)

    def record_run(self, *, run_id: str, service_id: str, operation: str, status: str,
                   inputs: list[str], outputs: list[str], evidence: dict[str, Any]) -> None:
        with self._session() as conn:
            conn.execute(
                "INSERT INTO runs VALUES(?,?,?,?,?,?,?,?,?)",
                (run_id, service_id, operation, status, time.time(), time.time(),
                 _canonical(inputs).decode(), _canonical(outputs).decode(),
                 _canonical(evidence).decode()),
            )

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
        all_blobs = {p.parent.name + p.name for p in self.blob_root.glob("*/*") if p.is_file()}
        return {"catalog_artifacts": len(rows), "verified": valid, "failures": failures,
                "orphan_digests": sorted(all_blobs - referenced)}
