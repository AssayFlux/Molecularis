"""Strict bounded parser for HMMER hmmscan --domtblout profile-search evidence.

The parser does not execute HMMER or certify profile licensing/biological validity.
It preserves HMMER statistics as reported and labels matches as candidates only.
"""
from __future__ import annotations

import math
from typing import Iterable
from urllib.parse import urlparse


def parse_hmmscan_domtblout(
    lines: Iterable[str],
    *,
    hmmer_version: str,
    profile_pack: dict[str, str],
    max_lines: int = 2_000_000,
    max_line_bytes: int = 16_384,
    max_domains: int = 1_000_000,
) -> dict[str, object]:
    """Parse hmmscan domtblout (one-based inclusive coordinates) under strict limits."""
    if not isinstance(hmmer_version, str) or not hmmer_version.strip():
        raise ValueError("hmmer_version must be non-empty")
    required_metadata = ("name", "version", "license", "source", "content_sha256")
    if any(not isinstance(profile_pack.get(key), str) or not profile_pack[key].strip()
           for key in required_metadata):
        raise ValueError("profile_pack requires name, version, license, source and content_sha256")
    source = urlparse(profile_pack["source"])
    if source.scheme not in {"https", "http", "doi"}:
        raise ValueError("profile_pack source must be an http(s) or doi URI")
    digest = profile_pack["content_sha256"]
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ValueError("profile_pack content_sha256 must be lowercase SHA-256 hex")
    for name, value in (
        ("max_lines", max_lines),
        ("max_line_bytes", max_line_bytes),
        ("max_domains", max_domains),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")

    hits: list[dict[str, object]] = []
    query_lengths: dict[str, int] = {}
    profile_lengths: dict[str, int] = {}
    domain_groups: dict[tuple[str, str], tuple[int, set[int]]] = {}
    line_count = 0
    for line_count, raw in enumerate(lines, 1):
        if line_count > max_lines:
            raise ValueError("HMMER domtblout exceeds max_lines")
        if not isinstance(raw, str):
            raise TypeError("HMMER domtblout lines must be text")
        if len(raw.encode("utf-8")) > max_line_bytes:
            raise ValueError("HMMER domtblout line exceeds max_line_bytes")
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(maxsplit=22)
        if len(fields) < 22:
            raise ValueError(f"HMMER domtblout line {line_count} has fewer than 22 fields")
        try:
            profile_length = int(fields[2])
            query_length = int(fields[5])
            domain_number = int(fields[9])
            domain_count = int(fields[10])
            full_evalue = float(fields[6])
            full_score = float(fields[7])
            conditional_evalue = float(fields[11])
            independent_evalue = float(fields[12])
            domain_score = float(fields[13])
            hmm_start, hmm_end = int(fields[15]), int(fields[16])
            ali_start, ali_end = int(fields[17]), int(fields[18])
            env_start, env_end = int(fields[19]), int(fields[20])
            accuracy = float(fields[21])
        except ValueError as exc:
            raise ValueError(
                f"HMMER domtblout line {line_count} contains invalid numeric fields"
            ) from exc
        numeric = (
            full_evalue, full_score, conditional_evalue, independent_evalue,
            domain_score, accuracy,
        )
        if any(not math.isfinite(value) for value in numeric):
            raise ValueError(f"HMMER domtblout line {line_count} contains non-finite statistics")
        if any(value < 0 for value in (full_evalue, conditional_evalue, independent_evalue)):
            raise ValueError(f"HMMER domtblout line {line_count} contains a negative E-value")
        if profile_length < 1 or query_length < 1 or domain_number < 1 or domain_count < 1:
            raise ValueError(
                f"HMMER domtblout line {line_count} contains invalid lengths or domain indices"
            )
        if domain_number > domain_count:
            raise ValueError(f"HMMER domtblout line {line_count} has an invalid domain index")
        if not (
            1 <= hmm_start <= hmm_end <= profile_length
            and 1 <= ali_start <= ali_end <= query_length
            and 1 <= env_start <= env_end <= query_length
            and env_start <= ali_start <= ali_end <= env_end
            and 0.0 <= accuracy <= 1.0
        ):
            raise ValueError(
                f"HMMER domtblout line {line_count} has invalid coordinates or accuracy"
            )
        if len(hits) >= max_domains:
            raise ValueError("HMMER domtblout exceeds max_domains")
        profile_id, query_id = fields[0], fields[3]
        if not profile_id or not query_id:
            raise ValueError(f"HMMER domtblout line {line_count} has an empty profile or query ID")
        previous_profile_length = profile_lengths.setdefault(profile_id, profile_length)
        if previous_profile_length != profile_length:
            raise ValueError(f"HMMER profile {profile_id!r} has inconsistent reported lengths")
        group_key = (profile_id, query_id)
        group_count, group_numbers = domain_groups.setdefault(group_key, (domain_count, set()))
        if group_count != domain_count or domain_number in group_numbers:
            raise ValueError(f"HMMER profile/query {group_key!r} has inconsistent domain indices")
        group_numbers.add(domain_number)
        previous_length = query_lengths.setdefault(query_id, query_length)
        if previous_length != query_length:
            raise ValueError(f"HMMER query {query_id!r} has inconsistent reported lengths")
        hits.append({
            "profile_id": profile_id,
            "profile_accession": None if fields[1] == "-" else fields[1],
            "profile_length": profile_length,
            "query_id": query_id,
            "query_accession": None if fields[4] == "-" else fields[4],
            "query_length": query_length,
            "full_sequence_evalue": full_evalue,
            "full_sequence_score": full_score,
            "domain_number": domain_number,
            "domain_count": domain_count,
            "conditional_evalue": conditional_evalue,
            "independent_evalue": independent_evalue,
            "domain_score": domain_score,
            "hmm_start_1based": hmm_start,
            "hmm_end_1based": hmm_end,
            "alignment_start_1based": ali_start,
            "alignment_end_1based": ali_end,
            "envelope_start_1based": env_start,
            "envelope_end_1based": env_end,
            "accuracy": accuracy,
            "description": fields[22] if len(fields) > 22 else "",
        })

    return {
        "schema": "kinetics.hmmscan-domain-evidence.v1",
        "tool": "hmmscan",
        "hmmer_version": hmmer_version,
        "profile_pack": dict(profile_pack),
        "query_count": len(query_lengths),
        "domain_hit_count": len(hits),
        "hits": hits,
        "conclusion": {
            "status": "profile_matches_reported" if hits else "no_profile_matches_reported",
            "family_or_domain_assignment": (
                "candidate_profile_matches_require_review" if hits else "not_established"
            ),
            "function": "not_inferred",
            "novelty": "not_established",
        },
        "limitations": [
            "Parses caller-supplied HMMER hmmscan domtblout; does not execute HMMER",
            ("Profile identity and licensing metadata are caller-supplied and not "
             "independently authenticated"),
            ("Profile matches are candidates and require threshold, coverage, provenance "
             "and expert review"),
            ("No protein function, pathogenicity, organism identity or biological validity "
             "is inferred"),
        ],
    }
