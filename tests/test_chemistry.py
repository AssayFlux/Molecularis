from __future__ import annotations

import pytest

from molecularis.chemistry import (
    graph_descriptors, parse_sdf_record, path_fingerprint, substructure_match, tanimoto,
)


def molecule(elements: list[str], bonds: list[tuple[int, int, int]]) -> dict[str, object]:
    atoms = [{"element": element, "x": 0.0, "y": 0.0, "z": 0.0} for element in elements]
    return {"atoms": atoms, "bonds": bonds}


def test_sdf_v2000_parses_formula_and_rejects_non_finite_coordinates() -> None:
    counts = f"{2:3d}{1:3d}  0  0  0  0            999 V2000"
    atom_a = f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    atom_b = f"{1.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    bond = f"{1:3d}{2:3d}{1:3d}"
    parsed = parse_sdf_record(
        "\n".join([
            "ethane", "Molecularis", "", counts, atom_a, atom_b,
            bond, "M  END", "$$",
        ])
    )
    assert parsed["formula"] == "C2"
    assert parsed["atom_count"] == 2
    assert graph_descriptors(parsed)["cycle_rank"] == 0


def test_graph_descriptors_and_path_fingerprint_are_deterministic() -> None:
    ring = molecule(["C", "C", "C"], [(0, 1, 1), (1, 2, 1), (2, 0, 1)])
    result = graph_descriptors(ring)
    assert result["cycle_rank"] == 1
    assert result["connected_components"] == 1
    assert path_fingerprint(ring) == path_fingerprint(ring)


def test_exact_substructure_match_respects_elements_and_bond_order() -> None:
    target = molecule(["C", "C", "O"], [(0, 1, 1), (1, 2, 1)])
    carbon_pair = molecule(["C", "C"], [(0, 1, 1)])
    double_bond = molecule(["C", "C"], [(0, 1, 2)])
    oxygen_pair = molecule(["O", "O"], [(0, 1, 1)])
    assert substructure_match(target, carbon_pair)
    assert not substructure_match(target, double_bond)
    assert not substructure_match(target, oxygen_pair)


def test_substructure_search_has_a_hard_state_limit() -> None:
    target = molecule(["C"] * 8, [(index, index + 1, 1) for index in range(7)])
    query = molecule(["C"] * 4, [(index, index + 1, 1) for index in range(3)])
    with pytest.raises(ValueError, match="max_search_states"):
        substructure_match(target, query, max_search_states=1)


def test_tanimoto_handles_empty_and_disjoint_fingerprints() -> None:
    assert tanimoto(frozenset(), frozenset()) == 1
    assert tanimoto(frozenset({"a"}), frozenset({"b"})) == 0


def test_sdf_iterator_reads_multiple_records_and_skips_empty_blocks() -> None:
    from molecularis.chemistry import iter_sdf_records

    counts = f"{1:3d}{0:3d}  0  0  0  0            999 V2000"
    atom = f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    record = "\n".join(["methane", "Molecularis", "", counts, atom, "M  END"])
    parsed = list(iter_sdf_records(record + "\n$$$$\n\n" + record + "\n$$$$\n"))
    assert len(parsed) == 2
    assert parsed[0]["formula"] == "C"
    assert parsed[1]["atom_count"] == 1



def test_sdf_v3000_parses_basic_atom_and_bond_graph() -> None:
    block = "\n".join([
        "ethane", "Molecularis", "",
        "  0  0  0     0  0            999 V3000",
        "M  V30 BEGIN CTAB",
        "M  V30 COUNTS 2 1 0 0 0",
        "M  V30 BEGIN ATOM",
        "M  V30 1 C 0.0 0.0 0.0 0",
        "M  V30 2 C 1.5 0.0 0.0 0",
        "M  V30 END ATOM",
        "M  V30 BEGIN BOND",
        "M  V30 1 1 1 2",
        "M  V30 END BOND",
        "M  V30 END CTAB",
        "M  END",
    ])
    parsed = parse_sdf_record(block)
    assert parsed["format"] == "V3000"
    assert parsed["formula"] == "C2"
    assert parsed["bonds"] == [(0, 1, 1)]



