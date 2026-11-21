from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from molecularis.advanced_science import (
    _tree_digest,
    run_alphafold3,
    run_molprobity_cli,
    run_nuad_design,
)


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_hash(path: Path) -> str:
    return str(_tree_digest(path, max_files=100, max_bytes=1024 * 1024)["sha256"])


def test_alphafold3_runner_executes_pinned_local_runtime_and_hashes_outputs(tmp_path: Path) -> None:
    python = Path(sys.executable)
    script = tmp_path / "run_alphafold.py"
    script.write_text(
        "import argparse, pathlib\n"
        "p=argparse.ArgumentParser()\n"
        "for n in ['json_path','model_dir','output_dir','db_dir','jax_backend','flash_attention_implementation']:\n"
        " p.add_argument('--'+n, required=True)\n"
        "a=p.parse_args()\n"
        "pathlib.Path(a.output_dir, 'prediction.cif').write_text('data_prediction\\n')\n",
        encoding="utf-8",
    )
    model = tmp_path / "model"
    model.mkdir()
    (model / "weights.bin").write_bytes(b"model-weights")
    database = tmp_path / "database"
    database.mkdir()
    (database / "sequences.fa").write_text(">seq\nACGT\n", encoding="utf-8")
    input_json = tmp_path / "input.json"
    input_json.write_text(json.dumps({"name": "test", "sequences": [{"protein": {"id": "A", "sequence": "ACDE"}}]}), encoding="utf-8")

    result = run_alphafold3(
        input_json, tmp_path / "out", python_executable=python,
        python_sha256=_hash(python), run_script=script,
        run_script_sha256=_hash(script), model_directory=model,
        model_directory_sha256=_tree_hash(model), database_directory=database,
        database_directory_sha256=_tree_hash(database), run_id="af3-test",
        timeout_seconds=30,
    )
    assert result["execution_status"] == "completed"
    assert result["scientific_validation"] == "not_assessed"
    assert result["structure_artifacts"][0]["path"] == "prediction.cif"
    assert len(result["structure_artifacts"][0]["sha256"]) == 64


def test_alphafold3_runner_rejects_model_digest_mismatch_before_execution(tmp_path: Path) -> None:
    python = Path(sys.executable)
    script = tmp_path / "run.py"
    script.write_text("raise SystemExit(99)", encoding="utf-8")
    model = tmp_path / "model"
    model.mkdir()
    (model / "w").write_bytes(b"w")
    database = tmp_path / "db"
    database.mkdir()
    (database / "db").write_bytes(b"d")
    source = tmp_path / "input.json"
    source.write_text('{"name":"x","sequences":[{}]}', encoding="utf-8")
    with pytest.raises(ValueError, match="model directory SHA-256 mismatch"):
        run_alphafold3(
            source, tmp_path / "out", python_executable=python,
            python_sha256=_hash(python), run_script=script,
            run_script_sha256=_hash(script), model_directory=model,
            model_directory_sha256="0" * 64, database_directory=database,
            database_directory_sha256=_tree_hash(database), run_id="x",
        )


def test_molprobity_runner_executes_allowlisted_tool_and_returns_raw_output(tmp_path: Path) -> None:
    executable = tmp_path / "clashscore"
    executable.write_text("#!/bin/sh\nprintf 'clashscore: 1.2\\n'\n", encoding="utf-8")
    executable.chmod(0o755)
    pdb = tmp_path / "input.pdb"
    pdb.write_text("HEADER    TEST\n", encoding="utf-8")
    result = run_molprobity_cli(
        pdb, tmp_path / "out", executable_path=executable,
        executable_sha256=_hash(executable), tool="clashscore", run_id="mp-1",
    )
    assert result["execution_status"] == "completed"
    assert result["scientific_validation"] == "tool_completed"
    assert "clashscore: 1.2" in result["stdout"]
    assert len(result["stdout_sha256"]) == 64


