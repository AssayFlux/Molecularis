from __future__ import annotations
import pytest
from molecularis.platform import Capability, ExecutionContext, MolecularisPlatform
from molecularis.platform.contracts import ValidationError
from molecularis.workflows_service import WorkflowDocument,WorkflowOperation,execute_workflow,ingest_workflow,load_workflow,register_workflows_service,validate_workflow,workflows_rulebook

def fixture():
    return WorkflowDocument("demo",(
      WorkflowOperation("second","test.double.v1",("first_result",),"second_result",'{"factor":2}'),
      WorkflowOperation("first","test.add.v1",("source_artifact",),"first_result",'{"offset":1}')),
      ("source_artifact",),provenance=(("fixture","synthetic"),))

def platform_fixture(tmp_path):
    p=MolecularisPlatform(tmp_path); p.start()
    p.register(Capability("test.add.v1","1","test","add","input","output"))
    p.register(Capability("test.double.v1","1","test","double","input","output"))
    p.bind("test.add.v1",lambda i,params,ctx:{"value":int(i["source_artifact"])+params["offset"]})
    p.bind("test.double.v1",lambda i,params,ctx:{"value":i["first_result"]["value"]*params["factor"]})
    register_workflows_service(p); return p

def test_canonical_round_trip_digest():
    w=fixture(); loaded=WorkflowDocument.from_json(w.to_json())
    assert loaded==w and loaded.sha256==w.sha256 and loaded.to_json()==w.to_json()

def test_topological_order_is_deterministic():
    assert [x.operation_id for x in fixture().topological_order()]==["first","second"]

def test_missing_inputs_and_cycles_rejected():
    with pytest.raises(ValueError,match="undeclared inputs"): WorkflowDocument("missing",(WorkflowOperation("op","x.y",("absent",),"out"),),())
    with pytest.raises(ValueError,match="cycle"): WorkflowDocument("cycle",(WorkflowOperation("a","x.y",("b_out",),"a_out"),WorkflowOperation("b","x.y",("a_out",),"b_out")),())

def test_duplicate_ids_and_outputs_rejected():
    with pytest.raises(ValueError,match="operation IDs"): WorkflowDocument("dup",(WorkflowOperation("same","x.y",("i",),"o1"),WorkflowOperation("same","x.y",("i",),"o2")),("i",))
    with pytest.raises(ValueError,match="output keys"): WorkflowDocument("dupout",(WorkflowOperation("a","x.y",("i",),"same"),WorkflowOperation("b","x.y",("i",),"same")),("i",))

def test_artifact_lifecycle_and_registry_validation(tmp_path):
    p=platform_fixture(tmp_path)
    try:
        w=fixture(); a=ingest_workflow(p,w); assert load_workflow(p,a.artifact_id)==w
        report=validate_workflow(p,w); assert report["execution_order"]==["first","second"] and report["operation_count"]==2
    finally: p.close()

def test_end_to_end_execution_and_lineage(tmp_path):
    p=platform_fixture(tmp_path)
    try:
        a=p.ingest(b"41",media_type="text/plain",schema_id="test.input")
        result=execute_workflow(p,fixture(),{"source_artifact":a.artifact_id},context=ExecutionContext(service_id="workflows"))
        assert result["first_result"]=={"value":42} and result["second_result"]=={"value":84}
        run=p.store.list_runs(limit=10)[0]
        assert run["status"]=="succeeded" and len(run["outputs"])==2 and a.artifact_id in run["inputs"]
    finally: p.close()

def test_registered_validate_and_plan_capabilities(tmp_path):
    p=platform_fixture(tmp_path)
    try:
        a=ingest_workflow(p,fixture()); initial={"workflow_artifact_id":a.artifact_id}
        assert p.execute(workflows_rulebook("validate"),initial)["workflows_result"]["result"]["valid"]
        assert p.execute(workflows_rulebook("plan"),initial)["workflows_result"]["result"]["execution_order"]==["first","second"]
    finally: p.close()

def test_exact_initial_inputs_required(tmp_path):
    p=platform_fixture(tmp_path)
    try:
        with pytest.raises(ValidationError,match="exactly match"): execute_workflow(p,fixture(),{"source_artifact":"x","extra":"y"})
    finally: p.close()

def test_unregistered_capability_rejected(tmp_path):
    p=MolecularisPlatform(tmp_path); p.start()
    try:
        w=WorkflowDocument("unknown",(WorkflowOperation("op","missing.capability.v1",("input",),"out"),),("input",))
        with pytest.raises(ValidationError,match="not registered"): validate_workflow(p,w)
    finally: p.close()
