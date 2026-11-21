"""Optional, bounded AutoDock Vina runner for prepared PDBQT inputs.

This adapter runs docking only on an explicitly configured host. It does not prepare
chemistry, validate biological relevance, estimate binding affinity or replace
independent redocking/cross-docking benchmarks.
"""
from __future__ import annotations

import json
from hashlib import sha256
from math import isfinite
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


def _pdbqt_bytes(value: str, *, label: str, maximum: int) -> bytes:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty PDBQT text")
    try:
        encoded = value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as error:
        raise ValueError(f"{label} contains invalid Unicode") from error
    if len(encoded) > maximum:
        raise ValueError(f"{label} exceeds the {maximum}-byte limit")
    if b"\x00" in encoded:
        raise ValueError(f"{label} must not contain NUL bytes")
    if not any(line.startswith(("ATOM  ", "HETATM")) for line in value.splitlines()):
        raise ValueError(f"{label} contains no PDBQT atom records")
    return encoded


def _vector3(name: str, values: list[float], *, positive: bool) -> tuple[float, float, float]:
    if not isinstance(values, (list, tuple)) or len(values) != 3:
        raise ValueError(f"{name} must contain exactly three numbers")
    parsed: list[float] = []
    for value in values:
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not isfinite(value)
        ):
            raise ValueError(f"{name} values must be finite numbers")
        number = float(value)
        if positive and not 0.0 < number <= 126.0:
            raise ValueError(f"{name} dimensions must be greater than 0 and at most 126 Å")
        if not positive and abs(number) > 10000.0:
            raise ValueError(f"{name} coordinates exceed the 10000 Å safety bound")
        parsed.append(number)
    return (parsed[0], parsed[1], parsed[2])


