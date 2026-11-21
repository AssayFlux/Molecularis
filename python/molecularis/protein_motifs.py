"""Bounded, provenance-aware protein motif matching for S6/S9.

Patterns are caller-supplied fixed-width strings: canonical amino acids match
literally and '.' matches any one canonical amino acid. This is not a motif
discovery engine, homology search, family classifier, or functional annotator.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from urllib.parse import urlparse


_CANONICAL = frozenset("ACDEFGHIKLMNPQRSTVWY")


@dataclass(frozen=True)
class MotifPack:
    name: str
    version: str
    license: str
    source: str
    content_sha256: str

    def validate(self) -> None:
        fields = (self.name, self.version, self.license, self.source, self.content_sha256)
        if any(not isinstance(value, str) or not value.strip() for value in fields):
            raise ValueError("Motif-pack metadata fields must be non-empty strings")
        parsed = urlparse(self.source)
        if parsed.scheme not in {"https", "http", "doi"}:
            raise ValueError("Motif-pack source must be an http(s) or doi URI")
        if len(self.content_sha256) != 64 or any(
            char not in "0123456789abcdef" for char in self.content_sha256
        ):
            raise ValueError("Motif-pack content_sha256 must be lowercase SHA-256 hex")


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Motif-pack JSON contains duplicate key {key!r}")
        result[key] = value
    return result


def scan_protein_motif_pack(
    query: str,
    motif_pack_bytes: bytes,
    *,
    motif_pack: MotifPack,
    max_pack_bytes: int = 2 * 1024 * 1024,
    max_motifs: int = 10_000,
    max_query_residues: int = 5_000_000,
    max_comparisons: int = 50_000_000,
    max_hits: int = 100_000,
) -> dict[str, object]:
    """Scan a protein sequence against a hash-pinned, caller-supplied motif pack.

    Motif JSON schema: {"schema_version": 1, "motifs": [
      {"id": "motif-id", "pattern": "A..G", "description": "optional"}
    ]}. A dot is a single-residue wildcard. No regular expressions are used.
    """
    motif_pack.validate()
    if not isinstance(motif_pack_bytes, bytes):
        raise TypeError("motif_pack_bytes must be bytes")
    limits = {
        "max_pack_bytes": max_pack_bytes,
        "max_motifs": max_motifs,
        "max_query_residues": max_query_residues,
        "max_comparisons": max_comparisons,
        "max_hits": max_hits,
    }
    for name, value in limits.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if len(motif_pack_bytes) > max_pack_bytes:
        raise ValueError("Motif pack exceeds max_pack_bytes limit")
    actual_digest = sha256(motif_pack_bytes).hexdigest()
    if actual_digest != motif_pack.content_sha256:
        raise ValueError("Motif-pack bytes do not match the declared SHA-256")

    normalized = "".join(query.split()).upper() if isinstance(query, str) else ""
    if not normalized:
        raise ValueError("Protein query must not be empty")
    if len(normalized) > max_query_residues:
        raise ValueError("Protein query exceeds max_query_residues limit")
    invalid = sorted(set(normalized) - _CANONICAL)
    if invalid:
        raise ValueError(f"Protein query contains unsupported residues: {''.join(invalid)}")

    try:
        document = json.loads(
            motif_pack_bytes.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"Invalid JSON constant: {value}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Motif pack must be valid UTF-8 JSON") from exc
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("Motif pack must use schema_version 1")
    definitions = document.get("motifs")
    if not isinstance(definitions, list) or not definitions:
        raise ValueError("Motif pack must contain a non-empty motifs list")
    if len(definitions) > max_motifs:
        raise ValueError("Motif pack exceeds max_motifs limit")

    validated: list[tuple[str, str, str]] = []
    identifiers: set[str] = set()
    comparisons = 0
    for definition in definitions:
        if not isinstance(definition, dict):
            raise ValueError("Every motif definition must be an object")
        identifier, pattern = definition.get("id"), definition.get("pattern")
        description = definition.get("description", "")
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError("Every motif requires a non-empty id")
        if identifier in identifiers:
            raise ValueError("Motif identifiers must be unique")
        identifiers.add(identifier)
        if not isinstance(pattern, str):
            raise ValueError(f"Motif {identifier!r} pattern must be text")
        pattern = pattern.upper()
        if not 2 <= len(pattern) <= 64 or any(
            char not in _CANONICAL and char != "." for char in pattern
        ):
            raise ValueError(
                f"Motif {identifier!r} must be 2-64 residues using canonical amino acids or '.'"
            )
        if not isinstance(description, str):
            raise ValueError(f"Motif {identifier!r} description must be text")
        comparisons += max(0, len(normalized) - len(pattern) + 1) * len(pattern)
        if comparisons > max_comparisons:
            raise ValueError("Motif scan exceeds max_comparisons limit")
        validated.append((identifier, pattern, description))

    hits: list[dict[str, object]] = []
    for identifier, pattern, description in sorted(validated):
        width = len(pattern)
        for start in range(len(normalized) - width + 1):
            window = normalized[start : start + width]
            if all(expected == "." or expected == observed
                   for expected, observed in zip(pattern, window, strict=True)):
                if len(hits) >= max_hits:
                    raise ValueError("Motif scan exceeds max_hits limit")
                hits.append({
                    "motif_id": identifier,
                    "pattern": pattern,
                    "description": description,
                    "start_1based": start + 1,
                    "end_1based": start + width,
                    "matched_sequence": window,
                    "evidence_type": "caller_supplied_fixed_width_motif_match",
                })

    return {
        "schema": "kinetics.protein-motif-scan.v1",
        "query": {
            "sequence_sha256": sha256(normalized.encode("ascii")).hexdigest(),
            "length": len(normalized),
        },
        "search": {
            "algorithm": "bounded-fixed-width-motif-scan-v1",
            "motif_pack": {
                "name": motif_pack.name,
                "version": motif_pack.version,
                "license": motif_pack.license,
                "source": motif_pack.source,
                "content_sha256": actual_digest,
            },
            "motif_count": len(validated),
            "comparison_budget_used": comparisons,
            "max_comparisons": max_comparisons,
        },
        "hits": hits,
        "conclusion": {
            "status": "motif_matches_found" if hits else "no_motif_match",
            "family_or_function": "not_inferred",
            "novelty": "not_established",
        },
        "limitations": [
            "Matches only caller-supplied fixed-width motifs; no motif discovery is performed.",
            "A motif match does not establish protein family, domain, function or biological activity.",
            "A no-match result is not evidence of novelty or absence of a functional site.",
            "Motif-pack source, version, licence and biological validity require independent review.",
            "No homology alignment, profile scoring, E-value or calibrated confidence is computed.",
        ],
    }
