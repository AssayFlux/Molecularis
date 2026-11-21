"""Capability registry and bounded, deterministic Rulebook DAG executor."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable
import json
import time
import uuid

from .contracts import Capability, ExecutionContext, PlatformError, ResourceLimitError, ValidationError
from .store import ArtifactStore


class ServiceRegistry:
    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        if not capability.id or capability.id in self._capabilities:
            raise ValidationError("capability ID must be non-empty and unique",
                                  details={"capability_id": capability.id})
        self._capabilities[capability.id] = capability

    def get(self, capability_id: str) -> Capability:
        try:
            return self._capabilities[capability_id]
        except KeyError as exc:
            raise ValidationError("capability is not registered",
                                  details={"capability_id": capability_id}) from exc

    def list(self, *, service: str | None = None) -> tuple[Capability, ...]:
        values = self._capabilities.values()
        return tuple(sorted((c for c in values if service is None or c.service == service),
                            key=lambda c: c.id))


@dataclass(frozen=True)
class Operation:
    id: str
    capability_id: str
    inputs: tuple[str, ...]
    output: str
    parameters: dict[str, Any]


@dataclass(frozen=True)
class Rulebook:
    id: str
    version: str
    operations: tuple[Operation, ...]
    max_steps: int = 100

    def validate(self, registry: ServiceRegistry) -> tuple[Operation, ...]:
        if not self.id or not self.version or self.max_steps <= 0:
            raise ValidationError("Rulebook identity and positive max_steps are required")
        if len(self.operations) > self.max_steps:
            raise ResourceLimitError("Rulebook exceeds max_steps")
        by_id: dict[str, Operation] = {}
        producers: dict[str, str] = {}
        for op in self.operations:
            if not op.id or op.id in by_id or not op.output:
                raise ValidationError("operation IDs and outputs must be unique and non-empty")
            registry.get(op.capability_id)
            by_id[op.id] = op
            if op.output in producers:
                raise ValidationError("multiple operations produce the same artifact key")
            producers[op.output] = op.id
        pending = list(self.operations)
        available: set[str] = set()
        ordered: list[Operation] = []
        while pending:
            ready = [op for op in pending
                     if all(name in available or name not in producers for name in op.inputs)]
            if not ready:
                raise ValidationError("Rulebook contains a dependency cycle")
            for op in ready:
                ordered.append(op)
                available.add(op.output)
                pending.remove(op)
        return tuple(ordered)


Handler = Callable[[dict[str, Any], dict[str, Any], ExecutionContext], Any]


class RulebookExecutor:
    def __init__(self, registry: ServiceRegistry, store: ArtifactStore) -> None:
        self.registry = registry
        self.store = store
        self._handlers: dict[str, Handler] = {}

    def bind(self, capability_id: str, handler: Handler) -> None:
        self.registry.get(capability_id)
        if capability_id in self._handlers:
            raise ValidationError("handler already bound", details={"capability_id": capability_id})
        self._handlers[capability_id] = handler

    def execute(self, rulebook: Rulebook, initial: dict[str, Any], *,
                context: ExecutionContext | None = None) -> dict[str, Any]:
        context = context or ExecutionContext(rulebook_version=rulebook.version)
        ordered = rulebook.validate(self.registry)
        values = dict(initial)
        outputs: list[str] = []
        started = time.monotonic()
        for op in ordered:
            if time.monotonic() - started > context.budget.max_wall_seconds:
                raise ResourceLimitError("Rulebook wall-time budget exceeded")
            capability = self.registry.get(op.capability_id)
            handler = self._handlers.get(op.capability_id)
            if handler is None:
                raise ValidationError("capability has no executable handler",
                                      details={"capability_id": op.capability_id})
            missing = [name for name in op.inputs if name not in values]
            if missing:
                raise ValidationError("operation input is missing", details={"inputs": missing})
            inputs = {name: values[name] for name in op.inputs}
            result = handler(inputs, dict(op.parameters), context)
            encoded = json.dumps(result, sort_keys=True, default=str).encode("utf-8")
            if len(encoded) > context.budget.max_bytes:
                raise ResourceLimitError("operation output exceeds byte budget")
            artifact = self.store.ingest(
                encoded, media_type="application/json",
                schema_id=capability.output_schema,
                metadata={"operation": op.id, "capability_id": capability.id,
                          "capability_version": capability.version,
                          "rulebook_id": rulebook.id, "rulebook_version": rulebook.version},
            )
            values[op.output] = result
            outputs.append(artifact.artifact_id)
        self.store.record_run(
            run_id=context.run_id, service_id=context.service_id,
            operation="rulebook:" + rulebook.id, status="succeeded",
            inputs=[], outputs=outputs,
            evidence={"rulebook_version": rulebook.version, "engine_version": context.engine_version,
                      "operations": [op.id for op in ordered], "elapsed_seconds": time.monotonic() - started},
        )
        return values
