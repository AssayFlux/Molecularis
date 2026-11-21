from __future__ import annotations

import hashlib
import io

import pytest

from molecularis.platform import ArtifactStore, Budget
from molecularis.platform.contracts import ArtifactNotFound, IntegrityError, ResourceLimitError, ValidationError


def test_ingest_deduplicates_blob_and_preserves_distinct_artifact_identity(tmp_path):
    store = ArtifactStore(tmp_path)
    first = store.ingest(b"abc", metadata={"kind": "sequence", "score": 1.5})
    second = store.ingest(b"abc", metadata={"kind": "reference"})
    assert first.digest == hashlib.sha256(b"abc").hexdigest()
    assert first.artifact_id != second.artifact_id
    assert store.get(first.artifact_id).size_bytes == 3
    assert b"".join(store.read(first.artifact_id)) == b"abc"


def test_stream_ingest_and_parent_lineage(tmp_path):
    store = ArtifactStore(tmp_path)
    parent = store.ingest(b"parent")
    child = store.ingest(io.BytesIO(b"child"), parents=[parent.artifact_id])
    assert store.get(child.artifact_id).parents == (parent.artifact_id,)


def test_reject_missing_parent_and_budget_overflow(tmp_path):
    store = ArtifactStore(tmp_path)
    with pytest.raises(ArtifactNotFound):
        store.ingest(b"x", parents=["missing"])
    with pytest.raises(ResourceLimitError):
        store.ingest([b"123", b"456"], budget=Budget(max_bytes=5))


def test_exact_and_numeric_range_indexes(tmp_path):
    store = ArtifactStore(tmp_path)
    a = store.ingest(b"a", metadata={"kind": "protein", "score": 0.2})
    store.ingest(b"b", metadata={"kind": "rna", "score": 0.8})
    exact = store.find_exact("kind", "protein")
    ranged = store.find_range("score", minimum=0.1, maximum=0.5)
    assert [x["artifact_id"] for x in exact.items] == [a.artifact_id]
    assert [x["artifact_id"] for x in ranged.items] == [a.artifact_id]
    assert exact.complete and ranged.exact


def test_query_limit_is_explicitly_incomplete(tmp_path):
    store = ArtifactStore(tmp_path)
    for i in range(4):
        store.ingest(str(i).encode(), metadata={"group": "x"})
    result = store.find_exact("group", "x", limit=2)
    assert len(result.items) == 2
    assert result.complete is False
    assert result.next_offset == 2


def test_audit_reports_integrity_and_does_not_delete_orphans(tmp_path):
    store = ArtifactStore(tmp_path)
    artifact = store.ingest(b"good")
    path = store._blob_path(artifact.digest)
    path.write_bytes(b"bad")
    with pytest.raises(IntegrityError):
        store.get(artifact.artifact_id)
    report = store.audit()
    assert report["failures"] == [artifact.artifact_id]
    assert path.exists()


def test_metadata_rejects_non_json_values(tmp_path):
    store = ArtifactStore(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        store.ingest(b"x", metadata={"not_json": object()})
