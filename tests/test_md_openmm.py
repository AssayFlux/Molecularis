from __future__ import annotations

import pytest

from molecularis.md_openmm import _derive_openmm_seed, run_openmm_dynamics


def _arguments() -> dict[str, object]:
    return {
        "coordinates_sha256": "a" * 64,
        "topology_sha256": "b" * 64,
        "force_field_name": "synthetic",
        "force_field_version": "1",
        "parameter_source_sha256": "c" * 64,
        "temperature_kelvin": 300.0,
        "timestep_fs": 1.0,
        "steps": 100,
        "equilibration_steps": 10,
        "replicas": 2,
        "seed": 1,
        "report_interval": 10,
    }


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("coordinates_sha256", "bad", "SHA-256"),
        ("timestep_fs", 5.0, "timestep_fs"),
        ("temperature_kelvin", 0.0, "temperature_kelvin"),
        ("steps", 0, "steps"),
        ("replicas", 1, "replicas"),
        ("seed", 2**32, "seed"),
        ("report_interval", 101, "report_interval"),
        ("cpu_threads", 0, "cpu_threads"),
        ("pressure_bar", 0.0, "pressure_bar"),
    ],
)
def test_openmm_runner_rejects_invalid_protocol_before_loading_engine(
    key: str, value: object, message: str
) -> None:
    arguments = _arguments()
    arguments[key] = value
    with pytest.raises(ValueError, match=message):
        run_openmm_dynamics(object(), object(), object(), **arguments)  # type: ignore[arg-type]


def test_openmm_seed_derivation_is_stable_distinct_and_signed_32_bit() -> None:
    seeds = [
        _derive_openmm_seed(base_seed, replica_index, stream)
        for base_seed in (0, 1, 2**32 - 1)
        for replica_index in range(1, 11)
        for stream in ("integrator", "velocities")
    ]
    assert all(1 <= seed <= 2**31 - 1 for seed in seeds)
    assert len(seeds) == len(set(seeds))
    assert _derive_openmm_seed(2**32 - 1, 10, "integrator") == _derive_openmm_seed(
        2**32 - 1, 10, "integrator"
    )
