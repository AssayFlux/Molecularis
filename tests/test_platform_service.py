from __future__ import annotations

import json

import pytest

from molecularis.platform import Capability, MolecularisPlatform, RuntimeState
from molecularis.platform.contracts import ValidationError


def test_lifecycle_and_persistent_restart(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    assert platform.state is RuntimeState.NEW
    with pytest.raises(ValidationError):
        platform.ingest(b"x", media_type="text/plain", schema_id="test:v1")
    platform.start()
    artifact = platform.ingest(b"payload", media_type="text/plain", schema_id="test:v1")
    platform.close()
    assert platform.state is RuntimeState.CLOSED
    with pytest.raises(ValidationError):
        platform.start()
    reopened = MolecularisPlatform(tmp_path)
    reopened.start()
    assert b"".join(reopened.store.read(artifact.artifact_id)) == b"payload"


def test_manifest_loads_declarations_without_importing_code(tmp_path):
    manifest = tmp_path / "capabilities.json"
    manifest.write_text(json.dumps({
        "schema_version": 1,
        "capabilities": [{
            "id": "test.echo", "version": "1", "service": "test",
            "operation": "echo", "input_schema": "test:in",
            "output_schema": "test:out", "deterministic": True,
            "description": "test capability"
        }]
    }), encoding="utf-8")
    platform = MolecularisPlatform.from_capability_manifest(tmp_path / "store", manifest)
    assert platform.registry.get("test.echo").service == "test"
    platform.close()


def test_invalid_manifest_rejected(tmp_path):
    manifest = tmp_path / "bad.json"
    manifest.write_text('{"schema_version": 2, "capabilities": []}', encoding="utf-8")
    with pytest.raises(ValidationError):
        MolecularisPlatform.from_capability_manifest(tmp_path / "store", manifest)
