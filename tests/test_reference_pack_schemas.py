from __future__ import annotations

import json

import yaml
from pathlib import Path


def test_local_reference_pack_schema_is_strict_and_content_addressed() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "local-reference-pack.schema.json").read_text(encoding="utf-8")
    )
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "schema_version", "name", "version", "license", "source",
        "sequence_type", "format", "content_sha256",
    }
    assert schema["properties"]["content_sha256"]["pattern"] == "^[0-9a-f]{64}$"
    assert schema["properties"]["sequence_type"]["enum"] == ["DNA", "RNA", "protein"]


def test_public_dataset_catalog_is_empty_and_non_patient_by_default() -> None:
    root = Path(__file__).resolve().parents[1]
    catalog = (root / "data" / "public-dataset-catalog.yaml").read_text(encoding="utf-8")
    assert "data_classification: public_non_patient_only" in catalog
    assert "entries: []" in catalog
    schema = json.loads(
        (root / "api" / "public-dataset-catalog.schema.json").read_text(encoding="utf-8")
    )
    assert schema["properties"]["data_classification"]["const"] == "public_non_patient_only"
    assert schema["properties"]["entries"]["items"]["properties"]["patient_data"]["const"] is False


def test_public_candidate_sources_are_explicitly_unapproved_and_non_patient() -> None:
    root = Path(__file__).resolve().parents[1]
    catalog = yaml.safe_load(
        (root / "data" / "public-dataset-catalog.yaml").read_text(encoding="utf-8")
    )
    schema = json.loads(
        (root / "api" / "public-dataset-catalog.schema.json").read_text(encoding="utf-8")
    )
    assert catalog["entries"] == []
    assert catalog["data_classification"] == "public_non_patient_only"
    assert catalog["candidate_sources"]
    candidate_schema = schema["properties"]["candidate_sources"]["items"]
    assert (
        candidate_schema["properties"]["license_review_status"]["const"]
        == "verify_before_intake"
    )
    assert candidate_schema["properties"]["patient_data"]["const"] is False
    for candidate in catalog["candidate_sources"]:
        assert candidate["license_review_status"] == "verify_before_intake"
        assert candidate["patient_data"] is False


def test_admet_candidate_catalog_is_metadata_only_and_unapproved() -> None:
    root = Path(__file__).resolve().parents[1]
    catalog = yaml.safe_load(
        (root / "data" / "admet-source-catalog.yaml").read_text(encoding="utf-8")
    )
    schema = json.loads(
        (root / "api" / "admet-source-catalog.schema.json").read_text(encoding="utf-8")
    )
    assert catalog["data_classification"] == "public_non_patient_only"
    assert catalog["entries"] == []
    assert catalog["candidate_sources"]
    item_schema = schema["properties"]["candidate_sources"]["items"]["properties"]
    assert item_schema["license_review_status"]["const"] == "verify_before_intake"
    assert item_schema["patient_data"]["const"] is False
    assert schema["properties"]["entries"]["maxItems"] == 0
    for source in catalog["candidate_sources"]:
        assert source["license_review_status"] == "verify_before_intake"
        assert source["patient_data"] is False


def test_i2_i3_job_contracts_are_strictly_non_executable_and_validate_inputs() -> None:
    import json
    from jsonschema import Draft202012Validator

    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "insilico-job.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    artifact = {"format": "pdb", "source_sha256": "a" * 64, "source_size_bytes": 100}
    docking = {
        "schema_version": 1, "job_type": "docking", "research_only": True,
        "execution_authorized": False,
        "engine": {
            "engine_id": "candidate-engine", "version": "unapproved",
            "license_review": "pending",
        },
        "receptor": artifact, "ligand": {**artifact, "format": "sdf"},
        "preparation": {
            "receptor_protonation_policy": "caller-declared",
            "ligand_protonation_policy": "caller-declared",
            "charge_method": "not-run", "atom_typing": "not-run",
            "water_policy": "caller-declared",
        },
        "search_box": {"center_angstrom": [0, 0, 0], "size_angstrom": [20, 20, 20]},
        "seed": 42,
    }
    assert validator.is_valid(docking)
    assert not validator.is_valid({**docking, "execution_authorized": True})
    invalid_box = {
        **docking,
        "search_box": {"center_angstrom": [0, 0, 0], "size_angstrom": [20, 0, 20]},
    }
    assert not validator.is_valid(invalid_box)
    md = {
        "schema_version": 1, "job_type": "molecular_dynamics", "research_only": True,
        "execution_authorized": False,
        "engine": {
            "engine_id": "candidate-md", "version": "unapproved",
            "license_review": "pending",
        },
        "coordinates": artifact, "topology": {**artifact, "format": "topology"},
        "force_field": {
            "name": "unapproved", "version": "unapproved",
            "license_review": "pending", "parameter_source_sha256": "b" * 64,
        },
        "protocol": {
            "temperature_kelvin": 300, "pressure_bar": 1, "timestep_fs": 2,
            "steps": 100000, "equilibration_steps": 10000, "replicas": 3, "seed": 7,
        },
    }
    assert validator.is_valid(md)
    assert not validator.is_valid({**md, "protocol": {**md["protocol"], "replicas": 1}})


