"""Deterministic smoke benchmark for streaming FASTA parsing."""
from __future__ import annotations
import argparse
import json
import time
from molecularis.sequence import iter_fasta_records


def run(records: int, bases_per_record: int) -> dict[str, object]:
    if records < 1 or bases_per_record < 1:
        raise ValueError("records and bases_per_record must be positive")
    sequence = ("ACGT" * ((bases_per_record + 3) // 4))[:bases_per_record]
    def lines():
        for index in range(records):
            yield f">record-{index}\n"
            for start in range(0, len(sequence), 80):
                yield sequence[start:start + 80] + "\n"
    started = time.perf_counter()
    parsed = sum(1 for _ in iter_fasta_records(lines()))
    elapsed = time.perf_counter() - started
    return {"records": parsed, "bases_per_record": bases_per_record,
            "total_bases": parsed * bases_per_record, "elapsed_seconds": elapsed,
            "records_per_second": parsed / elapsed if elapsed else None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=int, default=1000)
    parser.add_argument("--bases-per-record", type=int, default=1000)
    args = parser.parse_args()
    print(json.dumps(run(args.records, args.bases_per_record), sort_keys=True))
