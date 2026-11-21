"""Source-attributed, expandable ingestion of the full NCBI Gene gene_info schema."""
from __future__ import annotations

import gzip
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


@dataclass(frozen=True)
class GeneEntry:
    tax_id: str
    gene_id: str
    symbol: str
    description: str
    synonyms: tuple[str, ...]
    source: str
    source_release: str
    evidence_status: str = "catalogued"
    locus_tag: str = ""
    dbxrefs: tuple[str, ...] = ()
    chromosome: str = ""
    map_location: str = ""
    gene_type: str = ""
    nomenclature_symbol: str = ""
    nomenclature_full_name: str = ""
    nomenclature_status: str = ""
    other_designations: tuple[str, ...] = ()
    modification_date: str = ""
    feature_type: str = ""


def _split_pipe(value: str) -> tuple[str, ...]:
    return tuple(sorted({item for item in value.split("|") if item not in {"", "-"}}))


def iter_ncbi_gene_info(lines: Iterable[str], *, source_release: str) -> Iterator[GeneEntry]:
    """Stream all 16 NCBI gene_info columns; data remains source/release attributed."""
    if not source_release.strip():
        raise ValueError("Pin the NCBI gene_info release/date before import")
    for line_number, raw in enumerate(lines, 1):
        line = raw.rstrip("\r\n")
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 16:
            raise ValueError(f"gene_info line {line_number}: expected exactly 16 NCBI columns")
        (
            tax_id, gene_id, symbol, locus_tag, synonyms, dbxrefs, chromosome,
            map_location, description, gene_type, nomenclature_symbol,
            nomenclature_full_name, nomenclature_status, other_designations,
            modification_date, feature_type,
        ) = fields[:16]
        if not tax_id.isdigit() or not gene_id.isdigit() or not symbol or symbol == "-":
            raise ValueError(f"gene_info line {line_number}: invalid tax_id, GeneID or symbol")
        if modification_date:
            try:
                datetime.strptime(modification_date, "%Y%m%d")
            except ValueError as exc:
                raise ValueError(
                    f"gene_info line {line_number}: invalid modification date"
                ) from exc
        yield GeneEntry(
            tax_id=tax_id,
            gene_id=gene_id,
            symbol=symbol,
            description="" if description == "-" else description,
            synonyms=_split_pipe(synonyms),
            source="NCBI Gene gene_info",
            source_release=source_release,
            locus_tag="" if locus_tag == "-" else locus_tag,
            dbxrefs=_split_pipe(dbxrefs),
            chromosome="" if chromosome == "-" else chromosome,
            map_location="" if map_location == "-" else map_location,
            gene_type="" if gene_type == "-" else gene_type,
            nomenclature_symbol="" if nomenclature_symbol == "-" else nomenclature_symbol,
            nomenclature_full_name="" if nomenclature_full_name == "-" else nomenclature_full_name,
            nomenclature_status="" if nomenclature_status == "-" else nomenclature_status,
            other_designations=_split_pipe(other_designations),
            modification_date=modification_date,
            feature_type="" if feature_type == "-" else feature_type,
        )


def validate_gene_catalog(entries: Iterable[GeneEntry]) -> None:
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        if not all((
            entry.tax_id.isdigit(), entry.gene_id.isdigit(), entry.symbol,
            entry.source, entry.source_release,
        )):
            raise ValueError("Gene entries require valid tax_id, GeneID, symbol, source and release")
        key = (entry.tax_id, entry.gene_id)
        if key in seen:
            raise ValueError(f"Duplicate NCBI gene entry: {entry.tax_id}:{entry.gene_id}")
        seen.add(key)
        if entry.evidence_status not in {"catalogued", "prioritised", "implemented", "validated"}:
            raise ValueError(f"Unknown evidence status: {entry.evidence_status}")
        if entry.evidence_status == "validated":
            raise ValueError("A catalogue import cannot confer validated status")



