from __future__ import annotations

from pathlib import Path

from scripts.generate_source_sbom import generate


def test_source_sbom_tracks_current_molecularis_dependencies() -> None:
    root = Path(__file__).resolve().parents[1]
    document = generate(root)
    packages = {package["name"].casefold(): package for package in document["packages"]}

    for name in ("numpy", "scipy", "rdkit", "biopython", "ruff", "pytest"):
        assert name in packages

    assert document["spdxVersion"] == "SPDX-2.3"
    assert document["name"] == "molecularis-workbench declared source dependencies"
    assert "Molecularis/sbom/" in document["documentNamespace"]
    assert all("android" not in package["name"].casefold() for package in packages.values())
    assert all("gradle" not in package["name"].casefold() for package in packages.values())
    assert any(
        "validation/requirements-scipy.txt" in package["comment"]
        for package in packages.values() if package["name"].casefold() == "numpy"
    )


def test_source_sbom_does_not_require_retired_platform_files(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "molecularis-test"\n'
        '[project.optional-dependencies]\ndev = ["pytest==8.0"]\n',
        encoding="utf-8",
    )
    (tmp_path / "requirements-dev.txt").write_text("ruff==0.6\n", encoding="utf-8")
    document = generate(tmp_path)
    assert {item["name"] for item in document["packages"]} == {"pytest", "ruff"}
