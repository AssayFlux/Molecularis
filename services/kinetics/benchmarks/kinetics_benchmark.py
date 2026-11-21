"""Small deterministic RK4 benchmark smoke."""
import argparse
import time
from molecularis.kinetics_service import ReactionNetworkDocument, simulate_reaction_network

parser = argparse.ArgumentParser()
parser.add_argument("--steps", type=int, default=10000)
args = parser.parse_args()
if not 1 <= args.steps <= 1000000:
    raise SystemExit("--steps must be in [1, 1000000]")
record = ReactionNetworkDocument("benchmark-decay", ("A", "B"), (1.0, 0.0),
    ({"reactants": {"A": 1}, "products": {"B": 1}, "rate_constant": 0.1},))
start = time.perf_counter()
result = simulate_reaction_network(record, duration=float(args.steps), step_size=1.0, max_steps=args.steps)
print({"steps": result["steps"], "elapsed_seconds": time.perf_counter() - start,
       "final_A": result["final_concentrations"]["A"]})
