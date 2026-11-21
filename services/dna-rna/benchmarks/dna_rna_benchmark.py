"""Reproducible smoke benchmark for native RNA secondary folding."""
from __future__ import annotations
import argparse,json,time
from molecularis.dna_rna_service import fold_rna_nussinov

def main()->None:
    parser=argparse.ArgumentParser(); parser.add_argument("--length",type=int,default=120); args=parser.parse_args()
    if not 1<=args.length<=300: parser.error("--length must be between 1 and 300")
    sequence=("GCAU"*((args.length+3)//4))[:args.length]; start=time.perf_counter()
    result=fold_rna_nussinov(sequence)
    print(json.dumps({"benchmark":"nussinov-rna-v1","length":args.length,"pairs":result["pair_count"],"seconds":round(time.perf_counter()-start,6)},sort_keys=True))
if __name__=="__main__": main()
