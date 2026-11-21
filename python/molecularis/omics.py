"""Transparent exploratory count-table normalisation and omics statistics."""
from __future__ import annotations

from math import exp, isfinite, log, log1p, log2, sqrt


def _finite(values: list[float], label: str) -> None:
    if not all(isfinite(value) for value in values):
        raise ValueError(f"{label} must contain only finite values")


def cpm(counts: list[list[float]]) -> list[list[float]]:
    if not counts or not counts[0] or any(len(row) != len(counts[0]) for row in counts):
        raise ValueError("Counts must be a non-empty rectangular matrix")
    flattened = [value for row in counts for value in row]
    _finite(flattened, "Counts")
    if any(value < 0 for value in flattened):
        raise ValueError("Counts cannot be negative")
    columns = len(counts[0])
    totals = [sum(row[j] for row in counts) for j in range(columns)]
    if any(total == 0 for total in totals):
        raise ValueError("Cannot normalise a zero-library column")
    return [[row[j] * 1_000_000 / totals[j] for j in range(columns)] for row in counts]


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 3:
        raise ValueError("Need >=3 paired values")
    _finite(x + y, "Correlation inputs")
    mx, my = sum(x) / len(x), sum(y) / len(y)
    dx, dy = [value - mx for value in x], [value - my for value in y]
    denom = sqrt(sum(value * value for value in dx) * sum(value * value for value in dy))
    if denom == 0:
        raise ValueError("Correlation undefined for constant input")
    return sum(a * b for a, b in zip(dx, dy)) / denom


def log2_fold_change(
    group_a: list[float], group_b: list[float], *, pseudocount: float = 0.5,
) -> float:
    if not group_a or not group_b or not isfinite(pseudocount) or pseudocount <= 0:
        raise ValueError("Groups must be non-empty and pseudocount finite and positive")
    _finite(group_a + group_b, "Counts")
    if any(value < 0 for value in group_a + group_b):
        raise ValueError("Counts cannot be negative")
    mean_a = sum(group_a) / len(group_a)
    mean_b = sum(group_b) / len(group_b)
    return log2((mean_a + pseudocount) / (mean_b + pseudocount))


def shannon_diversity(counts: list[float]) -> float:
    if not counts:
        raise ValueError("Counts must be a non-empty non-negative vector")
    _finite(counts, "Counts")
    if any(value < 0 for value in counts):
        raise ValueError("Counts must be non-negative")
    total = sum(counts)
    if total <= 0:
        raise ValueError("Total abundance must be positive")
    return -sum((value / total) * log(value / total) for value in counts if value > 0)


def simpson_diversity(counts: list[float]) -> float:
    """Return Gini-Simpson diversity (1 - sum of squared relative abundances)."""
    if not counts:
        raise ValueError("Counts must be a non-empty non-negative vector")
    _finite(counts, "Counts")
    if any(value < 0 for value in counts):
        raise ValueError("Counts must be non-negative")
    total = sum(counts)
    if total <= 0:
        raise ValueError("Total abundance must be positive")
    return 1.0 - sum((value / total) ** 2 for value in counts)


def clr_transform(
    matrix: list[list[float]], *, pseudocount: float = 0.5,
) -> list[list[float]]:
    if not matrix or not matrix[0] or not isfinite(pseudocount) or pseudocount <= 0:
        raise ValueError("Require a non-empty matrix and finite positive pseudocount")
    width = len(matrix[0])
    flattened = [value for row in matrix for value in row]
    if any(len(row) != width for row in matrix):
        raise ValueError("Matrix must be rectangular")
    _finite(flattened, "Matrix")
    if any(value < 0 for value in flattened):
        raise ValueError("Matrix must be non-negative")
    output: list[list[float]] = []
    for column in range(width):
        logs = [log(matrix[row][column] + pseudocount) for row in range(len(matrix))]
        center = sum(logs) / len(logs)
        output.append([value - center for value in logs])
    return [list(row) for row in zip(*output)]


