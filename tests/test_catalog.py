from __future__ import annotations

import pytest

from molecularis.catalog import iter_ncbi_gene_info, validate_gene_catalog


def test_ncbi_gene_info_preserves_full_annotation_and_release() -> None:
    row = "\t".join([
        "9606", "7157", "TP53", "-", "P53|BCC7", "MIM:191170|HGNC:11998",
        "17", "17p13.1", "tumor protein p53", "protein-coding", "TP53",
        "tumor protein p53", "Official", "cellular tumor antigen p53",
        "20250101", "gene",
    ])
    gene = next(iter_ncbi_gene_info([row], source_release="NCBI-2025-01"))
    assert gene.gene_id == "7157"
    assert gene.synonyms == ("BCC7", "P53")
    assert gene.dbxrefs == ("HGNC:11998", "MIM:191170")
    assert gene.chromosome == "17"
    assert gene.nomenclature_full_name == "tumor protein p53"
    assert gene.source_release == "NCBI-2025-01"


def test_gene_catalog_rejects_truncated_rows_and_duplicate_ids() -> None:
    with pytest.raises(ValueError, match="16 NCBI columns"):
        list(iter_ncbi_gene_info(["9606\t1\tA"], source_release="release"))
    entries = list(iter_ncbi_gene_info([
        "\t".join([
            "9606", "1", "A", "-", "-", "-", "-", "-",
            "-", "-", "-", "-", "-", "-", "20250101", "gene",
        ]),
        "\t".join([
            "9606", "1", "A2", "-", "-", "-", "-", "-",
            "-", "-", "-", "-", "-", "-", "20250101", "gene",
        ]),
    ], source_release="release"))
    with pytest.raises(ValueError, match="Duplicate"):
        validate_gene_catalog(entries)


def test_catalog_import_cannot_mark_gene_validated() -> None:
    from dataclasses import replace

    entry = next(iter_ncbi_gene_info([
        "\t".join([
            "9606", "1", "A", "-", "-", "-", "-", "-",
            "-", "-", "-", "-", "-", "-", "20250101", "gene",
        ])
    ], source_release="release"))
    with pytest.raises(ValueError, match="cannot confer validated"):
        validate_gene_catalog([replace(entry, evidence_status="validated")])


def test_gene_catalog_searches_synonyms_and_nomenclature_with_taxonomy_filter() -> None:
    from molecularis.catalog import search_gene_catalog

    row = "\t".join([
        "9606", "7157", "TP53", "-", "P53|BCC7", "HGNC:11998", "17",
        "17p13.1", "tumor protein p53", "protein-coding", "TP53",
        "tumor protein p53", "Official", "-", "20250101", "gene",
    ])
    entries = list(iter_ncbi_gene_info([row], source_release="NCBI-2025-01"))
    assert search_gene_catalog(entries, "p53")[0].gene_id == "7157"
    assert search_gene_catalog(entries, "7157", tax_id="10090") == []
    with pytest.raises(ValueError, match="cannot be empty"):
        search_gene_catalog(entries, " ")



def test_pgx_definition_pack_requires_pinned_source_and_matches_only_complete_phase() -> None:
    import json

    from molecularis.pgx import VariantKey, match_phased_haplotype, parse_star_allele_definitions

    pack = {
        "schema_version": 1, "genome_build": "GRCh38",
        "source": {"name": "Reviewed PGx source fixture", "release": "fixture-1",
                   "url": "https://example.org/fixture",
                   "sha256": "a" * 64, "license": "CC-BY-4.0"},
        "definitions": [{
            "id": "CYP2C19-17-def-1", "gene": "CYP2C19", "star_allele": "*17",
            "required_variants": [{
                "chromosome": "10", "position": 94781859, "ref": "C", "alt": "T"
            }],
            "excluded_variants": [],
        }],
    }
    definitions = parse_star_allele_definitions(
        json.dumps(pack), expected_source_release="fixture-1"
    )
    variant = VariantKey("GRCh38", "10", 94781859, "C", "T")
    incomplete = match_phased_haplotype(
        "CYP2C19", [variant], definitions, genome_build="GRCh38", phase_confirmed=True,
    )
    assert incomplete.status == "no_call_incomplete"
    matched = match_phased_haplotype(
        "CYP2C19", [variant], definitions, genome_build="GRCh38",
        phase_confirmed=True, call_complete=True,
    )
    assert matched.status == "matched"
    assert matched.star_allele == "*17"


def test_pgx_definition_pack_rejects_release_mismatch_and_unphased_call() -> None:
    import json

    from molecularis.pgx import match_phased_haplotype, parse_star_allele_definitions

    pack = {
        "schema_version": 1, "genome_build": "GRCh38",
        "source": {
            "name": "fixture", "release": "v1", "url": "https://example.org",
            "sha256": "b" * 64, "license": "MIT",
        },
        "definitions": [{"id": "d1", "gene": "GENE1", "star_allele": "*1",
                         "required_variants": [], "excluded_variants": []}],
    }
    with pytest.raises(ValueError, match="pinned release"):
        parse_star_allele_definitions(json.dumps(pack), expected_source_release="v2")
    definitions = parse_star_allele_definitions(json.dumps(pack), expected_source_release="v1")
    result = match_phased_haplotype(
        "GENE1", [], definitions, genome_build="GRCh38", phase_confirmed=False,
        call_complete=True,
    )
    assert result.status == "no_call_unphased"



