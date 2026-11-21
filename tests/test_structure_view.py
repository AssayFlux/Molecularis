from __future__ import annotations

import copy
import json

import pytest

from molecularis.structure import Atom
from molecularis.structure_view import (
    PAYLOAD_SCHEMA,
    build_preparation_record,
    build_structure_session_export,
    prepare_viewer_payload,
    serialize_viewer_payload,
)


def atom(serial: int = 1, x: float = 1.0) -> Atom:
    return Atom(serial, "CA", "ALA", "A", 1, x, 2.0, 3.0, "C")


def test_viewer_payload_is_deterministic_and_explicit_about_limits() -> None:
    payload = prepare_viewer_payload([atom()], source_format="PDB")
    assert payload["schema"] == PAYLOAD_SCHEMA
    assert payload["coordinate_unit"] == "angstrom"
    assert payload["atom_count"] == 1
    assert payload["atoms"][0]["xyz"] == [1.0, 2.0, 3.0]
    assert "no inferred bonds" in payload["limitations"][0]
    encoded = serialize_viewer_payload(payload)
    assert encoded == serialize_viewer_payload(payload)
    assert json.loads(encoded) == payload


def test_viewer_payload_rejects_empty_or_unsupported_inputs() -> None:
    with pytest.raises(ValueError, match="empty"):
        prepare_viewer_payload([], source_format="pdb")
    with pytest.raises(ValueError, match="source_format"):
        prepare_viewer_payload([atom()], source_format="xyz")


def test_viewer_payload_enforces_atom_limit_and_unique_serials() -> None:
    with pytest.raises(ValueError, match="atom limit"):
        prepare_viewer_payload([atom(1), atom(2)], source_format="pdb", max_atoms=1)
    with pytest.raises(ValueError, match="Duplicate atom serial"):
        prepare_viewer_payload([atom(1), atom(1, 2.0)], source_format="pdb")


def test_viewer_payload_rejects_nonfinite_coordinates_and_bad_annotations() -> None:
    with pytest.raises(ValueError, match="non-finite"):
        prepare_viewer_payload([atom(x=float("nan"))], source_format="pdb")
    invalid = Atom(1, "C" * 9, "ALA", "A", 1, 0.0, 0.0, 0.0, "C")
    with pytest.raises(ValueError, match="oversized"):
        prepare_viewer_payload([invalid], source_format="pdb")


def test_viewer_payload_serializer_rejects_unknown_schema() -> None:
    with pytest.raises(ValueError, match="schema"):
        serialize_viewer_payload({"schema": "future"})


def test_preparation_record_is_reproducible_and_content_addressed() -> None:
    source = b"PDB fixture bytes"
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    record = build_preparation_record(source, payload, parser_version="kinetics-pdb-1")
    assert record["record_schema"] == "kinetics.structure-preparation.v1"
    assert record["source_bytes"] == len(source)
    assert len(record["source_sha256"]) == 64
    assert len(record["payload_sha256"]) == 64
    assert record["atom_count"] == 1
    assert record == build_preparation_record(source, payload, parser_version="kinetics-pdb-1")


def test_preparation_record_rejects_invalid_metadata() -> None:
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    with pytest.raises(ValueError, match="source_bytes"):
        build_preparation_record(b"", payload, parser_version="1")
    with pytest.raises(ValueError, match="parser_version"):
        build_preparation_record(b"x", payload, parser_version=" ")
    with pytest.raises(ValueError, match="dropped_record_count"):
        build_preparation_record(b"x", payload, parser_version="1", dropped_record_count=-1)


def test_viewer_payload_rejects_non_integer_or_boolean_atom_limits() -> None:
    for invalid_limit in (True, 1.5, "10"):
        with pytest.raises(ValueError, match="max_atoms"):
            prepare_viewer_payload([atom()], source_format="pdb", max_atoms=invalid_limit)  # type: ignore[arg-type]


