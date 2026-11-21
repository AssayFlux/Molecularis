"""PharmVar release-pinned TSV allele-definition ingestion.

Coordinates are preserved against the PharmVar reference accession (RefSeqGene/LRG or
chromosome accession); they are not silently relabelled as GRCh37/GRCh38 coordinates.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re
from dataclasses import dataclass
from typing import Iterable


def normalize(value: str) -> str:
    """Normalize TSV header labels for matching documented column aliases."""
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


@dataclass(frozen=True)
class PharmVarVariant:
    reference_accession: str
    start: int
    stop: int
    reference_allele: str
    variant_allele: str
    variant_type: str
    rsid: str | None = None

    def __post_init__(self) -> None:
        if not self.reference_accession.strip():
            raise ValueError("PharmVar variant requires a reference accession")
        if (
            isinstance(self.start, bool) or not isinstance(self.start, int)
            or isinstance(self.stop, bool) or not isinstance(self.stop, int)
        ):
            raise ValueError("PharmVar variant coordinates must be integers")
        if self.start < 1 or self.stop < self.start:
            raise ValueError("PharmVar variant coordinates must be positive and ordered")
        if not self.reference_allele or not self.variant_allele or not self.variant_type.strip():
            raise ValueError("PharmVar variant requires REF, ALT and variant type")
        if self.reference_allele.upper() == "REFERENCE" or self.variant_allele == ".":
            raise ValueError("Reference-haplotype sentinel is not a variant record")
        allowed = set("ACGTN-")
        if any(base not in allowed for base in (self.reference_allele + self.variant_allele).upper()):
            raise ValueError("PharmVar allele strings contain unsupported symbols")
        object.__setattr__(self, "reference_allele", self.reference_allele.upper())
        object.__setattr__(self, "variant_allele", self.variant_allele.upper())
        object.__setattr__(self, "variant_type", self.variant_type.casefold())
        if self.rsid == "." or self.rsid == "":
            object.__setattr__(self, "rsid", None)


@dataclass(frozen=True)
class PharmVarAlleleDefinition:
    gene_symbol: str
    haplotype: str
    reference_accession: str
    variants: frozenset[PharmVarVariant]
    is_reference: bool
    source_release: str
    source_url: str
    source_sha256: str
    license_id: str


@dataclass(frozen=True)
class PharmVarMatch:
    gene_symbol: str
    haplotype: str | None
    status: str
    matched_haplotypes: tuple[str, ...]
    observed_variant_count: int


def parse_pharmvar_tsv(
    document: str | bytes, *, source_release: str, source_url: str,
    source_sha256: str, license_id: str,
    expected_release: str,
    max_input_bytes: int = 10 * 1024 * 1024,
    max_rows: int = 100_000,
) -> list[PharmVarAlleleDefinition]:
    """Parse a bounded, release-pinned PharmVar TSV and verify its exact-byte checksum."""
    if not source_release or source_release != expected_release:
        raise ValueError("PharmVar release does not match the pinned expected release")
    if not source_url.startswith("https://") or not license_id.strip():
        raise ValueError("PharmVar source HTTPS URL and license identifier are mandatory")
    if not re.fullmatch(r"[a-fA-F0-9]{64}", source_sha256):
        raise ValueError("PharmVar source SHA-256 must be 64 hexadecimal characters")
    for name, limit in (("max_input_bytes", max_input_bytes), ("max_rows", max_rows)):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError(f"{name} must be a positive integer")
    if isinstance(document, bytes):
        raw_bytes = document
    elif isinstance(document, str):
        if len(document) > max_input_bytes:
            raise ValueError("PharmVar TSV exceeds configured max_input_bytes")
        raw_bytes = document.encode("utf-8")
    else:
        raise TypeError("PharmVar TSV document must be text or bytes")
    if len(raw_bytes) > max_input_bytes:
        raise ValueError("PharmVar TSV exceeds configured max_input_bytes")
    actual_hash = hashlib.sha256(raw_bytes).hexdigest()
    if actual_hash.lower() != source_sha256.lower():
        raise ValueError("PharmVar TSV SHA-256 does not match the pinned source checksum")
    text = raw_bytes.decode("utf-8-sig", errors="strict")

    source_lines = (
        line for line in io.StringIO(text)
        if line.strip() and not line.lstrip().startswith("#")
    )
    reader = csv.DictReader(source_lines, delimiter="\t")
    if reader.fieldnames is None:
        raise ValueError("PharmVar TSV header is missing")
    normalized_headers = [normalize(name) for name in reader.fieldnames]
    if any(not name for name in normalized_headers):
        raise ValueError("PharmVar TSV header contains an empty column name")
    if len(set(normalized_headers)) != len(normalized_headers):
        raise ValueError("PharmVar TSV header contains duplicate column names")
    if len(reader.fieldnames) != 9:
        raise ValueError("PharmVar TSV must contain exactly nine documented columns")
    columns = {normalize(name): name for name in reader.fieldnames}
    aliases = {
        "haplotype": ("haplotypeidentifier", "haplotype", "haplotypename", "allele", "name"),
        "gene": ("genesymbol", "gene"),
        "rsid": ("dbsnprs id", "dbsnprsid", "rsid"),
        "reference": ("referencesequence", "reference", "refseq"),
        "start": ("variantstart", "start"),
        "stop": ("variantstop", "stop"),
        "ref": ("referenceallele", "ref"),
        "alt": ("variantallele", "alt"),
        "type": ("varianttype", "type"),
    }
    selected: dict[str, str] = {}
    for field_name, candidates in aliases.items():
        found = next((columns[normalize(candidate)] for candidate in candidates
                      if normalize(candidate) in columns), None)
        if found is None:
            raise ValueError(f"PharmVar TSV is missing required {field_name} column")
        selected[field_name] = found

    grouped: dict[tuple[str, str, str], list[PharmVarVariant]] = {}
    reference_groups: set[tuple[str, str, str]] = set()
    row_count = 0
    for line_number, row in enumerate(reader, 2):
        row_count += 1
        if row_count > max_rows:
            raise ValueError("PharmVar TSV exceeds configured max_rows")
        if None in row or any(row.get(column) is None for column in reader.fieldnames):
            raise ValueError(f"PharmVar TSV line {line_number}: row must contain exactly nine fields")
        gene = (row.get(selected["gene"]) or "").strip()
        haplotype = (row.get(selected["haplotype"]) or "").strip()
        reference = (row.get(selected["reference"]) or "").strip()
        if not gene or not haplotype or not reference:
            raise ValueError(f"PharmVar TSV line {line_number}: gene, haplotype and reference are required")
        group_key: tuple[str, str, str] = (gene, haplotype, reference)
        ref = (row.get(selected["ref"]) or "").strip()
        alt = (row.get(selected["alt"]) or "").strip()
        if ref.upper() == "REFERENCE" and alt == ".":
            if group_key in grouped and grouped[group_key]:
                raise ValueError(f"PharmVar TSV line {line_number}: reference sentinel conflicts with variants")
            if group_key in reference_groups:
                raise ValueError(f"PharmVar TSV line {line_number}: duplicate reference sentinel")
            reference_groups.add(group_key)
            grouped.setdefault(group_key, [])
            continue
        if group_key in reference_groups:
            raise ValueError(f"PharmVar TSV line {line_number}: variants conflict with reference sentinel")
        try:
            start = int((row.get(selected["start"]) or "").strip())
            stop = int((row.get(selected["stop"]) or "").strip())
        except ValueError as error:
            raise ValueError(f"PharmVar TSV line {line_number}: invalid variant coordinates") from error
        rsid = (row.get(selected["rsid"]) or "").strip() or None
        if rsid == ".":
            rsid = None
        variant = PharmVarVariant(
            reference, start, stop, ref.upper(), alt.upper(),
            (row.get(selected["type"]) or "").strip().casefold(), rsid,
        )
        values = grouped.setdefault(group_key, [])
        if variant in values:
            raise ValueError(f"PharmVar TSV line {line_number}: duplicate variant row")
        values.append(variant)

    definitions = []
    for (gene, haplotype, reference), variants in sorted(grouped.items()):
        definitions.append(PharmVarAlleleDefinition(
            gene, haplotype, reference, frozenset(variants),
            (gene, haplotype, reference) in reference_groups,
            source_release, source_url, source_sha256.lower(), license_id,
        ))
    if not definitions:
        raise ValueError("PharmVar TSV contained no allele definitions")
    return definitions


def match_pharmvar_haplotype(
    gene_symbol: str, reference_accession: str,
    observed_variants: Iterable[PharmVarVariant],
    definitions: Iterable[PharmVarAlleleDefinition], *,
    phase_confirmed: bool, call_complete: bool,
) -> PharmVarMatch:
    """Conservatively match an already phased, complete locus call by exact variant set."""
    if not phase_confirmed:
        return PharmVarMatch(gene_symbol, None, "no_call_unphased", (), 0)
    if not call_complete:
        return PharmVarMatch(gene_symbol, None, "no_call_incomplete", (), 0)
    observed = frozenset(observed_variants)
    if any(item.reference_accession != reference_accession for item in observed):
        raise ValueError("Observed PharmVar variants use a different reference accession")
    candidates = [
        item for item in definitions
        if item.gene_symbol == gene_symbol
        and item.reference_accession == reference_accession
        and item.variants == observed
    ]
    if not candidates:
        return PharmVarMatch(gene_symbol, None, "no_exact_definition", (), len(observed))
    haplotypes = sorted({item.haplotype for item in candidates})
    if len(haplotypes) != 1:
        return PharmVarMatch(gene_symbol, None, "ambiguous", tuple(haplotypes), len(observed))
    return PharmVarMatch(gene_symbol, haplotypes[0], "matched", tuple(haplotypes), len(observed))
