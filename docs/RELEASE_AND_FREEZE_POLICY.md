# Release, Completion and Freeze Policy

## Completion package
A completed service must include approved specifications, engine/runtime/Rulebook documents, implementation, schemas, tests, scientific validation report, benchmark report, dependency/license inventory, changelog, and completion record.

## Freeze review
Review:
- All acceptance criteria and exclusions.
- Test and CI evidence.
- Scientific evidence level and limitations.
- API/schema compatibility.
- Security and resource behavior.
- Reproducibility and provenance.
- Documentation accuracy.
- Outstanding defects and explicit waivers.

## Freeze record
Record service version, commit SHA, date, reviewer/authorization, protected paths, supported contract versions, evidence level, test matrix, known limitations, and rollback reference.

## Post-freeze changes
Require explicit authorization and a change request. Re-run all affected regression and scientific validation tests. Increment service version according to compatibility impact. Update changelog and completion record. No drive-by refactoring of frozen paths.
