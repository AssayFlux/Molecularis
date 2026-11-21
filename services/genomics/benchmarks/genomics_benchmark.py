"""Deterministic synthetic assembly-QC benchmark smoke."""
from __future__ import annotations
import argparse
import json
import time
from molecularis.genome_qc import summarize_contigs
from molecularis.sequence import SequenceRecord


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contigs", type=int, default=1000)
    parser.add_argument("--bases-per-contig", type=int, default=1000)
    args = parser.parse_args()
    if args.contigs < 1 or args.bases_per_contig < 1:
        parser.error("contigs and bases-per-contig must be positive")
    records = (SequenceRecord(f"synthetic-{i}", "ACGT" * (args.bases_per_contig // 4) + "A" * (args.bases_per_contig % 4)) for i in range(args.contigs))
    started = time.perf_counter()
    result = summarize_contigs(records, max_records=args.contigs, max_total_bases=args.contigs * args.bases_per_contig)
    print(json.dumps({"contigs": result["contig_count"], "bases": result["total_bases"], "elapsed_seconds": time.perf_counter() - started}, sort_keys=True))


if __name__ == "__main__":
    main()