def test_viewer_serializer_rejects_inconsistent_or_unsafe_payloads() -> None:
    payload = prepare_viewer_payload([atom()], source_format="pdb")

    wrong_count = copy.deepcopy(payload)
    wrong_count["atom_count"] = 2
    with pytest.raises(ValueError, match="does not match"):
        serialize_viewer_payload(wrong_count)

    non_finite = copy.deepcopy(payload)
    non_finite["atoms"][0]["xyz"][0] = float("inf")
    with pytest.raises(ValueError, match="invalid coordinates"):
        serialize_viewer_payload(non_finite)

    duplicate = copy.deepcopy(payload)
    duplicate["atoms"].append(copy.deepcopy(duplicate["atoms"][0]))
    duplicate["atom_count"] = 2
    with pytest.raises(ValueError, match="duplicate serial"):
        serialize_viewer_payload(duplicate)

    extra_field = copy.deepcopy(payload)
    extra_field["unreviewed_html"] = "<script>"
    with pytest.raises(ValueError, match="unsupported fields"):
        serialize_viewer_payload(extra_field)


@pytest.mark.parametrize(
    "field, value",
    [
        ("source_format", []),
        ("coordinate_unit", "nm"),
        ("atom_count", True),
        ("limitations", []),
    ],
)
def test_viewer_serializer_rejects_invalid_payload_metadata(
    field: str, value: object,
) -> None:
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    payload[field] = value
    with pytest.raises(ValueError):
        serialize_viewer_payload(payload)



def test_viewer_payload_enforces_serialized_byte_limit() -> None:
    with pytest.raises(ValueError, match="max_payload_bytes"):
        prepare_viewer_payload(
            [atom()], source_format="pdb", max_payload_bytes=64,
        )
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    with pytest.raises(ValueError, match="max_payload_bytes"):
        serialize_viewer_payload(payload, max_payload_bytes=64)


@pytest.mark.parametrize("invalid_limit", [True, 0, -1, 1.5, "100"])
def test_viewer_payload_rejects_invalid_byte_limits(invalid_limit: object) -> None:
    with pytest.raises(ValueError, match="max_payload_bytes"):
        prepare_viewer_payload(
            [atom()], source_format="pdb", max_payload_bytes=invalid_limit,  # type: ignore[arg-type]
        )



def test_structure_session_export_is_deterministic_and_explicitly_unrendered() -> None:
    source = b"PDB fixture bytes"
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    exported = build_structure_session_export(
        source, payload, parser_version="kinetics-pdb-1",
    )
    bundle = json.loads(exported)
    assert bundle["schema"] == "kinetics.structure-session.v1"
    assert bundle["render_state"] == "not_rendered"
    assert bundle["preparation"]["source_sha256"]
    assert bundle["preparation"]["payload_sha256"]
    assert "No PNG/SVG image" in bundle["export_limitations"][1]
    assert exported == build_structure_session_export(
        source, payload, parser_version="kinetics-pdb-1",
    )


def test_structure_session_export_enforces_byte_limit() -> None:
    payload = prepare_viewer_payload([atom()], source_format="pdb")
    with pytest.raises(ValueError, match="max_export_bytes"):
        build_structure_session_export(
            b"source", payload, parser_version="1", max_export_bytes=64,
        )


def test_structure_source_parser_builds_payload_and_provenance() -> None:
    from molecularis.structure_view import prepare_structure_viewer_source

    pdb = (
        "ATOM      1  CA  ALA A   1      1.000   2.000   3.000  1.00 20.00           C  \\n"
        "END\\n"
    )
    result = prepare_structure_viewer_source(pdb, source_format="pdb")
    assert result["payload"]["atom_count"] == 1
    assert result["payload"]["atoms"][0]["xyz"] == [1.0, 2.0, 3.0]
    assert result["preparation"]["source_bytes"] == len(pdb.encode("utf-8"))
    assert len(result["preparation"]["source_sha256"]) == 64


def test_structure_source_parser_supports_mmcif_and_rejects_bounds() -> None:
    from molecularis.structure_view import prepare_structure_viewer_source

    cif = """data_demo
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
ATOM 1 C CA ALA A 1 1.0 2.0 3.0
"""
    result = prepare_structure_viewer_source(cif, source_format="mmcif")
    assert result["payload"]["source_format"] == "mmcif"
    assert result["payload"]["atoms"][0]["name"] == "CA"
    with pytest.raises(ValueError, match="max_source_bytes"):
        prepare_structure_viewer_source(cif, source_format="mmcif", max_source_bytes=4)
    with pytest.raises(ValueError, match="source_format"):
        prepare_structure_viewer_source(cif, source_format="xyz")
