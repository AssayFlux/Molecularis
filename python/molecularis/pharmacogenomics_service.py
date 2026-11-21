"""Pharmacogenomics L: provenance-bound, non-clinical phased star-allele matching."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from .pgx import AlleleMatch, StarAlleleDefinition, VariantKey, match_phased_haplotype, parse_star_allele_definitions
from .platform import Budget, Capability, MolecularisPlatform, Operation, Rulebook
from .platform.contracts import ResourceLimitError, ValidationError

PGX_SAMPLE_SCHEMA_ID = "molecularis.pharmacogenomics-sample.v1"
PGX_SAMPLE_MEDIA_TYPE = "application/vnd.molecularis.pharmacogenomics-sample+json"
PGX_DEFINITIONS_SCHEMA_ID = "molecularis.pharmacogenomics-definitions.v1"
PGX_DEFINITIONS_MEDIA_TYPE = "application/vnd.molecularis.pharmacogenomics-definitions+json"
PGX_REPORT_SCHEMA_ID = "molecularis.pharmacogenomics-report.v1"
PGX_RULEBOOK_ID = "pharmacogenomics-core-v1"
_CAPS = {
    "validate": "pharmacogenomics.validate.v1",
    "match": "pharmacogenomics.match-phased-star-alleles.v1",
}
_RULES = {
    "validate": ["PGX-001", "PGX-002", "PGX-003", "PGX-007"],
    "match": ["PGX-001", "PGX-002", "PGX-003", "PGX-004", "PGX-005", "PGX-006", "PGX-007"],
}
_MAX_CALLS = 500
_MAX_VARIANTS = 20_000
_MAX_PACK_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class HaplotypeCall:
    gene_symbol: str
    haplotype_id: str
    variants: tuple[VariantKey, ...]
    phase_confirmed: bool
    call_complete: bool


@dataclass(frozen=True, slots=True)
class PharmacogenomicsDocument:
    """Synthetic/public non-patient sample calls; each row is one already-phased haplotype."""
    identifier: str
    genome_build: str
    calls: tuple[HaplotypeCall, ...]
    data_classification: str = "synthetic_non_patient"

    def __post_init__(self) -> None:
        for name, value, limit in (
            ("identifier", self.identifier, 256), ("genome_build", self.genome_build, 128)
        ):
            if not isinstance(value, str) or not value.strip() or len(value) > limit or value != value.strip():
                raise ValueError(f"{name} must be bounded, non-empty trimmed text")
        if self.data_classification != "synthetic_non_patient":
            raise ValueError("v1 accepts synthetic_non_patient data only")
        if not isinstance(self.calls, tuple) or not 1 <= len(self.calls) <= _MAX_CALLS:
            raise ValueError(f"calls must contain 1..{_MAX_CALLS} haplotypes")
        seen: set[tuple[str, str]] = set()
        total = 0
        for call in self.calls:
            if not isinstance(call, HaplotypeCall):
                raise TypeError("calls must contain HaplotypeCall values")
            for name, value in (("gene_symbol", call.gene_symbol), ("haplotype_id", call.haplotype_id)):
                if not isinstance(value, str) or not value.strip() or len(value) > 128 or value != value.strip():
                    raise ValueError(f"{name} must be bounded, non-empty trimmed text")
            key = (call.gene_symbol, call.haplotype_id)
            if key in seen:
                raise ValueError("gene/haplotype identifiers must be unique")
            seen.add(key)
            if not isinstance(call.phase_confirmed, bool) or not isinstance(call.call_complete, bool):
                raise TypeError("phase_confirmed and call_complete must be booleans")
            if not isinstance(call.variants, tuple):
                raise TypeError("haplotype variants must be a tuple")
            total += len(call.variants)
            if len(set(call.variants)) != len(call.variants):
                raise ValueError("duplicate variant in haplotype call")
            if any(v.genome_build != self.genome_build for v in call.variants):
                raise ValueError("variant genome build does not match sample genome_build")
        if total > _MAX_VARIANTS:
            raise ValueError(f"sample exceeds {_MAX_VARIANTS} total variants")

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.to_json()).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": PGX_SAMPLE_SCHEMA_ID, "identifier": self.identifier,
            "genome_build": self.genome_build, "data_classification": self.data_classification,
            "calls": [{
                "gene_symbol": c.gene_symbol, "haplotype_id": c.haplotype_id,
                "phase_confirmed": c.phase_confirmed, "call_complete": c.call_complete,
                "variants": [{
                    "genome_build": v.genome_build, "chromosome": v.chromosome,
                    "position": v.position, "reference": v.reference, "alternate": v.alternate,
                } for v in c.variants],
            } for c in self.calls],
        }

    def to_json(self) -> bytes:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False, allow_nan=False,
                          separators=(",", ":")).encode("utf-8")

    @classmethod
    def from_json(cls, payload: bytes | str) -> "PharmacogenomicsDocument":
        def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key: {key}")
                result[key] = value
            return result
        try:
            raw = payload.decode("utf-8") if isinstance(payload, bytes) else payload
            value = json.loads(raw, object_pairs_hook=unique,
                               parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid PGx sample JSON: {exc}") from exc
        fields = {"schema", "identifier", "genome_build", "data_classification", "calls"}
        if not isinstance(value, dict) or set(value) != fields or value["schema"] != PGX_SAMPLE_SCHEMA_ID:
            raise ValueError("PGx sample fields/schema do not match v1")
        calls = []
        for item in value["calls"]:
            if not isinstance(item, dict) or set(item) != {
                "gene_symbol", "haplotype_id", "phase_confirmed", "call_complete", "variants"
            }:
                raise ValueError("PGx haplotype call fields do not match v1")
            variants = []
            for variant in item["variants"]:
                if not isinstance(variant, dict) or set(variant) != {
                    "genome_build", "chromosome", "position", "reference", "alternate"
                }:
                    raise ValueError("PGx variant fields do not match v1")
                variants.append(VariantKey(**variant))
            calls.append(HaplotypeCall(
                item["gene_symbol"], item["haplotype_id"], tuple(variants),
                item["phase_confirmed"], item["call_complete"],
            ))
        return cls(value["identifier"], value["genome_build"], tuple(calls),
                   value["data_classification"])


def ingest_pharmacogenomics(
    platform: MolecularisPlatform, record: PharmacogenomicsDocument, *,
    parents: tuple[str, ...] = (), budget: Budget | None = None,
):
    if not isinstance(record, PharmacogenomicsDocument):
        raise TypeError("record must be a PharmacogenomicsDocument")
    return platform.ingest(
        record.to_json(), media_type=PGX_SAMPLE_MEDIA_TYPE, schema_id=PGX_SAMPLE_SCHEMA_ID,
        metadata={"identifier": record.identifier, "pgx_sha256": record.sha256,
                  "genome_build": record.genome_build, "haplotype_count": len(record.calls),
                  "data_classification": record.data_classification},
        parents=parents, budget=budget,
    )


def ingest_pgx_definitions(
    platform: MolecularisPlatform, document: str | bytes, *, expected_source_release: str,
    budget: Budget | None = None,
):
    raw = document.encode("utf-8") if isinstance(document, str) else document
    if not isinstance(raw, bytes) or len(raw) > _MAX_PACK_BYTES:
        raise ValueError("PGx definitions must be bytes/text within the 2 MiB limit")
    # Parse before storage: malformed or unpinned packs never enter the artifact store.
    definitions = parse_star_allele_definitions(
        raw.decode("utf-8"), expected_source_release=expected_source_release,
        max_input_bytes=_MAX_PACK_BYTES,
    )
    digest = hashlib.sha256(raw).hexdigest()
    return platform.ingest(
        raw, media_type=PGX_DEFINITIONS_MEDIA_TYPE, schema_id=PGX_DEFINITIONS_SCHEMA_ID,
        metadata={"source_release": expected_source_release, "pack_sha256": digest,
                  "definition_count": len(definitions), "genome_build": definitions[0].genome_build},
        budget=budget,
    )


def load_pharmacogenomics(
    platform: MolecularisPlatform, artifact_id: str, *, budget: Budget | None = None,
) -> PharmacogenomicsDocument:
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.media_type != PGX_SAMPLE_MEDIA_TYPE or artifact.schema_id != PGX_SAMPLE_SCHEMA_ID:
        raise ValidationError("artifact is not a Pharmacogenomics sample v1")
    if artifact.size_bytes > budget.max_bytes:
        raise ResourceLimitError("PGx sample artifact exceeds byte budget")
    record = PharmacogenomicsDocument.from_json(b"".join(platform.store.read(artifact_id, budget=budget)))
    expected = {"identifier": record.identifier, "pgx_sha256": record.sha256,
                "genome_build": record.genome_build, "haplotype_count": len(record.calls),
                "data_classification": record.data_classification}
    if artifact.digest != record.sha256 or any(artifact.metadata.get(k) != v for k, v in expected.items()):
        raise ValidationError("PGx sample artifact integrity or metadata mismatch")
    if sum(len(c.variants) for c in record.calls) > budget.max_candidates:
        raise ResourceLimitError("PGx sample exceeds candidate budget")
    return record


def load_pgx_definitions(
    platform: MolecularisPlatform, artifact_id: str, *, budget: Budget | None = None,
) -> list[StarAlleleDefinition]:
    budget = budget or Budget()
    artifact = platform.store.get(artifact_id)
    if artifact.media_type != PGX_DEFINITIONS_MEDIA_TYPE or artifact.schema_id != PGX_DEFINITIONS_SCHEMA_ID:
        raise ValidationError("artifact is not a PGx definitions v1 pack")
    if artifact.size_bytes > min(budget.max_bytes, _MAX_PACK_BYTES):
        raise ResourceLimitError("PGx definitions exceed byte budget")
    raw = b"".join(platform.store.read(artifact_id, budget=budget))
    if hashlib.sha256(raw).hexdigest() != artifact.metadata.get("pack_sha256"):
        raise ValidationError("PGx definitions artifact digest mismatch")
    definitions = parse_star_allele_definitions(
        raw.decode("utf-8"), expected_source_release=str(artifact.metadata.get("source_release", "")),
        max_input_bytes=min(budget.max_bytes, _MAX_PACK_BYTES),
        max_definitions=budget.max_candidates,
    )
    if len(definitions) != artifact.metadata.get("definition_count"):
        raise ValidationError("PGx definitions metadata mismatch")
    if definitions[0].genome_build != artifact.metadata.get("genome_build"):
        raise ValidationError("PGx definitions genome build metadata mismatch")
    return definitions


def _match(record: PharmacogenomicsDocument, definitions: list[StarAlleleDefinition]) -> dict[str, Any]:
    output = []
    for call in record.calls:
        result: AlleleMatch = match_phased_haplotype(
            call.gene_symbol, call.variants, definitions, genome_build=record.genome_build,
            phase_confirmed=call.phase_confirmed, call_complete=call.call_complete,
        )
        output.append({
            "gene_symbol": result.gene_symbol, "haplotype_id": call.haplotype_id,
            "star_allele": result.star_allele, "status": result.status,
            "matched_definition_ids": list(result.matched_definition_ids),
            "observed_variant_count": result.observed_variant_count,
        })
    return {"matches": output, "matched_haplotypes": sum(x["status"] == "matched" for x in output),
            "unresolved_haplotypes": sum(x["status"] != "matched" for x in output),
            "interpretation_performed": False}


def register_pharmacogenomics_service(platform: MolecularisPlatform) -> None:
    descriptions = {
        "validate": "Validate a synthetic/public non-patient PGx haplotype artifact and provenance.",
        "match": "Match already-phased complete haplotypes against a release-pinned star-allele definition pack.",
    }
    for operation, capability_id in _CAPS.items():
        platform.register(Capability(
            id=capability_id, version="1.0.0", service="pharmacogenomics",
            operation=operation,
            input_schema=PGX_SAMPLE_SCHEMA_ID if operation == "validate" else PGX_SAMPLE_SCHEMA_ID + "+definitions",
            output_schema=PGX_REPORT_SCHEMA_ID, deterministic=True,
            description=descriptions[operation],
        ))
        def handler(inputs, parameters, context, selected=operation):
            values = list(inputs.values())
            expected_count = 1 if selected == "validate" else 2
            if len(values) != expected_count or any(not isinstance(v, str) for v in values):
                raise ValidationError(f"PGx {selected} requires {expected_count} artifact input(s)")
            record = load_pharmacogenomics(platform, values[0], budget=context.budget)
            if selected == "validate":
                result = {"valid": True, "haplotype_count": len(record.calls),
                          "genome_build": record.genome_build, "data_classification": record.data_classification}
            else:
                definitions = load_pgx_definitions(platform, values[1], budget=context.budget)
                if any(d.genome_build != record.genome_build for d in definitions):
                    raise ValidationError("sample and star-allele definition genome builds differ")
                result = _match(record, definitions)
            return {
                "schema": PGX_REPORT_SCHEMA_ID, "operation": selected,
                "sample_id": record.identifier, "sample_sha256": record.sha256,
                "result": result, "rulebook": PGX_RULEBOOK_ID,
                "rules_checked": list(_RULES[selected]),
                "limitations": [
                    "v1 is restricted to synthetic_non_patient data; patient/clinical records are rejected.",
                    "Only caller-supplied, already-phased, complete haplotypes are eligible for matching.",
                    "No phase inference, variant calling, copy-number or structural-allele analysis is performed.",
                    "No diplotype-to-phenotype translation, CPIC guideline interpretation, drug selection, dosing or treatment recommendation is performed.",
                    "A no-match or no-call is not evidence that an allele is absent; definition packs may be incomplete.",
                    "Variant representation and genome build must already agree with the pinned definition pack.",
                    "Definition source metadata and licensing are caller-supplied and require independent audit.",
                ],
            }
        platform.bind(capability_id, handler)


def pharmacogenomics_rulebook(
    operation: str, *, sample_key: str = "pgx_sample_artifact_id",
    definitions_key: str = "pgx_definitions_artifact_id",
) -> Rulebook:
    if operation not in _CAPS:
        raise ValueError(f"unsupported pharmacogenomics operation: {operation}")
    if not sample_key.strip() or not definitions_key.strip():
        raise ValueError("artifact input keys must be non-empty")
    inputs = (sample_key,) if operation == "validate" else (sample_key, definitions_key)
    return Rulebook(
        id=PGX_RULEBOOK_ID, version="1.0.0",
        operations=(Operation(id=f"{operation}-pharmacogenomics",
                              capability_id=_CAPS[operation], inputs=inputs,
                              output="pharmacogenomics_result", parameters={}),),
    )
