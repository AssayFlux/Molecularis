from __future__ import annotations
import json
import pytest
from molecularis.platform import MolecularisPlatform, Budget
from molecularis.platform.contracts import ValidationError
from molecularis.structure import Atom
from molecularis.structure_service import StructureDocument, ingest_structure, load_structure, register_structure_service, structure_rulebook

def atom(serial,x,y,z,*,name="CA",residue="GLY",chain="A",number=None,element="C"):
    return Atom(serial,name,residue,chain,serial if number is None else number,x,y,z,element)

def runtime(tmp_path):
    p=MolecularisPlatform(tmp_path/"store"); p.start(); register_structure_service(p); return p

def test_structure_canonical_roundtrip_hash():
    a=StructureDocument("fixture",(atom(1,0,0,0),atom(2,1,0,0))); b=StructureDocument.from_json(a.to_json())
    assert a==b and a.sha256==b.sha256 and b.atom_count==2 and b.residue_count==2

def test_structure_rejects_invalid_coordinates_and_duplicate_serials():
    with pytest.raises(ValueError,match="finite"): StructureDocument("bad",(atom(1,float("nan"),0,0),))
    with pytest.raises(ValueError,match="unique"): StructureDocument("bad",(atom(1,0,0,0),atom(1,1,0,0)))

def test_json_rejects_duplicate_keys_and_extra_fields():
    with pytest.raises(ValueError,match="duplicate"): StructureDocument.from_json(b'{"schema":"x","schema":"y"}')
    value=StructureDocument("x",(atom(1,0,0,0),)).to_dict(); value["extra"]=1
    with pytest.raises(ValueError,match="exact"): StructureDocument.from_json(json.dumps(value))

def test_pdb_mmcif_import():
    pdb="ATOM      1  CA  GLY A   1       0.000   0.000   0.000  1.00 20.00           C  \nATOM      2  N   GLY A   1       1.000   0.000   0.000  1.00 20.00           N  \n"
    assert StructureDocument.from_pdb("pdb",pdb).atom_count==2
    cif="""data_demo
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM 1 C CA GLY A 1 0.0 0.0 0.0
ATOM 2 N N GLY A 1 1.0 0.0 0.0
#
"""
    assert StructureDocument.from_mmcif("cif",cif).atoms[1].element=="N"

def test_artifact_integrity_and_type(tmp_path):
    p=runtime(tmp_path)
    try:
        doc=StructureDocument("one",(atom(1,0,0,0),)); art=ingest_structure(p,doc)
        assert load_structure(p,art.artifact_id)==doc
        other=p.ingest(b"{}",media_type="application/json",schema_id="other.v1")
        with pytest.raises(ValidationError,match="not a Structure"): load_structure(p,other.artifact_id)
    finally: p.close()

@pytest.mark.parametrize("op",["validate","geometry","contacts","sasa","interactions"])
def test_single_artifact_capabilities(tmp_path,op):
    p=runtime(tmp_path)
    try:
        doc=StructureDocument("small",(atom(1,0,0,0,name="NZ",residue="LYS",chain="A",number=1,element="N"),atom(2,3,0,0,name="OD1",residue="ASP",chain="B",number=2,element="O")))
        art=ingest_structure(p,doc); out=p.execute(structure_rulebook(op),{"structure_artifact_id":art.artifact_id})["structure_result"]
        assert out["operation"]==op and out["structure_sha256"]==doc.sha256 and len(out["rules_checked"])==7
    finally: p.close()

def test_rmsd_uses_two_artifacts_and_caller_order(tmp_path):
    p=runtime(tmp_path)
    try:
        a=StructureDocument("a",(atom(1,0,0,0),atom(2,1,0,0),atom(3,0,1,0)))
        b=StructureDocument("b",(atom(1,4,2,0),atom(2,5,2,0),atom(3,4,3,0)))
        aa,bb=ingest_structure(p,a),ingest_structure(p,b)
        out=p.execute(structure_rulebook("rmsd",parameters={"superpose":True}),{"structure_artifact_id":aa.artifact_id,"reference_structure_artifact_id":bb.artifact_id})
        assert out["structure_result"]["result"]["rmsd_angstrom"]==pytest.approx(0,abs=1e-8)
    finally: p.close()

def test_budget_enforced(tmp_path):
    p=runtime(tmp_path)
    try:
        art=ingest_structure(p,StructureDocument("one",(atom(1,0,0,0),)))
        with pytest.raises(Exception,match="byte budget"): load_structure(p,art.artifact_id,budget=Budget(max_bytes=1))
    finally: p.close()
