"""Domain-neutral Scientific Knowledge Engine (SKE) primitives.

This module stores typed scientific knowledge and its evidence. It deliberately does
not infer truth, execute equation strings, fetch remote sources, or train models.
All persistence and external ingestion are explicit adapter responsibilities.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence


class EvidenceClass(str, Enum):
    OBSERVED = "observed"
    ESTABLISHED = "established"
    DERIVED = "derived"
    INFERRED = "inferred"
    PREDICTED = "predicted"
    SIMULATED = "simulated"
    CONSTRUCTED = "constructed"
    HYPOTHESIZED = "hypothesized"
    VALIDATED = "validated"


class EvidenceStatus(str, Enum):
    ACTIVE = "active"
    DISPUTED = "disputed"
    SUPERSEDED = "superseded"
    RETRACTED = "retracted"


class SourcePermission(str, Enum):
    UNKNOWN = "unknown"
    RESEARCH_ONLY = "research_only"
    REDISTRIBUTION_ALLOWED = "redistribution_allowed"
    TRAINING_ALLOWED = "training_allowed"
    PROHIBITED = "prohibited"


def _text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")
    return value.strip()


def _finite(value: float, field_name: str = "value") -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field_name} must be finite")
    return result


def _canonical(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("Value must be finite JSON-compatible data") from exc


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class Dimension:
    """Physical dimension represented by integer powers of SI base dimensions."""

    powers: tuple[tuple[str, int], ...] = ()

    def __post_init__(self) -> None:
        normalized: dict[str, int] = {}
        for name, power in self.powers:
            key = _text(name, "dimension name")
            if isinstance(power, bool) or not isinstance(power, int):
                raise TypeError("dimension powers must be integers")
            if power:
                normalized[key] = normalized.get(key, 0) + power
        canonical = tuple(sorted((k, v) for k, v in normalized.items() if v))
        object.__setattr__(self, "powers", canonical)

    @classmethod
    def of(cls, **powers: int) -> "Dimension":
        return cls(tuple(powers.items()))

    def __mul__(self, other: "Dimension") -> "Dimension":
        return Dimension(self.powers + other.powers)

    def __truediv__(self, other: "Dimension") -> "Dimension":
        return Dimension(self.powers + tuple((k, -v) for k, v in other.powers))

    def __pow__(self, exponent: int) -> "Dimension":
        if isinstance(exponent, bool) or not isinstance(exponent, int):
            raise TypeError("dimension exponent must be an integer")
        return Dimension(tuple((k, v * exponent) for k, v in self.powers))

    def compatible_with(self, other: "Dimension") -> bool:
        return self == other


@dataclass(frozen=True, slots=True)
class UnitDefinition:
    symbol: str
    dimension: Dimension
    scale_to_si: float = 1.0
    offset_to_si: float = 0.0

    def __post_init__(self) -> None:
        _text(self.symbol, "unit symbol")
        scale = _finite(self.scale_to_si, "scale_to_si")
        offset = _finite(self.offset_to_si, "offset_to_si")
        if scale <= 0:
            raise ValueError("scale_to_si must be positive")
        if offset and self.dimension != TEMPERATURE:
            raise ValueError("offset units are supported only for temperature")
        object.__setattr__(self, "scale_to_si", scale)
        object.__setattr__(self, "offset_to_si", offset)


LENGTH = Dimension.of(L=1)
MASS = Dimension.of(M=1)
TIME = Dimension.of(T=1)
TEMPERATURE = Dimension.of(Theta=1)
AMOUNT = Dimension.of(N=1)
CURRENT = Dimension.of(I=1)
DIMENSIONLESS = Dimension()


class UnitRegistry:
    """Explicit unit registry; compound units are composed through Quantity arithmetic."""

    def __init__(self, definitions: Iterable[UnitDefinition] | None = None) -> None:
        self._units: dict[str, UnitDefinition] = {}
        defaults = definitions if definitions is not None else (
            UnitDefinition("1", DIMENSIONLESS),
            UnitDefinition("m", LENGTH), UnitDefinition("cm", LENGTH, 0.01),
            UnitDefinition("mm", LENGTH, 0.001), UnitDefinition("um", LENGTH, 1e-6),
            UnitDefinition("nm", LENGTH, 1e-9), UnitDefinition("km", LENGTH, 1000.0),
            UnitDefinition("kg", MASS), UnitDefinition("g", MASS, 0.001),
            UnitDefinition("mg", MASS, 1e-6), UnitDefinition("s", TIME),
            UnitDefinition("min", TIME, 60.0), UnitDefinition("h", TIME, 3600.0),
            UnitDefinition("K", TEMPERATURE), UnitDefinition("degC", TEMPERATURE, 1.0, 273.15),
            UnitDefinition("mol", AMOUNT), UnitDefinition("mmol", AMOUNT, 1e-3),
            UnitDefinition("A", CURRENT), UnitDefinition("Pa", MASS / TIME**2 / LENGTH),
            UnitDefinition("kPa", MASS / TIME**2 / LENGTH, 1000.0),
            UnitDefinition("J", MASS * LENGTH**2 / TIME**2),
            UnitDefinition("kJ", MASS * LENGTH**2 / TIME**2, 1000.0),
            UnitDefinition("N", MASS * LENGTH / TIME**2),
            UnitDefinition("W", MASS * LENGTH**2 / TIME**3),
            UnitDefinition("L", LENGTH**3, 1e-3), UnitDefinition("mL", LENGTH**3, 1e-6),
        )
        for definition in defaults:
            self.register(definition)

    def register(self, definition: UnitDefinition) -> None:
        if definition.symbol in self._units:
            raise ValueError(f"Unit already registered: {definition.symbol}")
        self._units[definition.symbol] = definition

    def get(self, symbol: str) -> UnitDefinition:
        if symbol in self._units:
            return self._units[symbol]
        if not re.fullmatch(r"(?:[A-Za-z]+|1)(?:\^-?\d+)?(?:[*/](?:[A-Za-z]+|1)(?:\^-?\d+)?)*", symbol):
            raise KeyError(f"Unknown unit: {symbol}")
        tokens = re.findall(r"([A-Za-z]+|1)(?:\^(-?\d+))?", symbol)
        operators = re.findall(r"[*/]", symbol)
        if len(tokens) != len(operators) + 1:
            raise KeyError(f"Unknown unit: {symbol}")
        dimension = DIMENSIONLESS
        scale = 1.0
        for index, (name, exponent_text) in enumerate(tokens):
            definition = self._units.get(name)
            if definition is None or definition.offset_to_si:
                raise KeyError(f"Unknown or non-composable unit: {name}")
            exponent = int(exponent_text) if exponent_text else 1
            if index and operators[index - 1] == "/":
                exponent = -exponent
            dimension = dimension * (definition.dimension ** exponent)
            scale *= definition.scale_to_si ** exponent
        derived = UnitDefinition(symbol, dimension, scale)
        self._units[symbol] = derived
        return derived

    def quantity(self, value: float, unit: str) -> "Quantity":
        definition = self.get(unit)
        return Quantity(value, unit, definition.dimension, self)


@dataclass(frozen=True, slots=True)
class Quantity:
    value: float
    unit: str
    dimension: Dimension
    registry: UnitRegistry = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _finite(self.value))
        definition = self.registry.get(self.unit)
        if definition.dimension != self.dimension and self.unit != "1":
            raise ValueError("Quantity dimension does not match its unit")

    @property
    def si_value(self) -> float:
        unit = self.registry.get(self.unit)
        return self.value * unit.scale_to_si + unit.offset_to_si

    def to(self, unit: str) -> "Quantity":
        target = self.registry.get(unit)
        if target.dimension != self.dimension:
            raise ValueError(f"Incompatible dimensions: {self.unit} and {unit}")
        return Quantity((self.si_value - target.offset_to_si) / target.scale_to_si,
                        unit, self.dimension, self.registry)

    def _coerce_add(self, other: "Quantity") -> float:
        if not isinstance(other, Quantity) or other.dimension != self.dimension:
            raise ValueError("Addition/subtraction requires compatible dimensions")
        return other.to(self.unit).value

    def __add__(self, other: "Quantity") -> "Quantity":
        return Quantity(self.value + self._coerce_add(other), self.unit,
                        self.dimension, self.registry)

    def __sub__(self, other: "Quantity") -> "Quantity":
        return Quantity(self.value - self._coerce_add(other), self.unit,
                        self.dimension, self.registry)

    def __mul__(self, other: float | "Quantity") -> "Quantity":
        if isinstance(other, Quantity):
            if self.registry is not other.registry:
                raise ValueError("Quantities must share a unit registry")
            return Quantity(self.si_value * other.si_value, "1",
                            self.dimension * other.dimension, self.registry)._with_si_unit()
        scalar = _finite(other, "multiplier")
        return Quantity(self.value * scalar, self.unit, self.dimension, self.registry)

    def __pow__(self, exponent: int) -> "Quantity":
        if isinstance(exponent, bool) or not isinstance(exponent, int):
            raise TypeError("quantity exponent must be an integer")
        if self.value == 0 and exponent < 0:
            raise ZeroDivisionError("zero quantity cannot have a negative power")
        return Quantity(self.si_value ** exponent, "1", self.dimension ** exponent,
                        self.registry)

    def __truediv__(self, other: float | "Quantity") -> "Quantity":
        if isinstance(other, Quantity):
            if self.registry is not other.registry:
                raise ValueError("Quantities must share a unit registry")
            if other.si_value == 0:
                raise ZeroDivisionError("quantity division by zero")
            dimension = self.dimension / other.dimension
            # Derived dimensions are carried with canonical SI scale in unit "1".
            return Quantity(self.si_value / other.si_value, "1", dimension,
                            self.registry)
        scalar = _finite(other, "divisor")
        if scalar == 0:
            raise ZeroDivisionError("quantity division by zero")
        return Quantity(self.value / scalar, self.unit, self.dimension, self.registry)

    def _with_si_unit(self) -> "Quantity":
        # Unit "1" is the neutral display unit; dimension remains explicit.
        return self


@dataclass(frozen=True, slots=True)
class CoordinateReference:
    reference_id: str
    frame: str
    axes: tuple[str, ...]
    handedness: str = "right"
    units: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.reference_id, "reference_id")
        _text(self.frame, "frame")
        if not self.axes or any(not x.strip() for x in self.axes):
            raise ValueError("coordinate axes must be non-empty")
        if self.handedness not in {"right", "left", "not_applicable"}:
            raise ValueError("unsupported coordinate handedness")
        if self.units and len(self.units) != len(self.axes):
            raise ValueError("coordinate units must match the number of axes")


@dataclass(frozen=True, slots=True)
class ScientificSource:
    source_id: str
    source_type: str
    locator: str
    title: str
    publisher: str | None = None
    version: str | None = None
    published_at: str | None = None
    accessed_at: str | None = None
    content_sha256: str | None = None
    license_id: str | None = None
    permission: SourcePermission = SourcePermission.UNKNOWN
    notes: str | None = None

    def __post_init__(self) -> None:
        for name in ("source_id", "source_type", "locator", "title"):
            _text(getattr(self, name), name)
        object.__setattr__(self, "permission", SourcePermission(self.permission))
        if self.content_sha256 and not re.fullmatch(r"[0-9a-f]{64}", self.content_sha256):
            raise ValueError("content_sha256 must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class ScientificConcept:
    concept_id: str
    label: str
    domain: str
    definition: str
    synonyms: tuple[str, ...] = ()
    parent_concept_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("concept_id", "label", "domain", "definition"):
            _text(getattr(self, name), name)
        _canonical(dict(self.metadata))
        if len(set(self.synonyms)) != len(self.synonyms):
            raise ValueError("concept synonyms must be unique")


@dataclass(frozen=True, slots=True)
class ScientificEntity:
    entity_id: str
    entity_type: str
    domain: str
    label: str
    concept_ids: tuple[str, ...] = ()
    external_identifiers: Mapping[str, str] = field(default_factory=dict)
    properties: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("entity_id", "entity_type", "domain", "label"):
            _text(getattr(self, name), name)
        _canonical(dict(self.external_identifiers))
        _canonical(dict(self.properties))


@dataclass(frozen=True, slots=True)
class ScientificRelation:
    relation_id: str
    subject_id: str
    predicate: str
    object_id: str
    domain: str
    evidence_ids: tuple[str, ...] = ()
    qualifiers: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("relation_id", "subject_id", "predicate", "object_id", "domain"):
            _text(getattr(self, name), name)
        _canonical(dict(self.qualifiers))


@dataclass(frozen=True, slots=True)
class EquationVariable:
    symbol: str
    description: str
    dimension: Dimension
    unit: str | None = None
    required: bool = True

    def __post_init__(self) -> None:
        _text(self.symbol, "variable symbol")
        _text(self.description, "variable description")
        if self.unit:
            _text(self.unit, "variable unit")


@dataclass(frozen=True, slots=True)
class ScientificEquation:
    equation_id: str
    label: str
    domain: str
    expression: str
    variables: tuple[EquationVariable, ...]
    assumptions: tuple[str, ...] = ()
    applicability: str = "unspecified"
    source_ids: tuple[str, ...] = ()
    version: str = "1.0.0"
    status: str = "proposed"

    def __post_init__(self) -> None:
        for name in ("equation_id", "label", "domain", "expression", "version"):
            _text(getattr(self, name), name)
        _text(self.applicability, "applicability")
        if self.status not in {"proposed", "reviewed", "approved", "retired"}:
            raise ValueError("invalid equation status")
        symbols = [v.symbol for v in self.variables]
        if len(symbols) != len(set(symbols)):
            raise ValueError("equation variable symbols must be unique")
        # Expression is inert text: never eval/exec it in the SKE.
        if len(self.expression) > 4096:
            raise ValueError("equation expression exceeds 4096 characters")


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    claim: str
    evidence_class: EvidenceClass
    status: EvidenceStatus
    source_ids: tuple[str, ...] = ()
    subject_ids: tuple[str, ...] = ()
    contradicts_evidence_ids: tuple[str, ...] = ()
    method: str | None = None
    assumptions: tuple[str, ...] = ()
    uncertainty: Mapping[str, Any] = field(default_factory=dict)
    applicability: str = "unspecified"
    reviewer: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        _text(self.evidence_id, "evidence_id")
        _text(self.claim, "claim")
        _text(self.applicability, "applicability")
        object.__setattr__(self, "evidence_class", EvidenceClass(self.evidence_class))
        object.__setattr__(self, "status", EvidenceStatus(self.status))
        _canonical(dict(self.uncertainty))
        try:
            datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("created_at must be an ISO-8601 timestamp") from exc


@dataclass(frozen=True, slots=True)
class KnowledgePackage:
    package_id: str
    version: str
    domain: str
    concepts: tuple[ScientificConcept, ...] = ()
    entities: tuple[ScientificEntity, ...] = ()
    relations: tuple[ScientificRelation, ...] = ()
    equations: tuple[ScientificEquation, ...] = ()
    sources: tuple[ScientificSource, ...] = ()
    evidence: tuple[EvidenceRecord, ...] = ()
    coordinate_references: tuple[CoordinateReference, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("package_id", "version", "domain"):
            _text(getattr(self, name), name)
        _canonical(dict(self.metadata))
        for collection_name in ("concepts", "entities", "relations", "equations",
                                "sources", "evidence", "coordinate_references"):
            records = getattr(self, collection_name)
            ids = [getattr(record, {
                "concepts": "concept_id", "entities": "entity_id",
                "relations": "relation_id", "equations": "equation_id",
                "sources": "source_id", "evidence": "evidence_id",
                "coordinate_references": "reference_id",
            }[collection_name]) for record in records]
            if len(ids) != len(set(ids)):
                raise ValueError(f"duplicate identifiers in {collection_name}")
        concept_ids = {x.concept_id for x in self.concepts}
        entity_ids = {x.entity_id for x in self.entities}
        source_ids = {x.source_id for x in self.sources}
        evidence_ids = {x.evidence_id for x in self.evidence}
        for concept in self.concepts:
            missing = set(concept.parent_concept_ids) - concept_ids
            if missing:
                raise ValueError(f"unknown parent concepts: {sorted(missing)}")
        for entity in self.entities:
            if set(entity.concept_ids) - concept_ids:
                raise ValueError(f"entity {entity.entity_id} references unknown concepts")
        for relation in self.relations:
            if relation.subject_id not in entity_ids or relation.object_id not in entity_ids:
                raise ValueError(f"relation {relation.relation_id} has unknown endpoints")
            if set(relation.evidence_ids) - evidence_ids:
                raise ValueError(f"relation {relation.relation_id} references unknown evidence")
        for equation in self.equations:
            if set(equation.source_ids) - source_ids:
                raise ValueError(f"equation {equation.equation_id} references unknown sources")
        for record in self.evidence:
            if set(record.source_ids) - source_ids:
                raise ValueError(f"evidence {record.evidence_id} references unknown sources")
            if set(record.contradicts_evidence_ids) - evidence_ids:
                raise ValueError(f"evidence {record.evidence_id} references unknown contradictory evidence")
            if record.evidence_id in record.contradicts_evidence_ids:
                raise ValueError("evidence cannot contradict itself")

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "KnowledgePackage":
        def as_dimension(raw: Mapping[str, Any]) -> Dimension:
            return Dimension(tuple((str(name), int(power))
                                   for name, power in raw.get("powers", ())))

        concepts = tuple(ScientificConcept(
            concept_id=item["concept_id"], label=item["label"], domain=item["domain"],
            definition=item["definition"], synonyms=tuple(item.get("synonyms", ())),
            parent_concept_ids=tuple(item.get("parent_concept_ids", ())),
            metadata=item.get("metadata", {}),
        ) for item in payload.get("concepts", ()))
        entities = tuple(ScientificEntity(
            entity_id=item["entity_id"], entity_type=item["entity_type"],
            domain=item["domain"], label=item["label"],
            concept_ids=tuple(item.get("concept_ids", ())),
            external_identifiers=item.get("external_identifiers", {}),
            properties=item.get("properties", {}),
        ) for item in payload.get("entities", ()))
        relations = tuple(ScientificRelation(
            relation_id=item["relation_id"], subject_id=item["subject_id"],
            predicate=item["predicate"], object_id=item["object_id"],
            domain=item["domain"], evidence_ids=tuple(item.get("evidence_ids", ())),
            qualifiers=item.get("qualifiers", {}),
        ) for item in payload.get("relations", ()))
        equations = tuple(ScientificEquation(
            equation_id=item["equation_id"], label=item["label"], domain=item["domain"],
            expression=item["expression"],
            variables=tuple(EquationVariable(
                symbol=v["symbol"], description=v["description"],
                dimension=as_dimension(v["dimension"]), unit=v.get("unit"),
                required=v.get("required", True),
            ) for v in item.get("variables", ())),
            assumptions=tuple(item.get("assumptions", ())),
            applicability=item.get("applicability", "unspecified"),
            source_ids=tuple(item.get("source_ids", ())),
            version=item.get("version", "1.0.0"), status=item.get("status", "proposed"),
        ) for item in payload.get("equations", ()))
        sources = tuple(ScientificSource(
            source_id=item["source_id"], source_type=item["source_type"],
            locator=item["locator"], title=item["title"],
            publisher=item.get("publisher"), version=item.get("version"),
            published_at=item.get("published_at"), accessed_at=item.get("accessed_at"),
            content_sha256=item.get("content_sha256"), license_id=item.get("license_id"),
            permission=SourcePermission(item.get("permission", "unknown")),
            notes=item.get("notes"),
        ) for item in payload.get("sources", ()))
        evidence = tuple(EvidenceRecord(
            evidence_id=item["evidence_id"], claim=item["claim"],
            evidence_class=EvidenceClass(item["evidence_class"]),
            status=EvidenceStatus(item["status"]),
            source_ids=tuple(item.get("source_ids", ())),
            subject_ids=tuple(item.get("subject_ids", ())),
            contradicts_evidence_ids=tuple(item.get("contradicts_evidence_ids", ())),
            method=item.get("method"), assumptions=tuple(item.get("assumptions", ())),
            uncertainty=item.get("uncertainty", {}),
            applicability=item.get("applicability", "unspecified"),
            reviewer=item.get("reviewer"), created_at=item["created_at"],
        ) for item in payload.get("evidence", ()))
        coordinate_references = tuple(CoordinateReference(
            reference_id=item["reference_id"], frame=item["frame"],
            axes=tuple(item["axes"]), handedness=item.get("handedness", "right"),
            units=tuple(item.get("units", ())),
        ) for item in payload.get("coordinate_references", ()))
        return cls(
            package_id=payload["package_id"], version=payload["version"],
            domain=payload["domain"], concepts=concepts, entities=entities,
            relations=relations, equations=equations, sources=sources,
            evidence=evidence, coordinate_references=coordinate_references,
            metadata=payload.get("metadata", {}),
        )

    @property
    def content_sha256(self) -> str:
        return _digest(self.to_dict())


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Dimension):
        return {k: v for k, v in value.powers}
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if hasattr(value, "__dataclass_fields__"):
        return _jsonable(asdict(value))
    return value


class ScientificKnowledgeEngine:
    """Deterministic, in-memory SKE reference implementation.

    Production persistence is provided by an explicit adapter (for example, the
    Molecularis artifact store); this class never silently writes to disk or network.
    """

    def __init__(self) -> None:
        self._packages: dict[tuple[str, str], KnowledgePackage] = {}

    def ingest(self, package: KnowledgePackage) -> str:
        key = (package.package_id, package.version)
        existing = self._packages.get(key)
        if existing is not None:
            if existing.content_sha256 != package.content_sha256:
                raise ValueError("immutable package version already exists with different content")
            return existing.content_sha256
        self._packages[key] = package
        return package.content_sha256

    def get(self, package_id: str, version: str) -> KnowledgePackage:
        try:
            return self._packages[(package_id, version)]
        except KeyError as exc:
            raise KeyError(f"Unknown knowledge package: {package_id}@{version}") from exc

    def list_packages(self, *, domain: str | None = None) -> tuple[tuple[str, str, str], ...]:
        rows = [
            (p.package_id, p.version, p.domain)
            for p in self._packages.values()
            if domain is None or p.domain == domain
        ]
        return tuple(sorted(rows))

    def query_concepts(self, *, domain: str | None = None,
                       text: str | None = None) -> tuple[ScientificConcept, ...]:
        needle = text.casefold() if text else None
        found: list[ScientificConcept] = []
        for package in self._packages.values():
            if domain is not None and package.domain != domain:
                continue
            for concept in package.concepts:
                haystack = " ".join((concept.label, concept.definition, *concept.synonyms)).casefold()
                if needle is None or needle in haystack:
                    found.append(concept)
        return tuple(sorted(found, key=lambda item: (item.domain, item.concept_id)))

    def query_entities(self, *, domain: str | None = None,
                       entity_type: str | None = None,
                       text: str | None = None) -> tuple[ScientificEntity, ...]:
        needle = text.casefold() if text else None
        found = []
        for package in self._packages.values():
            for entity in package.entities:
                if domain is not None and entity.domain != domain:
                    continue
                if entity_type is not None and entity.entity_type != entity_type:
                    continue
                if needle is not None and needle not in entity.label.casefold():
                    continue
                found.append(entity)
        return tuple(sorted(found, key=lambda item: (item.domain, item.entity_id)))

    def query_relations(self, *, subject_id: str | None = None,
                        predicate: str | None = None) -> tuple[ScientificRelation, ...]:
        found = [relation for package in self._packages.values()
                 for relation in package.relations
                 if (subject_id is None or relation.subject_id == subject_id)
                 and (predicate is None or relation.predicate == predicate)]
        return tuple(sorted(found, key=lambda item: item.relation_id))

    def query_equations(self, *, domain: str | None = None,
                        status: str | None = None) -> tuple[ScientificEquation, ...]:
        found = [equation for package in self._packages.values()
                 for equation in package.equations
                 if (domain is None or equation.domain == domain)
                 and (status is None or equation.status == status)]
        return tuple(sorted(found, key=lambda item: (item.domain, item.equation_id)))

    def query_sources(self, *, permission: SourcePermission | None = None) -> tuple[ScientificSource, ...]:
        found = [source for package in self._packages.values()
                 for source in package.sources
                 if permission is None or source.permission == permission]
        return tuple(sorted(found, key=lambda item: item.source_id))

    def query_evidence(self, *, subject_id: str | None = None,
                       evidence_class: EvidenceClass | None = None,
                       status: EvidenceStatus | None = None) -> tuple[EvidenceRecord, ...]:
        found: list[EvidenceRecord] = []
        for package in self._packages.values():
            for record in package.evidence:
                if subject_id is not None and subject_id not in record.subject_ids:
                    continue
                if evidence_class is not None and record.evidence_class != evidence_class:
                    continue
                if status is not None and record.status != status:
                    continue
                found.append(record)
        return tuple(sorted(found, key=lambda item: (item.evidence_id, item.created_at)))

    def conflicting_evidence(self, *, subject_id: str) -> tuple[EvidenceRecord, ...]:
        """Return all active/disputed claims for inspection; never choose a winner."""
        return tuple(
            record for record in self.query_evidence(subject_id=subject_id)
            if record.status in {EvidenceStatus.ACTIVE, EvidenceStatus.DISPUTED}
        )

    def export_package(self, package_id: str, version: str) -> str:
        return _canonical(self.get(package_id, version).to_dict())

    def persist(self, package: KnowledgePackage, artifact_store: Any, *,
                parent_artifact_ids: Iterable[str] = ()) -> Any:
        """Persist through Core ArtifactStore and preserve supplied parent lineage."""
        payload = _canonical(package.to_dict()).encode("utf-8")
        artifact = artifact_store.ingest(
            payload, media_type="application/vnd.molecularis.knowledge+json",
            schema_id="urn:molecularis:scientific-knowledge-package:1",
            metadata={"package_id": package.package_id, "package_version": package.version,
                      "domain": package.domain, "knowledge_sha256": package.content_sha256},
            parents=tuple(parent_artifact_ids),
        )
        self.ingest(package)
        return artifact

    def load_artifact(self, artifact_store: Any, artifact_id: str) -> KnowledgePackage:
        """Load and verify a package from Core ArtifactStore."""
        artifact = artifact_store.get(artifact_id)
        if artifact.schema_id != "urn:molecularis:scientific-knowledge-package:1":
            raise ValueError("artifact is not a Molecularis knowledge package")
        raw = b"".join(artifact_store.read(artifact_id))
        package = KnowledgePackage.from_dict(json.loads(raw.decode("utf-8")))
        if artifact.metadata.get("knowledge_sha256") != package.content_sha256:
            raise ValueError("knowledge package digest does not match artifact metadata")
        self.ingest(package)
        return package


__all__ = [
    "AMOUNT", "CURRENT", "DIMENSIONLESS", "LENGTH", "MASS", "TEMPERATURE", "TIME",
    "CoordinateReference", "Dimension", "EquationVariable", "EvidenceClass",
    "EvidenceRecord", "EvidenceStatus", "KnowledgePackage", "Quantity",
    "ScientificConcept", "ScientificEntity", "ScientificEquation",
    "ScientificKnowledgeEngine", "ScientificRelation", "ScientificSource",
    "SourcePermission", "UnitDefinition", "UnitRegistry",
]
