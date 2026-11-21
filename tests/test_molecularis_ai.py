from __future__ import annotations

import pytest

from molecularis.ai import MolecularisAI
from molecularis.bootstrap import create_full_platform, register_all_services
from molecularis.platform import Capability, ExecutionContext, MolecularisPlatform
from molecularis.platform.contracts import ValidationError


def _workflow(capability_id: str, input_keys: tuple[str, ...]) -> dict:
    return {
        "schema": "molecularis.workflow.v1", "workflow_id": "ai_demo",
        "version": "1.0.0", "source": "molecularis_ai",
        "input_keys": list(input_keys),
        "provenance": {"planner": "test-model", "purpose": "synthetic test"},
        "operations": [{
            "operation_id": "validate_input", "capability_id": capability_id,
            "inputs": [input_keys[0]], "output": "validation_report", "parameters": {},
        }],
    }


def test_bootstrap_registers_complete_a_to_n_runtime(tmp_path):
    platform = create_full_platform(str(tmp_path))
    try:
        assert len(platform.registry.list()) >= 14
        assert platform.registry.get("molecular.validate.v1").service == "molecular"
        assert platform.registry.get("workflows.validate.v1").service == "workflows"
    finally:
        platform.close()


def test_bootstrap_requires_fresh_registry(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    platform.register(Capability("test.existing.v1", "1", "test", "existing", "in", "out"))
    try:
        with pytest.raises(RuntimeError, match="fresh, empty"):
            register_all_services(platform)
    finally:
        platform.close()


def test_ai_plans_and_requires_approval_before_execution(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    platform.register(Capability("test.echo.v1", "1", "molecular", "echo", "input", "output"))
    platform.bind("test.echo.v1", lambda inputs, parameters, context: {"echo": b"".join(platform.store.read(inputs["source"])).decode("utf-8")})
    source = platform.ingest(b"synthetic", media_type="text/plain", schema_id="test.input")
    model = lambda request, catalog, available: _workflow("test.echo.v1", tuple(available))
    agent = MolecularisAI(platform, model, planner_id="test-model")
    try:
        plan = agent.plan("Validate this synthetic input", input_artifacts={"source": source.artifact_id})
        assert plan.workflow.source == "molecularis_ai"
        assert plan.report["valid"] is True
        assert plan.request_sha256
        with pytest.raises(ValidationError, match="approval"):
            agent.execute(plan, input_artifacts={"source": source.artifact_id})
        context = ExecutionContext(service_id="molecularis-ai")
        result = agent.execute(plan, input_artifacts={"source": source.artifact_id},
                               approved=True, context=context)
        assert result["result"]["validation_report"] == {"echo": "synthetic"}
        assert platform.store.get_run(context.run_id)["status"] == "succeeded"
    finally:
        platform.close()


def test_ai_rejects_unregistered_capability(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    source = platform.ingest(b"x", media_type="text/plain", schema_id="test.input")
    agent = MolecularisAI(platform, lambda request, catalog, available:
                          _workflow("missing.capability.v1", tuple(available)))
    try:
        with pytest.raises(ValidationError, match="not registered"):
            agent.plan("do work", input_artifacts={"source": source.artifact_id})
    finally:
        platform.close()


def test_ai_rejects_untrusted_workflow_source(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    platform.register(Capability("test.echo.v1", "1", "molecular", "echo", "in", "out"))
    platform.bind("test.echo.v1", lambda inputs, parameters, context: {"ok": True})
    source = platform.ingest(b"x", media_type="text/plain", schema_id="test.input")
    agent = MolecularisAI(platform, lambda request, catalog, available: {
        **_workflow("test.echo.v1", tuple(available)), "source": "untrusted_model"
    })
    try:
        with pytest.raises(ValidationError, match="source"):
            agent.plan("do work", input_artifacts={"source": source.artifact_id})
    finally:
        platform.close()
