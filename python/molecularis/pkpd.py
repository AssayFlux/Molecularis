"""Transparent, non-clinical PK/PD toy models with explicit units and limits.

These closed-form models are for software verification and teaching only. They are
not parameter estimators, dose calculators, clinical predictions or validated PBPK.
"""
from __future__ import annotations

from math import exp, isfinite
from typing import TypedDict


class PKPDResult(TypedDict):
    schema_version: int
    model: str
    engine: str
    units: dict[str, str]
    parameters: dict[str, float]
    observations: list[dict[str, float]]
    provenance: dict[str, object]
    limitations: list[str]


def _finite_positive(name: str, value: float, *, allow_zero: bool = False) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    invalid = value < 0 if allow_zero else value <= 0
    if invalid:
        comparator = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{name} must be {comparator}")


def one_compartment_oral_pk(
    times: list[float],
    *,
    dose_amount_mg: float,
    bioavailability_fraction: float,
    absorption_rate_per_h: float,
    elimination_rate_per_h: float,
    apparent_volume_l: float,
) -> PKPDResult:
    """First-order absorption/elimination, single dose, one compartment.

    C(t) = F*Dose/V * ka/(ka-ke) * (exp(-ke*t)-exp(-ka*t)).
    Concentration units are mg/L when dose is mg and volume is L.
    """
    _finite_positive("dose_amount_mg", dose_amount_mg)
    _finite_positive("bioavailability_fraction", bioavailability_fraction, allow_zero=True)
    if bioavailability_fraction > 1:
        raise ValueError("bioavailability_fraction must be between 0 and 1")
    _finite_positive("absorption_rate_per_h", absorption_rate_per_h)
    _finite_positive("elimination_rate_per_h", elimination_rate_per_h)
    _finite_positive("apparent_volume_l", apparent_volume_l)
    if not isinstance(times, list) or not times or len(times) > 10000:
        raise ValueError("times must be a non-empty list with at most 10000 values")
    valid_times = all(
        isinstance(t, (int, float))
        and not isinstance(t, bool)
        and isfinite(t)
        and t >= 0
        for t in times
    )
    if not valid_times:
        raise ValueError("times must contain finite non-negative hours")
    ka, ke = absorption_rate_per_h, elimination_rate_per_h
    equal_rates = abs(ka - ke) <= 1e-10 * max(ka, ke)
    if equal_rates:
        # Continuous limit as ka approaches ke: C(t)=F*Dose/V*k*t*exp(-k*t).
        scale = bioavailability_fraction * dose_amount_mg / apparent_volume_l
        observations = [
            {
                "time_h": float(t),
                "concentration_mg_per_l": max(0.0, scale * ka * t * exp(-ka * t)),
            }
            for t in times
        ]
        rate_case = "equal-rate continuous limit"
    else:
        scale = (
            bioavailability_fraction * dose_amount_mg / apparent_volume_l
            * ka / (ka - ke)
        )
        observations = [
            {
                "time_h": float(t),
                "concentration_mg_per_l": max(
                    0.0, scale * (exp(-ke * t) - exp(-ka * t))
                ),
            }
            for t in times
        ]
        rate_case = "distinct first-order rates"
    return {
        "schema_version": 1,
        "model": "single-dose one-compartment oral PK; first-order absorption and elimination",
        "engine": "Kinetics closed-form PKPD reference model",
        "units": {
            "dose_amount": "mg", "apparent_volume": "L", "time": "h",
            "rate_constants": "1/h", "concentration": "mg/L",
        },
        "parameters": {
            "dose_amount_mg": float(dose_amount_mg),
            "bioavailability_fraction": float(bioavailability_fraction),
            "absorption_rate_per_h": float(ka),
            "elimination_rate_per_h": float(ke),
            "apparent_volume_l": float(apparent_volume_l),
        },
        "observations": observations,
        "provenance": {
            "parameter_origin": "caller_supplied",
            "dose_regimen": "single theoretical input",
            "rate_case": rate_case,
        },
        "limitations": [
            "Educational/software-verification model only; not a dose calculator "
            "or treatment advice",
            "Assumes linear one-compartment disposition and first-order absorption/elimination",
            "No lag time, distribution phase, saturable clearance, active metabolites "
            "or interactions",
            "Bioavailability and apparent volume are caller assumptions, not inferred parameters",
            "No population variability, parameter uncertainty, calibration or external validation",
            "Not a PBPK model and not validated for any compound, species or patient",
        ],
    }


def emax_pd(
    concentrations: list[float],
    *,
    baseline_effect: float,
    maximum_effect_increment: float,
    ec50: float,
    hill_coefficient: float = 1.0,
) -> dict[str, object]:
    """Exploratory Emax relationship; effect units are caller-defined."""
    _finite_positive("ec50", ec50)
    _finite_positive("hill_coefficient", hill_coefficient)
    for name, value in (
        ("baseline_effect", baseline_effect),
        ("maximum_effect_increment", maximum_effect_increment),
    ):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if maximum_effect_increment < 0:
        raise ValueError("maximum_effect_increment must be non-negative")
    if not isinstance(concentrations, list) or not concentrations or len(concentrations) > 10000:
        raise ValueError("concentrations must be a non-empty list with at most 10000 values")
    if not all(
        isinstance(c, (int, float)) and not isinstance(c, bool) and isfinite(c) and c >= 0
        for c in concentrations
    ):
        raise ValueError("concentrations must be finite and non-negative")
    values = []
    for concentration in concentrations:
        power = float(concentration) ** hill_coefficient
        effect = baseline_effect + maximum_effect_increment * power / (
            ec50 ** hill_coefficient + power
        )
        values.append({"concentration": float(concentration), "effect": effect})
    return {
        "schema_version": 1,
        "model": "Emax concentration-effect relationship",
        "engine": "Kinetics closed-form PKPD reference model",
        "units": {"concentration": "caller-defined; must match EC50", "effect": "caller-defined"},
        "parameters": {
            "baseline_effect": float(baseline_effect),
            "maximum_effect_increment": float(maximum_effect_increment),
            "ec50": float(ec50),
            "hill_coefficient": float(hill_coefficient),
        },
        "observations": values,
        "provenance": {"parameter_origin": "caller_supplied"},
        "limitations": [
            "Exploratory empirical relationship; not a validated pharmacodynamic model",
            "Concentration and effect units are caller-defined and not inferred",
            "No hysteresis, tolerance, indirect response or time delay",
            "No efficacy, safety, treatment or dosing inference",
        ],
    }
