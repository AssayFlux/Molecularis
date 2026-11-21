from __future__ import annotations

import gzip
from pathlib import Path

from molecularis.catalog import iter_ncbi_gene_info_file


def test_ncbi_gene_info_file_streams_plain_and_gzip_sources(tmp_path: Path) -> None:
    row = "\t".join([
        "9606", "7157", "TP53", "-", "P53", "HGNC:11998",
        "17", "17p13.1", "tumor protein p53", "protein-coding", "TP53",
        "tumor protein p53", "Official", "-", "20250101", "gene",
    ])
    plain = tmp_path / "gene_info.tsv"
    plain.write_text("# header\n" + row + "\n", encoding="utf-8")
    compressed = tmp_path / "gene_info.tsv.gz"
    with gzip.open(compressed, "wt", encoding="utf-8") as handle:
        handle.write("# header\n" + row + "\n")
    assert next(iter_ncbi_gene_info_file(plain, source_release="release")).symbol == "TP53"
    assert next(iter_ncbi_gene_info_file(compressed, source_release="release")).gene_id == "7157"
