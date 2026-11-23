"""Molecularis AI: model-assisted scientific workflow planning with guarded execution.

The model proposes a workflow; Molecularis contracts validate it; native services
perform the scientific operations. No model output is executed without approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping
import hashlib
import json

from .platform import Budget, ExecutionContext, MolecularisPlatform
from .platform.contracts import ValidationError
from .workflows_service import (
    WorkflowDocument, execute_workflow, ingest_workflow, load_workflow,
    validate_workflow,
)

AI_PLAN_SCHEMA = "molecularis.ai-plan.v1"
AI_PLAN_MEDIA_TYPE = "application/vnd.molecularis.ai-plan+json"
AI_REPORT_SCHEMA = "molecularis.ai-report.v1"
_MAX_REQUEST_BYTES = 32_768

# A planner receives only the user request, active capability contracts and
# caller-supplied input artifact references. Provider SDKs stay outside Core.
Planner = Callable[[str, list[dict[str, Any]], dict[str, str]], Mapping[str, Any]]
ApprovalVerifier = Callable[[bytes, str, str], bool]


@dataclass(frozen=True, slots=True)
class ExecutionApproval:
    """Externally authenticated approval bound to exact plan, inputs and runtime policy."""

    approval_id: str
    principal_id: str
    plan_artifact_id: str
    input_artifact_ids: tuple[str, ...]
    capability_catalog_sha256: str
    budget_sha256: str
    policy_sha256: str
    signature: str


@dataclass(frozen=True, slots=True)
class AIPlan:
    artifact_id: str
    workflow: WorkflowDocument
    report: dict[str, Any]
    request_sha256: str
    planner_id: str


class MolecularisAI:
    """Plan scientific workflows through a pluggable model; execute via A–N."""

    def __init__(
        self, platform: MolecularisPlatform, planner: Planner, *,
        planner_id: str = "external-model-adapter", budget: Budget | None = None,
        max_operations: int = 50,
        execution_policy_id: str = "local-reviewed-handlers-no-egress",
    ) -> None:
        if not callable(planner):
            raise TypeError("planner must be a callable model adapter")
        if not isinstance(planner_id, str) or not planner_id.strip() or len(planner_id) > 128:
            raise ValueError("planner_id must be non-empty bounded text")
        if isinstance(max_operations, bool) or not isinstance(max_operations, int) or not 1 <= max_operations <= 100:
            raise ValueError("max_operations must be between 1 and 100")
        if platform.state.value != "ready":
            raise ValidationError("platform runtime must be ready")
        self.platform = platform
        self.planner = planner
        self.planner_id = planner_id
        self.budget = budget or Budget()
        self.max_operations = max_operations
        if not isinstance(execution_policy_id, str) or not execution_policy_id.strip() or len(execution_policy_id) > 256:
            raise ValueError("execution_policy_id must be non-empty bounded text")
        self.execution_policy_id = execution_policy_id

    def capability_catalog(self) -> list[dict[str, Any]]:
        """Return the active executable surface; never infer tools from prose."""
        return [{
            "id": cap.id, "version": cap.version, "service": cap.service,
            "operation": cap.operation, "input_schema": cap.input_schema,
            "output_schema": cap.output_schema, "deterministic": cap.deterministic,
            "description": cap.description,
        } for cap in self.platform.registry.list()]

    def plan(
        self, request: str, *, input_artifacts: Mapping[str, str] | None = None,
        provenance: Mapping[str, str] | None = None,
    ) -> AIPlan:
        """Ask the configured model for a workflow, then strictly validate it."""
        if not isinstance(request, str) or not request.strip():
            raise ValidationError("research request must be non-empty text")
        encoded = request.encode("utf-8")
        if len(encoded) > _MAX_REQUEST_BYTES:
            raise ValidationError("research request exceeds 32 KiB")
        supplied = dict(input_artifacts or {})
        if len(supplied) > 256:
            raise ValidationError("at most 256 input artifacts may be supplied")
        for key, artifact_id in supplied.items():
            if not isinstance(key, str) or not key or len(key) > 128:
                raise ValidationError("input artifact keys must be bounded non-empty identifiers")
            if not isinstance(artifact_id, str) or not artifact_id:
                raise ValidationError("input artifact references must be non-empty strings")
            self.platform.store.get(artifact_id)
        model_result = self.planner(request, self.capability_catalog(), supplied)
        if not isinstance(model_result, Mapping):
            raise ValidationError("planner must return a workflow JSON object")
        try:
            workflow = WorkflowDocument.from_json(json.dumps(
                model_result, ensure_ascii=False, allow_nan=False, separators=(",", ":")
            ))
        except (TypeError, ValueError) as exc:
            raise ValidationError("planner returned an invalid Workflow v1 document") from exc
        if workflow.source != "molecularis_ai":
            raise ValidationError("AI-generated workflow source must be molecularis_ai")
        if set(workflow.input_keys) != set(supplied):
            raise ValidationError("workflow inputs must exactly match caller-supplied artifact keys")
        if len(workflow.operations) > self.max_operations:
            raise ValidationError("AI plan exceeds configured operation limit")
        report = validate_workflow(self.platform, workflow)
        request_digest = hashlib.sha256(encoded).hexdigest()
        artifact = ingest_workflow(
            self.platform, workflow, parents=tuple(supplied.values()), budget=self.budget
        )
        return AIPlan(artifact.artifact_id, workflow, report, request_digest, self.planner_id)

    def approval_payload(
        self, plan: AIPlan | str, *, input_artifacts: Mapping[str, str],
        approval_id: str, principal_id: str, context: ExecutionContext | None = None,
    ) -> bytes:
        """Canonical bytes an external identity/approval service must sign."""
        artifact_id = plan.artifact_id if isinstance(plan, AIPlan) else plan
        if not isinstance(artifact_id, str) or not artifact_id:
            raise ValidationError("plan must be an AIPlan or workflow artifact ID")
        if not isinstance(approval_id, str) or not approval_id.strip() or len(approval_id) > 256:
            raise ValidationError("approval_id must be non-empty bounded text")
        if not isinstance(principal_id, str) or not principal_id.strip() or len(principal_id) > 256:
            raise ValidationError("principal_id must be non-empty bounded text")
        workflow = load_workflow(self.platform, artifact_id, budget=self.budget)
        supplied = dict(input_artifacts)
        if set(supplied) != set(workflow.input_keys):
            raise ValidationError("approval inputs must exactly match the validated plan")
        plan_artifact = self.platform.store.get(artifact_id)
        if tuple(sorted(supplied.values())) != tuple(sorted(plan_artifact.parents)):
            raise ValidationError("approval input identities differ from the plan lineage")
        for artifact_id_value in supplied.values():
            self.platform.store.get(artifact_id_value)
        execution_context = context or ExecutionContext(
            service_id="molecularis-ai", budget=self.budget
        )
        payload = {
            "schema": "molecularis.execution-approval.v1",
            "approval_scope": "single-execution",
            "approval_id": approval_id,
            "principal_id": principal_id,
            "plan_artifact_id": artifact_id,
            "workflow_sha256": workflow.sha256,
            "input_artifact_ids": sorted(supplied.values()),
            "capability_catalog_sha256": hashlib.sha256(json.dumps(
                self.capability_catalog(), sort_keys=True, separators=(",", ":"),
                ensure_ascii=False, allow_nan=False,
            ).encode("utf-8")).hexdigest(),
            "budget_sha256": hashlib.sha256(json.dumps({
                "max_bytes": execution_context.budget.max_bytes,
                "max_candidates": execution_context.budget.max_candidates,
                "max_results": execution_context.budget.max_results,
                "max_wall_seconds": execution_context.budget.max_wall_seconds,
                "chunk_bytes": execution_context.budget.chunk_bytes,
            }, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
            "policy_sha256": hashlib.sha256(self.execution_policy_id.encode("utf-8")).hexdigest(),
            "execution_context": {
                "service_id": execution_context.service_id,
                "engine_version": execution_context.engine_version,
                "schema_version": execution_context.schema_version,
                "rulebook_version": execution_context.rulebook_version,
                "parameters": execution_context.parameters,
            },
        }
        return json.dumps(
            payload, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")

    def execute(
        self, plan: AIPlan | str, *, input_artifacts: Mapping[str, str],
        approval: ExecutionApproval | None = None,
        approval_verifier: ApprovalVerifier | None = None,
        context: ExecutionContext | None = None,
    ) -> dict[str, Any]:
        """Execute only with externally authenticated, scope-bound approval."""
        if not isinstance(approval, ExecutionApproval) or not callable(approval_verifier):
            raise ValidationError(
                "an externally authenticated ExecutionApproval and verifier are required"
            )
        if any(not isinstance(value, str) or not value.strip() for value in (
            approval.approval_id, approval.principal_id, approval.signature
        )):
            raise ValidationError("approval identity and signature fields must be non-empty")
        artifact_id = plan.artifact_id if isinstance(plan, AIPlan) else plan
        if approval.plan_artifact_id != artifact_id:
            raise ValidationError("approval is bound to a different plan artifact")
        payload = self.approval_payload(
            plan, input_artifacts=input_artifacts, approval_id=approval.approval_id,
            principal_id=approval.principal_id, context=context,
        )
        parsed = json.loads(payload)
        expected_inputs = tuple(parsed["input_artifact_ids"])
        if approval.input_artifact_ids != expected_inputs:
            raise ValidationError("approval is bound to different input artifact identities")
        if approval.capability_catalog_sha256 != parsed["capability_catalog_sha256"]:
            raise ValidationError("approval capability catalog fingerprint is stale")
        if approval.budget_sha256 != parsed["budget_sha256"]:
            raise ValidationError("approval resource budget fingerprint is stale")
        if approval.policy_sha256 != parsed["policy_sha256"]:
            raise ValidationError("approval execution policy fingerprint is stale")
        try:
            verified = approval_verifier(payload, approval.signature, approval.principal_id)
        except Exception as exc:
            raise ValidationError("approval verifier rejected the approval") from exc
        if verified is not True:
            raise ValidationError("approval signature or principal authentication failed")
        workflow = load_workflow(self.platform, artifact_id, budget=self.budget)
        if workflow.source != "molecularis_ai":
            raise ValidationError("workflow artifact was not generated by Molecularis AI")
        supplied = dict(input_artifacts)
        if set(supplied) != set(workflow.input_keys):
            raise ValidationError("execution inputs must exactly match the validated plan")
        plan_artifact = self.platform.store.get(artifact_id)
        if tuple(sorted(supplied.values())) != tuple(sorted(plan_artifact.parents)):
            raise ValidationError("execution artifact identities differ from the approved plan inputs")
        for artifact_id_value in supplied.values():
            self.platform.store.get(artifact_id_value)
        context = context or ExecutionContext(service_id="molecularis-ai", budget=self.budget)
        result = execute_workflow(self.platform, workflow, supplied, context=context)
        return {
            "schema": AI_REPORT_SCHEMA, "workflow_id": workflow.workflow_id,
            "workflow_sha256": workflow.sha256, "plan_artifact_id": artifact_id,
            "planner_id": self.planner_id, "result": result, "run_id": context.run_id,
            "approval_id": approval.approval_id, "approved_by": approval.principal_id,
            "limitations": [
                "Model-generated plans are proposals, not scientific conclusions.",
                "Execution requires a one-use externally authenticated approval bound to this exact plan, inputs, capability catalog, resource budget and policy.",
                "Scientific correctness and external-engine validity require independent validation.",
            ],
        }
