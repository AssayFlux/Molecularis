"""Small deterministic smoke benchmark for PGx definition matching."""
from __future__ import annotations
import argparse
import hashlib
import json
import time
from molecularis.pharmacogenomics_service import HaplotypeCall, PharmacogenomicsDocument, _match
from molecularis.pgx import StarAlleleDefinition, VariantKey


def run(calls: int) -> dict[str, object]:
    if calls < 1 or calls > 500:
        raise ValueError("calls must be 1..500")
    variant = VariantKey("SYNTHETIC-v1", "chr1", 101, "A", "G")
    definitions = [StarAlleleDefinition(
        "GENE", "*2", frozenset({variant}), frozenset(), "synthetic",
        "fixture-1", "https://example.org/fixture", hashlib.sha256(b"fixture").hexdigest(),
        "CC0-1.0", "SYNTHETIC-v1", "definition-1",
    )]
    record = PharmacogenomicsDocument("benchmark", "SYNTHETIC-v1", tuple(
        HaplotypeCall("GENE", f"hap-{i}", (variant,), True, True) for i in range(calls)
    ))
    started = time.perf_counter()
    result = _match(record, definitions)
    return {"haplotype_calls": calls, "matched": result["matched_haplotypes"],
            "elapsed_seconds": time.perf_counter() - started}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--calls", type=int, default=100)
    print(json.dumps(run(parser.parse_args().calls), sort_keys=True))
