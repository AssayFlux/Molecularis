import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from molecularis_api.catalog_signing import generate_keypair, sign_catalog


def test_generate_and_sign_catalog(tmp_path: Path):
    private_path = tmp_path / "publisher.pem"
    public_path = tmp_path / "publisher.pub"
    generate_keypair(private_path, public_path)
    assert private_path.stat().st_mode & 0o777 == 0o600
    private = serialization.load_pem_private_key(private_path.read_bytes(), password=None)
    manifest = {
        "model_id": "chat-small", "version": "1.0.0", "file_name": "chat-small-1.0.0.litertlm",
        "name": "Chat Small", "publisher": "Molecularis", "description": "Small chat model",
        "license": "Apache-2.0", "license_url": "https://example.org/license",
        "architecture": "transformer", "quantization": "int4", "min_sdk": 26, "min_ram_mb": 2048,
        "capabilities": ["chat"], "runtime": "litertlm", "format": "litertlm",
        "size_bytes": 42, "sha256": "a" * 64,
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    envelope_path = tmp_path / "catalog.signed.json"
    sign_catalog([manifest_path], "https://models.example.org/releases", private_path, envelope_path)
    envelope = json.loads(envelope_path.read_text())
    payload = base64.b64decode(envelope["payload"])
    private.public_key().verify(base64.b64decode(envelope["signature"]), payload)
    catalog = json.loads(payload)
    assert catalog["models"][0]["download_url"] == "https://models.example.org/releases/chat-small-1.0.0.litertlm"


def test_refuses_http_download_host(tmp_path: Path):
    private_path = tmp_path / "key.pem"
    public_path = tmp_path / "key.pub"
    generate_keypair(private_path, public_path)
    import pytest
    with pytest.raises(ValueError, match="HTTPS"):
        sign_catalog([], "http://bad.example", private_path, tmp_path / "catalog.json")


def test_refuses_overwrite_key(tmp_path: Path):
    private_path = tmp_path / "key.pem"
    public_path = tmp_path / "key.pub"
    generate_keypair(private_path, public_path)
    import pytest
    with pytest.raises(FileExistsError):
        generate_keypair(private_path, public_path)
