# Molecularis

**Molecularis is a Molecularis-native, modular scientific computing system** for molecular science, sequence analysis, structural biology, chemistry, protein science, genomics, DNA/RNA, simulation, kinetics, omics, phylogenetics, pharmacogenomics, cohorts and reproducible scientific workflows.

Its purpose is to turn scientific methods into explicit, testable capabilities and connect them through versioned contracts, immutable data artifacts, provenance and executable Rulebooks.

## North Star

Build a trustworthy scientific system in which every result can be traced to its inputs, method, build, parameters, reference data and validation evidence. Accuracy, uncertainty, approximation and incompleteness must be explicit. See [docs/NORTH_STAR.md](docs/NORTH_STAR.md).

## Development sequence: one service at a time

After the shared Core/MSDE foundation passes its platform gate, services are built in this strict order:

A. Molecular  
B. Sequence  
C. Structure  
D. Chemistry  
E. Protein  
F. Genomics  
G. DNA/RNA  
H. Simulation  
I. Kinetics  
J. Omics  
K. Phylogeny  
L. Pharmacogenomics  
M. Cohorts  
N. Workflows

Each step includes discovery, specification, native engine, runtime, Rulebook, schemas/contracts, integration, tests, independent scientific validation, documentation and a freeze review. The next service does not begin until the active service is accepted. Full criteria and rationale: [Service Roadmap](docs/SERVICE_ROADMAP.md).

## Architecture

- `CORE/` — shared platform and the Molecularis Scientific Data Engine (MSDE) specifications/implementation.
- `services/<service>/` — service-owned ENGINE, RUNTIME, RULEBOOK and metadata; source, tests, schemas, data and benchmarks are added as each service is built.
- `python/molecularis/` and `python/kinetics/` — existing Python implementation; retained and audited before migration.
- `api/`, `schemas/` — versioned contracts.
- `capabilities/registry.yaml` — capability inventory; registration is not proof of implementation or scientific validation.
- `data/`, `validation/` — reference metadata, fixtures and validation assets.
- `remote-node/` — isolated remote execution component.
- `scripts/`, `tests/` — engineering checks and automated tests.
- `Assets/` — retained project identity and visual assets.

The **Engine** implements domain operations. The **Runtime** governs execution lifecycle and resources. The **Rulebook** expresses domain rules, generation/selection procedures and acceptance criteria. **Core/MSDE** provides shared contracts, artifact storage/query and provenance; it does not own domain science.

## Current implementation reality

The repository contains existing Python capabilities and tests, service specification scaffolds, governance documents and an MSDE architecture specification. The MSDE storage/index runtime and the A–N service implementations are not yet complete. Do not infer scientific readiness from a scaffold, capability registry entry or generic CI pass.

Latest recorded baseline: 557 tests passed, 12 skipped, 0 failed in GitHub Actions run [#127](https://github.com/AssayFlux/Molecularis/actions/runs/44879631802). Skips are associated with optional scientific dependencies (including RDKit, Biopython, pysam, Parasail and Biotite); those capabilities still require execution in dedicated dependency profiles and scientific validation. This is a software baseline, not a scientific accuracy certification.

## Development

Python 3.10 or newer:

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e .
pytest
python scripts/check_registry.py
```

Optional scientific dependencies, model weights, large reference databases and licensed runtimes are managed separately. Every dependency and dataset must be reviewed for provenance, licensing, security and reproducibility.

## Governing documents

- [North Star](docs/NORTH_STAR.md) — mission and non-negotiable principles.
- [Service Roadmap A–N](docs/SERVICE_ROADMAP.md) — ordered service steps and exit gates.
- [Master Development Plan](docs/MASTER_DEVELOPMENT_PLAN.md) — platform phases and system completion.
- [Master Engineering Rulebook](MASTER_ENGINEERING_RULEBOOK.md) — binding engineering policy.
- [Future Architecture](docs/FUTURE_ARCHITECTURE.md) — long-term design and research register.
- [Service Status](docs/SERVICE_STATUS.md) — evidence-based implementation status.
- [Work Backlog](docs/WORK_BACKLOG.md) — next actionable work.
- [Continuous Work Protocol](docs/CONTINUOUS_WORK_PROTOCOL.md) — repository operating procedure.
- [Scientific Validation Standard](docs/SCIENTIFIC_VALIDATION_STANDARD.md) — evidence and acceptance.
- [MSDE Architecture](docs/MSDE_ARCHITECTURE.md) — shared data substrate.

## Scientific integrity and security

- Implemented does not mean validated; prediction does not mean measurement.
- Preserve provenance, uncertainty, limitations and failed/intermediate evidence.
- Use independent validation where scientifically appropriate.
- Do not commit patient data, identifiable human-subject data, credentials or private datasets.
- External scientific tools are optional adapters/references, not hidden mandatory execution backends.

See [LICENSE](LICENSE) and [SECURITY.md](SECURITY.md).
