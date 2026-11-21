# Scientific Validation Standard

## Validation design
For each capability, document the scientific question, intended domain, assumptions, operating range, known failure modes, and measurable acceptance criteria before implementation.

## Required test classes
1. Unit tests for local mathematical and data invariants.
2. Property-based tests for general invariants and edge cases.
3. Golden fixtures with provenance and expected tolerances.
4. Independent reference comparisons where suitable.
5. Regression tests for every corrected defect.
6. Integration tests across service contracts.
7. Reproducibility tests including seeds, versions and environment.
8. Performance and scaling tests with representative inputs.

## Reference independence
A reference implementation may be used to compare results, but must not be called as the hidden production implementation of a Molecularis-native capability. Record reference source, version, license, parameters, dataset provenance, and known differences.

## Numerical reporting
Record units, precision, tolerances, convergence, stochasticity, random seed, and hardware-sensitive behavior. Explain acceptable deviations and why thresholds are scientifically justified.

## Dataset governance
Every fixture or reference dataset requires source, license/terms, version/date, checksum, transformations, and intended use. Never add sensitive or restricted datasets without authorization and a lawful basis.

## Reporting
Reports state exactly what was tested, what passed, what failed, what was not tested, and the evidence level achieved. Passing software tests alone does not establish biological or clinical validity.


## Agentics generation and verification requirements

Every AI-assisted scientific construction must define its objective, inputs, assumptions, constraints, units, reference frames, knowledge versions, method applicability and acceptance thresholds before generation. The pre-generation audit blocks invalid, underspecified, out-of-domain or unsafe requests or records explicit assumptions and review state.

Post-generation checks must be independent of the proposing model where feasible and must be appropriate to the scientific claim. Record equations/algorithms, reference implementations or fixtures, invariants, tolerances, uncertainty, sensitivity, boundary conditions, failed checks and unresolved alternatives. Distinguish mathematical consistency, domain validity, physical plausibility, stability, experimental realizability and demonstrated function. A model confidence score or successful workflow is not scientific proof. See the [AI Constitution](../services/ai/AI_CONSTITUTION.md).
