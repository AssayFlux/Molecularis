"""Simulation H: provenance-bound protocol artifacts and bounded energy analysis."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib,json,math,re
from typing import Any
from .gromacs import run_gromacs
from .platform import Artifact,Budget,Capability,ExecutionContext,MolecularisPlatform,Operation,Rulebook
from .platform.contracts import ResourceLimitError,ValidationError
SIMULATION_SCHEMA_ID="molecularis.simulation-job.v1"
SIMULATION_REF_SCHEMA_ID="molecularis.simulation-artifact-reference.v1"
SIMULATION_REPORT_SCHEMA_ID="molecularis.simulation-operation-report.v1"
SIMULATION_MEDIA_TYPE="application/vnd.molecularis.simulation-job+json"
SIMULATION_RULEBOOK_ID="simulation-core-v1"
_SHA=re.compile(r"^[0-9a-f]{64}$")
_CAPS={"validate":"simulation.validate.v1","energy_analysis":"simulation.energy-analysis.v1","gromacs_run":"simulation.gromacs-run.v1"}
_RULES=["SIM-001","SIM-002","SIM-003","SIM-004","SIM-005","SIM-006","SIM-007"]

@dataclass(frozen=True,slots=True)
class SimulationDocument:
    identifier:str
    engine:str
    ensemble:str
    temperature_kelvin:float
    timestep_fs:float
    steps:int
    equilibration_steps:int
    replicas:int
    seed:int
    coordinates_sha256:str
    topology_sha256:str
    force_field_name:str
    force_field_version:str
    parameter_source_sha256:str
    pressure_bar:float|None=None
    report_interval:int=100
    gromacs_tpr_path:str|None=None
    gromacs_tpr_sha256:str|None=None
    gromacs_executable_path:str|None=None
    gromacs_executable_sha256:str|None=None
    gromacs_threads:int=1
    gromacs_timeout_seconds:int=86400
    energy_series:tuple[float,...]=()
    energy_unit:str="kJ/mol"
    def __post_init__(self)->None:
        if not isinstance(self.identifier,str) or not self.identifier.strip() or len(self.identifier)>256: raise ValueError("identifier must contain 1..256 characters")
        if self.engine not in {"openmm","gromacs"}: raise ValueError("engine must be openmm or gromacs")
        if self.ensemble not in {"NVT","NPT"}: raise ValueError("ensemble must be NVT or NPT")
        for name,value in (("coordinates_sha256",self.coordinates_sha256),("topology_sha256",self.topology_sha256),("parameter_source_sha256",self.parameter_source_sha256)):
            if not isinstance(value,str) or not _SHA.fullmatch(value): raise ValueError(f"{name} must be lowercase SHA-256 hex")
        for name,value,maximum in (("temperature_kelvin",self.temperature_kelvin,2000.0),("timestep_fs",self.timestep_fs,4.0)):
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0<value<=maximum: raise ValueError(f"{name} must be finite and in (0, {maximum}]")
        if self.pressure_bar is not None and (isinstance(self.pressure_bar,bool) or not isinstance(self.pressure_bar,(int,float)) or not math.isfinite(self.pressure_bar) or not 0<self.pressure_bar<=10000): raise ValueError("pressure_bar must be finite and positive")
        if self.ensemble=="NPT" and self.pressure_bar is None: raise ValueError("NPT requires pressure_bar")
        if self.ensemble=="NVT" and self.pressure_bar is not None: raise ValueError("NVT must not specify pressure_bar")
        for name,value,low,high in (("steps",self.steps,1,10_000_000),("equilibration_steps",self.equilibration_steps,0,1_000_000),("replicas",self.replicas,2,10),("seed",self.seed,0,2**32-1),("report_interval",self.report_interval,1,10_000_000),("gromacs_threads",self.gromacs_threads,1,256),("gromacs_timeout_seconds",self.gromacs_timeout_seconds,1,604800)):
            if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high: raise ValueError(f"{name} must be an integer in [{low}, {high}]")
        if self.report_interval>self.steps: raise ValueError("report_interval must not exceed steps")
        if self.steps*self.replicas>50_000_000: raise ValueError("steps times replicas exceeds 50000000")
        if not all(isinstance(x,str) and x.strip() for x in (self.force_field_name,self.force_field_version)): raise ValueError("force-field name and version are required")
        if self.engine=="gromacs":
            if not all(isinstance(x,str) and x.strip() for x in (self.gromacs_tpr_path,self.gromacs_executable_path)): raise ValueError("GROMACS requires local TPR and executable paths")
            if not isinstance(self.gromacs_tpr_sha256,str) or not _SHA.fullmatch(self.gromacs_tpr_sha256): raise ValueError("GROMACS TPR digest must be lowercase SHA-256")
            if not isinstance(self.gromacs_executable_sha256,str) or not _SHA.fullmatch(self.gromacs_executable_sha256): raise ValueError("GROMACS executable digest must be lowercase SHA-256")
        if not isinstance(self.energy_unit,str) or not self.energy_unit.strip(): raise ValueError("energy_unit must be non-empty")
        if len(self.energy_series)>1_000_000: raise ValueError("energy_series exceeds 1000000 samples")
        if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in self.energy_series): raise ValueError("energy_series must contain finite numbers")
    def to_dict(self)->dict[str,Any]:
        return {"schema":SIMULATION_SCHEMA_ID,"identifier":self.identifier,"engine":self.engine,"ensemble":self.ensemble,"temperature_kelvin":self.temperature_kelvin,"pressure_bar":self.pressure_bar,"timestep_fs":self.timestep_fs,"steps":self.steps,"equilibration_steps":self.equilibration_steps,"replicas":self.replicas,"seed":self.seed,"report_interval":self.report_interval,"coordinates_sha256":self.coordinates_sha256,"topology_sha256":self.topology_sha256,"force_field":{"name":self.force_field_name,"version":self.force_field_version,"parameter_source_sha256":self.parameter_source_sha256},"gromacs":{"tpr_path":self.gromacs_tpr_path,"tpr_sha256":self.gromacs_tpr_sha256,"executable_path":self.gromacs_executable_path,"executable_sha256":self.gromacs_executable_sha256,"threads":self.gromacs_threads,"timeout_seconds":self.gromacs_timeout_seconds},"energy_series":list(self.energy_series),"energy_unit":self.energy_unit}
    def to_json(self)->bytes: return json.dumps(self.to_dict(),sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode()
    @property
    def sha256(self)->str: return hashlib.sha256(self.to_json()).hexdigest()
    @classmethod
    def from_json(cls,payload:bytes|str)->"SimulationDocument":
        def unique(pairs:list[tuple[str,Any]])->dict[str,Any]:
            out={}
            for k,v in pairs:
                if k in out: raise ValueError(f"duplicate JSON key: {k}")
                out[k]=v
            return out
        try:
            raw=payload.decode("utf-8") if isinstance(payload,bytes) else payload
            v=json.loads(raw,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc: raise ValueError(f"invalid simulation JSON: {exc}") from exc
        expected={"schema","identifier","engine","ensemble","temperature_kelvin","pressure_bar","timestep_fs","steps","equilibration_steps","replicas","seed","report_interval","coordinates_sha256","topology_sha256","force_field","gromacs","energy_series","energy_unit"}
        if not isinstance(v,dict) or set(v)!=expected or v.get("schema")!=SIMULATION_SCHEMA_ID: raise ValueError("simulation document fields/schema do not match v1")
        ff=v["force_field"]; gm=v["gromacs"]
        if not isinstance(ff,dict) or set(ff)!={"name","version","parameter_source_sha256"}: raise ValueError("invalid force_field object")
        if not isinstance(gm,dict) or set(gm)!={"tpr_path","tpr_sha256","executable_path","executable_sha256","threads","timeout_seconds"}: raise ValueError("invalid gromacs object")
        return cls(v["identifier"],v["engine"],v["ensemble"],v["temperature_kelvin"],v["timestep_fs"],v["steps"],v["equilibration_steps"],v["replicas"],v["seed"],v["coordinates_sha256"],v["topology_sha256"],ff["name"],ff["version"],ff["parameter_source_sha256"],v["pressure_bar"],v["report_interval"],gm["tpr_path"],gm["tpr_sha256"],gm["executable_path"],gm["executable_sha256"],gm["threads"],gm["timeout_seconds"],tuple(v["energy_series"]),v["energy_unit"])

def ingest_simulation(platform:MolecularisPlatform,record:SimulationDocument,*,parents:tuple[str,...]=(),budget:Budget|None=None)->Artifact:
    if not isinstance(record,SimulationDocument): raise TypeError("record must be SimulationDocument")
    return platform.ingest(record.to_json(),media_type=SIMULATION_MEDIA_TYPE,schema_id=SIMULATION_SCHEMA_ID,metadata={"identifier":record.identifier,"engine":record.engine,"ensemble":record.ensemble,"protocol_sha256":record.sha256,"coordinates_sha256":record.coordinates_sha256,"topology_sha256":record.topology_sha256},parents=parents,budget=budget)

def load_simulation(platform:MolecularisPlatform,artifact_id:str,*,budget:Budget|None=None)->SimulationDocument:
    budget=budget or Budget(); art=platform.store.get(artifact_id)
    if art.media_type!=SIMULATION_MEDIA_TYPE or art.schema_id!=SIMULATION_SCHEMA_ID: raise ValidationError("artifact is not a simulation protocol v1")
    if art.size_bytes>budget.max_bytes: raise ResourceLimitError("simulation artifact exceeds byte budget")
    record=SimulationDocument.from_json(b"".join(platform.store.read(artifact_id,budget=budget)))
    meta={"identifier":record.identifier,"engine":record.engine,"ensemble":record.ensemble,"protocol_sha256":record.sha256,"coordinates_sha256":record.coordinates_sha256,"topology_sha256":record.topology_sha256}
    if record.sha256!=art.digest or any(art.metadata.get(k)!=v for k,v in meta.items()): raise ValidationError("simulation protocol integrity or metadata mismatch")
    return record

def analyze_energy_series(values:tuple[float,...]|list[float],*,unit_name:str="kJ/mol")->dict[str,Any]:
    if not isinstance(values,(tuple,list)) or not 2<=len(values)<=1_000_000: raise ValueError("energy series requires 2..1000000 samples")
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in values): raise ValueError("energy samples must be finite numbers")
    n=len(values); mean=math.fsum(values)/n; variance=math.fsum((x-mean)**2 for x in values)/n
    xmean=(n-1)/2; denom=math.fsum((i-xmean)**2 for i in range(n))
    slope=math.fsum((i-xmean)*(v-mean) for i,v in enumerate(values))/denom if denom else 0.0
    return {"sample_count":n,"unit":unit_name,"mean":mean,"population_stddev":math.sqrt(variance),"minimum":min(values),"maximum":max(values),"range":max(values)-min(values),"first":values[0],"last":values[-1],"net_change":values[-1]-values[0],"linear_slope_per_sample":slope,"interpretation":"descriptive_only_no_equilibration_or_ensemble_acceptance_inferred"}

def _run(op:str,record:SimulationDocument,params:dict[str,Any],budget:Budget)->dict[str,Any]:
    if op=="validate": return {"valid":True,"engine":record.engine,"ensemble":record.ensemble,"temperature_kelvin":record.temperature_kelvin,"pressure_bar":record.pressure_bar,"steps":record.steps,"equilibration_steps":record.equilibration_steps,"replicas":record.replicas,"estimated_frames_per_replica":(record.steps+record.report_interval-1)//record.report_interval,"protocol_sha256":record.sha256,"execution":"not_started"}
    if op=="energy_analysis": return analyze_energy_series(record.energy_series,unit_name=record.energy_unit)
    if op=="gromacs_run":
        if record.engine!="gromacs": raise ValidationError("gromacs_run requires a GROMACS protocol")
        output=params.get("output_directory")
        if not isinstance(output,str) or not output.strip(): raise ValidationError("output_directory must be supplied as an explicit local path")
        return run_gromacs(record.gromacs_tpr_path,output,executable_path=record.gromacs_executable_path,executable_sha256=record.gromacs_executable_sha256,tpr_sha256=record.gromacs_tpr_sha256,force_field_manifest={"name":record.force_field_name,"version":record.force_field_version,"parameter_source_sha256":record.parameter_source_sha256},run_id=params.get("run_id",record.identifier),threads=record.gromacs_threads,timeout_seconds=min(record.gromacs_timeout_seconds,int(budget.max_wall_seconds)),max_tpr_bytes=budget.max_bytes,max_output_bytes=budget.max_bytes)
    raise ValidationError(f"unsupported simulation operation: {op}")

def register_simulation_service(platform:MolecularisPlatform)->None:
    descriptions={"validate":"Validate a canonical simulation protocol and provenance envelope","energy_analysis":"Descriptive bounded analysis of caller-supplied potential-energy samples","gromacs_run":"Execute hash-pinned GROMACS against an approved caller-prepared TPR"}
    for op,cap in _CAPS.items():
        platform.register(Capability(id=cap,version="1.0.0",service="simulation",operation=op,input_schema=SIMULATION_REF_SCHEMA_ID,output_schema=SIMULATION_REPORT_SCHEMA_ID,deterministic=op!="gromacs_run",description=descriptions[op]))
        def handler(inputs:dict[str,Any],parameters:dict[str,Any],context:ExecutionContext,selected:str=op)->dict[str,Any]:
            if len(inputs)!=1: raise ValidationError("simulation operation requires exactly one protocol artifact")
            artifact_id=next(iter(inputs.values()))
            if not isinstance(artifact_id,str): raise ValidationError("simulation artifact ID must be text")
            record=load_simulation(platform,artifact_id,budget=context.budget); result=_run(selected,record,parameters,context.budget)
            return {"schema":SIMULATION_REPORT_SCHEMA_ID,"operation":selected,"simulation_id":record.identifier,"protocol_sha256":record.sha256,"result":result,"rulebook":SIMULATION_RULEBOOK_ID,"rules_checked":_RULES,"limitations":["Protocol validity is not physical validity","Force-field provenance is caller-declared and not independently inspected","OpenMM execution remains an explicit in-process API requiring caller-constructed trusted System/Topology/positions","GROMACS requires a locally installed hash-pinned executable and caller-prepared TPR","No independent scientific or experimental validation is claimed"]}
        platform.bind(cap,handler)

def simulation_rulebook(operation:str,artifact_key:str="simulation_artifact_id",*,parameters:dict[str,Any]|None=None)->Rulebook:
    if operation not in _CAPS: raise ValueError(f"unsupported simulation operation: {operation}")
    if not isinstance(artifact_key,str) or not artifact_key.strip(): raise ValueError("artifact_key must be non-empty")
    return Rulebook(id=SIMULATION_RULEBOOK_ID,version="1.0.0",operations=(Operation(id=f"{operation}-simulation",capability_id=_CAPS[operation],inputs=(artifact_key,),output="simulation_result",parameters=dict(parameters or {})),))
