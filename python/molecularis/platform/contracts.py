"""Versioned, domain-neutral platform contracts."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
import uuid


class PlatformError(Exception):
    """Base class carrying a stable machine-readable platform error code."""

    code = "PLATFORM_ERROR"

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


class ValidationError(PlatformError):
    code = "INVALID_CONTRACT"


class ResourceLimitError(PlatformError):
    code = "RESOURCE_LIMIT"


class ArtifactNotFound(PlatformError):
    code = "ARTIFACT_NOT_FOUND"


class IntegrityError(PlatformError):
    code = "INTEGRITY_ERROR"


class ConflictError(PlatformError):
    code = "CONFLICT"


@dataclass(frozen=True)
class Budget:
    max_bytes: int = 1_073_741_824
    max_candidates: int = 100_000
    max_results: int = 10_000
    max_wall_seconds: float = 30.0
    chunk_bytes: int = 1_048_576

    def __post_init__(self) -> None:
        if min(self.max_bytes, self.max_candidates, self.max_results, self.chunk_bytes) <= 0:
            raise ValueError("integer budget limits must be positive")
        if self.max_wall_seconds <= 0:
            raise ValueError("max_wall_seconds must be positive")


@dataclass(frozen=True)
class Capability:
    id: str
    version: str
    service: str
    operation: str
    input_schema: str
    output_schema: str
    deterministic: bool = True
    description: str = ""


@dataclass(frozen=True)
class ExecutionContext:
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    service_id: str = "core"
    engine_version: str = "0.1.0"
    schema_version: str = "1"
    rulebook_version: str = "1"
    parameters: dict[str, Any] = field(default_factory=dict)
    budget: Budget = field(default_factory=Budget)


@dataclass(frozen=True)
class QueryResult:
    items: tuple[dict[str, Any], ...]
    snapshot_id: str
    candidates_examined: int
    complete: bool
    exact: bool
    next_offset: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
