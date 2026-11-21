from __future__ import annotations

import pytest

from molecularis.genetic_code import GENETIC_CODES, translate_coding_sequence


def test_standard_table_translation_and_cds_validation() -> None:
    result = translate_coding_sequence("ATG AAA TAA", cds=True)
    assert result["protein"] == "MK"
    assert result["table_id"] == 1
    assert result["cds_validation"] == "passed"
    assert result["terminal_stop_codon"] == "TAA"


@pytest.mark.parametrize(
    "table_id, sequence, expected",
    [
        (2, "ATA TGA AGA", "MW*"),
        (4, "ATG TGA TAA", "MW*"),
        (5, "ATG AGA TAG", "MS*"),
        (11, "GTG AAA TAA", "VK*"),
    ],
)
def test_explicit_alternative_translation_tables(
    table_id: int, sequence: str, expected: str,
) -> None:
    result = translate_coding_sequence(sequence, table_id=table_id)
    assert result["protein"] == expected
    assert result["table_id"] == table_id
    assert any("no genetic-code inference" in warning for warning in result["warnings"])


def test_alternative_start_is_methionine_only_in_cds_mode() -> None:
    ordinary = translate_coding_sequence("GTGAAATAA", table_id=11)
    cds = translate_coding_sequence("GTGAAATAA", table_id=11, cds=True)
    assert ordinary["protein"] == "VK*"
    assert cds["protein"] == "MK"


def test_translation_rejects_invalid_table_frame_ambiguous_and_partial_codons() -> None:
    with pytest.raises(ValueError, match="Unsupported NCBI"):
        translate_coding_sequence("ATG", table_id=99)
    with pytest.raises(ValueError, match="frame"):
        translate_coding_sequence("ATG", frame=True)
    with pytest.raises(ValueError, match="unambiguous"):
        translate_coding_sequence("ATGN")
    with pytest.raises(ValueError, match="not divisible"):
        translate_coding_sequence("ATGA")


def test_translation_can_explicitly_trim_trailing_partial_codon() -> None:
    result = translate_coding_sequence("ATGAA", trim_partial_codon=True)
    assert result["protein"] == "M"
    assert result["trimmed_trailing_bases"] == 2


def test_cds_rejects_invalid_start_stop_and_internal_stop() -> None:
    with pytest.raises(ValueError, match="start codon"):
        translate_coding_sequence("AAA TAA", cds=True)
    with pytest.raises(ValueError, match="terminal codon"):
        translate_coding_sequence("ATG AAA", cds=True)
    with pytest.raises(ValueError, match="internal"):
        translate_coding_sequence("ATG TAA AAA TAA", cds=True)


def test_genetic_code_table_ids_are_explicit_and_limited() -> None:
    assert set(GENETIC_CODES) == {
        1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16,
        21, 22, 23, 24, 25, 26, 29, 30, 32, 33,
    }


@pytest.mark.parametrize("table_id", [True, 1.0, "1"])
def test_translation_rejects_non_integer_or_boolean_table_ids(table_id: object) -> None:
    with pytest.raises(ValueError, match="Unsupported NCBI"):
        translate_coding_sequence("ATG", table_id=table_id)



@pytest.mark.parametrize(
    "table_id, sequence, expected",
    [
        (3, "ATA TGA CTT", "MWT"),
        (6, "TAA TAG TGA", "QQ*"),
        (9, "AAA AGA AGG", "NSS"),
        (10, "TGA TAA", "C*"),
        (12, "CTG TAA", "S*"),
        (13, "AGA AGG TGA", "GGW"),
        (14, "TAA AAA TGA", "YNW"),
        (15, "TAG TAA", "Q*"),
        (16, "TAG TAA", "L*"),
        (21, "ATA AAA AGA", "MNS"),
        (22, "TAG TCA TAA", "L**"),
        (23, "TTA TAA", "**"),
        (24, "AGA AGG TGA", "SKW"),
        (25, "TGA TAA", "G*"),
        (26, "CTG TAA", "A*"),
        (29, "TAA TAG TGA", "YY*"),
        (30, "TAA TAG TGA", "EE*"),
        (32, "TAG TAA TGA", "W**"),
        (33, "TAA TGA TAG", "YW*"),
    ],
)
def test_extended_explicit_ncbi_tables(
    table_id: int, sequence: str, expected: str,
) -> None:
    result = translate_coding_sequence(sequence, table_id=table_id)
    assert result["protein"] == expected
    assert result["table_id"] == table_id
