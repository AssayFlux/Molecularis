from __future__ import annotations
import hashlib
import json
import pytest
from molecularis.platform import Budget, MolecularisPlatform
from molecularis.platform.contracts import ValidationError
from molecularis.sequence_service import (
    SequenceDocument, ingest_sequence, load_sequence, register_sequence_service, sequence_rulebook,
)


def runtime(tmp_path):
    platform = MolecularisPlatform(tmp_path / "store")
    platform.start()
    register_sequence_service(platform)
    return platform


def test_sequence_normalization_and_hash():
    a = SequenceDocument("seq", " atg\ngct taa ", "DNA", "fixture")
    b = SequenceDocument("seq", "ATGGCTTAA", "DNA", "fixture")
    assert a.sequence == "ATGGCTTAA"
    assert a.to_json() == b.to_json()
    assert a.sha256 == hashlib.sha256(a.to_json()).hexdigest()


@pytest.mark.parametrize("kind,sequence", [
    ("DNA", "ACGU"), ("RNA", "ACTG"), ("protein", "ACGT*?"), ("unknown", "ACGT"), ("DNA", ""),
])
def test_invalid_alphabet_is_rejected(kind, sequence):
    with pytest.raises((ValueError, TypeError)):
        SequenceDocument("seq", sequence, kind)


def test_json_rejects_duplicate_and_unknown_fields():
    duplicate = b'{"schema":"molecularis.sequence-record.v1","identifier":"x","identifier":"y","description":"","sequence_type":"DNA","sequence":"ACGT"}'
    with pytest.raises(ValueError, match="duplicate"):
        SequenceDocument.from_json(duplicate)
    with pytest.raises(ValueError, match="fields"):
        SequenceDocument.from_json(json.dumps({"schema":"molecularis.sequence-record.v1",
            "identifier":"x","description":"","sequence_type":"DNA","sequence":"ACGT","extra":1}))


def test_artifact_round_trip(tmp_path):
    p = runtime(tmp_path)
    try:
        record = SequenceDocument("seq", "ACGT")
        artifact = ingest_sequence(p, record)
        assert load_sequence(p, artifact.artifact_id) == record
        assert p.store.get(artifact.artifact_id).metadata["sequence_sha256"] == record.sha256
    finally:
        p.close()


@pytest.mark.parametrize("operation,expected", [
    ("validate", {"valid": True, "length": 9}),
    ("statistics", {"length": 9, "gc_fraction": 3/9, "a": 3, "c": 1, "g": 2, "t": 3}),
    ("reverse_complement", {"sequence": "TTAAGCCAT"}),
    ("transcribe", {"sequence": "AUGGCUUAA"}),
    ("translate", {"protein": "MA", "table_id": 1}),
])
def test_rulebook_capability_operations(tmp_path, operation, expected):
    p = runtime(tmp_path)
    try:
        artifact = ingest_sequence(p, SequenceDocument("synthetic", "ATGGCTTAA"))
        values = p.execute(sequence_rulebook(operation),
                           {"sequence_artifact_id": artifact.artifact_id})
        report = values["sequence_result"]
        assert report["operation"] == operation
        assert report["sequence_sha256"] == artifact.digest
        for key, value in expected.items():
            assert report["result"][key] == value
        assert report["rules_checked"] == ["SEQ-001", "SEQ-002", "SEQ-003", "SEQ-004", "SEQ-005"]
    finally:
        p.close()


def test_cds_translation_fails_closed(tmp_path):
    p = runtime(tmp_path)
    try:
        artifact = ingest_sequence(p, SequenceDocument("partial", "ATGGCTAAA"))
        with pytest.raises(ValueError, match="terminal codon"):
            p.execute(sequence_rulebook("translate", parameters={"cds": True}),
                      {"sequence_artifact_id": artifact.artifact_id})
    finally:
        p.close()


def test_byte_budget_and_wrong_artifact_type(tmp_path):
    p = runtime(tmp_path)
    try:
        artifact = ingest_sequence(p, SequenceDocument("seq", "ACGT"))
        with pytest.raises(Exception, match="byte budget"):
            load_sequence(p, artifact.artifact_id, budget=Budget(max_bytes=1))
        other = p.ingest(b"{}", media_type="application/json", schema_id="other.v1")
        with pytest.raises(ValidationError, match="not a Sequence"):
            load_sequence(p, other.artifact_id)
    finally:
        p.close()
