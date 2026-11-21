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


## Agentics and scientific foundation release evidence

A release or service freeze involving Agentics must include the exact AI Constitution and Master Plan versions, implemented capability inventory, tool/package versions and licenses, data/model manifests, scientific contracts, pre-generation and independent verification tests, adversarial/failure tests, resource/security policy, provenance/reproducibility evidence and explicit limitations. Candidate tools listed in the registry are not treated as integrated dependencies. Engineering CI, benchmark evidence and independent scientific acceptance must be reported separately.
