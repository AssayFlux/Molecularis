from __future__ import annotations

import hashlib

import pytest

from molecularis.domain_integration import (
    DOMAIN_PROFILES,
    create_domain_handoff,
    register_scientific_domains,
    seed_domain_knowledge_packages,
    validate_scientific_domains,
)
from molecularis.knowledge import EvidenceClass, ScientificKnowledgeEngine
from molecularis.platform import MolecularisPlatform
from molecularis.platform.contracts import ValidationError
from molecularis.protein_service import (
    PROTEIN_MEDIA_TYPE,
    PROTEIN_SCHEMA_ID,
    ProteinDocument,
    load_protein,
)
from molecularis.sequence_service import SequenceDocument, ingest_sequence


def test_all_fourteen_native_domain_services_register_on_one_platform(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    try:
        report = register_scientific_domains(platform)
        assert report["domain_count"] == 14
        assert {item["code"] for item in report["domains"]} == {
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"
        }
        assert report["capability_count"] >= 50
        assert all(item["capabilities"] for item in report["domains"])
        assert validate_scientific_domains(platform) == report
    finally:
        platform.close()


def test_domain_registration_rejects_duplicate_installation(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    try:
        register_scientific_domains(platform)
        with pytest.raises(ValidationError, match="already registered"):
            register_scientific_domains(platform)
    finally:
        platform.close()


def test_domain_knowledge_manifests_do_not_fabricate_scientific_facts():
    engine = ScientificKnowledgeEngine()
    digests = seed_domain_knowledge_packages(engine)
    assert len(digests) == 14
    assert len(set(digests)) == 14
    packages = engine.list_packages()
    assert len(packages) == 14
    assert {domain for _, _, domain in packages} == {profile.service for profile in DOMAIN_PROFILES}
    assert engine.query_concepts() == ()
    assert engine.query_equations() == ()
    for package_id, version, _ in packages:
        package = engine.get(package_id, version)
        assert package.metadata["status"] == "framework_only"
        assert package.metadata["scientific_assertion_count"] == 0


def test_sequence_to_protein_handoff_preserves_types_verification_and_lineage(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    try:
        register_scientific_domains(platform)
        source = ingest_sequence(platform, SequenceDocument("coding-sequence", "ATGGCTTAA"))
        protein = ProteinDocument("translated-protein", "MA", "Caller-translated test fixture")
        verification = platform.ingest(
            b'{"status":"passed"}',
            media_type="application/vnd.molecularis.verification-report+json",
            schema_id="molecularis.verification-report.v1",
            metadata={
                "verification_status": "passed",
                "verifier_id": "test-independent-verifier",
                "verification_method": "fixture-sequence-translation-check-v1",
                "evidence_refs": [source.artifact_id],
            },
        )
        target_metadata = {
            "identifier": protein.identifier,
            "protein_sha256": protein.sha256,
            "length": len(protein.sequence),
            "sequence_sha256": hashlib.sha256(protein.sequence.encode("ascii")).hexdigest(),
        }
        target = create_domain_handoff(
            platform,
            source_artifact_id=source.artifact_id,
            target_domain="E",
            target_payload=protein.to_dict(),
            target_schema_id=PROTEIN_SCHEMA_ID,
            target_media_type=PROTEIN_MEDIA_TYPE,
            transformation_id="sequence-to-protein-translation",
            transformation_version="1.0.0",
            evidence_class=EvidenceClass.DERIVED,
            assumptions=("Input coding frame and genetic code were caller-declared.",),
            verification_artifact_id=verification.artifact_id,
            target_metadata=target_metadata,
        )
        loaded = load_protein(platform, target.artifact_id)
        assert loaded == protein
        assert set(target.parents) == {source.artifact_id, verification.artifact_id}
        handoff = target.metadata["domain_handoff"]
        assert handoff["source_domain"] == "sequence"
        assert handoff["target_domain"] == "protein"
        assert handoff["evidence_class"] == "derived"
        assert handoff["verification_status"] == "passed"
        assert handoff["semantic_conversion_is_caller_owned"] is True
    finally:
        platform.close()


def test_domain_handoff_rejects_unverified_or_mismatched_conversion(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    try:
        register_scientific_domains(platform)
        source = ingest_sequence(platform, SequenceDocument("source", "ATG"))
        bad_verification = platform.ingest(
            b"{}",
            media_type="application/json",
            schema_id="molecularis.verification-report.v1",
            metadata={
                "verification_status": "failed",
                "verifier_id": "verifier",
                "verification_method": "method-v1",
                "evidence_refs": [source.artifact_id],
            },
        )
        common = dict(
            source_artifact_id=source.artifact_id,
            target_domain="E",
            target_payload={"schema": PROTEIN_SCHEMA_ID, "identifier": "x", "description": "", "sequence": "M"},
            target_schema_id=PROTEIN_SCHEMA_ID,
            target_media_type=PROTEIN_MEDIA_TYPE,
            transformation_id="test-transform",
            transformation_version="1",
            evidence_class="constructed",
            assumptions=("test assumption",),
            verification_artifact_id=bad_verification.artifact_id,
        )
        with pytest.raises(ValidationError, match="passed verification"):
            create_domain_handoff(platform, **common)
        with pytest.raises(ValidationError, match="not registered"):
            create_domain_handoff(platform, **{**common, "target_schema_id": "unrelated.schema.v1"})
    finally:
        platform.close()
