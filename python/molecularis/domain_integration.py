"""P3 integration layer for all Molecularis scientific domains.

This module composes existing domain-owned engines; it does not replace their
algorithms, invent scientific facts, or infer semantic equivalence between schemas.
Cross-domain conversion is explicit, versioned, evidence-labelled and lineage-bound.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from .knowledge import EvidenceClass, KnowledgePackage, ScientificKnowledgeEngine
from .platform import Budget, MolecularisPlatform
from .platform.contracts import ValidationError


@dataclass(frozen=True, slots=True)
class DomainProfile:
    code: str
    service: str
    title: str
    rulebook_id: str
    artifact_schema_ids: tuple[str, ...]
    artifact_media_types: tuple[str, ...]
    scope: str
    non_claims: tuple[str, ...]


DOMAIN_PROFILES: tuple[DomainProfile, ...] = (
    DomainProfile("A", "molecular", "Molecular", "molecular-structural-validation",
        ("molecularis.molecule.v1",), ("application/vnd.molecularis.molecule+json",),
        "Explicit atom, bond, residue and coordinate molecular representations.",
        ("Graph validity is not experimental structure or energetic stability.",)),
    DomainProfile("B", "sequence", "Sequence", "sequence-core-v1",
        ("molecularis.sequence-record.v1",), ("application/vnd.molecularis.sequence+json",),
        "DNA, RNA and protein sequence validation and deterministic transforms.",
        ("Sequence validity does not establish biological function or annotation.",)),
    DomainProfile("C", "structure", "Structure", "structure-core-v1",
        ("molecularis.structure-record.v1",), ("application/vnd.molecularis.structure+json",),
        "Coordinate records, geometry, contacts, surface estimates and RMSD.",
        ("Geometric checks are not energetic or experimental structure validation.",)),
    DomainProfile("D", "chemistry", "Chemistry", "chemistry-core-v1",
        ("molecularis.chemistry-record.v1",), ("application/vnd.molecularis.chemistry+json",),
        "Explicit molecular graphs, descriptors, fingerprints and graph matching.",
        ("Graph descriptors do not establish reaction feasibility or physical stability.",)),
    DomainProfile("E", "protein", "Protein", "protein-core-v1",
        ("molecularis.protein-record.v1",), ("application/vnd.molecularis.protein+json",),
        "Protein sequence records, descriptors, motif scans and design-brief validation.",
        ("Motif or sequence analysis does not establish folding or function.",)),
    DomainProfile("F", "genomics", "Genomics", "genomics-core-v1",
        ("molecularis.genome-record.v1",), ("application/vnd.molecularis.genome+json",),
        "Genome contigs, assembly QC, ORF scans, annotation and variant QC.",
        ("QC and candidate ORFs are not validated biological annotations.",)),
    DomainProfile("G", "dna-rna", "DNA/RNA", "dna-rna-core-v1",
        ("molecularis.dna-rna-record.v1",), ("application/vnd.molecularis.dna-rna+json",),
        "Nucleic-acid records, transcription, translation and bounded folding utilities.",
        ("Predicted secondary structures and primer screens require separate validation.",)),
    DomainProfile("H", "simulation", "Simulation", "simulation-core-v1",
        ("molecularis.simulation-job.v1",), ("application/vnd.molecularis.simulation-job+json",),
        "Provenance-bound simulation protocols and energy-series analysis.",
        ("A simulation result is model-conditional, not an observation or experiment.",)),
    DomainProfile("I", "kinetics", "Kinetics", "kinetics-core-v1",
        ("molecularis.kinetics-network.v1",), ("application/vnd.molecularis.kinetics-network+json",),
        "Reaction networks, bounded deterministic integration and kinetic fits.",
        ("Caller-defined units and model assumptions are not inferred or validated.",)),
    DomainProfile("J", "omics", "Omics", "omics-core-v1",
        ("molecularis.omics-matrix.v1",), ("application/vnd.molecularis.omics-matrix+json",),
        "Feature-by-sample matrices, normalization, exploratory differential analysis and diversity.",
        ("Exploratory statistics are not causal, clinical or diagnostic conclusions.",)),
    DomainProfile("K", "phylogeny", "Phylogeny", "phylogeny-core-v1",
        ("molecularis.phylogeny-alignment.v1",), ("application/vnd.molecularis.phylogeny-alignment+json",),
        "Caller-aligned sequences, distance methods, NJ/UPGMA and bootstrap summaries.",
        ("Distance trees are assumption-dependent and do not establish species history.",)),
    DomainProfile("L", "pharmacogenomics", "Pharmacogenomics", "pharmacogenomics-core-v1",
        ("molecularis.pharmacogenomics-sample.v1", "molecularis.pharmacogenomics-definitions.v1"),
        ("application/vnd.molecularis.pharmacogenomics-sample+json",
         "application/vnd.molecularis.pharmacogenomics-definitions+json"),
        "Synthetic non-patient phased haplotypes and release-pinned star-allele matching.",
        ("No patient interpretation, phenotype translation, drug choice or dosing.",)),
    DomainProfile("M", "cohorts", "Cohorts", "cohorts-core-v1",
        ("molecularis.cohort.v1",), ("application/vnd.molecularis.cohort+json",),
        "Synthetic non-patient cohort summaries, strata and disclosure-aware overlap.",
        ("No patient records, clinical decisions or formal differential-privacy guarantee.",)),
    DomainProfile("N", "workflows", "Workflows", "workflows-core-v1",
        ("molecularis.workflow.v1",), ("application/vnd.molecularis.workflow+json",),
        "Typed workflow plans over registered capabilities and bounded Rulebook DAGs.",
        ("A valid workflow graph does not establish scientific correctness.",)),
)
_PROFILE_BY_SERVICE = {item.service: item for item in DOMAIN_PROFILES}
_PROFILE_BY_CODE = {item.code: item for item in DOMAIN_PROFILES}
_PROFILE_BY_SCHEMA = {
    schema: item for item in DOMAIN_PROFILES for schema in item.artifact_schema_ids
}


def register_scientific_domains(platform: MolecularisPlatform) -> dict[str, Any]:
    """Register every A–N native service on one already-started Core platform."""
    if not isinstance(platform, MolecularisPlatform):
        raise TypeError("platform must be a MolecularisPlatform")
    if platform.state.value != "ready":
        raise ValidationError("platform must be started before domain registration")
    from .molecular_service import register_molecular_service
    from .sequence_service import register_sequence_service
    from .structure_service import register_structure_service
    from .chemistry_service import register_chemistry_service
    from .protein_service import register_protein_service
    from .genomics_service import register_genomics_service
    from .dna_rna_service import register_dna_rna_service
    from .simulation_service import register_simulation_service
    from .kinetics_service import register_kinetics_service
    from .omics_service import register_omics_service
    from .phylogeny_service import register_phylogeny_service
    from .pharmacogenomics_service import register_pharmacogenomics_service
    from .cohorts_service import register_cohorts_service
    from .workflows_service import register_workflows_service

    registrars = (
        register_molecular_service, register_sequence_service, register_structure_service,
        register_chemistry_service, register_protein_service, register_genomics_service,
        register_dna_rna_service, register_simulation_service, register_kinetics_service,
        register_omics_service, register_phylogeny_service,
        register_pharmacogenomics_service, register_cohorts_service,
        register_workflows_service,
    )
    existing = {item.service for item in platform.registry.list()}
    if existing.intersection(_PROFILE_BY_SERVICE):
        raise ValidationError("one or more scientific services are already registered",
                              details={"existing_services": sorted(existing.intersection(_PROFILE_BY_SERVICE))})
    for register in registrars:
        register(platform)
    return validate_scientific_domains(platform)


def validate_scientific_domains(platform: MolecularisPlatform) -> dict[str, Any]:
    """Fail closed unless all fourteen domain capabilities and schema identities exist."""
    capabilities = platform.registry.list()
    by_service: dict[str, list[dict[str, Any]]] = {}
    for capability in capabilities:
        by_service.setdefault(capability.service, []).append({
            "id": capability.id, "version": capability.version,
            "operation": capability.operation, "input_schema": capability.input_schema,
            "output_schema": capability.output_schema,
            "deterministic": capability.deterministic,
        })
    missing = sorted(profile.service for profile in DOMAIN_PROFILES if not by_service.get(profile.service))
    if missing:
        raise ValidationError("scientific domain registration is incomplete",
                              details={"missing_services": missing})
    return {
        "schema": "molecularis.domain-integration-report.v1",
        "domain_count": len(DOMAIN_PROFILES),
        "domains": [{
            "code": profile.code, "service": profile.service, "title": profile.title,
            "rulebook_id": profile.rulebook_id,
            "artifact_schema_ids": list(profile.artifact_schema_ids),
            "capabilities": sorted(by_service[profile.service], key=lambda item: item["id"]),
            "scope": profile.scope, "non_claims": list(profile.non_claims),
        } for profile in DOMAIN_PROFILES],
        "capability_count": len(capabilities),
        "unregistered_capabilities": [],
        "limitations": [
            "Registration proves software availability, not scientific validity.",
            "Optional external engines and dependencies remain optional and must be verified at execution.",
            "Domain-specific scientific review remains separate from engineering integration.",
        ],
    }


def seed_domain_knowledge_packages(engine: ScientificKnowledgeEngine) -> tuple[str, ...]:
    """Install immutable domain framework manifests, not fabricated scientific facts."""
    if not isinstance(engine, ScientificKnowledgeEngine):
        raise TypeError("engine must be a ScientificKnowledgeEngine")
    digests: list[str] = []
    for profile in DOMAIN_PROFILES:
        package = KnowledgePackage(
            package_id=f"molecularis.domain.{profile.service}.framework",
            version="1.0.0",
            domain=profile.service,
            metadata={
                "status": "framework_only",
                "scientific_assertion_count": 0,
                "rulebook_id": profile.rulebook_id,
                "artifact_schema_ids": list(profile.artifact_schema_ids),
                "scope": profile.scope,
                "non_claims": list(profile.non_claims),
                "population_policy": "No facts are seeded; ingest only source-attributed, permission-checked knowledge.",
            },
        )
        digests.append(engine.ingest(package))
    return tuple(digests)


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValidationError("handoff payload must be finite JSON-compatible data") from exc
    if len(encoded) > 8_000_000:
        raise ValidationError("handoff payload exceeds 8 MB")
    return encoded


def create_domain_handoff(
    platform: MolecularisPlatform,
    *,
    source_artifact_id: str,
    target_domain: str,
    target_payload: Mapping[str, Any],
    target_schema_id: str,
    target_media_type: str,
    transformation_id: str,
    transformation_version: str,
    evidence_class: EvidenceClass | str,
    assumptions: tuple[str, ...],
    verification_artifact_id: str,
    target_metadata: Mapping[str, Any] | None = None,
    budget: Budget | None = None,
) -> Any:
    """Persist an explicit domain conversion with source and verifier lineage.

    The caller supplies the target-domain representation; this function never
    guesses or performs semantic conversion. Verification metadata is a traceable
    software contract, not proof of institutional independence or scientific truth.
    """
    if not isinstance(platform, MolecularisPlatform) or platform.state.value != "ready":
        raise ValidationError("a started MolecularisPlatform is required")
    if not isinstance(source_artifact_id, str) or not source_artifact_id.strip():
        raise ValidationError("source_artifact_id is required")
    if not isinstance(verification_artifact_id, str) or not verification_artifact_id.strip():
        raise ValidationError("verification_artifact_id is required")
    target = _PROFILE_BY_CODE.get(target_domain) or _PROFILE_BY_SERVICE.get(target_domain)
    if target is None:
        raise ValidationError("target_domain must identify one of A–N")
    source = platform.store.get(source_artifact_id)
    source_profile = _PROFILE_BY_SCHEMA.get(source.schema_id)
    if source_profile is None:
        raise ValidationError("source artifact schema is not owned by an integrated domain",
                              details={"schema_id": source.schema_id})
    if source_profile.service == target.service:
        raise ValidationError("domain handoff must cross distinct scientific domains")
    if target_schema_id not in target.artifact_schema_ids or target_media_type not in target.artifact_media_types:
        raise ValidationError("target schema/media type is not registered for the target domain",
                              details={"target_domain": target.service})
    for name, value in (("transformation_id", transformation_id),
                        ("transformation_version", transformation_version)):
        if not isinstance(value, str) or not value.strip() or len(value) > 128:
            raise ValidationError(f"{name} must be bounded non-empty text")
    if not isinstance(assumptions, tuple) or not assumptions or any(
        not isinstance(item, str) or not item.strip() or len(item) > 2048 for item in assumptions
    ):
        raise ValidationError("handoff assumptions must be explicit non-empty strings")
    try:
        label = EvidenceClass(evidence_class).value
    except (TypeError, ValueError) as exc:
        raise ValidationError("evidence_class is not a supported epistemic label") from exc
    verification = platform.store.get(verification_artifact_id)
    verification_meta = verification.metadata
    verifier = verification_meta.get("verifier_id")
    method = verification_meta.get("verification_method")
    status = verification_meta.get("verification_status")
    evidence_refs = verification_meta.get("evidence_refs")
    if status != "passed" or not isinstance(verifier, str) or not verifier.strip() or not isinstance(method, str) or not method.strip():
        raise ValidationError("handoff requires a passed verification artifact with verifier identity and method")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        raise ValidationError("verification artifact must cite evidence_refs")
    parents = [source_artifact_id, verification_artifact_id]
    for reference in evidence_refs:
        if not isinstance(reference, str) or not reference.strip():
            raise ValidationError("verification evidence references must be artifact IDs")
        platform.store.get(reference)
        if reference not in parents:
            parents.append(reference)
    payload = _canonical_json(target_payload)
    service_metadata = dict(target_metadata or {})
    reserved = {"domain_handoff"}
    if reserved.intersection(service_metadata):
        raise ValidationError("target_metadata contains a reserved P3 key")
    metadata = {**service_metadata, "domain_handoff": {
        "integration_version": "p3-domain-handoff-v1",
        "source_domain": source_profile.service,
        "target_domain": target.service,
        "source_artifact_id": source.artifact_id,
        "source_digest": source.digest,
        "source_schema_id": source.schema_id,
        "target_schema_id": target_schema_id,
        "transformation_id": transformation_id,
        "transformation_version": transformation_version,
        "evidence_class": label,
        "assumptions": list(assumptions),
        "verification_artifact_id": verification_artifact_id,
        "verifier_id": verifier,
        "verification_method": method,
        "verification_status": status,
        "evidence_refs": list(evidence_refs),
        "semantic_conversion_is_caller_owned": True,
    }}
    return platform.ingest(payload, media_type=target_media_type, schema_id=target_schema_id,
                           metadata=metadata, parents=tuple(parents), budget=budget)


def domain_profile(domain: str) -> DomainProfile:
    """Return a stable A–N profile by letter or service name."""
    profile = _PROFILE_BY_CODE.get(domain) or _PROFILE_BY_SERVICE.get(domain)
    if profile is None:
        raise KeyError(f"unknown Molecularis domain: {domain}")
    return profile
