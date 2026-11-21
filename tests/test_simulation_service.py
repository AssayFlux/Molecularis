from __future__ import annotations
import hashlib,json,pytest
from molecularis.simulation_service import SimulationDocument,analyze_energy_series,ingest_simulation,load_simulation,register_simulation_service,simulation_rulebook
from molecularis.platform import Budget,MolecularisPlatform
from molecularis.platform.contracts import ValidationError

def doc(**kw):
    base=dict(identifier="md-001",engine="openmm",ensemble="NVT",temperature_kelvin=300.0,timestep_fs=1.0,steps=1000,equilibration_steps=100,replicas=2,seed=7,coordinates_sha256="a"*64,topology_sha256="b"*64,force_field_name="amber",force_field_version="ff19SB",parameter_source_sha256="c"*64)
    base.update(kw); return SimulationDocument(**base)
def runtime(tmp_path):
    p=MolecularisPlatform(tmp_path/"store"); p.start(); register_simulation_service(p); return p

def test_canonical_roundtrip_digest():
    a=doc(); assert SimulationDocument.from_json(a.to_json())==a
    assert hashlib.sha256(a.to_json()).hexdigest()==a.sha256 and a.to_json()==doc().to_json()
@pytest.mark.parametrize("kw",[{"engine":"bad"},{"ensemble":"NPT"},{"temperature_kelvin":0},{"timestep_fs":5},{"steps":0},{"replicas":1},{"seed":2**32},{"pressure_bar":1.0},{"coordinates_sha256":"bad"},{"parameter_source_sha256":"A"*64}])
def test_protocol_rejects_invalid_values(kw):
    with pytest.raises(ValueError): doc(**kw)
def test_npt_and_gromacs_contracts():
    assert doc(ensemble="NPT",pressure_bar=1.0).ensemble=="NPT"
    g=doc(engine="gromacs",gromacs_tpr_path="/tmp/input.tpr",gromacs_tpr_sha256="d"*64,gromacs_executable_path="/usr/bin/gmx",gromacs_executable_sha256="e"*64)
    assert SimulationDocument.from_json(g.to_json())==g
def test_json_duplicate_and_unknown_fields():
    a=doc().to_dict(); raw=json.dumps(a).replace('"identifier":"md-001"','"identifier":"md-001","identifier":"other"')
    with pytest.raises(ValueError,match="duplicate"): SimulationDocument.from_json(raw)
    a["unexpected"]=True
    with pytest.raises(ValueError,match="fields"): SimulationDocument.from_json(json.dumps(a))
def test_msde_roundtrip_and_validation_rulebook(tmp_path):
    p=runtime(tmp_path)
    try:
        art=ingest_simulation(p,doc()); assert load_simulation(p,art.artifact_id)==doc()
        result=p.execute(simulation_rulebook("validate"),{"simulation_artifact_id":art.artifact_id})["simulation_result"]
        assert result["result"]["valid"] and result["protocol_sha256"]==art.digest
        with pytest.raises(Exception,match="byte budget"): load_simulation(p,art.artifact_id,budget=Budget(max_bytes=1))
    finally: p.close()
def test_energy_analysis_statistics_and_limits():
    r=analyze_energy_series([1.0,2.0,3.0,4.0])
    assert r["sample_count"]==4 and r["mean"]==2.5 and r["net_change"]==3.0
    assert r["linear_slope_per_sample"]==pytest.approx(1.0)
    with pytest.raises(ValueError,match="2..1000000"): analyze_energy_series([1.0])
    with pytest.raises(ValueError,match="finite"): analyze_energy_series([1.0,float("nan")])
def test_energy_analysis_via_rulebook(tmp_path):
    p=runtime(tmp_path)
    try:
        art=ingest_simulation(p,doc(energy_series=(1.0,2.0,3.0)))
        result=p.execute(simulation_rulebook("energy_analysis"),{"simulation_artifact_id":art.artifact_id})["simulation_result"]
        assert result["result"]["mean"]==2.0
    finally: p.close()
def test_gromacs_rulebook_rejects_wrong_engine(tmp_path):
    p=runtime(tmp_path)
    try:
        art=ingest_simulation(p,doc())
        with pytest.raises(ValidationError,match="requires a GROMACS"): p.execute(simulation_rulebook("gromacs_run",parameters={"output_directory":str(tmp_path/"out")}),{"simulation_artifact_id":art.artifact_id})
    finally: p.close()
