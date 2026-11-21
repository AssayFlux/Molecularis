from __future__ import annotations

from pathlib import Path
import struct

import pytest

from molecularis.genomics import fastq_quality_summary, parse_sam, parse_vcf


def test_sam_parses_valid_record_and_optional_tag() -> None:
    rows = parse_sam("read1\t0\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!!\tNM:i:0")
    assert len(rows) == 1
    assert rows[0].query_name == "read1"
    assert rows[0].cigar == "4M"


@pytest.mark.parametrize(
    "record",
    [
        "read1\t65536\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!!",
        "read1\t0\tchr1\t1\t60\t4Q\t*\t0\t0\tACGT\t!!!!",
        "read1\t0\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!",
        "read1\t0\tchr1\t1\t60\t4M\t*\t0\t0\tACGT\t!!!!\tNM:x:0",
    ],
)
def test_sam_rejects_malformed_records(record: str) -> None:
    with pytest.raises(ValueError):
        parse_sam(record)


def test_vcf_parses_header_and_sample_columns() -> None:
    text = (
        "##fileformat=VCFv4.3\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n"
        "chr1\t10\t.\tA\tG\t50\tPASS\t.\tGT\t0/1\n"
    )
    result = parse_vcf(text)
    assert result[0]["pos"] == 10
    assert result[0]["samples"] == ["S1"]
    assert result[0]["genotypes"] == ["0/1"]


@pytest.mark.parametrize(
    "text",
    [
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t0\t.\tA\tG\t.\tPASS\t.\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t1\t.\tA\tG\tNaN\tPASS\t.\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t1\t.\tA\tG\t.\tPASS\t.\textra\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\nchr1\t1\t.\tA\tG\t.\tPASS\t.\tGT\n",
    ],
)
def test_vcf_rejects_invalid_position_quality_and_column_counts(text: str) -> None:
    with pytest.raises(ValueError):
        parse_vcf(text)


def test_fastq_quality_summary_requires_explicit_supported_offset() -> None:
    assert fastq_quality_summary(["IIII"], offset=33)["mean_phred"] == 40
    with pytest.raises(ValueError):
        fastq_quality_summary(["IIII"], offset=0)



def test_vcf_small_variant_normalization_checks_reference_and_left_aligns() -> None:
    from molecularis.genomics import normalize_small_variant

    # An A insertion in an A repeat is represented at the left-most valid anchor.
    result = normalize_small_variant("chr1", 4, "A", "AA", "CAAAA")
    assert (result["pos"], result["ref"], result["alt"]) == (1, "C", "CA")
    assert result["reference_checked"] is True


def test_variant_normalization_minimizes_substitution_and_rejects_bad_reference() -> None:
    from molecularis.genomics import normalize_small_variant

    result = normalize_small_variant("chr2", 10, "AC", "AT", "N" * 9 + "AC")
    assert (result["pos"], result["ref"], result["alt"]) == (11, "C", "T")
    with pytest.raises(ValueError, match="does not match"):
        normalize_small_variant("chr2", 10, "AG", "AT", "N" * 9 + "AC")


@pytest.mark.parametrize("ref,alt", [("A", "<DEL>"), ("A", "G,T"), ("N", "A")])
def test_variant_normalization_rejects_non_literal_or_ambiguous_alleles(
    ref: str, alt: str,
) -> None:
    from molecularis.genomics import normalize_small_variant

    with pytest.raises(ValueError):
        normalize_small_variant("chr1", 1, ref, alt, "ACGT")


def test_sam_allows_missing_qualities_and_checks_cigar_query_consumption() -> None:
    valid = parse_sam("read1\t0\tchr1\t1\t60\t2M1I1S\t*\t0\t0\tACGT\t*")
    assert valid[0].sequence == "ACGT"
    with pytest.raises(ValueError, match="CIGAR query length"):
        parse_sam("read1\t0\tchr1\t1\t60\t4M\t*\t0\t0\tACG\t*")



