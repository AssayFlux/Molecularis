"""Enzyme kinetics models and transparent, dependency-free parameter estimation."""
from __future__ import annotations

from math import isfinite, log, sqrt
from typing import cast


def michaelis_menten(substrate: float, vmax: float, km: float) -> float:
    if not all(isfinite(x) for x in (substrate, vmax, km)):
        raise ValueError("Inputs must be finite")
    if substrate < 0 or vmax < 0 or km <= 0:
        raise ValueError("Require S>=0, Vmax>=0 and Km>0")
    return vmax * substrate / (km + substrate)


def inhibition_rate(
    substrate: float, inhibitor: float, vmax: float, km: float,
    ki: float, mode: str, ki_uncompetitive: float | None = None,
) -> float:
    if not all(isfinite(x) for x in (substrate, inhibitor, vmax, km, ki)):
        raise ValueError("Inputs must be finite")
    if substrate < 0 or inhibitor < 0 or vmax < 0 or km <= 0 or ki <= 0:
        raise ValueError("Require S,I,Vmax>=0 and Km,Ki>0")
    alpha = 1 + inhibitor / ki
    if mode == "competitive":
        return vmax * substrate / (alpha * km + substrate)
    if mode == "uncompetitive":
        return vmax * substrate / (km + alpha * substrate)
    if mode == "noncompetitive":
        return (vmax / alpha) * substrate / (km + substrate)
    if mode == "mixed":
        if ki_uncompetitive is None or not isfinite(ki_uncompetitive) or ki_uncompetitive <= 0:
            raise ValueError("mixed inhibition requires finite ki_uncompetitive>0")
        alpha_prime = 1 + inhibitor / ki_uncompetitive
        return vmax * substrate / (alpha * km + alpha_prime * substrate)
    raise ValueError("mode must be competitive, uncompetitive, noncompetitive or mixed")


