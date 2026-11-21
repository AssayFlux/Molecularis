#!/usr/bin/env python3
"""Validate Track G governance registers and evidence-index integrity."""
from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID = re.compile(r"\bG[0-7]-\d{2}\b")


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path.relative_to(ROOT)} has no CSV header")
        rows = [
            {str(key): str(value or "") for key, value in row.items() if key is not None}
            for row in reader
        ]
        return list(reader.fieldnames), rows


def validate() -> list[str]:
    errors: list[str] = []
    required = [
        "docs/track-g/implementation-plan.md",
        "docs/track-g/audit-report-2026-11-12.md",
        "docs/track-g/control-evidence-register.md",
        "docs/track-g/roles-and-review-cadence.md",
        "docs/track-g/requirements-traceability.csv",
        "docs/track-g/dependency-decision-register.csv",
        "docs/track-g/capability-claims-matrix.csv",
        "docs/track-g/capa-register.csv",
        "docs/track-g/data-flow-inventory.md",
        "docs/track-g/security-verification-matrix.md",
        "docs/track-g/publication-integrity.md",
        "docs/track-g/operational-controls.md",
        "docs/security-threat-model.md",
        "SECURITY.md",
        "PRIVACY.md",
        "docs/release-checklist.md",
        "paper/claim-evidence-ledger.csv",
        "capabilities/registry.yaml",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing required governance artifact: {relative}")

    register_path = ROOT / "docs/track-g/control-evidence-register.md"
    trace_path = ROOT / "docs/track-g/requirements-traceability.csv"
    if register_path.is_file() and trace_path.is_file():
        register = register_path.read_text(encoding="utf-8")
        controls = set(CONTROL_ID.findall(register))
        expected = {
            f"G{group}-{number:02d}"
            for group, count in enumerate((6, 4, 4, 4, 3, 3, 3, 3))
            for number in range(1, count + 1)
        }
        missing = sorted(expected - controls)
        if missing:
            errors.append("Control register is missing IDs: " + ", ".join(missing))
        headers, rows = _read_csv(trace_path)
        if not {"requirement_id", "control_ids", "status"}.issubset(headers):
            errors.append("Requirements traceability CSV is missing required columns")
        else:
            mapped = set()
            requirement_ids = []
            for row in rows:
                requirement_ids.append(row["requirement_id"])
                mapped.update(CONTROL_ID.findall(row["control_ids"]))
            if len(requirement_ids) != len(set(requirement_ids)):
                errors.append("Duplicate requirement_id in traceability CSV")
            if len(rows) != 8 or set(requirement_ids) != {f"G-REQ-{n:03d}" for n in range(1, 9)}:
                errors.append(
                    "Requirements traceability must contain exactly "
                    "G-REQ-001 through G-REQ-008"
                )
            unmapped = sorted(expected - mapped)
            if unmapped:
                errors.append("Controls missing traceability rows: " + ", ".join(unmapped))

    dependency_path = ROOT / "docs/track-g/dependency-decision-register.csv"
    if dependency_path.is_file():
        headers, rows = _read_csv(dependency_path)
        required_columns = {
            "component_id", "version", "ecosystem", "scope", "source_or_coordinate",
            "artifact_sha256", "license_status", "redistribution_status", "reviewer", "status",
        }
        if not required_columns.issubset(headers):
            errors.append("Dependency decision register is missing required columns")
        component_ids = [row.get("component_id", "").strip() for row in rows]
        if any(not item for item in component_ids):
            errors.append("Dependency decision register contains an empty component_id")
        if len(component_ids) != len(set(component_ids)):
            errors.append("Dependency decision register contains duplicate component_id values")
        for row in rows:
            if not row.get("license_status", "").strip() or not row.get(
                "redistribution_status", ""
            ).strip():
                errors.append(
                    "Dependency decision register must explicitly state license and "
                    "redistribution status for every component"
                )
                break

    claim_path = ROOT / "docs/track-g/capability-claims-matrix.csv"
    registry_path = ROOT / "capabilities/registry.yaml"
    if claim_path.is_file() and registry_path.is_file():
        headers, rows = _read_csv(claim_path)
        required_columns = {
            "capability_id", "capability_name", "implementation_path",
            "implementation_status", "evidence_level", "validation_status",
            "device_status", "license_status", "permitted_claim", "limitations",
        }
        if not required_columns.issubset(headers):
            errors.append("Capability claims matrix is missing required columns")
        claim_ids = [row.get("capability_id", "").strip() for row in rows]
        if any(not item for item in claim_ids):
            errors.append("Capability claims matrix contains an empty capability_id")
        if len(claim_ids) != len(set(claim_ids)):
            errors.append("Capability claims matrix contains duplicate capability_id values")
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        registry_ids = {
            str(tool.get("id", "")) for tool in registry.get("tools", [])
        }
        if set(claim_ids) != registry_ids:
            errors.append("Capability claims matrix IDs do not match capabilities/registry.yaml")
        for row in rows:
            if not row.get("device_status", "").strip() or not row.get(
                "license_status", ""
            ).strip():
                errors.append(
                    "Capability claims matrix must explicitly state device and license "
                    "status for every capability"
                )
                break

    capa_path = ROOT / "docs/track-g/capa-register.csv"
    if capa_path.is_file():
        headers, _ = _read_csv(capa_path)
        required_columns = {
            "record_id", "record_type", "severity", "description", "containment",
            "root_cause", "corrective_action", "effectiveness_check", "owner",
            "reviewer", "status", "linked_controls", "evidence_uri",
        }
        if not required_columns.issubset(headers):
            errors.append("CAPA register is missing required columns")

    security_path = ROOT / "docs/track-g/security-verification-matrix.md"
    if security_path.is_file():
        security = security_path.read_text(encoding="utf-8")
        test_ids = re.findall(r"\|\s*(SEC-\d{3})\s*\|", security)
        expected_test_ids = {f"SEC-{number:03d}" for number in range(1, 17)}
        if len(test_ids) != len(set(test_ids)):
            errors.append("Duplicate security verification test IDs")
        if set(test_ids) != expected_test_ids:
            errors.append(
                "Security verification matrix must contain SEC-001 through SEC-016 exactly"
            )

    data_flow_path = ROOT / "docs/track-g/data-flow-inventory.md"
    if data_flow_path.is_file():
        data_flow = data_flow_path.read_text(encoding="utf-8")
        flow_ids = re.findall(r"\|\s*(DF-\d{2})\s*\|", data_flow)
        expected_flow_ids = {f"DF-{number:02d}" for number in range(1, 10)}
        if len(flow_ids) != len(set(flow_ids)) or set(flow_ids) != expected_flow_ids:
            errors.append("Data-flow inventory must contain DF-01 through DF-09 exactly once")

    roles_path = ROOT / "docs/track-g/roles-and-review-cadence.md"
    if roles_path.is_file():
        roles = roles_path.read_text(encoding="utf-8")
        for role in (
            "G-ROLE-OWNER",
            "G-ROLE-ENG",
            "G-ROLE-SEC",
            "G-ROLE-SC",
            "G-ROLE-DATA",
            "G-ROLE-PRIV",
            "G-ROLE-QUALITY",
            "G-ROLE-RELEASE",
            "G-ROLE-PUB",
        ):
            role_rows = [
                line for line in roles.splitlines()
                if role in line and line.startswith("|")
            ]
            if len(role_rows) != 1:
                errors.append(f"{role} must have exactly one accountability row")
                continue
            columns = [column.strip() for column in role_rows[0].strip("|").split("|")]
            if len(columns) != 4 or not columns[2] or not columns[3]:
                errors.append(f"{role} must record an assignment state and independence limitation")

    operations_path = ROOT / "docs/track-g/operational-controls.md"
    if operations_path.is_file():
        operations = operations_path.read_text(encoding="utf-8")
        if "No exercise is marked complete by this template" not in operations:
            errors.append(
                "Operational procedure must distinguish templates from completed exercises"
            )
        for exercise in ("OPS-TT-01", "OPS-TT-02", "OPS-TT-03", "OPS-TT-04", "OPS-TT-05"):
            exercise_rows = [
                line for line in operations.splitlines()
                if line.startswith("|") and exercise in line
            ]
            if len(exercise_rows) != 1:
                errors.append(f"Missing or duplicate operational tabletop scenario {exercise}")
                continue
            status = exercise_rows[0].strip("|").split("|")[-1].strip()
            if status != "NOT RUN" and not status.startswith("COMPLETED — evidence:"):
                errors.append(f"{exercise} needs NOT RUN or a completed status with evidence")

    claim_path = ROOT / "paper/claim-evidence-ledger.csv"
    if claim_path.is_file():
        headers, rows = _read_csv(claim_path)
        required_columns = {
            "claim_id", "claim_text", "implementation_commit", "validation_protocol",
            "reference_dataset", "metric", "measured_value", "uncertainty",
            "artifact_path", "artifact_sha256", "independent_review", "status",
            "limitations",
        }
        if not required_columns.issubset(headers):
            errors.append("Manuscript claim ledger is missing required columns")
        if any(row.get("status", "").strip().lower() == "validated" and
               not row.get("independent_review", "").strip() for row in rows):
            errors.append("Validated manuscript claim lacks independent-review evidence")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Track G governance structure and register checks passed.")
    print("This validates document/register structure only; it is not external assurance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