def test_molprobity_runner_rejects_unknown_tool_and_bad_executable_digest(tmp_path: Path) -> None:
    executable = tmp_path / "tool"
    executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    executable.chmod(0o755)
    pdb = tmp_path / "input.pdb"
    pdb.write_text("HEADER TEST\n", encoding="utf-8")
    with pytest.raises(ValueError, match="tool must be"):
        run_molprobity_cli(pdb, tmp_path / "out", executable_path=executable,
            executable_sha256=_hash(executable), tool="arbitrary-command", run_id="x")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        run_molprobity_cli(pdb, tmp_path / "out", executable_path=executable,
            executable_sha256="0" * 64, tool="clashscore", run_id="x")


def test_nuad_runner_uses_seeded_bounded_search_and_exports_strands(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConstraint:
        pass

    class FakeStrand:
        name = "strand-A"

        def sequence(self) -> str:
            return "ACGTAC"

    class FakeDesign:
        def __init__(self) -> None:
            self.strands = [FakeStrand()]

    class FakeSearchParameters:
        def __init__(self, **kwargs: object) -> None:
            self.kwargs = kwargs

    design = FakeDesign()
    calls: list[object] = []
    search_module = ModuleType("nuad.search")
    search_module.SearchParameters = FakeSearchParameters
    search_module.search_for_sequences = lambda d, p: calls.append((d, p))
    constraints_module = ModuleType("nuad.constraints")
    constraints_module.Design = FakeDesign
    constraints_module.Constraint = FakeConstraint
    nuad_module = ModuleType("nuad")
    nuad_module.__path__ = []  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "nuad", nuad_module)
    monkeypatch.setitem(sys.modules, "nuad.search", search_module)
    monkeypatch.setitem(sys.modules, "nuad.constraints", constraints_module)

    result = run_nuad_design(design, [FakeConstraint()], tmp_path / "nuad-out",
                             random_seed=17, max_iterations=1000, run_id="nuad-1")
    assert len(calls) == 1
    assert result["execution_status"] == "completed"
    assert result["strands"] == [{"name": "strand-A", "sequence": "ACGTAC"}]
    assert json.loads(Path(result["sequence_artifact"]["path"]).read_text())["random_seed"] == 17


def test_nuad_runner_rejects_non_dna_sequences(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeConstraint:
        pass

    class FakeDesign:
        strands = [SimpleNamespace(name="bad", sequence=lambda: "ACGN")]

    class FakeSearchParameters:
        def __init__(self, **kwargs: object) -> None:
            pass

    search_module = ModuleType("nuad.search")
    search_module.SearchParameters = FakeSearchParameters
    search_module.search_for_sequences = lambda d, p: None
    constraints_module = ModuleType("nuad.constraints")
    constraints_module.Design = FakeDesign
    constraints_module.Constraint = FakeConstraint
    nuad_module = ModuleType("nuad")
    nuad_module.__path__ = []  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "nuad", nuad_module)
    monkeypatch.setitem(sys.modules, "nuad.search", search_module)
    monkeypatch.setitem(sys.modules, "nuad.constraints", constraints_module)
    with pytest.raises(RuntimeError, match="invalid or incomplete"):
        run_nuad_design(FakeDesign(), [FakeConstraint()], tmp_path / "bad-out",
                        random_seed=1, max_iterations=5, run_id="bad")


def test_molprobity_oneline_analysis_receives_isolated_input_directory(tmp_path: Path) -> None:
    executable = tmp_path / "oneline-analysis"
    executable.write_text(
        "#!/bin/sh\\n"
        "test -d \"$1\" || exit 8\\n"
        "test -f \"$1/input.pdb\" || exit 9\\n"
        "printf 'summary\\n'\\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    pdb = tmp_path / "input.pdb"
    pdb.write_text("HEADER TEST\\n", encoding="utf-8")
    result = run_molprobity_cli(
        pdb, tmp_path / "oneline-out", executable_path=executable,
        executable_sha256=_hash(executable), tool="oneline-analysis", run_id="mp-summary",
    )
    assert "summary" in result["stdout"]
    assert (tmp_path / "oneline-out" / "input" / "input.pdb").is_file()
