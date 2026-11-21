"""Synthetic-only aggregate genotype frequency simulation for research software tests.

This module does not read patient data, infer ancestry, estimate clinical risk or
model variant effects. Hardy-Weinberg equilibrium is an explicit assumption.
"""
from __future__ import annotations

import random
from math import isfinite


def simulate_hardy_weinberg_cohort(
    allele_frequencies: dict[str, float],
    *,
    sample_size: int,
    seed: int,
) -> dict[str, object]:
    """Generate aggregate synthetic diploid genotype counts for independent loci."""
    valid_size = (
        isinstance(sample_size, int)
        and not isinstance(sample_size, bool)
        and 1 <= sample_size <= 1_000_000
    )
    if not valid_size:
        raise ValueError("sample_size must be an integer between 1 and 1000000")
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")
    if (
        not isinstance(allele_frequencies, dict)
        or not allele_frequencies
        or len(allele_frequencies) > 1000
    ):
        raise ValueError("allele_frequencies must contain 1 to 1000 loci")
    normalized: dict[str, float] = {}
    for locus, frequency in allele_frequencies.items():
        if not isinstance(locus, str) or not locus or len(locus) > 128:
            raise ValueError(
                "locus identifiers must be non-empty strings of at most 128 characters"
            )
        if (
            not isinstance(frequency, (int, float))
            or isinstance(frequency, bool)
            or not isfinite(frequency)
        ):
            raise ValueError(f"allele frequency for {locus} must be finite")
        if not 0.0 <= frequency <= 1.0:
            raise ValueError(f"allele frequency for {locus} must be between 0 and 1")
        normalized[locus] = float(frequency)

    if sample_size * len(normalized) > 10_000_000:
        raise ValueError("sample_size times locus count must not exceed 10000000")

    rng = random.Random(seed)
    results: list[dict[str, object]] = []
    for locus in sorted(normalized):
        p = normalized[locus]
        q = 1.0 - p
        observed = [0, 0, 0]
        for _ in range(sample_size):
            genotype = int(rng.random() < p) + int(rng.random() < p)
            observed[genotype] += 1
        expected = [sample_size * q * q, sample_size * 2.0 * p * q, sample_size * p * p]
        results.append({
            "locus_id": locus,
            "alternate_allele_frequency": p,
            "reference_allele_frequency": q,
            "genotype_order": ["reference_homozygous", "heterozygous", "alternate_homozygous"],
            "observed_synthetic_counts": observed,
            "expected_hardy_weinberg_counts": expected,
        })
    return {
        "schema_version": 1,
        "simulation": "independent-locus Hardy-Weinberg synthetic aggregate cohort",
        "data_classification": "synthetic_non_patient",
        "sample_size": sample_size,
        "seed": seed,
        "loci": results,
        "assumptions": [
            "Diploid autosomal loci with caller-supplied allele frequencies",
            "Hardy-Weinberg equilibrium within the synthetic population",
            "Independent loci; linkage disequilibrium and haplotypes are not modelled",
            "No ancestry, population structure, relatedness, selection or missingness",
        ],
        "limitations": [
            "Synthetic aggregate counts only; no individual-level genotypes are returned",
            "No variant-effect, disease-risk, penetrance or phenotype model is implemented",
            "Not representative of any real population or cohort",
            "No clinical interpretation, diagnosis, treatment or risk estimate",
        ],
        "provenance": {
            "generator": "Kinetics synthetic HWE generator",
            "seeded_prng": "Python random.Random",
        },
    }



