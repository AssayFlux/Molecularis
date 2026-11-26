#!/usr/bin/env python3
"""Generate an SPDX 2.3 inventory of installed Python and native OS packages.

This is an environment inventory, not a signed provenance attestation. License
metadata remains NOASSERTION; package origin, publisher, and binary hashes are
not inferred from installation metadata.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib import metadata
import json
import platform
import re
from pathlib import Path
import shutil
import subprocess
import uuid
from urllib.parse import quote


def _normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _spdx_id(prefix: str, identity: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9.-]", "-", identity)
    suffix = str(uuid.uuid5(uuid.NAMESPACE_URL, identity))[:8]
    return f"SPDXRef-{prefix}-{safe}-{suffix}"


def _python_packages() -> tuple[list[dict], list[dict]]:
    installed: dict[str, dict] = {}
    for dist in metadata.distributions():
        name = dist.metadata.get("Name")
        version = dist.version
        if not name or not version:
            continue
        normalized = _normalize(name)
        installed[normalized] = {
            "name": name,
            "version": version,
            "requirements": tuple(dist.requires or ()),
            "direct_url": dist.read_text("direct_url.json"),
            "license": dist.metadata.get("License"),
            "license_expression": dist.metadata.get("License-Expression"),
            "classifiers": tuple(dist.metadata.get_all("Classifier") or ()),
        }

    package_ids = {
        key: _spdx_id("Python", key + "@" + value["version"])
        for key, value in installed.items()
    }
    packages: list[dict] = []
    relationships: list[dict] = []
    for key, value in sorted(installed.items()):
        name, version = value["name"], value["version"]
        package = {
            "name": name,
            "SPDXID": package_ids[key],
            "versionInfo": version,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "packageComment": (
                "License metadata hints are recorded as sourceInfo only; "
                "they have not been validated as SPDX expressions or legally reviewed."
            ),
            "sourceInfo": (
                "Installed Python distribution; origin, publisher, binary hashes "
                "and license compliance are not attested. "
                f"Metadata License={value['license']!r}; "
                f"License-Expression={value['license_expression']!r}; "
                f"Classifiers={list(value['classifiers'])!r}."
            ),
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:pypi/{_normalize(name)}@{version}",
            }],
        }
        if value["direct_url"]:
            try:
                direct = json.loads(value["direct_url"])
                hashes = direct.get("archive_info", {}).get("hashes", {})
                sha256 = hashes.get("sha256")
                if isinstance(sha256, str) and re.fullmatch(r"[a-f0-9]{64}", sha256):
                    package["checksums"] = [{"algorithm": "SHA256", "checksumValue": sha256}]
                package["sourceInfo"] += " Direct installation metadata is present; it is not publisher attestation."
            except (TypeError, ValueError):
                package["sourceInfo"] += " direct_url.json was malformed."
        packages.append(package)
        relationships.append({
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": package_ids[key],
        })

    for key, value in sorted(installed.items()):
        for requirement in value["requirements"]:
            match = re.match(r"\s*([A-Za-z0-9_.-]+)", requirement)
            if not match:
                continue
            dependency = _normalize(match.group(1))
            if dependency in package_ids:
                relationships.append({
                    "spdxElementId": package_ids[key],
                    "relationshipType": "DEPENDS_ON",
                    "relatedSpdxElement": package_ids[dependency],
                })
    return packages, relationships


def _native_packages() -> tuple[list[dict], list[dict]]:
    """Collect dpkg/rpm package names and versions without invoking package scripts."""
    command: list[str] | None = None
    manager = ""
    if shutil.which("dpkg-query"):
        command = ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\n"]
        manager = "deb"
    elif shutil.which("rpm"):
        command = ["rpm", "-qa", "--qf", "%{NAME}\t%{VERSION}-%{RELEASE}\n"]
        manager = "rpm"
    if command is None:
        return [], []

    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, timeout=30,
            stdin=subprocess.DEVNULL, env={"PATH": "/usr/bin:/bin", "LANG": "C"},
        )
    except (OSError, subprocess.SubprocessError):
        return [], []

    packages: list[dict] = []
    relationships: list[dict] = []
    for line in result.stdout.splitlines():
        fields = line.split("\t", 1)
        if len(fields) != 2 or not all(fields):
            continue
        name, version = fields
        identity = f"{manager}:{name}@{version}"
        package_id = _spdx_id("Native", identity)
        native_name = quote(name, safe=".-_")
        native_version = quote(version, safe=".-_+~")
        packages.append({
            "name": name,
            "SPDXID": package_id,
            "versionInfo": version,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "sourceInfo": (
                f"Installed host package inventoried via {manager} database; "
                "repository origin, publisher, file hashes and license compliance "
                "are not attested."
            ),
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:{manager}/{native_name}@{native_version}",
            }],
        })
        relationships.append({
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": package_id,
        })
    return packages, relationships


def build_environment_sbom() -> dict:
    python_packages, python_relationships = _python_packages()
    native_packages, native_relationships = _native_packages()
    packages = python_packages + native_packages
    identity = "\n".join(sorted(
        f"{package['SPDXID']}=={package['versionInfo']}" for package in packages
    ))
    namespace_id = uuid.uuid5(uuid.NAMESPACE_URL, identity)
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    os_release = platform.platform()
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "Molecularis Installed Python and Native Environment",
        "documentNamespace": f"https://molecularis.dev/sbom/environment/{namespace_id}",
        "creationInfo": {
            "created": created,
            "creators": ["Tool: Molecularis environment SBOM generator"],
            "comment": (
                f"Host platform: {os_release}. Includes installed Python distributions "
                "and dpkg/rpm packages when available. No license, origin, publisher, "
                "or binary-integrity attestation is implied."
            ),
        },
        "packages": packages,
        "relationships": python_relationships + native_relationships,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("environment.spdx.json"))
    args = parser.parse_args()
    document = build_environment_sbom()
    args.output.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if document["spdxVersion"] != "SPDX-2.3" or not document["packages"]:
        raise SystemExit("SBOM generation failed: empty or invalid SPDX document")
    print(
        "Wrote SPDX 2.3 environment inventory: "
        f"{len(document['packages'])} packages "
        f"({sum(p['SPDXID'].startswith('SPDXRef-Python-') for p in document['packages'])} Python, "
        f"{sum(p['SPDXID'].startswith('SPDXRef-Native-') for p in document['packages'])} native)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
