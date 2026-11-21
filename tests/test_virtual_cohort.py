from __future__ import annotations

import pytest

from molecularis.virtual_cohort import simulate_hardy_weinberg_cohort


def test_synthetic_cohort_is_reproducible_aggregate_and_conserves_counts() -> None:
    args = {"rsSynthetic1": 0.2, "rsSynthetic2": 0.5}
    first = simulate_hardy_weinberg_cohort(args, sample_size=5000, seed=42)
    second = simulate_hardy_weinberg_cohort(args, sample_size=5000, seed=42)
    assert first == second
    assert first["data_classification"] == "synthetic_non_patient"
    for locus in first["loci"]:
        assert sum(locus["observed_synthetic_counts"]) == 5000
        assert len(locus["expected_hardy_weinberg_counts"]) == 3
    assert "No variant-effect" in first["limitations"][1]


@pytest.mark.parametrize(
    ("frequencies", "sample_size", "seed"),
    [
        ({}, 10, 1),
        ({"rs1": -0.1}, 10, 1),
        ({"rs1": 1.1}, 10, 1),
        ({"rs1": float("nan")}, 10, 1),
        ({"rs1": 0.5}, 0, 1),
        ({"rs1": 0.5}, 10, -1),
        ({"rs1": 0.5}, 10, True),
    ],
)
def test_synthetic_cohort_rejects_invalid_inputs(
    frequencies: dict[str, float], sample_size: int, seed: int
) -> None:
    with pytest.raises(ValueError):
        simulate_hardy_weinberg_cohort(frequencies, sample_size=sample_size, seed=seed)


def test_synthetic_cohort_caps_total_genotype_draws() -> None:
    with pytest.raises(ValueError, match="locus count"):
        simulate_hardy_weinberg_cohort(
            {f"locus_{index}": 0.5 for index in range(11)},
            sample_size=1_000_000,
            seed=1,
        )



def test_synthetic_additive_effects_are_reproducible_and_aggregate_only() -> None:
    from molecularis.virtual_cohort import simulate_synthetic_additive_variant_effects

    first = simulate_synthetic_additive_variant_effects(
        {"rsSyntheticEffect": 0.5},
        {"rsSyntheticEffect": 2.0},
        sample_size=1000,
        baseline_trait_mean=3.0,
        residual_standard_deviation=0.0,
        seed=19,
    )
    second = simulate_synthetic_additive_variant_effects(
        {"rsSyntheticEffect": 0.5},
        {"rsSyntheticEffect": 2.0},
        sample_size=1000,
        baseline_trait_mean=3.0,
        residual_standard_deviation=0.0,
        seed=19,
    )
    assert first == second
    locus = first["loci"][0]
    groups = locus["genotype_groups"]
    assert [group["expected_trait_mean_under_model"] for group in groups] == [3.0, 5.0, 7.0]
    assert sum(group["synthetic_count"] for group in groups) == 1000
    assert first["data_classification"] == "synthetic_non_patient"
    assert "individual genotypes or phenotypes" in first["limitations"][0]


def test_synthetic_additive_effects_reject_invalid_inputs() -> None:
    from molecularis.virtual_cohort import simulate_synthetic_additive_variant_effects

    with pytest.raises(ValueError, match="same 1 to 100 loci"):
        simulate_synthetic_additive_variant_effects(
            {"rs1": 0.5}, {}, sample_size=100,
            baseline_trait_mean=0.0, residual_standard_deviation=1.0, seed=1,
        )
    with pytest.raises(ValueError, match="sample_size"):
        simulate_synthetic_additive_variant_effects(
            {"rs1": 0.5}, {"rs1": 1.0}, sample_size=10,
            baseline_trait_mean=0.0, residual_standard_deviation=1.0, seed=1,
        )
    with pytest.raises(ValueError, match="additive effect"):
        simulate_synthetic_additive_variant_effects(
            {"rs1": 0.5}, {"rs1": float("nan")}, sample_size=100,
            baseline_trait_mean=0.0, residual_standard_deviation=1.0, seed=1,
        )