def simulate_synthetic_additive_variant_effects(
    allele_frequencies: dict[str, float],
    additive_effects: dict[str, float],
    *,
    sample_size: int,
    baseline_trait_mean: float,
    residual_standard_deviation: float,
    seed: int,
) -> dict[str, object]:
    """Simulate per-locus additive effects and return aggregate synthetic summaries only."""
    if not isinstance(sample_size, int) or isinstance(sample_size, bool) or not 100 <= sample_size <= 1_000_000:
        raise ValueError("sample_size must be an integer between 100 and 1000000")
    if (
        not isinstance(allele_frequencies, dict)
        or not isinstance(additive_effects, dict)
        or not allele_frequencies
        or len(allele_frequencies) > 100
        or set(allele_frequencies) != set(additive_effects)
    ):
        raise ValueError("frequency and effect maps must contain the same 1 to 100 loci")
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")
    for name, value in (
        ("baseline_trait_mean", baseline_trait_mean),
        ("residual_standard_deviation", residual_standard_deviation),
    ):
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not isfinite(value)
        ):
            raise ValueError(f"{name} must be finite")
    if abs(baseline_trait_mean) > 1_000_000:
        raise ValueError("baseline_trait_mean exceeds the supported bound")
    if not 0.0 <= residual_standard_deviation <= 1_000_000:
        raise ValueError("residual_standard_deviation must be between 0 and 1000000")
    if sample_size * len(allele_frequencies) > 10_000_000:
        raise ValueError("sample_size times locus count must not exceed 10000000")

    normalized: dict[str, tuple[float, float]] = {}
    for locus, frequency in allele_frequencies.items():
        effect = additive_effects[locus]
        if not isinstance(locus, str) or not locus or len(locus) > 128:
            raise ValueError("locus identifiers must be non-empty strings of at most 128 characters")
        if (
            not isinstance(frequency, (int, float))
            or isinstance(frequency, bool)
            or not isfinite(frequency)
            or not 0.0 <= frequency <= 1.0
        ):
            raise ValueError(f"allele frequency for {locus} must be finite and in [0, 1]")
        if (
            not isinstance(effect, (int, float))
            or isinstance(effect, bool)
            or not isfinite(effect)
            or abs(effect) > 1_000_000
        ):
            raise ValueError(f"additive effect for {locus} must be finite and bounded")
        normalized[locus] = (float(frequency), float(effect))

    rng = random.Random(seed)
    summaries: list[dict[str, object]] = []
    for locus in sorted(normalized):
        frequency, effect = normalized[locus]
        counts = [0, 0, 0]
        sums = [0.0, 0.0, 0.0]
        squares = [0.0, 0.0, 0.0]
        for _ in range(sample_size):
            dosage = int(rng.random() < frequency) + int(rng.random() < frequency)
            phenotype = (
                baseline_trait_mean
                + effect * dosage
                + rng.gauss(0.0, residual_standard_deviation)
            )
            counts[dosage] += 1
            sums[dosage] += phenotype
            squares[dosage] += phenotype * phenotype
        genotype_groups: list[dict[str, object]] = []
        for dosage, genotype_name in enumerate(
            ("reference_homozygous", "heterozygous", "alternate_homozygous")
        ):
            count = counts[dosage]
            mean = sums[dosage] / count if count else None
            variance = (
                max(0.0, squares[dosage] / count - mean * mean)
                if count and mean is not None
                else None
            )
            genotype_groups.append(
                {
                    "genotype": genotype_name,
                    "alternate_allele_dosage": dosage,
                    "synthetic_count": count,
                    "observed_trait_mean": mean,
                    "observed_trait_variance": variance,
                    "expected_trait_mean_under_model": (
                        baseline_trait_mean + effect * dosage
                    ),
                }
            )
        summaries.append(
            {
                "locus_id": locus,
                "alternate_allele_frequency": frequency,
                "caller_supplied_additive_effect": effect,
                "genotype_groups": genotype_groups,
                "observed_aggregate_count": sum(counts),
            }
        )
    return {
        "schema_version": 1,
        "simulation": "synthetic independent-locus additive genotype-to-trait model",
        "data_classification": "synthetic_non_patient",
        "sample_size": sample_size,
        "seed": seed,
        "trait_units": "caller-defined arbitrary units",
        "baseline_trait_mean": float(baseline_trait_mean),
        "residual_standard_deviation": float(residual_standard_deviation),
        "loci": summaries,
        "assumptions": [
            "Diploid autosomal loci with caller-supplied allele frequencies and effects",
            "Independent loci; linkage disequilibrium and haplotypes are not modelled",
            "Additive dosage effect with independent Gaussian residual noise",
            "No ancestry, population structure, relatedness, selection or missingness",
        ],
        "limitations": [
            "Synthetic aggregate summaries only; no individual genotypes or phenotypes are returned",
            "Effects are caller-supplied inputs, not learned or predicted from biological evidence",
            "No variant pathogenicity, penetrance, disease risk or clinical outcome model is implemented",
            "Not representative of any real population or cohort",
            "No clinical interpretation, diagnosis, treatment or risk estimate",
        ],
        "provenance": {
            "generator": "Kinetics synthetic additive variant-effect simulator",
            "seeded_prng": "Python random.Random",
            "parameter_origin": "caller_supplied",
        },
    }
