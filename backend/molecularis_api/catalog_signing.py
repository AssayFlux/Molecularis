from __future__ import annotations

import argparse
import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def generate_keypair(private_path: Path, public_path: Path) -> None:
    if private_path.exists() or public_path.exists():
        raise FileExistsError("Refusing to overwrite an existing signing key.")
    private = Ed25519PrivateKey.generate()
    private_path.parent.mkdir(parents=True, exist_ok=True)
    private_path.write_bytes(private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    os.chmod(private_path, 0o600)
    public_path.write_text(base64.b64encode(private.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )).decode("ascii") + "\n", encoding="ascii")


def sign_catalog(manifest_paths: list[Path], base_download_url: str, private_path: Path, output: Path) -> None:
    base = urlparse(base_download_url)
    if base.scheme != "https" or not base.netloc:
        raise ValueError("The model download base URL must use HTTPS.")
    manifests = []
    seen: set[str] = set()
    for path in manifest_paths:
        item = json.loads(path.read_text(encoding="utf-8"))
        model_id, version = item.get("model_id"), item.get("version")
        if not isinstance(model_id, str) or not isinstance(version, str):
            raise ValueError(f"{path} is missing model_id or version.")
        key = f"{model_id}:{version}"
        if key in seen:
            raise ValueError(f"Duplicate catalog model version: {key}")
        seen.add(key)
        file_name = item.get("file_name")
        if not isinstance(file_name, str) or "/" in file_name or "\\" in file_name:
            raise ValueError(f"Unsafe artifact filename in {path}.")
        item["download_url"] = base_download_url.rstrip("/") + "/" + file_name
        manifests.append(item)
    payload = json.dumps({
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "models": manifests,
    }, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    private = serialization.load_pem_private_key(private_path.read_bytes(), password=None)
    if not isinstance(private, Ed25519PrivateKey):
        raise ValueError("Catalog signing key must be an Ed25519 private key.")
    envelope = {
        "payload": base64.b64encode(payload).decode("ascii"),
        "signature": base64.b64encode(private.sign(payload)).decode("ascii"),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Ed25519 publisher keys or sign a model catalog.")
    commands = parser.add_subparsers(dest="command", required=True)
    keygen = commands.add_parser("generate-keypair")
    keygen.add_argument("--private-key", type=Path, required=True)
    keygen.add_argument("--public-key", type=Path, required=True)
    sign = commands.add_parser("sign")
    sign.add_argument("--manifest", type=Path, action="append", required=True)
    sign.add_argument("--base-download-url", required=True)
    sign.add_argument("--private-key", type=Path, required=True)
    sign.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "generate-keypair":
        generate_keypair(args.private_key, args.public_key)
    else:
        sign_catalog(args.manifest, args.base_download_url, args.private_key, args.output)


if __name__ == "__main__":
    main()
