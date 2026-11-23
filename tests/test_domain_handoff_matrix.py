from __future__ import annotations

from molecularis.domain_integration import (
    DOMAIN_PROFILES,
    create_domain_handoff,
    register_scientific_domains,
)
from molecularis.knowledge import EvidenceClass
from molecularis.platform import MolecularisPlatform


def test_all_registered_domain_pairs_support_typed_lineage_envelopes(tmp_path):
    """Exercise all A–N handoff pairs as transport contracts, not semantic conversions."""
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    try:
        register_scientific_domains(platform)
        sources = {}
        for profile in DOMAIN_PROFILES:
            sources[profile.code] = platform.ingest(
                b'{"synthetic_contract_fixture":true}',
                media_type=profile.artifact_media_types[0],
                schema_id=profile.artifact_schema_ids[0],
                metadata={"domain": profile.service, "fixture_only": True},
            )
        evidence_ids = [artifact.artifact_id for artifact in sources.values()]
        verification = platform.ingest(
            b'{"status":"passed","scope":"synthetic-contract-only"}',
            media_type="application/vnd.molecularis.verification-report+json",
            schema_id="molecularis.verification-report.v1",
            metadata={
                "verification_status": "passed",
                "verifier_id": "contract-matrix-test-verifier",
                "verification_method": "artifact-existence-and-lineage-v1",
                "evidence_refs": evidence_ids,
            },
            parents=evidence_ids,
        )

        handoff_count = 0
        for source_profile in DOMAIN_PROFILES:
            for target_profile in DOMAIN_PROFILES:
                if source_profile.code == target_profile.code:
                    continue
                source = sources[source_profile.code]
                target = create_domain_handoff(
                    platform,
                    source_artifact_id=source.artifact_id,
                    target_domain=target_profile.code,
                    target_payload={
                        "synthetic_contract_fixture": True,
                        "source_artifact_id": source.artifact_id,
                        "target_domain": target_profile.code,
                    },
                    target_schema_id=target_profile.artifact_schema_ids[0],
                    target_media_type=target_profile.artifact_media_types[0],
                    transformation_id="contract-only-no-semantic-conversion",
                    transformation_version="1.0.0",
                    evidence_class=EvidenceClass.DERIVED,
                    assumptions=(
                        "Synthetic contract fixture only; no scientific semantic conversion is claimed.",
                    ),
                    verification_artifact_id=verification.artifact_id,
                    target_metadata={"fixture_only": True, "target_domain": target_profile.service},
                )
                assert target.schema_id == target_profile.artifact_schema_ids[0]
                assert target.media_type == target_profile.artifact_media_types[0]
                assert target.metadata["domain_handoff"]["source_domain"] == source_profile.service
                assert target.metadata["domain_handoff"]["target_domain"] == target_profile.service
                assert set(target.parents) == set(evidence_ids) | {
                    source.artifact_id, verification.artifact_id
                }
                handoff_count += 1

        assert handoff_count == 14 * 13
    finally:
        platform.close()
