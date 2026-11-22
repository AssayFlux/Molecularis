from __future__ import annotations

import math

import pytest

from molecularis.knowledge import LENGTH, TIME
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
    wrong = ConstructionCandidate("c2", "chemistry", {"length": 4}, ("wrong-domain candidate",))
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



def test_bootstrap_interval_is_reproducible_and_contains_sample_mean() -> None:
    from molecularis.reasoning import bootstrap_mean_interval

    one = bootstrap_mean_interval([1, 2, 3, 4, 5], resamples=1000, seed=23)
    two = bootstrap_mean_interval([1, 2, 3, 4, 5], resamples=1000, seed=23)
    assert one == two
    assert one.lower <= one.estimate <= one.upper


def test_sensitivity_and_probability_calibration_reference_cases() -> None:
    from molecularis.reasoning import calibration_metrics, local_sensitivity

    sensitivity = local_sensitivity(lambda p: p["x"] ** 2, {"x": 3})[0]
    assert sensitivity.derivative == pytest.approx(6, rel=1e-5)
    assert sensitivity.normalized_sensitivity == pytest.approx(2)
    calibration = calibration_metrics([0.1, 0.2, 0.8, 0.9], [0, 0, 1, 1], bins=2)
    assert calibration.brier_score == pytest.approx(0.025)
    assert calibration.expected_calibration_error == pytest.approx(0.15)
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        calibration_metrics([1.1], [1])



def test_linear_system_solver_and_singularity_diagnostics() -> None:
    from molecularis.reasoning import solve_linear_system

    result = solve_linear_system([[3, 2], [1, 2]], [5, 5])
    assert result.solution == pytest.approx((0, 2.5))
    assert result.residual_inf_norm < 1e-12
    with pytest.raises(ValueError, match="singular"):
        solve_linear_system([[1, 2], [2, 4]], [3, 6])


def test_simpson_integration_reports_error_and_convergence() -> None:
    from molecularis.reasoning import integrate_simpson

    result = integrate_simpson(lambda x: x**3, 0, 1, tolerance=1e-10, intervals=4)
    assert result.converged
    assert result.value == pytest.approx(0.25, abs=1e-12)
    assert result.estimated_absolute_error <= result.tolerance


def test_graph_topology_primitives_are_deterministic() -> None:
    from molecularis.reasoning import GraphEdge, ScientificGraph

    graph = ScientificGraph(
        ("a", "b", "c", "d"),
        (GraphEdge("a", "b"), GraphEdge("b", "c"), GraphEdge("c", "a")),
    )
    assert graph.degrees() == {"a": 2, "b": 2, "c": 2, "d": 0}
    assert graph.connected_components() == (("a", "b", "c"), ("d",))
    assert graph.shortest_path("a", "c") == ("a", "c")
    assert graph.cycle_rank() == 1
    with pytest.raises(ValueError, match="Duplicate"):
        ScientificGraph(("a", "b"), (GraphEdge("a", "b"), GraphEdge("b", "a")))


def test_vector_geometry_enforces_coordinate_and_unit_compatibility() -> None:
    from molecularis.reasoning import Vector3

    x_axis = Vector3(1, 0, 0, "nm", "cartesian")
    y_axis = Vector3(0, 1, 0, "nm", "cartesian")
    assert x_axis.norm() == 1
    assert x_axis.dot(y_axis) == 0
    assert x_axis.cross(y_axis) == Vector3(0, 0, 1, "nm", "cartesian")
    assert x_axis.angle_degrees(y_axis) == pytest.approx(90)
    assert x_axis.distance(y_axis) == pytest.approx(math.sqrt(2))
    assert Vector3.centroid([x_axis, y_axis]) == Vector3(0.5, 0.5, 0, "nm", "cartesian")
    with pytest.raises(ValueError, match="matching units"):
        x_axis.distance(Vector3(1, 0, 0, "angstrom", "cartesian"))



def test_welch_t_test_reference_case_and_alternatives() -> None:
    from molecularis.reasoning import welch_t_test

    result = welch_t_test([10, 11, 12, 13, 14], [1, 2, 3, 4, 5])
    assert result.statistic == pytest.approx(9.0)
    assert result.degrees_of_freedom == pytest.approx(8.0)
    assert result.p_value == pytest.approx(1.85311843e-5, rel=1e-6)
    assert result.alternative == "two-sided"
    assert welch_t_test([1, 2, 3], [4, 5, 6], alternative="less").p_value < 0.1
    with pytest.raises(ValueError):
        welch_t_test([1], [2, 3])


def test_simple_linear_regression_reference_and_constant_predictor() -> None:
    from molecularis.reasoning import simple_linear_regression

    result = simple_linear_regression([1, 2, 3, 4, 5], [3.1, 4.9, 7.2, 8.8, 11.1])
    assert result.slope == pytest.approx(2.0, abs=0.1)
    assert result.intercept == pytest.approx(1.0, abs=0.3)
    assert result.r_squared > 0.99
    assert result.slope_ci[0] < result.slope < result.slope_ci[1]
    assert result.slope_p_value < 0.001
    with pytest.raises(ValueError, match="variance"):
        simple_linear_regression([1, 1, 1], [1, 2, 3])


def test_benjamini_hochberg_controls_fdr_and_preserves_input_order() -> None:
    from molecularis.reasoning import benjamini_hochberg

    result = benjamini_hochberg([0.01, 0.04, 0.03, 0.2], alpha=0.05)
    assert result.adjusted_p_values == pytest.approx((0.04, 0.0533333333, 0.0533333333, 0.2))
    assert result.rejected == (True, False, False, False)
    with pytest.raises(ValueError):
        benjamini_hochberg([0.01, 1.2])


