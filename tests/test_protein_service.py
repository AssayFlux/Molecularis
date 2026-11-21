from __future__ import annotations
import hashlib,json
import pytest
from molecularis.platform import MolecularisPlatform
from molecularis.protein_service import ProteinDocument,ingest_protein,load_protein,register_protein_service,protein_rulebook

def runtime(tmp_path):
    p=MolecularisPlatform(tmp_path/"store"); p.start(); register_protein_service(p); return p

def test_document_roundtrip_integrity_and_normalization(tmp_path):
    p=runtime(tmp_path)
    try:
        doc=ProteinDocument("p1"," acd\nEFG ","fixture"); art=ingest_protein(p,doc)
        assert doc.sequence=="ACDEFG" and load_protein(p,art.artifact_id)==doc
        assert ProteinDocument.from_json(doc.to_json()).sha256==doc.sha256
    finally:p.close()

@pytest.mark.parametrize("op",["validate","descriptors"])
def test_basic_capabilities(tmp_path,op):
    p=runtime(tmp_path)
    try:
        doc=ProteinDocument("p1","ACDEFGHIKLMNPQRSTVWY"); art=ingest_protein(p,doc)
        out=p.execute(protein_rulebook(op),{"protein_artifact_id":art.artifact_id})["protein_result"]
        assert out["operation"]==op and out["protein_sha256"]==doc.sha256
        if op=="descriptors": assert out["result"]["length"]==20
    finally:p.close()

def test_motif_scan_capability_is_hash_pinned(tmp_path):
    p=runtime(tmp_path)
    try:
        doc=ProteinDocument("p1","AAMKWPHAD"); art=ingest_protein(p,doc)
        raw=json.dumps({"schema_version":1,"motifs":[{"id":"m1","pattern":"MKW"}]},separators=(",",":"))
        params={"motif_pack_json":raw,"motif_pack":{"name":"fixture","version":"1","license":"CC0-1.0","source":"https://example.org","content_sha256":hashlib.sha256(raw.encode()).hexdigest()}}
        out=p.execute(protein_rulebook("motif_scan",parameters=params),{"protein_artifact_id":art.artifact_id})["protein_result"]
        assert out["result"]["hits"][0]["start_1based"]==3
    finally:p.close()

def test_design_brief_capability_is_non_generative(tmp_path):
    p=runtime(tmp_path)
    try:
        art=ingest_protein(p,ProteinDocument("p1","ACDEFG"))
        brief={"schema":"kinetics.protein-design-brief.v1","objective":"stability","target_description":"research scaffold","length_min":80,"length_max":100,"fold_constraints":[],"expression_host":"unspecified","localization":"unspecified","disallowed_motifs":[],"safety_exclusions":["toxicity"],"human_review_required":True}
        out=p.execute(protein_rulebook("design_brief",parameters={"brief":brief}),{"protein_artifact_id":art.artifact_id})["protein_result"]
        assert out["result"]["generation_status"]=="blocked_no_approved_model_or_benchmark"
    finally:p.close()

def test_contract_rejects_duplicate_keys_and_noncanonical_residues():
    with pytest.raises(ValueError,match="duplicate JSON key"):
        ProteinDocument.from_json(b'{"schema":"x","schema":"y"}')
    with pytest.raises(ValueError,match="canonical 20"):
        ProteinDocument("x","ACDX")
    with pytest.raises(ValueError,match="exact v1"):
        ProteinDocument.from_json(b'{"schema":"wrong"}')

def test_rulebook_rejects_unknown_operation():
    with pytest.raises(ValueError,match="unsupported"):
        protein_rulebook("fold")
