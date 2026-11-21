#!/usr/bin/env python3
"""Validate registry references and evidence claims; never infer validation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capabilities" / "registry.yaml"
COLLECTIONS = (
    "tools",
    "engines",
    "data_packs",
    "domains",
    "device_logs",
    "validation_records",
    "ui_screens",
    "ui_settings",
    "security_features",
)
STATUSES = {"planned", "implemented", "validated"}
EVIDENCE = {"none", "benchmark", "reference-concordance", "clinical-study"}


def _ids(items: Any, collection: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{collection} must be a list")
        return set()
    found: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{collection}[{index}] must be a mapping")
            continue
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"{collection}[{index}] requires a non-empty id")
        elif identifier in found:
            errors.append(f"duplicate {collection} id: {identifier}")
        else:
            found.add(identifier)
    return found


def validate_registry(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry root must be a mapping"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    known = {name: _ids(data.get(name, []), name, errors) for name in COLLECTIONS}
    tools = data.get("tools", [])
    if not isinstance(tools, list):
        tools = []
    tool_by_id = {
        str(tool.get("id")): tool
        for tool in tools
        if isinstance(tool, dict) and isinstance(tool.get("id"), str)
    }

    for tool in tools:
        if not isinstance(tool, dict):
            continue
        tid = str(tool.get("id", "<unknown>"))
        status = tool.get("status", "planned")
        evidence = tool.get("evidence_level", "none")
        if status not in STATUSES:
            errors.append(f"tool {tid}: invalid status {status!r}")
        if evidence not in EVIDENCE:
            errors.append(f"tool {tid}: invalid evidence_level {evidence!r}")
        if status == "implemented" and not tool.get("implementation"):
            errors.append(f"tool {tid}: implemented status requires implementation")
        implementation = tool.get("implementation")
        if implementation is not None:
            if not isinstance(implementation, str) or not implementation.strip():
                errors.append(
                    f"tool {tid}: implementation must be a non-empty repository-relative path"
                )
            else:
                relative = PurePosixPath(implementation)
                if relative.is_absolute() or ".." in relative.parts:
                    errors.append(
                        f"tool {tid}: implementation path must stay inside the repository"
                    )
                elif not (ROOT / Path(*relative.parts)).is_file():
                    errors.append(
                        f"tool {tid}: implementation file does not exist: {implementation}"
                    )
        references = (
            ("engine_ids", "engines"),
            ("data_pack_ids", "data_packs"),
            ("domain_ids", "domains"),
        )
        for field, collection in references:
            refs = tool.get(field, [])
            if not isinstance(refs, list):
                errors.append(f"tool {tid}: {field} must be a list")
                continue
            for ref in refs:
                if ref not in known[collection]:
                    errors.append(
                        f"tool {tid}: {field} references missing {collection} id {ref!r}"
                    )
        if status == "validated":
            records = tool.get("validation_records", [])
            if not isinstance(records, list) or not records:
                errors.append(f"tool {tid}: validated status requires validation_records")
            else:
                for record_id in records:
                    if record_id not in known["validation_records"]:
                        errors.append(
                            f"tool {tid}: validation_records references missing id {record_id!r}"
                        )
            if evidence == "none":
                errors.append(
                    f"tool {tid}: validated status requires non-none evidence_level"
                )
        if "device_verified" in tool and not isinstance(tool["device_verified"], bool):
            errors.append(f"tool {tid}: device_verified must be a boolean")
        if tool.get("device_verified", False):
            logs = tool.get("device_log_ids", [])
            if not isinstance(logs, list) or not logs:
                errors.append(f"tool {tid}: device_verified requires device_log_ids")
            elif any(log not in known["device_logs"] for log in logs):
                errors.append(
                    f"tool {tid}: device_verified references a missing device log"
                )
        if tool.get("clinical", False):
            gate = data.get("clinical_gate", {})
            if not isinstance(gate, dict) or gate.get("enabled") is not True:
                errors.append(
                    f"tool {tid}: clinical capability requires clinical_gate.enabled"
                )
            elif not gate.get("part12_evidence"):
                errors.append(f"tool {tid}: clinical capability requires Part 12 evidence")


    # UI/security inventories are explicit registry records. Planned entries
    # are not executable until implementation and tests are recorded.
    for collection in ("ui_screens", "ui_settings", "security_features"):
        for item in data.get(collection, []):
            if not isinstance(item, dict):
                continue
            identifier = str(item.get("id", "<unknown>"))
            if item.get("track") not in {"UI", "G"}:
                errors.append(f"{collection} {identifier}: track must be UI or G")
            status = item.get("status", "planned")
            if status not in STATUSES:
                errors.append(f"{collection} {identifier}: invalid status {status!r}")
            tests = item.get("tests", [])
            if not isinstance(tests, list):
                errors.append(f"{collection} {identifier}: tests must be a list")
            if status == "implemented" and not tests:
                errors.append(f"{collection} {identifier}: implemented requires test references")
            if collection == "ui_screens" and status == "implemented":
                if item.get("accessibility_check") != "passed":
                    errors.append(
                        f"{collection} {identifier}: implemented requires a passed "
                        "accessibility check"
                    )
                matrix = item.get("device_matrix")
                if not isinstance(matrix, list) or not matrix:
                    errors.append(
                        f"{collection} {identifier}: implemented requires device-matrix evidence"
                    )

    settings_path = ROOT / "design" / "settings-schema.yaml"
    try:
        settings_doc = yaml.safe_load(settings_path.read_text(encoding="utf-8"))
        schema_keys = {
            item.get("key") for item in settings_doc.get("settings", [])
            if isinstance(item, dict)
        }
    except (OSError, yaml.YAMLError, AttributeError):
        schema_keys = set()
    for item in data.get("ui_settings", []):
        if isinstance(item, dict) and item.get("schema_key") not in schema_keys:
            errors.append(
                f"ui_settings {item.get('id')}: missing settings schema key "
                f"{item.get('schema_key')!r}"
            )

    claims = data.get("claims", [])
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    _ids(claims, "claims", errors)
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = str(claim.get("id", "<unknown>"))
        if claim.get("claim_type") not in {"public", "paper"}:
            errors.append(f"claim {claim_id}: claim_type must be public or paper")
        tool_ids = claim.get("tool_ids", [])
        if not isinstance(tool_ids, list) or not tool_ids:
            errors.append(f"claim {claim_id}: requires tool_ids")
            continue
        for tool_id in tool_ids:
            tool = tool_by_id.get(str(tool_id))
            if tool is None:
                errors.append(f"claim {claim_id}: references missing tool {tool_id!r}")
            elif tool.get("status") != "validated":
                errors.append(
                    f"claim {claim_id}: tool {tool_id!r} is not validated; "
                    "public/paper claims require validated tools"
                )
    if not isinstance(data.get("clinical_gate", {}), dict):
        errors.append("clinical_gate must be a mapping")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args()
    try:
        data = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"registry load failed: {exc}", file=sys.stderr)
        return 2
    errors = validate_registry(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Registry valid: {args.registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
