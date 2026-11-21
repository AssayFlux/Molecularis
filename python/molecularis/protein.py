"""Protein sequence descriptors with explicit assumptions and ambiguity handling."""
from __future__ import annotations
from collections import Counter
from .sequence import PROTEIN, _normalise, validate_sequence

AA_MASS = {"A":71.0788,"R":156.1875,"N":114.1038,"D":115.0886,"C":103.1388,"E":129.1155,
"Q":128.1307,"G":57.0519,"H":137.1411,"I":113.1594,"L":113.1594,"K":128.1741,
"M":131.1926,"F":147.1766,"P":97.1167,"S":87.0782,"T":101.1051,"W":186.2132,
"Y":163.1760,"V":99.1326}
HYDROPATHY = dict(zip("ACDEFGHIKLMNPQRSTVWY",[1.8,2.5,-3.5,-3.5,2.5,-3.5,-3.5,-3.2,4.5,-3.9,3.8,1.9,-3.5,-3.5,-1.6,-3.5,-0.8,-0.7,-0.9,-1.3]))
PKA = {"n_term":8.0,"c_term":3.1,"D":3.9,"E":4.1,"C":8.3,"Y":10.1,"H":6.0,"K":10.5,"R":12.5}

def protein_descriptors(sequence: str) -> dict[str, object]:
    seq = _normalise(sequence)
    validate_sequence(seq, PROTEIN - {"*", "B", "X", "Z", "J", "U", "O"})
    if not seq or "*" in seq:
        raise ValueError("Provide a non-empty protein sequence without stop symbols")
    unknown = sorted(set(seq) - set(AA_MASS))
    if unknown:
        raise ValueError(f"Unsupported ambiguous/rare residues: {''.join(unknown)}")
    counts = Counter(seq)
    mass = sum(AA_MASS[aa] * n for aa, n in counts.items()) - 18.01528 * (len(seq)-1)
    return {"length":len(seq),"molecular_weight_da":mass,
            "composition":{aa:counts[aa]/len(seq) for aa in sorted(AA_MASS) if counts[aa]},
            "mean_hydropathy":sum(HYDROPATHY[a] for a in seq)/len(seq),
            "assumptions":["unmodified linear peptide","average residue masses","free termini"],
            "theoretical_pi":theoretical_pi(seq)}

def theoretical_pi(sequence: str) -> float:
    seq = _normalise(sequence)
    if not seq: raise ValueError("Sequence is empty")
    counts = Counter(seq)
    if set(seq) - set(AA_MASS): raise ValueError("Ambiguous/rare residues unsupported for pI")
    def charge(ph: float) -> float:
        positive = 1/(1+10**(ph-PKA["n_term"]))
        positive += sum(counts[a]/(1+10**(ph-PKA[a])) for a in "HKR")
        negative = 1/(1+10**(PKA["c_term"]-ph))
        negative += sum(counts[a]/(1+10**(PKA[a]-ph)) for a in "DECY")
        return positive-negative
    lo, hi = 0.0, 14.0
    for _ in range(80):
        mid=(lo+hi)/2
        if charge(mid)>0: lo=mid
        else: hi=mid
    return (lo+hi)/2