def logistic_growth(
    timepoints: list[float], counts: list[float], *,
    carrying_capacity: float, growth_rate: float, initial: float,
) -> list[float]:
    if len(timepoints) != len(counts) or not timepoints:
        raise ValueError("Timepoints and counts must have equal non-zero lengths")
    _finite(timepoints + counts + [carrying_capacity, growth_rate, initial], "Model inputs")
    if carrying_capacity <= 0 or growth_rate <= 0 or initial <= 0:
        raise ValueError("Model parameters must be positive")
    if any(time < 0 for time in timepoints) or any(value < 0 for value in counts):
        raise ValueError("Timepoints and counts must be non-negative")
    return [
        carrying_capacity
        / (1 + ((carrying_capacity - initial) / initial) * exp(-growth_rate * time))
        for time in timepoints
    ]


def cross_omics_correlation(
    first: list[list[float]], second: list[list[float]],
) -> list[list[float]]:
    """Pairwise feature correlations; rows are features, columns are matched samples."""
    if not first or not second or not first[0] or not second[0]:
        raise ValueError("Both omics matrices must be non-empty")
    sample_count = len(first[0])
    if any(len(row) != sample_count for row in first + second):
        raise ValueError("All features must share the same sample order and count")
    return [[pearson(left, right) for right in second] for left in first]


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    """Modified Lentz continued fraction for the incomplete beta function."""
    max_iterations, epsilon, tiny = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, max_iterations + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < epsilon:
            return h
    raise ArithmeticError("Incomplete beta continued fraction did not converge")


