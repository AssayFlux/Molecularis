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


def test_failed_rulebook_execution_persists_failure_evidence(tmp_path):
    from molecularis.platform import ExecutionContext
    registry = ServiceRegistry()
    registry.register(Capability('test.fail', '1', 'test', 'fail', 'in:v1', 'out:v1'))
    store = ArtifactStore(tmp_path)
    executor = RulebookExecutor(registry, store)
    def fail(inputs, params, context):
        raise RuntimeError('intentional test failure')
    executor.bind('test.fail', fail)
    context = ExecutionContext(run_id='failure-evidence-test')
    book = Rulebook('failure-book', '1', (Operation('fail-step', 'test.fail', ('x',), 'y', {}),))
    with pytest.raises(RuntimeError):
        executor.execute(book, {'x': 7}, context=context)
    evidence = store.get_run(context.run_id)
    assert evidence['status'] == 'failed'
    assert evidence['evidence']['failed_operation'] == 'fail-step'


def test_operation_outputs_preserve_input_artifact_lineage(tmp_path):
    registry = ServiceRegistry()
    registry.register(Capability('test.copy', '1', 'test', 'copy', 'in:v1', 'out:v1'))
    store = ArtifactStore(tmp_path)
    source = store.ingest(b'source')
    executor = RulebookExecutor(registry, store)
    executor.bind('test.copy', lambda inputs, params, ctx: {'source': inputs['source']})
    book = Rulebook('lineage-book', '1', (Operation('copy-step', 'test.copy', ('source',), 'copied', {}),))
    executor.execute(book, {'source': source.artifact_id})
    with store._session() as conn:
        row = conn.execute("SELECT artifact_id FROM artifacts WHERE json_extract(metadata_json, '$.rulebook_id')='lineage-book'").fetchone()
    assert row is not None
    assert store.get(row['artifact_id']).parents == (source.artifact_id,)


def test_missing_artifact_reference_is_rejected_before_handler_execution(tmp_path):
    registry = ServiceRegistry()
    registry.register(Capability("test.inspect", "1", "test", "inspect", "in:v1", "out:v1"))
    executor = RulebookExecutor(registry, ArtifactStore(tmp_path))
    called = []
    executor.bind("test.inspect", lambda inputs, params, ctx: called.append(True))
    book = Rulebook("missing-artifact", "1", (
        Operation("inspect", "test.inspect", ("source",), "result", {}),
    ))
    with pytest.raises(ValidationError, match="artifact"):
        executor.execute(book, {"source": "art_missing-reference"})
    assert called == []
