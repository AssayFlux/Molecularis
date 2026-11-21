from __future__ import annotations

from scripts.check_registry import validate_registry


def base_registry() -> dict[str, object]:
    return {
        "schema_version": 1,
        "tools": [],
        "engines": [{"id": "engine-a"}],
        "data_packs": [{"id": "pack-a"}],
        "domains": [{"id": "domain-a"}],
        "device_logs": [{"id": "device-log-a"}],
        "validation_records": [{"id": "validation-a"}],
        "claims": [],
        "clinical_gate": {"enabled": False, "part12_evidence": []},
    }


def test_empty_r0_registry_is_valid() -> None:
    assert validate_registry(base_registry()) == []


def test_missing_engine_reference_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "planned", "engine_ids": ["missing"]}]
    assert any("missing engines id" in error for error in validate_registry(data))


def test_implemented_without_implementation_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "implemented"}]
    assert any("requires implementation" in error for error in validate_registry(data))


def test_validated_without_record_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "validated", "evidence_level": "benchmark"}]
    assert any("requires validation_records" in error for error in validate_registry(data))


def test_validated_with_missing_record_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [
        {
            "id": "tool-a",
            "status": "validated",
            "evidence_level": "benchmark",
            "validation_records": ["missing"],
        }
    ]
    assert any("references missing id" in error for error in validate_registry(data))


def test_device_verified_without_log_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "device_verified": True}]
    assert any("requires device_log_ids" in error for error in validate_registry(data))


def test_device_verified_with_unknown_log_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [
        {"id": "tool-a", "device_verified": True, "device_log_ids": ["missing"]}
    ]
    assert any("missing device log" in error for error in validate_registry(data))


def test_clinical_capability_without_part12_gate_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "clinical": True}]
    assert any("clinical_gate.enabled" in error for error in validate_registry(data))


def test_clinical_capability_without_part12_evidence_is_rejected() -> None:
    data = base_registry()
    data["clinical_gate"] = {"enabled": True, "part12_evidence": []}
    data["tools"] = [{"id": "tool-a", "clinical": True}]
    assert any("Part 12 evidence" in error for error in validate_registry(data))


def test_public_claim_from_unvalidated_tool_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "implemented"}]
    data["claims"] = [{"id": "claim-a", "claim_type": "public", "tool_ids": ["tool-a"]}]
    assert any("is not validated" in error for error in validate_registry(data))


def test_invalid_status_is_rejected() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "shipped"}]
    assert any("invalid status" in error for error in validate_registry(data))


def test_implemented_tool_must_reference_existing_repository_file() -> None:
    data = base_registry()
    data["tools"] = [
        {
            "id": "tool-a",
            "status": "implemented",
            "implementation": "python/molecularis/not_a_real_module.py",
        }
    ]
    assert any("implementation file does not exist" in error for error in validate_registry(data))


def test_implementation_path_cannot_escape_repository() -> None:
    data = base_registry()
    data["tools"] = [{"id": "tool-a", "status": "implemented", "implementation": "../outside.py"}]
    assert any("must stay inside the repository" in error for error in validate_registry(data))


def test_duplicate_collection_ids_are_rejected() -> None:
    data = base_registry()
    data["engines"] = [{"id": "same"}, {"id": "same"}]
    assert any("duplicate engines id: same" in error for error in validate_registry(data))


def test_non_mapping_registry_is_rejected() -> None:
    assert validate_registry([]) == ["registry root must be a mapping"]


def test_unknown_registry_collection_is_not_required() -> None:
    # UI inventories were retired with the UI product surface; engine registry
    # validation must not depend on removed UI settings schemas.
    assert validate_registry(base_registry()) == []
