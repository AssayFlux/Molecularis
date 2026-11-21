from __future__ import annotations
import json
import pytest
from molecularis.phylogeny_service import PhylogenyDocument, ingest_phylogeny, load_phylogeny, register_phylogeny_service, phylogeny_rulebook
from molecularis.platform import MolecularisPlatform

def alignment():
    return PhylogenyDocument("demo",("A","B","C","D"),("A"*40+"C"*10,"A"*39+"G"+"C"*10,"A"*38+"GG"+"C"*10,"A"*37+"GGG"+"C"*10),"fixture-alignment")

def test_document_canonical_round_trip_and_digest():
    record=alignment(); restored=PhylogenyDocument.from_json(record.to_json())
    assert restored==record and restored.sha256==record.sha256 and restored.alignment_length==50

@pytest.mark.parametrize("taxa,sequences",[(("A","A","C"),("AAAA","AAAT","AATT")),(("A","B","C"),("AAAA","AAA","AATT")),(("A","B","C"),("AAAA","AA?A","AATT"))])
def test_document_rejects_duplicate_ids_dimensions_and_symbols(taxa,sequences):
    with pytest.raises((ValueError,TypeError)): PhylogenyDocument("bad",taxa,sequences)

def test_document_rejects_duplicate_json_keys_and_unknown_fields():
    with pytest.raises(ValueError,match="duplicate"): PhylogenyDocument.from_json('{"schema":"x","schema":"y"}')
    value=json.loads(alignment().to_json()); value["unexpected"]=True
    with pytest.raises(ValueError,match="fields"): PhylogenyDocument.from_json(json.dumps(value))

def test_artifact_round_trip_and_metadata_integrity():
    platform=MolecularisPlatform(); record=alignment(); artifact=ingest_phylogeny(platform,record)
    assert load_phylogeny(platform,artifact.id)==record

def test_msde_operations_and_rulebook_execution():
    platform=MolecularisPlatform(); artifact=ingest_phylogeny(platform,alignment()); register_phylogeny_service(platform)
    for operation in ("validate","distance_matrix","neighbor_joining","upgma","bootstrap"):
        report=platform.execute_rulebook(phylogeny_rulebook(operation,parameters={"minimum_sites":20,"replicates":20,"seed":7}),{"phylogeny_artifact_id":artifact.id})
        assert report.status=="succeeded"
    report=platform.execute_rulebook(phylogeny_rulebook("neighbor_joining"),{"phylogeny_artifact_id":artifact.id})
    assert report.outputs["phylogeny_result"]["result"]["newick"].endswith(";")

def test_bootstrap_is_reproducible_and_bounded():
    from molecularis.phylo import bootstrap_neighbor_joining_from_alignment
    record=alignment(); data=dict(zip(record.taxon_ids,record.aligned_sequences))
    a=bootstrap_neighbor_joining_from_alignment(data,replicates=25,seed=91,minimum_sites=20)
    b=bootstrap_neighbor_joining_from_alignment(data,replicates=25,seed=91,minimum_sites=20)
    assert a["splits"]==b["splits"] and a["requested_replicates"]==25
    assert a["successful_replicates"]+a["failed_replicates"]==25

def test_service_rejects_saturated_distances():
    record=PhylogenyDocument("saturated",("A","B","C"),("A"*30,"C"*30,"G"*30))
    platform=MolecularisPlatform(); artifact=ingest_phylogeny(platform,record); register_phylogeny_service(platform)
    result=platform.execute_rulebook(phylogeny_rulebook("neighbor_joining"),{"phylogeny_artifact_id":artifact.id})
    assert result.status=="failed"

def test_rulebook_rejects_unknown_operation():
    with pytest.raises(ValueError,match="unsupported"): phylogeny_rulebook("maximum_likelihood")
