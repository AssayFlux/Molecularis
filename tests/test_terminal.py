"""Tests for the Molecularis Terminal command workbench."""
from __future__ import annotations

import json

from molecularis.cli import _capability_dict, _json_value, build_parser
from molecularis.bootstrap import create_full_platform


def test_cli_parser_exposes_core_commands() -> None:
    parser = build_parser()
    args = parser.parse_args(["doctor"])
    assert args.command == "doctor"
    args = parser.parse_args(["run", "sequence.analyze.v1", "--input", '{"sequence":"ATGC"}'])
    assert args.command == "run"
    assert args.capability_id == "sequence.analyze.v1"


def test_json_input_supports_inline_and_file(tmp_path) -> None:
    assert _json_value('{"x": 3}', label="input") == {"x": 3}
    source = tmp_path / "input.json"
    source.write_text('{"y": 4}', encoding="utf-8")
    assert _json_value("@" + str(source), label="input") == {"y": 4}


def test_bootstrap_inventory_reports_bound_handlers(tmp_path) -> None:
    platform = create_full_platform(str(tmp_path / "workspace"))
    try:
        capabilities = platform.registry.list()
        assert len(capabilities) >= 50
        assert len({cap.service for cap in capabilities}) == 14
        assert all(platform.has_handler(cap.id) for cap in capabilities)
        first = capabilities[0]
        details = _capability_dict(first, platform)
        assert details["handler_bound"] is True
        assert details["input_schema"] == first.input_schema
    finally:
        platform.close()
