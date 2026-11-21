from __future__ import annotations

import pytest

from molecularis.scientific_core import (
    Candidate, RuleEngine, RuleSpec, ScientificArtifact, ScientificCore,
    ScientificGoal, ValidationFinding, content_digest,
)


def test_content_digest_is_order_independent_and_rejects_nan() -> None:
    assert content_digest({"b": 2, "a": 1}) == content_digest({"a": 1, "b": 2})
    with pytest.raises(ValueError):
        content_digest({"not_finite": float("nan")})


def test_artifact_digest_tracks_payload_and_schema() -> None:
    one = ScientificArtifact("a", "sequence", "v1", {"sequence": "ACGT"})
    two = ScientificArtifact("b", "sequence", "v1", {"sequence": "ACGA"})
    assert one.sha256 != two.sha256


def test_rule_engine_requires_review_approval_by_default() -> None:
    engine = RuleEngine()
    spec = RuleSpec("sequence.length", "1.0.0", "sequence", "Check sequence length")
    engine.register(spec, lambda inputs: {"length": len(str(inputs["sequence"]))})
    with pytest.raises(PermissionError):
        engine.evaluate("sequence.length", "1.0.0", {"sequence": "ACGT"})
    result = engine.evaluate(
        "sequence.length", "1.0.0", {"sequence": "ACGT"}, require_approved=False
    )
    assert result.passed is True
    assert result.output["length"] == 4


def test_approved_rule_requires_reviewer() -> None:
    with pytest.raises(ValueError, match="reviewer"):
        RuleSpec("x", "1", "test", "test", approval_state="approved")


class _Generator:
    generator_id = "test.generator"
    version = "1.0"

    def generate(self, goal: ScientificGoal, *, max_candidates: int):
        artifact = ScientificArtifact("candidate-1", "sequence", "v1", {"sequence": "ACGT"})
        yield Candidate(artifact, self.generator_id, self.version, 1.0, "score")


class _Validator:
    validator_id = "test.validator"
    version = "1.0"

    def validate(self, goal: ScientificGoal, artifact: ScientificArtifact):
        return [ValidationFinding(
            self.validator_id, self.version, "non_empty", bool(artifact.payload), "error",
            "Artifact payload is non-empty",
        )]


def _goal() -> ScientificGoal:
    return ScientificGoal("goal-1", "sequence", "construct", {"length": 4})


def test_generation_requires_separate_validator_and_records_provenance() -> None:
    run = ScientificCore().run(_goal(), _Generator(), [_Validator()])
    assert run.state == "validated"
    assert run.candidates[0].artifact.payload["sequence"] == "ACGT"
    assert run.reports[0].passed
    assert run.provenance["schema"] == "molecularis.generation-run.v1"


def test_generator_cannot_validate_itself() -> None:
    generator = _Generator()
    with pytest.raises(ValueError, match="own validator"):
        ScientificCore().run(_goal(), generator, [generator])  # type: ignore[list-item]


def test_candidate_count_is_enforced() -> None:
    class Many(_Generator):
        def generate(self, goal: ScientificGoal, *, max_candidates: int):
            for index in range(max_candidates + 1):
                artifact = ScientificArtifact(str(index), "sequence", "v1", {"sequence": str(index)})
                yield Candidate(artifact, self.generator_id, self.version)

    with pytest.raises(ValueError, match="exceeded"):
        ScientificCore().run(_goal(), Many(), [_Validator()], max_candidates=1)


def test_empty_validator_output_is_not_reported_as_a_pass() -> None:
    class EmptyValidator:
        validator_id = "empty.validator"
        version = "1.0"

        def validate(self, goal: ScientificGoal, artifact: ScientificArtifact):
            return []

    run = ScientificCore().run(_goal(), _Generator(), [EmptyValidator()])
    assert run.state == "validation_incomplete"
    assert run.reports[0].validation_state == "not_assessed"
    assert run.reports[0].passed is False
