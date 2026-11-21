"""Deterministic benchmark for simulation energy-series summaries."""
from __future__ import annotations
import argparse,json,time
from molecularis.simulation_service import analyze_energy_series
def main()->None:
 p=argparse.ArgumentParser(); p.add_argument("--samples",type=int,default=10000); a=p.parse_args()
 if not 2<=a.samples<=1000000: p.error("--samples must be 2..1000000")
 values=tuple(float((i%101)-50) for i in range(a.samples)); start=time.perf_counter(); result=analyze_energy_series(values)
 print(json.dumps({"benchmark":"simulation-energy-series-v1","samples":a.samples,"mean":result["mean"],"seconds":round(time.perf_counter()-start,6)},sort_keys=True))
if __name__=="__main__": main()
