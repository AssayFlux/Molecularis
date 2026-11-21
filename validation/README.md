# Validation evidence

No scientific validation records exist yet. Add versioned, reproducible records only after a capability has an implementation, pinned reference materials, test vectors, tolerances and review. Never mark a registry item validated without committed evidence and a reproducible command.


## Pinned host-side kinetic numerical comparison

The CI workflow runs `validation/kinetics_scipy_reference.py` in a separate,
host-only environment pinned by `validation/requirements-scipy.txt`. The job
uploads its JSON output as a workflow artifact. It compares the exploratory
Molecularis enzyme-kinetics estimator against `scipy.optimize.curve_fit` on deterministic
synthetic noise-free and Gaussian-noise cases.

This is a numerical implementation cross-check, not experimental truth,
biological validation, a calibrated uncertainty study, or Android runtime
evidence. NumPy and SciPy are validation-host dependencies only and are not
added to the Android application. The registry evidence level remains
`none` until independent experimental reference datasets and a reviewed
validation protocol are completed.


## Pinned host-side chemistry sanity fixtures

The CI job installs the exact host-only RDKit version from
`validation/requirements-rdkit.txt`, runs
`validation/chemistry_reference.py`, and uploads its JSON result. The fixture
set covers ethanol and benzene identity/formula/basic descriptor expectations.
It is an engineering sanity check, not an independent curated chemical
benchmark, ADMET or biological-activity validation, and does not validate
Android chemistry feasibility. RDKit remains outside the Android app.


## Structural biology software comparison

`structure_biopython_reference.py` uses the pinned Biopython parser and NumPy
geometry routines to compare a deterministic synthetic PDB fixture with the
Molecularis PDB parser, contact calculation and superposed RMSD implementation.
The CI job stores the JSON result with the SciPy and genetic-code comparison
records. This is software concordance, not an experimental structure benchmark.


## Phylogenetics software comparison

`phylo_biopython_reference.py` compares all pairwise patristic distances from
Molecularis neighbour joining with Biopython's independent NJ implementation on a
deterministic additive four-taxon matrix. The result is part of the pinned
host-side reference CI artifact. It is a synthetic software check, not a
published-tree or biological-evolution validation.


## Differential-expression software comparison

`omics_nb2_scipy_reference.py` compares the exploratory NB2 GLM with an
independent SciPy maximum-likelihood optimizer on fixed synthetic raw counts.
It uses the same recorded size factors and fixed moment dispersion, then checks
coefficients, Fisher-information standard errors and Wald p-values. This is a
software/numerical comparison, not null/power/FDR or biological validation.


## Track I1 — pinned RDKit descriptor sanity fixtures

`chemistry_reference.py` runs against the exact pinned host-only RDKit release in `requirements-rdkit.txt`. The ethanol and benzene fixtures check formula, atom/bond/ring counts, charge, heavy/aromatic atom counts, aliphatic/aromatic ring counts, fraction Csp3, molecular/exact mass, TPSA, Crippen LogP, fingerprint configuration, Rule-of-Five screen output and input SHA-256 provenance. The runner also checks that embedded NUL, invalid Unicode and inputs exceeding the UTF-8 byte ceiling are rejected before parsing.

These are deterministic descriptor/parser sanity checks, not a curated chemistry benchmark, biological-activity or ADMET validation, or evidence of Android runtime feasibility.