def fit_michaelis_menten(
    substrates: list[float], rates: list[float], *,
    vmax_bounds: tuple[float, float] | None = None,
    km_bounds: tuple[float, float] | None = None, grid_size: int = 100,
) -> dict[str, object]:
    """Exploratory log-grid fit; diagnostics are descriptive, not validation."""
    if len(substrates) != len(rates) or len(rates) < 3:
        raise ValueError("Need >=3 paired observations")
    if not isinstance(grid_size, int) or isinstance(grid_size, bool) or not 10 <= grid_size <= 1000:
        raise ValueError("grid_size must be an integer between 10 and 1000")
    if not all(isfinite(x) for x in [*substrates, *rates]):
        raise ValueError("Inputs must be finite")
    if any(x < 0 for x in [*substrates, *rates]):
        raise ValueError("Inputs must be non-negative")
    if max(substrates) == 0 or max(rates) == 0:
        raise ValueError("Non-informative data")

    smax, rmax = max(substrates), max(rates)
    vlo, vhi = vmax_bounds or (rmax * 0.5, rmax * 5)
    klo, khi = km_bounds or (max(smax / 1000, 1e-12), smax * 100)
    if not all(isfinite(x) for x in (vlo, vhi, klo, khi)):
        raise ValueError("Bounds must be finite")
    if not (0 < vlo < vhi and 0 < klo < khi):
        raise ValueError("Bounds must be positive and increasing")

    best: tuple[float, float, float, list[float]] | None = None
    for i in range(grid_size):
        vmax = vlo * (vhi / vlo) ** (i / (grid_size - 1))
        for j in range(grid_size):
            km = klo * (khi / klo) ** (j / (grid_size - 1))
            residuals = [
                observed - michaelis_menten(substrate, vmax, km)
                for substrate, observed in zip(substrates, rates)
            ]
            sse = sum(x * x for x in residuals)
            if best is None or sse < best[0]:
                best = (sse, vmax, km, residuals)

    assert best is not None
    sse, vmax, km, residuals = best
    n = len(rates)
    mean_rate = sum(rates) / n
    total_ss = sum((x - mean_rate) ** 2 for x in rates)
    residual_mean = sum(residuals) / n
    residual_sd = sqrt(sum((x - residual_mean) ** 2 for x in residuals) / (n - 1))
    r_squared = None if total_ss == 0 else 1 - sse / total_ss

    # Gaussian least-squares AIC/BIC, assuming independent homoscedastic errors.
    # A perfect fit has degenerate plug-in likelihood; report undefined values.
    if sse == 0:
        aic = bic = None
    else:
        likelihood_term = n * log(sse / n)
        aic = likelihood_term + 2 * 3  # Vmax, Km and residual variance
        bic = likelihood_term + 3 * log(n)

    # Local Jacobian diagnostics for the two fitted parameters. These are
    # descriptive linear approximations, not validated confidence intervals.
    jacobian = [
        (substrate / (km + substrate), -vmax * substrate / ((km + substrate) ** 2))
        for substrate in substrates
    ]
    j11 = sum(row[0] * row[0] for row in jacobian)
    j12 = sum(row[0] * row[1] for row in jacobian)
    j22 = sum(row[1] * row[1] for row in jacobian)
    determinant = j11 * j22 - j12 * j12
    covariance = None
    standard_errors = None
    leverage: list[float] = []
    standardized_residuals: list[float] = []
    cooks_distance: list[float] = []
    condition_number = None
    if determinant > 1e-24 and n > 2:
        inverse = ((j22 / determinant, -j12 / determinant),
                   (-j12 / determinant, j11 / determinant))
        residual_variance = sse / (n - 2)
        covariance = [
            [residual_variance * inverse[0][0], residual_variance * inverse[0][1]],
            [residual_variance * inverse[1][0], residual_variance * inverse[1][1]],
        ]
        standard_errors = [sqrt(max(0.0, covariance[0][0])),
                           sqrt(max(0.0, covariance[1][1]))]
        trace = j11 + j22
        discriminant = sqrt(max(0.0, trace * trace - 4.0 * determinant))
        largest = (trace + discriminant) / 2.0
        smallest = (trace - discriminant) / 2.0
        condition_number = None if smallest <= 0 else largest / smallest
        for row, residual in zip(jacobian, residuals):
            h = (inverse[0][0] * row[0] ** 2 +
                 2.0 * inverse[0][1] * row[0] * row[1] +
                 inverse[1][1] * row[1] ** 2)
            h = min(1.0, max(0.0, h))
            leverage.append(h)
            denominator = sqrt(max(residual_variance * (1.0 - h), 1e-30))
            standardized = residual / denominator
            standardized_residuals.append(standardized)
            cooks_distance.append(
                (standardized ** 2) * h / max(2.0 * (1.0 - h), 1e-12)
            )

    residual_differences = sum(
        (residuals[index] - residuals[index - 1]) ** 2
        for index in range(1, n)
    )
    durbin_watson = None if sse == 0 else residual_differences / sse
    residual_signs = [1 if value > 0 else -1 for value in residuals if value != 0]
    residual_runs = 0 if not residual_signs else 1 + sum(
        residual_signs[index] != residual_signs[index - 1]
        for index in range(1, len(residual_signs))
    )
    bound_tolerance = 1e-6
    vmax_at_bound = min(abs(vmax - vlo), abs(vmax - vhi)) <= bound_tolerance * max(1.0, abs(vmax))
    km_at_bound = min(abs(km - klo), abs(km - khi)) <= bound_tolerance * max(1.0, abs(km))

    warnings = [
        "No validated confidence intervals calculated; use bootstrap only as exploratory uncertainty",
        "Grid search is approximate; the optimum may lie between grid points",
        "Jacobian covariance, leverage and Cook's distance are local Gaussian least-squares approximations",
        "AIC/BIC assume independent observations and constant Gaussian variance",
        "Concentration and rate units must be consistent; units are not inferred",
    ]
    if condition_number is None or condition_number > 1e12:
        warnings.append("Kinetic parameters may be weakly identifiable over the supplied substrate range")
    if vmax_at_bound or km_at_bound:
        warnings.append("At least one fitted parameter lies on a search boundary; expand/review bounds")
    if r_squared is None:
        warnings.append("R-squared is undefined because observed rates have zero variance")
    if aic is None:
        warnings.append("AIC/BIC are undefined for a perfect zero-residual fit")

    return {
        "vmax": vmax, "km": km, "sse": sse, "rmse": sqrt(sse / n), "n": n,
        "estimator": "log-grid least squares", "confidence_intervals": None,
        "residuals": residuals, "residual_mean": residual_mean,
        "residual_sample_sd": residual_sd, "r_squared": r_squared,
        "aic": aic, "bic": bic,
        "parameter_standard_errors_local_approximation": standard_errors,
        "parameter_covariance_local_approximation": covariance,
        "identifiability": {
            "jacobian_information_determinant": determinant,
            "jacobian_condition_number": condition_number,
            "vmax_at_search_bound": vmax_at_bound,
            "km_at_search_bound": km_at_bound,
        },
        "residual_diagnostics": {
            "standardized_residuals_local_approximation": standardized_residuals,
            "leverage": leverage,
            "cooks_distance": cooks_distance,
            "durbin_watson": durbin_watson,
            "residual_sign_runs": residual_runs,
        },
        "information_criteria_assumptions": [
            "independent observations", "constant Gaussian residual variance",
            "two fitted kinetic parameters plus residual variance",
        ],
        "warnings": warnings,
    }


def _validate_transform_data(
    substrates: list[float], rates: list[float],
) -> None:
    if len(substrates) != len(rates) or len(rates) < 2:
        raise ValueError("Need >=2 paired observations")
    if not all(isfinite(value) for value in [*substrates, *rates]):
        raise ValueError("Transform inputs must be finite")
    if any(value <= 0 for value in [*substrates, *rates]):
        raise ValueError("Linearized transforms require strictly positive S and v")


