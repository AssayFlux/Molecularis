from __future__ import annotations

import math

import pytest

from molecularis.knowledge import DIMENSIONLESS, LENGTH, TIME
from molecularis.reasoning import (
    ConstructionCandidate, ConstructionTask, ConstraintSpec, DerivationTrace,
    ObjectiveSpec, SymbolicExpression, audit_candidate, bisect_root,
    bounded_grid_search, check_constraints, describe, monte_carlo_uncertainty,
    pearson_correlation, propagate_independent_uncertainty,
)
from molecularis.scientific_core import (
    Candidate, ScientificArtifact, ScientificCore, ScientificGoal, ValidationFinding,
)


def test_safe_expression_evaluation_and_variable_discovery() -> None:
    expr = SymbolicExpression("(x + 2) * y / 4")
    assert expr.variables() == ("x", "y")
    assert expr.evaluate({"x": 2, "y": 8}) == 8
    with pytest.raises(ValueError, match="Missing expression variables"):
        expr.evaluate({"x": 1})


@pytest.mark.parametrize("source", [
    "__import__('os').system('id')", "x.real", "x[0]", "x if x else 0",
    "lambda: 1", "open('/etc/passwd')", "2 ** 100",
])
def test_expression_language_rejects_code_and_unsupported_syntax(source: str) -> None:
    with pytest.raises(ValueError):
        SymbolicExpression(source)


def test_dimensional_analysis_and_derivation_trace_are_deterministic() -> None:
    velocity = SymbolicExpression("distance / time")
    assert velocity.infer_dimension({"distance": LENGTH, "time": TIME}) == LENGTH / TIME
    with pytest.raises(ValueError, match="compatible dimensions"):
        SymbolicExpression("distance + time").infer_dimension({"distance": LENGTH, "time": TIME})
    trace = DerivationTrace.build([
        (velocity, {"distance": 10, "time": 2},
         {"distance": LENGTH, "time": TIME}, ("constant speed",)),
    ], source_refs=("lab-notebook:run-1",))
    same = DerivationTrace.build([
        (velocity, {"distance": 10, "time": 2},
         {"distance": LENGTH, "time": TIME}, ("constant speed",)),
    ], source_refs=("lab-notebook:run-1",))
    assert trace.steps[0].result == 5
    assert trace.steps[0].dimension == LENGTH / TIME
    assert trace.trace_id == same.trace_id


def test_bisection_reports_convergence_and_invalid_brackets() -> None:
    result = bisect_root(lambda x: x * x - 2, 0, 2, tolerance=1e-12)
    assert result.diagnostics.converged
    assert result.value == pytest.approx(math.sqrt(2), abs=1e-10)
    assert result.diagnostics.iterations > 0
    with pytest.raises(ValueError, match="not bracketed"):
        bisect_root(lambda x: x * x + 1, -1, 1)


def test_descriptive_statistics_and_correlation_reference_cases() -> None:
    stats = describe([1, 2, 3, 4])
    assert stats.mean == 2.5
    assert stats.variance == pytest.approx(5 / 3)
    assert stats.standard_deviation == pytest.approx(math.sqrt(5 / 3))
    assert pearson_correlation([1, 2, 3], [2, 4, 6]) == pytest.approx(1)
    with pytest.raises(ValueError, match="constant"):
        pearson_correlation([1, 1], [2, 3])


def test_uncertainty_propagation_first_order_and_seeded_monte_carlo() -> None:
    fn = lambda p: p["x"] * 2
    linear = propagate_independent_uncertainty(fn, {"x": 3}, {"x": 0.5})
    assert linear.estimate == 6
    assert linear.standard_uncertainty == pytest.approx(1)
    mc1 = monte_carlo_uncertainty(fn, {"x": 3}, {"x": 0.5}, samples=1000, seed=17)
    mc2 = monte_carlo_uncertainty(fn, {"x": 3}, {"x": 0.5}, samples=1000, seed=17)
    assert mc1 == mc2
    assert mc1.standard_uncertainty == pytest.approx(1, rel=0.12)
    assert mc1.interval_95 is not None


