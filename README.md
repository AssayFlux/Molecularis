# Molecularis Engine

Molecularis is a modular scientific-computing engine for sequence, genomics, protein, structural biology, chemistry, molecular dynamics, omics, phylogenetics and related computational research.

The repository is intentionally focused on the scientific Engine. Product UI, mobile application code, archived planning documents and obsolete project scaffolding are maintained outside this codebase.

## Architecture

- `python/molecularis/` — scientific algorithms, domain workflows, execution adapters, provenance and validation.
- `python/kinetics/` — kinetics domain package.
- `api/` and `schemas/` — versioned input, execution and scientific-result contracts.
- `capabilities/registry.yaml` — explicit capability inventory; implementation status is not scientific validation.
- `data/` and `datapacks/` — public reference metadata and future local reference packs.
- `remote-node/` — isolated remote execution service and contract tests.
- `scripts/` — repository validation and reproducibility utilities.
- `tests/` — automated scientific and software tests.
- `validation/` — independent reference comparisons, smoke tests and pinned optional dependencies.
- `Assets/` — project identity and retained visual assets.

The Engine is separate from the planned Rulebook. The Rulebook will express scientific objectives, generation strategies, constraints and acceptance criteria; it will call Engine capabilities rather than duplicate scientific algorithms.

## Development

Python 3.10 or newer:

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e .
pytest
python scripts/check_registry.py
```

Optional scientific backends are installed separately using their documented dependency profiles. Model weights, large scientific databases and licensed runtimes are not bundled. Every external dependency must be used under its own terms.

## Scientific integrity

- A registered or implemented capability is not automatically scientifically validated.
- Outputs must retain relevant input, software, model, parameter and reference-data provenance.
- Independent validation and benchmark evidence are required before scientific accuracy claims.
- Unsupported, unverified or ambiguous results must remain explicitly marked.
- Do not commit patient data, identifiable human-subject data, credentials or private datasets. Tests and CI must use synthetic or appropriately public fixtures.

See [LICENSE](LICENSE) and [SECURITY.md](SECURITY.md) for repository terms and security reporting.
