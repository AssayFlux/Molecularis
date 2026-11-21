# Molecularis Scientific Data Engine (MSDE)

Status: architecture specification; implementation not yet started.

MSDE is a Molecularis-owned, domain-neutral data substrate for scientific artifacts, indexing, streaming, provenance, evidence, and Rulebook execution support. Scientific services consume stable Core contracts; Core does not depend on service implementations.

Documents:
- ENGINE.md: architecture, data model, index portfolio, storage, query and verification boundaries.
- RUNTIME.md: lifecycle, resource governance, concurrency, recovery and observability.
- RULEBOOK.md: normative invariants for data and evidence operations.
- IMPLEMENTATION_PLAN.md: staged delivery and acceptance gates.
- schemas/: versioned interchange contracts.

MSDE is not a scientific inference model and not a claim that one index fits every workload. Search and ranking do not establish scientific truth. Future AI-assisted planning cannot bypass deterministic contracts, resource controls or independent verification.