def test_rdkit_backend_uses_sanitized_molecules_and_morgan_fingerprints() -> None:
    pytest.importorskip("rdkit")
    from molecularis.chemistry_rdkit import analyze_smiles, morgan_tanimoto

    ethanol = analyze_smiles("CCO")
    from hashlib import sha256

    assert ethanol["engine"] == "RDKit"
    assert ethanol["formula"] == "C2H6O"
    assert ethanol["morgan_fingerprint"]["algorithm"] == "Morgan"
    provenance = ethanol["input_provenance"]
    assert provenance["sha256_utf8"] == sha256(b"CCO").hexdigest()
    assert provenance["utf8_bytes"] == 3
    assumptions = ethanol["representation_assumptions"]
    assert assumptions["protonation"] == "input state retained; no protonation adjustment"
    assert assumptions["tautomer"] == "input tautomer retained; no tautomer canonicalization"
    assert assumptions["molecular_weight_unit"] == "Da"
    assert morgan_tanimoto("CCO", "CCO") == pytest.approx(1.0)
    assert morgan_tanimoto("CCO", "CC") < 1.0


def test_rdkit_backend_rejects_invalid_molecules() -> None:
    pytest.importorskip("rdkit")
    from molecularis.chemistry_rdkit import analyze_smiles

    with pytest.raises(ValueError):
        analyze_smiles("not a valid smiles string")


def test_rdkit_reference_sanity_fixture_script() -> None:
    pytest.importorskip("rdkit")
    import json
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, str(root / "validation" / "chemistry_reference.py")],
        cwd=root, check=True, capture_output=True, text=True,
    )
    result = json.loads(completed.stdout)
    assert result["overall_pass"] is True
    assert result["engine"]["engine"] == "RDKit"
    assert all(item["pass"] for item in result["results"])
    assert result["graph_parser_comparison"]["pass"] is True


def test_sdf_stream_parses_incrementally_and_enforces_record_budgets() -> None:
    from molecularis.chemistry import iter_sdf_stream

    counts = f"{1:3d}{0:3d}  0  0  0  0            999 V2000"
    atom_line = f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    record = ["carbon", "Molecularis", "", counts, atom_line, "M  END"]
    source = iter(record + ["$$$$"] + record)
    parsed = list(iter_sdf_stream(source, max_records=2))
    assert len(parsed) == 2
    assert all(item["formula"] == "C" for item in parsed)

    with pytest.raises(ValueError, match="max_records"):
        list(iter_sdf_stream(iter(record + ["$$$$"] + record), max_records=1))
    with pytest.raises(ValueError, match="max_record_chars"):
        list(iter_sdf_stream(iter(record), max_record_chars=10))
    with pytest.raises(ValueError, match="max_total_chars"):
        list(iter_sdf_stream(iter(record), max_total_chars=10))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_records": True},
        {"max_records": 1.5},
        {"max_record_chars": False},
        {"max_total_chars": 1.5},
    ],
)
def test_sdf_stream_rejects_non_integer_budgets(kwargs: dict[str, object]) -> None:
    from molecularis.chemistry import iter_sdf_stream

    with pytest.raises(ValueError, match="positive integer"):
        list(iter_sdf_stream(iter([]), **kwargs))


