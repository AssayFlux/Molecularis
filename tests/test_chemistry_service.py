from __future__ import annotations
import pytest
from molecularis.chemistry_service import ChemistryDocument, ingest_chemistry, load_chemistry, register_chemistry_service, chemistry_rulebook
from molecularis.platform import MolecularisPlatform
from molecularis.platform.contracts import ValidationError

def sdf():
    counts=f"{2:3d}{1:3d}  0  0  0  0            999 V2000"
    a=f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    b=f"{1.5:10.4f}{0.0:10.4f}{0.0:10.4f} {'O':>3s}"
    bond=f"{1:3d}{2:3d}{1:3d}"
    return "\n".join(["ethanol-fragment","Molecularis","",counts,a,b,bond,"M  END"])

def runtime(tmp_path):
    p=MolecularisPlatform(tmp_path/"store"); p.start(); register_chemistry_service(p); return p

def test_chemistry_document_roundtrip_and_integrity(tmp_path):
    p=runtime(tmp_path)
    try:
        doc=ChemistryDocument.from_sdf("ethanol-fragment",sdf()); artifact=ingest_chemistry(p,doc)
        assert load_chemistry(p,artifact.artifact_id)==doc
        assert ChemistryDocument.from_json(doc.to_json()).sha256==doc.sha256
    finally: p.close()

@pytest.mark.parametrize("op",["validate","descriptors","fingerprint"])
def test_single_artifact_capabilities(tmp_path,op):
    p=runtime(tmp_path)
    try:
        doc=ChemistryDocument.from_sdf("molecule",sdf()); art=ingest_chemistry(p,doc)
        out=p.execute(chemistry_rulebook(op,parameters={"max_path":2}),{"chemistry_artifact_id":art.artifact_id})["chemistry_result"]
        assert out["operation"]==op and out["molecule_sha256"]==doc.sha256
        assert out["rules_checked"]==[f"CHM-{i:03d}" for i in range(1,7)]
    finally: p.close()

@pytest.mark.parametrize("op",["substructure","similarity"])
def test_two_artifact_capabilities(tmp_path,op):
    p=runtime(tmp_path)
    try:
        doc=ChemistryDocument.from_sdf("one",sdf())
        a=ingest_chemistry(p,doc); b=ingest_chemistry(p,ChemistryDocument.from_sdf("two",sdf()))
        out=p.execute(chemistry_rulebook(op),{"chemistry_artifact_id":a.artifact_id,"query_chemistry_artifact_id":b.artifact_id})["chemistry_result"]
        assert out["operation"]==op
    finally: p.close()

def test_contract_rejects_duplicate_keys_and_wrong_schema():
    with pytest.raises(ValueError,match="duplicate JSON key"):
        ChemistryDocument.from_json(b'{"schema":"x","schema":"y"}')
    with pytest.raises(ValueError,match="exact v1"):
        ChemistryDocument.from_json(b'{"schema":"wrong"}')

def test_rulebook_rejects_invalid_operation_and_duplicate_input_key():
    with pytest.raises(ValueError,match="unsupported"):
        chemistry_rulebook("sanitize")
    with pytest.raises(ValueError,match="distinct"):
        chemistry_rulebook("similarity",second_artifact_key="chemistry_artifact_id")
