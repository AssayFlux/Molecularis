"""Leakage-aware ADMET model evaluation and applicability-domain utilities.

These utilities do not train or select a predictive model. They require a separately
licensed, curated dataset and return research evaluation metrics only.
"""
from __future__ import annotations

import random
from math import isfinite
from typing import Sequence


def _validate_smiles_inputs(*collections: Sequence[str]) -> None:
    total_bytes = 0
    for collection in collections:
        for index, value in enumerate(collection):
            if not isinstance(value, str) or not value.strip() or len(value) > 100_000:
                raise ValueError(f"SMILES at index {index} must be non-empty and bounded")
            try:
                total_bytes += len(value.encode("utf-8", errors="strict"))
            except UnicodeEncodeError as error:
                raise ValueError(
                    f"SMILES at index {index} contains invalid Unicode"
                ) from error
            if total_bytes > 16 * 1024 * 1024:
                raise ValueError("combined SMILES input exceeds the 16 MiB limit")


def scaffold_group_split(
    smiles: Sequence[str],
    *,
    train_fraction: float = 0.8,
    validation_fraction: float = 0.1,
    seed: int = 42,
) -> dict[str, object]:
    """Split compounds by Bemis-Murcko scaffold so a scaffold cannot cross partitions."""
    if not isinstance(smiles, Sequence) or isinstance(smiles, (str, bytes)):
        raise ValueError("smiles must be a sequence of strings")
    if not 3 <= len(smiles) <= 100_000:
        raise ValueError("smiles must contain between 3 and 100000 compounds")
    _validate_smiles_inputs(smiles)
    if (
        not isinstance(train_fraction, (int, float))
        or isinstance(train_fraction, bool)
        or not isfinite(train_fraction)
        or not 0.1 <= train_fraction <= 0.9
    ):
        raise ValueError("train_fraction must be finite and in [0.1, 0.9]")
    if (
        not isinstance(validation_fraction, (int, float))
        or isinstance(validation_fraction, bool)
        or not isfinite(validation_fraction)
        or not 0.05 <= validation_fraction <= 0.4
    ):
        raise ValueError("validation_fraction must be finite and in [0.05, 0.4]")
    if train_fraction + validation_fraction >= 1.0:
        raise ValueError("train_fraction plus validation_fraction must be below 1")
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")

    try:
        from rdkit import Chem, rdBase  # type: ignore[import-not-found]
        from rdkit.Chem.Scaffolds import MurckoScaffold  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError("RDKit is required for Bemis-Murcko scaffold splitting") from error

    groups: dict[str, list[int]] = {}
    for index, value in enumerate(smiles):
        if not isinstance(value, str) or not value.strip() or len(value) > 100_000:
            raise ValueError(f"SMILES at index {index} must be non-empty and bounded")
        molecule = Chem.MolFromSmiles(value)
        if molecule is None:
            raise ValueError(f"Invalid SMILES at index {index}")
        scaffold = MurckoScaffold.GetScaffoldForMol(molecule)
        key = Chem.MolToSmiles(scaffold, canonical=True) or Chem.MolToSmiles(
            molecule, canonical=True
        )
        groups.setdefault(key, []).append(index)
    if len(groups) < 3:
        raise ValueError("at least three distinct scaffold groups are required")

    group_items = list(groups.items())
    random.Random(seed).shuffle(group_items)
    group_items.sort(key=lambda item: len(item[1]), reverse=True)
    total = len(smiles)
    targets = [
        total * float(train_fraction),
        total * float(validation_fraction),
        total * (1.0 - float(train_fraction) - float(validation_fraction)),
    ]
    partitions: list[list[int]] = [[], [], []]
    counts = [0, 0, 0]
    for group_index, (_, indices) in enumerate(group_items):
        if group_index < 3:
            destination = group_index
        else:
            destination = max(
                range(3),
                key=lambda candidate: targets[candidate] - counts[candidate],
            )
        partitions[destination].extend(indices)
        counts[destination] += len(indices)
    if any(not partition for partition in partitions):
        raise ValueError("scaffold groups could not populate all three partitions")

    # Build partition membership directly from the assigned index sets for an
    # explicit no-overlap assertion, including acyclic fallback groups.
    index_partition = {
        index: partition_index
        for partition_index, partition in enumerate(partitions)
        for index in partition
    }
    if len(index_partition) != total:
        raise RuntimeError("scaffold split lost or duplicated compound indices")
    for indices in groups.values():
        if len({index_partition[index] for index in indices}) != 1:
            raise RuntimeError("a Bemis-Murcko scaffold crossed data partitions")

    return {
        "schema_version": 1,
        "method": "Bemis-Murcko scaffold-group split",
        "engine": {"name": "RDKit", "version": rdBase.rdkitVersion},
        "seed": seed,
        "train_indices": sorted(partitions[0]),
        "validation_indices": sorted(partitions[1]),
        "test_indices": sorted(partitions[2]),
        "partition_counts": counts,
        "scaffold_group_count": len(groups),
        "no_scaffold_overlap": True,
        "limitations": [
            "Requires curated structures and endpoint harmonization",
            "Scaffold grouping does not eliminate every source of chemical or temporal leakage",
            "Acyclic molecules fall back to canonical SMILES groups; related acyclic series may still cross partitions",
            "Not a model-performance result or evidence of clinical applicability",
        ],
    }


