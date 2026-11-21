"""Cohorts M: canonical, privacy-conscious research cohort artifacts and summaries."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any

from .platform import Budget, Capability, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

COHORT_SCHEMA_ID = "molecularis.cohort.v1"
COHORT_MEDIA_TYPE = "application/vnd.molecularis.cohort+json"
COHORT_REPORT_SCHEMA_ID = "molecularis.cohort-report.v1"
COHORT_RULEBOOK_ID = "cohorts-core-v1"
_CAPS = {
    "validate": "cohorts.validate.v1",
    "summary": "cohorts.summary.v1",
    "stratify": "cohorts.stratify.v1",
    "overlap": "cohorts.overlap.v1",
}
_RULES = {
    "validate": ["COH-001", "COH-002", "COH-003", "COH-008"],
    "summary": ["COH-001", "COH-002", "COH-003", "COH-004", "COH-008"],
    "stratify": ["COH-001", "COH-002", "COH-003", "COH-005", "COH-006", "COH-008"],
    "overlap": ["COH-001", "COH-002", "COH-003", "COH-007", "COH-008"],
}
_MAX_MEMBERS = 100_000
_MAX_VISITS = 1_000_000
_MAX_FIELDS = 128
_MAX_LABEL = 256


@dataclass(frozen=True, slots=True)
class CohortVisit:
    visit_id: str
    timepoint: float
    measurements: tuple[tuple[str, float | None], ...] = ()


@dataclass(frozen=True, slots=True)
class CohortMember:
    member_id: str
    attributes: tuple[tuple[str, str], ...] = ()
    visits: tuple[CohortVisit, ...] = ()
    included: bool = True


@dataclass(frozen=True, slots=True)
class CohortDocument:
    """Research cohort with pseudonymous IDs; v1 permits synthetic non-patient data only."""
    identifier: str
    members: tuple[CohortMember, ...]
    data_classification: str = "synthetic_non_patient"
    source: str = "synthetic_fixture"
    source_release: str = "1"
    provenance: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        for name, value in (("identifier", self.identifier), ("source", self.source),
                            ("source_release", self.source_release)):
            if not isinstance(value, str) or not value.strip() or value != value.strip() or len(value) > _MAX_LABEL:
                raise ValueError(f"{name} must be bounded, non-empty trimmed text")
        if self.data_classification != "synthetic_non_patient":
            raise ValueError("v1 accepts synthetic_non_patient cohort data only")
        if not isinstance(self.members, tuple) or not 1 <= len(self.members) <= _MAX_MEMBERS:
            raise ValueError(f"members must contain 1..{_MAX_MEMBERS} records")
        ids: set[str] = set()
        visit_total = 0
        for member in self.members:
            if not isinstance(member, CohortMember):
                raise TypeError("members must contain CohortMember values")
            if not isinstance(member.member_id, str) or not member.member_id.strip() or member.member_id != member.member_id.strip() or len(member.member_id) > _MAX_LABEL:
                raise ValueError("member_id must be bounded, non-empty trimmed pseudonymous text")
            if member.member_id in ids:
                raise ValueError("member IDs must be unique within a cohort")
            ids.add(member.member_id)
            if not isinstance(member.included, bool):
                raise TypeError("included must be boolean")
            self._validate_pairs(member.attributes, "attributes", categorical=True)
            if not isinstance(member.visits, tuple):
                raise TypeError("visits must be a tuple")
            visit_ids: set[str] = set()
            previous = -math.inf
            for visit in member.visits:
                if not isinstance(visit, CohortVisit):
                    raise TypeError("visits must contain CohortVisit values")
                if not isinstance(visit.visit_id, str) or not visit.visit_id.strip() or len(visit.visit_id) > _MAX_LABEL or visit.visit_id in visit_ids:
                    raise ValueError("visit IDs must be unique bounded non-empty text per member")
                if isinstance(visit.timepoint, bool) or not isinstance(visit.timepoint, (int, float)) or not math.isfinite(visit.timepoint):
                    raise ValueError("visit timepoint must be finite numeric")
                if visit.timepoint < previous:
                    raise ValueError("visit timepoints must be non-decreasing within each member")
                previous = float(visit.timepoint)
                visit_ids.add(visit.visit_id)
                self._validate_pairs(visit.measurements, "measurements", categorical=False)
                visit_total += 1
        if visit_total > _MAX_VISITS:
            raise ValueError(f"cohort exceeds {_MAX_VISITS} total visits")
        self._validate_pairs(self.provenance, "provenance", categorical=True)

    @staticmethod
    def _validate_pairs(pairs: tuple[tuple[str, Any], ...], label: str, *, categorical: bool) -> None:
        if not isinstance(pairs, tuple) or len(pairs) > _MAX_FIELDS:
            raise ValueError(f"{label} must be a tuple with at most {_MAX_FIELDS} entries")
        names: set[str] = set()
        for pair in pairs:
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise ValueError(f"{label} entries must be key/value pairs")
            key, value = pair
            if not isinstance(key, str) or not key.strip() or len(key) > _MAX_LABEL or key in names:
                raise ValueError(f"{label} keys must be unique bounded non-empty text")
            names.add(key)
            if categorical:
                if not isinstance(value, str) or len(value) > _MAX_LABEL:
                    raise ValueError(f"{label} values must be bounded text")
            elif value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)):
                raise ValueError(f"{label} values must be finite numbers or null")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": COHORT_SCHEMA_ID, "identifier": self.identifier,
            "data_classification": self.data_classification, "source": self.source,
            "source_release": self.source_release,
            "provenance": dict(self.provenance),
            "members": [{
                "member_id": m.member_id, "attributes": dict(m.attributes), "included": m.included,
                "visits": [{"visit_id": v.visit_id, "timepoint": float(v.timepoint),
                            "measurements": dict(v.measurements)} for v in m.visits],
            } for m in self.members],
        }

    def to_json(self) -> bytes:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False, allow_nan=False,
                          separators=(",", ":")).encode("utf-8")

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.to_json()).hexdigest()

    @classmethod
    def from_json(cls, payload: bytes | str) -> "CohortDocument":
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key: {key}")
                result[key] = value
            return result
        try:
            raw = payload.decode("utf-8") if isinstance(payload, bytes) else payload
            value = json.loads(raw, object_pairs_hook=unique,
                               parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid Cohort JSON: {exc}") from exc
        if not isinstance(value, dict) or set(value) != {
            "schema", "identifier", "data_classification", "source", "source_release", "provenance", "members"
        } or value["schema"] != COHORT_SCHEMA_ID:
            raise ValueError("Cohort document fields/schema do not match v1")
        if not isinstance(value["members"], list) or not isinstance(value["provenance"], dict):
            raise ValueError("members/provenance must be JSON array/object")
        members = []
        for item in value["members"]:
            if not isinstance(item, dict) or set(item) != {"member_id", "attributes", "included", "visits"}:
                raise ValueError("cohort member fields do not match v1")
            if not isinstance(item["attributes"], dict) or not isinstance(item["visits"], list):
                raise ValueError("member attributes/visits have invalid types")
            visits = []
            for visit in item["visits"]:
                if not isinstance(visit, dict) or set(visit) != {"visit_id", "timepoint", "measurements"} or not isinstance(visit["measurements"], dict):
                    raise ValueError("cohort visit fields do not match v1")
                visits.append(CohortVisit(visit["visit_id"], visit["timepoint"], tuple(sorted(visit["measurements"].items()))))
            members.append(CohortMember(item["member_id"], tuple(sorted(item["attributes"].items())),
                                        tuple(visits), item["included"]))
        return cls(value["identifier"], tuple(members), value["data_classification"],
                   value["source"], value["source_release"], tuple(sorted(value["provenance"].items())))


def ingest_cohort(platform: MolecularisPlatform, record: CohortDocument, *,
                  parents: tuple[str, ...] = (), budget: Budget | None = None):
    if not isinstance(record, CohortDocument):
        raise TypeError("record must be a CohortDocument")
    payload = record.to_json()
    if budget is not None and len(payload) > budget.max_bytes:
        raise ResourceLimitError("cohort artifact exceeds byte budget")
    return platform.ingest(payload, media_type=COHORT_MEDIA_TYPE, schema_id=COHORT_SCHEMA_ID,
                           metadata={"identifier": record.identifier, "cohort_sha256": record.sha256,
                                     "member_count": len(record.members), "data_classification": record.data_classification},
                           parents=parents, budget=budget)


def load_cohort(platform: MolecularisPlatform, artifact_id: str, *, budget: Budget | None = None) -> CohortDocument:
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.media_type != COHORT_MEDIA_TYPE or artifact.schema_id != COHORT_SCHEMA_ID:
        raise ValidationError("artifact is not a Cohort v1")
    if artifact.size_bytes > budget.max_bytes:
        raise ResourceLimitError("cohort artifact exceeds byte budget")
    record = CohortDocument.from_json(b"".join(platform.store.read(artifact_id, budget=budget)))
    expected = {"identifier": record.identifier, "cohort_sha256": record.sha256,
                "member_count": len(record.members), "data_classification": record.data_classification}
    if artifact.digest != record.sha256 or any(artifact.metadata.get(k) != v for k, v in expected.items()):
        raise ValidationError("cohort artifact integrity or metadata mismatch")
    if len(record.members) > budget.max_candidates:
        raise ResourceLimitError("cohort exceeds candidate budget")
    return record


def _active(record: CohortDocument) -> list[CohortMember]:
    return [member for member in record.members if member.included]


def _summary(members: list[CohortMember]) -> dict[str, Any]:
    fields = sorted({key for member in members for key, _ in member.attributes})
    categorical = {}
    for field in fields:
        counts: dict[str, int] = {}
        missing = 0
        for member in members:
            value = dict(member.attributes).get(field)
            if value is None:
                missing += 1
            else:
                counts[value] = counts.get(value, 0) + 1
        categorical[field] = {"counts": dict(sorted(counts.items())), "missing": missing}
    measure_fields = sorted({key for member in members for visit in member.visits for key, _ in visit.measurements})
    measurements = {}
    for field in measure_fields:
        values = [float(value) for member in members for visit in member.visits
                  for key, value in visit.measurements if key == field and value is not None]
        measurements[field] = {
            "observations": len(values), "missing": sum(1 for member in members for visit in member.visits
                                                        for key, value in visit.measurements if key == field and value is None),
            "mean": sum(values) / len(values) if values else None,
            "minimum": min(values) if values else None, "maximum": max(values) if values else None,
        }
    return {"member_count": len(members), "categorical_attributes": categorical,
            "visit_count": sum(len(m.visits) for m in members), "measurements": measurements}


def _stratify(members: list[CohortMember], field: str, minimum_cell_size: int) -> dict[str, Any]:
    groups: dict[str, list[CohortMember]] = {}
    for member in members:
        value = dict(member.attributes).get(field)
        label = value if value is not None else "__MISSING__"
        groups.setdefault(label, []).append(member)
    result = {}
    suppressed = 0
    for label, group in sorted(groups.items()):
        if len(group) < minimum_cell_size:
            suppressed += 1
            continue
        result[label] = _summary(group)
    return {"stratification_field": field, "minimum_cell_size": minimum_cell_size,
            "groups": result, "suppressed_group_count": suppressed,
            "suppression_applied": suppressed > 0}


def _overlap(left: CohortDocument, right: CohortDocument, minimum_cell_size: int) -> dict[str, Any]:
    a = {m.member_id for m in _active(left)}
    b = {m.member_id for m in _active(right)}
    intersection = len(a & b)
    union = len(a | b)
    if intersection < minimum_cell_size:
        intersection_output = None
        suppressed = True
    else:
        intersection_output = intersection
        suppressed = False
    return {"left_cohort": left.identifier, "right_cohort": right.identifier,
            "left_size": len(a), "right_size": len(b), "intersection_size": intersection_output,
            "union_size": union, "jaccard_index": intersection / union if union else 1.0,
            "intersection_suppressed": suppressed,
            "note": "Member-ID overlap is exact only when identifiers share a documented pseudonymization namespace."}


def register_cohorts_service(platform: MolecularisPlatform) -> None:
    descriptions = {
        "validate": "Validate canonical synthetic non-patient cohort artifacts and provenance.",
        "summary": "Produce bounded aggregate cohort and longitudinal measurement summaries.",
        "stratify": "Produce aggregate attribute strata with minimum-cell suppression.",
        "overlap": "Compute pseudonymous member-set overlap with small-intersection suppression.",
    }
    for operation, capability_id in _CAPS.items():
        count = 2 if operation == "overlap" else 1
        platform.register(Capability(
            id=capability_id, version="1.0.0", service="cohorts", operation=operation,
            input_schema=COHORT_SCHEMA_ID if count == 1 else COHORT_SCHEMA_ID + "+cohort",
            output_schema=COHORT_REPORT_SCHEMA_ID, deterministic=True,
            description=descriptions[operation],
        ))
        def handler(inputs, parameters, context, selected=operation, input_count=count):
            values = list(inputs.values())
            if len(values) != input_count or any(not isinstance(v, str) for v in values):
                raise ValidationError(f"Cohorts {selected} requires {input_count} artifact input(s)")
            records = [load_cohort(platform, value, budget=context.budget) for value in values]
            minimum = parameters.get("minimum_cell_size", 5)
            if not isinstance(minimum, int) or isinstance(minimum, bool) or not 2 <= minimum <= 1000:
                raise ValidationError("minimum_cell_size must be an integer from 2 to 1000")
            if selected == "validate":
                result = {"valid": True, "member_count": len(records[0].members),
                          "included_count": len(_active(records[0]))}
            elif selected == "summary":
                result = _summary(_active(records[0]))
            elif selected == "stratify":
                field = parameters.get("field")
                if not isinstance(field, str) or not field.strip() or len(field) > _MAX_LABEL:
                    raise ValidationError("stratify requires a bounded field parameter")
                result = _stratify(_active(records[0]), field, minimum)
            else:
                result = _overlap(records[0], records[1], minimum)
            return {"schema": COHORT_REPORT_SCHEMA_ID, "operation": selected,
                    "cohort_ids": [r.identifier for r in records],
                    "cohort_sha256": [r.sha256 for r in records],
                    "result": result, "rulebook": COHORT_RULEBOOK_ID,
                    "rules_checked": list(_RULES[selected]),
                    "limitations": [
                        "v1 accepts synthetic_non_patient records only; patient or directly identifying data are rejected by classification contract.",
                        "Member IDs must be pseudonymous and are not emitted in aggregate reports.",
                        "Minimum-cell suppression is a disclosure-control heuristic, not differential privacy or a formal privacy guarantee.",
                        "Longitudinal measurements are summarized descriptively; no repeated-measures inference, causal analysis, survival analysis or clinical interpretation is performed.",
                        "Cross-cohort overlap is meaningful only when pseudonymous IDs share a documented namespace.",
                        "No recruitment, consent adjudication, eligibility decision or automated inclusion/exclusion decision is performed.",
                    ]}
        platform.bind(capability_id, handler)


def cohorts_rulebook(operation: str, *, cohort_key: str = "cohort_artifact_id",
                     second_cohort_key: str = "comparison_cohort_artifact_id") -> Rulebook:
    if operation not in _CAPS:
        raise ValueError(f"unsupported Cohorts operation: {operation}")
    if not cohort_key.strip() or not second_cohort_key.strip():
        raise ValueError("artifact input keys must be non-empty")
    inputs = (cohort_key, second_cohort_key) if operation == "overlap" else (cohort_key,)
    parameters = {"minimum_cell_size": 5}
    if operation == "stratify":
        parameters["field"] = ""
    return Rulebook(
        id=COHORT_RULEBOOK_ID, version="1.0.0",
        operations=(Operation(id=f"{operation}-cohorts", capability_id=_CAPS[operation],
                              inputs=inputs, output="cohorts_result", parameters=parameters),),
    )
