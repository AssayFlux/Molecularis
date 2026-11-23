#!/usr/bin/env python3
"""Generate an SPDX 2.3 inventory of the active Python environment.

This records installed distributions and declared Requires-Dist edges. It does
not attest package hashes, licenses, publisher identity or native system libraries.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib import metadata
import json
import re
from pathlib import Path
import uuid


def _normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def build_environment_sbom() -> dict:
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
        }

    package_ids = {
        key: "SPDXRef-Package-" + re.sub(r"[^A-Za-z0-9.-]", "-", key) + "-"
             + str(uuid.uuid5(uuid.NAMESPACE_URL, key + "@" + value["version"]))[:8]
        for key, value in installed.items()
    }
    packages = []
    relationships = []
    for key, value in sorted(installed.items()):
        name, version = value["name"], value["version"]
        purl_name = _normalize(name)
        packages.append({
            "name": name,
            "SPDXID": package_ids[key],
            "versionInfo": version,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "sourceInfo": "Installed Python distribution inventory; license, origin and hashes are not attested.",
            "externalRefs": [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:pypi/{purl_name}@{version}",
            }],
        })
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

    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    identity = "\n".join(
        f"{key}=={value['version']}" for key, value in sorted(installed.items())
    )
    namespace_id = uuid.uuid5(uuid.NAMESPACE_URL, identity)
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": "Molecularis Installed Python Environment",
        "documentNamespace": f"https://molecularis.dev/sbom/python-environment/{namespace_id}",
        "creationInfo": {
            "created": created,
            "creators": ["Tool: Molecularis environment SBOM generator"],
            "comment": "Installed Python distribution inventory; not a complete OS/native dependency SBOM or license/security attestation.",
        },
        "packages": packages,
        "relationships": relationships,
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
    print(f"Wrote SPDX 2.3 environment inventory: {len(document['packages'])} packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
