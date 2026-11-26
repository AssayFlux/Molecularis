from __future__ import annotations

import json

import pytest

from molecularis.ai import ExecutionApproval, MolecularisAI
from molecularis.domain_integration import validate_scientific_domains
from molecularis.bootstrap import create_full_platform, register_all_services
from molecularis.platform import Capability, ExecutionContext, MolecularisPlatform
from molecularis.platform.contracts import ConflictError, ValidationError


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
        assert len(platform.registry.list()) >= 50
        assert validate_scientific_domains(platform)["domain_count"] == 14
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
        payload = agent.approval_payload(
            plan, input_artifacts={"source": source.artifact_id},
            approval_id="approval-test-001", principal_id="university-reviewer", context=context
        )
        approval_data = json.loads(payload)
        approval = ExecutionApproval(
            approval_id="approval-test-001",
            principal_id="university-reviewer",
            plan_artifact_id=plan.artifact_id,
            input_artifact_ids=tuple(approval_data["input_artifact_ids"]),
            capability_catalog_sha256=approval_data["capability_catalog_sha256"],
            budget_sha256=approval_data["budget_sha256"],
            policy_sha256=approval_data["policy_sha256"],
            signature="signed-test-payload",
        )
        verifier = lambda signed, signature, principal: (
            signed == payload and signature == "signed-test-payload"
            and principal == "university-reviewer"
        )
        result = agent.execute(
            plan, input_artifacts={"source": source.artifact_id},
            approval=approval, approval_verifier=verifier, context=context,
        )
        assert result["result"]["validation_report"] == {"echo": "synthetic"}
        assert platform.store.get_run(context.run_id)["status"] == "succeeded"
        with pytest.raises(ConflictError, match="already been consumed"):
            agent.execute(
                plan, input_artifacts={"source": source.artifact_id},
                approval=approval, approval_verifier=verifier, context=context,
            )
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


def test_ai_execution_rejects_replaced_input_artifact_after_planning(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    platform.register(Capability("test.echo.v1", "1", "molecular", "echo", "input", "output"))
    platform.bind("test.echo.v1", lambda inputs, parameters, context: {"ok": True})
    original = platform.ingest(b"approved", media_type="text/plain", schema_id="test.input")
    replacement = platform.ingest(b"substituted", media_type="text/plain", schema_id="test.input")
    agent = MolecularisAI(
        platform,
        lambda request, catalog, available: _workflow("test.echo.v1", tuple(available)),
    )
    try:
        plan = agent.plan("process the approved input", input_artifacts={"source": original.artifact_id})
        with pytest.raises(ValidationError, match="identities"):
            agent.approval_payload(
                plan, input_artifacts={"source": replacement.artifact_id},
                approval_id="approval-test-002", principal_id="university-reviewer"
            )
    finally:
        platform.close()



def test_ai_execution_rejects_unverified_or_stale_approval(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    platform.register(Capability("test.echo.v1", "1", "molecular", "echo", "input", "output"))
    platform.bind("test.echo.v1", lambda inputs, parameters, context: {"ok": True})
    source = platform.ingest(b"synthetic", media_type="text/plain", schema_id="test.input")
    agent = MolecularisAI(
        platform,
        lambda request, catalog, available: _workflow("test.echo.v1", tuple(available)),
    )
    try:
        plan = agent.plan("run safely", input_artifacts={"source": source.artifact_id})
        context = ExecutionContext(service_id="molecularis-ai")
        payload = agent.approval_payload(
            plan, input_artifacts={"source": source.artifact_id},
            approval_id="nonce-001", principal_id="reviewer-A", context=context,
        )
        data = json.loads(payload)
        approval = ExecutionApproval(
            approval_id="nonce-001", principal_id="reviewer-A",
            plan_artifact_id=plan.artifact_id,
            input_artifact_ids=tuple(data["input_artifact_ids"]),
            capability_catalog_sha256=data["capability_catalog_sha256"],
            budget_sha256=data["budget_sha256"], policy_sha256=data["policy_sha256"],
            signature="not-a-valid-signature",
        )
        with pytest.raises(ValidationError, match="authentication"):
            agent.execute(
                plan, input_artifacts={"source": source.artifact_id},
                approval=approval, approval_verifier=lambda payload, signature, principal: False,
                context=context,
            )

        platform.register(Capability("test.extra.v1", "1", "molecular", "extra", "input", "output"))
        with pytest.raises(ValidationError, match="catalog fingerprint"):
            agent.execute(
                plan, input_artifacts={"source": source.artifact_id},
                approval=approval, approval_verifier=lambda payload, signature, principal: True,
                context=context,
            )

        changed_nonce = agent.approval_payload(
            plan, input_artifacts={"source": source.artifact_id},
            approval_id="nonce-002", principal_id="reviewer-A", context=context,
        )
        changed_principal = agent.approval_payload(
            plan, input_artifacts={"source": source.artifact_id},
            approval_id="nonce-001", principal_id="reviewer-B", context=context,
        )
        assert changed_nonce != payload
        assert changed_principal != payload
    finally:
        platform.close()
