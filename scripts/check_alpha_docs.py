#!/usr/bin/env python3
"""Validate that the Alpha all-device documentation set is complete."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "NORTH_STAR.md",
    "ROADMAP.md",
    "DECISIONS.md",
    "CONTRIBUTING.md",
    "docs/architecture.md",
    "docs/alpha/README.md",
    "docs/alpha/MASTERPLAN.md",
    "docs/alpha/LANGUAGE_STRATEGY.md",
    "docs/alpha/DEVICE_MATRIX.md",
    "docs/alpha/MIGRATION_PLAN.md",
    "docs/alpha/INTEGRATION_CATALOG.md",
    "docs/alpha/DATA_MODEL.md",
    "docs/alpha/API_AND_JOB_CONTRACTS.md",
    "docs/alpha/OPERATIONS_AND_COMPUTE.md",
    "docs/alpha/SECURITY_AND_VALIDATION.md",
    "docs/alpha/TEST_STRATEGY.md",
    "docs/alpha/BACKLOG.md",
    "docs/alpha/RISK_REGISTER.md",
    "docs/alpha/RELEASE_AND_GOVERNANCE.md",
    "docs/alpha/adr/0001-all-device-architecture.md",
]
REQUIRED_PHRASES = {
    "NORTH_STAR.md": ["all-device", "C++", "Rust", "Python"],
    "docs/alpha/MASTERPLAN.md": ["Alpha", "Mol*", "Galaxy", "Molecularis Node"],
    "docs/alpha/INTEGRATION_CATALOG.md": ["Biotite", "AlphaFold", "OpenMM", "NUAD", "SciREPL"],
}
missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
errors = []
for rel, phrases in REQUIRED_PHRASES.items():
    path = ROOT / rel
    if path.is_file():
        body = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase.casefold() not in body.casefold():
                errors.append(f"{rel}: missing required phrase {phrase!r}")
if missing or errors:
    for item in missing:
        print(f"MISSING: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    sys.exit(1)
print(f"Alpha documentation check passed: {len(REQUIRED)} required files present.")
