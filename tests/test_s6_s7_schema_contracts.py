from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from molecularis.gff3 import parse_gff3
from molecularis.sequence import SequenceRecord
from molecularis.sequence_reference import ReferencePack, local_alignment_reference_search


ROOT = Path(__file__).resolve().parents[1]


def _schema(name: str) -> dict[str, object]:
    return json.loads((ROOT / "api" / name).read_text(encoding="utf-8"))


def test_local_alignment_result_matches_versioned_schema() -> None:
    pack = ReferencePack(
        "fixture", "1", "CC0-1.0", "https://example.org/fixture",
        hashlib.sha256(b"fixture").hexdigest(),
    )
    result = local_alignment_reference_search(
        "ACGT", [SequenceRecord("ref", "TTACGTAA")],
        sequence_type="DNA", reference_pack=pack,
    )
    Draft202012Validator.check_schema(_schema("local-alignment-evidence.schema.json"))
    Draft202012Validator(_schema("local-alignment-evidence.schema.json")).validate(result)


def test_gff3_import_result_matches_versioned_schema() -> None:
    result = parse_gff3([
        "##gff-version 3\n",
        "chr1\ts\tgene\t1\t20\t.\t+\t.\tID=g1\n",
        "chr1\ts\tmRNA\t1\t20\t.\t+\t.\tID=t1;Parent=g1\n",
    ])
    Draft202012Validator.check_schema(_schema("gff3-annotation-import.schema.json"))
    Draft202012Validator(_schema("gff3-annotation-import.schema.json")).validate(result)


def test_gff3_transcript_cds_result_matches_versioned_schema() -> None:
    from molecularis.gff3_transcripts import reconstruct_gff3_cds

    annotation = parse_gff3([
        "##gff-version 3\n",
        "chr1\ts\tgene\t1\t9\t.\t+\t.\tID=g\n",
        "chr1\ts\tmRNA\t1\t9\t.\t+\t.\tID=t;Parent=g\n",
        "chr1\ts\tCDS\t1\t9\t.\t+\t0\tParent=t\n",
    ])
    result = reconstruct_gff3_cds(annotation, {"chr1": "ATGAAATAA"}, table_id=1)
    Draft202012Validator.check_schema(_schema("gff3-transcript-cds.schema.json"))
    Draft202012Validator(_schema("gff3-transcript-cds.schema.json")).validate(result)
