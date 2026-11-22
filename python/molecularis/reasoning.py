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
from dataclasses import dataclass, field
from typing import Mapping, Sequence

from .knowledge import DIMENSIONLESS, Dimension


def _finite(value: float, name: str = "value") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside the finite floating-point range") from exc
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
        if not isinstance(self.constraint_id, str) or not self.constraint_id.strip() or self.operator not in {"<=", ">=", "=="}:
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
        if not isinstance(self.objective_id, str) or not self.objective_id.strip() or self.direction not in {"minimize", "maximize"}:
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
    identifiers = [constraint.constraint_id for constraint in constraints]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Constraint IDs must be unique within an evaluation")
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
    if any(not isinstance(name, str) or not name.strip() for name in bounds):
        raise ValueError("Optimization variable names must be non-empty strings")
    objective_ids = [objective.objective_id for objective in objectives]
    if len(objective_ids) != len(set(objective_ids)):
        raise ValueError("Objective IDs must be unique")
    if len(bounds) > 8 or isinstance(points_per_dimension, bool) or not isinstance(points_per_dimension, int) or not 2 <= points_per_dimension <= 1000:
        raise ValueError("Grid search supports 1–8 dimensions and 2–1000 integer points per dimension")
    if isinstance(max_evaluations, bool) or not isinstance(max_evaluations, int) or not 1 <= max_evaluations <= 1_000_000:
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
        if not self.assumptions or any(not isinstance(item, str) or not item.strip() for item in self.assumptions):
            raise ValueError("Task assumptions must be explicit non-empty strings")
        if isinstance(self.max_candidates, bool) or not isinstance(self.max_candidates, int) or not 1 <= self.max_candidates <= 1000:
            raise ValueError("max_candidates must be an integer between 1 and 1000")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or not 0 <= self.seed <= 2**32 - 1:
            raise ValueError("seed must be an unsigned 32-bit integer")


@dataclass(frozen=True, slots=True)
class ConstructionCandidate:
    candidate_id: str
    domain: str
    representation: Mapping[str, object]
    assumptions: tuple[str, ...]
    evidence_refs: tuple[str, ...] = ()
    uncertainty: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.candidate_id, str) or not self.candidate_id.strip():
            raise ValueError("Candidate identity is required")
        if not isinstance(self.domain, str) or not self.domain.strip():
            raise ValueError("Candidate domain is required")
        if not isinstance(self.representation, Mapping) or not self.representation:
            raise ValueError("Candidate representation must be a non-empty mapping")
        if not self.assumptions or any(not isinstance(item, str) or not item.strip() for item in self.assumptions):
            raise ValueError("Candidate assumptions must be explicit non-empty strings")
        if any(not isinstance(ref, str) or not ref.strip() for ref in self.evidence_refs):
            raise ValueError("Candidate evidence references must be non-empty strings")
        if any(not isinstance(key, str) or not key.strip() or _finite(value, key) < 0 for key, value in self.uncertainty.items()):
            raise ValueError("Candidate uncertainty values must be finite and non-negative")
        # Canonical JSON validation rejects non-serializable objects and NaN/Infinity.
        try:
            self.digest
        except (TypeError, ValueError) as exc:
            raise ValueError("Candidate representation must be finite JSON-compatible data") from exc

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



@dataclass(frozen=True, slots=True)
class LinearSystemResult:
    solution: tuple[float, ...]
    residual_inf_norm: float
    minimum_pivot: float
    converged: bool
    method: str = "gaussian-elimination-partial-pivoting-v1"


