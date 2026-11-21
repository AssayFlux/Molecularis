"""Lifecycle-managed local Molecularis Core reference service."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Iterable
import json

from .contracts import Budget, Capability, ExecutionContext, QueryResult, ValidationError
from .runtime import Rulebook, RulebookExecutor, ServiceRegistry
from .store import Artifact, ArtifactStore


class RuntimeState(str, Enum):
    NEW = "new"
    READY = "ready"
    CLOSED = "closed"


class MolecularisPlatform:
    """Small reference runtime that composes the shared Core platform components."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.state = RuntimeState.NEW
        self._store: ArtifactStore | None = None
        self.registry = ServiceRegistry()
        self._executor: RulebookExecutor | None = None

    def start(self) -> None:
        if self.state is RuntimeState.READY:
            return
        if self.state is RuntimeState.CLOSED:
            raise ValidationError("closed platform instances cannot be restarted")
        self._store = ArtifactStore(self.root)
        self._executor = RulebookExecutor(self.registry, self._store)
        self.state = RuntimeState.READY

    def close(self) -> None:
        if self.state is RuntimeState.CLOSED:
            return
        self._store = None
        self._executor = None
        self.state = RuntimeState.CLOSED

    def _require_ready(self) -> tuple[ArtifactStore, RulebookExecutor]:
        if self.state is not RuntimeState.READY or self._store is None or self._executor is None:
            raise ValidationError("platform runtime is not ready")
        return self._store, self._executor

    @property
    def store(self) -> ArtifactStore:
        return self._require_ready()[0]

    def register(self, capability: Capability) -> None:
        self._require_ready()
        self.registry.register(capability)

    def bind(self, capability_id: str, handler: Any) -> None:
        self._require_ready()[1].bind(capability_id, handler)

    def ingest(self, chunks: bytes | Iterable[bytes], *, media_type: str,
               schema_id: str, metadata: dict[str, Any] | None = None,
               parents: Iterable[str] = (), budget: Budget | None = None) -> Artifact:
        return self.store.ingest(chunks, media_type=media_type, schema_id=schema_id,
                                 metadata=metadata, parents=parents, budget=budget)

    def find_exact(self, key: str, value: Any, *, limit: int = 1000,
                   budget: Budget | None = None) -> QueryResult:
        return self.store.find_exact(key, value, limit=limit, budget=budget)

    def find_range(self, key: str, *, minimum: float | None = None,
                   maximum: float | None = None, limit: int = 1000,
                   budget: Budget | None = None) -> QueryResult:
        return self.store.find_range(key, minimum=minimum, maximum=maximum,
                                      limit=limit, budget=budget)

    def execute(self, rulebook: Rulebook, initial: dict[str, Any], *,
                context: ExecutionContext | None = None) -> dict[str, Any]:
        return self._require_ready()[1].execute(rulebook, initial, context=context)

    @classmethod
    def from_capability_manifest(cls, root: str | Path, manifest_path: str | Path
                                 ) -> "MolecularisPlatform":
        """Load an explicit JSON capability manifest; never imports code from the manifest."""
        payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            raise ValidationError("unsupported capability manifest schema")
        capabilities = payload.get("capabilities")
        if not isinstance(capabilities, list):
            raise ValidationError("capability manifest must contain a capabilities array")
        platform = cls(root)
        platform.start()
        for item in capabilities:
            if not isinstance(item, dict):
                raise ValidationError("capability entries must be objects")
            platform.register(Capability(**item))
        return platform
