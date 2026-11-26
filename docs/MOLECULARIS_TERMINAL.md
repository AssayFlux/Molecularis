# Molecularis Terminal

Molecularis Terminal is a local command-line workbench for the real A–N service
runtime. It bootstraps the same service registrars used by the platform, then
exposes the capability registry and executes a selected capability through the
Core Rulebook executor and ArtifactStore.

## Install

From the repository root:

```bash
python -m pip install -e .
molecularis --help
```

No extra dependency is required beyond the base project installation.

## Commands

```bash
molecularis doctor
molecularis services
molecularis list
molecularis list --service sequence
molecularis show sequence.analyze.v1
molecularis run sequence.analyze.v1 --input '{"sequence_artifact_id":"art_..."}'
molecularis shell
```

Use `--workspace PATH` to choose where the local ArtifactStore persists data.
The default is `.molecularis-workspace` in the current directory. The same
workspace can be reused across sessions.

The `run` command accepts a JSON object whose keys are the Rulebook input names
for that capability. Input can be inline JSON or a file prefixed with `@`:

```bash
molecularis run example.capability.v1 --input @inputs/example.json --params '{"mode":"strict"}'
```

Use `show CAPABILITY_ID` to inspect the registered input/output schema IDs and
description before constructing an input. The CLI deliberately does not guess
missing scientific inputs or silently fabricate artifacts.

## What the diagnostics mean

- **Registered** means the A–N bootstrap declared the capability.
- **Handler bound** means the runtime has a Python handler for it.
- **Execution succeeded** means the handler ran and its output was persisted
  through the Rulebook/ArtifactStore path.
- **Scientific validation** is a separate question. This terminal does not
  certify scientific correctness, physical stability, experimental
  reproducibility, clinical validity or suitability for a research decision.
- Some operations require an existing Molecularis artifact ID. Create/import
  the required typed artifact with the relevant service API or a future
  guided input workflow. Some optional operations additionally require RDKit,
  OpenMM, Vina, GROMACS, reference datasets, model weights or external tools.

The terminal reports a capability as registered even if its optional external
runtime is not installed. Attempting that operation will report the actual
runtime error. A successful inventory is not a claim that all external
dependencies are available.

## Guided capability test lab

`molecularis testlab` runs deterministic, built-in fixture cases for
capabilities that have an explicit local fixture provider. The initial suite
covers the five Sequence service operations. It creates typed sequence
artifacts in the selected workspace, executes each operation through its
native Sequence Rulebook and checks a small deterministic output assertion.

`molecularis testlab --service chemistry` demonstrates honest coverage
reporting: until reviewed chemistry fixtures are added, those registered
capabilities are marked `NOT_COVERED`, not passed or simulated. The JSON report
includes registered counts, case outcomes, execution run IDs, output artifact
IDs, and coverage for every capability in the selected service.

Fixture smoke tests establish that a software path executes against a known
input and returns an expected basic result. They are not scientific reference
validation, benchmark evidence, or a substitute for independent review.