def solve_linear_system(
    matrix: Sequence[Sequence[float]], vector: Sequence[float], *, pivot_tolerance: float = 1e-12,
) -> LinearSystemResult:
    """Solve a small dense square system using Gaussian elimination and partial pivoting."""
    n = len(vector)
    if n == 0 or n > 2048 or len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Matrix must be square, match the vector length and contain 1 to 2048 rows")
    a = [[_finite(value, "matrix value") for value in row] for row in matrix]
    b = [_finite(value, "vector value") for value in vector]
    tolerance = _finite(pivot_tolerance)
    if tolerance <= 0:
        raise ValueError("pivot_tolerance must be positive")
    min_pivot = math.inf
    for column in range(n):
        pivot_row = max(range(column, n), key=lambda row: abs(a[row][column]))
        pivot = abs(a[pivot_row][column])
        if pivot <= tolerance:
            raise ValueError("Matrix is singular or numerically rank deficient at the selected tolerance")
        min_pivot = min(min_pivot, pivot)
        if pivot_row != column:
            a[column], a[pivot_row] = a[pivot_row], a[column]
            b[column], b[pivot_row] = b[pivot_row], b[column]
        diagonal = a[column][column]
        for row in range(column + 1, n):
            factor = a[row][column] / diagonal
            a[row][column] = 0.0
            for j in range(column + 1, n):
                a[row][j] -= factor * a[column][j]
            b[row] -= factor * b[column]
    solution = [0.0] * n
    for row in range(n - 1, -1, -1):
        solution[row] = _finite((b[row] - math.fsum(a[row][j] * solution[j] for j in range(row + 1, n))) / a[row][row], "linear solution")
    residual = max(
        abs(math.fsum(_finite(matrix[i][j]) * solution[j] for j in range(n)) - _finite(vector[i]))
        for i in range(n)
    )
    return LinearSystemResult(tuple(solution), residual, min_pivot, math.isfinite(residual))


@dataclass(frozen=True, slots=True)
class IntegrationResult:
    value: float
    estimated_absolute_error: float
    intervals: int
    tolerance: float
    converged: bool
    method: str = "composite-simpson-richardson-v1"


def integrate_simpson(
    function, lower: float, upper: float, *, tolerance: float = 1e-8,
    intervals: int = 16, max_intervals: int = 1_000_000,
) -> IntegrationResult:
    """Composite Simpson integration with doubled-grid Richardson error estimate."""
    a, b = _finite(lower, "lower"), _finite(upper, "upper")
    tol = _finite(tolerance, "tolerance")
    if tol <= 0 or isinstance(intervals, bool) or not isinstance(intervals, int) or intervals < 2 or intervals % 2:
        raise ValueError("Tolerance must be positive and intervals must be a positive even integer")
    if isinstance(max_intervals, bool) or not isinstance(max_intervals, int) or max_intervals > 1_000_000 or max_intervals < intervals * 2:
        raise ValueError("max_intervals must allow at least one refinement and be at most 1,000,000")
    if a == b:
        return IntegrationResult(0.0, 0.0, intervals, tol, True)
    n = intervals

    def simpson(count: int) -> float:
        width = (b - a) / count
        total = _finite(function(a)) + _finite(function(b))
        total += 4 * math.fsum(_finite(function(a + i * width)) for i in range(1, count, 2))
        total += 2 * math.fsum(_finite(function(a + i * width)) for i in range(2, count, 2))
        return _finite(total * width / 3, "integral")

    coarse = simpson(n)
    while n * 2 <= max_intervals:
        n *= 2
        refined = simpson(n)
        error = abs(refined - coarse) / 15
        if error <= tol:
            return IntegrationResult(refined, error, n, tol, True)
        coarse = refined
    return IntegrationResult(coarse, error if n > intervals else math.inf, n, tol, False)


@dataclass(frozen=True, slots=True)
class GraphEdge:
    source: str
    target: str


