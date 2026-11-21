from __future__ import annotations

import hashlib
import json

import pytest

from molecularis.pharmacogenomics_service import (
    HaplotypeCall, PharmacogenomicsDocument, ingest_pharmacogenomics,
    ingest_pgx_definitions, load_pharmacogenomics, pharmacogenomics_rulebook,
    register_pharmacogenomics_service,
)
from molecularis.pgx import VariantKey
from molecularis.platform import MolecularisPlatform
from molecularis.platform.contracts import ValidationError


def _pack() -> str:
    # Source digest is a pinned source release identifier, not a clinical assertion.
    return json.dumps({
        "schema_version": 1, "genome_build": "SYNTHETIC-v1",
        "source": {"name": "Synthetic PGx fixture", "release": "fixture-1",
                   "url": "https://example.org/synthetic-pgx", "license": "CC0-1.0",
                   "sha256": hashlib.sha256(b"fixture-source").hexdigest()},
        "definitions": [
            {"id": "def-cyp-demo", "gene": "CYPDEMO", "star_allele": "*2",
             "required_variants": [{"chromosome": "chr1", "position": 101,
                                    "ref": "A", "alt": "G"}],
             "excluded_variants": []},
            {"id": "def-cyp-ref", "gene": "CYPDEMO", "star_allele": "*1",
             "required_variants": [], "excluded_variants": [
                 {"chromosome": "chr1", "position": 101, "ref": "A", "alt": "G"}]},
        ],
    })


def _record() -> PharmacogenomicsDocument:
    variant = VariantKey("SYNTHETIC-v1", "chr1", 101, "A", "G")
    return PharmacogenomicsDocument("synthetic-sample-1", "SYNTHETIC-v1", (
        HaplotypeCall("CYPDEMO", "hap-1", (variant,), True, True),
        HaplotypeCall("CYPDEMO", "hap-2", (), True, True),
        HaplotypeCall("CYPDEMO", "hap-3", (), False, True),
    ))


def _runtime(tmp_path):
    platform = MolecularisPlatform(tmp_path / "store")
    platform.start()
    register_pharmacogenomics_service(platform)
    return platform


def test_document_round_trip_digest_and_input_validation():
    record = _record()
    restored = PharmacogenomicsDocument.from_json(record.to_json())
    assert restored == record and restored.sha256 == record.sha256
    with pytest.raises(ValueError, match="synthetic_non_patient"):
        PharmacogenomicsDocument("patient", "b1", (), "patient")
    with pytest.raises(ValueError, match="genome build"):
        PharmacogenomicsDocument("x", "b1", (
            HaplotypeCall("G", "h1", (VariantKey("b2", "1", 1, "A", "C"),), True, True),
        ))


def test_document_rejects_duplicate_keys_unknown_fields_and_duplicate_variants():
    with pytest.raises(ValueError, match="duplicate JSON key"):
        PharmacogenomicsDocument.from_json('{"schema":"x","schema":"y"}')
    value = json.loads(_record().to_json())
    value["unexpected"] = True
    with pytest.raises(ValueError, match="fields/schema"):
        PharmacogenomicsDocument.from_json(json.dumps(value))
    v = VariantKey("SYNTHETIC-v1", "chr1", 101, "A", "G")
    with pytest.raises(ValueError, match="duplicate variant"):
        PharmacogenomicsDocument("x", "SYNTHETIC-v1", (
            HaplotypeCall("G", "h1", (v, v), True, True),
        ))


def test_artifact_round_trip_and_integrity(tmp_path):
    platform = _runtime(tmp_path)
    try:
        record = _record()
        artifact = ingest_pharmacogenomics(platform, record)
        assert load_pharmacogenomics(platform, artifact.artifact_id) == record
    finally:
        platform.close()


def test_definition_pack_is_release_pinned_and_artifact_backed(tmp_path):
    platform = _runtime(tmp_path)
    try:
        artifact = ingest_pgx_definitions(platform, _pack(), expected_source_release="fixture-1")
        assert artifact.metadata["definition_count"] == 2
        with pytest.raises(ValueError, match="release"):
            ingest_pgx_definitions(platform, _pack(), expected_source_release="other")
    finally:
        platform.close()


def test_rulebook_matches_only_complete_phased_haplotypes(tmp_path):
    platform = _runtime(tmp_path)
    try:
        sample = ingest_pharmacogenomics(platform, _record())
        definitions = ingest_pgx_definitions(platform, _pack(), expected_source_release="fixture-1")
        report = platform.execute(
            pharmacogenomics_rulebook("match"),
            {"pgx_sample_artifact_id": sample.artifact_id,
             "pgx_definitions_artifact_id": definitions.artifact_id},
        )["pharmacogenomics_result"]
        matches = report["result"]["matches"]
        assert [(m["status"], m["star_allele"]) for m in matches] == [
            ("matched", "*2"), ("matched", "*1"), ("no_call_unphased", None),
        ]
        assert report["result"]["interpretation_performed"] is False
        assert report["rules_checked"] == ["PGX-001", "PGX-002", "PGX-003",
                                           "PGX-004", "PGX-005", "PGX-006", "PGX-007"]
    finally:
        platform.close()


def test_rulebook_validate_and_rejects_genome_build_mismatch(tmp_path):
    platform = _runtime(tmp_path)
    try:
        sample = ingest_pharmacogenomics(platform, _record())
        report = platform.execute(
            pharmacogenomics_rulebook("validate"),
            {"pgx_sample_artifact_id": sample.artifact_id},
        )["pharmacogenomics_result"]
        assert report["result"]["valid"] is True
        other = _pack().replace("SYNTHETIC-v1", "OTHER-v1")
        definitions = ingest_pgx_definitions(platform, other, expected_source_release="fixture-1")
        with pytest.raises(ValidationError, match="genome builds differ"):
            platform.execute(
                pharmacogenomics_rulebook("match"),
                {"pgx_sample_artifact_id": sample.artifact_id,
                 "pgx_definitions_artifact_id": definitions.artifact_id},
            )
    finally:
        platform.close()


def test_rulebook_rejects_unknown_operation():
    with pytest.raises(ValueError, match="unsupported"):
        pharmacogenomics_rulebook("dose")
