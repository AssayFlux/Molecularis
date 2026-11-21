from __future__ import annotations
import pytest
from molecularis.omics_service import OmicsDocument,ingest_omics,load_omics,omics_rulebook,register_omics_service
from molecularis.platform import Budget,MolecularisPlatform

def runtime(tmp_path):
    p=MolecularisPlatform(tmp_path/"store"); p.start(); register_omics_service(p); return p

def counts():
    return OmicsDocument("counts",("g1","g2","g3"),("s1","s2","s3","s4","s5","s6"),((10,12,11,30,32,31),(50,48,52,49,51,50),(5,7,6,8,9,7)))

def test_document_roundtrip_digest_artifact_lifecycle(tmp_path):
    p=runtime(tmp_path)
    try:
        doc=counts(); a=ingest_omics(p,doc)
        assert load_omics(p,a.artifact_id)==doc
        assert OmicsDocument.from_json(doc.to_json()).sha256==doc.sha256
    finally: p.close()

@pytest.mark.parametrize("op",["validate","normalize_cpm","clr","differential_nb2","diversity"])
def test_single_artifact_operations(tmp_path,op):
    p=runtime(tmp_path)
    try:
        doc=counts(); a=ingest_omics(p,doc)
        params={"condition":[0,0,0,1,1,1]} if op=="differential_nb2" else {}
        out=p.execute(omics_rulebook(op,parameters=params),{"omics_artifact_id":a.artifact_id})["omics_result"]
        assert out["operation"]==op and out["matrix_sha256"]==doc.sha256
        assert out["rules_checked"]==[f"OMI-{i:03d}" for i in range(1,10)]
    finally: p.close()

def test_welch_and_cross_omics_correlation(tmp_path):
    p=runtime(tmp_path)
    try:
        expr=OmicsDocument("expression",("g1","g2"),("a1","a2","a3","b1","b2","b3"),((1.,1.1,.9,3.,3.1,2.9),(2.,2.1,1.9,2.,2.1,1.9)),assay_type="log_expression",value_unit="log2")
        a=ingest_omics(p,expr)
        out=p.execute(omics_rulebook("differential_welch",parameters={"group_a":[0,1,2],"group_b":[3,4,5]}),{"omics_artifact_id":a.artifact_id})["omics_result"]
        assert out["result"]["results"][0]["difference"]<0
        b=ingest_omics(p,OmicsDocument("second",("h1",),expr.sample_ids,((3.,2.,1.,6.,5.,4.),),assay_type="normalized"))
        corr=p.execute(omics_rulebook("correlate"),{"omics_artifact_id":a.artifact_id,"second_omics_artifact_id":b.artifact_id})["omics_result"]
        assert corr["result"]["correlations"][0][0]>0
    finally: p.close()

def test_rejects_duplicate_nonfinite_fractional_counts_and_bad_design():
    with pytest.raises(ValueError,match="duplicate JSON key"): OmicsDocument.from_json(b'{"schema":"x","schema":"y"}')
    with pytest.raises(ValueError,match="integers"): OmicsDocument("bad",("g",),("s1","s2"),((1.5,2),))
    with pytest.raises(ValueError,match="finite"): OmicsDocument("bad",("g",),("s1","s2"),((1,float("nan")),))

def test_scale_guards_budget_and_rulebook_validation(tmp_path):
    p=runtime(tmp_path)
    try:
        a=ingest_omics(p,counts())
        with pytest.raises(Exception): load_omics(p,a.artifact_id,budget=Budget(max_candidates=2))
        with pytest.raises(ValueError,match="unsupported"): omics_rulebook("p-hacking")
        with pytest.raises(ValueError,match="distinct"): omics_rulebook("correlate",second_artifact_key="omics_artifact_id")
        expr=OmicsDocument("log",("g",),("s1","s2"),((1.,2.),),assay_type="log_expression")
        e=ingest_omics(p,expr)
        with pytest.raises(Exception): p.execute(omics_rulebook("normalize_cpm"),{"omics_artifact_id":e.artifact_id})
    finally: p.close()