@dataclass(frozen=True, slots=True)
class ScientificGraph:
    """Deterministic simple graph with bounded, explicit node and edge identities."""

    nodes: tuple[str, ...]
    edges: tuple[GraphEdge, ...]
    directed: bool = False

    def __post_init__(self) -> None:
        if not self.nodes or len(self.nodes) > 100000:
            raise ValueError("Graph must contain 1 to 100,000 nodes")
        if any(not isinstance(n, str) or not n.strip() for n in self.nodes) or len(set(self.nodes)) != len(self.nodes):
            raise ValueError("Graph node IDs must be unique non-empty strings")
        if len(self.edges) > 1_000_000:
            raise ValueError("Graph exceeds one million edges")
        known = set(self.nodes)
        seen = set()
        for edge in self.edges:
            if edge.source not in known or edge.target not in known:
                raise ValueError("Graph edge references an unknown node")
            if edge.source == edge.target:
                raise ValueError("Self-loops are not supported by this simple graph contract")
            key = (edge.source, edge.target) if self.directed else tuple(sorted((edge.source, edge.target)))
            if key in seen:
                raise ValueError("Duplicate graph edge")
            seen.add(key)

    def adjacency(self) -> dict[str, tuple[str, ...]]:
        links: dict[str, set[str]] = {node: set() for node in self.nodes}
        for edge in self.edges:
            links[edge.source].add(edge.target)
            if not self.directed:
                links[edge.target].add(edge.source)
        return {node: tuple(sorted(neighbors)) for node, neighbors in links.items()}

    def degrees(self) -> dict[str, int]:
        adjacency = self.adjacency()
        return {node: len(adjacency[node]) for node in self.nodes}

    def connected_components(self) -> tuple[tuple[str, ...], ...]:
        """Return ordinary components for undirected graphs and weak components for directed graphs."""
        adjacency: dict[str, set[str]] = {node: set() for node in self.nodes}
        for edge in self.edges:
            adjacency[edge.source].add(edge.target)
            adjacency[edge.target].add(edge.source)
        unseen = set(self.nodes)
        components = []
        while unseen:
            start = min(unseen)
            stack, found = [start], []
            unseen.remove(start)
            while stack:
                node = stack.pop()
                found.append(node)
                for neighbor in adjacency[node]:
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        stack.append(neighbor)
            components.append(tuple(sorted(found)))
        return tuple(components)

    def shortest_path(self, source: str, target: str) -> tuple[str, ...] | None:
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("Path endpoints must exist in graph")
        adjacency = self.adjacency()
        queue = [source]
        parents: dict[str, str | None] = {source: None}
        cursor = 0
        while cursor < len(queue):
            node = queue[cursor]
            cursor += 1
            if node == target:
                path = []
                current: str | None = target
                while current is not None:
                    path.append(current)
                    current = parents[current]
                return tuple(reversed(path))
            for neighbor in adjacency[node]:
                if neighbor not in parents:
                    parents[neighbor] = node
                    queue.append(neighbor)
        return None

    def cycle_rank(self) -> int:
        if self.directed:
            raise ValueError("Cycle rank is defined here only for undirected graphs")
        return len(self.edges) - len(self.nodes) + len(self.connected_components())


@dataclass(frozen=True, slots=True)
class Vector3:
    x: float
    y: float
    z: float
    unit: str = "m"
    coordinate_system: str = "cartesian"

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _finite(self.x, "x"))
        object.__setattr__(self, "y", _finite(self.y, "y"))
        object.__setattr__(self, "z", _finite(self.z, "z"))
        if not self.unit.strip() or not self.coordinate_system.strip():
            raise ValueError("Vector unit and coordinate system must be non-empty")

    def _compatible(self, other: "Vector3") -> None:
        if self.unit != other.unit or self.coordinate_system != other.coordinate_system:
            raise ValueError("Vector operations require matching units and coordinate systems")

    def norm(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def dot(self, other: "Vector3") -> float:
        self._compatible(other)
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3") -> "Vector3":
        self._compatible(other)
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
            self.unit, self.coordinate_system,
        )

    def distance(self, other: "Vector3") -> float:
        self._compatible(other)
        return Vector3(
            self.x - other.x, self.y - other.y, self.z - other.z,
            self.unit, self.coordinate_system,
        ).norm()

    def angle_degrees(self, other: "Vector3") -> float:
        denominator = self.norm() * other.norm()
        if denominator == 0:
            raise ValueError("Angle is undefined for a zero-length vector")
        cosine = max(-1.0, min(1.0, self.dot(other) / denominator))
        return math.degrees(math.acos(cosine))

    @classmethod
    def centroid(cls, points: Sequence["Vector3"]) -> "Vector3":
        if not points:
            raise ValueError("Centroid requires at least one point")
        first = points[0]
        for point in points[1:]:
            first._compatible(point)
        n = len(points)
        return cls(
            math.fsum(p.x for p in points) / n,
            math.fsum(p.y for p in points) / n,
            math.fsum(p.z for p in points) / n,
            first.unit, first.coordinate_system,
        )