def run_vina_docking(
    receptor_pdbqt: str,
    ligand_pdbqt: str,
    *,
    center_angstrom: list[float],
    box_size_angstrom: list[float],
    seed: int = 1,
    exhaustiveness: int = 8,
    n_poses: int = 9,
    cpu: int = 1,
    scoring_function: str = "vina",
    energy_range_kcal_per_mol: float = 3.0,
) -> dict[str, object]:
    """Run bounded Vina/Vinardo docking on caller-prepared receptor and ligand PDBQT.

    The score and energy components are engine outputs, not experimental free
    energies, binding affinities, activity or efficacy predictions.
    """
    receptor_bytes = _pdbqt_bytes(
        receptor_pdbqt, label="receptor_pdbqt", maximum=16 * 1024 * 1024
    )
    ligand_bytes = _pdbqt_bytes(
        ligand_pdbqt, label="ligand_pdbqt", maximum=2 * 1024 * 1024
    )
    center = _vector3("center_angstrom", center_angstrom, positive=False)
    box_size = _vector3("box_size_angstrom", box_size_angstrom, positive=True)
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")
    if (
        not isinstance(exhaustiveness, int)
        or isinstance(exhaustiveness, bool)
        or not 1 <= exhaustiveness <= 128
    ):
        raise ValueError("exhaustiveness must be an integer between 1 and 128")
    if not isinstance(n_poses, int) or isinstance(n_poses, bool) or not 1 <= n_poses <= 20:
        raise ValueError("n_poses must be an integer between 1 and 20")
    if not isinstance(cpu, int) or isinstance(cpu, bool) or not 1 <= cpu <= 32:
        raise ValueError("cpu must be an integer between 1 and 32")
    if scoring_function not in {"vina", "vinardo"}:
        raise ValueError("scoring_function must be 'vina' or 'vinardo'")
    if (
        not isinstance(energy_range_kcal_per_mol, (int, float))
        or isinstance(energy_range_kcal_per_mol, bool)
        or not isfinite(energy_range_kcal_per_mol)
        or not 0.0 < energy_range_kcal_per_mol <= 100.0
    ):
        raise ValueError("energy_range_kcal_per_mol must be finite and in (0, 100]")

    try:
        from vina import Vina, __version__ as vina_version  # type: ignore[import-not-found]
        import vina.vina_wrapper as vina_wrapper  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "AutoDock Vina is unavailable; install the pinned optional docking dependency"
        ) from error

    with TemporaryDirectory(prefix="kinetics-vina-") as temporary:
        root = Path(temporary)
        receptor_path = root / "receptor.pdbqt"
        ligand_path = root / "ligand.pdbqt"
        poses_path = root / "poses.pdbqt"
        receptor_path.write_bytes(receptor_bytes)
        ligand_path.write_bytes(ligand_bytes)

        engine: Any = Vina(
            sf_name=scoring_function,
            cpu=cpu,
            seed=seed,
            verbosity=0,
        )
        engine.set_receptor(str(receptor_path))
        engine.set_ligand_from_file(str(ligand_path))
        engine.compute_vina_maps(center=list(center), box_size=list(box_size))
        engine.dock(exhaustiveness=exhaustiveness, n_poses=n_poses)
        energies = engine.energies(n_poses=n_poses, energy_range=float(energy_range_kcal_per_mol))
        engine.write_poses(
            str(poses_path),
            n_poses=n_poses,
            energy_range=float(energy_range_kcal_per_mol),
            overwrite=True,
        )
        if not poses_path.is_file():
            raise RuntimeError("Vina completed without writing the pose file")
        pose_bytes = poses_path.read_bytes()
        if not pose_bytes or len(pose_bytes) > 16 * 1024 * 1024:
            raise RuntimeError("Vina pose output is empty or exceeds the 16 MiB result limit")
        energy_rows = [
            [float(component) for component in row]
            for row in energies.tolist()
        ]
        pose_text = pose_bytes.decode("utf-8", errors="strict")
        pose_blocks: list[str] = []
        current: list[str] = []
        for line in pose_text.splitlines(keepends=True):
            if line.startswith("MODEL"):
                if current:
                    pose_blocks.append("".join(current))
                current = [line]
            elif current:
                current.append(line)
                if line.startswith("ENDMDL"):
                    pose_blocks.append("".join(current))
                    current = []
        if current:
            pose_blocks.append("".join(current))
        if not pose_blocks:
            pose_blocks = [pose_text]
        if len(pose_blocks) != len(energy_rows):
            raise RuntimeError("Vina pose count does not match its energy rows")
        protocol = {
            "center_angstrom": list(center),
            "box_size_angstrom": list(box_size),
            "seed": seed,
            "exhaustiveness": exhaustiveness,
            "n_poses_requested": n_poses,
            "cpu": cpu,
            "scoring_function": scoring_function,
            "energy_range_kcal_per_mol": float(energy_range_kcal_per_mol),
        }
        protocol_sha256 = sha256(
            json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        engine_binary = Path(vina_wrapper.__file__).read_bytes()
        if not engine_binary or len(engine_binary) > 512 * 1024 * 1024:
            raise RuntimeError("Vina engine binary is empty or exceeds the 512 MiB hash limit")
        engine_build_sha256 = sha256(engine_binary).hexdigest()
        pose_results = [
            {
                "rank": index + 1,
                "score": energy[0],
                "score_unit": "kcal/mol (Vina score; not measured binding free energy)",
                "pose_sha256": sha256(block.encode("utf-8")).hexdigest(),
                "pose_pdbqt": block,
            }
            for index, (energy, block) in enumerate(zip(energy_rows, pose_blocks, strict=True))
        ]

    return {
        "schema_version": 1,
        "job_type": "docking",
        "research_only": True,
        "validation_status": "not_independently_validated",
        "engine": {
            "engine_id": "AutoDock Vina",
            "version": str(vina_version),
            "build_sha256": engine_build_sha256,
            "scoring_function": scoring_function,
        },
        "input_hashes": {
            "coordinates_or_receptor_sha256": sha256(receptor_bytes).hexdigest(),
            "ligand_or_topology_sha256": sha256(ligand_bytes).hexdigest(),
        },
        "protocol": protocol,
        "protocol_sha256": protocol_sha256,
        "poses": pose_results,
        "limitations": [
            "Requires caller-prepared PDBQT; ligand and receptor preparation are not performed",
            "Scores are engine outputs, not experimental binding free energies or binding affinities",
            "No redocking, cross-docking, decoy enrichment or prospective validation is performed",
            "No biological activity, efficacy, safety, ADMET or clinical prediction is produced",
            "Use only licensed structures and approved research compute",
        ],
    }
