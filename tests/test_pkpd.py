from __future__ import annotations

import math

import pytest

from molecularis.pkpd import emax_pd, one_compartment_oral_pk


def test_one_compartment_oral_pk_matches_closed_form_and_provenance() -> None:
    result = one_compartment_oral_pk(
        [0.0, 1.0, 4.0],
        dose_amount_mg=100.0,
        bioavailability_fraction=0.8,
        absorption_rate_per_h=1.5,
        elimination_rate_per_h=0.2,
        apparent_volume_l=20.0,
    )
    assert result["observations"][0]["concentration_mg_per_l"] == 0.0
    expected = 0.8 * 100 / 20 * 1.5 / (1.5 - 0.2) * (
        math.exp(-0.2) - math.exp(-1.5)
    )
    assert result["observations"][1]["concentration_mg_per_l"] == pytest.approx(expected)
    assert result["units"]["concentration"] == "mg/L"
    assert result["provenance"]["parameter_origin"] == "caller_supplied"
    assert any("not a dose calculator" in item for item in result["limitations"])


@pytest.mark.parametrize(
    "kwargs",
    [
        {"dose_amount_mg": 0},
        {"bioavailability_fraction": 1.1},
        {"apparent_volume_l": 0},
    ],
)
def test_one_compartment_oral_pk_rejects_invalid_parameters(kwargs: dict[str, float]) -> None:
    parameters: dict[str, float] = {
        "dose_amount_mg": 100.0,
        "bioavailability_fraction": 0.8,
        "absorption_rate_per_h": 1.5,
        "elimination_rate_per_h": 0.2,
        "apparent_volume_l": 20.0,
    }
    parameters.update(kwargs)
    with pytest.raises(ValueError):
        one_compartment_oral_pk([0.0, 1.0], **parameters)


def test_one_compartment_oral_pk_rejects_unbounded_or_invalid_time_series() -> None:
    args = {
        "dose_amount_mg": 100.0,
        "bioavailability_fraction": 0.8,
        "absorption_rate_per_h": 1.5,
        "elimination_rate_per_h": 0.2,
        "apparent_volume_l": 20.0,
    }
    with pytest.raises(ValueError, match="times"):
        one_compartment_oral_pk([], **args)
    with pytest.raises(ValueError, match="times"):
        one_compartment_oral_pk([float("nan")], **args)
    with pytest.raises(ValueError, match="10000"):
        one_compartment_oral_pk([0.0] * 10001, **args)


def test_emax_pd_has_expected_baseline_half_max_and_asymptote() -> None:
    result = emax_pd(
        [0.0, 2.0, 2000000.0],
        baseline_effect=5.0,
        maximum_effect_increment=80.0,
        ec50=2.0,
    )
    effects = [row["effect"] for row in result["observations"]]
    assert effects[0] == pytest.approx(5.0)
    assert effects[1] == pytest.approx(45.0)
    assert effects[2] == pytest.approx(85.0, rel=1e-5)
    assert any("not a validated" in item for item in result["limitations"])


def test_emax_pd_rejects_negative_and_non_finite_inputs() -> None:
    with pytest.raises(ValueError):
        emax_pd([-1.0], baseline_effect=0.0, maximum_effect_increment=1.0, ec50=1.0)
    with pytest.raises(ValueError):
        emax_pd([1.0], baseline_effect=0.0, maximum_effect_increment=1.0, ec50=0.0)


def test_one_compartment_oral_pk_uses_continuous_limit_for_equal_rates() -> None:
    result = one_compartment_oral_pk(
        [0.0, 2.0],
        dose_amount_mg=100.0,
        bioavailability_fraction=0.8,
        absorption_rate_per_h=0.5,
        elimination_rate_per_h=0.5,
        apparent_volume_l=20.0,
    )
    assert result["observations"][0]["concentration_mg_per_l"] == 0.0
    assert result["observations"][1]["concentration_mg_per_l"] == pytest.approx(
        0.8 * 100.0 / 20.0 * 0.5 * 2.0 * math.exp(-1.0)
    )
    assert result["provenance"]["rate_case"] == "equal-rate continuous limit"
