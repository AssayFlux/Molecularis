from __future__ import annotations

import pytest

from molecularis.genomics_service import (
    GenomeDocument, ingest_genome, load_genome, register_genomics_service, genomics_rulebook,
)
from molecularis.platform import MolecularisPlatform
from molecularis.sequence import SequenceRecord


def _platform(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    register_genomics_service(platform)
    return platform


def _genome():
    return GenomeDocument("fixture-genome", (
        SequenceRecord("chr1", "ATG" + "AAA" * 12 + "TAA" + "ACGT" * 10),
        SequenceRecord("plasmid", "GGCCNNATTA"),
    ), "synthetic assembly")


def test_genome_document_is_canonical_and_roundtrips():
    document = _genome()
    restored = GenomeDocument.from_json(document.to_json())
    assert restored == document
    assert restored.sha256 == document.sha256
    assert restored.total_bases == document.total_bases


@pytest.mark.parametrize("payload", [
    b'{"schema":"molecularis.genome-record.v1","schema":"x"}',
    b'{"schema":"molecularis.genome-record.v1","identifier":"x","description":"","alphabet":"DNA_IUPAC","contigs":[]}',
])
def test_genome_document_rejects_duplicate_keys_and_empty_assemblies(payload):
    with pytest.raises(ValueError):
        GenomeDocument.from_json(payload)


def test_genome_document_rejects_duplicate_contigs_and_invalid_alphabet():
    with pytest.raises(ValueError, match="unique"):
        GenomeDocument("x", (SequenceRecord("c", "ACGT"), SequenceRecord("c", "TTTT")))
    with pytest.raises(ValueError):
        GenomeDocument("x", (SequenceRecord("c", "ACGT-"),))


def test_ingest_load_and_integrity_metadata(tmp_path):
    platform = _platform(tmp_path)
    document = _genome()
    artifact = ingest_genome(platform, document)
    assert load_genome(platform, artifact.artifact_id) == document
    assert artifact.metadata["total_bases"] == document.total_bases
    platform.close()


def _execute(platform, operation, **parameters):
    artifact = ingest_genome(platform, _genome())
    rulebook = genomics_rulebook(operation, parameters=parameters)
    return platform.execute(rulebook, {"genome_artifact_id": artifact.artifact_id})["genomics_result"]


def test_msde_validate_and_assembly_qc(tmp_path):
    platform = _platform(tmp_path)
    assert _execute(platform, "validate")["result"]["valid"] is True
    qc = _execute(platform, "assembly_qc")
    assert qc["result"]["contig_count"] == 2
    assert qc["result"]["total_bases"] > 0
    platform.close()


def test_msde_orf_scan_is_explicitly_candidate_only(tmp_path):
    platform = _platform(tmp_path)
    result = _execute(platform, "orf_scan", min_protein_length=1, table_id=11)
    assert result["result"]["conclusion"] == "candidate_orfs_only_not_gene_annotation"
    platform.close()


def test_msde_gff3_checks_contig_membership(tmp_path):
    platform = _platform(tmp_path)
    gff = "##gff-version 3\nchr1\ts\tgene\t1\t20\t.\t+\t.\tID=g1\n"
    result = _execute(platform, "annotation_validate", gff3_text=gff)
    assert result["result"]["feature_count"] == 1
    with pytest.raises(Exception, match="contigs absent"):
        _execute(platform, "annotation_validate", gff3_text=gff.replace("chr1", "unknown"))
    platform.close()


def test_msde_vcf_qc_is_aggregate_and_binds_reference_contigs(tmp_path):
    platform = _platform(tmp_path)
    vcf = "##fileformat=VCFv4.3\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t2\t.\tT\tC\t50\tPASS\t.\n"
    result = _execute(platform, "variant_qc", vcf_text=vcf)
    assert result["result"]["record_count"] == 1
    assert result["result"]["reference_genome_sha256"]
    assert "samples" not in result["result"]
    assert result["result"]["reference_alleles_checked"] is False
    platform.close()


def test_rulebook_rejects_unknown_operation():
    with pytest.raises(ValueError, match="unsupported"):
        genomics_rulebook("shell")
