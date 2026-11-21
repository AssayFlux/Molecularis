#!/usr/bin/env python3
"""Static guardrails for the Android build and user-initiated public-reference network boundary."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def validate_android_config(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "android/app/src/main/AndroidManifest.xml"
    gradle_path = root / "android/app/build.gradle.kts"
    cmake_path = root / "android/app/src/main/cpp/CMakeLists.txt"
    workflow_path = root / ".github/workflows/ci.yml"
    try:
        manifest = ET.parse(manifest_path).getroot()
    except (OSError, ET.ParseError) as exc:
        return [f"Android manifest could not be parsed: {exc}"]

    permissions = {
        node.get(ANDROID_NS + "name", "")
        for node in manifest.findall("uses-permission")
    }
    if "android.permission.INTERNET" not in permissions:
        errors.append("public reference retrieval requires the INTERNET permission")
    unexpected_permissions = permissions - {"android.permission.INTERNET"}
    if unexpected_permissions:
        errors.append(
            "unexpected Android permissions are not approved: "
            f"{sorted(unexpected_permissions)}"
        )
    application = manifest.find("application")
    if application is None:
        errors.append("Android manifest is missing application")
    else:
        if application.get(ANDROID_NS + "allowBackup") != "false":
            errors.append("application must disable Android backup")
        if application.get(ANDROID_NS + "usesCleartextTraffic") != "false":
            errors.append("application must disable cleartext traffic")

    try:
        gradle = gradle_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Android Gradle config could not be read: {exc}")
        gradle = ""
    required_gradle = {
        'srcDir("../../python")': (
            "Chaquopy must package the repository's Molecularis Python modules"
        ),
        'minSdk = 29': "Android minimum SDK must remain API 29",
        'targetSdk = 36': "Android target SDK must remain explicitly pinned to API 36",
        'ndkVersion = "28.2.13676358"': "Android NDK version must match the local build script",
        'abiFilters += "arm64-v8a"': "Android ABI must remain arm64-v8a only",
        'useLegacyPackaging = false': "JNI libraries must use modern uncompressed packaging",
    }
    for marker, message in required_gradle.items():
        if marker not in gradle:
            errors.append(message)

    wrapper_properties = root / "android/gradle/wrapper/gradle-wrapper.properties"
    try:
        wrapper = wrapper_properties.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Gradle wrapper properties could not be read: {exc}")
        wrapper = ""
    if "gradle-8.13-bin.zip" not in wrapper:
        errors.append("Gradle wrapper distribution must be pinned to 8.13")
    gradle_sha256 = (
        "distributionSha256Sum=20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78"
    )
    if gradle_sha256 not in wrapper:
        errors.append("Gradle wrapper must verify the official Gradle 8.13 SHA-256")
    local_build = root / "scripts/build_android_local.sh"
    try:
        build_source = local_build.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Local Android build script could not be read: {exc}")
        build_source = ""
    for marker in (
        'CHAQUOPY_COMMIT="1f63c93d8beaf7062fbe51888ab9235475df3bb8"',
        'BIOPYTHON_COMMIT="d7e4b8b19399668b09442a5b35765d9186b5f665"',
        'GRADLE_SHA256="20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78"',
        'NDK_VERSION="28.2.13676358"',
        'PYTHON_TARGET="3.11.17-0"',
    ):
        if marker not in build_source:
            errors.append(f"Local build inputs must remain pinned: {marker}")

    rust_toolchain = root / "rust-toolchain.toml"
    cargo_lock = root / "android/native-rust/Cargo.lock"
    rust_channel = 'channel = "1.88.0"'
    if not rust_toolchain.is_file() or rust_channel not in rust_toolchain.read_text(encoding="utf-8"):
        errors.append("Native Rust toolchain must be pinned to 1.88.0")
    if not cargo_lock.is_file():
        errors.append("Native Rust Cargo.lock is required for --locked builds")

    manifest_path = root / "android/app/src/main/AndroidManifest.xml"
    try:
        manifest_text = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Android manifest could not be read: {exc}")
        manifest_text = ""
    if 'android:allowBackup="false"' not in manifest_text:
        errors.append("Android backup must remain disabled for local research data")
    if 'android:usesCleartextTraffic="false"' not in manifest_text:
        errors.append("Android cleartext traffic must remain disabled")
    if "android.permission.INTERNET" not in manifest_text:
        errors.append(
            "Android manifest must declare INTERNET for explicit public-reference retrieval"
        )
    client_path = (
        root / "android/app/src/main/java/org/assayflux/molecularis/PublicDatabaseClient.kt"
    )
    card_path = root / "android/app/src/main/java/org/assayflux/molecularis/PublicDatabaseCard.kt"
    try:
        client_source = client_path.read_text(encoding="utf-8")
        card_source = card_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Public database boundary source could not be read: {exc}")
        client_source = ""
        card_source = ""
    for marker in (
        '"eutils.ncbi.nlm.nih.gov"',
        '"rest.uniprot.org"',
        '"files.rcsb.org"',
        'url.protocol == "https"',
        'url.host in ALLOWED_HOSTS',
        'instanceFollowRedirects = false',
        'requestMethod = "GET"',
        'CONNECT_TIMEOUT_MS',
        'READ_TIMEOUT_MS',
        'MAX_STRUCTURE_BYTES',
    ):
        if marker not in client_source:
            errors.append(
                "Public database client must retain its HTTPS/host/size boundary: "
                f"{marker}"
            )
    if "never submit patient sequences" not in client_source:
        errors.append(
            "Public database client must explicitly prohibit private patient-data submission"
        )
    if "Imported patient data is never uploaded" not in card_source:
        errors.append(
            "Public database UI must disclose that imported patient data is never uploaded"
        )

    package_init = root / "python/molecularis/__init__.py"
    runtime_probe = root / "android/app/src/main/python/molecularis_probe.py"
    if not package_init.is_file():
        errors.append("Repository Molecularis Python package is missing")
    try:
        probe_source = runtime_probe.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Embedded Python runtime probe could not be read: {exc}")
        probe_source = ""
    if "import molecularis" not in probe_source:
        errors.append("Embedded Python runtime probe must import the packaged Molecularis module")

    try:
        cmake = cmake_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Native CMake config could not be read: {exc}")
        cmake = ""
    if "-Wl,-z,max-page-size=16384" not in cmake:
        errors.append("Native linker must request 16 KB maximum page alignment")

    try:
        workflow = workflow_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"GitHub workflow could not be read: {exc}")
        workflow = ""
    for marker, message in (
        (
            "android-arm64-build:",
            "GitHub Actions must include the authorized arm64 APK/AAB build job",
        ),
        (
            "scripts/build_android_local.sh",
            "Android CI must use the pinned repository build script",
        ),
        (":app:testDebugUnitTest", "Android CI must run the JVM unit-test task"),
        (
            "actions/upload-artifact@v4",
            "Android CI must retain APK/AAB build evidence as artifacts",
        ),
    ):
        if marker not in workflow:
            errors.append(message)
    if "workflow_dispatch:" not in workflow:
        errors.append("Android CI must retain its manual-dispatch entry point")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_android_config(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Android build and public-reference network boundary guardrails are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