def test_bam_binary_record_core_fields_decode_from_gzip_stream() -> None:
    import gzip
    import io
    import struct

    from molecularis.genomics import iter_bam_records

    header = b"BAM\x01" + struct.pack("<i", 0) + struct.pack("<i", 1)
    header += struct.pack("<i", 5) + b"chr1\x00" + struct.pack("<i", 1000)
    core = struct.pack("<iiIIiiii", 0, 9, (60 << 8) | 3, 1, 4, -1, -1, 0)
    name = b"r1\x00"
    cigar = struct.pack("<I", (4 << 4) | 0)
    packed_sequence = bytes([0x12, 0x48])
    qualities = bytes([30, 30, 30, 30])
    block = core + name + cigar + packed_sequence + qualities
    bam = header + struct.pack("<i", len(block)) + block
    records = list(iter_bam_records(io.BytesIO(gzip.compress(bam))))
    assert len(records) == 1
    assert records[0].query_name == "r1"
    assert (records[0].reference, records[0].position, records[0].mapq) == ("chr1", 10, 60)
    assert records[0].cigar == "4M"
    assert records[0].sequence == "ACGT"
    assert records[0].quality == "????"



def test_optional_htslib_adapter_reads_bam_and_requires_local_reference_for_cram(tmp_path: Path) -> None:
    pysam = pytest.importorskip("pysam")
    from molecularis.genomics_htslib import iter_alignment_records

    bam_path = tmp_path / "fixture.bam"
    header = {"HD": {"VN": "1.6"}, "SQ": [{"SN": "chr1", "LN": 1000}]}
    with pysam.AlignmentFile(str(bam_path), "wb", header=header) as output:
        record = pysam.AlignedSegment()
        record.query_name = "read1"
        record.query_sequence = "ACGT"
        record.flag = 0
        record.reference_id = 0
        record.reference_start = 9
        record.mapping_quality = 60
        record.cigar = ((0, 4),)
        record.query_qualities = pysam.qualitystring_to_array("????")
        output.write(record)
    pysam.index(str(bam_path))
    decoded = list(iter_alignment_records(bam_path, region=("chr1", 10, 10)))
    assert decoded[0].sequence == "ACGT"
    assert decoded[0].position == 10
    assert decoded[0].cigar == "4M"

    cram_path = tmp_path / "fixture.cram"
    cram_path.touch()
    with pytest.raises(ValueError, match="local reference"):
        list(iter_alignment_records(cram_path))


@pytest.mark.parametrize(
    "payload, message",
    [
        (b"NOPE", "Invalid BAM magic"),
        (b"BAM\x01" + struct.pack("<i", -1), "header text length"),
        (b"BAM\x01" + struct.pack("<i", 0), "reference count"),
        (
            b"BAM\x01" + struct.pack("<i", 0) + struct.pack("<i", 1),
            "reference name length",
        ),
        (
            b"BAM\x01" + struct.pack("<i", 0) + struct.pack("<i", 0)
            + struct.pack("<i", 31),
            "record block size",
        ),
        (
            b"BAM\x01" + struct.pack("<i", 0) + struct.pack("<i", 0)
            + struct.pack("<i", 32) + b"short",
            "Truncated BAM record block",
        ),
    ],
)
def test_bam_parser_rejects_truncated_and_out_of_bounds_streams(
    payload: bytes, message: str,
) -> None:
    import gzip
    import io

    from molecularis.genomics import iter_bam_records

    with pytest.raises(ValueError, match=message):
        list(iter_bam_records(io.BytesIO(gzip.compress(payload))))


