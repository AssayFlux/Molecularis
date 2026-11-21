"""Deterministic Omics matrix benchmark smoke."""
import argparse, time
from molecularis.omics import cpm
from molecularis.omics_service import OmicsDocument
parser=argparse.ArgumentParser()
parser.add_argument("--features",type=int,default=1000)
parser.add_argument("--samples",type=int,default=12)
args=parser.parse_args()
if not 1<=args.features<=100000 or not 2<=args.samples<=10000 or args.features*args.samples>2000000:
    raise SystemExit("matrix exceeds Omics v1 dimension or cell limits")
matrix=[[float((i*17+j*13)%100+1) for j in range(args.samples)] for i in range(args.features)]
doc=OmicsDocument("benchmark",tuple(f"g{i}" for i in range(args.features)),tuple(f"s{j}" for j in range(args.samples)),tuple(tuple(r) for r in matrix))
start=time.perf_counter(); normalized=cpm([list(r) for r in doc.values])
print({"features":args.features,"samples":args.samples,"cells":args.features*args.samples,"elapsed_seconds":time.perf_counter()-start,"first_sample_cpm_sum":sum(r[0] for r in normalized)})