def binary_admet_metrics(
    labels: Sequence[int],
    probabilities: Sequence[float],
    *,
    threshold: float = 0.5,
    calibration_bins: int = 10,
) -> dict[str, object]:
    """Calculate ROC-AUC, average precision, Brier score and calibration summaries."""
    if len(labels) != len(probabilities) or not 2 <= len(labels) <= 1_000_000:
        raise ValueError("labels and probabilities must have the same length in [2, 1000000]")
    if (
        not isinstance(threshold, (int, float))
        or isinstance(threshold, bool)
        or not isfinite(threshold)
        or not 0.0 <= threshold <= 1.0
    ):
        raise ValueError("threshold must be finite and in [0, 1]")
    if (
        not isinstance(calibration_bins, int)
        or isinstance(calibration_bins, bool)
        or not 2 <= calibration_bins <= 50
    ):
        raise ValueError("calibration_bins must be an integer in [2, 50]")
    normalized_labels: list[int] = []
    normalized_probabilities: list[float] = []
    for index, (label, probability) in enumerate(zip(labels, probabilities, strict=True)):
        if not isinstance(label, int) or isinstance(label, bool) or label not in (0, 1):
            raise ValueError(f"label at index {index} must be integer 0 or 1")
        if (
            not isinstance(probability, (int, float))
            or isinstance(probability, bool)
            or not isfinite(probability)
            or not 0.0 <= probability <= 1.0
        ):
            raise ValueError(f"probability at index {index} must be finite and in [0, 1]")
        normalized_labels.append(label)
        normalized_probabilities.append(float(probability))

    positives = sum(normalized_labels)
    negatives = len(normalized_labels) - positives
    if positives == 0 or negatives == 0:
        raise ValueError("ROC-AUC requires both positive and negative labels")

    ranked = sorted(
        zip(normalized_probabilities, normalized_labels, strict=True),
        key=lambda item: item[0],
    )
    positive_rank_sum = 0.0
    rank = 1
    cursor = 0
    while cursor < len(ranked):
        end = cursor + 1
        while end < len(ranked) and ranked[end][0] == ranked[cursor][0]:
            end += 1
        average_rank = (rank + rank + (end - cursor) - 1) / 2.0
        positive_rank_sum += average_rank * sum(
            label for _, label in ranked[cursor:end]
        )
        rank += end - cursor
        cursor = end
    roc_auc = (
        positive_rank_sum - positives * (positives + 1) / 2.0
    ) / (positives * negatives)

    descending = sorted(
        zip(normalized_probabilities, normalized_labels, strict=True),
        key=lambda item: item[0],
        reverse=True,
    )
    true_positives = 0
    false_positives = 0
    previous_recall = 0.0
    average_precision = 0.0
    cursor = 0
    while cursor < len(descending):
        end = cursor + 1
        while end < len(descending) and descending[end][0] == descending[cursor][0]:
            end += 1
        tied_labels = [label for _, label in descending[cursor:end]]
        true_positives += sum(tied_labels)
        false_positives += len(tied_labels) - sum(tied_labels)
        recall = true_positives / positives
        precision = true_positives / (true_positives + false_positives)
        average_precision += (recall - previous_recall) * precision
        previous_recall = recall
        cursor = end

    predicted = [int(value >= threshold) for value in normalized_probabilities]
    tp = sum(
        label == 1 and prediction == 1
        for label, prediction in zip(normalized_labels, predicted, strict=True)
    )
    tn = sum(
        label == 0 and prediction == 0
        for label, prediction in zip(normalized_labels, predicted, strict=True)
    )
    fp = negatives - tn
    fn = positives - tp
    brier = sum(
        (probability - label) ** 2
        for probability, label in zip(normalized_probabilities, normalized_labels, strict=True)
    ) / len(normalized_labels)
    bins: list[dict[str, float | int]] = []
    for bin_index in range(calibration_bins):
        lower = bin_index / calibration_bins
        upper = (bin_index + 1) / calibration_bins
        members = [
            index for index, probability in enumerate(normalized_probabilities)
            if lower <= probability < upper
            or (bin_index == calibration_bins - 1 and probability == 1.0)
        ]
        if members:
            bins.append(
                {
                    "lower_probability": lower,
                    "upper_probability": upper,
                    "count": len(members),
                    "mean_predicted_probability": sum(
                        normalized_probabilities[index] for index in members
                    ) / len(members),
                    "observed_positive_fraction": sum(
                        normalized_labels[index] for index in members
                    ) / len(members),
                }
            )

    return {
        "schema_version": 1,
        "metric_scope": "binary classification research evaluation",
        "sample_count": len(normalized_labels),
        "positive_count": positives,
        "negative_count": negatives,
        "roc_auc": roc_auc,
        "average_precision": average_precision,
        "brier_score": brier,
        "threshold": float(threshold),
        "confusion_matrix": {"true_positive": tp, "true_negative": tn, "false_positive": fp, "false_negative": fn},
        "sensitivity": tp / positives,
        "specificity": tn / negatives,
        "calibration_bins": bins,
        "limitations": [
            "Metrics are descriptive for the supplied held-out set only",
            "No calibration, threshold, model or endpoint is selected automatically",
            "No external validation, applicability domain or clinical utility is implied",
        ],
    }


