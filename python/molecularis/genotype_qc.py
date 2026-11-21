"""Aggregate QC for explicitly synthetic VCF fixtures.

This module intentionally emits cohort-level summaries only and rejects any input
not explicitly classified as public_non_patient_synthetic. It is not a patient-data
ingestion or clinical interpretation interface.
"""
from __future__ import annotations

import re
from hashlib import sha256
from statistics import fmean
from typing import Any

from .genomics import parse_vcf
from .variant_reference import ReferenceSequence

_FIXTURE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_LITERAL_ALLELE = re.compile(r"^[ACGT]+$")


def _positive_limit(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _parse_genotype(
    value: str, *, alternate_count: int, line_number: int,
) -> tuple[tuple[int, ...] | None, bool]:
    """Return called allele indexes and phase flag; partial calls count as missing."""
    if value == ".":
        return None, False
    if "/" in value and "|" in value:
        raise ValueError(f"VCF line {line_number}: genotype mixes phased and unphased separators")
    separator = "|" if "|" in value else "/" if "/" in value else None
    alleles = value.split(separator) if separator else [value]
    # P1 deliberately supports diploid fixtures only. Haploid/polyploid calls
    # need an explicit chromosome/ploidy contract and must not be guessed.
    if len(alleles) != 2:
        raise ValueError(f"VCF line {line_number}: unsupported ploidy; diploid genotypes only")
    missing = any(item == "." for item in alleles)
    called_tokens = [item for item in alleles if item != "."]
    if any(not re.fullmatch(r"(?:0|[1-9][0-9]*)", item) for item in called_tokens):
        raise ValueError(f"VCF line {line_number}: malformed genotype allele index")
    indexes = tuple(int(item) for item in called_tokens)
    if any(index > alternate_count for index in indexes):
        raise ValueError(f"VCF line {line_number}: genotype allele index exceeds ALT count")
    if missing:
        return None, separator == "|"
    return indexes, separator == "|"


def aggregate_synthetic_vcf_qc(
    document: str,
    *,
    fixture_id: str,
    data_classification: str,
    reference: ReferenceSequence,
    max_input_bytes: int = 10 * 1024 * 1024,
    max_variants: int = 100_000,
    max_samples: int = 1_000,
) -> dict[str, Any]:
    """Return aggregate QC for a caller-asserted synthetic fixture only.

    The classification argument is not a patient-data detector or privacy filter.
    Callers must only supply generated synthetic fixtures through this API.
    """
    if data_classification != "public_non_patient_synthetic":
        raise ValueError("Only explicitly synthetic non-patient VCF fixtures are accepted")
    if not isinstance(fixture_id, str) or not _FIXTURE_ID.fullmatch(fixture_id):
        raise ValueError("fixture_id must be a lowercase kebab-case identifier")
    if not isinstance(reference, ReferenceSequence):
        raise TypeError("reference must be a verified ReferenceSequence")
    reference.validate()
    _positive_limit("max_input_bytes", max_input_bytes)
    _positive_limit("max_variants", max_variants)
    _positive_limit("max_samples", max_samples)
    if not isinstance(document, str):
        raise TypeError("VCF document must be text")
    raw = document.encode("utf-8")
    if len(raw) > max_input_bytes:
        raise ValueError("VCF input exceeds configured max_input_bytes")

    records = parse_vcf(document, max_records=max_variants, max_samples=max_samples)
    if not records:
        raise ValueError("Synthetic VCF must contain at least one variant record")
    if len(records) > max_variants:
        raise ValueError("VCF variant count exceeds configured max_variants")
    sample_names = records[0].get("samples")
    if not isinstance(sample_names, list) or not sample_names:
        raise ValueError("Synthetic VCF must contain at least one sample column")
    if len(sample_names) > max_samples:
        raise ValueError("VCF sample count exceeds configured max_samples")

    variant_results: list[dict[str, Any]] = []
    call_rates: list[float] = []
    for index, record in enumerate(records, start=1):
        if record.get("samples") != sample_names:
            raise ValueError("VCF sample columns changed between records")
        ref = record.get("ref")
        alt = record.get("alt")
        if not isinstance(ref, str) or not _LITERAL_ALLELE.fullmatch(ref.upper()):
            raise ValueError(f"VCF variant {index}: REF must be a literal A/C/G/T allele")
        if not isinstance(alt, str):
            raise ValueError(f"VCF variant {index}: ALT must be text")
        alternate_alleles = alt.split(",")
        if (
            not alternate_alleles
            or any(not _LITERAL_ALLELE.fullmatch(item.upper()) for item in alternate_alleles)
            or len({item.upper() for item in alternate_alleles}) != len(alternate_alleles)
            or ref.upper() in {item.upper() for item in alternate_alleles}
        ):
            raise ValueError(f"VCF variant {index}: ALT must contain distinct literal A/C/G/T alleles")
        format_value = record.get("format")
        if not isinstance(format_value, str) or not format_value:
            raise ValueError(f"VCF variant {index}: FORMAT is required")
        format_fields = format_value.split(":")
        if len(set(format_fields)) != len(format_fields) or "GT" not in format_fields:
            raise ValueError(f"VCF variant {index}: FORMAT must contain one unique GT field")
        gt_index = format_fields.index("GT")
        genotype_values = record.get("genotypes")
        if not isinstance(genotype_values, list) or len(genotype_values) != len(sample_names):
            raise ValueError(f"VCF variant {index}: sample genotype count does not match header")

        called = 0
        missing = 0
        heterozygous = 0
        alternate_count = 0
        total_alleles = 0
        phased = 0
        for sample_value in genotype_values:
            if not isinstance(sample_value, str):
                raise ValueError(f"VCF variant {index}: sample value must be text")
            sample_fields = sample_value.split(":")
            if len(sample_fields) != len(format_fields):
                raise ValueError(f"VCF variant {index}: sample FORMAT field count mismatch")
            genotype, is_phased = _parse_genotype(
                sample_fields[gt_index],
                alternate_count=len(alternate_alleles),
                line_number=index,
            )
            if genotype is None:
                missing += 1
                continue
            called += 1
            total_alleles += len(genotype)
            alternate_count += sum(allele > 0 for allele in genotype)
            heterozygous += len(set(genotype)) > 1
            phased += is_phased

        call_rate = called / len(sample_names)
        call_rates.append(call_rate)
        chrom_value = record.get("chrom")
        pos_value = record.get("pos")
        if not isinstance(chrom_value, str) or not chrom_value:
            raise ValueError(f"VCF variant {index}: chromosome must be non-empty text")
        if isinstance(pos_value, bool) or not isinstance(pos_value, int) or pos_value < 1:
            raise ValueError(f"VCF variant {index}: position must be a positive integer")
        if chrom_value != reference.contig:
            raise ValueError(f"VCF variant {index}: chromosome does not match reference contig")
        reference_start = pos_value - 1
        if reference.sequence[reference_start:reference_start + len(ref)] != ref.upper():
            raise ValueError(f"VCF variant {index}: REF does not match the pinned reference sequence")
        variant_results.append({
            "chrom": chrom_value,
            "pos": pos_value,
            "ref": ref.upper(),
            "alt": ",".join(item.upper() for item in alternate_alleles),
            "sample_count": len(sample_names),
            "called_sample_count": called,
            "missing_sample_count": missing,
            "call_rate": call_rate,
            "heterozygous_sample_count": heterozygous,
            "alternate_allele_count": alternate_count,
            "total_called_allele_count": total_alleles,
            "phased_sample_count": phased,
        })

    return {
        "schema_version": 1,
        "data_classification": "public_non_patient_synthetic",
        "fixture_id": fixture_id,
        "input_sha256": sha256(raw).hexdigest(),
        "reference_assembly": reference.assembly,
        "reference_accession": reference.accession,
        "reference_release": reference.release,
        "reference_contig": reference.contig,
        "reference_sequence_sha256": reference.sequence_sha256,
        "reference_retrieved_at": reference.retrieved_at,
        "coordinate_system": reference.coordinate_system,
        "interpretation_performed": False,
        "sample_count": len(sample_names),
        "variant_count": len(variant_results),
        "mean_variant_call_rate": fmean(call_rates),
        "variants": variant_results,
    }