def _regularized_beta(x: float, a: float, b: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    from math import lgamma

    front = exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * log(x) + b * log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _beta_continued_fraction(a, b, x) / a
    return 1.0 - front * _beta_continued_fraction(b, a, 1.0 - x) / b


def _student_two_sided_p(statistic: float, degrees_freedom: float) -> float:
    if degrees_freedom <= 0 or not isfinite(degrees_freedom):
        raise ValueError("Welch degrees of freedom must be finite and positive")
    x = degrees_freedom / (degrees_freedom + statistic * statistic)
    return min(1.0, max(0.0, _regularized_beta(x, degrees_freedom / 2.0, 0.5)))


def welch_differential_expression(
    values: list[list[float]], group_a: list[int], group_b: list[int], *,
    feature_ids: list[str] | None = None,
) -> list[dict[str, float | str]]:
    """Exploratory two-group Welch tests on pre-normalized/log-scale feature values.

    Rows are features and columns are independent biological samples. This function
    does not normalize counts, model covariates/batches, or correct for study design.
    Benjamini-Hochberg q-values are returned across the supplied feature family.
    """
    if not values or not values[0] or not group_a or not group_b:
        raise ValueError("Feature matrix and both sample groups must be non-empty")
    width = len(values[0])
    if any(len(row) != width for row in values):
        raise ValueError("Feature matrix must be rectangular")
    if len(group_a) < 2 or len(group_b) < 2:
        raise ValueError("Welch testing requires at least two samples per group")
    indices = group_a + group_b
    if len(set(indices)) != len(indices) or any(index < 0 or index >= width for index in indices):
        raise ValueError("Sample indices must be unique, disjoint and within matrix bounds")
    if feature_ids is None:
        feature_ids = [str(index) for index in range(len(values))]
    if len(feature_ids) != len(values) or len(set(feature_ids)) != len(feature_ids):
        raise ValueError("Feature identifiers must be unique and match matrix rows")
    _finite([value for row in values for value in row], "Differential-expression values")

    raw: list[dict[str, float | str]] = []
    for index, row in enumerate(values):
        left = [row[i] for i in group_a]
        right = [row[i] for i in group_b]
        mean_a, mean_b = sum(left) / len(left), sum(right) / len(right)
        var_a = sum((x - mean_a) ** 2 for x in left) / (len(left) - 1)
        var_b = sum((x - mean_b) ** 2 for x in right) / (len(right) - 1)
        term_a, term_b = var_a / len(left), var_b / len(right)
        standard_error = sqrt(term_a + term_b)
        difference = mean_a - mean_b
        if standard_error == 0:
            statistic, p_value = (0.0, 1.0) if difference == 0 else (float("inf"), 0.0)
        else:
            statistic = difference / standard_error
            denominator = term_a * term_a / (len(left) - 1) + term_b * term_b / (len(right) - 1)
            degrees = (term_a + term_b) ** 2 / denominator
            p_value = _student_two_sided_p(abs(statistic), degrees)
        raw.append({
            "feature_id": feature_ids[index], "mean_group_a": mean_a,
            "mean_group_b": mean_b, "difference": difference,
            "welch_t": statistic, "p_value": p_value, "q_value": 1.0,
        })

    order = sorted(range(len(raw)), key=lambda i: float(raw[i]["p_value"]))
    running = 1.0
    count = len(raw)
    for rank_index in range(count - 1, -1, -1):
        position = order[rank_index]
        adjusted = min(1.0, float(raw[position]["p_value"]) * count / (rank_index + 1))
        running = min(running, adjusted)
        raw[position]["q_value"] = running
    return raw


def _solve_wls(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    a = [matrix[i][:] + [vector[i]] for i in range(n)]
    scale = max(abs(x) for row in matrix for x in row)
    if scale == 0:
        raise ValueError("Rank-deficient design matrix")
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) <= scale * 1e-12:
            raise ValueError("rank-deficient or ill-conditioned design matrix")
        a[col], a[pivot] = a[pivot], a[col]
        d = a[col][col]
        a[col] = [x / d for x in a[col]]
        for r in range(n):
            if r != col:
                factor = a[r][col]
                a[r] = [x - factor * y for x, y in zip(a[r], a[col])]
    return [a[i][-1] for i in range(n)]


def _invert_wls(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    cols = []
    for j in range(n):
        unit = [0.0] * n
        unit[j] = 1.0
        cols.append(_solve_wls(matrix, unit))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def negative_binomial_differential_expression(
    counts: list[list[int | float]], condition: list[int], *,
    covariates: list[list[float]] | None = None,
    feature_ids: list[str] | None = None,
) -> list[dict[str, float | str | bool | int]]:
    """Exploratory NB2 log-link GLM with numeric covariates and Wald tests.

    Counts are raw non-negative integers (features x independent samples).
    Condition is 0/1; numeric covariates are caller-encoded, including reference-
    coded batch indicators. Uses median-of-ratios size factors when possible,
    otherwise library-size factors, and unmoderated per-feature moment dispersions.
    Wald p-values are asymptotic normal approximations; no repeated-measures,
    empirical-Bayes dispersion shrinkage or small-sample correction is claimed.
    """
    from math import erfc

    if not counts or not counts[0]:
        raise ValueError("Count matrix must be non-empty")
    n = len(counts[0])
    if n < 4 or len(condition) != n or set(condition) != {0, 1}:
        raise ValueError("Need >=4 samples and a 0/1 condition containing both groups")
    if any(len(row) != n for row in counts):
        raise ValueError("Count matrix must be rectangular")
    flat = [float(x) for row in counts for x in row]
    _finite(flat, "Raw counts")
    if any(x < 0 or not x.is_integer() for x in flat):
        raise ValueError("NB2 requires non-negative integer raw counts")
    covariates = covariates or []
    if any(len(row) != n for row in covariates):
        raise ValueError("Covariate rows must match sample count")
    _finite([float(x) for row in covariates for x in row], "Covariates")
    p = 2 + len(covariates)
    if n <= p:
        raise ValueError("Insufficient residual degrees of freedom")
    if feature_ids is None:
        feature_ids = [str(i) for i in range(len(counts))]
    if len(feature_ids) != len(counts) or len(set(feature_ids)) != len(feature_ids):
        raise ValueError("Feature IDs must be unique and match feature rows")

    libraries = [sum(float(row[j]) for row in counts) for j in range(n)]
    if any(x <= 0 for x in libraries):
        raise ValueError("Every sample must have a non-zero library size")
    ratios: list[list[float]] = [[] for _ in range(n)]
    for row in counts:
        values = [float(x) for x in row]
        if all(x > 0 for x in values):
            gm = exp(sum(log(x) for x in values) / n)
            for j in range(n):
                ratios[j].append(values[j] / gm)
    def median(xs: list[float]) -> float:
        xs = sorted(xs)
        m = len(xs) // 2
        return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2
    if all(ratios):
        factors = [median(row) for row in ratios]
    else:
        gm = exp(sum(log(x) for x in libraries) / n)
        factors = [x / gm for x in libraries]
    gm_f = exp(sum(log(x) for x in factors) / n)
    factors = [x / gm_f for x in factors]
    offsets = [log(x) for x in factors]
    design = [[1.0, float(condition[j])] + [float(row[j]) for row in covariates] for j in range(n)]
    design_information = [
        [sum(sample[row] * sample[column] for sample in design) for column in range(p)]
        for row in range(p)
    ]
    # Reject confounded/aliased condition and batch designs before feature-wise fitting.
    _solve_wls(design_information, [0.0] * p)
    results: list[dict[str, float | str | bool | int]] = []

    for feature, row in zip(feature_ids, counts):
        y = [float(x) for x in row]
        if not any(y):
            # An all-zero feature has no estimable abundance or condition effect.
            # Keep it in the tested family with p=1 so BH adjustment remains explicit.
            results.append({
                "feature_id": feature, "log2_fold_change": 0.0,
                "condition_coefficient": 0.0, "standard_error": float("inf"),
                "wald_z": 0.0, "p_value": 1.0, "dispersion": 1e-8,
                "converged": True, "iterations": 0,
                "warning": "All-zero feature; condition effect is not estimable",
            })
            continue
        norm = [y[j] / factors[j] for j in range(n)]
        mean = sum(norm) / n
        variance = sum((x - mean) ** 2 for x in norm) / (n - 1)
        alpha = min(10.0, max(1e-8, (variance - mean) / max(mean * mean, 1e-12)))
        beta = [0.0] * p
        beta[0] = log((sum(y) + 0.5) / n) - sum(offsets) / n
        converged = False
        information = [[0.0] * p for _ in range(p)]
        warning = ""
        iterations = 0
        try:
            for iterations in range(1, 101):
                weights, z = [], []
                for j in range(n):
                    eta = min(30.0, sum(design[j][k] * beta[k] for k in range(p)) + offsets[j])
                    mu = max(exp(eta), 1e-10)
                    weights.append(mu / (1.0 + alpha * mu))
                    z.append(eta + (y[j] - mu) / mu - offsets[j])
                information = [[sum(design[j][a] * weights[j] * design[j][b] for j in range(n))
                                for b in range(p)] for a in range(p)]
                score = [sum(design[j][a] * weights[j] *
                             (z[j] - sum(design[j][k] * beta[k] for k in range(p)))
                             for j in range(n)) for a in range(p)]
                delta = _solve_wls(information, score)
                beta = [beta[k] + delta[k] for k in range(p)]
                if not all(isfinite(x) for x in beta):
                    raise ValueError("Non-finite NB2 coefficients")
                if max(abs(x) for x in delta) < 1e-8:
                    converged = True
                    break
            covariance = _invert_wls(information)
            se = sqrt(max(0.0, covariance[1][1]))
            zstat = beta[1] / se if se > 0 else (0.0 if beta[1] == 0 else float("inf"))
            pvalue = 1.0 if zstat == 0 else (0.0 if not isfinite(zstat) else erfc(abs(zstat) / sqrt(2)))
            if not converged:
                warning = "IRLS did not converge within 100 iterations"
            lfc = beta[1] / log(2)
        except (ValueError, ArithmeticError, OverflowError) as error:
            se, zstat, pvalue, lfc = float("nan"), float("nan"), 1.0, float("nan")
            converged, warning, iterations = False, str(error), 0
        results.append({
            "feature_id": feature, "log2_fold_change": lfc, "condition_coefficient": beta[1],
            "standard_error": se, "wald_z": zstat, "p_value": pvalue,
            "dispersion": alpha, "converged": converged, "iterations": iterations,
            "warning": warning,
        })

    order = sorted(range(len(results)), key=lambda i: float(results[i]["p_value"]))
    q = [1.0] * len(results)
    running = 1.0
    for k in range(len(order) - 1, -1, -1):
        i = order[k]
        running = min(running, float(results[i]["p_value"]) * len(order) / (k + 1))
        q[i] = min(1.0, running)
    for i, result in enumerate(results):
        result["q_value"] = q[i]
    return results