def test_rdkit_descriptor_schema_reports_chemistry_assumptions_and_extended_descriptors() -> None:
    pytest.importorskip("rdkit")
    from molecularis.chemistry_rdkit import analyze_smiles

    ethanol = analyze_smiles("CCO")
    assert ethanol["descriptor_schema_version"] == 2
    assert ethanol["formula"] == "C2H6O"
    assert ethanol["heavy_atom_count"] == 3
    assert ethanol["aromatic_atom_count"] == 0
    assert ethanol["formal_charge"] == 0
    assert ethanol["fraction_csp3"] == pytest.approx(1.0)
    assert ethanol["rule_of_five_screen"]["criterion_count"] == 4
    assert ethanol["rule_of_five_screen"]["pass_count"] == 4
    assert ethanol["rule_of_five_screen"]["all_criteria_pass"] is True
    assert ethanol["aliphatic_ring_count"] == 0
    assert ethanol["aromatic_ring_count"] == 0
    assert ethanol["representation_assumptions"]["crippen_logp_unit"] == "dimensionless"

    benzene = analyze_smiles("c1ccccc1")
    assert benzene["heavy_atom_count"] == 6
    assert benzene["aromatic_atom_count"] == 6
    assert benzene["aromatic_ring_count"] == 1
    assert benzene["fraction_csp3"] == pytest.approx(0.0)


def test_rdkit_inputs_are_bounded_by_utf8_bytes_and_reject_nul_or_invalid_unicode() -> None:
    pytest.importorskip("rdkit")
    from molecularis.chemistry_rdkit import analyze_smiles

    with pytest.raises(ValueError, match="UTF-8 limit"):
        analyze_smiles("é" * 600_000)
    with pytest.raises(ValueError, match="NUL"):
        analyze_smiles("CCO\x00")
    with pytest.raises(ValueError, match="Unicode"):
        analyze_smiles("CCO\ud800")


def test_rdkit_morgan_similarity_rejects_invalid_parameters_and_oversize_input() -> None:
    pytest.importorskip("rdkit")
    from molecularis.chemistry_rdkit import morgan_tanimoto

    with pytest.raises(ValueError, match="integer"):
        morgan_tanimoto("CCO", "CCO", radius=True)
    with pytest.raises(ValueError, match="power of two"):
        morgan_tanimoto("CCO", "CCO", bits=1000)
    with pytest.raises(ValueError, match="UTF-8 limit"):
        morgan_tanimoto("C" * 1_000_001, "CCO")


def test_bounded_sdf_graph_analysis_reports_provenance_and_explicit_atom_limitations() -> None:
    from hashlib import sha256

    from molecularis.chemistry import analyze_sdf_graph

    counts = f"{2:3d}{1:3d}  0  0  0  0            999 V2000"
    atom_a = f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    atom_b = f"{1.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'O':>3s}"
    bond = f"{1:3d}{2:3d}{1:3d}"
    source = "\n".join(
        ["ethanol-fragment", "Molecularis", "", counts, atom_a, atom_b, bond, "M  END", "$$$$"]
    )
    result = analyze_sdf_graph(source)
    assert result["source_sha256"] == sha256(source.encode("utf-8")).hexdigest()
    assert result["source_utf8_bytes"] == len(source.encode("utf-8"))
    assert result["formula_explicit_atoms"] == "CO"
    assert result["graph"]["atom_count"] == 2
    assert (
        "Implicit hydrogens are not inferred; formula and mass use explicit atoms only"
        in result["limitations"]
    )


def test_bounded_sdf_graph_analysis_rejects_invalid_records() -> None:
    from molecularis.chemistry import analyze_sdf_graph

    counts = f"{1:3d}{0:3d}  0  0  0  0            999 V2000"
    atom = f"{0.0:10.4f}{0.0:10.4f}{0.0:10.4f} {'C':>3s}"
    record = "\n".join(["carbon", "Molecularis", "", counts, atom, "M  END"])
    with pytest.raises(ValueError, match="NUL"):
        analyze_sdf_graph(record + "\x00")
    with pytest.raises(ValueError, match="UTF-8 limit"):
        analyze_sdf_graph(record, max_bytes=10)
    with pytest.raises(ValueError, match="Unicode"):
        analyze_sdf_graph(record + "\ud800")
    with pytest.raises(ValueError, match="exactly one"):
        analyze_sdf_graph(record + "\n" + "$" * 4 + "\n" + record)
