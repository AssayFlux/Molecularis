"""Bounded synthetic contact-analysis smoke benchmark."""
import argparse,json,time
from molecularis.structure import Atom,contact_pairs
def run(atom_count):
    if atom_count<1 or atom_count>5000: raise ValueError("atom_count must be 1..5000")
    atoms=[Atom(i+1,"CA","GLY","A",i+1,float(i)*4.0,0.0,0.0,"C") for i in range(atom_count)]
    start=time.perf_counter(); contacts=contact_pairs(atoms,8.0); elapsed=time.perf_counter()-start
    return {"atoms":atom_count,"contacts":len(contacts),"elapsed_seconds":elapsed}
if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--atoms",type=int,default=1000); args=parser.parse_args()
    print(json.dumps(run(args.atoms),sort_keys=True))