def test_experiment_design_sample_size_reference_case() -> None:
    from molecularis.reasoning import normal_two_group_sample_size

    result = normal_two_group_sample_size(0.5, alpha=0.05, power=0.8)
    assert result.per_group == 63
    assert result.total == 126
    assert "Normal approximation; no attrition adjustment" in result.assumptions


def test_student_t_distribution_reference_quantile() -> None:
    from molecularis.reasoning import _student_t_cdf, _student_t_quantile

    assert _student_t_cdf(0, 10) == 0.5
    assert _student_t_cdf(2.22813885, 10) == pytest.approx(0.975, abs=1e-7)
    assert _student_t_quantile(0.975, 10) == pytest.approx(2.22813885, abs=1e-7)



def test_independent_verifier_contract_requires_separate_identity_method_and_evidence() -> None:
    from molecularis.reasoning import (
        IndependentVerification, VerificationCheck, audit_and_verify_candidate,
    )

    task = ConstructionTask("task-v", "sequence", "reconstruction", "valid sequence", ("alphabet ACGT",))
    candidate = ConstructionCandidate("candidate-v", "sequence", {"length": 4}, ("input fixed",), ("source:ref-1",))
    def verifier(item):
        assert item.digest == candidate.digest
        return IndependentVerification(
            "verifier-2", "independent alphabet scan",
            (VerificationCheck("alphabet", True, "Only A/C/G/T symbols"),),
            ("validation:sequence-rulebook-v1",),
        )
    result = audit_and_verify_candidate(
        task, candidate, proposer_id="proposer-1", proposer_method="candidate sampler",
        verifier_id="verifier-2", verifier_method="independent alphabet scan", verifier=verifier,
    )
    assert result.publishable
    assert result.candidate_digest == candidate.digest
    assert result.independent_verification.passed
    with pytest.raises(ValueError, match="identities must differ"):
        audit_and_verify_candidate(
            task, candidate, proposer_id="same", proposer_method="generator",
            verifier_id="same", verifier_method="checker", verifier=verifier,
        )


def test_independent_verification_failure_blocks_publication() -> None:
    from molecularis.reasoning import IndependentVerification, VerificationCheck, audit_and_verify_candidate

    task = ConstructionTask("task-v2", "chemistry", "exploration", "formula valid", ("integer atom counts",))
    candidate = ConstructionCandidate("candidate-v2", "chemistry", {"C": 2, "H": 6}, ("neutral formula",), ("source:formula-input",))
    result = audit_and_verify_candidate(
        task, candidate, proposer_id="generator", proposer_method="formula builder",
        verifier_id="checker", verifier_method="element count parser",
        verifier=lambda _: IndependentVerification(
            "checker", "element count parser",
            (VerificationCheck("valence", False, "Valence model check", "not evaluated"),),
            ("rulebook:chemistry-v1",),
        ),
    )
    assert not result.publishable



def test_candidate_rejects_nonfinite_or_unserializable_representation() -> None:
    with pytest.raises(ValueError):
        ConstructionCandidate("bad", "sequence", {"score": math.nan}, ("exploratory assumption",))
    with pytest.raises(ValueError):
        ConstructionCandidate("bad2", "sequence", {"value": object()}, ("exploratory assumption",))


def test_independent_publication_requires_candidate_provenance() -> None:
    from molecularis.reasoning import IndependentVerification, VerificationCheck, audit_and_verify_candidate

    task = ConstructionTask("task-prov", "sequence", "exploration", "candidate validity", ("explicit search bounds",))
    candidate = ConstructionCandidate("candidate-prov", "sequence", {"length": 3}, ("exploratory hypothesis",))
    verifier = lambda _: IndependentVerification(
        "verifier", "independent check", (VerificationCheck("check", True, "candidate structure"),), ("audit:1",)
    )
    with pytest.raises(ValueError, match="source/evidence references"):
        audit_and_verify_candidate(
            task, candidate, proposer_id="proposer", proposer_method="sampler",
            verifier_id="verifier", verifier_method="independent check", verifier=verifier,
        )



def test_directed_graph_reports_weak_components_but_respects_direction_for_paths() -> None:
    from molecularis.reasoning import GraphEdge, ScientificGraph

    graph = ScientificGraph(("a", "b", "c"), (GraphEdge("a", "b"),), directed=True)
    assert graph.connected_components() == (("a", "b"), ("c",))
    assert graph.shortest_path("a", "b") == ("a", "b")
    assert graph.shortest_path("b", "a") is None


def test_duplicate_constraint_ids_are_rejected() -> None:
    constraint = ConstraintSpec("same", SymbolicExpression("x"), "<=", 1)
    with pytest.raises(ValueError, match="unique"):
        check_constraints((constraint, constraint), {"x": 0})



def test_beta_binomial_posterior_uses_explicit_prior_and_reference_case() -> None:
    from molecularis.reasoning import beta_binomial_posterior

    result = beta_binomial_posterior(5, 10, prior_alpha=1, prior_beta=1)
    assert result.posterior_alpha == 6
    assert result.posterior_beta == 6
    assert result.posterior_mean == pytest.approx(0.5)
    assert result.credible_interval[0] == pytest.approx(1 - result.credible_interval[1], abs=1e-10)
    assert 0.2 < result.credible_interval[0] < 0.4
    assert 0.6 < result.credible_interval[1] < 0.8
    assert result.assumptions[2] == "Beta prior parameters explicitly supplied"
    with pytest.raises(ValueError):
        beta_binomial_posterior(3, 2, prior_alpha=1, prior_beta=1)
