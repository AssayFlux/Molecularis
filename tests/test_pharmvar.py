from __future__ import annotations

import hashlib
from typing import cast

import pytest

from molecularis.pharmvar import match_pharmvar_haplotype, parse_pharmvar_tsv

TSV = (
    "Haplotype Identifier\tGene Symbol\tdbSNP rsID\tReference Sequence\t"
    "Variant Start\tVariant Stop\tReference Allele\tVariant Allele\t"
    "Variant Type\n"
    "*1\tSYN1\t.\tNG_SYNTHETIC.1\t0\t0\tREFERENCE\t.\treference\n"
    "*2\tSYN1\trsSynthetic1\tNG_SYNTHETIC.1\t2\t2\tA\tG\tsnv\n"
)


def defs():
    return parse_pharmvar_tsv(
        TSV,
        source_release="fixture-1",
        source_url="https://example.invalid/source",
        source_sha256=hashlib.sha256(TSV.encode()).hexdigest(),
        license_id="CC0 synthetic test only",
        expected_release="fixture-1",
    )


def test_pharmvar_exact_byte_digest_and_accession_preservation():
    definitions = defs()
    assert len(definitions) == 2 and definitions[0].is_reference
    assert next(iter(definitions[1].variants)).reference_accession == "NG_SYNTHETIC.1"


def test_pharmvar_exact_haplotype_match_and_unphased_abstention():
    definitions = defs()
    variant = next(iter(definitions[1].variants))
    matched = match_pharmvar_haplotype(
        "SYN1",
        "NG_SYNTHETIC.1",
        [variant],
        definitions,
        phase_confirmed=True,
        call_complete=True,
    )
    assert matched.status == "matched" and matched.haplotype == "*2"
    unphased = match_pharmvar_haplotype(
        "SYN1",
        "NG_SYNTHETIC.1",
        [variant],
        definitions,
        phase_confirmed=False,
        call_complete=True,
    )
    assert unphased.status == "no_call_unphased" and unphased.haplotype is None


def test_pharmvar_rejects_digest_release_and_accession_mismatch():
    digest = hashlib.sha256(TSV.encode()).hexdigest()
    with pytest.raises(ValueError, match="checksum"):
        parse_pharmvar_tsv(
            TSV,
            source_release="fixture-1",
            source_url="https://example.invalid/source",
            source_sha256="0" * 64,
            license_id="test",
            expected_release="fixture-1",
        )
    with pytest.raises(ValueError, match="release"):
        parse_pharmvar_tsv(
            TSV,
            source_release="fixture-1",
            source_url="https://example.invalid/source",
            source_sha256=digest,
            license_id="test",
            expected_release="fixture-2",
        )
    with pytest.raises(ValueError, match="different reference accession"):
        match_pharmvar_haplotype(
            "SYN1",
            "OTHER",
            [next(iter(defs()[1].variants))],
            defs(),
            phase_confirmed=True,
            call_complete=True,
        )


def test_pharmvar_parser_enforces_input_and_row_bounds():
    digest = hashlib.sha256(TSV.encode()).hexdigest()
    common = {
        "source_release": "fixture-1",
        "source_url": "https://example.invalid/source",
        "source_sha256": digest,
        "license_id": "CC0 synthetic test only",
        "expected_release": "fixture-1",
    }
    with pytest.raises(ValueError, match="max_input_bytes"):
        parse_pharmvar_tsv(TSV, **common, max_input_bytes=1)
    with pytest.raises(ValueError, match="max_rows"):
        parse_pharmvar_tsv(TSV, **common, max_rows=1)
    for invalid in (0, -1, True, 1.5):
        with pytest.raises(ValueError, match="positive integer"):
            parse_pharmvar_tsv(TSV, **common, max_rows=cast(int, invalid))


def test_pharmvar_parser_rejects_non_text_input():
    with pytest.raises(TypeError, match="text or bytes"):
        parse_pharmvar_tsv(
            cast(str, None),
            source_release="fixture-1",
            source_url="https://example.invalid/source",
            source_sha256=hashlib.sha256(TSV.encode()).hexdigest(),
            license_id="CC0 synthetic test only",
            expected_release="fixture-1",
        )



@pytest.mark.parametrize(("start", "stop"), [(True, 1), (1, False)])
def test_pharmvar_variant_rejects_boolean_coordinates(start, stop):
    from molecularis.pharmvar import PharmVarVariant

    with pytest.raises(ValueError, match="coordinates must be integers"):
        PharmVarVariant(
            "NG_SYNTHETIC.1", start, stop, "A", "G", "snv"
        )