def test_pharmvar_tsv_import_is_release_and_checksum_pinned() -> None:
    import hashlib

    from molecularis.pharmvar import match_pharmvar_haplotype, parse_pharmvar_tsv

    tsv = (
        "Haplotype Name\tGene Symbol\tdbSNP rsID\tReference Sequence\tVariant Start\t"
        "Variant Stop\tReference Allele\tVariant Allele\tVariant Type\n"
        "CYP2C19*17\tCYP2C19\trs12248560\tNG_008384.3\t991\t991\tC\tT\tsubstitution\n"
        "CYP2C19*1\tCYP2C19\t.\tNG_008384.3\t.\t.\tREFERENCE\t.\treference\n"
    )
    digest = hashlib.sha256(tsv.encode("utf-8")).hexdigest()
    definitions = parse_pharmvar_tsv(
        tsv, source_release="6.2.29", expected_release="6.2.29",
        source_url="https://www.pharmvar.org/download", source_sha256=digest,
        license_id="CC-BY-SA-4.0",
    )
    assert len(definitions) == 2
    allele_17 = next(item for item in definitions if item.haplotype == "CYP2C19*17")
    variant = next(iter(allele_17.variants))
    match = match_pharmvar_haplotype(
        "CYP2C19", "NG_008384.3", [variant], definitions,
        phase_confirmed=True, call_complete=True,
    )
    assert match.status == "matched"
    assert match.haplotype == "CYP2C19*17"


def test_pharmvar_tsv_rejects_checksum_and_incomplete_phase() -> None:
    from molecularis.pharmvar import parse_pharmvar_tsv

    tsv = (
        "Haplotype Name\tGene Symbol\tdbSNP rsID\tReference Sequence\tVariant Start\t"
        "Variant Stop\tReference Allele\tVariant Allele\tVariant Type\n"
        "GENE*1\tGENE\t.\tNG_000001.1\t.\t.\tREFERENCE\t.\treference\n"
    )
    with pytest.raises(ValueError, match="SHA-256"):
        parse_pharmvar_tsv(
            tsv, source_release="6.2.29", expected_release="6.2.29",
            source_url="https://www.pharmvar.org/download", source_sha256="0" * 64,
            license_id="CC-BY-SA-4.0",
        )


def test_gene_catalogue_coverage_report_is_descriptive_and_has_no_fake_denominator() -> None:
    from molecularis.catalog import gene_catalogue_coverage_report

    rows = [
        "\t".join([
            "9606", "1", "GENE1", "-", "-", "-", "1", "1p", "description",
            "protein-coding", "GENE1", "Gene one", "Official", "-", "20250101", "gene",
        ]),
        "\t".join([
            "10090", "2", "GENE2", "-", "-", "-", "-", "-", "-", "ncRNA",
            "-", "-", "-", "-", "20250101", "gene",
        ]),
    ]
    entries = list(iter_ncbi_gene_info(rows, source_release="fixture-1"))
    report = gene_catalogue_coverage_report(entries)
    assert report["entry_count"] == 2
    assert report["taxonomy_counts"] == {"10090": 1, "9606": 1}
    assert report["gene_type_counts"] == {"ncRNA": 1, "protein-coding": 1}
    assert report["coverage_percentage"] is None
    assert report["coverage_denominator"] is None
    assert report["scope"] == "supplied_catalogue_snapshot_only"


def test_gene_catalogue_coverage_report_enforces_bounds() -> None:
    from molecularis.catalog import gene_catalogue_coverage_report

    entry = next(iter_ncbi_gene_info([
        "\t".join([
            "9606", "1", "A", "-", "-", "-", "-", "-",
            "-", "-", "-", "-", "-", "-", "20250101", "gene",
        ])
    ], source_release="fixture"))
    with pytest.raises(ValueError, match="max_entries"):
        gene_catalogue_coverage_report([entry, entry], max_entries=1)



def test_pharmvar_tsv_rejects_duplicate_normalized_headers() -> None:
    import hashlib
    from molecularis.pharmvar import parse_pharmvar_tsv

    tsv = (
        "Haplotype Name\tGene Symbol\tGene-Symbol\tReference Sequence\tVariant Start\t"
        "Variant Stop\tReference Allele\tVariant Allele\tVariant Type\n"
        "GENE*1\tGENE\tGENE\tNG_000001.1\t.\t.\tREFERENCE\t.\treference\n"
    )
    with pytest.raises(ValueError, match="duplicate column"):
        parse_pharmvar_tsv(
            tsv, source_release="fixture-1", expected_release="fixture-1",
            source_url="https://example.org/download",
            source_sha256=hashlib.sha256(tsv.encode()).hexdigest(), license_id="CC0-1.0",
        )


