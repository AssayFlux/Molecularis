from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse


MAX_MODEL_BYTES = 8 * 1024 * 1024 * 1024
REQUIRED_METADATA = {
    "model_id", "name", "publisher", "version", "license", "license_url",
    "architecture", "quantization", "min_sdk", "min_ram_mb", "capabilities",
    "converter_name", "converter_version",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_adapter_archive(path: Path) -> None:
    if not path.is_file() or path.suffix.lower() != ".zip":
        raise ValueError("Training adapter must be a ZIP archive.")
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if not entries or len(entries) > 10000:
            raise ValueError("Adapter archive has an invalid entry count.")
        total = 0
        for entry in entries:
            member = PurePosixPath(entry.filename)
            mode = (entry.external_attr >> 16) & 0o170000
            if member.is_absolute() or ".." in member.parts or "\\\\" in entry.filename or mode == 0o120000:
                raise ValueError("Adapter archive contains an unsafe path or symbolic link.")
            if entry.file_size > MAX_MODEL_BYTES:
                raise ValueError("Adapter archive contains an oversized entry.")
            total += entry.file_size
            if total > MAX_MODEL_BYTES:
                raise ValueError("Adapter archive expands beyond the 8 GiB limit.")


def package_mobile_export(
    converted_model: Path,
    adapter_archive: Path,
    output_dir: Path,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Package and attest an externally converted LiteRT-LM model; does not convert weights."""
    missing = sorted(REQUIRED_METADATA - metadata.keys())
    if missing:
        raise ValueError("Missing export metadata: " + ", ".join(missing))
    model_id = metadata["model_id"]
    version = metadata["version"]
    if not isinstance(model_id, str) or not model_id or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789._-" for c in model_id):
        raise ValueError("model_id must be a lowercase safe identifier.")
    if not isinstance(version, str) or not version or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._+-" for c in version):
        raise ValueError("version must be a safe version string.")
    license_url = urlparse(str(metadata["license_url"]))
    if license_url.scheme != "https" or not license_url.netloc:
        raise ValueError("license_url must be HTTPS.")
    if not isinstance(metadata["capabilities"], list) or not metadata["capabilities"]:
        raise ValueError("At least one model capability is required.")
    if not converted_model.is_file() or converted_model.suffix.lower() != ".litertlm":
        raise ValueError("The external converter must provide a .litertlm file.")
    if converted_model.stat().st_size <= 0 or converted_model.stat().st_size > MAX_MODEL_BYTES:
        raise ValueError("Converted model is empty or exceeds the 8 GiB limit.")
    validate_adapter_archive(adapter_archive)

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_name = f"{model_id}-{version}.litertlm"
    artifact = output_dir / artifact_name
    shutil.copyfile(converted_model, artifact)
    artifact_sha = sha256_file(artifact)
    adapter_sha = sha256_file(adapter_archive)
    manifest = {
        "schema_version": 1,
        "model_id": model_id,
        "name": metadata["name"],
        "publisher": metadata["publisher"],
        "version": version,
        "license": metadata["license"],
        "license_url": str(metadata["license_url"]),
        "architecture": metadata["architecture"],
        "quantization": metadata["quantization"],
        "min_sdk": int(metadata["min_sdk"]),
        "min_ram_mb": int(metadata["min_ram_mb"]),
        "capabilities": metadata["capabilities"],
        "runtime": "litertlm",
        "format": "litertlm",
        "file_name": artifact_name,
        "size_bytes": artifact.stat().st_size,
        "sha256": artifact_sha,
        "source_adapter_sha256": adapter_sha,
        "converter_name": metadata["converter_name"],
        "converter_version": metadata["converter_version"],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Package and checksum an externally converted Molecularis LiteRT-LM model.")
    parser.add_argument("--converted-model", type=Path, required=True, help="Output .litertlm file from a compatible external converter")
    parser.add_argument("--adapter-zip", type=Path, required=True, help="PEFT adapter ZIP from Molecularis training")
    parser.add_argument("--metadata-json", type=Path, required=True, help="Publisher and compatibility metadata JSON")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    metadata = json.loads(args.metadata_json.read_text(encoding="utf-8"))
    manifest = package_mobile_export(args.converted_model, args.adapter_zip, args.output_dir, metadata)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