def tanimoto_applicability_domain(
    reference_smiles: Sequence[str],
    query_smiles: Sequence[str],
    *,
    threshold: float = 0.4,
    radius: int = 2,
    fingerprint_bits: int = 2048,
) -> dict[str, object]:
    """Return nearest-reference Morgan/Tanimoto similarity for each query compound."""
    if (
        not isinstance(reference_smiles, Sequence)
        or isinstance(reference_smiles, (str, bytes))
        or not isinstance(query_smiles, Sequence)
        or isinstance(query_smiles, (str, bytes))
        or not reference_smiles
        or not query_smiles
    ):
        raise ValueError("reference_smiles and query_smiles must be non-empty sequences")
    if len(reference_smiles) > 100_000 or len(query_smiles) > 10_000:
        raise ValueError("applicability-domain inputs exceed configured limits")
    if len(reference_smiles) * len(query_smiles) > 10_000_000:
        raise ValueError("reference/query comparison count must not exceed 10000000")
    _validate_smiles_inputs(reference_smiles, query_smiles)
    if (
        not isinstance(threshold, (int, float))
        or isinstance(threshold, bool)
        or not isfinite(threshold)
        or not 0.0 <= threshold <= 1.0
    ):
        raise ValueError("threshold must be finite and in [0, 1]")
    if not isinstance(radius, int) or isinstance(radius, bool) or not 1 <= radius <= 4:
        raise ValueError("radius must be an integer in [1, 4]")
    if (
        not isinstance(fingerprint_bits, int)
        or isinstance(fingerprint_bits, bool)
        or not 256 <= fingerprint_bits <= 8192
    ):
        raise ValueError("fingerprint_bits must be an integer in [256, 8192]")
    try:
        from rdkit import Chem, DataStructs, rdBase
        from rdkit.Chem import rdFingerprintGenerator  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError("RDKit is required for Morgan/Tanimoto applicability-domain analysis") from error

    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=radius, fpSize=fingerprint_bits
    )
    reference_fingerprints = []
    for index, value in enumerate(reference_smiles):
        if not isinstance(value, str) or not value.strip() or len(value) > 100_000:
            raise ValueError(f"Reference SMILES at index {index} must be non-empty and bounded")
        molecule = Chem.MolFromSmiles(value)
        if molecule is None:
            raise ValueError(f"Invalid reference SMILES at index {index}")
        reference_fingerprints.append(generator.GetFingerprint(molecule))
    results: list[dict[str, object]] = []
    for index, value in enumerate(query_smiles):
        if not isinstance(value, str) or not value.strip() or len(value) > 100_000:
            raise ValueError(f"Query SMILES at index {index} must be non-empty and bounded")
        molecule = Chem.MolFromSmiles(value)
        if molecule is None:
            raise ValueError(f"Invalid query SMILES at index {index}")
        fingerprint = generator.GetFingerprint(molecule)
        similarities = DataStructs.BulkTanimotoSimilarity(
            fingerprint, reference_fingerprints
        )
        nearest_index = max(range(len(similarities)), key=similarities.__getitem__)
        nearest_similarity = float(similarities[nearest_index])
        results.append(
            {
                "query_index": index,
                "nearest_reference_index": nearest_index,
                "nearest_tanimoto_similarity": nearest_similarity,
                "within_applicability_domain": nearest_similarity >= threshold,
            }
        )
    return {
        "schema_version": 1,
        "fingerprint": {"type": "Morgan", "radius": radius, "bits": fingerprint_bits},
        "engine": {"name": "RDKit", "version": rdBase.rdkitVersion},
        "threshold": float(threshold),
        "reference_count": len(reference_smiles),
        "query_count": len(query_smiles),
        "results": results,
        "limitations": [
            "Similarity is a structural heuristic, not a calibrated uncertainty estimate",
            "Reference-set quality and endpoint coverage determine applicability",
            "No ADMET endpoint prediction or clinical safety inference is performed",
        ],
    }
