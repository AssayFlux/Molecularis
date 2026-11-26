from __future__ import annotations

import runpy


def test_environment_sbom_describes_python_and_native_packages():
    module = runpy.run_path("scripts/generate_environment_sbom.py")
    document = module["build_environment_sbom"]()
    assert document["spdxVersion"] == "SPDX-2.3"
    assert document["packages"]
    package_ids = {package["SPDXID"] for package in document["packages"]}
    assert len(package_ids) == len(document["packages"])
    assert all(package["licenseDeclared"] == "NOASSERTION" for package in document["packages"])
    assert all(package["licenseConcluded"] == "NOASSERTION" for package in document["packages"])
    assert any(package["SPDXID"].startswith("SPDXRef-Python-") for package in document["packages"])
    for relationship in document["relationships"]:
        assert relationship["spdxElementId"] == "SPDXRef-DOCUMENT" or (
            relationship["spdxElementId"] in package_ids
        )
        assert relationship["relatedSpdxElement"] in package_ids


def test_environment_sbom_records_license_metadata_without_claiming_review():
    module = runpy.run_path("scripts/generate_environment_sbom.py")
    packages, _ = module["_python_packages"]()
    assert packages
    assert all(package["licenseDeclared"] == "NOASSERTION" for package in packages)
    assert all("not been validated" in package["packageComment"] for package in packages)
