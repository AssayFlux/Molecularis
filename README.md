# Molecularis

**Molecularis is a Molecularis-native, modular scientific computing system** for molecular science, sequence analysis, structural biology, chemistry, protein science, genomics, DNA/RNA, simulation, kinetics, omics, phylogenetics, pharmacogenomics, cohorts and reproducible scientific workflows.

Its purpose is to turn scientific methods into explicit, testable capabilities and connect them through versioned contracts, immutable data artifacts, provenance and executable Rulebooks.

## North Star

Build a trustworthy scientific system in which every result can be traced to its inputs, method, build, parameters, reference data and validation evidence. Accuracy, uncertainty, approximation and incompleteness must be explicit. See [docs/NORTH_STAR.md](docs/NORTH_STAR.md).

## Development sequence: one service at a time

After the shared Core/MSDE foundation passes its platform gate, services are built in this strict order:

A. Molecular · B. Sequence · C. Structure · D. Chemistry · E. Protein · F. Genomics · G. DNA/RNA · H. Simulation · I. Kinetics · J. Omics · K. Phylogeny · L. Pharmacogenomics · M. Cohorts · N. Workflows.

Each step includes discovery, specification, native engine, runtime, Rulebook, schemas/contracts, integration, tests, independent scientific validation, documentation and a freeze review. The next service does not begin until the active service is accepted. Full criteria: [Service Roadmap](docs/SERVICE_ROADMAP.md).

## Architecture

- `CORE/` — shared contracts and Molecularis Scientific Data Engine (MSDE).
- `services/<service>/` — service-owned ENGINE, RUNTIME, RULEBOOK and metadata.
- `python/molecularis/platform/` — local Core reference runtime, immutable artifact store, catalog, capability registry and Rulebook executor.
- `python/molecularis/` and `python/kinetics/` — existing scientific implementations; retained pending audit/migration.
- `api/`, `schemas/` — versioned contracts.
- `capabilities/registry.yaml` — capability inventory; registration is not proof of validation.
- `services/kinetics/` — canonical mass-action reaction-network artifacts, bounded RK4 integration, and retained Michaelis–Menten / exploratory PK/PD primitives.
- `data/`, `validation/` — reference metadata and validation assets.
- `remote-node/` — isolated remote execution component.
- `scripts/`, `tests/` — engineering checks and automated tests.
- `Assets/` — retained project identity and visual assets.

The **Engine** implements domain operations. The **Runtime** governs lifecycle and resources. The **Rulebook** expresses domain rules and acceptance criteria. **Core/MSDE** provides shared contracts, artifact storage, metadata lookup and provenance; it does not own domain science.

## Current implementation reality

The local Core/MSDE reference slice now includes immutable SHA-256 blobs, SQLite WAL catalog, lineage, bounded streaming, integrity audit, exact/numeric metadata lookup, snapshot-bound pagination, capability registration, Rulebook DAG execution and success/failure run evidence. Optional sequence, genomics and chemistry CI profiles are configured. It remains a local single-catalog reference implementation—not a distributed production platform. Native sorted-segment indexes, robust recovery certification, general query planning, cross-process discovery, C++/Rust interoperability and OS-level sandboxing remain open.

Latest fully green core CI remains [run #132](https://github.com/AssayFlux/Molecularis/actions/runs/44880497095). [Run #133](https://github.com/AssayFlux/Molecularis/actions/runs/44880802259) passed all three optional scientific profile jobs but failed core schema validation because one legacy schema contained literal escape wrappers; that file is corrected in the current change and the next run is authoritative. Software CI is not scientific accuracy certification.

## Development

Python 3.10 or newer:

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e .
pytest
python scripts/check_registry.py
```

## Governing documents

- [North Star](docs/NORTH_STAR.md)
- [Service Roadmap A–N](docs/SERVICE_ROADMAP.md)
- [Master Development Plan](docs/MASTER_DEVELOPMENT_PLAN.md)
- [Master Engineering Rulebook](MASTER_ENGINEERING_RULEBOOK.md)
- [Future Architecture](docs/FUTURE_ARCHITECTURE.md)
- [Service Status](docs/SERVICE_STATUS.md)
- [Work Backlog](docs/WORK_BACKLOG.md)
- [Continuous Work Protocol](docs/CONTINUOUS_WORK_PROTOCOL.md)
- [Scientific Validation Standard](docs/SCIENTIFIC_VALIDATION_STANDARD.md)
- [MSDE Architecture and Implementation Plan](CORE/data-engine/README.md)

## Scientific integrity and security

Implemented does not mean validated; prediction does not mean measurement. Preserve provenance, uncertainty, limitations and failed/intermediate evidence. Use independent validation where scientifically appropriate. Do not commit patient data, identifiable human-subject data, credentials or private datasets. External scientific tools are optional adapters/references, not hidden mandatory execution backends.

See [LICENSE](LICENSE) and [SECURITY.md](SECURITY.md).
