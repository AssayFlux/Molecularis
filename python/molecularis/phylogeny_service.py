"""Phylogeny K: canonical aligned-sequence artifacts and bounded distance-tree workflows."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from typing import Any
from .phylo import bootstrap_neighbor_joining_from_alignment, jukes_cantor_distance, neighbor_joining, to_newick, upgma
from .platform import Budget, Capability, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

PHYLOGENY_SCHEMA_ID = "molecularis.phylogeny-alignment.v1"
PHYLOGENY_MEDIA_TYPE = "application/vnd.molecularis.phylogeny-alignment+json"
PHYLOGENY_REPORT_SCHEMA_ID = "molecularis.phylogeny-report.v1"
PHYLOGENY_RULEBOOK_ID = "phylogeny-core-v1"
_CAPS = {"validate":"phylogeny.validate.v1","distance_matrix":"phylogeny.distance-matrix.v1","neighbor_joining":"phylogeny.neighbor-joining.v1","upgma":"phylogeny.upgma.v1","bootstrap":"phylogeny.bootstrap-nj.v1"}
_RULES = {
 "validate":["PHY-001","PHY-002","PHY-003"],
 "distance_matrix":["PHY-001","PHY-002","PHY-003","PHY-004"],
 "neighbor_joining":["PHY-001","PHY-002","PHY-003","PHY-004","PHY-005"],
 "upgma":["PHY-001","PHY-002","PHY-003","PHY-004","PHY-006"],
 "bootstrap":["PHY-001","PHY-002","PHY-003","PHY-004","PHY-005","PHY-007"]}
_IUPAC=set("ACGTRYSWKMBDHVN-")
_MAX_TAXA=500
_MAX_SITES=2_000_000
_MAX_CELLS=5_000_000

@dataclass(frozen=True, slots=True)
class PhylogenyDocument:
    """Caller-aligned homologous nucleotide sequences; input order is preserved."""
    identifier: str
    taxon_ids: tuple[str,...]
    aligned_sequences: tuple[str,...]
    alignment_method: str = "caller-supplied"
    alphabet: str = "DNA_IUPAC"

    def __post_init__(self) -> None:
        if not isinstance(self.identifier,str) or not self.identifier.strip() or len(self.identifier)>256:
            raise ValueError("identifier must be non-empty text of at most 256 characters")
        if not isinstance(self.taxon_ids,tuple) or not 3<=len(self.taxon_ids)<=_MAX_TAXA:
            raise ValueError(f"taxon_ids must contain 3..{_MAX_TAXA} taxa")
        if any(not isinstance(x,str) or not x.strip() or len(x)>256 or any(ord(c)<32 for c in x) for x in self.taxon_ids):
            raise ValueError("taxon IDs must be bounded, non-empty text without control characters")
        if len(set(self.taxon_ids))!=len(self.taxon_ids):
            raise ValueError("taxon IDs must be unique")
        if not isinstance(self.aligned_sequences,tuple) or len(self.aligned_sequences)!=len(self.taxon_ids):
            raise ValueError("one aligned sequence is required for each taxon")
        if self.alphabet!="DNA_IUPAC":
            raise ValueError("v1 supports DNA_IUPAC only")
        if not isinstance(self.alignment_method,str) or not self.alignment_method.strip() or len(self.alignment_method)>256:
            raise ValueError("alignment_method must be bounded non-empty text")
        normalized=tuple("".join(seq.split()).upper() for seq in self.aligned_sequences if isinstance(seq,str))
        if len(normalized)!=len(self.aligned_sequences):
            raise TypeError("aligned sequences must be text")
        lengths={len(seq) for seq in normalized}
        if len(lengths)!=1 or not normalized[0] or len(normalized[0])>_MAX_SITES:
            raise ValueError(f"sequences must have equal alignment length in 1..{_MAX_SITES}")
        if len(self.taxon_ids)*len(normalized[0])>_MAX_CELLS:
            raise ValueError("alignment exceeds five million cells")
        for seq in normalized:
            invalid=set(seq)-_IUPAC
            if invalid: raise ValueError(f"unsupported nucleotide/gap symbols: {''.join(sorted(invalid))}")
            if set(seq)=={"-"}: raise ValueError("an all-gap sequence is not admissible")
        object.__setattr__(self,"aligned_sequences",normalized)

    @property
    def alignment_length(self)->int:
        return len(self.aligned_sequences[0])
    @property
    def sha256(self)->str:
        return hashlib.sha256(self.to_json()).hexdigest()
    def to_dict(self)->dict[str,Any]:
        return {"schema":PHYLOGENY_SCHEMA_ID,"identifier":self.identifier,"taxon_ids":list(self.taxon_ids),"aligned_sequences":list(self.aligned_sequences),"alignment_method":self.alignment_method,"alphabet":self.alphabet}
    def to_json(self)->bytes:
        return json.dumps(self.to_dict(),sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode("utf-8")
    @classmethod
    def from_json(cls,payload:bytes|str)->"PhylogenyDocument":
        def unique(pairs:list[tuple[str,Any]])->dict[str,Any]:
            result={}
            for key,value in pairs:
                if key in result: raise ValueError(f"duplicate JSON key: {key}")
                result[key]=value
            return result
        try:
            raw=payload.decode("utf-8") if isinstance(payload,bytes) else payload
            value=json.loads(raw,object_pairs_hook=unique,parse_constant=lambda item:(_ for _ in ()).throw(ValueError(item)))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc:
            raise ValueError(f"invalid phylogeny JSON: {exc}") from exc
        fields={"schema","identifier","taxon_ids","aligned_sequences","alignment_method","alphabet"}
        if not isinstance(value,dict) or set(value)!=fields or value["schema"]!=PHYLOGENY_SCHEMA_ID:
            raise ValueError("Phylogeny document fields/schema do not match v1")
        return cls(value["identifier"],tuple(value["taxon_ids"]),tuple(value["aligned_sequences"]),value["alignment_method"],value["alphabet"])

def ingest_phylogeny(platform:MolecularisPlatform,record:PhylogenyDocument,*,parents:tuple[str,...]=(),budget:Budget|None=None):
    if not isinstance(record,PhylogenyDocument): raise TypeError("record must be a PhylogenyDocument")
    return platform.ingest(record.to_json(),media_type=PHYLOGENY_MEDIA_TYPE,schema_id=PHYLOGENY_SCHEMA_ID,metadata={"identifier":record.identifier,"phylogeny_sha256":record.sha256,"taxon_count":len(record.taxon_ids),"alignment_length":record.alignment_length,"alignment_method":record.alignment_method},parents=parents,budget=budget)

def load_phylogeny(platform:MolecularisPlatform,artifact_id:str,*,budget:Budget|None=None)->PhylogenyDocument:
    budget=budget or Budget()
    artifact=platform.store.get(artifact_id)
    if artifact.media_type!=PHYLOGENY_MEDIA_TYPE or artifact.schema_id!=PHYLOGENY_SCHEMA_ID: raise ValidationError("artifact is not a Phylogeny alignment v1")
    if artifact.size_bytes>budget.max_bytes: raise ResourceLimitError("phylogeny artifact exceeds byte budget")
    record=PhylogenyDocument.from_json(b"".join(platform.store.read(artifact_id,budget=budget)))
    expected={"identifier":record.identifier,"phylogeny_sha256":record.sha256,"taxon_count":len(record.taxon_ids),"alignment_length":record.alignment_length,"alignment_method":record.alignment_method}
    if artifact.digest!=record.sha256 or any(artifact.metadata.get(k)!=v for k,v in expected.items()): raise ValidationError("phylogeny artifact integrity or metadata mismatch")
    if len(record.taxon_ids)*record.alignment_length>budget.max_candidates: raise ResourceLimitError("alignment exceeds candidate budget")
    return record

def _distance_matrix(record:PhylogenyDocument,minimum_sites:int)->tuple[list[list[float]],list[list[int]]]:
    n=len(record.taxon_ids); matrix=[[0.0]*n for _ in range(n)]; comparable=[[record.alignment_length]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            try: result=jukes_cantor_distance(record.aligned_sequences[i],record.aligned_sequences[j],minimum_sites=minimum_sites)
            except ValueError as exc: raise ValidationError(f"distance unavailable for {record.taxon_ids[i]} vs {record.taxon_ids[j]}: {exc}") from exc
            matrix[i][j]=matrix[j][i]=float(result["distance"])
            comparable[i][j]=comparable[j][i]=int(result["comparable_sites"])
    return matrix,comparable

def _execute(operation:str,record:PhylogenyDocument,parameters:dict[str,Any],max_replicates:int=1000)->dict[str,Any]:
    if operation=="validate":
        return {"valid":True,"taxon_count":len(record.taxon_ids),"alignment_length":record.alignment_length,"alignment_method":record.alignment_method,"alphabet":record.alphabet}
    minimum_sites=parameters.get("minimum_sites",20)
    if isinstance(minimum_sites,bool) or not isinstance(minimum_sites,int) or not 1<=minimum_sites<=record.alignment_length:
        raise ValidationError("minimum_sites must be an integer within alignment length")
    matrix,comparable=_distance_matrix(record,minimum_sites)
    if operation=="distance_matrix":
        return {"model":"Jukes-Cantor 1969","taxon_ids":list(record.taxon_ids),"distances":matrix,"comparable_sites":comparable,"missing_data":"pairwise deletion; only unambiguous A/C/G/T sites retained"}
    if operation=="neighbor_joining":
        tree=neighbor_joining(matrix,list(record.taxon_ids))
        return {"method":"neighbor joining","distance_model":"Jukes-Cantor 1969","rooting":"arbitrary computational root; NJ topology is unrooted","newick":to_newick(tree),"taxon_ids":list(record.taxon_ids)}
    if operation=="upgma":
        tree=upgma(matrix,list(record.taxon_ids))
        return {"method":"UPGMA","distance_model":"Jukes-Cantor 1969","rooting":"rooted by ultrametric assumption","newick":to_newick(tree),"taxon_ids":list(record.taxon_ids),"assumption":"UPGMA assumes approximately constant evolutionary rate"}
    if operation=="bootstrap":
        replicates=parameters.get("replicates",100); seed=parameters.get("seed",0)
        if isinstance(replicates,bool) or not isinstance(replicates,int) or not 1<=replicates<=max_replicates:
            raise ValidationError(f"replicates must be an integer between 1 and {max_replicates}")
        if isinstance(seed,bool) or not isinstance(seed,int): raise ValidationError("seed must be an integer")
        try:
            result=bootstrap_neighbor_joining_from_alignment(dict(zip(record.taxon_ids,record.aligned_sequences)),replicates=replicates,seed=seed,minimum_sites=minimum_sites)
        except ValueError as exc: raise ValidationError(str(exc)) from exc
        result["newick"]=to_newick(result.pop("tree"))
        return result
    raise ValidationError(f"unsupported phylogeny operation: {operation}")

def register_phylogeny_service(platform:MolecularisPlatform)->None:
    descriptions={"validate":"Validate canonical aligned nucleotide artifact and provenance metadata.","distance_matrix":"Calculate pairwise-deletion Jukes-Cantor nucleotide distances.","neighbor_joining":"Construct an unrooted neighbor-joining topology from Jukes-Cantor distances.","upgma":"Construct an ultrametric UPGMA tree from Jukes-Cantor distances.","bootstrap":"Estimate exploratory NJ split support by seeded alignment-site bootstrap."}
    for operation,capability_id in _CAPS.items():
        platform.register(Capability(id=capability_id,version="1.0.0",service="phylogeny",operation=operation,input_schema=PHYLOGENY_SCHEMA_ID,output_schema=PHYLOGENY_REPORT_SCHEMA_ID,deterministic=True,description=descriptions[operation]))
        def handler(inputs,parameters,context,selected=operation):
            if len(inputs)!=1 or not isinstance(next(iter(inputs.values())),str): raise ValidationError("Phylogeny operation requires exactly one alignment artifact ID")
            record=load_phylogeny(platform,next(iter(inputs.values())),budget=context.budget)
            max_replicates=min(1000,max(1,context.budget.max_candidates//max(1,record.alignment_length*len(record.taxon_ids))))
            result=_execute(selected,record,parameters,max_replicates=max_replicates)
            return {"schema":PHYLOGENY_REPORT_SCHEMA_ID,"operation":selected,"alignment_id":record.identifier,"alignment_sha256":record.sha256,"result":result,"rulebook":PHYLOGENY_RULEBOOK_ID,"rules_checked":list(_RULES[selected]),"limitations":["Input sequences must be pre-aligned homologous nucleotide sequences; alignment is not performed.","Jukes-Cantor assumes equal base frequencies and equal substitution rates; ambiguous/gap columns are pairwise-deleted.","Saturated or insufficient pairwise comparisons fail rather than being imputed.","Neighbor joining is distance-based and does not provide a biological root or likelihood support.","UPGMA assumes a molecular clock/ultrametric distances.","Bootstrap support is exploratory and failed replicates are excluded from its denominator.","No maximum-likelihood, Bayesian, codon, recombination, gene-tree/species-tree or calibrated dating inference is implemented."]}
        platform.bind(capability_id,handler)

def phylogeny_rulebook(operation:str,artifact_key:str="phylogeny_artifact_id",*,parameters:dict[str,Any]|None=None)->Rulebook:
    if operation not in _CAPS: raise ValueError(f"unsupported phylogeny operation: {operation}")
    if not isinstance(artifact_key,str) or not artifact_key.strip(): raise ValueError("artifact_key must be non-empty text")
    return Rulebook(id=PHYLOGENY_RULEBOOK_ID,version="1.0.0",operations=(Operation(id=f"{operation}-phylogeny",capability_id=_CAPS[operation],inputs=(artifact_key,),output="phylogeny_result",parameters=dict(parameters or {})),))
