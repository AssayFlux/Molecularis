from __future__ import annotations

import pytest

from molecularis.scientific_engines import (
    ENGINE_SPECS,
    align_with_parasail,
    discover_engine,
    engine_inventory,
)


def test_inventory_contains_all_18_requested_engines() -> None:
    inventory = engine_inventory()
    assert len(inventory) == 18
    assert len({item["engine_id"] for item in inventory}) == 18


def test_discovery_is_explicitly_not_scientific_validation() -> None:
    result = discover_engine("scipy")
    assert result["engine_id"] == "scipy"
    assert result["discovery_only"] is True
    assert result["scientific_validation"] == "not_assessed"


def test_unknown_engine_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown engine_id"):
        discover_engine("not-an-engine")


def test_parasail_bounds_and_alphabet_are_checked_before_import() -> None:
    with pytest.raises(ValueError, match="symbols"):
        align_with_parasail("ACGTZ", "ACGT")
    with pytest.raises(ValueError, match="max_alignment_cells"):
        align_with_parasail("A" * 100, "A" * 100, max_alignment_cells=10)


def test_parasail_adapter_returns_molecularis_owned_result() -> None:
    pytest.importorskip("parasail")
    result = align_with_parasail("ACGT", "ACCT")
    assert result["engine"] == "parasail"
    assert result["algorithm"] == "needleman-wunsch"
    assert isinstance(result["traceback"], dict)
