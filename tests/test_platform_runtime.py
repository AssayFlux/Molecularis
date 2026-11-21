from __future__ import annotations

import pytest

from molecularis.platform import (
    ArtifactStore, Capability, Operation, Rulebook, RulebookExecutor, ServiceRegistry,
)
from molecularis.platform.contracts import ValidationError


def _executor(tmp_path):
    registry = ServiceRegistry()
    registry.register(Capability("math.add", "1", "test", "add", "input:v1", "output:v1"))
    executor = RulebookExecutor(registry, ArtifactStore(tmp_path))
    executor.bind("math.add", lambda inputs, params, ctx: inputs["x"] + params["n"])
    return registry, executor


def test_rulebook_executes_and_persists_evidence(tmp_path):
    _, executor = _executor(tmp_path)
    book = Rulebook("test-book", "1", (Operation("add", "math.add", ("x",), "y", {"n": 2}),))
    result = executor.execute(book, {"x": 3})
    assert result["y"] == 5
    with executor.store._connect() as conn:
        row = conn.execute("SELECT status,operation FROM runs").fetchone()
    assert row["status"] == "succeeded"
    assert row["operation"] == "rulebook:test-book"


def test_rulebook_cycle_is_rejected(tmp_path):
    registry, _ = _executor(tmp_path)
    book = Rulebook("cycle", "1", (
        Operation("a", "math.add", ("b",), "a", {}),
        Operation("b", "math.add", ("a",), "b", {}),
    ))
    with pytest.raises(ValidationError):
        book.validate(registry)


def test_unregistered_capability_is_rejected(tmp_path):
    registry, _ = _executor(tmp_path)
    book = Rulebook("bad", "1", (Operation("x", "missing", (), "y", {}),))
    with pytest.raises(ValidationError):
        book.validate(registry)


def test_duplicate_capability_registration_rejected():
    registry = ServiceRegistry()
    cap = Capability("same", "1", "x", "y", "in", "out")
    registry.register(cap)
    with pytest.raises(ValidationError):
        registry.register(cap)
