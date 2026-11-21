from __future__ import annotations

import pytest

from molecularis.gff3 import parse_gff3
from molecularis.gff3_transcripts import reconstruct_gff3_cds


def test_plus_strand_multiexon_cds_reconstruction_and_translation() -> None:
    annotation = parse_gff3([
        "##gff-version 3\n",
        "chr1\ts\tgene\t1\t12\t.\t+\t.\tID=g\n",
        "chr1\ts\tmRNA\t1\t12\t.\t+\t.\tID=t;Parent=g\n",
        "chr1\ts\tCDS\t1\t4\t.\t+\t0\tParent=t\n",
        "chr1\ts\tCDS\t9\t12\t.\t+\t2\tParent=t\n",
    ])
    result = reconstruct_gff3_cds(annotation, {"chr1": "ATGAAAAAATAA"}, table_id=1)
    transcript = result["transcripts"][0]
    assert transcript["cds_sequence"] == "ATGAATAA"
    assert transcript["phase_consistent"] is True
    assert transcript["translation_status"] == "abstained"


def test_minus_strand_segments_are_joined_in_transcriptional_order() -> None:
    annotation = parse_gff3([
        "##gff-version 3\n",
        "chr1\ts\tgene\t1\t12\t.\t-\t.\tID=g\n",
        "chr1\ts\tmRNA\t1\t12\t.\t-\t.\tID=t;Parent=g\n",
        "chr1\ts\tCDS\t9\t12\t.\t-\t0\tParent=t\n",
        "chr1\ts\tCDS\t1\t4\t.\t-\t2\tParent=t\n",
    ])
    result = reconstruct_gff3_cds(annotation, {"chr1": "TTACAAAAATCA"}, table_id=1)
    transcript = result["transcripts"][0]
    assert transcript["cds_sequence"] == "TGATGTAA"
    assert transcript["segment_phases"][1]["expected_phase"] == 2


def test_reconstruction_rejects_missing_transcript_and_bounds() -> None:
    with pytest.raises(ValueError, match="does not resolve"):
        parse_gff3([
            "##gff-version 3\n",
            "chr1\ts\tCDS\t1\t3\t.\t+\t0\tParent=missing\n",
        ])


def test_complete_single_exon_cds_translates_with_explicit_table() -> None:
    annotation = parse_gff3([
        "##gff-version 3\n",
        "chr1\ts\tgene\t1\t9\t.\t+\t.\tID=g\n",
        "chr1\ts\tmRNA\t1\t9\t.\t+\t.\tID=t;Parent=g\n",
        "chr1\ts\tCDS\t1\t9\t.\t+\t0\tParent=t\n",
    ])
    result = reconstruct_gff3_cds(annotation, {"chr1": "ATGAAATAA"}, table_id=1)
    transcript = result["transcripts"][0]
    assert transcript["translation_status"] == "translated"
    assert transcript["protein_sequence"] == "MK"
    assert transcript["cds_sequence"] == "ATGAAATAA"


def test_partial_first_cds_phase_is_preserved_but_not_translated() -> None:
    annotation = parse_gff3([
        "##gff-version 3\n",
        "chr1\ts\tgene\t1\t6\t.\t+\t.\tID=g\n",
        "chr1\ts\tmRNA\t1\t6\t.\t+\t.\tID=t;Parent=g\n",
        "chr1\ts\tCDS\t1\t6\t.\t+\t1\tParent=t\n",
    ])
    result = reconstruct_gff3_cds(annotation, {"chr1": "AATGAA"}, table_id=1)
    transcript = result["transcripts"][0]
    assert transcript["phase_consistent"] is True
    assert transcript["translation_status"] == "partial_cds"
