#!/usr/bin/env python3
"""Independent host-side Michaelis-Menten comparison against SciPy curve_fit.

Requires SciPy and NumPy on the validation host. This script does not run on Android
and does not turn the Kinetics estimator into a validated capability by itself.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

try:
    import numpy as np
    import scipy
    from scipy.optimize import curve_fit
except ImportError as error:
    raise SystemExit(
        "Install a reviewed SciPy/NumPy host validation environment before running this check"
    ) from error

from molecularis.kinetics import fit_michaelis_menten


def model(substrate, vmax, km):
    return vmax * substrate / (km + substrate)


def run() -> dict[str, object]:
    rng = random.Random(20261108)
    substrates = [0.5, 1, 2, 3, 5, 8, 12, 20, 35, 60, 100, 180]
    true_vmax, true_km = 120.0, 15.0
    exact = [model(value, true_vmax, true_km) for value in substrates]
    noisy = [value + rng.gauss(0.0, 0.35) for value in exact]
    bounds = ((80.0, 160.0), (5.0, 30.0))
    scenarios = []
    for name, rates, tolerance in (
        ("noise_free_synthetic", exact, 0.02),
        ("gaussian_noise_sd_0_35", noisy, 0.05),
    ):
        scipy_parameters, scipy_covariance = curve_fit(
            model, np.asarray(substrates), np.asarray(rates),
            p0=(110.0, 12.0), bounds=([80.0, 5.0], [160.0, 30.0]),
            method="trf", max_nfev=100_000,
        )
        local = fit_michaelis_menten(
            substrates, rates, vmax_bounds=bounds[0], km_bounds=bounds[1],
            grid_size=400,
        )
        vmax_relative_error = float(
            abs(float(local["vmax"]) - scipy_parameters[0]) / abs(scipy_parameters[0])
        )
        km_relative_error = float(
            abs(float(local["km"]) - scipy_parameters[1]) / abs(scipy_parameters[1])
        )
        scenarios.append({
            "scenario": name,
            "known_parameters": {"vmax": true_vmax, "km": true_km},
            "kinetics_estimate": {"vmax": local["vmax"], "km": local["km"]},
            "scipy_curve_fit": {
                "vmax": float(scipy_parameters[0]), "km": float(scipy_parameters[1]),
                "covariance_diagonal": [float(value) for value in np.diag(scipy_covariance)],
            },
            "relative_parameter_error_vs_scipy": {
                "vmax": vmax_relative_error, "km": km_relative_error,
            },
            "tolerance": tolerance,
            "pass": bool(max(vmax_relative_error, km_relative_error) <= tolerance),
            "local_residual_diagnostics": local["residual_diagnostics"],
            "local_identifiability": local["identifiability"],
        })
    return {
        "validation_id": "kinetics-mm-scipy-curve-fit-2026-11-08",
        "reference": "scipy.optimize.curve_fit(method='trf')",
        "scipy_version": scipy.__version__,
        "numpy_version": np.__version__,
        "seed": 20261108,
        "method": "independent bounded nonlinear least-squares comparison",
        "limitations": [
            "Synthetic data only; no external experimental reference dataset",
            "SciPy curve_fit is an independent numerical implementation, not an experimental truth source",
            "Grid resolution and parameter bounds affect the Kinetics result",
            "This host validation does not establish Android/SciPy availability or device performance",
        ],
        "scenarios": scenarios,
        "overall_pass": all(item["pass"] for item in scenarios),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
