"""Bounded GFF3 v3 annotation import; does not predict or validate biology."""
from __future__ import annotations

from collections import Counter
import math
from typing import TypedDict
from urllib.parse import unquote


class _Feature(TypedDict):
    seqid: str
    source: str
    type: str
    start: int
    end: int
    score: float | None
    strand: str
    phase: int | None
    attributes: dict[str, str]


def parse_gff3(
    lines: object,
    *,
    max_lines: int = 2_000_000,
    max_features: int = 1_000_000,
    max_attribute_bytes: int = 16_384,
    max_total_attribute_bytes: int = 64 * 1024 * 1024,
) -> dict[str, object]:
    """Validate GFF3 structure, feature IDs, parent graph and coordinate bounds."""
    limits = {
        "max_lines": max_lines,
        "max_features": max_features,
        "max_attribute_bytes": max_attribute_bytes,
        "max_total_attribute_bytes": max_total_attribute_bytes,
    }
    for name, value in limits.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if not hasattr(lines, "__iter__"):
        raise TypeError("lines must be an iterable of text lines")

    features: list[_Feature] = []
    ids: dict[str, _Feature] = {}
    parent_graph: dict[str, tuple[str, ...]] = {}
    regions: dict[str, tuple[int, int]] = {}
    counts: Counter[str] = Counter()
    attribute_bytes = 0
    saw_version = False
    saw_fasta = False
    line_count = 0

    for line_count, raw in enumerate(lines, 1):
        if line_count > max_lines:
            raise ValueError("GFF3 input exceeds max_lines")
        if not isinstance(raw, str):
            raise TypeError("GFF3 lines must be text")
        line = raw.rstrip("\r\n")
        if not line:
            continue
        if saw_fasta:
            continue
        if line == "##FASTA":
            saw_fasta = True
            continue
        if line.startswith("##"):
            if line == "##gff-version 3":
                if saw_version:
                    raise ValueError("GFF3 version directive must occur once")
                saw_version = True
            elif line.startswith("##sequence-region "):
                fields = line.split()
                if len(fields) != 4:
                    raise ValueError("Malformed GFF3 sequence-region directive")
                try:
                    start, end = int(fields[2]), int(fields[3])
                except ValueError as exc:
                    raise ValueError("Invalid GFF3 sequence-region coordinates") from exc
                if not fields[1] or start < 1 or end < start or fields[1] in regions:
                    raise ValueError("Invalid or duplicate GFF3 sequence-region")
                regions[fields[1]] = (start, end)
            continue
        if line.startswith("#"):
            continue

        cols = line.split("\t")
        if len(cols) != 9:
            raise ValueError(f"GFF3 line {line_count} must contain nine columns")
        seqid, source, kind, start_s, end_s, score_s, strand, phase_s, attr_s = cols
        if not seqid or not source or not kind:
            raise ValueError("GFF3 seqid, source and type must be non-empty")
        try:
            start, end = int(start_s), int(end_s)
        except ValueError as exc:
            raise ValueError("GFF3 coordinates must be integers") from exc
        if start < 1 or end < start:
            raise ValueError("GFF3 coordinates must be positive, ordered and 1-based")
        if score_s == ".":
            score = None
        else:
            try:
                score = float(score_s)
            except ValueError as exc:
                raise ValueError("GFF3 score must be numeric or '.'") from exc
            if not math.isfinite(score):
                raise ValueError("GFF3 score must be finite")
        if strand not in {"+", "-", ".", "?"}:
            raise ValueError("Invalid GFF3 strand")
        if kind == "CDS":
            if phase_s not in {"0", "1", "2"}:
                raise ValueError("CDS phase must be 0, 1 or 2")
            phase: int | None = int(phase_s)
        else:
            if phase_s != ".":
                raise ValueError("Non-CDS feature phase must be '.'")
            phase = None

        encoded_size = len(attr_s.encode("utf-8"))
        attribute_bytes += encoded_size
        if encoded_size > max_attribute_bytes:
            raise ValueError("GFF3 feature exceeds max_attribute_bytes")
        if attribute_bytes > max_total_attribute_bytes:
            raise ValueError("GFF3 input exceeds max_total_attribute_bytes")
        attrs: dict[str, str] = {}
        if attr_s != ".":
            for item in attr_s.split(";"):
                if not item or "=" not in item:
                    raise ValueError("GFF3 attributes must be key=value pairs")
                key_raw, value_raw = item.split("=", 1)
                try:
                    attribute_key = unquote(key_raw, errors="strict")
                    attribute_value = unquote(value_raw, errors="strict")
                except UnicodeDecodeError as exc:
                    raise ValueError("GFF3 attributes contain invalid UTF-8 escapes") from exc
                if not attribute_key or attribute_key in attrs:
                    raise ValueError("GFF3 attribute keys must be non-empty and unique")
                attrs[attribute_key] = attribute_value

        identifier = attrs.get("ID")
        if identifier is not None:
            if not identifier or identifier in ids:
                raise ValueError("GFF3 feature IDs must be non-empty and globally unique")
        parents = tuple(attrs.get("Parent", "").split(",")) if attrs.get("Parent") else ()
        if any(not parent for parent in parents) or len(set(parents)) != len(parents):
            raise ValueError("GFF3 Parent references must be non-empty and unique")
        feature: _Feature = {
            "seqid": seqid, "source": source, "type": kind, "start": start, "end": end,
            "score": score, "strand": strand, "phase": phase, "attributes": attrs,
        }
        features.append(feature)
        counts[kind] += 1
        if identifier is not None:
            ids[identifier] = feature
            parent_graph[identifier] = parents
        elif parents:
            parent_graph[f"@anonymous-{len(features)}"] = parents
        if len(features) > max_features:
            raise ValueError("GFF3 input exceeds max_features")

    if not saw_version:
        raise ValueError("GFF3 version 3 directive is required")
    for feature in features:
        region = regions.get(feature["seqid"])
        if region and (feature["start"] < region[0] or feature["end"] > region[1]):
            raise ValueError("GFF3 feature lies outside its sequence-region")
        raw_parents = feature["attributes"].get("Parent", "")
        for parent_identifier in raw_parents.split(",") if raw_parents else ():
            parent_feature = ids.get(parent_identifier)
            if parent_feature is None:
                raise ValueError(f"GFF3 Parent {parent_identifier!r} does not resolve to an ID")
            if (
                parent_feature["seqid"] != feature["seqid"]
                or parent_feature["start"] > feature["start"]
                or parent_feature["end"] < feature["end"]
            ):
                raise ValueError("GFF3 child feature must lie within its parent on the same sequence")

    # Iterative DFS avoids Python recursion limits on adversarially deep graphs.
    visited: set[str] = set()
    for root in ids:
        if root in visited:
            continue
        active: set[str] = set()
        stack: list[tuple[str, bool]] = [(root, False)]
        while stack:
            identifier, exiting = stack.pop()
            if exiting:
                active.discard(identifier)
                visited.add(identifier)
                continue
            if identifier in active:
                raise ValueError("GFF3 Parent graph contains a cycle")
            if identifier in visited:
                continue
            active.add(identifier)
            stack.append((identifier, True))
            for parent_identifier in reversed(parent_graph.get(identifier, ())):
                if parent_identifier in active:
                    raise ValueError("GFF3 Parent graph contains a cycle")
                if parent_identifier in ids and parent_identifier not in visited:
                    stack.append((parent_identifier, False))

    seqids = sorted({str(feature["seqid"]) for feature in features})
    return {
        "schema": "kinetics.gff3-annotation-import.v1",
        "format": "GFF3",
        "feature_count": len(features),
        "features": features,
        "sequence_count": len(seqids),
        "sequence_ids": seqids,
        "feature_type_counts": dict(sorted(counts.items())),
        "identified_feature_count": len(ids),
        "parent_edge_count": sum(len(value) for value in parent_graph.values()),
        "sequence_regions": {
            key: {"start": value[0], "end": value[1]} for key, value in sorted(regions.items())
        },
        "coordinate_system": "1-based inclusive (GFF3)",
        "resource_limits": {**limits, "lines_read": line_count, "attribute_bytes_read": attribute_bytes},
        "limitations": [
            "Imports supplied annotations; does not predict genes, transcripts or splice sites.",
            "No taxonomy, organism class, function, pathway or biological correctness is inferred.",
            "Embedded FASTA is ignored; sequence/annotation concordance is not checked.",
            "CDS phases are range-checked only; translation and splice consistency are not validated.",
            "Structural validity does not establish annotation quality or experimental support.",
        ],
    }
