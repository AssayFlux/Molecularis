"""Deterministic smoke benchmark for native Chemistry graph descriptors."""
from __future__ import annotations
import argparse
import json
import time
from molecularis.chemistry import graph_descriptors, path_fingerprint

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--atoms",type=int,default=1000)
    args=parser.parse_args()
    if args.atoms<1 or args.atoms>100000: parser.error("--atoms must be 1..100000")
    molecule={"atoms":[{"element":"C","x":float(i),"y":0.0,"z":0.0} for i in range(args.atoms)],
              "bonds":[(i,i+1,1) for i in range(args.atoms-1)]}
    start=time.perf_counter()
    summary=graph_descriptors(molecule)
    fingerprint=path_fingerprint(molecule,max_path=2,max_walk_states=max(200000,args.atoms*4))
    print(json.dumps({"atoms":args.atoms,"bonds":summary["bond_count"],"features":len(fingerprint),
                      "elapsed_seconds":time.perf_counter()-start},sort_keys=True))
if __name__=="__main__": main()
