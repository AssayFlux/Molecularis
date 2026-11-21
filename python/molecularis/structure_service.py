"""Structure service C: immutable coordinate artifacts and bounded geometry capabilities."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, json
from math import isfinite
from typing import Any
from .platform import Artifact, Budget, Capability, ExecutionContext, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError
from .structure import Atom, contact_pairs, interaction_candidates, parse_mmcif, parse_pdb, rmsd, solvent_accessible_surface_area

STRUCTURE_SCHEMA_ID="molecularis.structure-record.v1"
STRUCTURE_REFERENCE_SCHEMA_ID="molecularis.structure-artifact-reference.v1"
STRUCTURE_REPORT_SCHEMA_ID="molecularis.structure-operation-report.v1"
STRUCTURE_MEDIA_TYPE="application/vnd.molecularis.structure+json"
STRUCTURE_RULEBOOK_ID="structure-core-v1"
OPS={"validate":"structure.validate.v1","geometry":"structure.geometry.v1","contacts":"structure.contacts.v1","sasa":"structure.sasa.v1","interactions":"structure.interactions.v1","rmsd":"structure.rmsd.v1"}

@dataclass(frozen=True, slots=True)
class StructureDocument:
    identifier: str
    atoms: tuple[Atom,...]
    source_format: str="native"
    model_number: int=1
    coordinate_unit: str="angstrom"
    coordinate_system: str="cartesian_right_handed"
    def __post_init__(self):
        if not isinstance(self.identifier,str) or not self.identifier.strip() or len(self.identifier)>256 or any(ord(c)<32 for c in self.identifier): raise ValueError("identifier must be bounded non-empty text")
        if not isinstance(self.atoms,tuple) or not self.atoms or len(self.atoms)>100000 or any(not isinstance(a,Atom) for a in self.atoms): raise ValueError("atoms must be a non-empty tuple of at most 100000 Atom records")
        if self.source_format not in {"native","pdb","mmcif"}: raise ValueError("unsupported source_format")
        if isinstance(self.model_number,bool) or not isinstance(self.model_number,int) or self.model_number<1: raise ValueError("model_number must be positive")
        if self.coordinate_unit!="angstrom" or self.coordinate_system!="cartesian_right_handed": raise ValueError("v1 requires right-handed Cartesian Angstroms")
        serials=[a.serial for a in self.atoms]
        if len(serials)!=len(set(serials)): raise ValueError("atom serials must be unique")
        for a in self.atoms:
            if isinstance(a.serial,bool) or not isinstance(a.serial,int) or a.serial<0: raise ValueError("atom serials must be non-negative integers")
            if any(not isinstance(v,str) for v in (a.name,a.residue,a.chain,a.element)) or not a.name.strip() or not a.residue.strip() or not a.element.strip(): raise ValueError("atom labels must be non-empty strings")
            if isinstance(a.residue_number,bool) or not isinstance(a.residue_number,int): raise ValueError("residue_number must be an integer")
            if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and isfinite(v) for v in (a.x,a.y,a.z)): raise ValueError("coordinates must be finite real numbers")
    @classmethod
    def from_pdb(cls,identifier,text,*,include_hetero=False): return cls(identifier,tuple(parse_pdb(text,include_hetero=include_hetero)),"pdb")
    @classmethod
    def from_mmcif(cls,identifier,text,*,include_hetero=False): return cls(identifier,tuple(parse_mmcif(text,include_hetero=include_hetero)),"mmcif")
    def to_dict(self):
        return {"schema":STRUCTURE_SCHEMA_ID,"identifier":self.identifier,"source_format":self.source_format,"model_number":self.model_number,"coordinate_unit":self.coordinate_unit,"coordinate_system":self.coordinate_system,"atoms":[{"serial":a.serial,"name":a.name,"residue":a.residue,"chain":a.chain,"residue_number":a.residue_number,"x":a.x,"y":a.y,"z":a.z,"element":a.element} for a in self.atoms]}
    def to_json(self): return json.dumps(self.to_dict(),sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode()
    @property
    def sha256(self): return hashlib.sha256(self.to_json()).hexdigest()
    @property
    def atom_count(self): return len(self.atoms)
    @property
    def residue_count(self): return len({(a.chain,a.residue_number,a.residue) for a in self.atoms})
    @property
    def chain_count(self): return len({a.chain for a in self.atoms})
    @classmethod
    def from_json(cls,payload):
        def unique(pairs):
            out={}
            for k,v in pairs:
                if k in out: raise ValueError(f"duplicate JSON key: {k}")
                out[k]=v
            return out
        try: value=json.loads(payload.decode() if isinstance(payload,bytes) else payload,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc: raise ValueError(f"invalid structure JSON: {exc}") from exc
        fields={"schema","identifier","source_format","model_number","coordinate_unit","coordinate_system","atoms"}
        if not isinstance(value,dict) or set(value)!=fields or value["schema"]!=STRUCTURE_SCHEMA_ID: raise ValueError("structure JSON does not match exact v1 contract")
        af={"serial","name","residue","chain","residue_number","x","y","z","element"}
        if not isinstance(value["atoms"],list): raise ValueError("atoms must be an array")
        atoms=[]
        for item in value["atoms"]:
            if not isinstance(item,dict) or set(item)!=af: raise ValueError("atom fields do not match v1 contract")
            atoms.append(Atom(**item))
        return cls(value["identifier"],tuple(atoms),value["source_format"],value["model_number"],value["coordinate_unit"],value["coordinate_system"])

def ingest_structure(platform,structure,*,parents=(),budget=None):
    if not isinstance(structure,StructureDocument): raise TypeError("structure must be StructureDocument")
    return platform.ingest(structure.to_json(),media_type=STRUCTURE_MEDIA_TYPE,schema_id=STRUCTURE_SCHEMA_ID,metadata={"identifier":structure.identifier,"structure_sha256":structure.sha256,"atom_count":structure.atom_count,"residue_count":structure.residue_count,"chain_count":structure.chain_count,"coordinate_unit":structure.coordinate_unit,"coordinate_system":structure.coordinate_system},parents=parents,budget=budget)

def load_structure(platform,artifact_id,*,budget=None):
    budget=budget or Budget(); artifact=platform.store.get(artifact_id)
    if artifact.schema_id!=STRUCTURE_SCHEMA_ID or artifact.media_type!=STRUCTURE_MEDIA_TYPE: raise ValidationError("artifact is not a Structure v1 document")
    if artifact.size_bytes>budget.max_bytes: raise ResourceLimitError("structure artifact exceeds byte budget")
    doc=StructureDocument.from_json(b"".join(platform.store.read(artifact_id,budget=budget)))
    expected={"identifier":doc.identifier,"structure_sha256":doc.sha256,"atom_count":doc.atom_count,"residue_count":doc.residue_count,"chain_count":doc.chain_count,"coordinate_unit":doc.coordinate_unit,"coordinate_system":doc.coordinate_system}
    if doc.sha256!=artifact.digest or any(artifact.metadata.get(k)!=v for k,v in expected.items()): raise ValidationError("structure content or metadata failed integrity verification")
    return doc

def _geometry(doc):
    xyz=[(a.x,a.y,a.z) for a in doc.atoms]
    return {"atom_count":doc.atom_count,"residue_count":doc.residue_count,"chain_count":doc.chain_count,"bounding_box_angstrom":{"minimum":[min(p[i] for p in xyz) for i in range(3)],"maximum":[max(p[i] for p in xyz) for i in range(3)]},"coordinate_unit":"angstrom","coordinate_system":"cartesian_right_handed"}

def register_structure_service(platform):
    descriptions={"validate":"Integrity-check canonical Structure v1 artifact.","geometry":"Coordinate extents and structural counts.","contacts":"Distance-based inter-residue atom contact candidates.","sasa":"Approximate Shrake-Rupley solvent-accessible surface area.","interactions":"Distance-only interaction candidate screening.","rmsd":"Raw or superposed RMSD between caller-matched coordinate arrays."}
    for operation,capid in OPS.items():
        platform.register(Capability(id=capid,version="1.0.0",service="structure",operation=operation,input_schema=STRUCTURE_REFERENCE_SCHEMA_ID,output_schema=STRUCTURE_REPORT_SCHEMA_ID,deterministic=True,description=descriptions[operation]))
        def handler(inputs,parameters,context,selected=operation):
            n=2 if selected=="rmsd" else 1
            if len(inputs)!=n: raise ValidationError(f"structure.{selected} requires exactly {n} artifact ID(s)")
            ids=list(inputs.values())
            if any(not isinstance(x,str) for x in ids): raise ValidationError("structure artifact IDs must be strings")
            first=load_structure(platform,ids[0],budget=context.budget)
            if selected=="validate": result={"valid":True,**_geometry(first)}
            elif selected=="geometry": result=_geometry(first)
            elif selected=="contacts":
                if first.atom_count>5000: raise ResourceLimitError("contact screening is limited to 5000 atoms")
                cutoff=parameters.get("cutoff_angstrom",8.0)
                result={"contacts":[{"atom_index_1":i,"atom_index_2":j,"distance_angstrom":d} for i,j,d in contact_pairs(first.atoms,cutoff)],"cutoff_angstrom":cutoff}
            elif selected=="sasa": result=solvent_accessible_surface_area(first.atoms,probe_radius=parameters.get("probe_radius_angstrom",1.4),sphere_points=parameters.get("sphere_points",96))
            elif selected=="interactions": result=interaction_candidates(first.atoms,hydrogen_bond_range=tuple(parameters.get("hydrogen_bond_range",(2.5,3.5))),salt_bridge_cutoff=parameters.get("salt_bridge_cutoff_angstrom",4.0),disulfide_range=tuple(parameters.get("disulfide_range",(1.8,2.3))))
            else:
                second=load_structure(platform,ids[1],budget=context.budget)
                if first.atom_count!=second.atom_count: raise ValidationError("RMSD requires equal atom counts and caller-matched atom ordering")
                if parameters.get("expected_sha256") not in (None,second.sha256): raise ValidationError("second structure digest differs from expected_sha256")
                result={"rmsd_angstrom":rmsd(first.atoms,second.atoms,superpose=parameters.get("superpose",False)),"superposed":bool(parameters.get("superpose",False)),"atom_count":first.atom_count,"matching_policy":"caller-supplied atom order; no automatic atom mapping"}
            return {"schema":STRUCTURE_REPORT_SCHEMA_ID,"operation":selected,"structure_id":first.identifier,"structure_sha256":first.sha256,"result":result,"rulebook":STRUCTURE_RULEBOOK_ID,"rules_checked":[f"STR-{i:03d}" for i in range(1,8)],"limitations":["Geometry and interaction candidates are not chemical validation or energetic calculations.","SASA uses generic radii and deterministic finite surface sampling.","No missing atoms, alternate conformers, biological assemblies or symmetry are inferred.","RMSD requires caller-matched atom order and performs no atom correspondence."]}
        platform.bind(capid,handler)

def structure_rulebook(operation,artifact_key="structure_artifact_id",*,second_artifact_key="reference_structure_artifact_id",parameters=None):
    if operation not in OPS: raise ValueError(f"unsupported structure operation: {operation}")
    if not isinstance(artifact_key,str) or not artifact_key.strip(): raise ValueError("artifact_key must be non-empty text")
    keys=(artifact_key,second_artifact_key) if operation=="rmsd" else (artifact_key,)
    if operation=="rmsd" and (not isinstance(second_artifact_key,str) or not second_artifact_key.strip() or second_artifact_key==artifact_key): raise ValueError("RMSD requires distinct second artifact key")
    return Rulebook(id=STRUCTURE_RULEBOOK_ID,version="1.0.0",operations=(Operation(id=f"{operation}-structure",capability_id=OPS[operation],inputs=keys,output="structure_result",parameters=dict(parameters or {})),))
