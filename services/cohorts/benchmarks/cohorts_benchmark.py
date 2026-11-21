"""Deterministic smoke benchmark for Cohorts aggregate summaries."""
from __future__ import annotations
import argparse
import json
import time
from molecularis.cohorts_service import CohortDocument, CohortMember, CohortVisit, _summary


def run(members: int) -> dict[str, object]:
    if not 1 <= members <= 100_000:
        raise ValueError("members must be 1..100000")
    record = CohortDocument("benchmark", tuple(
        CohortMember(f"synthetic-{i}", (("arm", "A" if i % 2 else "B"),),
                     (CohortVisit("baseline", 0, (("signal", float(i % 100)),)),))
        for i in range(members)
    ))
    started = time.perf_counter()
    result = _summary([m for m in record.members if m.included])
    return {"members": members, "summary_member_count": result["member_count"],
            "elapsed_seconds": time.perf_counter() - started}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--members", type=int, default=10000)
    print(json.dumps(run(parser.parse_args().members), sort_keys=True))
