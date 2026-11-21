#!/usr/bin/env python3
"""Generate a transparent SPDX 2.3 inventory of declared direct source dependencies.

This is not a resolved/transitive SBOM. Unresolved versions and licenses are explicitly
NOASSERTION; release packaging must additionally resolve and audit every artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tomli as tomllib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPDX_LICENSE = "CC0-1.0"


def generate(root: Path = ROOT) -> dict[str, object]:
    packages: dict[tuple[str, str], dict[str, object]] = {}

    def add(name: str, version: str, ecosystem: str, purl: str | None = None) -> None:
        key = (name.casefold(), version)
        if key in packages:
            return
        item: dict[str, object] = {
            "name": name, "SPDXID": f"SPDXRef-Package-{len(packages) + 1}",
            "versionInfo": version, "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False, "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION", "copyrightText": "NOASSERTION",
            "primaryPackagePurpose": "LIBRARY",
            "comment": f"ecosystem={ecosystem}; declared dependency only",
        }
        if purl:
            item["externalRefs"] = [{
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl", "referenceLocator": purl,
            }]
        packages[key] = item

    gradle_app = (root / "android/app/build.gradle.kts").read_text(encoding="utf-8")
    gradle_root = (root / "android/build.gradle.kts").read_text(encoding="utf-8")
    for source in (gradle_root, gradle_app):
        for group, artifact, version in re.findall(
            r'(?:"|id\()"([A-Za-z0-9_.-]+):([A-Za-z0-9_.-]+):([A-Za-z0-9_.+-]+)(?:"|\))',
            source,
        ):
            add(f"{group}:{artifact}", version, "maven",
                f"pkg:maven/{group}/{artifact}@{version}")
        for plugin, version in re.findall(
            r'id\("([A-Za-z0-9_.-]+)"\) version "([^"]+)"', source,
        ):
            add(plugin, version, "gradle-plugin", f"pkg:generic/{plugin}@{version}")

    bom = re.search(r'compose-bom:([0-9.]+)', gradle_app)
    bom_version = bom.group(1) if bom else "NOASSERTION"
    for group, artifact in re.findall(
        (
            r'(?:implementation|debugImplementation|testImplementation|'
            r'androidTestImplementation)\("([A-Za-z0-9_.-]+):([A-Za-z0-9_.-]+)"\)'
        ),
        gradle_app,
    ):
        add(f"{group}:{artifact}", f"managed-by-compose-bom-{bom_version}", "maven",
            f"pkg:maven/{group}/{artifact}")

    for versioned_name in re.findall(r'install\("([^"]+)"\)', gradle_app):
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^=]+)", versioned_name)
        if match:
            name, version = match.groups()
            add(name, version, "pypi", f"pkg:pypi/{name}@{version}")

    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    for requirement in pyproject.get("build-system", {}).get("requires", []):
        match = re.match(r"([A-Za-z0-9_.-]+)\s*(.*)", requirement)
        if match:
            name, constraint = match.groups()
            add(name, constraint.strip() or "UNPINNED", "pypi", f"pkg:pypi/{name}")

    for line in (root / "requirements-dev.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(("-", "http")):
            continue
        match = re.match(r"([A-Za-z0-9_.-]+)(?:\[[^]]+\])?\s*(.*)", line)
        if match:
            name, constraint = match.groups()
            add(name, constraint.strip() or "UNPINNED", "pypi",
                f"pkg:pypi/{name}")

    validation_dir = root / "validation"
    if validation_dir.is_dir():
        for requirements_file in sorted(validation_dir.glob("requirements-*.txt")):
            for line in requirements_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith(("-", "http")):
                    continue
                match = re.match(
                    r"([A-Za-z0-9_.-]+)(?:\[[^]]+\])?\s*(.*)", line,
                )
                if match:
                    name, constraint = match.groups()
                    version = constraint.strip() or "UNPINNED"
                    if version.startswith("=="):
                        version = version[2:]
                    key = (name.casefold(), version)
                    was_declared_elsewhere = key in packages
                    add(name, version, "pypi", f"pkg:pypi/{name}")
                    if was_declared_elsewhere:
                        packages[key]["comment"] = str(packages[key]["comment"]) + (
                            f"; also used by host-only validation dependency from "
                            f"{requirements_file.relative_to(root)}"
                        )
                    else:
                        packages[key]["comment"] = (
                            f"ecosystem=pypi; host-only validation dependency from "
                            f"{requirements_file.relative_to(root)}; not Android runtime"
                        )

    local_build = (root / "scripts/build_android_local.sh").read_text(encoding="utf-8")
    rust_toolchain = (root / "rust-toolchain.toml").read_text(encoding="utf-8")
    app_build = gradle_app
    def pinned(pattern: str, source: str, label: str) -> str:
        match = re.search(pattern, source)
        if not match:
            raise ValueError(f"Missing pinned toolchain input: {label}")
        return match.group(1)

    gradle_version = pinned(r'GRADLE_VERSION="([^"]+)"', local_build, "Gradle")
    ndk_version = pinned(r'NDK_VERSION="([^"]+)"', local_build, "Android NDK")
    build_tools = pinned(r'BUILD_TOOLS_VERSION="([^"]+)"', local_build, "Android Build Tools")
    python_host = pinned(r'PYTHON_HOST_VERSION="([^"]+)"', local_build, "Python host")
    python_target = pinned(r'PYTHON_TARGET="([^"]+)"', local_build, "Chaquopy Python target")
    rust_version = pinned(r'channel = "([^"]+)"', rust_toolchain, "Rust")
    sdk_platform = pinned(r'compileSdk = ([0-9]+)', app_build, "Android SDK platform")
    cmake_version = pinned(r'version = "([^"]+)"', app_build, "CMake")
    add("Gradle", gradle_version, "build-tool", f"pkg:generic/gradle@{gradle_version}")
    add("Android NDK", ndk_version, "build-tool", f"pkg:generic/android-ndk@{ndk_version}")
    add(
        "Android Build Tools", build_tools, "build-tool",
        f"pkg:generic/android-build-tools@{build_tools}"
    )
    add(
        "Android SDK Platform", sdk_platform, "build-tool",
        f"pkg:generic/android-sdk-platform@{sdk_platform}"
    )
    add("CMake", cmake_version, "build-tool", f"pkg:generic/cmake@{cmake_version}")
    add("Python host", python_host, "build-tool", f"pkg:generic/python@{python_host}")
    add("Chaquopy Python target", python_target, "runtime-target",
        f"pkg:generic/python@{python_target}")
    add("Rust toolchain", rust_version, "build-tool", f"pkg:generic/rust@{rust_version}")
    add("JDK", "17 (patch/vendor not pinned)", "build-tool")

    cargo = root / "android/native-rust/Cargo.toml"
    if cargo.is_file():
        section = ""
        for line in cargo.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                section = stripped
            elif section == "[dependencies]" and "=" in stripped:
                name, value = (part.strip() for part in stripped.split("=", 1))
                version = value.strip('"')
                add(name, version, "cargo", f"pkg:cargo/{name}@{version}")

    ordered = sorted(packages.values(), key=lambda item: str(item["name"]).casefold())
    for index, package in enumerate(ordered, 1):
        package["SPDXID"] = f"SPDXRef-Package-{index}"
    biopython_license = root / "android/app/src/main/assets/third-party/BIOPYTHON-LICENSE.txt"
    extracted_licenses = []
    if biopython_license.is_file():
        biopython_package = next(
            (item for item in ordered if str(item["name"]).casefold() == "biopython"), None
        )
        if biopython_package is not None:
            biopython_package["licenseDeclared"] = "LicenseRef-Biopython-License-Agreement"
            biopython_package["sourceInfo"] = (
                "Built from Biopython Git commit d7e4b8b19399668b09442a5b35765d9186b5f665"
            )
            extracted_licenses.append({
                "licenseId": "LicenseRef-Biopython-License-Agreement",
                "name": "Biopython License Agreement",
                "extractedText": biopython_license.read_text(encoding="utf-8"),
                "comment": (
                    "Biopython 1.88 LICENSE states this is the default license unless "
                    "individual file headers say otherwise; some files are dual licensed."
                ),
            })
    identity = "\n".join(
        f"{item['name']}@{item['versionInfo']}" for item in ordered
    )
    namespace_hash = hashlib.sha256(identity.encode()).hexdigest()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "spdxVersion": "SPDX-2.3", "dataLicense": SPDX_LICENSE,
        "SPDXID": "SPDXRef-DOCUMENT", "name": "Kinetics declared direct dependencies",
        "documentNamespace": f"https://assayflux.github.io/Kinetics/sbom/{namespace_hash}",
        "creationInfo": {
            "creators": ["Tool: kinetics-source-sbom-generator"],
            "created": now,
            "comment": (
                "Static declared-dependency inventory; not a resolved transitive "
                "release SBOM."
            ),
        },
        "packages": ordered,
        "hasExtractedLicensingInfos": extracted_licenses,
        "relationships": [{
            "spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES",
            "relatedSpdxElement": item["SPDXID"],
        } for item in ordered],
        "annotations": [{
            "annotationDate": now, "annotationType": "OTHER",
            "annotator": "Tool: kinetics-source-sbom-generator",
            "comment": (
                "Direct declarations only. Gradle BOM-managed modules are not resolved here. "
                "Transitive artifacts, exact resolved versions, checksums, file-level licenses "
                "and native binary contents are not included. Do not use this as the "
                    "final release SBOM."
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
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote declared-dependency SPDX inventory: {args.output}")
    print("WARNING: this is not a resolved transitive release SBOM.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