def test_pharmvar_tsv_rejects_short_and_extra_field_rows() -> None:
    import hashlib
    from molecularis.pharmvar import parse_pharmvar_tsv

    header = (
        "Haplotype Name\tGene Symbol\tdbSNP rsID\tReference Sequence\tVariant Start\t"
        "Variant Stop\tReference Allele\tVariant Allele\tVariant Type\n"
    )
    for row in (
        "GENE*1\tGENE\t.\tNG_000001.1\t.\t.\tREFERENCE\t.\n",
        "GENE*1\tGENE\t.\tNG_000001.1\t.\t.\tREFERENCE\t.\treference\textra\n",
    ):
        tsv = header + row
        with pytest.raises(ValueError, match="exactly nine fields"):
            parse_pharmvar_tsv(
                tsv, source_release="fixture-1", expected_release="fixture-1",
                source_url="https://example.org/download",
                source_sha256=hashlib.sha256(tsv.encode()).hexdigest(), license_id="CC0-1.0",
            )


def test_pharmvar_exact_match_reports_ambiguous_definitions_without_order_bias() -> None:
    import hashlib
    from molecularis.pharmvar import match_pharmvar_haplotype, parse_pharmvar_tsv

    tsv = (
        "Haplotype Name\tGene Symbol\tdbSNP rsID\tReference Sequence\tVariant Start\t"
        "Variant Stop\tReference Allele\tVariant Allele\tVariant Type\n"
        "GENE*2\tGENE\trs1\tNG_000001.1\t10\t10\tA\tG\tsubstitution\n"
        "GENE*3\tGENE\trs1\tNG_000001.1\t10\t10\tA\tG\tsubstitution\n"
    )
    definitions = parse_pharmvar_tsv(
        tsv, source_release="fixture-1", expected_release="fixture-1",
        source_url="https://example.org/download",
        source_sha256=hashlib.sha256(tsv.encode()).hexdigest(), license_id="CC0-1.0",
    )
    observed = next(iter(definitions[0].variants))
    result = match_pharmvar_haplotype(
        "GENE", "NG_000001.1", [observed], definitions,
        phase_confirmed=True, call_complete=True,
    )
    assert result.status == "ambiguous"
    assert result.haplotype is None
    assert result.matched_haplotypes == ("GENE*2", "GENE*3")


def test_pharmvar_matching_requires_complete_phase_and_matching_accession() -> None:
    import hashlib
    from molecularis.pharmvar import match_pharmvar_haplotype, parse_pharmvar_tsv

    tsv = (
        "Haplotype Name\tGene Symbol\tdbSNP rsID\tReference Sequence\tVariant Start\t"
        "Variant Stop\tReference Allele\tVariant Allele\tVariant Type\n"
        "GENE*2\tGENE\trs1\tNG_000001.1\t10\t10\tA\tG\tsubstitution\n"
    )
    definitions = parse_pharmvar_tsv(
        tsv, source_release="fixture-1", expected_release="fixture-1",
        source_url="https://example.org/download",
        source_sha256=hashlib.sha256(tsv.encode()).hexdigest(), license_id="CC0-1.0",
    )
    observed = next(iter(definitions[0].variants))
    unphased = match_pharmvar_haplotype(
        "GENE", "NG_000001.1", [observed], definitions,
        phase_confirmed=False, call_complete=True,
    )
    incomplete = match_pharmvar_haplotype(
        "GENE", "NG_000001.1", [observed], definitions,
        phase_confirmed=True, call_complete=False,
    )
    assert unphased.status == "no_call_unphased"
    assert incomplete.status == "no_call_incomplete"
    with pytest.raises(ValueError, match="different reference accession"):
        match_pharmvar_haplotype(
            "GENE", "NG_000002.1", [observed], definitions,
            phase_confirmed=True, call_complete=True,
        )



def test_gene_info_rejects_extra_columns_instead_of_silently_ignoring_them() -> None:
    row = "\t".join([
        "9606", "1", "GENE1", "-", "-", "-", "-", "-", "description",
        "protein-coding", "GENE1", "Gene one", "Official", "-", "20250101", "gene",
        "unexpected-extra",
    ])
    with pytest.raises(ValueError, match="exactly 16"):
        list(iter_ncbi_gene_info([row], source_release="fixture-1"))


def test_gene_info_rejects_impossible_calendar_modification_date() -> None:
    row = "\t".join([
        "9606", "1", "GENE1", "-", "-", "-", "-", "-", "description",
        "protein-coding", "GENE1", "Gene one", "Official", "-", "20250230", "gene",
    ])
    with pytest.raises(ValueError, match="invalid modification date"):
        list(iter_ncbi_gene_info([row], source_release="fixture-1"))
