"""Deterministic Protein sequence descriptor smoke benchmark."""
from __future__ import annotations
import argparse,json,time
from molecularis.protein import protein_descriptors

def main():
 p=argparse.ArgumentParser(); p.add_argument("--residues",type=int,default=10000); a=p.parse_args()
 if not 1<=a.residues<=5_000_000: p.error("--residues must be 1..5000000")
 seq=("ACDEFGHIKLMNPQRSTVWY"*((a.residues+19)//20))[:a.residues]
 start=time.perf_counter(); result=protein_descriptors(seq)
 print(json.dumps({"residues":result["length"],"molecular_weight_da":result["molecular_weight_da"],"elapsed_seconds":time.perf_counter()-start},sort_keys=True))
if __name__=="__main__": main()
