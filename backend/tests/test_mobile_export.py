import json
import zipfile
from pathlib import Path

import pytest

from molecularis_api.mobile_export import package_mobile_export


def metadata():
    return {
        "model_id": "astronaut-chat-small",
        "name": "Molecularis Chat Small",
        "publisher": "Molecularis",
        "version": "1.0.0",
        "license": "Apache-2.0",
        "license_url": "https://example.org/license",
        "architecture": "transformer",
        "quantization": "int4",
        "min_sdk": 26,
        "min_ram_mb": 2048,
        "capabilities": ["chat"],
        "converter_name": "external-litertlm-converter",
        "converter_version": "1.2.3",
    }


def fixtures(tmp_path: Path):
    model = tmp_path / "converted.litertlm"
    model.write_bytes(b"test model bytes")
    adapter = tmp_path / "adapter.zip"
    with zipfile.ZipFile(adapter, "w") as archive:
        archive.writestr("adapter_config.json", "{}")
        archive.writestr("adapter_model.safetensors", b"weights")
    return model, adapter


def test_packages_converted_model_with_checksums(tmp_path):
    model, adapter = fixtures(tmp_path)
    output = tmp_path / "release"
    manifest = package_mobile_export(model, adapter, output, metadata())
    assert manifest["format"] == "litertlm"
    assert manifest["source_adapter_sha256"]
    assert len(manifest["sha256"]) == 64
    assert (output / manifest["file_name"]).read_bytes() == model.read_bytes()
    assert json.loads((output / "manifest.json").read_text())["sha256"] == manifest["sha256"]


def test_rejects_missing_provenance_metadata(tmp_path):
    model, adapter = fixtures(tmp_path)
    with pytest.raises(ValueError, match="Missing export metadata"):
        package_mobile_export(model, adapter, tmp_path / "out", {})


def test_rejects_non_https_license(tmp_path):
    model, adapter = fixtures(tmp_path)
    details = metadata()
    details["license_url"] = "http://example.org/license"
    with pytest.raises(ValueError, match="HTTPS"):
        package_mobile_export(model, adapter, tmp_path / "out", details)


def test_rejects_unsafe_adapter_archive_path(tmp_path):
    model = tmp_path / "converted.litertlm"
    model.write_bytes(b"model")
    adapter = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(adapter, "w") as archive:
        archive.writestr("../escape.txt", "bad")
    with pytest.raises(ValueError, match="unsafe path"):
        package_mobile_export(model, adapter, tmp_path / "out", metadata())