def test_bam_parser_enforces_record_and_total_base_limits() -> None:
    import gzip
    import io

    from molecularis.genomics import iter_bam_records

    header = b"BAM\x01" + struct.pack("<i", 0) + struct.pack("<i", 1)
    header += struct.pack("<i", 5) + b"chr1\x00" + struct.pack("<i", 1000)

    def record(name: bytes, sequence: bytes = bytes([0x12, 0x48])) -> bytes:
        core = struct.pack(
            "<iiIIiiii", 0, 0, (60 << 8) | len(name), (1 << 16) | 1,
            4, -1, -1, 0,
        )
        cigar = struct.pack("<I", (4 << 4) | 0)
        qualities = bytes([30, 30, 30, 30])
        block = core + name + cigar + sequence + qualities
        return struct.pack("<i", len(block)) + block

    bam = header + record(b"r1\x00") + record(b"r2\x00")
    with pytest.raises(ValueError, match="max_records"):
        list(iter_bam_records(io.BytesIO(gzip.compress(bam)), max_records=1))

    with pytest.raises(ValueError, match="max_total_bases"):
        list(iter_bam_records(io.BytesIO(gzip.compress(bam)), max_total_bases=7))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_records": 0},
        {"max_records": True},
        {"max_total_bases": 0},
        {"max_total_bases": False},
    ],
)
def test_bam_parser_rejects_invalid_resource_limits(kwargs: dict[str, object]) -> None:
    import gzip
    import io

    from molecularis.genomics import iter_bam_records

    with pytest.raises(ValueError, match="positive integer"):
        list(iter_bam_records(io.BytesIO(gzip.compress(b"NOPE")), **kwargs))


def test_bam_parser_bounds_aggregate_header_and_reference_dictionary() -> None:
    import gzip
    import io

    from molecularis.genomics import iter_bam_records

    payload = (
        b"BAM\x01" + struct.pack("<i", 0) + struct.pack("<i", 1)
        + struct.pack("<i", 5) + b"chr1\x00" + struct.pack("<i", 1000)
    )
    with pytest.raises(ValueError, match="reference dictionary"):
        list(iter_bam_records(io.BytesIO(gzip.compress(payload)), max_header_bytes=12))


def test_bam_parser_rejects_invalid_header_budget() -> None:
    import gzip
    import io

    from molecularis.genomics import iter_bam_records

    with pytest.raises(ValueError, match="max_header_bytes"):
        list(iter_bam_records(io.BytesIO(gzip.compress(b"NOPE")), max_header_bytes=0))



def test_vcf_aggregate_qc_never_returns_sample_names_or_genotypes() -> None:
    from molecularis.genomics import summarize_vcf_qc

    text = (
        "##fileformat=VCFv4.3\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPRIVATE_SAMPLE_ID\n"
        "chr1\t10\t.\tA\tG\t50\tPASS\t.\tGT\t0/1\n"
        "chr1\t20\t.\tC\tT,G\t.\tLowQual\t.\tGT\t1|2\n"
    )
    result = summarize_vcf_qc(text)
    assert result["record_count"] == 2
    assert result["sample_count"] == 1
    assert result["contig_record_counts"] == {"chr1": 2}
    assert result["filter_counts"] == {"LowQual": 1, "PASS": 1}
    assert result["multiallelic_record_count"] == 1
    assert result["missing_quality_record_count"] == 1
    assert "PRIVATE_SAMPLE_ID" not in str(result)
    assert "0/1" not in str(result) and "1|2" not in str(result)
    assert "genotypes" not in result and "samples" not in result


def test_vcf_aggregate_qc_enforces_resource_bounds_and_requires_records() -> None:
    from molecularis.genomics import summarize_vcf_qc

    with pytest.raises(ValueError, match="5 MiB"):
        summarize_vcf_qc("x" * (5 * 1024 * 1024 + 1))
    with pytest.raises(ValueError, match="max_records"):
        summarize_vcf_qc(
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
            "chr1\t1\t.\tA\tG\t.\tPASS\t.\n"
            "chr1\t2\t.\tA\tC\t.\tPASS\t.\n",
            max_records=1,
        )
    with pytest.raises(ValueError, match="no variant records"):
        summarize_vcf_qc("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
