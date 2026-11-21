"""Optional bounded OpenMM CPU molecular-dynamics runner.

The caller must construct a trusted OpenMM System/Topology and provide provenance
for its coordinates, topology, force field and parameter source. This adapter does
not parameterize ligands or proteins and does not validate biological relevance.
"""
from __future__ import annotations

import base64
import json
import re
from hashlib import sha256
from math import isfinite
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


_SHA256 = re.compile(r"^[a-fA-F0-9]{64}$")


def _positive_number(name: str, value: float, *, maximum: float) -> float:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not isfinite(value)
        or not 0.0 < value <= maximum
    ):
        raise ValueError(f"{name} must be finite and in (0, {maximum}]")
    return float(value)


def _derive_openmm_seed(base_seed: int, replica_index: int, stream: str) -> int:
    """Derive a deterministic positive signed-32-bit seed for one replica stream."""
    digest = sha256(
        f"kinetics-openmm-seed-v1:{base_seed}:{replica_index}:{stream}".encode("utf-8")
    ).digest()
    seed = int.from_bytes(digest[:4], "little") & 0x7FFFFFFF
    return seed or 1


def run_openmm_dynamics(
    system: Any,
    topology: Any,
    positions: Any,
    *,
    coordinates_sha256: str,
    topology_sha256: str,
    force_field_name: str,
    force_field_version: str,
    parameter_source_sha256: str,
    temperature_kelvin: float = 300.0,
    pressure_bar: float | None = None,
    timestep_fs: float = 1.0,
    steps: int = 1000,
    equilibration_steps: int = 100,
    replicas: int = 2,
    seed: int = 1,
    report_interval: int = 100,
    cpu_threads: int = 1,
) -> dict[str, object]:
    """Run independent seeded NVT or NPT CPU replicas and return bounded DCD artifacts.

    OpenMM objects must be constructed by trusted caller code; arbitrary XML/system
    deserialization is deliberately not accepted by this boundary.
    """
    for name, value in (
        ("coordinates_sha256", coordinates_sha256),
        ("topology_sha256", topology_sha256),
        ("parameter_source_sha256", parameter_source_sha256),
    ):
        if not isinstance(value, str) or not _SHA256.fullmatch(value):
            raise ValueError(f"{name} must be a 64-character SHA-256 digest")
    if not isinstance(force_field_name, str) or not force_field_name.strip():
        raise ValueError("force_field_name must be non-empty")
    if not isinstance(force_field_version, str) or not force_field_version.strip():
        raise ValueError("force_field_version must be non-empty")
    temperature = _positive_number("temperature_kelvin", temperature_kelvin, maximum=2000.0)
    timestep = _positive_number("timestep_fs", timestep_fs, maximum=4.0)
    pressure: float | None = None
    if pressure_bar is not None:
        pressure = _positive_number("pressure_bar", pressure_bar, maximum=10000.0)
    if not isinstance(steps, int) or isinstance(steps, bool) or not 1 <= steps <= 10_000_000:
        raise ValueError("steps must be an integer between 1 and 10000000")
    if (
        not isinstance(equilibration_steps, int)
        or isinstance(equilibration_steps, bool)
        or not 0 <= equilibration_steps <= 1_000_000
    ):
        raise ValueError("equilibration_steps must be an integer between 0 and 1000000")
    if not isinstance(replicas, int) or isinstance(replicas, bool) or not 2 <= replicas <= 10:
        raise ValueError("replicas must be an integer between 2 and 10")
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")
    if (
        not isinstance(report_interval, int)
        or isinstance(report_interval, bool)
        or not 1 <= report_interval <= steps
    ):
        raise ValueError("report_interval must be an integer between 1 and steps")
    if not isinstance(cpu_threads, int) or isinstance(cpu_threads, bool) or not 1 <= cpu_threads <= 64:
        raise ValueError("cpu_threads must be an integer between 1 and 64")
    frame_count = (steps + report_interval - 1) // report_interval
    if frame_count > 10000:
        raise ValueError("trajectory frame count must not exceed 10000")
    if steps * replicas > 50_000_000:
        raise ValueError("steps times replicas must not exceed 50000000")

    try:
        import numpy as np  # type: ignore[import-not-found]
        import openmm  # type: ignore[import-not-found]
        from openmm import app, unit
        import openmm.openmm as openmm_binary  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "OpenMM is unavailable; install the pinned optional MD engine dependency"
        ) from error

    if not isinstance(system, openmm.System):
        raise ValueError("system must be a constructed OpenMM System")
    if not isinstance(topology, app.Topology):
        raise ValueError("topology must be an OpenMM Topology")
    atom_count = topology.getNumAtoms()
    if atom_count < 1 or atom_count > 50000 or system.getNumParticles() != atom_count:
        raise ValueError("topology and system particle counts must match within 1..50000")
    try:
        xyz = np.asarray(positions.value_in_unit(unit.nanometer), dtype=float)
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("positions must be an OpenMM length Quantity") from error
    if xyz.shape != (atom_count, 3) or not np.isfinite(xyz).all() or np.max(np.abs(xyz)) > 10000:
        raise ValueError("positions must be finite N×3 nanometre coordinates within bounds")
    if pressure is not None and system.usesPeriodicBoundaryConditions() is False:
        raise ValueError("NPT pressure control requires periodic boundary conditions")

    # Clone the caller's System via OpenMM's serializer to avoid mutating it between
    # replicas. The caller does not pass arbitrary XML text into this function.
    system_xml = openmm.XmlSerializer.serialize(system)
    system_bytes = system_xml.encode("utf-8")
    if len(system_bytes) > 256 * 1024 * 1024:
        raise ValueError("serialized OpenMM System exceeds the 256 MiB provenance limit")
    coordinates_canonical_sha256 = sha256(
        np.asarray(xyz, dtype="<f8").tobytes(order="C")
    ).hexdigest()
    atom_manifest = [
        {
            "index": atom.index,
            "name": atom.name,
            "element": atom.element.symbol if atom.element is not None else None,
            "residue_name": atom.residue.name,
            "residue_id": atom.residue.id,
            "chain_id": atom.residue.chain.id,
        }
        for atom in topology.atoms()
    ]
    bond_manifest = sorted(
        [min(bond.atom1.index, bond.atom2.index), max(bond.atom1.index, bond.atom2.index)]
        for bond in topology.bonds()
    )
    box_vectors = system.getDefaultPeriodicBoxVectors()
    box_manifest = [
        [
            float(component.value_in_unit(unit.nanometer))
            if hasattr(component, "value_in_unit")
            else float(component)
            for component in vector
        ]
        for vector in box_vectors
    ]
    topology_manifest = {
        "atoms": atom_manifest,
        "bonds": bond_manifest,
        "default_periodic_box_vectors_nm": box_manifest,
    }
    topology_canonical_sha256 = sha256(
        json.dumps(
            topology_manifest, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    system_sha256 = sha256(system_bytes).hexdigest()
    engine_build = Path(openmm_binary.__file__).read_bytes()
    if not engine_build or len(engine_build) > 512 * 1024 * 1024:
        raise RuntimeError("OpenMM core binary is empty or exceeds the 512 MiB hash limit")
    engine_digest = sha256(engine_build)
    plugin_directory = Path(openmm.Platform.getDefaultPluginsDirectory())
    cpu_plugins = sorted(plugin_directory.glob("*CPU*")) if plugin_directory.is_dir() else []
    for plugin_path in cpu_plugins:
        if plugin_path.is_file():
            plugin_bytes = plugin_path.read_bytes()
            if len(plugin_bytes) > 512 * 1024 * 1024:
                raise RuntimeError("OpenMM CPU plugin exceeds the 512 MiB hash limit")
            engine_digest.update(plugin_path.name.encode("utf-8"))
            engine_digest.update(plugin_bytes)
    engine_build_sha256 = engine_digest.hexdigest()
    protocol = {
        "temperature_kelvin": temperature,
        "pressure_bar": pressure,
        "timestep_fs": timestep,
        "steps": steps,
        "equilibration_steps": equilibration_steps,
        "replicas": replicas,
        "seed": seed,
        "report_interval": report_interval,
        "cpu_threads": cpu_threads,
        "platform": "CPU",
        "integrator": "LangevinMiddleIntegrator",
        "friction_per_ps": 1.0,
        "integrator_seed_derivation": (
            "sha256(kinetics-openmm-seed-v1:base_seed:replica_index:integrator)"
            "[0:4] little-endian masked to 31 bits; zero mapped to 1"
        ),
        "velocity_seed_derivation": (
            "sha256(kinetics-openmm-seed-v1:base_seed:replica_index:velocities)"
            "[0:4] little-endian masked to 31 bits; zero mapped to 1"
        ),
    }
    protocol_sha256 = sha256(
        json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    replica_results: list[dict[str, object]] = []

    with TemporaryDirectory(prefix="kinetics-openmm-") as temporary:
        root = Path(temporary)
        for index in range(replicas):
            replica_seed = _derive_openmm_seed(seed, index + 1, "integrator")
            velocity_seed = _derive_openmm_seed(seed, index + 1, "velocities")
            replica_system = openmm.XmlSerializer.deserialize(system_xml)
            if pressure is not None:
                replica_system.addForce(
                    openmm.MonteCarloBarostat(
                        pressure * unit.bar, temperature * unit.kelvin, 25
                    )
                )
            integrator = openmm.LangevinMiddleIntegrator(
                temperature * unit.kelvin,
                1.0 / unit.picosecond,
                timestep * unit.femtoseconds,
            )
            integrator.setRandomNumberSeed(replica_seed)
            platform = openmm.Platform.getPlatformByName("CPU")
            simulation = app.Simulation(
                topology,
                replica_system,
                integrator,
                platform,
                {"Threads": str(cpu_threads), "DeterministicForces": "true"},
            )
            simulation.context.setPositions(positions)
            simulation.context.setVelocitiesToTemperature(
                temperature * unit.kelvin, velocity_seed
            )
            if equilibration_steps:
                simulation.step(equilibration_steps)
            initial_state = simulation.context.getState(getEnergy=True)
            initial_energy = initial_state.getPotentialEnergy().value_in_unit(
                unit.kilojoule_per_mole
            )
            if not isfinite(initial_energy):
                raise RuntimeError("OpenMM returned a non-finite initial potential energy")
            trajectory_path = root / f"replica-{index + 1}.dcd"
            simulation.reporters.append(
                app.DCDReporter(str(trajectory_path), report_interval)
            )
            simulation.step(steps)
            final_state = simulation.context.getState(getEnergy=True, getPositions=True)
            final_energy = final_state.getPotentialEnergy().value_in_unit(
                unit.kilojoule_per_mole
            )
            final_xyz = np.asarray(
                final_state.getPositions(asNumpy=True).value_in_unit(unit.nanometer),
                dtype=float,
            )
            if (
                not isfinite(final_energy)
                or final_xyz.shape != (atom_count, 3)
                or not np.isfinite(final_xyz).all()
                or np.max(np.abs(final_xyz)) > 10000
            ):
                raise RuntimeError("OpenMM returned non-finite or out-of-bounds final state")
            simulation = None
            integrator = None
            trajectory_bytes = trajectory_path.read_bytes()
            if not trajectory_bytes or len(trajectory_bytes) > 32 * 1024 * 1024:
                raise RuntimeError("DCD trajectory is empty or exceeds the 32 MiB per-replica limit")
            replica_results.append(
                {
                    "replica_id": index + 1,
                    "integrator_seed": replica_seed,
                    "velocity_seed": velocity_seed,
                    "steps_completed": steps,
                    "initial_potential_energy": float(initial_energy),
                    "final_potential_energy": float(final_energy),
                    "energy_unit": "kJ/mol",
                    "trajectory_sha256": sha256(trajectory_bytes).hexdigest(),
                    "trajectory_dcd_base64": base64.b64encode(trajectory_bytes).decode("ascii"),
                }
            )

    return {
        "schema_version": 1,
        "job_type": "molecular_dynamics",
        "research_only": True,
        "validation_status": "not_independently_validated",
        "engine": {
            "engine_id": "OpenMM",
            "version": str(openmm.__version__),
            "build_sha256": engine_build_sha256,
            "platform": "CPU",
        },
        "input_hashes": {
            "coordinates_or_receptor_sha256": coordinates_sha256,
            "ligand_or_topology_sha256": topology_sha256,
            "coordinates_canonical_sha256": coordinates_canonical_sha256,
            "topology_canonical_sha256": topology_canonical_sha256,
        },
        "force_field": {
            "name": force_field_name,
            "version": force_field_version,
            "parameter_source_sha256": parameter_source_sha256,
            "system_sha256": system_sha256,
        },
        "protocol": protocol,
        "protocol_sha256": protocol_sha256,
        "replicas": replica_results,
        "limitations": [
            "Caller must construct and validate the molecular system and topology",
            "No protein/ligand parameterization, protonation or solvent preparation is performed",
            "CPU-only reference execution; GPU plugins and platform-specific licenses are not included",
            "System virtual sites or particles beyond the topology atom count are not accepted",
            "No independent stability, energy-conservation, ensemble or experimental validation is implied",
            "Trajectory and energy outputs are research artifacts, not biological efficacy or clinical predictions",
        ],
    }