# Reference statistical inference primitives (P2). Assumptions are explicit in result records.
@dataclass(frozen=True, slots=True)
class HypothesisTestResult:
    method: str
    statistic: float
    degrees_of_freedom: float
    p_value: float
    alternative: str
    sample_sizes: tuple[int, int]
    assumptions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RegressionResult:
    intercept: float
    slope: float
    r_squared: float
    slope_standard_error: float
    slope_ci: tuple[float, float]
    slope_p_value: float
    degrees_of_freedom: int
    sample_count: int
    assumptions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MultipleTestingResult:
    method: str
    adjusted_p_values: tuple[float, ...]
    rejected: tuple[bool, ...]
    alpha: float


@dataclass(frozen=True, slots=True)
class SampleSizeResult:
    method: str
    per_group: int
    total: int
    alpha: float
    power: float
    standardized_effect: float
    assumptions: tuple[str, ...]


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    """Modified Lentz continued fraction for the incomplete beta function."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    tiny = 1e-300
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 201):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny: d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny: c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny: d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny: c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) <= 3e-14:
            return h
    raise ArithmeticError("Incomplete beta continued fraction did not converge")


def _regularized_beta(x: float, a: float, b: float) -> float:
    if not (a > 0 and b > 0 and 0 <= x <= 1):
        raise ValueError("Invalid regularized beta arguments")
    if x == 0: return 0.0
    if x == 1: return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return front * _beta_continued_fraction(a, b, x) / a
    return 1.0 - front * _beta_continued_fraction(b, a, 1 - x) / b


def _student_t_cdf(value: float, degrees: float) -> float:
    if degrees <= 0:
        raise ValueError("Degrees of freedom must be positive")
    if value == 0: return 0.5
    tail = 0.5 * _regularized_beta(degrees / (degrees + value * value), degrees / 2, 0.5)
    return 1 - tail if value > 0 else tail


def _student_t_quantile(probability: float, degrees: float) -> float:
    if not 0 < probability < 1 or degrees <= 0:
        raise ValueError("Invalid Student-t quantile arguments")
    if probability == 0.5: return 0.0
    sign = 1.0 if probability > 0.5 else -1.0
    target = max(probability, 1 - probability)
    lo, hi = 0.0, 1.0
    while _student_t_cdf(hi, degrees) < target and hi < 1e8:
        hi *= 2
    for _ in range(160):
        mid = (lo + hi) / 2
        if _student_t_cdf(mid, degrees) < target: lo = mid
        else: hi = mid
    return sign * (lo + hi) / 2


def welch_t_test(
    first: Sequence[float], second: Sequence[float], *, alternative: str = "two-sided",
) -> HypothesisTestResult:
    """Welch independent-samples t-test; unequal variances are not pooled."""
    if alternative not in {"two-sided", "less", "greater"}:
        raise ValueError("alternative must be two-sided, less or greater")
    x, y = [_finite(v) for v in first], [_finite(v) for v in second]
    if len(x) < 2 or len(y) < 2:
        raise ValueError("Welch test requires at least two observations per group")
    mx, my = math.fsum(x) / len(x), math.fsum(y) / len(y)
    vx = math.fsum((v - mx) ** 2 for v in x) / (len(x) - 1)
    vy = math.fsum((v - my) ** 2 for v in y) / (len(y) - 1)
    ax, by = vx / len(x), vy / len(y)
    se2 = ax + by
    if se2 == 0:
        raise ValueError("Welch test is undefined when both groups have zero variance")
    statistic = (mx - my) / math.sqrt(se2)
    df = se2 * se2 / (ax * ax / (len(x) - 1) + by * by / (len(y) - 1))
    cdf = _student_t_cdf(statistic, df)
    p = 2 * min(cdf, 1 - cdf) if alternative == "two-sided" else (cdf if alternative == "less" else 1 - cdf)
    return HypothesisTestResult(
        "welch_two_sample_t_v1", statistic, df, min(1.0, max(0.0, p)), alternative,
        (len(x), len(y)),
        ("Independent observations", "Approximately normal sampling distribution or adequate sample sizes", "Unequal group variances allowed"),
    )


def simple_linear_regression(
    x: Sequence[float], y: Sequence[float], *, confidence: float = 0.95,
) -> RegressionResult:
    """Ordinary least squares for one predictor with classical homoskedastic SE."""
    if len(x) != len(y) or len(x) < 3:
        raise ValueError("Regression requires equal-length vectors and at least three observations")
    level = _finite(confidence)
    if not 0 < level < 1: raise ValueError("confidence must lie in (0, 1)")
    xs, ys = [_finite(v) for v in x], [_finite(v) for v in y]
    mx, my = math.fsum(xs) / len(xs), math.fsum(ys) / len(ys)
    sxx = math.fsum((v - mx) ** 2 for v in xs)
    if sxx == 0: raise ValueError("Predictor must have non-zero variance")
    slope = math.fsum((a - mx) * (b - my) for a, b in zip(xs, ys, strict=True)) / sxx
    intercept = my - slope * mx
    residuals = [b - (intercept + slope * a) for a, b in zip(xs, ys, strict=True)]
    sse = math.fsum(v * v for v in residuals)
    sst = math.fsum((v - my) ** 2 for v in ys)
    df = len(xs) - 2
    se = math.sqrt((sse / df) / sxx)
    if se == 0:
        p = 0.0 if slope != 0 else 1.0
        critical = 0.0
    else:
        statistic = slope / se
        p = 2 * min(_student_t_cdf(statistic, df), 1 - _student_t_cdf(statistic, df))
        critical = _student_t_quantile((1 + level) / 2, df)
    return RegressionResult(
        intercept, slope, 1.0 if sst == 0 and sse == 0 else (1 - sse / sst if sst else 0.0),
        se, (slope - critical * se, slope + critical * se), p, df, len(xs),
        ("Independent errors", "Linear conditional mean", "Homoskedastic errors for classical standard error and interval", "No influential unmodelled dependence"),
    )


def benjamini_hochberg(p_values: Sequence[float], *, alpha: float = 0.05) -> MultipleTestingResult:
    """Benjamini-Hochberg step-up FDR control under independence/positive dependence."""
    values = [_finite(p, "p-value") for p in p_values]
    level = _finite(alpha)
    if not values or not 0 < level < 1 or any(p < 0 or p > 1 for p in values):
        raise ValueError("Require p-values in [0,1] and alpha in (0,1)")
    order = sorted(range(len(values)), key=lambda i: (values[i], i))
    m = len(values)
    adjusted = [1.0] * m
    running = 1.0
    for rank_index in range(m - 1, -1, -1):
        index = order[rank_index]
        running = min(running, values[index] * m / (rank_index + 1))
        adjusted[index] = min(1.0, running)
    rejected = [False] * m
    last = -1
    for rank_index, index in enumerate(order):
        if values[index] <= level * (rank_index + 1) / m:
            last = rank_index
    for rank_index in range(last + 1):
        rejected[order[rank_index]] = True
    return MultipleTestingResult("benjamini_hochberg_fdr_v1", tuple(adjusted), tuple(rejected), level)


def normal_two_group_sample_size(
    standardized_effect: float, *, alpha: float = 0.05, power: float = 0.8,
) -> SampleSizeResult:
    """Normal-approximation sample size for equal-sized, two-sided independent groups."""
    effect, level, target_power = _finite(standardized_effect), _finite(alpha), _finite(power)
    if effect <= 0 or not 0 < level < 1 or not 0 < target_power < 1:
        raise ValueError("Effect must be positive; alpha and power must lie in (0,1)")
    def normal_quantile(p: float) -> float:
        lo, hi = -10.0, 10.0
        for _ in range(120):
            mid = (lo + hi) / 2
            cdf = 0.5 * (1 + math.erf(mid / math.sqrt(2)))
            if cdf < p: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    z_alpha = normal_quantile(1 - level / 2)
    z_power = normal_quantile(target_power)
    n = math.ceil(2 * (z_alpha + z_power) ** 2 / (effect * effect))
    return SampleSizeResult(
        "normal_two_independent_groups_v1", n, 2 * n, level, target_power, effect,
        ("Equal allocation", "Independent observations", "Continuous outcome", "Normal approximation; no attrition adjustment"),
    )



@dataclass(frozen=True, slots=True)
class VerificationCheck:
    check_id: str
    passed: bool
    claim: str
    details: str = ""

    def __post_init__(self) -> None:
        if not self.check_id.strip() or not self.claim.strip():
            raise ValueError("Verification checks require an ID and claim")
        if not isinstance(self.passed, bool):
            raise TypeError("Verification outcome must be boolean")


@dataclass(frozen=True, slots=True)
class IndependentVerification:
    verifier_id: str
    method: str
    checks: tuple[VerificationCheck, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.verifier_id.strip() or not self.method.strip():
            raise ValueError("Independent verifier identity and method are required")
        if not self.checks:
            raise ValueError("At least one independent verification check is required")
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("Independent verification requires evidence references")

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)


@dataclass(frozen=True, slots=True)
class ConstructionAuditResult:
    candidate_digest: str
    prepublication: FeasibilityReport
    independent_verification: IndependentVerification
    publishable: bool


def audit_and_verify_candidate(
    task: ConstructionTask,
    candidate: ConstructionCandidate,
    *,
    proposer_id: str,
    proposer_method: str,
    verifier_id: str,
    verifier_method: str,
    verifier,
) -> ConstructionAuditResult:
    """Run prechecks and a separately identified verifier before declaring a candidate publishable.

    Distinct identities/method labels are a contract-level separation, not proof of institutional
    independence. Deployments must enforce process, credential and implementation separation.
    """
    if not proposer_id.strip() or not proposer_method.strip():
        raise ValueError("Proposer identity and method are required")
    if verifier_id.strip() == proposer_id.strip():
        raise ValueError("Proposer and verifier identities must differ")
    if not verifier_method.strip() or verifier_method.strip() == proposer_method.strip():
        raise ValueError("Verifier must declare a distinct method")
    if not callable(verifier):
        raise TypeError("An independent verifier callable is required")
    if not candidate.evidence_refs:
        raise ValueError("Candidate source/evidence references are required for publication")
    precheck = audit_candidate(task, candidate)
    if not precheck.feasible:
        raise ValueError("Candidate failed pre-publication hard constraints")
    result = verifier(candidate)
    if not isinstance(result, IndependentVerification):
        raise TypeError("Verifier must return an IndependentVerification result")
    if result.verifier_id != verifier_id or result.method != verifier_method:
        raise ValueError("Verifier result identity/method does not match the declared verifier")
    return ConstructionAuditResult(
        candidate.digest, precheck, result, precheck.feasible and result.passed,
    )



@dataclass(frozen=True, slots=True)
class BetaBinomialPosterior:
    prior_alpha: float
    prior_beta: float
    successes: int
    failures: int
    posterior_alpha: float
    posterior_beta: float
    posterior_mean: float
    credible_interval: tuple[float, float]
    credible_level: float
    method: str = "beta_binomial_conjugate_v1"
    assumptions: tuple[str, ...] = (
        "Binary exchangeable outcomes",
        "Conditional Bernoulli likelihood",
        "Beta prior parameters explicitly supplied",
    )


def _beta_quantile(probability: float, alpha: float, beta: float) -> float:
    if not 0 < probability < 1:
        raise ValueError("Beta quantile probability must lie in (0,1)")
    lo, hi = 0.0, 1.0
    for _ in range(160):
        mid = (lo + hi) / 2
        if _regularized_beta(mid, alpha, beta) < probability:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def beta_binomial_posterior(
    successes: int, trials: int, *, prior_alpha: float, prior_beta: float,
    credible_level: float = 0.95,
) -> BetaBinomialPosterior:
    """Conjugate Bayesian inference for a Bernoulli rate with an explicit Beta prior."""
    if isinstance(successes, bool) or not isinstance(successes, int):
        raise ValueError("successes must be an integer")
    if isinstance(trials, bool) or not isinstance(trials, int) or trials < 0 or not 0 <= successes <= trials:
        raise ValueError("trials must be non-negative and successes must lie between zero and trials")
    a, b = _finite(prior_alpha, "prior_alpha"), _finite(prior_beta, "prior_beta")
    level = _finite(credible_level, "credible_level")
    if a <= 0 or b <= 0 or not 0 < level < 1:
        raise ValueError("Beta prior parameters must be positive and credible level in (0,1)")
    post_a, post_b = a + successes, b + trials - successes
    tail = (1 - level) / 2
    interval = (_beta_quantile(tail, post_a, post_b), _beta_quantile(1 - tail, post_a, post_b))
    return BetaBinomialPosterior(
        a, b, successes, trials - successes, post_a, post_b,
        post_a / (post_a + post_b), interval, level,
    )
