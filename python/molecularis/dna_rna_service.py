"""DNA/RNA service G: canonical nucleic-acid artifacts and bounded native operations."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, json
from typing import Any
from .genetic_code import translate_coding_sequence
from .platform import Artifact, Budget, Capability, ExecutionContext, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError
from .sequence import DNA, RNA, reverse_complement, transcribe, validate_sequence

DNA_RNA_SCHEMA_ID="molecularis.dna-rna-record.v1"
DNA_RNA_REFERENCE_SCHEMA_ID="molecularis.dna-rna-artifact-reference.v1"
DNA_RNA_REPORT_SCHEMA_ID="molecularis.dna-rna-operation-report.v1"
DNA_RNA_MEDIA_TYPE="application/vnd.molecularis.dna-rna+json"
DNA_RNA_RULEBOOK_ID="dna-rna-core-v1"
_ALPHABETS={"DNA":DNA,"RNA":RNA}
_OPERATIONS={"validate":"dna-rna.validate.v1","statistics":"dna-rna.statistics.v1",
"reverse_complement":"dna-rna.reverse-complement.v1","transcribe":"dna-rna.transcribe.v1",
"reverse_transcribe":"dna-rna.reverse-transcribe.v1","translate":"dna-rna.translate.v1",
"primer_screen":"dna-rna.primer-screen.v1","fold_rna":"dna-rna.rna-secondary-fold.v1"}
_RULES=["DRNA-001","DRNA-002","DRNA-003","DRNA-004","DRNA-005","DRNA-006","DRNA-007"]

@dataclass(frozen=True,slots=True)
class NucleicAcidDocument:
    """Immutable canonical single-strand DNA or RNA record."""
    identifier:str
    sequence:str
    sequence_type:str="DNA"
    description:str=""
    def __post_init__(self)->None:
        for name,value in (("identifier",self.identifier),("description",self.description)):
            if not isinstance(value,str): raise TypeError(f"{name} must be text")
        if not self.identifier.strip() or len(self.identifier)>256: raise ValueError("identifier must contain 1..256 characters")
        if any(ord(c)<32 for c in self.identifier+self.description): raise ValueError("metadata must not contain control characters")
        if not isinstance(self.sequence,str): raise TypeError("sequence must be text")
        if self.sequence_type not in _ALPHABETS: raise ValueError("sequence_type must be DNA or RNA")
        seq="".join(self.sequence.split()).upper()
        if not seq: raise ValueError("sequence must not be empty")
        validate_sequence(seq,_ALPHABETS[self.sequence_type])
        object.__setattr__(self,"sequence",seq)
    def to_dict(self)->dict[str,Any]:
        return {"schema":DNA_RNA_SCHEMA_ID,"identifier":self.identifier,"description":self.description,"sequence_type":self.sequence_type,"sequence":self.sequence}
    def to_json(self)->bytes:
        return json.dumps(self.to_dict(),sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode()
    @property
    def sha256(self)->str: return hashlib.sha256(self.to_json()).hexdigest()
    @classmethod
    def from_json(cls,payload:bytes|str)->"NucleicAcidDocument":
        def unique(pairs:list[tuple[str,Any]])->dict[str,Any]:
            out={}
            for k,v in pairs:
                if k in out: raise ValueError(f"duplicate JSON key: {k}")
                out[k]=v
            return out
        try:
            raw=payload.decode("utf-8") if isinstance(payload,bytes) else payload
            value=json.loads(raw,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc: raise ValueError(f"invalid DNA/RNA JSON: {exc}") from exc
        if not isinstance(value,dict) or set(value)!={"schema","identifier","description","sequence_type","sequence"}: raise ValueError("DNA/RNA document fields do not match v1 contract")
        if value["schema"]!=DNA_RNA_SCHEMA_ID: raise ValueError("unsupported DNA/RNA schema")
        return cls(value["identifier"],value["sequence"],value["sequence_type"],value["description"])

def ingest_nucleic_acid(platform:MolecularisPlatform,record:NucleicAcidDocument,*,parents:tuple[str,...]=(),budget:Budget|None=None)->Artifact:
    if not isinstance(record,NucleicAcidDocument): raise TypeError("record must be a validated NucleicAcidDocument")
    return platform.ingest(record.to_json(),media_type=DNA_RNA_MEDIA_TYPE,schema_id=DNA_RNA_SCHEMA_ID,
      metadata={"identifier":record.identifier,"sequence_type":record.sequence_type,"length":len(record.sequence),"sequence_sha256":record.sha256},parents=parents,budget=budget)

def load_nucleic_acid(platform:MolecularisPlatform,artifact_id:str,*,budget:Budget|None=None)->NucleicAcidDocument:
    budget=budget or Budget(); artifact=platform.store.get(artifact_id)
    if artifact.media_type!=DNA_RNA_MEDIA_TYPE or artifact.schema_id!=DNA_RNA_SCHEMA_ID: raise ValidationError("artifact is not a DNA/RNA v1 document")
    if artifact.size_bytes>budget.max_bytes: raise ResourceLimitError("DNA/RNA artifact exceeds byte budget")
    record=NucleicAcidDocument.from_json(b"".join(platform.store.read(artifact_id,budget=budget)))
    expected={"identifier":record.identifier,"sequence_type":record.sequence_type,"length":len(record.sequence),"sequence_sha256":record.sha256}
    if record.sha256!=artifact.digest or any(artifact.metadata.get(k)!=v for k,v in expected.items()): raise ValidationError("DNA/RNA content or metadata failed integrity verification")
    return record

def primer_screen(sequence:str)->dict[str,Any]:
    """Wallace-rule oligo screen; not a nearest-neighbour Tm model."""
    seq="".join(sequence.split()).upper(); validate_sequence(seq,set("ACGT"))
    if not 15<=len(seq)<=40: raise ValueError("primer screen supports 15..40 nt")
    gc=seq.count("G")+seq.count("C"); tm=2*(seq.count("A")+seq.count("T"))+4*gc
    return {"length":len(seq),"gc_fraction":gc/len(seq),"wallace_tm_c":tm,"gc_clamp":seq[-1] in "GC",
      "screening_flags":not(0.35<=gc/len(seq)<=0.65 and 45<=tm<=75),
      "limitations":["Wallace estimate only","No salt/Mg2+/concentration correction","No thermodynamic hairpin or primer-dimer model","Not primer-pair specificity or wet-lab validation"]}

def fold_rna_nussinov(sequence:str,*,max_length:int=300,min_loop:int=3)->dict[str,Any]:
    """Maximum-cardinality non-crossing AU/GC/GU RNA pairing using Nussinov DP."""
    seq="".join(sequence.split()).upper().replace("T","U"); validate_sequence(seq,set("ACGU")); n=len(seq)
    if not n: raise ValueError("RNA sequence must not be empty")
    if isinstance(max_length,bool) or not isinstance(max_length,int) or max_length<1: raise ValueError("max_length must be positive")
    if n>max_length: raise ValueError(f"RNA length {n} exceeds fold limit {max_length}")
    if isinstance(min_loop,bool) or not isinstance(min_loop,int) or min_loop<0: raise ValueError("min_loop must be non-negative")
    allowed={("A","U"),("U","A"),("G","C"),("C","G"),("G","U"),("U","G")}
    dp=[[0]*n for _ in range(n)]; trace=[[None]*n for _ in range(n)]
    for span in range(1,n):
        for i in range(n-span):
            j=i+span; best=dp[i][j-1]; choice=("right",)
            if dp[i+1][j]>best: best,choice=dp[i+1][j],("left",)
            if j-i>min_loop and (seq[i],seq[j]) in allowed and dp[i+1][j-1]+1>best: best,choice=dp[i+1][j-1]+1,("pair",)
            for k in range(i+1,j):
                score=dp[i][k]+dp[k+1][j]
                if score>best: best,choice=score,("split",k)
            dp[i][j],trace[i][j]=best,choice
    pairs=[]; stack=[(0,n-1)] if n>1 else []
    while stack:
        i,j=stack.pop()
        if i>=j: continue
        choice=trace[i][j]
        if choice is None: continue
        if choice[0]=="right": stack.append((i,j-1))
        elif choice[0]=="left": stack.append((i+1,j))
        elif choice[0]=="pair": pairs.append((i,j)); stack.append((i+1,j-1))
        else:
            k=choice[1]; stack.extend(((k+1,j),(i,k)))
    pairs.sort(); structure=["."]*n
    for i,j in pairs: structure[i],structure[j]="(",")"
    return {"algorithm":"nussinov_maximum_pair_count_v1","sequence":seq,"dot_bracket":"".join(structure),
      "pairs":[{"i":i,"j":j,"bases":seq[i]+seq[j]} for i,j in pairs],"pair_count":len(pairs),"length":n,
      "limitations":["Maximum pair count, not minimum free energy","No loop thermodynamics, ionic conditions or ligand effects","No pseudoknots or tertiary structure; not experimental prediction"]}

def _execute(op:str,record:NucleicAcidDocument,p:dict[str,Any],budget:Budget)->dict[str,Any]:
    seq,kind=record.sequence,record.sequence_type
    if op=="validate": return {"valid":True,"sequence_type":kind,"length":len(seq)}
    if op=="statistics":
        gc=seq.count("G")+seq.count("C"); canonical=set(seq)<=set("ACGT" if kind=="DNA" else "ACGU")
        return {"length":len(seq),"gc_fraction":gc/len(seq),"gc_count":gc,"a":seq.count("A"),"c":seq.count("C"),"g":seq.count("G"),"t":seq.count("T"),"u":seq.count("U"),"ambiguous_count":0 if canonical else sum(c not in "ACGTU" for c in seq)}
    if op=="reverse_complement":
        if kind!="DNA": raise ValidationError("reverse_complement requires DNA")
        return {"sequence":reverse_complement(seq),"sequence_type":"DNA"}
    if op=="transcribe":
        if kind!="DNA": raise ValidationError("transcribe requires DNA")
        return {"sequence":transcribe(seq),"sequence_type":"RNA","strand_convention":"input DNA is coding/sense strand"}
    if op=="reverse_transcribe":
        if kind!="RNA": raise ValidationError("reverse_transcribe requires RNA")
        return {"sequence":seq.replace("U","T"),"sequence_type":"DNA","strand_convention":"corresponding coding/sense DNA orientation"}
    if op=="translate":
        if len(seq)>budget.max_candidates*3: raise ResourceLimitError("translation exceeds candidate budget")
        return translate_coding_sequence(seq,table_id=p.get("table_id",1),frame=p.get("frame",0),cds=p.get("cds",False),trim_partial_codon=p.get("trim_partial_codon",False))
    if op=="primer_screen": return primer_screen(seq)
    if op=="fold_rna":
        if kind!="RNA": raise ValidationError("fold_rna requires an RNA artifact")
        return fold_rna_nussinov(seq,max_length=min(300,budget.max_candidates),min_loop=p.get("min_loop",3))
    raise ValidationError(f"unsupported DNA/RNA operation: {op}")

def register_dna_rna_service(platform:MolecularisPlatform)->None:
    descriptions={"validate":"Validate canonical DNA/RNA artifact","statistics":"Nucleotide composition and GC fraction",
      "reverse_complement":"IUPAC DNA reverse complement","transcribe":"Coding/sense DNA transcription",
      "reverse_transcribe":"RNA-to-DNA alphabet conversion","translate":"Explicit NCBI table translation",
      "primer_screen":"Bounded Wallace-rule DNA oligo screen","fold_rna":"Nussinov maximum-pair RNA secondary candidate"}
    for op,cap_id in _OPERATIONS.items():
        platform.register(Capability(id=cap_id,version="1.0.0",service="dna-rna",operation=op,
          input_schema=DNA_RNA_REFERENCE_SCHEMA_ID,output_schema=DNA_RNA_REPORT_SCHEMA_ID,deterministic=True,description=descriptions[op]))
        def handler(inputs:dict[str,Any],parameters:dict[str,Any],context:ExecutionContext,selected:str=op)->dict[str,Any]:
            if len(inputs)!=1: raise ValidationError("DNA/RNA operation requires exactly one artifact ID")
            artifact_id=next(iter(inputs.values()))
            if not isinstance(artifact_id,str): raise ValidationError("DNA/RNA artifact ID must be text")
            record=load_nucleic_acid(platform,artifact_id,budget=context.budget)
            return {"schema":DNA_RNA_REPORT_SCHEMA_ID,"operation":selected,"sequence_id":record.identifier,
              "sequence_sha256":record.sha256,"result":_execute(selected,record,parameters,context.budget),
              "rulebook":DNA_RNA_RULEBOOK_ID,"rules_checked":_RULES,
              "limitations":["Computational screening does not establish biological function","NUPACK/NUAD are not invoked; optional adapters require explicit local installation","No wet-lab suitability, safety or experimental validation is claimed"]}
        platform.bind(cap_id,handler)

def dna_rna_rulebook(operation:str,artifact_key:str="dna_rna_artifact_id",*,parameters:dict[str,Any]|None=None)->Rulebook:
    if operation not in _OPERATIONS: raise ValueError(f"unsupported DNA/RNA operation: {operation}")
    if not isinstance(artifact_key,str) or not artifact_key.strip(): raise ValueError("artifact_key must be non-empty text")
    return Rulebook(id=DNA_RNA_RULEBOOK_ID,version="1.0.0",operations=(Operation(id=f"{operation}-dna-rna",capability_id=_OPERATIONS[operation],inputs=(artifact_key,),output="dna_rna_result",parameters=dict(parameters or {})),))