def gene_catalogue_coverage_report(
    entries: Iterable[GeneEntry], *, max_entries: int = 1_000_000,
) -> dict[str, object]:
    """Summarize imported catalogue composition without implying genome-wide coverage.

    Counts are descriptive of the supplied snapshot only. No denominator or
    completeness percentage is invented because the expected gene universe is
    organism-, release- and feature-policy-dependent.
    """
    if isinstance(max_entries, bool) or not isinstance(max_entries, int) or max_entries < 1:
        raise ValueError("max_entries must be a positive integer")
    snapshot: list[GeneEntry] = []
    for entry in entries:
        if len(snapshot) >= max_entries:
            raise ValueError("Gene catalogue exceeds max_entries")
        snapshot.append(entry)
    validate_gene_catalog(snapshot)

    by_taxonomy: dict[str, int] = {}
    by_gene_type: dict[str, int] = {}
    by_release: dict[str, int] = {}
    missing: dict[str, int] = {
        "description": 0, "chromosome": 0, "map_location": 0,
        "gene_type": 0, "nomenclature_symbol": 0,
    }
    for entry in snapshot:
        by_taxonomy[entry.tax_id] = by_taxonomy.get(entry.tax_id, 0) + 1
        gene_type = entry.gene_type or "unspecified"
        by_gene_type[gene_type] = by_gene_type.get(gene_type, 0) + 1
        by_release[entry.source_release] = by_release.get(entry.source_release, 0) + 1
        for field in missing:
            if not getattr(entry, field):
                missing[field] += 1
    return {
        "schema_version": 1,
        "scope": "supplied_catalogue_snapshot_only",
        "entry_count": len(snapshot),
        "taxonomy_counts": dict(sorted(by_taxonomy.items())),
        "gene_type_counts": dict(sorted(by_gene_type.items())),
        "source_release_counts": dict(sorted(by_release.items())),
        "missing_annotation_counts": dict(sorted(missing.items())),
        "coverage_percentage": None,
        "coverage_denominator": None,
        "limitations": [
            "No completeness percentage is calculated without an independently defined expected gene universe.",
            "Counts describe only the supplied source release and imported records.",
            "Catalogue presence does not imply assay, caller, interpretation or clinical validation.",
        ],
    }


def iter_ncbi_gene_info_file(
    path: str | Path, *, source_release: str,
) -> Iterator[GeneEntry]:
    """Stream plain or gzip-compressed NCBI gene_info without loading it into memory."""
    source = Path(path)
    if source.suffix.lower() == ".gz":
        with gzip.open(source, "rt", encoding="utf-8", newline="") as handle:
            yield from iter_ncbi_gene_info(handle, source_release=source_release)
    else:
        with source.open("rt", encoding="utf-8", newline="") as handle:
            yield from iter_ncbi_gene_info(handle, source_release=source_release)


def search_gene_catalog(
    entries: Iterable[GeneEntry], query: str, *, tax_id: str | None = None,
    limit: int = 100,
) -> list[GeneEntry]:
    """Search official symbols, synonyms, names and identifiers without hiding provenance."""
    term = query.strip().casefold()
    if not term:
        raise ValueError("Gene search query cannot be empty")
    if limit < 1 or limit > 10_000:
        raise ValueError("Gene search limit must be between 1 and 10000")
    if tax_id is not None and not tax_id.isdigit():
        raise ValueError("Taxonomy ID must contain digits only")
    exact: list[GeneEntry] = []
    partial: list[GeneEntry] = []
    for entry in entries:
        if tax_id is not None and entry.tax_id != tax_id:
            continue
        fields = (
            entry.gene_id, entry.symbol, entry.description, entry.locus_tag,
            entry.nomenclature_symbol, entry.nomenclature_full_name,
            *entry.synonyms, *entry.other_designations, *entry.dbxrefs,
        )
        normalized = [field.casefold() for field in fields if field]
        if term in normalized:
            exact.append(entry)
            if len(exact) >= limit:
                return exact
        elif any(term in field for field in normalized) and len(partial) < limit:
            partial.append(entry)
    return exact + partial[:max(0, limit - len(exact))]
