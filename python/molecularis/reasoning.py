"""Shared scientific reasoning primitives for Agentics Molecularis (P2).

The core is dependency-free and deterministic. Expressions are parsed into a restricted
AST (never eval/exec); numerical methods report tolerances and termination diagnostics.
Methods are computational aids, not scientific truth oracles.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass, field
from typing import Mapping, Sequence

from .knowledge import DIMENSIONLESS, Dimension


def _finite(value: float, name: str = "value") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


_ALLOWED_BINARY = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)
_ALLOWED_UNARY = (ast.UAdd, ast.USub)


@dataclass(frozen=True, slots=True)
class SymbolicExpression:
    """A small, safe arithmetic expression language with explicit variable names."""

    source: str

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source.strip() or len(self.source) > 2048:
            raise ValueError("Expression must be non-empty text no longer than 2048 characters")
        try:
            tree = ast.parse(self.source, mode="eval")
        except SyntaxError as exc:
            raise ValueError("Invalid arithmetic expression") from exc
        nodes = list(ast.walk(tree))
        if len(nodes) > 128:
            raise ValueError("Expression exceeds 128 AST nodes")
        for node in nodes:
            if isinstance(node, ast.Expression | ast.Load):
                continue
            if isinstance(node, ast.Constant):
                if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                    raise ValueError("Only numeric constants are allowed")
                _finite(node.value)
            elif isinstance(node, ast.Name):
                if not node.id.isidentifier() or node.id.startswith("_"):
                    raise ValueError("Invalid variable name")
            elif isinstance(node, ast.BinOp):
                if not isinstance(node.op, _ALLOWED_BINARY):
                    raise ValueError("Unsupported arithmetic operator")
                if isinstance(node.op, ast.Pow) and isinstance(node.right, ast.Constant):
                    if abs(_finite(node.right.value, "exponent")) > 12:
                        raise ValueError("Exponent magnitude exceeds 12")
            elif isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, _ALLOWED_UNARY):
                    raise ValueError("Unsupported unary operator")
            elif isinstance(node, _ALLOWED_BINARY + _ALLOWED_UNARY):
                continue
            else:
                raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")
        self._check_depth(tree, 0)

    @classmethod
    def _check_depth(cls, node: ast.AST, depth: int) -> None:
        if depth > 24:
            raise ValueError("Expression nesting exceeds 24 levels")
        for child in ast.iter_child_nodes(node):
            cls._check_depth(child, depth + 1)

    def _tree(self) -> ast.Expression:
        return ast.parse(self.source, mode="eval")

    def variables(self) -> tuple[str, ...]:
        return tuple(sorted({n.id for n in ast.walk(self._tree()) if isinstance(n, ast.Name)}))

    def evaluate(self, values: Mapping[str, float]) -> float:
        missing = set(self.variables()) - set(values)
        if missing:
            raise ValueError(f"Missing expression variables: {', '.join(sorted(missing))}")

        def visit(node: ast.AST) -> float:
            if isinstance(node, ast.Expression):
                return visit(node.body)
            if isinstance(node, ast.Constant):
                return _finite(node.value)
            if isinstance(node, ast.Name):
                return _finite(values[node.id], node.id)
            if isinstance(node, ast.UnaryOp):
                value = visit(node.operand)
                return value if isinstance(node.op, ast.UAdd) else -value
            if isinstance(node, ast.BinOp):
                left, right = visit(node.left), visit(node.right)
                if isinstance(node.op, ast.Add):
                    result = left + right
                elif isinstance(node.op, ast.Sub):
                    result = left - right
                elif isinstance(node.op, ast.Mult):
                    result = left * right
                elif isinstance(node.op, ast.Div):
                    if right == 0:
                        raise ZeroDivisionError("Expression division by zero")
                    result = left / right
                elif isinstance(node.op, ast.Pow):
                    if abs(right) > 12:
                        raise ValueError("Exponent magnitude exceeds 12")
                    result = left ** right
                elif isinstance(node.op, ast.Mod):
                    if right == 0:
                        raise ZeroDivisionError("Expression modulo by zero")
                    result = left % right
                else:
                    raise ValueError("Unsupported operator")
                return _finite(result, "expression result")
            raise ValueError(f"Unsupported expression node: {type(node).__name__}")

        return visit(self._tree())

    def infer_dimension(self, variables: Mapping[str, Dimension]) -> Dimension:
        missing = set(self.variables()) - set(variables)
        if missing:
            raise ValueError(f"Missing variable dimensions: {', '.join(sorted(missing))}")

        def visit(node: ast.AST) -> Dimension:
            if isinstance(node, ast.Expression):
                return visit(node.body)
            if isinstance(node, ast.Constant):
                return DIMENSIONLESS
            if isinstance(node, ast.Name):
                return variables[node.id]
            if isinstance(node, ast.UnaryOp):
                return visit(node.operand)
            if isinstance(node, ast.BinOp):
                left, right = visit(node.left), visit(node.right)
                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mod)):
                    if left != right:
                        raise ValueError("Addition, subtraction and modulo require compatible dimensions")
                    return left
                if isinstance(node.op, ast.Mult):
                    return left * right
                if isinstance(node.op, ast.Div):
                    return left / right
                if isinstance(node.op, ast.Pow):
                    if not isinstance(node.right, ast.Constant) or isinstance(node.right.value, bool):
                        raise ValueError("Dimensional powers must be literal integers")
                    exponent = node.right.value
                    if not isinstance(exponent, int):
                        raise ValueError("Dimensional powers must be integers")
                    return left ** exponent
            raise ValueError("Cannot infer expression dimension")

        return visit(self._tree())


@dataclass(frozen=True, slots=True)
class DerivationStep:
    expression: str
    variables: Mapping[str, float]
    result: float
    dimension: Dimension
    assumptions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DerivationTrace:
    trace_id: str
    steps: tuple[DerivationStep, ...]
    source_refs: tuple[str, ...] = ()
    method: str = "restricted-arithmetic-v1"

    @classmethod
    def build(
        cls,
        steps: Sequence[tuple[SymbolicExpression, Mapping[str, float], Mapping[str, Dimension], tuple[str, ...]]],
        *,
        source_refs: Sequence[str] = (),
    ) -> "DerivationTrace":
        if not steps or len(steps) > 128:
            raise ValueError("A derivation must contain 1 to 128 steps")
        records: list[DerivationStep] = []
        for expression, values, dimensions, assumptions in steps:
            result = expression.evaluate(values)
            dimension = expression.infer_dimension(dimensions)
            records.append(DerivationStep(expression.source, dict(values), result, dimension, tuple(assumptions)))
        payload = {
            "steps": [
                {"expression": s.expression, "variables": dict(s.variables), "result": s.result,
                 "dimension": s.dimension.powers, "assumptions": s.assumptions}
                for s in records
            ],
            "source_refs": tuple(source_refs),
            "method": "restricted-arithmetic-v1",
        }
        return cls(_digest(payload), tuple(records), tuple(source_refs))


@dataclass(frozen=True, slots=True)
class SolverDiagnostics:
    method: str
    converged: bool
    iterations: int
    residual: float
    tolerance: float
    bracket: tuple[float, float] | None
    termination: str


@dataclass(frozen=True, slots=True)
class NumericalResult:
    value: float
    diagnostics: SolverDiagnostics


def bisect_root(
    function, lower: float, upper: float, *, tolerance: float = 1e-10, max_iterations: int = 256,
) -> NumericalResult:
    """Bisection with bracket validation and explicit convergence diagnostics."""
    lo, hi = _finite(lower, "lower"), _finite(upper, "upper")
    tol = _finite(tolerance, "tolerance")
    if lo >= hi or tol <= 0 or isinstance(max_iterations, bool) or not 1 <= max_iterations <= 10000:
        raise ValueError("Invalid bisection bounds, tolerance or iteration budget")
    flo, fhi = _finite(function(lo), "f(lower)"), _finite(function(hi), "f(upper)")
    if flo == 0:
        return NumericalResult(lo, SolverDiagnostics("bisection", True, 0, 0.0, tol, (lo, hi), "exact_lower"))
    if fhi == 0:
        return NumericalResult(hi, SolverDiagnostics("bisection", True, 0, 0.0, tol, (lo, hi), "exact_upper"))
    if flo * fhi > 0:
        raise ValueError("Root is not bracketed: endpoint function values have the same sign")
    mid, residual = lo, math.inf
    for iteration in range(1, max_iterations + 1):
        mid = lo + (hi - lo) / 2
        fm = _finite(function(mid), "function value")
        residual = abs(fm)
        if residual <= tol or (hi - lo) / 2 <= tol:
            return NumericalResult(mid, SolverDiagnostics(
                "bisection", True, iteration, residual, tol, (lo, hi), "tolerance_reached",
            ))
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return NumericalResult(mid, SolverDiagnostics(
        "bisection", False, max_iterations, residual, tol, (lo, hi), "iteration_limit",
    ))


@dataclass(frozen=True, slots=True)
class DescriptiveStatistics:
    count: int
    mean: float
    variance: float
    standard_deviation: float
    minimum: float
    maximum: float
    variance_ddof: int


def describe(values: Sequence[float], *, ddof: int = 1) -> DescriptiveStatistics:
    data = [_finite(v, "sample") for v in values]
    if not data or ddof not in (0, 1) or len(data) <= ddof:
        raise ValueError("Need more observations than ddof (0 or 1)")
    mean = math.fsum(data) / len(data)
    variance = math.fsum((x - mean) ** 2 for x in data) / (len(data) - ddof)
    return DescriptiveStatistics(len(data), mean, variance, math.sqrt(variance), min(data), max(data), ddof)


def pearson_correlation(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Correlation requires equal-length vectors with at least two values")
    xs, ys = [_finite(v) for v in x], [_finite(v) for v in y]
    mx, my = math.fsum(xs) / len(xs), math.fsum(ys) / len(ys)
    dx, dy = [v - mx for v in xs], [v - my for v in ys]
    sx = math.sqrt(math.fsum(v * v for v in dx))
    sy = math.sqrt(math.fsum(v * v for v in dy))
    if sx == 0 or sy == 0:
        raise ValueError("Correlation is undefined for a constant vector")
    return _finite(math.fsum(a * b for a, b in zip(dx, dy, strict=True)) / (sx * sy))


@dataclass(frozen=True, slots=True)
class UncertaintyResult:
    estimate: float
    standard_uncertainty: float
    method: str
    samples: int
    seed: int | None
    interval_95: tuple[float, float] | None
    assumptions: tuple[str, ...]


def propagate_independent_uncertainty(
    function, means: Mapping[str, float], standard_uncertainties: Mapping[str, float],
    *, relative_step: float = 1e-5,
) -> UncertaintyResult:
    """First-order GUM-style propagation assuming independent input uncertainties."""
    if set(means) != set(standard_uncertainties) or not means:
        raise ValueError("Means and uncertainty maps must have identical non-empty keys")
    step = _finite(relative_step)
    if step <= 0:
        raise ValueError("relative_step must be positive")
    center = {k: _finite(v) for k, v in means.items()}
    sigmas = {k: _finite(v) for k, v in standard_uncertainties.items()}
    if any(v < 0 for v in sigmas.values()):
        raise ValueError("Standard uncertainties must be non-negative")
    estimate = _finite(function(center))
    variance = 0.0
    for key, sigma in sigmas.items():
        h = step * max(1.0, abs(center[key]))
        plus, minus = dict(center), dict(center)
        plus[key] += h
        minus[key] -= h
        derivative = (_finite(function(plus)) - _finite(function(minus))) / (2 * h)
        variance += (derivative * sigma) ** 2
    return UncertaintyResult(
        estimate, math.sqrt(variance), "first_order_independent", 0, None, None,
        ("Independent input uncertainties", "Local linearization; nonlinear effects may be material"),
    )


def monte_carlo_uncertainty(
    function, means: Mapping[str, float], standard_uncertainties: Mapping[str, float],
    *, samples: int = 10000, seed: int = 0,
) -> UncertaintyResult:
    """Deterministic-seed independent Gaussian propagation; interval is empirical 2.5–97.5%."""
    if set(means) != set(standard_uncertainties) or not means:
        raise ValueError("Means and uncertainty maps must have identical non-empty keys")
    if isinstance(samples, bool) or not 100 <= samples <= 1_000_000:
        raise ValueError("samples must be between 100 and 1,000,000")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")
    center = {k: _finite(v) for k, v in means.items()}
    sigmas = {k: _finite(v) for k, v in standard_uncertainties.items()}
    if any(v < 0 for v in sigmas.values()):
        raise ValueError("Standard uncertainties must be non-negative")
    rng = random.Random(seed)
    outputs = []
    for _ in range(samples):
        point = {k: rng.gauss(center[k], sigmas[k]) for k in center}
        outputs.append(_finite(function(point), "Monte Carlo output"))
    outputs.sort()
    mean = math.fsum(outputs) / samples
    variance = math.fsum((v - mean) ** 2 for v in outputs) / (samples - 1)
    return UncertaintyResult(
        mean, math.sqrt(variance), "monte_carlo_independent_gaussian", samples, seed,
        (outputs[int(0.025 * (samples - 1))], outputs[int(0.975 * (samples - 1))]),
        ("Independent Gaussian input distributions", "Empirical percentile interval; tail accuracy depends on sample count"),
    )


@dataclass(frozen=True, slots=True)
class ConstraintSpec:
    constraint_id: str
    expression: SymbolicExpression
    operator: str
    bound: float
    tolerance: float = 1e-9
    hard: bool = True

    def __post_init__(self) -> None:
        if not self.constraint_id.strip() or self.operator not in {"<=", ">=", "=="}:
            raise ValueError("Constraint needs an id and operator <=, >= or ==")
        _finite(self.bound, "constraint bound")
        if _finite(self.tolerance) < 0:
            raise ValueError("Constraint tolerance cannot be negative")

    def evaluate(self, variables: Mapping[str, float]) -> bool:
        value = self.expression.evaluate(variables)
        if self.operator == "<=":
            return value <= self.bound + self.tolerance
        if self.operator == ">=":
            return value >= self.bound - self.tolerance
        return abs(value - self.bound) <= self.tolerance


@dataclass(frozen=True, slots=True)
class ObjectiveSpec:
    objective_id: str
    expression: SymbolicExpression
    direction: str = "minimize"
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not self.objective_id.strip() or self.direction not in {"minimize", "maximize"}:
            raise ValueError("Objective needs an id and direction")
        if _finite(self.weight) <= 0:
            raise ValueError("Objective weight must be positive")


@dataclass(frozen=True, slots=True)
class FeasibilityReport:
    feasible: bool
    passed: tuple[str, ...]
    failed: tuple[str, ...]
    soft_violations: tuple[str, ...]


def check_constraints(constraints: Sequence[ConstraintSpec], variables: Mapping[str, float]) -> FeasibilityReport:
    passed, failed, soft = [], [], []
    for constraint in constraints:
        valid = constraint.evaluate(variables)
        if valid:
            passed.append(constraint.constraint_id)
        elif constraint.hard:
            failed.append(constraint.constraint_id)
        else:
            soft.append(constraint.constraint_id)
    return FeasibilityReport(not failed, tuple(passed), tuple(failed), tuple(soft))


@dataclass(frozen=True, slots=True)
class OptimizationResult:
    variables: Mapping[str, float]
    objective_values: Mapping[str, float]
    feasible: bool
    evaluations: int
    budget: int
    state: str
    method: str = "bounded-grid-v1"


def bounded_grid_search(
    bounds: Mapping[str, tuple[float, float]], objectives: Sequence[ObjectiveSpec],
    constraints: Sequence[ConstraintSpec] = (), *, points_per_dimension: int = 21,
    max_evaluations: int = 100000,
) -> OptimizationResult:
    """Deterministic bounded grid search for low-dimensional reference problems."""
    if not bounds or not objectives:
        raise ValueError("At least one bounded variable and objective are required")
    if len(bounds) > 8 or isinstance(points_per_dimension, bool) or not 2 <= points_per_dimension <= 1000:
        raise ValueError("Grid search supports 1–8 dimensions and 2–1000 points per dimension")
    if isinstance(max_evaluations, bool) or not 1 <= max_evaluations <= 1_000_000:
        raise ValueError("max_evaluations must be between 1 and 1,000,000")
    names = tuple(sorted(bounds))
    axes = []
    for name in names:
        lo, hi = map(_finite, bounds[name])
        if lo >= hi:
            raise ValueError(f"Invalid bounds for {name}")
        axes.append([lo + (hi - lo) * i / (points_per_dimension - 1) for i in range(points_per_dimension)])
    total = points_per_dimension ** len(names)
    budget = min(total, max_evaluations)
    best: tuple[float, dict[str, float], dict[str, float]] | None = None
    evaluations = 0
    # Mixed-radix enumeration avoids materializing the full Cartesian product.
    for index in range(budget):
        cursor, point = index, {}
        for name, axis in reversed(list(zip(names, axes))):
            point[name] = axis[cursor % points_per_dimension]
            cursor //= points_per_dimension
        point = {name: point[name] for name in names}
        evaluations += 1
        if not check_constraints(constraints, point).feasible:
            continue
        values = {obj.objective_id: obj.expression.evaluate(point) for obj in objectives}
        score = math.fsum(
            obj.weight * (values[obj.objective_id] if obj.direction == "minimize" else -values[obj.objective_id])
            for obj in objectives
        )
        if best is None or score < best[0]:
            best = (score, point, values)
    if best is None:
        return OptimizationResult({}, {}, False, evaluations, max_evaluations, "no_feasible_candidate")
    state = "optimal_on_grid" if total <= max_evaluations else "budget_exhausted"
    return OptimizationResult(best[1], best[2], True, evaluations, max_evaluations, state)


@dataclass(frozen=True, slots=True)
class ConstructionTask:
    task_id: str
    domain: str
    mode: str
    objective: str
    assumptions: tuple[str, ...]
    constraints: tuple[ConstraintSpec, ...] = ()
    max_candidates: int = 32
    seed: int = 0

    def __post_init__(self) -> None:
        if not all(isinstance(v, str) and v.strip() for v in (self.task_id, self.domain, self.objective)):
            raise ValueError("Task identity, domain and objective are required")
        if self.mode not in {"reconstruction", "generalization", "exploration"}:
            raise ValueError("Unsupported construction mode")
        if not 1 <= self.max_candidates <= 1000:
            raise ValueError("max_candidates must be between 1 and 1000")
        if not 0 <= self.seed <= 2**32 - 1:
            raise ValueError("seed must be an unsigned 32-bit integer")


@dataclass(frozen=True, slots=True)
class ConstructionCandidate:
    candidate_id: str
    domain: str
    representation: Mapping[str, object]
    assumptions: tuple[str, ...]
    evidence_refs: tuple[str, ...] = ()
    uncertainty: Mapping[str, float] = field(default_factory=dict)

    @property
    def digest(self) -> str:
        return _digest({
            "candidate_id": self.candidate_id, "domain": self.domain,
            "representation": dict(self.representation), "assumptions": self.assumptions,
            "evidence_refs": self.evidence_refs, "uncertainty": dict(self.uncertainty),
        })


def audit_candidate(task: ConstructionTask, candidate: ConstructionCandidate) -> FeasibilityReport:
    """Pre-publication check: task/domain identity, finite uncertainty and declared constraints."""
    if candidate.domain != task.domain:
        raise ValueError("Candidate domain does not match construction task")
    if not candidate.candidate_id.strip():
        raise ValueError("Candidate identity is required")
    for key, value in candidate.uncertainty.items():
        if _finite(value, f"uncertainty {key}") < 0:
            raise ValueError("Candidate uncertainty cannot be negative")
    numeric = {k: _finite(v, k) for k, v in candidate.representation.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
    return check_constraints(task.constraints, numeric)



@dataclass(frozen=True, slots=True)
class BootstrapInterval:
    estimate: float
    lower: float
    upper: float
    confidence: float
    resamples: int
    seed: int


def bootstrap_mean_interval(
    values: Sequence[float], *, confidence: float = 0.95,
    resamples: int = 2000, seed: int = 0,
) -> BootstrapInterval:
    """Percentile bootstrap interval for a sample mean; resampling unit is one observation."""
    data = [_finite(v, "sample") for v in values]
    level = _finite(confidence, "confidence")
    if len(data) < 2 or not 0 < level < 1:
        raise ValueError("At least two observations and confidence in (0, 1) are required")
    if isinstance(resamples, bool) or not 100 <= resamples <= 100000:
        raise ValueError("resamples must be between 100 and 100,000")
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an unsigned 32-bit integer")
    rng = random.Random(seed)
    n = len(data)
    means = sorted(math.fsum(data[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples))
    tail = (1 - level) / 2
    lower = means[int(tail * (resamples - 1))]
    upper = means[int((1 - tail) * (resamples - 1))]
    return BootstrapInterval(math.fsum(data) / n, lower, upper, level, resamples, seed)


@dataclass(frozen=True, slots=True)
class SensitivityResult:
    parameter: str
    derivative: float
    normalized_sensitivity: float | None


def local_sensitivity(function, values: Mapping[str, float], *, relative_step: float = 1e-5) -> tuple[SensitivityResult, ...]:
    """Central finite-difference local sensitivities, including dimensionless normalized values."""
    if not values:
        raise ValueError("At least one parameter is required")
    center = {k: _finite(v) for k, v in values.items()}
    step = _finite(relative_step)
    if step <= 0:
        raise ValueError("relative_step must be positive")
    baseline = _finite(function(center))
    results = []
    for key, value in center.items():
        h = step * max(1.0, abs(value))
        plus, minus = dict(center), dict(center)
        plus[key] += h
        minus[key] -= h
        derivative = (_finite(function(plus)) - _finite(function(minus))) / (2 * h)
        normalized = derivative * value / baseline if baseline != 0 else None
        results.append(SensitivityResult(key, derivative, normalized))
    return tuple(results)


@dataclass(frozen=True, slots=True)
class CalibrationBin:
    count: int
    mean_probability: float
    observed_frequency: float


@dataclass(frozen=True, slots=True)
class CalibrationMetrics:
    brier_score: float
    expected_calibration_error: float
    bins: tuple[CalibrationBin, ...]
    sample_count: int


def calibration_metrics(
    probabilities: Sequence[float], outcomes: Sequence[int], *, bins: int = 10,
) -> CalibrationMetrics:
    """Binary probability calibration via Brier score and equal-width expected calibration error."""
    if len(probabilities) != len(outcomes) or not probabilities:
        raise ValueError("Probabilities and outcomes must have equal non-zero length")
    if isinstance(bins, bool) or not 1 <= bins <= 100:
        raise ValueError("bins must be between 1 and 100")
    probs = [_finite(p, "probability") for p in probabilities]
    if any(p < 0 or p > 1 for p in probs):
        raise ValueError("Probabilities must lie in [0, 1]")
    if any(isinstance(y, bool) or y not in (0, 1) for y in outcomes):
        raise ValueError("Binary outcomes must be integer 0 or 1")
    brier = math.fsum((p - y) ** 2 for p, y in zip(probs, outcomes, strict=True)) / len(probs)
    grouped: list[list[tuple[float, int]]] = [[] for _ in range(bins)]
    for probability, outcome in zip(probs, outcomes, strict=True):
        index = min(bins - 1, int(probability * bins))
        grouped[index].append((probability, outcome))
    summaries = []
    ece = 0.0
    for group in grouped:
        if not group:
            continue
        mean_p = math.fsum(p for p, _ in group) / len(group)
        observed = math.fsum(y for _, y in group) / len(group)
        ece += len(group) / len(probs) * abs(mean_p - observed)
        summaries.append(CalibrationBin(len(group), mean_p, observed))
    return CalibrationMetrics(brier, ece, tuple(summaries), len(probs))
