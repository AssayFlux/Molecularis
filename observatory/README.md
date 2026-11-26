# Molecularis Observatory

A read-only, browser-based live repository control centre for Agentics Molecularis.

## Run locally

From the repository root:

```bash
python -m http.server 8765 --directory observatory
```

Open [http://localhost:8765](http://localhost:8765).

The dashboard fetches the `CORE` branch's recursive Git tree, `capabilities/registry.yaml`, and recent commit metadata from the public GitHub API. An internet connection is required. It does not require a Python package installation.

## What it reports

- Repository file and Python source counts from the live Git tree.
- Test-module count as file presence only; it does not execute tests or imply passing status.
- Service directory and contract-document inventory.
- Capability declarations and their declared evidence level.
- Recent commit metadata.
- Explicit limits around scientific validation, dataset permissions, model availability, and execution status.

## Integrity rules

1. A declared capability is not a validated capability.
2. A test file is not a passing test.
3. A CI workflow file is not a successful CI run.
4. An adapter is not proof that its external executable, database, model weights, or hardware are installed.
5. Unknown and unverified states remain unknown; the dashboard does not fabricate readiness percentages.

## Design

The interface adapts the Director X design language: warm editorial surfaces, restrained accents, reusable cards, readable hierarchy, responsive layouts, and ten selectable palettes. It is a web implementation and does not import Director X's Android/Kotlin code.

## Scope of this release

Read-only telemetry only. No repository writes, training jobs, scientific calculations, workflow execution, authentication, or operational control endpoints are exposed.
