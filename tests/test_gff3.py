from __future__ import annotations

import pytest

from molecularis.gff3 import parse_gff3


def test_gff3_import_checks_hierarchy_and_coordinate_system() -> None:
    result = parse_gff3([
        "##gff-version 3\n",
        "##sequence-region chr1 1 1000\n",
        "chr1\tRefSeq\tgene\t10\t900\t.\t+\t.\tID=g1;Name=gene%20one\n",
        "chr1\tRefSeq\tmRNA\t10\t900\t.\t+\t.\tID=t1;Parent=g1\n",
        "chr1\tRefSeq\texon\t10\t100\t.\t+\t.\tParent=t1\n",
        "chr1\tRefSeq\tCDS\t20\t100\t42.5\t+\t0\tID=c1;Parent=t1\n",
    ])
    assert result["feature_count"] == 4
    assert result["features"][0]["attributes"]["Name"] == "gene one"
    assert result["parent_edge_count"] == 3
    assert result["coordinate_system"] == "1-based inclusive (GFF3)"
    assert result["feature_type_counts"] == {"CDS": 1, "exon": 1, "gene": 1, "mRNA": 1}


def test_gff3_import_accepts_multiple_parents_and_skips_embedded_fasta() -> None:
    result = parse_gff3([
        "##gff-version 3\n",
        "chr1\ts\tgene\t1\t50\t.\t+\t.\tID=g1\n",
        "chr1\ts\tgene\t1\t50\t.\t+\t.\tID=g2\n",
        "chr1\ts\texon\t5\t10\t.\t+\t.\tParent=g1,g2\n",
        "##FASTA\n", ">chr1\n", "ACGT\n",
    ])
    assert result["feature_count"] == 3
    assert result["parent_edge_count"] == 2


@pytest.mark.parametrize("records, message", [
    (["chr1\ts\tgene\t1\t4\t.\t+\t.\tID=g1\n"], "version 3"),
    (["##gff-version 3\n", "chr1\ts\tCDS\t1\t4\t.\t+\t.\tID=c1\n"], "CDS phase"),
    (["##gff-version 3\n", "chr1\ts\tgene\t0\t4\t.\t+\t.\tID=g1\n"], "positive"),
    (["##gff-version 3\n", "chr1\ts\tgene\t1\t4\tNaN\t+\t.\tID=g1\n"], "finite"),
    (["##gff-version 3\n", "chr1\ts\texon\t1\t4\t.\t+\t.\tParent=missing\n"], "does not resolve"),
])
def test_gff3_rejects_invalid_annotations(records, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parse_gff3(records)


def test_gff3_rejects_duplicate_ids_out_of_parent_bounds_and_cycles() -> None:
    with pytest.raises(ValueError, match="unique"):
        parse_gff3(["##gff-version 3\n",
                    "chr1\ts\tgene\t1\t4\t.\t+\t.\tID=g1\n",
                    "chr1\ts\tgene\t1\t4\t.\t+\t.\tID=g1\n"])
    with pytest.raises(ValueError, match="within its parent"):
        parse_gff3(["##gff-version 3\n",
                    "chr1\ts\tgene\t1\t4\t.\t+\t.\tID=g1\n",
                    "chr1\ts\texon\t1\t5\t.\t+\t.\tParent=g1\n"])
    with pytest.raises(ValueError, match="cycle"):
        parse_gff3(["##gff-version 3\n",
                    "chr1\ts\tgene\t1\t20\t.\t+\t.\tID=a;Parent=b\n",
                    "chr1\ts\tgene\t1\t20\t.\t+\t.\tID=b;Parent=a\n"])


@pytest.mark.parametrize("kwargs", [
    {"max_lines": True}, {"max_features": 0},
    {"max_attribute_bytes": 1.5}, {"max_total_attribute_bytes": 0},
])
def test_gff3_validates_resource_limits(kwargs) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        parse_gff3(["##gff-version 3\n"], **kwargs)


def test_gff3_enforces_feature_and_attribute_budgets() -> None:
    records = ["##gff-version 3\n",
               "chr1\ts\tgene\t1\t4\t.\t+\t.\tID=g1\n",
               "chr1\ts\tgene\t5\t8\t.\t+\t.\tID=g2\n"]
    with pytest.raises(ValueError, match="max_features"):
        parse_gff3(records, max_features=1)
    with pytest.raises(ValueError, match="max_attribute_bytes"):
        parse_gff3(records[:2], max_attribute_bytes=2)


def test_gff3_enforces_total_attribute_and_line_budgets_and_sequence_regions() -> None:
    valid = [
        "##gff-version 3\n",
        "##sequence-region chr1 1 10\n",
        "chr1\ts\tgene\t1\t4\t.\t+\t.\tID=g1\n",
    ]
    with pytest.raises(ValueError, match="max_total_attribute_bytes"):
        parse_gff3(valid, max_total_attribute_bytes=2)
    with pytest.raises(ValueError, match="max_lines"):
        parse_gff3(valid, max_lines=2)
    outside = valid[:2] + ["chr1\ts\tgene\t1\t11\t.\t+\t.\tID=g1\n"]
    with pytest.raises(ValueError, match="sequence-region"):
        parse_gff3(outside)
