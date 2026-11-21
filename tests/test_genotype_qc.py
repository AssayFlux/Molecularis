from __future__ import annotations

import json
from typing import cast
from hashlib import sha256
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from molecularis.genotype_qc import aggregate_synthetic_vcf_qc
from molecularis.variant_reference import ReferenceSequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "api" / "synthetic-genotype-qc.schema.json").read_text(encoding="utf-8")
)

VCF = """##fileformat=VCFv4.3
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYN_A\tSYN_B\tSYN_C
chrSynthetic1\t2\t.\tA\tG\t60\tPASS\t.\tGT:GQ\t0/1:99\t1|1:80\t./.:.
chrSynthetic1\t5\t.\tC\tT,G\t50\tPASS\t.\tGT\t0/2\t0/0\t1/2
"""


def _reference() -> ReferenceSequence:
    sequence = "CAAACTGCC"
    return ReferenceSequence(
        assembly="synthetic-build-v1",
        accession="SYNTHETIC:CONTIG1",
        release="fixture-1",
        contig="chrSynthetic1",
        sequence=sequence,
        sequence_sha256=sha256(sequence.encode("ascii")).hexdigest(),
        retrieved_at="2026-11-11T00:00:00Z",
    )


def _run(document: str = VCF, *, reference: ReferenceSequence | None = None) -> dict:
    return aggregate_synthetic_vcf_qc(
        document,
        fixture_id="tiny-synthetic-cohort",
        data_classification="public_non_patient_synthetic",
        reference=reference or _reference(),
    )


def test_synthetic_vcf_qc_returns_aggregate_only_and_valid_schema() -> None:
    result = _run()
    Draft202012Validator.check_schema(SCHEMA)
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(result)
    assert result["sample_count"] == 3
    assert result["variant_count"] == 2
    assert result["reference_assembly"] == "synthetic-build-v1"
    assert result["reference_sequence_sha256"] == _reference().sequence_sha256
    assert result["coordinate_system"] == "1-based-closed"
    assert result["interpretation_performed"] is False
    assert result["variants"][0]["called_sample_count"] == 2
    assert result["variants"][0]["missing_sample_count"] == 1
    assert result["variants"][0]["heterozygous_sample_count"] == 1
    assert result["variants"][0]["alternate_allele_count"] == 3
    assert result["variants"][1]["alternate_allele_count"] == 3
    assert "samples" not in result
    assert all("genotypes" not in variant for variant in result["variants"])


def test_qc_digest_is_deterministic_and_changes_with_input() -> None:
    first = _run()
    second = _run()
    changed = _run(VCF.replace("60", "61", 1))
    assert first["input_sha256"] == second["input_sha256"]
    assert first["input_sha256"] != changed["input_sha256"]


def test_rejects_non_synthetic_classification_and_bad_fixture_id() -> None:
    with pytest.raises(ValueError, match="Only explicitly synthetic"):
        aggregate_synthetic_vcf_qc(
            VCF, fixture_id="fixture", data_classification="public_non_patient", reference=_reference()
        )
    with pytest.raises(ValueError, match="kebab-case"):
        aggregate_synthetic_vcf_qc(
            VCF, fixture_id="Not Valid", data_classification="public_non_patient_synthetic", reference=_reference()
        )


@pytest.mark.parametrize(
    "document, message",
    [
        (VCF.replace("0/1:99", "0/3:99"), "exceeds ALT count"),
        (VCF.replace("0/1:99", "x/.:99"), "malformed genotype allele index"),
        (VCF.replace("0/1:99", "0/1|1:99"), "mixes phased and unphased"),
        (VCF.replace("GT:GQ", "DP:GQ", 1), "one unique GT field"),
        (VCF.replace("T,G", "<DEL>,G"), "literal A/C/G/T"),
    ],
)
def test_rejects_malformed_or_unsupported_genotypes(document: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _run(document)


def _run_with_limits(*, max_variants: int = 100_000, max_samples: int = 1_000) -> dict:
    return aggregate_synthetic_vcf_qc(
        VCF, fixture_id="tiny-synthetic-cohort",
        data_classification="public_non_patient_synthetic",
        max_variants=max_variants, max_samples=max_samples, reference=_reference(),
    )


def test_enforces_resource_limits_and_requires_sample_columns() -> None:
    with pytest.raises(ValueError, match="max_input_bytes"):
        aggregate_synthetic_vcf_qc(
            VCF,
            fixture_id="tiny-synthetic-cohort",
            data_classification="public_non_patient_synthetic",
            max_input_bytes=10,
            reference=_reference(),
        )
    with pytest.raises(ValueError, match="max_records"):
        _run_with_limits(max_variants=1)
    with pytest.raises(ValueError, match="max_samples"):
        _run_with_limits(max_samples=2)
    for invalid in (0, -1, True, 1.5):
        with pytest.raises(ValueError, match="positive integer"):
            _run_with_limits(max_variants=cast(int, invalid))
    header_only = "\n".join(VCF.splitlines()[:2]) + "\n"
    with pytest.raises(ValueError, match="at least one variant"):
        _run(header_only)
    no_samples = VCF.splitlines()[0] + "\n" + "\t".join(
        VCF.splitlines()[1].split("\t")[:8]
    ) + "\n" + "\t".join(VCF.splitlines()[2].split("\t")[:8])
    with pytest.raises(ValueError, match="at least one sample"):
        _run(no_samples)


def test_partial_missing_genotype_is_counted_as_missing() -> None:
    result = _run(VCF.replace("0/1:99", "0/.:99"))
    assert result["variants"][0]["called_sample_count"] == 1
    assert result["variants"][0]["missing_sample_count"] == 2



@pytest.mark.parametrize("genotype", ["0", "0/1/1", "0/1/2", "0|1|1"])
def test_rejects_unsupported_haploid_and_polyploid_calls(genotype: str) -> None:
    document = VCF.replace("0/1:99", f"{genotype}:99", 1)
    with pytest.raises(ValueError, match="unsupported ploidy"):
        _run(document)



def test_qc_requires_matching_reference_contig_and_ref_alleles() -> None:
    with pytest.raises(ValueError, match="reference contig"):
        _run(VCF.replace("chrSynthetic1", "chrOther"))
    with pytest.raises(ValueError, match="REF does not match"):
        _run(VCF.replace("\tA\tG\t", "\tC\tG\t", 1))
    with pytest.raises(ValueError, match="REF does not match"):
        _run(VCF.replace("\t2\t.\tA\tG\t", "\t99\t.\tA\tG\t", 1))


def test_qc_rejects_reference_digest_tampering() -> None:
    from dataclasses import replace

    with pytest.raises(ValueError, match="SHA-256 does not match"):
        _run(reference=replace(_reference(), sequence_sha256="0" * 64))
