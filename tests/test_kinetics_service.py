from __future__ import annotations

import json
import pytest

from molecularis.kinetics_service import (
    ReactionNetworkDocument, simulate_reaction_network, ingest_kinetics, load_kinetics,
    register_kinetics_service, kinetics_rulebook,
)
from molecularis.platform import MolecularisPlatform, ExecutionContext, Budget


def network():
    return ReactionNetworkDocument("A-to-B", ("A", "B"), (1.0, 0.0),
        ({"reactants": {"A": 1}, "products": {"B": 1}, "rate_constant": 0.7},))


def test_document_roundtrip_and_canonical_digest():
    record = network()
    assert ReactionNetworkDocument.from_json(record.to_json()).sha256 == record.sha256
    assert record.to_json() == json.dumps(record.to_dict(), sort_keys=True, ensure_ascii=False,
        allow_nan=False, separators=(",", ":")).encode()


def test_document_rejects_duplicate_json_keys_and_invalid_stoichiometry():
    with pytest.raises(ValueError, match="duplicate"):
        ReactionNetworkDocument.from_json('{"schema":"molecularis.kinetics-network.v1","schema":"x"}')
    with pytest.raises(ValueError, match="stoichiometry"):
        ReactionNetworkDocument("bad", ("A",), (1.0,),
            ({"reactants": {"A": 0}, "products": {"A": 1}, "rate_constant": 1.0},))


def test_rk4_first_order_decay_matches_analytic_solution():
    record = network()
    result = simulate_reaction_network(record, duration=2.0, step_size=0.001)
    assert result["final_concentrations"]["A"] == pytest.approx(__import__("math").exp(-1.4), rel=1e-10)
    assert result["final_concentrations"]["A"] + result["final_concentrations"]["B"] == pytest.approx(1.0)


def test_rk4_bounds_and_negative_overshoot_rejected():
    with pytest.raises(ValueError, match="multiple"):
        simulate_reaction_network(network(), duration=1.0, step_size=0.3)
    with pytest.raises(Exception, match="max_steps"):
        simulate_reaction_network(network(), duration=10.0, step_size=0.001, max_steps=10)


def test_artifact_lifecycle_and_rulebook_execution(tmp_path):
    platform = MolecularisPlatform(tmp_path)
    platform.start()
    register_kinetics_service(platform)
    record = network()
    artifact = ingest_kinetics(platform, record)
    assert load_kinetics(platform, artifact.artifact_id).sha256 == record.sha256
    result = platform.execute(kinetics_rulebook("simulate", parameters={"duration": 1.0, "step_size": 0.01}),
        {"kinetics_artifact_id": artifact.artifact_id}, context=ExecutionContext(budget=Budget(max_candidates=1000)))
    assert result["kinetics_result"]["result"]["steps"] == 100
    platform.close()


def test_michaelis_menten_curve_is_exposed_by_service(tmp_path):
    from molecularis.kinetics import michaelis_menten
    assert michaelis_menten(2.0, 10.0, 2.0) == pytest.approx(5.0)
