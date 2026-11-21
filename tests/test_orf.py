from __future__ import annotations

import pytest

from molecularis.orf import find_orf_candidates


def test_orf_scan_finds_forward_complete_cds_with_explicit_coordinates() -> None:
    result = find_orf_candidates("ATGAAATAA", table_id=1, min_protein_length=1)
    assert result["orf_count"] == 1
    orf = result["orfs"][0]
    assert (orf["start"], orf["end"], orf["strand"], orf["frame"]) == (0, 9, "+", 0)
    assert (orf["protein"], orf["start_codon"], orf["stop_codon"]) == ("MK", "ATG", "TAA")


def test_orf_scan_retains_nested_starts() -> None:
    result = find_orf_candidates("ATGATGTAA", table_id=1, min_protein_length=1)
    assert [(item["start"], item["protein"]) for item in result["orfs"]] == [
        (0, "MM"), (3, "M"),
    ]


def test_orf_scan_maps_reverse_strand_coordinates_to_input() -> None:
    result = find_orf_candidates("TTATTTCAT", table_id=1, min_protein_length=1)
    reverse = [item for item in result["orfs"] if item["strand"] == "-"]
    assert len(reverse) == 1
    assert (reverse[0]["start"], reverse[0]["end"], reverse[0]["protein"]) == (0, 9, "MK")


def test_orf_scan_uses_selected_code_for_stop_and_translation() -> None:
    sequence = "ATGTGAAAATAG"
    standard = find_orf_candidates(sequence, table_id=1, min_protein_length=1)
    mitochondrial = find_orf_candidates(sequence, table_id=2, min_protein_length=1)
    standard_hits = [item for item in standard["orfs"] if item["strand"] == "+"]
    mito_hits = [item for item in mitochondrial["orfs"] if item["strand"] == "+"]
    assert any(item["protein"] == "M" and item["end"] == 6 for item in standard_hits)
    assert any(item["protein"] == "MWK" and item["end"] == 12 for item in mito_hits)


def test_orf_scan_enforces_limits_and_rejects_ambiguous_sequence() -> None:
    with pytest.raises(ValueError, match="unambiguous"):
        find_orf_candidates("ATGNNNTAA", min_protein_length=1)
    with pytest.raises(ValueError, match="max_orfs"):
        find_orf_candidates("ATGATGTAA", min_protein_length=1, max_orfs=1)
    with pytest.raises(ValueError, match="positive integer"):
        find_orf_candidates("ATGAAATAA", min_protein_length=0)
    with pytest.raises(ValueError, match="max_sequence_bases"):
        find_orf_candidates("ATGAAATAA", max_sequence_bases=8)
    with pytest.raises(ValueError, match="max_open_starts"):
        find_orf_candidates("ATGATG", max_open_starts=1)
    with pytest.raises(ValueError, match="positive integer"):
        find_orf_candidates("ATG", max_open_starts=0)


@pytest.mark.parametrize("table_id", [True, 11.0, "11"])
def test_orf_scan_rejects_non_integer_or_boolean_table_ids(table_id: object) -> None:
    with pytest.raises(ValueError, match="Unsupported NCBI"):
        find_orf_candidates("ATGAAATAA", table_id=table_id)



def test_orf_scan_enforces_total_candidate_pair_work_ceiling(monkeypatch: pytest.MonkeyPatch) -> None:
    # Lower the module ceiling so the boundary is exercised without a million translations.
    import molecularis.orf as orf_module

    monkeypatch.setattr(orf_module, "MAX_CANDIDATE_ORF_PAIRS", 1)
    with pytest.raises(ValueError, match="candidate work exceeds"):
        find_orf_candidates("ATGATGTAA", min_protein_length=1)
