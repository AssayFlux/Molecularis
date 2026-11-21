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


## Agentics knowledge, data and scientific-tool governance

The [Scientific Tool Registry](../services/ai/SCIENTIFIC_TOOL_REGISTRY.md) is a candidate catalogue, not authorization to install, redistribute or train on any package, executable, dataset or model. Before adoption, record exact version, license, security/maintenance state, transitive dependencies, deployment profile, scientific scope, resource needs, data egress, failure behavior and independent verification method. Prefer one suitable tool per responsibility; avoid redundant overlapping stacks without measured justification.

Knowledge acquisition must record source identity, version/date, checksum, transformations, provenance, license/terms, privacy classification, intended use and quality review. Data access does not imply model-training permission. Separate retrieval/index updates, curated knowledge changes, Rulebook/algorithm changes and model-weight training. Training requires a measured need, permission-cleared data, deduplication, leakage-resistant evaluation, reproducible manifests, regression gates and rollback. Never allow a source document or model output to modify system policy.
