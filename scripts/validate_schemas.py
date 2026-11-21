"""Validate repository JSON Schemas against their declared drafts."""
from __future__ import annotations
import json
from pathlib import Path
from jsonschema.validators import validator_for
ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "venv", "node_modules", "__pycache__"}
def main() -> int:
    schemas = sorted(p for p in ROOT.rglob("*.schema.json") if not any(x in EXCLUDED for x in p.parts))
    errors = []
    for path in schemas:
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            validator_for(document).check_schema(document)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {type(exc).__name__}: {exc}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(schemas)} JSON Schemas.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
