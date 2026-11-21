#!/usr/bin/env python3
"""Private Node-worker entry point for one owner-authorized Vina research job."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from molecularis.docking_vina import run_vina_docking


ROOT = Path(__file__).resolve().parents[1]
MAX_REQUEST_BYTES = 20 * 1024 * 1024


def main() -> int:
    raw = sys.stdin.buffer.read(MAX_REQUEST_BYTES + 1)
    if len(raw) > MAX_REQUEST_BYTES:
        raise ValueError("request exceeds the 20 MiB worker limit")
    request = json.loads(raw.decode("utf-8", errors="strict"))
    request_schema = json.loads(
        (ROOT / "api" / "docking-execution.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(request_schema).validate(request)
    if request["execution_authorized"] is not True or request["owner_approval"] is not True:
        raise ValueError("explicit owner authorization is required")

    result = run_vina_docking(
        request["receptor_pdbqt"],
        request["ligand_pdbqt"],
        center_angstrom=request["center_angstrom"],
        box_size_angstrom=request["box_size_angstrom"],
        seed=request["seed"],
        exhaustiveness=request["exhaustiveness"],
        n_poses=request["n_poses"],
        cpu=request["cpu"],
        scoring_function=request["scoring_function"],
        energy_range_kcal_per_mol=request["energy_range_kcal_per_mol"],
    )
    result_schema = json.loads(
        (ROOT / "api" / "insilico-result.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(result_schema).validate(result)
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        message = str(error).replace("\n", " ")[:1000]
        sys.stderr.write(f"docking job rejected or failed: {message}\n")
        raise SystemExit(2) from error
