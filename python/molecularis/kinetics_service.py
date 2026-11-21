"""Kinetics I: versioned reaction-network artifacts and bounded deterministic ODE execution."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any

from .kinetics import fit_michaelis_menten, michaelis_menten
from .platform import Artifact, Budget, Capability, ExecutionContext, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

KINETICS_SCHEMA_ID = "molecularis.kinetics-network.v1"
KINETICS_MEDIA_TYPE = "application/vnd.molecularis.kinetics-network+json"
KINETICS_REPORT_SCHEMA_ID = "molecularis.kinetics-report.v1"
KINETICS_RULEBOOK_ID = "kinetics-core-v1"
_CAPS = {
    "validate": "kinetics.validate.v1",
    "simulate": "kinetics.reaction-network-simulate.v1",
    "michaelis_menten": "kinetics.michaelis-menten.v1",
    "fit_michaelis_menten": "kinetics.michaelis-menten-fit.v1",
}
_RULES = ("KIN-001", "KIN-002", "KIN-003", "KIN-004", "KIN-005", "KIN-006")


@dataclass(frozen=True, slots=True)
class ReactionNetworkDocument:
    """Mass-action reaction network; all concentration/time units are caller-defined."""
    identifier: str
    species: tuple[str, ...]
    initial_concentrations: tuple[float, ...]
    reactions: tuple[dict[str, Any], ...]
    time_unit: str = "s"
    concentration_unit: str = "mol/L"

    def __post_init__(self) -> None:
        if not isinstance(self.identifier, str) or not self.identifier.strip() or len(self.identifier) > 256:
            raise ValueError("identifier must contain 1..256 characters")
        if not isinstance(self.species, tuple) or not 1 <= len(self.species) <= 256:
            raise ValueError("species must contain 1..256 names")
        if any(not isinstance(x, str) or not x.strip() or len(x) > 128 for x in self.species):
            raise ValueError("species names must be non-empty strings of at most 128 characters")
        if len(set(self.species)) != len(self.species):
            raise ValueError("species names must be unique")
        if not isinstance(self.initial_concentrations, tuple) or len(self.initial_concentrations) != len(self.species):
            raise ValueError("initial_concentrations must align with species")
        for value in self.initial_concentrations:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError("initial concentrations must be finite and non-negative")
        if not isinstance(self.reactions, tuple) or not 1 <= len(self.reactions) <= 512:
            raise ValueError("reactions must contain 1..512 entries")
        for reaction in self.reactions:
            if not isinstance(reaction, dict) or set(reaction) != {"reactants", "products", "rate_constant"}:
                raise ValueError("each reaction requires reactants, products and rate_constant")
            for side in ("reactants", "products"):
                stoich = reaction[side]
                if not isinstance(stoich, dict) or not stoich:
                    raise ValueError(f"{side} must be a non-empty species-to-stoichiometry mapping")
                for name, coefficient in stoich.items():
                    if name not in self.species or isinstance(coefficient, bool) or not isinstance(coefficient, int) or not 1 <= coefficient <= 8:
                        raise ValueError("stoichiometry must reference known species with integer coefficients 1..8")
            rate = reaction["rate_constant"]
            if isinstance(rate, bool) or not isinstance(rate, (int, float)) or not math.isfinite(rate) or rate < 0:
                raise ValueError("rate_constant must be finite and non-negative")
        for name, unit in (("time_unit", self.time_unit), ("concentration_unit", self.concentration_unit)):
            if not isinstance(unit, str) or not unit.strip() or len(unit) > 32:
                raise ValueError(f"{name} must be a non-empty unit label")

    def to_dict(self) -> dict[str, Any]:
        return {"schema": KINETICS_SCHEMA_ID, "identifier": self.identifier,
                "species": list(self.species), "initial_concentrations": list(self.initial_concentrations),
                "reactions": [{"reactants": dict(sorted(r["reactants"].items())),
                               "products": dict(sorted(r["products"].items())),
                               "rate_constant": float(r["rate_constant"])} for r in self.reactions],
                "time_unit": self.time_unit, "concentration_unit": self.concentration_unit}

    def to_json(self) -> bytes:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False, allow_nan=False,
                          separators=(",", ":")).encode("utf-8")

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.to_json()).hexdigest()

    @classmethod
    def from_json(cls, payload: bytes | str) -> "ReactionNetworkDocument":
        def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key: {key}")
                result[key] = value
            return result
        try:
            raw = payload.decode("utf-8") if isinstance(payload, bytes) else payload
            value = json.loads(raw, object_pairs_hook=unique,
                               parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid kinetics JSON: {exc}") from exc
        fields = {"schema", "identifier", "species", "initial_concentrations", "reactions",
                  "time_unit", "concentration_unit"}
        if not isinstance(value, dict) or set(value) != fields or value["schema"] != KINETICS_SCHEMA_ID:
            raise ValueError("kinetics document fields/schema do not match v1")
        return cls(value["identifier"], tuple(value["species"]), tuple(value["initial_concentrations"]),
                   tuple(value["reactions"]), value["time_unit"], value["concentration_unit"])


def ingest_kinetics(platform: MolecularisPlatform, record: ReactionNetworkDocument, *,
                    parents: tuple[str, ...] = (), budget: Budget | None = None) -> Artifact:
    if not isinstance(record, ReactionNetworkDocument):
        raise TypeError("record must be ReactionNetworkDocument")
    return platform.ingest(record.to_json(), media_type=KINETICS_MEDIA_TYPE,
        schema_id=KINETICS_SCHEMA_ID, metadata={"identifier": record.identifier,
        "kinetics_sha256": record.sha256, "species_count": len(record.species),
        "reaction_count": len(record.reactions)}, parents=parents, budget=budget)


def load_kinetics(platform: MolecularisPlatform, artifact_id: str, *,
                  budget: Budget | None = None) -> ReactionNetworkDocument:
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.media_type != KINETICS_MEDIA_TYPE or artifact.schema_id != KINETICS_SCHEMA_ID:
        raise ValidationError("artifact is not a kinetics network v1")
    if artifact.size_bytes > budget.max_bytes:
        raise ResourceLimitError("kinetics artifact exceeds byte budget")
    record = ReactionNetworkDocument.from_json(b"".join(platform.store.read(artifact_id, budget=budget)))
    expected = {"identifier": record.identifier, "kinetics_sha256": record.sha256,
                "species_count": len(record.species), "reaction_count": len(record.reactions)}
    if artifact.digest != record.sha256 or any(artifact.metadata.get(k) != v for k, v in expected.items()):
        raise ValidationError("kinetics artifact integrity or metadata mismatch")
    return record


def _derivative(record: ReactionNetworkDocument, concentrations: list[float]) -> list[float]:
    rates = [0.0] * len(record.species)
    indexes = {name: i for i, name in enumerate(record.species)}
    for reaction in record.reactions:
        rate = float(reaction["rate_constant"])
        for name, coefficient in reaction["reactants"].items():
            rate *= concentrations[indexes[name]] ** coefficient
        for name, coefficient in reaction["reactants"].items():
            rates[indexes[name]] -= coefficient * rate
        for name, coefficient in reaction["products"].items():
            rates[indexes[name]] += coefficient * rate
    return rates


def simulate_reaction_network(record: ReactionNetworkDocument, *, duration: float,
                              step_size: float, max_steps: int = 100_000) -> dict[str, Any]:
    """Deterministic fixed-step RK4 mass-action integration; no automatic stiffness handling."""
    for name, value in (("duration", duration), ("step_size", step_size)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or not 1 <= max_steps <= 1_000_000:
        raise ValueError("max_steps must be an integer in [1, 1000000]")
    steps_float = duration / step_size
    steps = round(steps_float)
    if steps < 1 or not math.isclose(steps_float, steps, rel_tol=1e-10, abs_tol=1e-10):
        raise ValueError("duration must be an integer multiple of step_size")
    if steps > max_steps:
        raise ResourceLimitError("requested integration exceeds max_steps")
    y = [float(x) for x in record.initial_concentrations]
    trajectory = [{"time": 0.0, "concentrations": dict(zip(record.species, y))}]
    h = float(step_size)
    for index in range(steps):
        k1 = _derivative(record, y)
        y2 = [v + h * k / 2 for v, k in zip(y, k1)]
        k2 = _derivative(record, y2)
        y3 = [v + h * k / 2 for v, k in zip(y, k2)]
        k3 = _derivative(record, y3)
        y4 = [v + h * k for v, k in zip(y, k3)]
        k4 = _derivative(record, y4)
        updated = [v + h * (a + 2*b + 2*c + d) / 6 for v, a, b, c, d in zip(y, k1, k2, k3, k4)]
        scale = max(1.0, *(abs(v) for v in y))
        if any(not math.isfinite(v) for v in updated):
            raise ArithmeticError("integration produced a non-finite concentration")
        if any(v < -1e-10 * scale for v in updated):
            raise ArithmeticError("integration produced a negative concentration; reduce step_size")
        y = [0.0 if -1e-10 * scale <= v < 0 else v for v in updated]
        if index == steps - 1 or (index + 1) % max(1, steps // 1000) == 0:
            trajectory.append({"time": (index + 1) * h, "concentrations": dict(zip(record.species, y))})
    return {"algorithm": "fixed_step_classical_rk4_mass_action_v1", "steps": steps,
            "step_size": h, "duration": float(duration), "time_unit": record.time_unit,
            "concentration_unit": record.concentration_unit, "trajectory": trajectory,
            "initial_concentrations": dict(zip(record.species, record.initial_concentrations)),
            "final_concentrations": dict(zip(record.species, y)),
            "limitations": ["Caller-supplied rate constants and units are not independently checked",
                "Fixed-step RK4; no stiffness detection, adaptive error control or stochastic kinetics",
                "No automatic conservation-law, thermodynamic or parameter-identifiability inference",
                "Numerical output is not experimental validation or a calibrated biochemical prediction"]}


def _execute(operation: str, record: ReactionNetworkDocument, params: dict[str, Any],
             budget: Budget) -> dict[str, Any]:
    if operation == "validate":
        return {"valid": True, "species_count": len(record.species),
                "reaction_count": len(record.reactions), "network_sha256": record.sha256}
    if operation == "simulate":
        duration, step_size = params.get("duration"), params.get("step_size")
        if duration is None or step_size is None:
            raise ValidationError("simulate requires duration and step_size")
        return simulate_reaction_network(record, duration=duration, step_size=step_size,
            max_steps=min(int(params.get("max_steps", 100_000)), budget.max_candidates))
    raise ValidationError(f"unsupported kinetics operation: {operation}")


def register_kinetics_service(platform: MolecularisPlatform) -> None:
    descriptions = {"validate": "Validate a canonical mass-action reaction network",
        "simulate": "Integrate a bounded reaction network using deterministic fixed-step RK4",
        "michaelis_menten": "Evaluate the classical Michaelis-Menten rate equation",
        "fit_michaelis_menten": "Exploratory bounded log-grid Michaelis-Menten fitting"}
    for operation, capability_id in _CAPS.items():
        platform.register(Capability(id=capability_id, version="1.0.0", service="kinetics",
            operation=operation, input_schema=KINETICS_SCHEMA_ID,
            output_schema=KINETICS_REPORT_SCHEMA_ID, deterministic=True,
            description=descriptions[operation]))
        def handler(inputs: dict[str, Any], parameters: dict[str, Any],
                    context: ExecutionContext, selected: str = operation) -> dict[str, Any]:
            if len(inputs) != 1:
                raise ValidationError("kinetics network operation requires exactly one artifact")
            artifact_id = next(iter(inputs.values()))
            if not isinstance(artifact_id, str):
                raise ValidationError("kinetics artifact ID must be text")
            record = load_kinetics(platform, artifact_id, budget=context.budget)
            if selected == "michaelis_menten":
                result = {"rate": michaelis_menten(parameters["substrate"], parameters["vmax"], parameters["km"])}
            elif selected == "fit_michaelis_menten":
                result = fit_michaelis_menten(parameters["substrates"], parameters["rates"],
                    grid_size=parameters.get("grid_size", 100))
            else:
                result = _execute(selected, record, parameters, context.budget)
            return {"schema": KINETICS_REPORT_SCHEMA_ID, "operation": selected,
                "network_id": record.identifier, "network_sha256": record.sha256,
                "result": result, "rulebook": KINETICS_RULEBOOK_ID, "rules_checked": list(_RULES),
                "limitations": ["Caller-defined units are not inferred", "Curve fits are exploratory and not scientific validation"]}
        platform.bind(capability_id, handler)


def kinetics_rulebook(operation: str, artifact_key: str = "kinetics_artifact_id", *,
                      parameters: dict[str, Any] | None = None) -> Rulebook:
    if operation not in _CAPS:
        raise ValueError(f"unsupported kinetics operation: {operation}")
    return Rulebook(id=KINETICS_RULEBOOK_ID, version="1.0.0", operations=(
        Operation(id=f"{operation}-kinetics", capability_id=_CAPS[operation],
                  inputs=(artifact_key,), output="kinetics_result", parameters=dict(parameters or {})),))
