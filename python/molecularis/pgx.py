"""Provenance-first PGx allele-definition foundations; no clinical interpretation.

Definitions must be imported from reviewed, versioned sources. This module only
matches fully phased small-variant sets to explicitly supplied allele definitions.
It does not infer phase, copy number, structural alleles, phenotype or treatment.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterable, cast


@dataclass(frozen=True, order=True)
class VariantKey:
    genome_build: str
    chromosome: str
    position: int
    reference: str
    alternate: str

    def __post_init__(self) -> None:
        if not isinstance(self.genome_build, str) or not isinstance(self.chromosome, str) or not self.genome_build.strip() or not self.chromosome.strip():
            raise ValueError("Variant requires genome build and chromosome")
        if not isinstance(self.position, int) or isinstance(self.position, bool) or self.position < 1:
            raise ValueError("Variant position must be a positive 1-based integer")
        if not self.reference or not self.alternate or self.reference.upper() == self.alternate.upper():
            raise ValueError("Variant requires distinct non-empty REF and ALT alleles")
        if any(base not in "ACGT" for base in (self.reference + self.alternate).upper()):
            raise ValueError("Only normalized literal A/C/G/T variants are supported")
        object.__setattr__(self, "reference", self.reference.upper())
        object.__setattr__(self, "alternate", self.alternate.upper())


@dataclass(frozen=True)
class StarAlleleDefinition:
    gene_symbol: str
    star_allele: str
    required_variants: frozenset[VariantKey]
    excluded_variants: frozenset[VariantKey]
    source_name: str
    source_release: str
    source_url: str
    source_sha256: str
    license_id: str
    genome_build: str
    definition_id: str


@dataclass(frozen=True)
class AlleleMatch:
    gene_symbol: str
    star_allele: str | None
    status: str
    matched_definition_ids: tuple[str, ...]
    observed_variant_count: int


def parse_star_allele_definitions(
    document: str, *, expected_source_release: str,
    max_input_bytes: int = 2 * 1024 * 1024,
    max_definitions: int = 10_000,
    max_variants_per_definition: int = 1_000,
) -> list[StarAlleleDefinition]:
    """Load a bounded JSON definition pack with mandatory provenance metadata."""
    for name, limit in (
        ("max_input_bytes", max_input_bytes),
        ("max_definitions", max_definitions),
        ("max_variants_per_definition", max_variants_per_definition),
    ):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError(f"{name} must be a positive integer")
    if not isinstance(document, str):
        raise TypeError("PGx definition pack must be text")
    if len(document) > max_input_bytes:
        raise ValueError("PGx definition pack exceeds configured max_input_bytes")
    if len(document.encode("utf-8")) > max_input_bytes:
        raise ValueError("PGx definition pack exceeds configured max_input_bytes")
    try:
        value = json.loads(document)
    except json.JSONDecodeError as error:
        raise ValueError("PGx definition pack must be valid JSON") from error
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("Unsupported PGx definition schema version")
    value = cast(dict[str, object], value)
    source_raw = value.get("source")
    if not isinstance(source_raw, dict):
        raise ValueError("PGx definition source metadata is mandatory")
    source = cast(dict[str, object], source_raw)

    def required_string(data: dict[str, object], key: str) -> str:
        item = data.get(key)
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"PGx definition requires non-empty {key}")
        return item

    source_name = required_string(source, "name")
    source_release = required_string(source, "release")
    source_url = required_string(source, "url")
    license_id = required_string(source, "license")
    source_sha256 = required_string(source, "sha256")
    genome_build = required_string(value, "genome_build")
    if not source_url.startswith("https://"):
        raise ValueError("PGx source URL must use HTTPS")
    if not re.fullmatch(r"[a-fA-F0-9]{64}", source_sha256):
        raise ValueError("PGx source SHA-256 must be 64 hexadecimal characters")
    if source_release != expected_source_release:
        raise ValueError("PGx source release does not match the pinned release")
    raw_definitions = value.get("definitions")
    if not isinstance(raw_definitions, list) or not raw_definitions:
        raise ValueError("PGx definition pack must contain allele definitions")
    if len(raw_definitions) > max_definitions:
        raise ValueError("PGx definition count exceeds configured max_definitions")

    definitions: list[StarAlleleDefinition] = []
    seen: set[tuple[str, str, str]] = set()

    def variants(raw: object) -> frozenset[VariantKey]:
        if not isinstance(raw, list):
            raise ValueError("Allele variants must be arrays")
        if len(raw) > max_variants_per_definition:
            raise ValueError(
                "Allele variant count exceeds configured max_variants_per_definition"
            )
        result: set[VariantKey] = set()
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError("Variant definition must be an object")
            item_data = cast(dict[str, object], item)
            position = item_data.get("position")
            if not isinstance(position, int) or isinstance(position, bool):
                raise ValueError("Variant position must be an integer")
            variant = VariantKey(
                genome_build=genome_build,
                chromosome=str(item_data.get("chromosome", "")),
                position=position,
                reference=str(item_data.get("ref", "")).upper(),
                alternate=str(item_data.get("alt", "")).upper(),
            )
            if variant in result:
                raise ValueError("Duplicate variant in allele definition")
            result.add(variant)
        return frozenset(result)

    for raw in raw_definitions:
        if not isinstance(raw, dict):
            raise ValueError("Allele definition must be an object")
        raw_data = cast(dict[str, object], raw)
        gene = required_string(raw_data, "gene")
        star = required_string(raw_data, "star_allele")
        definition_id = required_string(raw_data, "id")
        if not star.startswith("*"):
            raise ValueError("Star allele names must begin with '*'")
        key = (gene, star, definition_id)
        if key in seen:
            raise ValueError("Duplicate PGx allele definition identifier")
        seen.add(key)
        required = variants(raw_data.get("required_variants", []))
        excluded = variants(raw_data.get("excluded_variants", []))
        if required & excluded:
            raise ValueError("A variant cannot be both required and excluded")
        definitions.append(StarAlleleDefinition(
            gene, star, required, excluded, source_name, source_release,
            source_url, source_sha256.lower(), license_id, genome_build, definition_id,
        ))
    return definitions


def match_phased_haplotype(
    gene_symbol: str, observed_variants: Iterable[VariantKey],
    definitions: Iterable[StarAlleleDefinition], *, genome_build: str,
    phase_confirmed: bool, call_complete: bool = False,
) -> AlleleMatch:
    """Match one completely called, already phased haplotype; never infer missing calls."""
    if not phase_confirmed:
        return AlleleMatch(gene_symbol, None, "no_call_unphased", (), 0)
    if not call_complete:
        return AlleleMatch(gene_symbol, None, "no_call_incomplete", (), 0)
    observed = frozenset(observed_variants)
    if any(variant.genome_build != genome_build for variant in observed):
        raise ValueError("Observed variants do not match requested genome build")
    candidates = [
        definition for definition in definitions
        if definition.gene_symbol == gene_symbol and definition.genome_build == genome_build
        and definition.required_variants.issubset(observed)
        and not (definition.excluded_variants & observed)
    ]
    if not candidates:
        return AlleleMatch(gene_symbol, None, "no_matching_definition", (), len(observed))
    # A definition with more required variants is more specific, but tied best
    # definitions remain ambiguous rather than being resolved by file order.
    specificity = max(len(item.required_variants) for item in candidates)
    best = [item for item in candidates if len(item.required_variants) == specificity]
    names = sorted({item.star_allele for item in best})
    if len(names) != 1:
        return AlleleMatch(
            gene_symbol, None, "ambiguous", tuple(sorted(item.definition_id for item in best)),
            len(observed),
        )
    return AlleleMatch(
        gene_symbol, names[0], "matched", tuple(sorted(item.definition_id for item in best)),
        len(observed),
    )