def lineweaver_burk(substrates: list[float], rates: list[float]) -> dict[str, object]:
    """Return reciprocal coordinates; error weighting is distorted by reciprocals."""
    _validate_transform_data(substrates, rates)
    return {
        "x": [1.0 / value for value in substrates],
        "y": [1.0 / value for value in rates],
        "axes": ["1/[S]", "1/v"],
        "warning": "Exploratory reciprocal transform; low-substrate errors are strongly amplified",
    }


def eadie_hofstee(substrates: list[float], rates: list[float]) -> dict[str, object]:
    """Return Eadie-Hofstee coordinates; both axes contain the measured rate."""
    _validate_transform_data(substrates, rates)
    return {
        "x": [rate / substrate for substrate, rate in zip(substrates, rates)],
        "y": list(rates),
        "axes": ["v/[S]", "v"],
        "warning": "Exploratory transform; x and y share measured v and therefore correlated errors",
    }


def hanes_woolf(substrates: list[float], rates: list[float]) -> dict[str, object]:
    """Return Hanes-Woolf coordinates; transformed errors remain heteroscedastic."""
    _validate_transform_data(substrates, rates)
    return {
        "x": list(substrates),
        "y": [substrate / rate for substrate, rate in zip(substrates, rates)],
        "axes": ["[S]", "[S]/v"],
        "warning": "Exploratory transform; transformed errors are not generally constant variance",
    }

def bootstrap_michaelis_menten(
    substrates: list[float], rates: list[float], *,
    replicates: int = 200, confidence_level: float = 0.95,
    seed: int = 0, grid_size: int = 40,
) -> dict[str, object]:
    """Paired nonparametric bootstrap percentile intervals for the exploratory grid fit.

    Resampling assumes independent, identically distributed paired observations.
    The same parameter search bounds are held fixed across replicates. This does not
    address model misspecification, identifiability, measurement error or study design.
    """
    import random

    if not isinstance(replicates, int) or isinstance(replicates, bool) or not 100 <= replicates <= 10_000:
        raise ValueError("replicates must be an integer between 100 and 10000")
    if not isfinite(confidence_level) or not 0.5 <= confidence_level < 1.0:
        raise ValueError("confidence_level must be finite and in [0.5, 1)")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be an integer")

    point = fit_michaelis_menten(substrates, rates, grid_size=grid_size)
    smax, rmax = max(substrates), max(rates)
    vmax_bounds = (rmax * 0.5, rmax * 5.0)
    km_bounds = (max(smax / 1000.0, 1e-12), smax * 100.0)
    generator = random.Random(seed)
    vmax_samples: list[float] = []
    km_samples: list[float] = []
    sample_count = len(substrates)

    for _ in range(replicates):
        indices = [generator.randrange(sample_count) for _ in range(sample_count)]
        sampled_s = [substrates[index] for index in indices]
        sampled_r = [rates[index] for index in indices]
        if max(sampled_s) <= 0 or max(sampled_r) <= 0:
            continue
        try:
            fitted = fit_michaelis_menten(
                sampled_s, sampled_r, vmax_bounds=vmax_bounds,
                km_bounds=km_bounds, grid_size=grid_size,
            )
        except ValueError:
            continue
        vmax_samples.append(cast(float, fitted["vmax"]))
        km_samples.append(cast(float, fitted["km"]))

    minimum_successes = max(50, int(replicates * 0.8))
    if len(vmax_samples) < minimum_successes:
        raise ValueError(
            f"Only {len(vmax_samples)} of {replicates} bootstrap fits succeeded; "
            "data may be non-informative for the selected model"
        )

    def percentile(values: list[float], probability: float) -> float:
        ordered = sorted(values)
        location = (len(ordered) - 1) * probability
        lower = int(location)
        upper = min(lower + 1, len(ordered) - 1)
        fraction = location - lower
        return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction

    tail = (1.0 - confidence_level) / 2.0
    return {
        "point_estimate": {"vmax": point["vmax"], "km": point["km"]},
        "confidence_level": confidence_level,
        "interval_method": "paired nonparametric percentile bootstrap",
        "confidence_intervals": {
            "vmax": [percentile(vmax_samples, tail), percentile(vmax_samples, 1.0 - tail)],
            "km": [percentile(km_samples, tail), percentile(km_samples, 1.0 - tail)],
        },
        "successful_replicates": len(vmax_samples),
        "requested_replicates": replicates,
        "seed": seed,
        "search_grid_size": grid_size,
        "warnings": [
            "Exploratory percentile intervals; independent reference validation is required",
            "Assumes independent, identically distributed paired observations",
            "Fixed search bounds and finite grid resolution affect interval estimates",
            "Intervals do not resolve model misspecification or parameter non-identifiability",
            "No concentration or rate units are inferred",
        ],
    }

