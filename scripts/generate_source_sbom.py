#!/usr/bin/env python3
"""Generate a declared-dependency SPDX 2.3 inventory for Molecularis.

This source inventory is not a resolved/transitive release SBOM. Exact resolved
artifacts, hashes, file-level licenses and native binaries require release scanning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
SPDX_LICENSE = "CC0-1.0"
_REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[[^]]+\])?\s*(.*)$")


def generate(root: Path = ROOT) -> dict[str, object]:
    packages: dict[tuple[str, str], dict[str, object]] = {}

    def add(name: str, version: str, ecosystem: str, source: str,
            purl: str | None = None) -> None:
        key = (name.casefold(), version)
        if key in packages:
            item = packages[key]
            comment = str(item["comment"])
            if source not in comment:
                item["comment"] = f"{comment}; also declared by {source}"
            return
        item: dict[str, object] = {
            "name": name,
            "SPDXID": f"SPDXRef-Package-{len(packages) + 1}",
            "versionInfo": version or "UNPINNED",
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION",
            "primaryPackagePurpose": "LIBRARY",
            "comment": f"ecosystem={ecosystem}; declared dependency from {source}",
        }
        if purl:
            item["externalRefs"] = [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": purl,
            }]
        packages[key] = item

    pyproject_path = root / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    for requirement in pyproject.get("build-system", {}).get("requires", []):
        match = _REQUIREMENT.match(requirement)
        if match:
            name, constraint = match.groups()
            add(name, constraint.strip() or "UNPINNED", "pypi", "pyproject build-system",
                f"pkg:pypi/{name}")

    project = pyproject.get("project", {})
    optional = project.get("optional-dependencies", {})
    for group, requirements in optional.items():
        for requirement in requirements:
            match = _REQUIREMENT.match(requirement)
            if match:
                name, constraint = match.groups()
                add(name, constraint.strip() or "UNPINNED", "pypi",
                    f"pyproject optional-dependencies.{group}", f"pkg:pypi/{name}")

    requirements_files = [root / "requirements-dev.txt"]
    validation_dir = root / "validation"
    if validation_dir.is_dir():
        requirements_files.extend(sorted(validation_dir.glob("requirements-*.txt")))
    for requirements_file in requirements_files:
        if not requirements_file.is_file():
            continue
        source = requirements_file.relative_to(root).as_posix()
        for line in requirements_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "-", "http")):
                continue
            match = _REQUIREMENT.match(line)
            if not match:
                continue
            name, constraint = match.groups()
            version = constraint.strip() or "UNPINNED"
            add(name, version, "pypi", source, f"pkg:pypi/{name}")

    ordered = sorted(packages.values(), key=lambda item: str(item["name"]).casefold())
    for index, package in enumerate(ordered, 1):
        package["SPDXID"] = f"SPDXRef-Package-{index}"

    identity = "\n".join(
        f"{item['name']}@{item['versionInfo']}" for item in ordered
    )
    namespace_hash = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    project_name = str(project.get("name", "molecularis"))
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": SPDX_LICENSE,
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"{project_name} declared source dependencies",
        "documentNamespace": f"https://assayflux.github.io/Molecularis/sbom/{namespace_hash}",
        "creationInfo": {
            "creators": ["Tool: molecularis-source-sbom-generator"],
            "created": now,
            "comment": (
                "Declared direct and optional dependencies only. This is not a resolved "
                "transitive release SBOM."
            ),
        },
        "packages": ordered,
        "hasExtractedLicensingInfos": [],
        "relationships": [{
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": item["SPDXID"],
        } for item in ordered],
        "annotations": [{
            "annotationDate": now,
            "annotationType": "OTHER",
            "annotator": "Tool: molecularis-source-sbom-generator",
            "comment": (
                "No Android, Gradle, Rust or other retired platform toolchain is inferred. "
                "Transitive artifacts, resolved versions, checksums, file-level licenses "
                "and native binary contents are not included; do not use as final release SBOM."
            ),
        }],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "sbom/source-dependencies.spdx.json")
    args = parser.parse_args()
    document = generate(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Wrote declared-dependency SPDX inventory: {args.output}")
    print("WARNING: this is not a resolved transitive release SBOM.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
