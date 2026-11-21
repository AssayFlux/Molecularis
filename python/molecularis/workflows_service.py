"""Molecularis-native cross-service workflow orchestration on the MSDE Rulebook DAG."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, json, re
from typing import Any
from .platform import Budget, Capability, ExecutionContext, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

WORKFLOW_SCHEMA_ID="molecularis.workflow.v1"
WORKFLOW_MEDIA_TYPE="application/vnd.molecularis.workflow+json"
WORKFLOW_REPORT_SCHEMA_ID="molecularis.workflow-report.v1"
WORKFLOW_RULEBOOK_ID="workflows-core-v1"
_CAPABILITIES={"validate":"workflows.validate.v1","plan":"workflows.plan.v1"}
_ID=re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
_MAX_OPERATIONS=100
_MAX_INPUTS=256
_MAX_PARAMETERS_BYTES=64*1024

@dataclass(frozen=True, slots=True)
class WorkflowOperation:
    operation_id: str
    capability_id: str
    inputs: tuple[str,...]
    output: str
    parameters_json: str="{}"
    def __post_init__(self):
        for name,value in (("operation_id",self.operation_id),("capability_id",self.capability_id),("output",self.output)):
            if not isinstance(value,str) or not _ID.fullmatch(value): raise ValueError(f"{name} must be a safe bounded identifier")
        if not isinstance(self.inputs,tuple) or not 1<=len(self.inputs)<=_MAX_INPUTS: raise ValueError(f"inputs must contain 1..{_MAX_INPUTS} keys")
        if any(not isinstance(x,str) or not _ID.fullmatch(x) for x in self.inputs) or len(set(self.inputs))!=len(self.inputs): raise ValueError("input keys must be unique safe identifiers")
        if not isinstance(self.parameters_json,str) or len(self.parameters_json.encode())>_MAX_PARAMETERS_BYTES: raise ValueError("parameters_json exceeds byte limit")
        try: params=json.loads(self.parameters_json,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except (json.JSONDecodeError,ValueError) as exc: raise ValueError("parameters_json must contain finite valid JSON") from exc
        if not isinstance(params,dict): raise ValueError("operation parameters must be a JSON object")
        object.__setattr__(self,"parameters_json",json.dumps(params,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")))
    @property
    def parameters(self): return json.loads(self.parameters_json)

@dataclass(frozen=True, slots=True)
class WorkflowDocument:
    workflow_id: str
    operations: tuple[WorkflowOperation,...]
    input_keys: tuple[str,...]
    version: str="1.0.0"
    source: str="molecularis_native"
    provenance: tuple[tuple[str,str],...]=()
    def __post_init__(self):
        if not isinstance(self.workflow_id,str) or not _ID.fullmatch(self.workflow_id): raise ValueError("workflow_id must be a safe bounded identifier")
        if not isinstance(self.version,str) or not _ID.fullmatch(self.version): raise ValueError("version must be a safe bounded identifier")
        if not isinstance(self.source,str) or not self.source.strip() or len(self.source)>256: raise ValueError("source must be non-empty bounded text")
        if not isinstance(self.operations,tuple) or not 1<=len(self.operations)<=_MAX_OPERATIONS: raise ValueError(f"operations must contain 1..{_MAX_OPERATIONS}")
        if not isinstance(self.input_keys,tuple) or len(self.input_keys)>_MAX_INPUTS or any(not isinstance(k,str) or not _ID.fullmatch(k) for k in self.input_keys): raise ValueError("input_keys must be safe bounded identifiers")
        if len(set(self.input_keys))!=len(self.input_keys): raise ValueError("input_keys must be unique")
        if not isinstance(self.provenance,tuple) or len(self.provenance)>128: raise ValueError("provenance must be bounded")
        seen=set()
        for pair in self.provenance:
            if not isinstance(pair,tuple) or len(pair)!=2: raise ValueError("provenance entries must be key/value pairs")
            k,v=pair
            if not isinstance(k,str) or not k.strip() or len(k)>128 or k in seen or not isinstance(v,str) or len(v)>512: raise ValueError("provenance must contain unique bounded text")
            seen.add(k)
        ids=[o.operation_id for o in self.operations]; outputs=[o.output for o in self.operations]
        if len(set(ids))!=len(ids): raise ValueError("operation IDs must be unique")
        if len(set(outputs))!=len(outputs): raise ValueError("operation output keys must be unique")
        if set(outputs)&set(self.input_keys): raise ValueError("operation outputs cannot shadow declared workflow inputs")
        self.topological_order()
    def topological_order(self):
        producers={o.output:o.operation_id for o in self.operations}; available=set(self.input_keys); pending=list(self.operations); ordered=[]
        while pending:
            ready=[o for o in pending if all(k in available for k in o.inputs)]
            if not ready:
                missing=sorted({k for o in pending for k in o.inputs if k not in available and k not in producers})
                if missing: raise ValueError(f"workflow references undeclared inputs: {missing}")
                raise ValueError("workflow contains a dependency cycle")
            for op in ready: ordered.append(op); available.add(op.output); pending.remove(op)
        return tuple(ordered)
    def to_dict(self):
        return {"schema":WORKFLOW_SCHEMA_ID,"workflow_id":self.workflow_id,"version":self.version,"source":self.source,
          "input_keys":list(self.input_keys),"provenance":dict(self.provenance),"operations":[
          {"operation_id":o.operation_id,"capability_id":o.capability_id,"inputs":list(o.inputs),"output":o.output,"parameters":o.parameters} for o in self.operations]}
    def to_json(self): return json.dumps(self.to_dict(),sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode()
    @property
    def sha256(self): return hashlib.sha256(self.to_json()).hexdigest()
    def to_rulebook(self,registry,*,max_steps=_MAX_OPERATIONS):
        if isinstance(max_steps,bool) or not isinstance(max_steps,int) or not 1<=max_steps<=_MAX_OPERATIONS: raise ValueError(f"max_steps must be in 1..{_MAX_OPERATIONS}")
        if len(self.operations)>max_steps: raise ResourceLimitError("workflow exceeds configured operation budget")
        for op in self.operations: registry.get(op.capability_id)
        return Rulebook(id=f"{WORKFLOW_RULEBOOK_ID}:{self.workflow_id}",version=self.version,
          operations=tuple(Operation(id=o.operation_id,capability_id=o.capability_id,inputs=o.inputs,output=o.output,parameters=o.parameters) for o in self.topological_order()),max_steps=max_steps)
    @classmethod
    def from_json(cls,payload):
        def unique(pairs):
            d={}
            for k,v in pairs:
                if k in d: raise ValueError(f"duplicate JSON key: {k}")
                d[k]=v
            return d
        try: value=json.loads(payload.decode() if isinstance(payload,bytes) else payload,object_pairs_hook=unique,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc: raise ValueError(f"invalid Workflow JSON: {exc}") from exc
        required={"schema","workflow_id","version","source","input_keys","provenance","operations"}
        if not isinstance(value,dict) or set(value)!=required or value["schema"]!=WORKFLOW_SCHEMA_ID: raise ValueError("Workflow document fields/schema do not match v1")
        if not isinstance(value["operations"],list) or not isinstance(value["input_keys"],list) or not isinstance(value["provenance"],dict): raise ValueError("Workflow arrays/objects have invalid types")
        ops=[]
        for item in value["operations"]:
            if not isinstance(item,dict) or set(item)!={"operation_id","capability_id","inputs","output","parameters"} or not isinstance(item["inputs"],list) or not isinstance(item["parameters"],dict): raise ValueError("Workflow operation fields/types do not match v1")
            ops.append(WorkflowOperation(item["operation_id"],item["capability_id"],tuple(item["inputs"]),item["output"],json.dumps(item["parameters"],sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":"))))
        return cls(value["workflow_id"],tuple(ops),tuple(value["input_keys"]),value["version"],value["source"],tuple(sorted(value["provenance"].items())))

def ingest_workflow(platform,workflow,*,parents=(),budget=None):
    if not isinstance(workflow,WorkflowDocument): raise TypeError("workflow must be a WorkflowDocument")
    payload=workflow.to_json()
    if budget is not None and len(payload)>budget.max_bytes: raise ResourceLimitError("workflow artifact exceeds byte budget")
    return platform.ingest(payload,media_type=WORKFLOW_MEDIA_TYPE,schema_id=WORKFLOW_SCHEMA_ID,
      metadata={"workflow_id":workflow.workflow_id,"workflow_sha256":workflow.sha256,"operation_count":len(workflow.operations)},parents=parents,budget=budget)

def load_workflow(platform,artifact_id,*,budget=None):
    budget=budget or Budget(); artifact=platform.store.get(artifact_id)
    if artifact.media_type!=WORKFLOW_MEDIA_TYPE or artifact.schema_id!=WORKFLOW_SCHEMA_ID: raise ValidationError("artifact is not a Workflow v1")
    if artifact.size_bytes>budget.max_bytes: raise ResourceLimitError("workflow artifact exceeds byte budget")
    workflow=WorkflowDocument.from_json(b"".join(platform.store.read(artifact_id,budget=budget)))
    if artifact.digest!=workflow.sha256 or artifact.metadata.get("workflow_sha256")!=workflow.sha256 or artifact.metadata.get("workflow_id")!=workflow.workflow_id: raise ValidationError("workflow artifact integrity or metadata mismatch")
    if len(workflow.operations)>budget.max_candidates: raise ResourceLimitError("workflow exceeds operation budget")
    return workflow

def validate_workflow(platform,workflow):
    ordered=workflow.to_rulebook(platform.registry).validate(platform.registry)
    return {"valid":True,"workflow_id":workflow.workflow_id,"version":workflow.version,"operation_count":len(ordered),"execution_order":[o.id for o in ordered],"input_keys":list(workflow.input_keys),"workflow_sha256":workflow.sha256}

def execute_workflow(platform,workflow,initial,*,context=None,max_steps=_MAX_OPERATIONS):
    if not isinstance(initial,dict) or set(initial)!=set(workflow.input_keys): raise ValidationError("initial workflow values must exactly match declared input_keys")
    if any(not isinstance(k,str) or not _ID.fullmatch(k) or not isinstance(v,str) or not v for k,v in initial.items()): raise ValidationError("workflow initial keys/values must be safe keys and non-empty strings")
    return platform.execute(workflow.to_rulebook(platform.registry,max_steps=max_steps),initial,context=context)

def register_workflows_service(platform):
    for operation,capability_id in _CAPABILITIES.items():
        platform.register(Capability(id=capability_id,version="1.0.0",service="workflows",operation=operation,input_schema=WORKFLOW_SCHEMA_ID,output_schema=WORKFLOW_REPORT_SCHEMA_ID,deterministic=True,description=f"Validate or plan a canonical workflow against registered capabilities ({operation})."))
        def handler(inputs,parameters,context,selected=operation):
            if len(inputs)!=1: raise ValidationError("workflow operation requires one workflow artifact")
            workflow=load_workflow(platform,next(iter(inputs.values())),budget=context.budget)
            report=validate_workflow(platform,workflow)
            return {"schema":WORKFLOW_REPORT_SCHEMA_ID,"operation":selected,**report,
              "limitations":["Validation checks graph contracts and capability registration, not scientific correctness.","Planning does not execute scientific capabilities."]}
        platform.bind(capability_id,handler)

def workflows_rulebook(operation,*,workflow_key="workflow_artifact_id"):
    if operation not in _CAPABILITIES: raise ValueError(f"unsupported Workflows operation: {operation}")
    if not isinstance(workflow_key,str) or not _ID.fullmatch(workflow_key): raise ValueError("workflow_key must be a safe identifier")
    return Rulebook(id=WORKFLOW_RULEBOOK_ID,version="1.0.0",operations=(Operation(id=f"{operation}-workflow",capability_id=_CAPABILITIES[operation],inputs=(workflow_key,),output="workflows_result",parameters={}),))
