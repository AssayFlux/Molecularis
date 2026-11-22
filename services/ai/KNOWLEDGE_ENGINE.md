# Scientific Knowledge Engine (P1)

**Status:** Initial P1 reference implementation committed on the Agentics P1 branch. The phase remains subject to CI and acceptance review.

## Purpose

The SKE is the domain-neutral, versioned knowledge substrate shared by Agentics Molecularis and services A–N. It stores scientific semantics and their evidence without treating stored claims as automatically true.

## Implemented contracts

- **Concepts:** identifiers, labels, domain namespaces, definitions, synonyms and parent concepts.
- **Entities:** typed domain objects, concept links, external identifiers and structured properties.
- **Relations:** directed subject-predicate-object links, qualifiers and evidence references.
- **Equations:** inert expression text, typed variables, dimensions, assumptions, applicability, source references, version and review state. Expressions are never evaluated with `eval` or `exec`.
- **Evidence:** observed, established, derived, inferred, predicted, simulated, constructed, hypothesized and validated classes; active, disputed, superseded and retracted states; source links, assumptions, uncertainty and explicit contradiction links.
- **Sources:** locator, title, publisher/version, content digest, license identifier and explicit permission state. Unknown permission is not training permission.
- **Quantities:** finite numeric values, SI base-dimension algebra, explicit units, safe compound-unit composition and conversion.
- **Coordinate references:** frame, axes, handedness and per-axis units.
- **Packages:** immutable package identity/version, deterministic canonical serialization and SHA-256 content identity.
- **Queries:** deterministic package, concept, entity, relation, equation, source and evidence lookup.
- **Core persistence:** package JSON is persisted through the existing Core `ArtifactStore` using a dedicated media/schema identifier and caller-supplied parent artifact lineage.

## Module and contracts

- Runtime: `python/molecularis/knowledge.py`
- Public API: `python/molecularis/__init__.py`
- Package schema: `services/ai/schemas/scientific-knowledge-package-v1.schema.json`
- Quantity schema: `services/ai/schemas/scientific-quantity-v1.schema.json`
- Tests: `tests/test_scientific_knowledge.py`

## Safety and epistemic rules

1. A source's `unknown` permission state never authorizes redistribution or model training.
2. Evidence classes are labels, not an automatic confidence ranking.
3. Conflicting or disputed evidence is retained; the engine does not silently select a winner.
4. Equation expressions are inert data. A later symbolic adapter must parse them through a constrained grammar.
5. Unit conversion rejects incompatible dimensions and non-finite values.
6. Package versions are immutable: the same package ID/version cannot be overwritten with different content.
7. The in-memory engine is a reference query/index layer. Durable storage is delegated explicitly to Core ArtifactStore.
8. A knowledge record is not experimental validation, and schema validity is not scientific truth.

## P1 boundary

This phase implements knowledge representation, evidence/provenance metadata, dimensions/units, coordinate references, deterministic queries, package serialization and artifact-store persistence.

It does **not** claim to implement symbolic derivation, general scientific reasoning, causal inference, numerical solvers, constraint optimization, model training, automated web ingestion, full-text indexing, distributed knowledge storage or scientific verification. Those belong to later P2/P3/P4/P5 work.

## Example

```python
from molecularis.knowledge import (
    EvidenceClass, EvidenceRecord, EvidenceStatus, KnowledgePackage,
    ScientificConcept, ScientificKnowledgeEngine, ScientificSource,
    SourcePermission,
)

source = ScientificSource(
    source_id="src:example:1",
    source_type="dataset",
    locator="https://example.org/dataset",
    title="Example measurements",
    license_id="CC-BY-4.0",
    permission=SourcePermission.RESEARCH_ONLY,
)
concept = ScientificConcept(
    concept_id="concept:concentration",
    label="Concentration",
    domain="chemistry",
    definition="Amount of substance per volume.",
)
evidence = EvidenceRecord(
    evidence_id="evidence:1",
    claim="The supplied dataset reports the stated concentration.",
    evidence_class=EvidenceClass.OBSERVED,
    status=EvidenceStatus.ACTIVE,
    source_ids=(source.source_id,),
    subject_ids=("sample:1",),
)
package = KnowledgePackage(
    package_id="chemistry:example",
    version="1.0.0",
    domain="chemistry",
    concepts=(concept,),
    sources=(source,),
    evidence=(evidence,),
)
engine = ScientificKnowledgeEngine()
engine.ingest(package)
assert engine.query_concepts(domain="chemistry", text="concentration")
```

## Acceptance evidence required

Run the focused tests, complete schema validation and full CI on the exact commit. Then test persistence against Core ArtifactStore with parent lineage, round-trip loading, crash/recovery behavior and real domain packages. Independent scientific review remains separate from engineering CI.