def test_constraints_and_bounded_optimization_respect_hard_limits() -> None:
    constraints = [ConstraintSpec("positive", SymbolicExpression("x"), ">=", 0)]
    assert check_constraints(constraints, {"x": 2}).feasible
    assert not check_constraints(constraints, {"x": -1}).feasible
    result = bounded_grid_search(
        {"x": (-2, 2)}, [ObjectiveSpec("distance", SymbolicExpression("(x - 1) ** 2"))],
        constraints, points_per_dimension=41,
    )
    assert result.feasible
    assert result.variables["x"] == pytest.approx(1)
    assert result.state == "optimal_on_grid"


def test_grid_search_budget_and_infeasible_states_are_explicit() -> None:
    exhausted = bounded_grid_search(
        {"x": (0, 1), "y": (0, 1)},
        [ObjectiveSpec("sum", SymbolicExpression("x + y"))],
        points_per_dimension=10, max_evaluations=5,
    )
    assert exhausted.state == "budget_exhausted"
    impossible = bounded_grid_search(
        {"x": (0, 1)}, [ObjectiveSpec("x", SymbolicExpression("x"))],
        [ConstraintSpec("impossible", SymbolicExpression("x"), ">=", 2)],
    )
    assert impossible.state == "no_feasible_candidate"
    assert not impossible.feasible


def test_construction_task_pre_audit_enforces_domain_and_constraints() -> None:
    task = ConstructionTask(
        "task-1", "sequence", "generalization", "build length 4",
        ("DNA alphabet",),
        (ConstraintSpec("length", SymbolicExpression("length"), "==", 4),),
    )
    candidate = ConstructionCandidate("c1", "sequence", {"length": 4, "gc": 0.5}, ("synthetic",))
    assert audit_candidate(task, candidate).feasible
    wrong = ConstructionCandidate("c2", "chemistry", {"length": 4}, ())
    with pytest.raises(ValueError, match="domain"):
        audit_candidate(task, wrong)


class _SequenceGenerator:
    generator_id = "p2.sequence.proposer"
    version = "1"

    def generate(self, goal: ScientificGoal, *, max_candidates: int):
        artifact = ScientificArtifact("seq-1", "sequence.candidate", "v1", {"sequence": "ACGT"})
        yield Candidate(artifact, self.generator_id, self.version)


class _SequenceVerifier:
    validator_id = "p2.sequence.verifier"
    version = "1"

    def validate(self, goal: ScientificGoal, artifact: ScientificArtifact):
        sequence = str(artifact.payload["sequence"])
        valid = bool(sequence) and set(sequence) <= set("ACGT")
        return [ValidationFinding(
            self.validator_id, self.version, "dna_alphabet", valid, "error",
            "DNA alphabet and non-empty sequence checked",
        )]


class _FormulaGenerator:
    generator_id = "p2.formula.proposer"
    version = "1"

    def generate(self, goal: ScientificGoal, *, max_candidates: int):
        artifact = ScientificArtifact(
            "formula-1", "chemical.formula.candidate", "v1",
            {"formula": "H2O", "element_counts": {"H": 2, "O": 1}, "atom_count": 3},
        )
        yield Candidate(artifact, self.generator_id, self.version)


class _FormulaVerifier:
    validator_id = "p2.formula.verifier"
    version = "1"

    def validate(self, goal: ScientificGoal, artifact: ScientificArtifact):
        counts = artifact.payload["element_counts"]
        valid = (
            isinstance(counts, dict)
            and all(isinstance(v, int) and v > 0 for v in counts.values())
            and sum(counts.values()) == artifact.payload["atom_count"]
        )
        return [ValidationFinding(
            self.validator_id, self.version, "formula_atom_count", valid, "error",
            "Element-count sum agrees with declared atom count",
        )]


@pytest.mark.parametrize(
    ("domain", "generator", "verifier"),
    [
        ("sequence", _SequenceGenerator(), _SequenceVerifier()),
        ("chemistry", _FormulaGenerator(), _FormulaVerifier()),
    ],
)
def test_two_domain_construction_has_separate_verification(domain, generator, verifier) -> None:
    goal = ScientificGoal(f"{domain}-goal", domain, "construct reference candidate", {"mode": "bounded"})
    run = ScientificCore().run(goal, generator, [verifier])
    assert run.state == "validated"
    assert run.reports[0].passed
    assert run.provenance["generator"]["id"] != run.provenance["validators"][0]["id"]
