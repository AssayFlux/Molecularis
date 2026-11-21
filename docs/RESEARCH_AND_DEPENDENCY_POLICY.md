# Research, External References and Dependency Policy

## Research
- Prefer primary literature, standards, authoritative datasets and reproducible methods.
- Record citation, version, publication date, assumptions, domain of applicability and known limitations.
- Distinguish established methods from hypotheses and proprietary claims.
- Do not copy source code or model weights without license and provenance review.

## External software
External tools may be inspected for conceptual reference, optional data interchange, or independent benchmarking. They must not be a required hidden backend for a Molecularis-native capability. Any proposed runtime dependency requires an architecture decision and explicit approval.

## Dependencies
For every dependency record purpose, version range, license, security posture, maintenance state, transitive dependencies, replacement risk and whether it is required at build-time, test-time or runtime. Prefer standard libraries and Molecularis-owned implementations when technically and scientifically justified; do not reimplement commodity infrastructure without a reason.

## Data and model assets
Record source, license/terms, checksum, version, transformations, intended use and redistribution rights. Model weights and datasets are governed artifacts, not casual repository additions.

## Attribution
Independent implementations must still credit scientific papers, algorithms, datasets, standards and prior discoveries appropriately. Native ownership does not mean claiming original discovery.
