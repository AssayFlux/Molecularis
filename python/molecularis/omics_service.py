"""Omics J: canonical matrix artifacts and bounded MSDE-backed analysis."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib, json, math
from typing import Any
from .omics import clr_transform, cpm, cross_omics_correlation, negative_binomial_differential_expression, shannon_diversity, simpson_diversity, welch_differential_expression
from .platform import Budget, Capability, ExecutionContext, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

OMICS_SCHEMA_ID = "molecularis.omics-matrix.v1"
OMICS_MEDIA_TYPE = "application/vnd.molecularis.omics-matrix+json"
OMICS_REPORT_SCHEMA_ID = "molecularis.omics-report.v1"
OMICS_RULEBOOK_ID = "omics-core-v1"
_CAPS = {"validate":"omics.validate.v1","normalize_cpm":"omics.normalize-cpm.v1","clr":"omics.clr-transform.v1","differential_welch":"omics.differential-welch.v1","differential_nb2":"omics.differential-nb2.v1","diversity":"omics.diversity.v1","correlate":"omics.cross-omics-correlation.v1"}
_RULES = tuple(f"OMI-{i:03d}" for i in range(1,10))

@dataclass(frozen=True, slots=True)
class OmicsDocument:
    """Feature-by-sample matrix; assay scale and units are caller-declared."""
    identifier: str
    feature_ids: tuple[str,...]
    sample_ids: tuple[str,...]
    values: tuple[tuple[float,...],...]
    assay_type: str = "raw_counts"
    value_unit: str = "count"

    def __post_init__(self):
        if not isinstance(self.identifier,str) or not self.identifier.strip() or len(self.identifier)>256:
            raise ValueError("identifier must contain 1..256 characters")
        if not isinstance(self.feature_ids,tuple) or not 1<=len(self.feature_ids)<=100000:
            raise ValueError("feature_ids must contain 1..100000 identifiers")
        if not isinstance(self.sample_ids,tuple) or not 2<=len(self.sample_ids)<=10000:
            raise ValueError("sample_ids must contain 2..10000 identifiers")
        for label, ids in (("feature",self.feature_ids),("sample",self.sample_ids)):
            if any(not isinstance(x,str) or not x.strip() or len(x)>256 for x in ids) or len(set(ids))!=len(ids):
                raise ValueError(f"{label} identifiers must be unique non-empty strings of at most 256 characters")
        if not isinstance(self.values,tuple) or len(self.values)!=len(self.feature_ids) or any(not isinstance(r,tuple) or len(r)!=len(self.sample_ids) for r in self.values):
            raise ValueError("values must be a rectangular feature-by-sample matrix")
        if len(self.feature_ids)*len(self.sample_ids)>2000000:
            raise ValueError("matrix exceeds 2,000,000-cell contract limit")
        if self.assay_type not in {"raw_counts","normalized","log_expression","abundance"}:
            raise ValueError("unsupported assay_type")
        for row in self.values:
            for value in row:
                if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0:
                    raise ValueError("matrix values must be finite and non-negative")
                if self.assay_type=="raw_counts" and not float(value).is_integer():
                    raise ValueError("raw_counts assay values must be integers")
        if not isinstance(self.value_unit,str) or not self.value_unit.strip() or len(self.value_unit)>64:
            raise ValueError("value_unit must be non-empty text of at most 64 characters")

    def to_dict(self):
        return {"schema":OMICS_SCHEMA_ID,"identifier":self.identifier,"feature_ids":list(self.feature_ids),"sample_ids":list(self.sample_ids),"values":[[float(x) for x in r] for r in self.values],"assay_type":self.assay_type,"value_unit":self.value_unit}
    def to_json(self):
        return json.dumps(self.to_dict(),sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode()
    @property
    def sha256(self):
        return hashlib.sha256(self.to_json()).hexdigest()
    @classmethod
    def from_json(cls,payload):
        def unique(pairs):
            result={}
            for k,v in pairs:
                if k in result: raise ValueError("duplicate JSON key: "+k)
                result[k]=v
            return result
        try:
            raw=payload.decode("utf-8") if isinstance(payload,bytes) else payload
            value=json.loads(raw,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc:
            raise ValueError(f"invalid Omics JSON: {exc}") from exc
        fields={"schema","identifier","feature_ids","sample_ids","values","assay_type","value_unit"}
        if not isinstance(value,dict) or set(value)!=fields or value["schema"]!=OMICS_SCHEMA_ID:
            raise ValueError("Omics document fields/schema do not match v1")
        return cls(value["identifier"],tuple(value["feature_ids"]),tuple(value["sample_ids"]),tuple(tuple(r) for r in value["values"]),value["assay_type"],value["value_unit"])

def ingest_omics(platform: MolecularisPlatform,record: OmicsDocument,*,parents=(),budget: Budget|None=None):
    if not isinstance(record,OmicsDocument): raise TypeError("record must be an OmicsDocument")
    return platform.ingest(record.to_json(),media_type=OMICS_MEDIA_TYPE,schema_id=OMICS_SCHEMA_ID,metadata={"identifier":record.identifier,"omics_sha256":record.sha256,"feature_count":len(record.feature_ids),"sample_count":len(record.sample_ids),"assay_type":record.assay_type,"value_unit":record.value_unit},parents=parents,budget=budget)

def load_omics(platform: MolecularisPlatform,artifact_id: str,*,budget: Budget|None=None)->OmicsDocument:
    budget=budget or Budget()
    artifact=platform.store.get(artifact_id)
    if artifact.media_type!=OMICS_MEDIA_TYPE or artifact.schema_id!=OMICS_SCHEMA_ID: raise ValidationError("artifact is not an Omics matrix v1")
    if artifact.size_bytes>budget.max_bytes: raise ResourceLimitError("Omics artifact exceeds byte budget")
    record=OmicsDocument.from_json(b"".join(platform.store.read(artifact_id,budget=budget)))
    expected={"identifier":record.identifier,"omics_sha256":record.sha256,"feature_count":len(record.feature_ids),"sample_count":len(record.sample_ids),"assay_type":record.assay_type,"value_unit":record.value_unit}
    if artifact.digest!=record.sha256 or any(artifact.metadata.get(k)!=v for k,v in expected.items()): raise ValidationError("Omics artifact integrity or metadata mismatch")
    if len(record.feature_ids)*len(record.sample_ids)>budget.max_candidates: raise ResourceLimitError("Omics matrix exceeds candidate budget")
    return record

def _safe(value: Any):
    if isinstance(value,float) and not math.isfinite(value): return None
    if isinstance(value,dict): return {k:_safe(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [_safe(v) for v in value]
    return value

def _execute(operation,record,params):
    matrix=[list(r) for r in record.values]
    if operation=="validate": return {"valid":True,"feature_count":len(record.feature_ids),"sample_count":len(record.sample_ids),"assay_type":record.assay_type}
    if operation=="normalize_cpm":
        if record.assay_type!="raw_counts": raise ValidationError("CPM requires raw_counts")
        return {"algorithm":"counts-per-million-v1","feature_ids":list(record.feature_ids),"sample_ids":list(record.sample_ids),"values":cpm(matrix),"value_unit":"CPM"}
    if operation=="clr":
        return {"algorithm":"centered-log-ratio-v1","feature_ids":list(record.feature_ids),"sample_ids":list(record.sample_ids),"values":clr_transform(matrix,pseudocount=params.get("pseudocount",0.5)),"value_unit":"log-ratio"}
    if operation=="differential_welch":
        if record.assay_type not in {"normalized","log_expression"}: raise ValidationError("Welch requires normalized or log_expression values")
        return {"method":"Welch unequal-variance t-test with Benjamini-Hochberg correction","results":welch_differential_expression(matrix,params["group_a"],params["group_b"],feature_ids=list(record.feature_ids)),"input_scale":record.assay_type}
    if operation=="differential_nb2":
        if record.assay_type!="raw_counts": raise ValidationError("NB2 requires raw_counts")
        return {"method":"exploratory NB2 log-link GLM with Wald tests and BH correction","results":negative_binomial_differential_expression(matrix,params["condition"],covariates=params.get("covariates"),feature_ids=list(record.feature_ids))}
    if operation=="diversity":
        if record.assay_type not in {"raw_counts","abundance"}: raise ValidationError("diversity requires raw_counts or abundance")
        return {"method":"Shannon entropy and Gini-Simpson diversity","samples":[{"sample_id":s,"shannon":shannon_diversity([r[j] for r in matrix]),"simpson":simpson_diversity([r[j] for r in matrix]),"observed_features":sum(r[j]>0 for r in matrix),"total_abundance":sum(r[j] for r in matrix)} for j,s in enumerate(record.sample_ids)]}
    raise ValidationError("unsupported Omics operation: "+operation)

def register_omics_service(platform: MolecularisPlatform):
    descriptions={"validate":"Validate canonical feature-by-sample matrix artifact","normalize_cpm":"Normalize raw counts to counts per million","clr":"Centered-log-ratio compositional transform","differential_welch":"Exploratory Welch differential analysis with BH correction","differential_nb2":"Exploratory NB2 GLM differential analysis","diversity":"Per-sample Shannon and Gini-Simpson diversity","correlate":"Cross-omics Pearson feature correlation"}
    for operation,capability_id in _CAPS.items():
        platform.register(Capability(id=capability_id,version="1.0.0",service="omics",operation=operation,input_schema=OMICS_SCHEMA_ID,output_schema=OMICS_REPORT_SCHEMA_ID,deterministic=True,description=descriptions[operation]))
        def handler(inputs,parameters,context,selected=operation):
            required=2 if selected=="correlate" else 1
            if len(inputs)!=required or any(not isinstance(v,str) for v in inputs.values()): raise ValidationError(f"{selected} requires {required} Omics artifact reference(s)")
            ids=list(inputs.values()); first=load_omics(platform,ids[0],budget=context.budget)
            if selected=="correlate":
                second=load_omics(platform,ids[1],budget=context.budget)
                if first.sample_ids!=second.sample_ids: raise ValidationError("cross-omics matrices require identical ordered sample IDs")
                result={"method":"Pearson feature correlation","feature_ids_a":list(first.feature_ids),"feature_ids_b":list(second.feature_ids),"correlations":cross_omics_correlation([list(r) for r in first.values],[list(r) for r in second.values])}
            else: result=_execute(selected,first,parameters)
            return {"schema":OMICS_REPORT_SCHEMA_ID,"operation":selected,"matrix_id":first.identifier,"matrix_sha256":first.sha256,"result":_safe(result),"rulebook":OMICS_RULEBOOK_ID,"rules_checked":list(_RULES),"limitations":["Caller-provided units, normalization and study design are not inferred","Differential tests are exploratory and do not model repeated measures or latent batch effects","NB2 uses unmoderated moment dispersions and asymptotic Wald p-values","No causal, clinical, diagnostic or biological-function inference is provided"]}
        platform.bind(capability_id,handler)

def omics_rulebook(operation,artifact_key="omics_artifact_id",*,second_artifact_key="second_omics_artifact_id",parameters=None):
    if operation not in _CAPS: raise ValueError("unsupported Omics operation: "+operation)
    if not isinstance(artifact_key,str) or not artifact_key.strip(): raise ValueError("artifact_key must be non-empty text")
    keys=(artifact_key,second_artifact_key) if operation=="correlate" else (artifact_key,)
    if len(keys)==2 and (not isinstance(second_artifact_key,str) or not second_artifact_key.strip() or second_artifact_key==artifact_key): raise ValueError("cross-omics correlation requires distinct artifact keys")
    return Rulebook(id=OMICS_RULEBOOK_ID,version="1.0.0",operations=(Operation(id=f"{operation}-omics",capability_id=_CAPS[operation],inputs=keys,output="omics_result",parameters=dict(parameters or {})),))
