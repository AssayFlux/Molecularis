# Change Control and Protected Files

## Change classes
- C0 Documentation correction: no behavior or contract change.
- C1 Internal refactor: behavior and public contracts demonstrably unchanged.
- C2 Compatible feature: additive behavior with backward compatibility.
- C3 Breaking change: contract, data format, or behavior incompatibility.
- C4 Critical remediation: security, data integrity, or scientific correctness defect.

## Authorization
Before modifying frozen files, submit a change record containing reason, evidence, exact paths, impact, migration plan, tests, rollback plan, and requested authorization. Do not proceed until explicit authorization is given. C4 remediation must be narrowly scoped and fully documented.

## Required safeguards
- CORE only; verify current HEAD before update.
- Never force-push or rewrite history.
- No unreviewed bulk moves or deletions.
- Preserve Assets and user data unless explicit authorization says otherwise.
- Maintain compatibility shims when moving public modules, until a deprecation plan is approved.
- Update schemas and contract versions deliberately.
- Record every C2-C4 decision in docs/DECISION_LOG.md.
- Update CHANGELOG and service completion record for affected service.

## Commit requirements
Each commit should represent one coherent approved task, use an imperative message, and be traceable to a work item or decision. Verify commit SHA and changed paths after updating CORE.


## Agentics scientific-document and architecture changes

Changes to the Agentics Master Plan, AI Constitution, shared scientific contracts, tool governance, model/data policy or service scientific acceptance criteria are architectural or scientific changes. Record rationale, exact files, compatibility impact, evidence, dependency/license implications, tests, rollback and approval as required by this policy. Supporting AI documents must remain subordinate to the single Agentics Master Plan. Do not silently change scientific thresholds or promote a candidate tool to a required dependency.
