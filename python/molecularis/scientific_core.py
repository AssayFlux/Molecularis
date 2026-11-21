"""Molecularis-owned scientific rule, generation and validation kernel.

The kernel is deliberately domain-neutral and dependency-free. Domain packages provide
scientific object schemas, rule implementations, generators and independent validators.
This module owns execution contracts, deterministic provenance and failure semantics.
It does not claim that a passing rule set establishes experimental truth.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence


JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
RuleFunction = Callable[[Mapping[str, JsonValue]], Mapping[str, JsonValue]]


def _canonical(value: Any, *, max_bytes: int = 8_000_000) -> str:
    """Serialize JSON-compatible scientific data canonically and reject NaN/Infinity."""
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Scientific payload must contain finite JSON-compatible values") from exc
    if len(encoded.encode("utf-8")) > max_bytes:
        raise ValueError(f"Scientific payload exceeds {max_bytes} bytes")
    return encoded


def content_digest(value: Any, *, max_bytes: int = 8_000_000) -> str:
    """Return SHA-256 over canonical JSON; stable across dictionary insertion order."""
    return hashlib.sha256(_canonical(value, max_bytes=max_bytes).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ScientificArtifact:
    """Portable scientific value with explicit type, schema, units and provenance."""

    artifact_id: str
    artifact_type: str
    schema_version: str
    payload: Mapping[str, JsonValue]
    units: Mapping[str, str] = field(default_factory=dict)
    coordinate_system: str | None = None
    provenance: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, value in (
            ("artifact_id", self.artifact_id),
            ("artifact_type", self.artifact_type),
            ("schema_version", self.schema_version),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        _canonical(dict(self.payload))
        _canonical(dict(self.units))
        _canonical(dict(self.provenance))
        if any(not isinstance(k, str) or not isinstance(v, str) for k, v in self.units.items()):
            raise ValueError("units must map field names to unit strings")
        if self.coordinate_system is not None and not self.coordinate_system.strip():
            raise ValueError("coordinate_system must be non-empty when supplied")

    @property
    def sha256(self) -> str:
        return content_digest({
            "artifact_type": self.artifact_type,
            "schema_version": self.schema_version,
            "payload": dict(self.payload),
            "units": dict(self.units),
            "coordinate_system": self.coordinate_system,
        })


@dataclass(frozen=True)
class ScientificGoal:
    """User intent normalized into a bounded, typed generation specification."""

    goal_id: str
    domain: str
    objective: str
    specification: Mapping[str, JsonValue]
    hard_constraints: tuple[str, ...] = ()
    soft_objectives: tuple[str, ...] = ()
    seed: int | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("goal_id", self.goal_id), ("domain", self.domain), ("objective", self.objective)
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        _canonical(dict(self.specification))
        for field_name, values in (
            ("hard_constraints", self.hard_constraints),
            ("soft_objectives", self.soft_objectives),
        ):
            if len(values) > 256 or any(not isinstance(v, str) or not v.strip() for v in values):
                raise ValueError(f"{field_name} must contain at most 256 non-empty strings")
        if self.seed is not None and (
            isinstance(self.seed, bool) or not isinstance(self.seed, int)
            or not 0 <= self.seed <= 2**32 - 1
        ):
            raise ValueError("seed must be an unsigned 32-bit integer")


@dataclass(frozen=True)
class RuleSpec:
    """Metadata for a versioned, explicitly scoped scientific rule."""

    rule_id: str
    version: str
    domain: str
    description: str
    assumptions: tuple[str, ...] = ()
    source_references: tuple[str, ...] = ()
    applicability: str = "not_further_restricted"
    reviewer: str | None = None
    approval_state: str = "proposed"

    def __post_init__(self) -> None:
        for name, value in (
            ("rule_id", self.rule_id), ("version", self.version),
            ("domain", self.domain), ("description", self.description),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        if self.approval_state not in {"proposed", "reviewed", "approved", "retired"}:
            raise ValueError("Unsupported rule approval_state")
        if self.approval_state == "approved" and not self.reviewer:
            raise ValueError("Approved rules require a named reviewer")
        if len(self.assumptions) > 128 or len(self.source_references) > 128:
            raise ValueError("Rule metadata exceeds bounded list size")


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    version: str
    passed: bool
    output: Mapping[str, JsonValue]
    message: str


class RuleEngine:
    """Execute registered Molecularis rules; no eval, dynamic imports or implicit I/O."""

    def __init__(self) -> None:
        self._rules: dict[tuple[str, str], tuple[RuleSpec, RuleFunction]] = {}

    def register(self, spec: RuleSpec, function: RuleFunction) -> None:
        if not callable(function):
            raise TypeError("Rule implementation must be callable")
        key = (spec.rule_id, spec.version)
        if key in self._rules:
            raise ValueError(f"Rule already registered: {spec.rule_id}@{spec.version}")
        self._rules[key] = (spec, function)

    def evaluate(
        self, rule_id: str, version: str, inputs: Mapping[str, JsonValue],
        *, require_approved: bool = True,
    ) -> RuleResult:
        key = (rule_id, version)
        if key not in self._rules:
            raise KeyError(f"Unknown rule: {rule_id}@{version}")
        spec, function = self._rules[key]
        if spec.approval_state == "retired":
            raise ValueError(f"Rule is retired: {rule_id}@{version}")
        if require_approved and spec.approval_state != "approved":
            raise PermissionError(f"Rule is not approved for trusted execution: {rule_id}@{version}")
        _canonical(dict(inputs))
        try:
            output = dict(function(dict(inputs)))
            _canonical(output)
        except Exception as exc:
            return RuleResult(rule_id, version, False, {}, f"Rule execution failed: {type(exc).__name__}")
        return RuleResult(rule_id, version, True, output, "Rule executed; scientific validity not implied")


@dataclass(frozen=True)
class Candidate:
    artifact: ScientificArtifact
    generator_id: str
    generator_version: str
    score: float | None = None
    score_name: str | None = None


@dataclass(frozen=True)
class ValidationFinding:
    validator_id: str
    validator_version: str
    check_id: str
    passed: bool
    severity: str
    message: str
    evidence: Mapping[str, JsonValue] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationReport:
    artifact_sha256: str
    findings: tuple[ValidationFinding, ...]
    validation_state: str
    limitations: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return self.validation_state == "passed"


class CandidateGenerator(Protocol):
    generator_id: str
    version: str

    def generate(
        self, goal: ScientificGoal, *, max_candidates: int
    ) -> Iterable[Candidate]: ...


class IndependentValidator(Protocol):
    validator_id: str
    version: str

    def validate(
        self, goal: ScientificGoal, artifact: ScientificArtifact
    ) -> Sequence[ValidationFinding]: ...


@dataclass(frozen=True)
class GenerationRun:
    run_id: str
    goal_digest: str
    generator_id: str
    generator_version: str
    candidates: tuple[Candidate, ...]
    reports: tuple[ValidationReport, ...]
    state: str
    provenance: Mapping[str, JsonValue]


class ScientificCore:
    """Coordinate candidate generation and independent validation with bounded outputs."""

    def run(
        self,
        goal: ScientificGoal,
        generator: CandidateGenerator,
        validators: Sequence[IndependentValidator],
        *,
        max_candidates: int = 32,
    ) -> GenerationRun:
        if isinstance(max_candidates, bool) or not isinstance(max_candidates, int) or not 1 <= max_candidates <= 1000:
            raise ValueError("max_candidates must be an integer between 1 and 1000")
        if not validators:
            raise ValueError("At least one independent validator is required")
        if any(getattr(v, "validator_id", None) == generator.generator_id for v in validators):
            raise ValueError("A generator cannot serve as its own validator")
        if not generator.generator_id or not generator.version:
            raise ValueError("Generator identity and version are required")

        candidates: list[Candidate] = []
        seen: set[str] = set()
        for candidate in generator.generate(goal, max_candidates=max_candidates):
            if len(candidates) >= max_candidates:
                raise ValueError("Generator exceeded max_candidates")
            if candidate.generator_id != generator.generator_id or candidate.generator_version != generator.version:
                raise ValueError("Candidate generator provenance does not match active generator")
            if candidate.score is not None and (
                isinstance(candidate.score, bool) or not math.isfinite(candidate.score)
            ):
                raise ValueError("Candidate score must be finite")
            digest = candidate.artifact.sha256
            if digest in seen:
                continue
            seen.add(digest)
            candidates.append(candidate)

        reports: list[ValidationReport] = []
        for candidate in candidates:
            findings: list[ValidationFinding] = []
            for validator in validators:
                if not validator.validator_id or not validator.version:
                    raise ValueError("Validator identity and version are required")
                validator_findings = validator.validate(goal, candidate.artifact)
                for finding in validator_findings:
                    if finding.validator_id != validator.validator_id or finding.validator_version != validator.version:
                        raise ValueError("Validation finding provenance does not match validator")
                    if finding.severity not in {"info", "warning", "error", "critical"}:
                        raise ValueError("Unsupported validation severity")
                    _canonical(dict(finding.evidence))
                    findings.append(finding)
            failed = any(not finding.passed and finding.severity in {"error", "critical"} for finding in findings)
            validation_state = "failed" if failed else ("passed" if findings else "not_assessed")
            reports.append(ValidationReport(
                artifact_sha256=candidate.artifact.sha256,
                findings=tuple(findings),
                validation_state=validation_state,
                limitations=("Passing checks only covers the listed validators and declared scope; it is not experimental confirmation.",),
            ))

        now = datetime.now(timezone.utc).isoformat()
        provenance: dict[str, JsonValue] = {
            "schema": "molecularis.generation-run.v1",
            "created_at": now,
            "goal": {
                "goal_id": goal.goal_id, "domain": goal.domain, "objective": goal.objective,
                "sha256": content_digest(dict(goal.specification)),
                "hard_constraints": list(goal.hard_constraints),
                "soft_objectives": list(goal.soft_objectives),
                "seed": goal.seed,
            },
            "generator": {"id": generator.generator_id, "version": generator.version},
            "validators": [
                {"id": validator.validator_id, "version": validator.version}
                for validator in validators
            ],
            "candidate_count": len(candidates),
        }
        run_id = content_digest({"provenance": provenance, "artifacts": [c.artifact.sha256 for c in candidates]})[:24]
        state = "no_candidates" if not candidates else (
            "validated" if all(report.passed for report in reports) else (
                "validation_failed" if any(report.validation_state == "failed" for report in reports)
                else "validation_incomplete"
            )
        )
        return GenerationRun(
            run_id=run_id,
            goal_digest=content_digest(asdict(goal)),
            generator_id=generator.generator_id,
            generator_version=generator.version,
            candidates=tuple(candidates),
            reports=tuple(reports),
            state=state,
            provenance=provenance,
        )
