# Continuous Repository Work Protocol

## Start-of-session checklist
1. Read MASTER_ENGINEERING_RULEBOOK.md, PROJECT_CHARTER.md, MASTER_DEVELOPMENT_PLAN.md, ARCHITECTURE.md, and SERVICE_STATUS.md.
2. Fetch current CORE HEAD; never assume the previous session's SHA is current.
3. Inspect the active service's scope, decisions, backlog, and protected-file register.
4. Check CI and test baseline; identify pre-existing failures separately from new failures.
5. Confirm the exact task and acceptance criteria before editing.

## During work
- Work only on CORE and preserve Git history.
- Keep changes within the active task's approved scope.
- Prefer small, coherent commits; avoid oversized multi-file edits.
- Never create placeholder behavior and describe it as functional.
- Do not modify frozen service files without explicit authorization.
- Update decisions, status, backlog, and documentation when implementation facts change.
- Do not use external scientific engines as hidden execution backends.
- Keep generated files, dependencies, licenses, and data provenance explicit.

## Before committing
1. Review the complete diff and changed-path list.
2. Check for accidental deletions, unrelated formatting, generated secrets, binaries, and asset changes.
3. Run relevant unit, integration, schema, static, and packaging checks.
4. Run the full required CI suite when feasible.
5. Record tests that could not run and why.
6. Confirm documentation accurately describes actual behavior.
7. Commit directly to CORE with a specific message.
8. Re-fetch CORE and verify the resulting commit and tree.

## End-of-session handoff
Update SERVICE_STATUS.md, docs/WORK_BACKLOG.md, and the active service's progress record. Record commit SHA, completed work, test outcomes, known issues, next exact task, and files that must not be touched. Never report success without repository evidence.

## Stop conditions
Stop before editing if branch identity is uncertain, a concurrent CORE update is detected, a protected file would be changed without authorization, the task would require deleting unreviewed user work, or scientific acceptance criteria are unclear.


## Agentics and scientific foundation work

Before building or integrating an AI/scientific capability, inspect the current Master Plan, AI Constitution, existing Core/MSDE contracts, A–N service implementations, dependencies, licenses and tests. Distinguish planned modules from implemented ones. Reuse existing artifact/provenance, capability and workflow infrastructure; do not add parallel stores or runtimes.

For each scientific capability, define its discipline, domain, assumptions, units, applicability, method, uncertainty, resource envelope, tool/data provenance, independent verification and acceptance evidence. Model output is untrusted input. Every scientific generation path needs pre-generation audit and independent post-generation verification. Update status/backlog only from verified commits and test results; engineering CI is not scientific acceptance.
