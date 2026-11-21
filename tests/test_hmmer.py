from __future__ import annotations

import pytest

from molecularis.hmmer import parse_hmmscan_domtblout


PACK = {
    "name": "synthetic-profile-pack",
    "version": "1",
    "license": "CC0-1.0",
    "source": "https://example.org/profiles",
    "content_sha256": "a" * 64,
}

# target name/accession/tlen, query name/accession/qlen, full E/score/bias,
# domain #/of, c-E/i-E, domain score/bias, HMM, alignment, envelope coords, acc.
ROW = (
    "PF00001 PF00001.1 100 query-1 - 80 1e-20 72.5 0.1 1 1 "
    "1e-18 1e-18 70.0 0.0 5 75 3 73 2 75 0.98 kinase-like domain"
)


def test_domtblout_parser_preserves_profile_statistics_and_coordinates() -> None:
    result = parse_hmmscan_domtblout(
        ["# HMMER output\n", ROW + "\n"],
        hmmer_version="3.4",
        profile_pack=PACK,
    )
    hit = result["hits"][0]
    assert hit["profile_id"] == "PF00001"
    assert hit["query_id"] == "query-1"
    assert hit["independent_evalue"] == pytest.approx(1e-18)
    assert hit["alignment_start_1based"] == 3
    assert hit["description"] == "kinase-like domain"
    assert result["conclusion"]["function"] == "not_inferred"


def test_domtblout_empty_result_does_not_claim_novelty() -> None:
    result = parse_hmmscan_domtblout(
        ["# no hits\n"], hmmer_version="3.4", profile_pack=PACK,
    )
    assert result["domain_hit_count"] == 0
    assert result["conclusion"]["novelty"] == "not_established"


@pytest.mark.parametrize("row", [
    "short row",
    ROW.replace("1e-20", "NaN"),
    ROW.replace("5 75 3 73 2 75", "101 75 3 73 2 75"),
    ROW.replace("0.98", "1.5"),
    ROW.replace("3 73", "3 81"),
])
def test_domtblout_rejects_malformed_or_inconsistent_rows(row: str) -> None:
    with pytest.raises(ValueError):
        parse_hmmscan_domtblout([row], hmmer_version="3.4", profile_pack=PACK)


def test_domtblout_resource_limits_and_metadata_are_strict() -> None:
    with pytest.raises(ValueError, match="max_domains"):
        parse_hmmscan_domtblout(
            [ROW, ROW], hmmer_version="3.4", profile_pack=PACK, max_domains=1,
        )
    with pytest.raises(ValueError, match="max_lines"):
        parse_hmmscan_domtblout(
            ["# one\n", "# two\n"], hmmer_version="3.4", profile_pack=PACK, max_lines=1,
        )
    with pytest.raises(ValueError, match="content_sha256"):
        parse_hmmscan_domtblout(
            [], hmmer_version="3.4", profile_pack={**PACK, "content_sha256": "bad"},
        )



def test_domtblout_rejects_inconsistent_domain_group_counts_and_duplicate_indices() -> None:
    second_domain = ROW.replace("1 1 1e-18", "2 2 1e-18")
    mismatched_count = ROW + "\n" + second_domain.replace("2 2 1e-18", "2 3 1e-18")
    with pytest.raises(ValueError, match="inconsistent domain indices"):
        parse_hmmscan_domtblout(
            mismatched_count.splitlines(), hmmer_version="3.4", profile_pack=PACK,
        )
    duplicate = ROW + "\n" + ROW
    with pytest.raises(ValueError, match="inconsistent domain indices"):
        parse_hmmscan_domtblout(
            duplicate.splitlines(), hmmer_version="3.4", profile_pack=PACK,
        )
