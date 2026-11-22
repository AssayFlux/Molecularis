from __future__ import annotations

import pytest

from molecularis.knowledge import (
    LENGTH, MASS, TIME, CoordinateReference, Dimension, EquationVariable,
    EvidenceClass, EvidenceRecord, EvidenceStatus, KnowledgePackage, Quantity,
    ScientificConcept, ScientificEntity, ScientificEquation,
    ScientificKnowledgeEngine, ScientificRelation, ScientificSource,
    SourcePermission, UnitDefinition, UnitRegistry,
)


def test_dimension_algebra_is_canonical() -> None:
    velocity = LENGTH / TIME
    acceleration = velocity / TIME
    assert acceleration == Dimension.of(L=1, T=-2)
    assert (MASS * LENGTH / TIME**2) == Dimension.of(M=1, L=1, T=-2)


def test_unit_conversion_and_compatible_arithmetic() -> None:
    units = UnitRegistry()
    assert units.quantity(1, "m").to("cm").value == pytest.approx(100)
    assert (units.quantity(1, "m") + units.quantity(25, "cm")).value == pytest.approx(1.25)
    assert units.quantity(1000, "g").to("kg").value == pytest.approx(1)
    assert units.quantity(0, "degC").to("K").value == pytest.approx(273.15)


def test_incompatible_units_and_non_finite_values_are_rejected() -> None:
    units = UnitRegistry()
    with pytest.raises(ValueError, match="Incompatible"):
        units.quantity(1, "m").to("s")
    with pytest.raises(ValueError, match="compatible dimensions"):
        _ = units.quantity(1, "m") + units.quantity(1, "s")
    with pytest.raises(ValueError, match="finite"):
        units.quantity(float("nan"), "m")


def test_quantity_products_preserve_derived_dimensions() -> None:
    units = UnitRegistry()
    velocity = units.quantity(10, "m") / units.quantity(2, "s")
    assert velocity.dimension == Dimension.of(L=1, T=-1)
    assert velocity.si_value == pytest.approx(5)
    force = units.quantity(2, "kg") * units.quantity(3, "m") / units.quantity(1, "s")**2
    assert force.dimension == Dimension.of(M=1, L=1, T=-2)
    assert force.si_value == pytest.approx(6)


def _package() -> KnowledgePackage:
    source = ScientificSource(
        source_id="src:mechanics:001", source_type="textbook",
        locator="https://example.org/mechanics", title="Classical mechanics",
        publisher="Example Press", license_id="CC-BY-4.0",
        permission=SourcePermission.RESEARCH_ONLY,
    )
    concept = ScientificConcept(
        concept_id="concept:velocity", label="Velocity", domain="physics",
        definition="Rate of change of position with respect to time.",
        synonyms=("speed vector",),
    )
    body = ScientificEntity(
        entity_id="entity:body", entity_type="physical_system", domain="physics",
        label="Test body", concept_ids=("concept:velocity",),
    )
    evidence = EvidenceRecord(
        evidence_id="evidence:velocity", claim="Velocity is displacement per time.",
        evidence_class=EvidenceClass.ESTABLISHED, status=EvidenceStatus.ACTIVE,
        source_ids=(source.source_id,), subject_ids=(body.entity_id,),
        method="textbook derivation", applicability="classical mechanics",
        created_at="2026-01-01T00:00:00+00:00",
    )
    relation = ScientificRelation(
        relation_id="relation:has-velocity", subject_id=body.entity_id,
        predicate="has_property", object_id=body.entity_id, domain="physics",
        evidence_ids=(evidence.evidence_id,),
    )
    equation = ScientificEquation(
        equation_id="equation:velocity", label="Average velocity",
        domain="physics", expression="v = displacement / elapsed_time",
        variables=(
            EquationVariable("v", "Average velocity", LENGTH / TIME, "m/s"),
            EquationVariable("displacement", "Change in position", LENGTH, "m"),
            EquationVariable("elapsed_time", "Elapsed time", TIME, "s"),
        ),
        assumptions=("elapsed_time > 0",), applicability="classical mechanics",
        source_ids=(source.source_id,),
    )
    return KnowledgePackage(
        package_id="physics:kinematics", version="1.0.0", domain="physics",
        concepts=(concept,), entities=(body,), relations=(relation,),
        equations=(equation,), sources=(source,), evidence=(evidence,),
        coordinate_references=(CoordinateReference(
            "frame:cartesian-3d", "Cartesian", ("x", "y", "z"),
            units=("m", "m", "m"),
        ),),
    )


def test_package_validates_references_and_exports_deterministically() -> None:
    package = _package()
    assert package.content_sha256 == _package().content_sha256
    exported = package.to_dict()
    assert exported["domain"] == "physics"
    assert exported["evidence"][0]["evidence_class"] == "established"
    assert exported["equations"][0]["expression"].startswith("v =")
    assert "powers" in exported["equations"][0]["variables"][0]["dimension"]


def test_package_rejects_dangling_relation_and_evidence_references() -> None:
    package = _package()
    with pytest.raises(ValueError, match="unknown endpoints"):
        KnowledgePackage(
            package_id="bad", version="1", domain="physics",
            relations=(ScientificRelation(
                "r", "missing", "related_to", "also-missing", "physics"
            ),),
        )
    with pytest.raises(ValueError, match="unknown sources"):
        ScientificEquation(
            "eq", "bad equation", "physics", "x = 1", (),
            source_ids=("missing-source",),
        )


def test_engine_ingest_is_idempotent_and_versions_are_immutable() -> None:
    engine = ScientificKnowledgeEngine()
    package = _package()
    digest = engine.ingest(package)
    assert engine.ingest(package) == digest
    assert engine.get(package.package_id, package.version) == package
    changed = KnowledgePackage(
        package_id=package.package_id, version=package.version,
        domain=package.domain,
        concepts=(ScientificConcept(
            "different", "Different", "physics", "Different definition"
        ),),
    )
    with pytest.raises(ValueError, match="immutable"):
        engine.ingest(changed)


def test_deterministic_queries_and_disputed_evidence_are_preserved() -> None:
    engine = ScientificKnowledgeEngine()
    package = _package()
    engine.ingest(package)
    assert [x.concept_id for x in engine.query_concepts(text="velocity")] == [
        "concept:velocity"
    ]
    results = engine.query_evidence(
        subject_id="entity:body", evidence_class=EvidenceClass.ESTABLISHED
    )
    assert len(results) == 1
    assert results[0].status == EvidenceStatus.ACTIVE
    assert engine.conflicting_evidence(subject_id="entity:body") == results


def test_package_version_collision_does_not_overwrite_prior_content() -> None:
    engine = ScientificKnowledgeEngine()
    first = _package()
    engine.ingest(first)
    assert engine.list_packages(domain="physics") == (
        ("physics:kinematics", "1.0.0", "physics"),
    )
    assert engine.export_package(first.package_id, first.version) == engine.export_package(
        first.package_id, first.version
    )


def test_coordinate_reference_rejects_axis_unit_mismatch() -> None:
    with pytest.raises(ValueError, match="match the number of axes"):
        CoordinateReference("frame", "Cartesian", ("x", "y", "z"), units=("m", "m"))
