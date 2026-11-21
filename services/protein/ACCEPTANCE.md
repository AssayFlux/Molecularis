# Protein E — engineering acceptance record

Status: engineering implementation complete and CI-verified. University scientific review, reference comparisons and formal contract freeze are deferred until all A–N engineering is complete under DEC-0010.

Implemented: canonical protein sequence artifacts; MSDE integrity and lineage; four executable capabilities; PRO-001–PRO-006; three JSON schemas; retained ESM, HMMER, motif and design-brief functionality; bounded benchmark and tests.

Not claimed: folding, sequence generation, function prediction, clinical validity, biosafety, calibrated ESM confidence or scientific acceptance. Local ESM inference requires operator-provided model weights and optional PyTorch/Transformers runtime. HMMER evidence requires caller-provided databases and explicit thresholds.

Engineering commit: d1b75c9cce9dc7776fa4b1e8c2fc2eda2244e3da. CI run [#44889593877](https://github.com/AssayFlux/Molecularis/actions/runs/44889593877) passed all four jobs. Core: 651 passed, 12 skipped. Optional profiles: Sequence 654 passed/9 skipped; Genomics 652 passed/11 skipped; Chemistry 659 passed/4 skipped. Capability registry valid, 40 JSON Schemas validated, Ruff E9/F and compilation passed, and Protein 10,000-residue benchmark smoke passed.
