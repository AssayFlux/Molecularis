"""Protein service E: canonical protein artifacts and bounded analysis capabilities."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from typing import Any
from .protein import protein_descriptors
from .protein_motifs import MotifPack, scan_protein_motif_pack
from .protein_design import validate_protein_design_brief
from .sequence import PROTEIN, validate_sequence
from .platform import Budget, Capability, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

PROTEIN_SCHEMA_ID="molecularis.protein-record.v1"
PROTEIN_REF_SCHEMA_ID="molecularis.protein-artifact-reference.v1"
PROTEIN_REPORT_SCHEMA_ID="molecularis.protein-operation-report.v1"
PROTEIN_MEDIA_TYPE="application/vnd.molecularis.protein+json"
PROTEIN_RULEBOOK_ID="protein-core-v1"
OPS={"validate":"protein.validate.v1","descriptors":"protein.descriptors.v1","motif_scan":"protein.motif-scan.v1","design_brief":"protein.design-brief.v1"}
_CANONICAL=frozenset("ACDEFGHIKLMNPQRSTVWY")

@dataclass(frozen=True,slots=True)
class ProteinDocument:
    identifier:str
    sequence:str
    description:str=""
    def __post_init__(self):
        if not isinstance(self.identifier,str) or not self.identifier.strip() or len(self.identifier)>256 or any(ord(c)<32 for c in self.identifier): raise ValueError("identifier must be bounded non-empty text")
        if not isinstance(self.description,str) or len(self.description)>2048 or any(ord(c)<32 and c not in "\t\n\r" for c in self.description): raise ValueError("description must be bounded text")
        if not isinstance(self.sequence,str): raise TypeError("sequence must be text")
        seq="".join(self.sequence.split()).upper()
        if not seq or len(seq)>5_000_000: raise ValueError("protein sequence must contain 1..5000000 residues")
        validate_sequence(seq,PROTEIN)
        if set(seq)-_CANONICAL: raise ValueError("Protein v1 artifacts require canonical 20 amino acids; ambiguous and rare residues are not accepted")
        object.__setattr__(self,"sequence",seq)
    def to_dict(self): return {"schema":PROTEIN_SCHEMA_ID,"identifier":self.identifier,"description":self.description,"sequence":self.sequence}
    def to_json(self): return json.dumps(self.to_dict(),sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False).encode("utf-8")
    @property
    def sha256(self): return hashlib.sha256(self.to_json()).hexdigest()
    @classmethod
    def from_json(cls,payload):
        def unique(pairs):
            out={}
            for k,v in pairs:
                if k in out: raise ValueError(f"duplicate JSON key: {k}")
                out[k]=v
            return out
        try: value=json.loads(payload.decode("utf-8") if isinstance(payload,bytes) else payload,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc: raise ValueError(f"invalid Protein JSON: {exc}") from exc
        if not isinstance(value,dict) or set(value)!={"schema","identifier","description","sequence"} or value["schema"]!=PROTEIN_SCHEMA_ID: raise ValueError("Protein document does not match exact v1 contract")
        return cls(value["identifier"],value["sequence"],value["description"])

def ingest_protein(platform,protein:ProteinDocument,*,parents=(),budget=None):
    if not isinstance(protein,ProteinDocument): raise TypeError("protein must be ProteinDocument")
    return platform.ingest(protein.to_json(),media_type=PROTEIN_MEDIA_TYPE,schema_id=PROTEIN_SCHEMA_ID,metadata={"identifier":protein.identifier,"protein_sha256":protein.sha256,"length":len(protein.sequence),"sequence_sha256":hashlib.sha256(protein.sequence.encode("ascii")).hexdigest()},parents=parents,budget=budget)

def load_protein(platform,artifact_id:str,*,budget:Budget|None=None):
    budget=budget or Budget(); artifact=platform.store.get(artifact_id)
    if artifact.media_type!=PROTEIN_MEDIA_TYPE or artifact.schema_id!=PROTEIN_SCHEMA_ID: raise ValidationError("artifact is not a Protein v1 document")
    if artifact.size_bytes>budget.max_bytes: raise ResourceLimitError("protein artifact exceeds byte budget")
    doc=ProteinDocument.from_json(b"".join(platform.store.read(artifact_id,budget=budget)))
    expected={"identifier":doc.identifier,"protein_sha256":doc.sha256,"length":len(doc.sequence),"sequence_sha256":hashlib.sha256(doc.sequence.encode("ascii")).hexdigest()}
    if artifact.digest!=doc.sha256 or any(artifact.metadata.get(k)!=v for k,v in expected.items()): raise ValidationError("Protein content or metadata failed integrity verification")
    return doc

def register_protein_service(platform):
    descriptions={"validate":"Validate and integrity-check a canonical protein sequence artifact.","descriptors":"Calculate explicit unmodified linear-peptide descriptors.","motif_scan":"Scan a protein against a hash-pinned caller-supplied motif pack.","design_brief":"Validate a non-generative research brief and report release gates."}
    for operation,capid in OPS.items():
        platform.register(Capability(id=capid,version="1.0.0",service="protein",operation=operation,input_schema=PROTEIN_REF_SCHEMA_ID,output_schema=PROTEIN_REPORT_SCHEMA_ID,deterministic=True,description=descriptions[operation]))
        def handler(inputs,parameters,context,selected=operation):
            if len(inputs)!=1 or not isinstance(next(iter(inputs.values())),str): raise ValidationError("Protein operation requires exactly one protein artifact ID")
            doc=load_protein(platform,next(iter(inputs.values())),budget=context.budget)
            if selected=="validate": result={"valid":True,"length":len(doc.sequence),"alphabet":"canonical_20"}
            elif selected=="descriptors": result=protein_descriptors(doc.sequence)
            elif selected=="motif_scan":
                try:
                    raw=parameters["motif_pack_json"].encode("utf-8")
                    meta=parameters["motif_pack"]
                    pack=MotifPack(meta["name"],meta["version"],meta["license"],meta["source"],meta["content_sha256"])
                except (KeyError,TypeError,AttributeError) as exc: raise ValidationError("motif_scan requires motif_pack_json and complete motif_pack metadata") from exc
                if len(raw)>2*1024*1024: raise ResourceLimitError("motif pack exceeds 2 MiB")
                result=scan_protein_motif_pack(doc.sequence,raw,motif_pack=pack)
            else:
                try: brief=parameters["brief"]
                except KeyError as exc: raise ValidationError("design_brief requires a brief parameter") from exc
                result=validate_protein_design_brief(brief)
            return {"schema":PROTEIN_REPORT_SCHEMA_ID,"operation":selected,"protein_id":doc.identifier,"protein_sha256":doc.sha256,"result":result,"rulebook":PROTEIN_RULEBOOK_ID,"rules_checked":[f"PRO-{i:03d}" for i in range(1,7)],"limitations":["Sequence descriptors assume an unmodified linear peptide with average residue masses and free termini.","Motif matches do not establish family, function, activity or novelty.","Design-brief validation does not generate or rank sequences and is not a biosafety assessment.","ESM embeddings and HMMER domain evidence remain separate optional local workflows; no weights or databases are downloaded."]}
        platform.bind(capid,handler)

def protein_rulebook(operation:str,artifact_key:str="protein_artifact_id",*,parameters=None)->Rulebook:
    if operation not in OPS: raise ValueError("unsupported Protein operation: "+operation)
    if not isinstance(artifact_key,str) or not artifact_key.strip(): raise ValueError("artifact_key must be non-empty text")
    return Rulebook(id=PROTEIN_RULEBOOK_ID,version="1.0.0",operations=(Operation(id=f"{operation}-protein",capability_id=OPS[operation],inputs=(artifact_key,),output="protein_result",parameters=dict(parameters or {})),))