def test_i5_synthetic_cohort_schema_accepts_only_aggregate_non_patient_output() -> None:
    import json
    from jsonschema import Draft202012Validator

    from molecularis.virtual_cohort import simulate_hardy_weinberg_cohort

    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "virtual-cohort.schema.json").read_text(encoding="utf-8")
    )
    result = simulate_hardy_weinberg_cohort({"synthetic_locus_1": 0.25}, sample_size=100, seed=4)
    assert Draft202012Validator(schema).is_valid(result)
    invalid_patient = {**result, "data_classification": "patient_data"}
    assert not Draft202012Validator(schema).is_valid(invalid_patient)


def test_i2_i3_result_contracts_require_hashes_and_nonvalidated_status() -> None:
    import json
    from jsonschema import Draft202012Validator

    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "insilico-result.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    hashes = {
        "coordinates_or_receptor_sha256": "a" * 64,
        "ligand_or_topology_sha256": "b" * 64,
    }
    engine = {"engine_id": "unapproved", "version": "unapproved", "build_sha256": "c" * 64}
    docking = {
        "schema_version": 1, "job_type": "docking", "research_only": True,
        "validation_status": "not_independently_validated", "engine": engine,
        "input_hashes": hashes,
        "protocol": {
            "center_angstrom": [0, 0, 0], "box_size_angstrom": [20, 20, 20],
            "seed": 42, "exhaustiveness": 8, "n_poses_requested": 1, "cpu": 1,
            "scoring_function": "vina", "energy_range_kcal_per_mol": 3.0,
        },
        "protocol_sha256": "d" * 64,
        "poses": [{
            "rank": 1, "score": -7.2, "score_unit": "engine-defined",
            "pose_sha256": "e" * 64, "pose_pdbqt": "MODEL 1\nENDMDL\n",
        }],
        "limitations": ["Scores are not binding affinities."],
    }
    assert validator.is_valid(docking)
    assert not validator.is_valid({**docking, "validation_status": "validated"})
    md = {
        "schema_version": 1, "job_type": "molecular_dynamics", "research_only": True,
        "validation_status": "not_independently_validated", "engine": {**engine, "platform": "CPU"},
        "input_hashes": {
            **hashes,
            "coordinates_canonical_sha256": "7" * 64,
            "topology_canonical_sha256": "8" * 64,
        },
        "force_field": {
            "name": "synthetic harmonic reference", "version": "1",
            "parameter_source_sha256": "9" * 64, "system_sha256": "a" * 64,
        },
        "protocol": {
            "temperature_kelvin": 300, "pressure_bar": None, "timestep_fs": 1,
            "steps": 100, "equilibration_steps": 10, "replicas": 2, "seed": 1,
            "report_interval": 10, "cpu_threads": 1, "platform": "CPU",
            "integrator": "LangevinMiddleIntegrator", "friction_per_ps": 1.0,
            "integrator_seed_derivation": (
                "sha256(kinetics-openmm-seed-v1:base_seed:replica_index:integrator)"
                "[0:4] little-endian masked to 31 bits; zero mapped to 1"
            ),
            "velocity_seed_derivation": (
                "sha256(kinetics-openmm-seed-v1:base_seed:replica_index:velocities)"
                "[0:4] little-endian masked to 31 bits; zero mapped to 1"
            ),
        },
        "protocol_sha256": "d" * 64,
        "replicas": [
            {
                "replica_id": 1, "integrator_seed": 1, "velocity_seed": 11, "steps_completed": 100,
                "initial_potential_energy": -10.0, "final_potential_energy": -9.9,
                "energy_unit": "kJ/mol", "trajectory_sha256": "e" * 64,
                "trajectory_dcd_base64": "ZGF0YQ==",
            },
            {
                "replica_id": 2, "integrator_seed": 2, "velocity_seed": 12, "steps_completed": 100,
                "initial_potential_energy": -10.1, "final_potential_energy": -10.0,
                "energy_unit": "kJ/mol", "trajectory_sha256": "f" * 64,
                "trajectory_dcd_base64": "ZGF0YQ==",
            },
        ],
        "limitations": ["No independent stability validation."],
    }
    assert validator.is_valid(md)


def test_i4_pkpd_result_schema_accepts_reference_models_and_rejects_clinical_flags() -> None:
    import json
    from jsonschema import Draft202012Validator

    from molecularis.pkpd import emax_pd, one_compartment_oral_pk

    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "pkpd-result.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    pk = one_compartment_oral_pk(
        [0.0, 1.0], dose_amount_mg=10.0, bioavailability_fraction=0.5,
        absorption_rate_per_h=1.0, elimination_rate_per_h=0.1,
        apparent_volume_l=5.0,
    )
    pd = emax_pd(
        [0.0, 1.0], baseline_effect=0.0,
        maximum_effect_increment=1.0, ec50=0.5,
    )
    assert validator.is_valid(pk)
    assert validator.is_valid(pd)
    assert not validator.is_valid({**pk, "clinical_recommendation": "dose"})



def test_i5_synthetic_variant_effect_schema_rejects_patient_or_prediction_payloads() -> None:
    import json
    from jsonschema import Draft202012Validator

    from molecularis.virtual_cohort import simulate_synthetic_additive_variant_effects

    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "api" / "synthetic-variant-effect.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    result = simulate_synthetic_additive_variant_effects(
        {"synthetic_rs1": 0.3}, {"synthetic_rs1": 0.25},
        sample_size=1000, baseline_trait_mean=1.0,
        residual_standard_deviation=0.5, seed=5,
    )
    assert validator.is_valid(result)
    assert not validator.is_valid({**result, "data_classification": "patient_data"})
    assert not validator.is_valid({**result, "individual_predictions": []})
