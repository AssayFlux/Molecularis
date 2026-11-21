from __future__ import annotations
import hashlib,json,pytest
from molecularis.dna_rna_service import NucleicAcidDocument,dna_rna_rulebook,fold_rna_nussinov,ingest_nucleic_acid,load_nucleic_acid,primer_screen,register_dna_rna_service
from molecularis.platform import Budget,MolecularisPlatform
from molecularis.platform.contracts import ValidationError

def runtime(tmp_path):
    p=MolecularisPlatform(tmp_path/"store"); p.start(); register_dna_rna_service(p); return p

def test_canonical_document_and_hash():
    a=NucleicAcidDocument("rna"," aug cgu ","RNA","fixture"); b=NucleicAcidDocument("rna","AUGCGU","RNA","fixture")
    assert a.sequence=="AUGCGU" and a.to_json()==b.to_json()
    assert a.sha256==hashlib.sha256(a.to_json()).hexdigest() and NucleicAcidDocument.from_json(a.to_json())==a

@pytest.mark.parametrize("kind,seq",[("DNA","ACGU"),("RNA","ACTG"),("protein","ACGT"),("DNA","")])
def test_invalid_record(kind,seq):
    with pytest.raises((ValueError,TypeError)): NucleicAcidDocument("bad",seq,kind)

def test_json_rejects_duplicate_and_unknown_fields():
    raw=b'{"schema":"molecularis.dna-rna-record.v1","identifier":"x","identifier":"y","description":"","sequence_type":"DNA","sequence":"ACGT"}'
    with pytest.raises(ValueError,match="duplicate"): NucleicAcidDocument.from_json(raw)
    value={"schema":"molecularis.dna-rna-record.v1","identifier":"x","description":"","sequence_type":"DNA","sequence":"ACGT","x":1}
    with pytest.raises(ValueError,match="fields"): NucleicAcidDocument.from_json(json.dumps(value))

def test_artifact_roundtrip_and_integrity(tmp_path):
    p=runtime(tmp_path)
    try:
        rec=NucleicAcidDocument("dna","ATGC"); art=ingest_nucleic_acid(p,rec)
        assert load_nucleic_acid(p,art.artifact_id)==rec
        assert p.store.get(art.artifact_id).metadata["sequence_sha256"]==rec.sha256
        with pytest.raises(Exception,match="byte budget"): load_nucleic_acid(p,art.artifact_id,budget=Budget(max_bytes=1))
        other=p.ingest(b"{}",media_type="application/json",schema_id="other.v1")
        with pytest.raises(ValidationError,match="not a DNA/RNA"): load_nucleic_acid(p,other.artifact_id)
    finally: p.close()

@pytest.mark.parametrize("op,kind,seq,expected",[
("validate","DNA","ATGC",{"valid":True,"length":4}),("statistics","DNA","ATGC",{"gc_fraction":0.5,"gc_count":2}),
("reverse_complement","DNA","ATGC",{"sequence":"GCAT"}),("transcribe","DNA","ATGC",{"sequence":"AUGC"}),
("reverse_transcribe","RNA","AUGC",{"sequence":"ATGC"}),("translate","DNA","ATGGCTTAA",{"protein":"MA*"}),
("primer_screen","DNA","ATGCGTACGTAGCTAGCT",{"length":18}),("fold_rna","RNA","GGGAAACCC",{"dot_bracket":"(((...)))","pair_count":3})])
def test_rulebook_operations(tmp_path,op,kind,seq,expected):
    p=runtime(tmp_path)
    try:
        art=ingest_nucleic_acid(p,NucleicAcidDocument("fixture",seq,kind))
        report=p.execute(dna_rna_rulebook(op),{"dna_rna_artifact_id":art.artifact_id})["dna_rna_result"]
        assert report["operation"]==op and report["sequence_sha256"]==art.digest
        for key,val in expected.items(): assert report["result"][key]==val
        assert report["rules_checked"]==["DRNA-001","DRNA-002","DRNA-003","DRNA-004","DRNA-005","DRNA-006","DRNA-007"]
    finally: p.close()

def test_type_constraints_and_fold_limits(tmp_path):
    p=runtime(tmp_path)
    try:
        rna=ingest_nucleic_acid(p,NucleicAcidDocument("rna","AUGC","RNA"))
        with pytest.raises(ValidationError,match="requires DNA"): p.execute(dna_rna_rulebook("transcribe"),{"dna_rna_artifact_id":rna.artifact_id})
        dna=ingest_nucleic_acid(p,NucleicAcidDocument("dna","ATGC"))
        with pytest.raises(ValidationError,match="requires an RNA"): p.execute(dna_rna_rulebook("fold_rna"),{"dna_rna_artifact_id":dna.artifact_id})
        with pytest.raises(ValueError,match="fold limit"): fold_rna_nussinov("A"*21,max_length=20)
    finally: p.close()

def test_fold_determinism_and_ambiguity():
    assert fold_rna_nussinov("GGGAAACCC")==fold_rna_nussinov("GGGAAACCC")
    with pytest.raises(ValueError,match="Invalid symbols"): fold_rna_nussinov("GGNAAACCC")

def test_primer_screen_bounds():
    assert primer_screen("ATGCGTACGTAGCTAGCT")["length"]==18
    with pytest.raises(ValueError,match="15..40"): primer_screen("ATGC")
