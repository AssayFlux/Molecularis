# Simulation H — engineering acceptance

Implemented: strict canonical protocol artifact; NVT/NPT validation; SHA-256 input and force-field provenance; MSDE ingest/load; three executable capabilities; bounded energy time-series analysis; hash-pinned GROMACS TPR execution integration; retained OpenMM CPU replica runner and direct API; seven executable rules; schemas, tests, benchmark and documentation.

CI verification: GitHub Actions run #44893264385 passed all four jobs. Core 696 passed/12 skipped; optional Chemistry 704 passed/4 skipped, Genomics 697 passed/11 skipped, Sequence 699 passed/9 skipped (4 warnings). Registry, three JSON schemas, Ruff E9/F, Python compilation and all benchmark smoke steps passed.

Not claimed: force-field validation, topology generation, parameterization, equilibration/convergence assessment, ensemble validity, free energies, enhanced sampling, trajectory physical correctness or experimental agreement. Scientific review and independent engine comparisons are deferred until A–N engineering completion.
