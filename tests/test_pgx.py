from __future__ import annotations

import hashlib
import json
from typing import cast

import pytest
from molecularis.pgx import VariantKey, match_phased_haplotype, parse_star_allele_definitions

def pack() -> str:
    value = {"schema_version":1,"genome_build":"synthetic-build-v1",
      "source":{"name":"synthetic","release":"fixture-1","url":"https://example.invalid/source",
      "license":"CC0 synthetic test only","sha256":hashlib.sha256(b"synthetic source").hexdigest()},
      "definitions":[
       {"gene":"SYN1","star_allele":"*1","id":"syn1-star1","required_variants":[],
        "excluded_variants":[{"chromosome":"chr1","position":2,"ref":"A","alt":"G"}]},
       {"gene":"SYN1","star_allele":"*2","id":"syn1-star2","required_variants":[
        {"chromosome":"chr1","position":2,"ref":"A","alt":"G"}],"excluded_variants":[]}]}
    return json.dumps(value)

def test_synthetic_pack_and_confirmed_haplotype_match():
    definitions=parse_star_allele_definitions(pack(),expected_source_release="fixture-1")
    result=match_phased_haplotype("SYN1",[VariantKey("synthetic-build-v1","chr1",2,"A","G")],
      definitions,genome_build="synthetic-build-v1",phase_confirmed=True,call_complete=True)
    assert result.status=="matched" and result.star_allele=="*2"

@pytest.mark.parametrize(("phase","complete","expected"),[(False,True,"no_call_unphased"),(True,False,"no_call_incomplete")])
def test_incomplete_or_unphased_abstains(phase,complete,expected):
    result=match_phased_haplotype("SYN1",[],parse_star_allele_definitions(pack(),expected_source_release="fixture-1"),
      genome_build="synthetic-build-v1",phase_confirmed=phase,call_complete=complete)
    assert result.status==expected and result.star_allele is None

def test_build_mismatch_and_release_digest_metadata_rejected():
    definitions=parse_star_allele_definitions(pack(),expected_source_release="fixture-1")
    with pytest.raises(ValueError,match="genome build"):
      match_phased_haplotype("SYN1",[VariantKey("other","chr1",2,"A","G")],definitions,
        genome_build="synthetic-build-v1",phase_confirmed=True,call_complete=True)
    with pytest.raises(ValueError,match="release"):
      parse_star_allele_definitions(pack(),expected_source_release="fixture-2")
    value=json.loads(pack()); value["source"]["sha256"]="bad"
    with pytest.raises(ValueError,match="SHA-256"):
      parse_star_allele_definitions(json.dumps(value),expected_source_release="fixture-1")

def test_overlapping_best_definitions_abstain_as_ambiguous():
    value=json.loads(pack()); value["definitions"].append({
      "gene":"SYN1","star_allele":"*3","id":"syn1-star3",
      "required_variants":[{"chromosome":"chr1","position":2,"ref":"A","alt":"G"}],"excluded_variants":[]})
    defs=parse_star_allele_definitions(json.dumps(value),expected_source_release="fixture-1")
    result=match_phased_haplotype("SYN1",[VariantKey("synthetic-build-v1","chr1",2,"A","G")],defs,
      genome_build="synthetic-build-v1",phase_confirmed=True,call_complete=True)
    assert result.status=="ambiguous" and result.star_allele is None

def test_variant_key_rejects_bool_coordinate_and_nonliteral_allele():
    with pytest.raises(ValueError): VariantKey("b","c",True,"A","G")
    with pytest.raises(ValueError): VariantKey("b","c",1,"N","G")


def test_pgx_definition_parser_enforces_resource_bounds():
    with pytest.raises(ValueError, match="max_input_bytes"):
        parse_star_allele_definitions(
            pack(), expected_source_release="fixture-1", max_input_bytes=1
        )
    with pytest.raises(ValueError, match="max_definitions"):
        parse_star_allele_definitions(
            pack(), expected_source_release="fixture-1", max_definitions=1
        )
    value = json.loads(pack())
    value["definitions"][0]["excluded_variants"] = [
        {"chromosome": "chr1", "position": 2, "ref": "A", "alt": "G"},
        {"chromosome": "chr1", "position": 3, "ref": "C", "alt": "T"},
    ]
    with pytest.raises(ValueError, match="max_variants_per_definition"):
        parse_star_allele_definitions(
            json.dumps(value), expected_source_release="fixture-1",
            max_variants_per_definition=1,
        )
    for invalid in (0, -1, True, 1.5):
        with pytest.raises(ValueError, match="positive integer"):
            parse_star_allele_definitions(
                pack(), expected_source_release="fixture-1",
                max_definitions=cast(int, invalid),
            )


def test_pgx_definition_parser_rejects_non_text_input():
    with pytest.raises(TypeError, match="must be text"):
        parse_star_allele_definitions(
            cast(str, None), expected_source_release="fixture-1"
        )
