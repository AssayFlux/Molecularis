"""Smoke benchmark for bounded distance-matrix and NJ tree construction."""
from __future__ import annotations
import argparse
import json
import time
from molecularis.phylo import neighbor_joining, jukes_cantor_distance, to_newick

def run(taxa: int, sites: int) -> dict[str, object]:
    if taxa < 3 or taxa > 500 or sites < 20 or sites > 2_000_000:
        raise ValueError("taxa must be 3..500 and sites 20..2000000")
    sequences=[("ACGT"*((sites+3)//4))[:sites] for _ in range(taxa)]
    sequences=[s[:i]+("A" if s[i]!="A" else "C")+s[i+1:] for i,s in enumerate(sequences)]
    labels=[f"taxon-{i}" for i in range(taxa)]
    started=time.perf_counter()
    matrix=[[0.0]*taxa for _ in range(taxa)]
    for i in range(taxa):
        for j in range(i+1,taxa):
            d=jukes_cantor_distance(sequences[i],sequences[j],minimum_sites=20)["distance"]
            matrix[i][j]=matrix[j][i]=float(d)
    tree=neighbor_joining(matrix,labels)
    elapsed=time.perf_counter()-started
    return {"taxa":taxa,"sites":sites,"newick_bytes":len(to_newick(tree)),"elapsed_seconds":elapsed,"pairwise_comparisons":taxa*(taxa-1)//2}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--taxa",type=int,default=20)
    parser.add_argument("--sites",type=int,default=1000)
    args=parser.parse_args()
    print(json.dumps(run(args.taxa,args.sites),sort_keys=True))
