from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from molecularis.docking_vina import run_vina_docking


RECEPTOR = "ATOM      1  C   ALA A   1       0.000   0.000   0.000  1.00  0.00     0.000 C\n"
LIGAND = "ATOM      1  C1  UNL     1       1.000   1.000   1.000  1.00  0.00     0.000 C\n"


class _EnergyRows:
    def tolist(self) -> list[list[float]]:
        return [[-7.5, -7.0, -0.5, 0.0, -0.5]]


class _FakeVina:
    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs

    def set_receptor(self, path: str) -> None:
        assert Path(path).is_file()

    def set_ligand_from_file(self, path: str) -> None:
        assert Path(path).is_file()

    def compute_vina_maps(self, **kwargs: object) -> None:
        assert kwargs["center"] == [0.0, 0.0, 0.0]

    def dock(self, **kwargs: object) -> None:
        assert kwargs["exhaustiveness"] == 8

    def energies(self, **kwargs: object) -> _EnergyRows:
        return _EnergyRows()

    def write_poses(self, path: str, **kwargs: object) -> None:
        Path(path).write_text(
            "MODEL 1\n" + LIGAND + "ENDMDL\n",
            encoding="utf-8",
        )


def _install_fake_vina(monkeypatch: pytest.MonkeyPatch) -> None:
    package = types.ModuleType("vina")
    package.__path__ = []  # type: ignore[attr-defined]
    package.Vina = _FakeVina  # type: ignore[attr-defined]
    package.__version__ = "1.2.7"  # type: ignore[attr-defined]
    wrapper = types.ModuleType("vina.vina_wrapper")
    wrapper.__file__ = __file__  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "vina", package)
    monkeypatch.setitem(sys.modules, "vina.vina_wrapper", wrapper)


def test_vina_runner_returns_hash_bound_research_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_vina(monkeypatch)
    result = run_vina_docking(
        RECEPTOR,
        LIGAND,
        center_angstrom=[0, 0, 0],
        box_size_angstrom=[20, 20, 20],
        n_poses=1,
    )
    assert result["validation_status"] == "not_independently_validated"
    assert result["engine"]["version"] == "1.2.7"  # type: ignore[index]
    assert result["poses"][0]["score"] == -7.5  # type: ignore[index]
    assert len(result["poses"][0]["pose_sha256"]) == 64  # type: ignore[index]
    assert result["input_hashes"]["coordinates_or_receptor_sha256"]  # type: ignore[index]
    schema_path = (
        Path(__file__).resolve().parents[1] / "api" / "insilico-result.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(result)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"center_angstrom": [0, 0]}, "exactly three"),
        ({"box_size_angstrom": [20, 0, 20]}, "greater than 0"),
        ({"seed": -1}, "unsigned 32-bit"),
        ({"exhaustiveness": 0}, "between 1 and 128"),
        ({"n_poses": 21}, "between 1 and 20"),
        ({"cpu": 0}, "between 1 and 32"),
        ({"scoring_function": "ad4"}, "vina.*vinardo"),
    ],
)
def test_vina_runner_rejects_invalid_protocol(
    monkeypatch: pytest.MonkeyPatch,
    kwargs: dict[str, object],
    message: str,
) -> None:
    _install_fake_vina(monkeypatch)
    arguments: dict[str, object] = {
        "center_angstrom": [0, 0, 0],
        "box_size_angstrom": [20, 20, 20],
    }
    arguments.update(kwargs)
    with pytest.raises(ValueError, match=message):
        run_vina_docking(RECEPTOR, LIGAND, **arguments)  # type: ignore[arg-type]


def test_vina_runner_rejects_unbounded_or_invalid_pdbqt() -> None:
    with pytest.raises(ValueError, match="no PDBQT atom"):
        run_vina_docking(
            "REMARK empty\n",
            LIGAND,
            center_angstrom=[0, 0, 0],
            box_size_angstrom=[20, 20, 20],
        )
    with pytest.raises(ValueError, match="NUL"):
        run_vina_docking(
            RECEPTOR + "\x00",
            LIGAND,
            center_angstrom=[0, 0, 0],
            box_size_angstrom=[20, 20, 20],
        )
