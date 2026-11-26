"""Deterministic, fixture-backed capability smoke tests for Molecularis Terminal.

Only capabilities with reviewed local fixture providers are executed. Other
registered capabilities are reported as NOT COVERED rather than simulated.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .platform import ExecutionContext
from .sequence_service import (
    SequenceDocument,
    ingest_sequence,
    sequence_rulebook,
)


@dataclass(frozen=True, slots=True)
class TestCase:
    case_id: str
    capability_id: str
    description: str
    sequence_type: str
    sequence: str
    parameters: dict[str, Any]
    check: Callable[[dict[str, Any]], bool]


def _result(values: dict[str, Any]) -> dict[str, Any]:
    return values["sequence_result"]["result"]


def _is_valid(values: dict[str, Any]) -> bool:
    return _result(values).get("valid") is True


def _has_length_4(values: dict[str, Any]) -> bool:
    return _result(values).get("length") == 4


def _has_reverse_complement(values: dict[str, Any]) -> bool:
    return _result(values).get("sequence") == "GCAT"


def _has_transcript(values: dict[str, Any]) -> bool:
    return _result(values).get("sequence") == "AUGC"


def _has_translation(values: dict[str, Any]) -> bool:
    return _result(values).get("protein") == "MAI"


CASES = (
    TestCase("SEQ-SMOKE-001", "sequence.validate.v1", "Validate a canonical DNA artifact",
             "DNA", "ATGC", {}, _is_valid),
    TestCase("SEQ-SMOKE-002", "sequence.analyze.v1", "Calculate sequence composition",
             "DNA", "ATGC", {}, _has_length_4),
    TestCase("SEQ-SMOKE-003", "sequence.reverse-complement.v1", "IUPAC DNA reverse complement",
             "DNA", "ATGC", {}, _has_reverse_complement),
    TestCase("SEQ-SMOKE-004", "sequence.transcribe.v1", "Transcribe DNA to RNA",
             "DNA", "ATGC", {}, _has_transcript),
    TestCase("SEQ-SMOKE-005", "sequence.translate.v1", "Translate an explicit coding sequence",
             "DNA", "ATGGCCATT", {"frame": 0, "table_id": 1}, _has_translation),
)


def run_testlab(platform: Any, *, service: str | None = None) -> dict[str, Any]:
    """Run all available deterministic fixture cases for a selected service."""
    registered = platform.registry.list(service=service)
    registered_ids = {cap.id for cap in registered}
    cases = [case for case in CASES if case.capability_id in registered_ids]
    rows: list[dict[str, Any]] = []
    for case in cases:
        try:
            artifact = ingest_sequence(
                platform,
                SequenceDocument(
                    identifier=f"terminal-{case.case_id.lower()}",
                    sequence=case.sequence,
                    sequence_type=case.sequence_type,
                    description="Built-in deterministic Molecularis Terminal smoke fixture",
                ),
            )
            operation = {
                "sequence.validate.v1": "validate",
                "sequence.analyze.v1": "statistics",
                "sequence.reverse-complement.v1": "reverse_complement",
                "sequence.transcribe.v1": "transcribe",
                "sequence.translate.v1": "translate",
            }[case.capability_id]
            rulebook = sequence_rulebook(operation, parameters=case.parameters)
            context = ExecutionContext(
                service_id="molecularis-terminal-testlab",
                rulebook_version=rulebook.version,
                parameters={"test_case": case.case_id, "fixture": "built-in-v1"},
            )
            values = platform.execute(
                rulebook,
                {"sequence_artifact_id": artifact.artifact_id},
                context=context,
            )
            passed = bool(case.check(values))
            rows.append({
                "case_id": case.case_id,
                "capability_id": case.capability_id,
                "status": "PASS" if passed else "FAIL",
                "description": case.description,
                "run_id": context.run_id,
                "output_artifact_ids": [
                    item["artifact_id"]
                    for item in platform.find_exact("run_id", context.run_id).items
                ],
                "observed": values.get("sequence_result"),
            })
        except Exception as exc:
            rows.append({
                "case_id": case.case_id,
                "capability_id": case.capability_id,
                "status": "ERROR",
                "description": case.description,
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
    covered_ids = {row["capability_id"] for row in rows}
    untested = sorted(registered_ids - covered_ids)
    passed = sum(row["status"] == "PASS" for row in rows)
    failed = sum(row["status"] == "FAIL" for row in rows)
    errors = sum(row["status"] == "ERROR" for row in rows)
    return {
        "schema": "molecularis.terminal-test-report.v1",
        "service_filter": service,
        "registered_capability_count": len(registered_ids),
        "fixture_case_count": len(rows),
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "not_covered": len(untested),
        "coverage": [
            {"capability_id": capability_id,
             "status": "COVERED" if capability_id in covered_ids else "NOT_COVERED"}
            for capability_id in sorted(registered_ids)
        ],
        "cases": rows,
        "scientific_validation": "NOT_PERFORMED",
    }
