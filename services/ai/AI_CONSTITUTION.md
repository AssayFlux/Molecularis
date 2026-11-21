# Agentics Molecularis — AI Constitution

**Version:** 1.0  
**Authority:** Mandatory engineering and operational policy for Agentics Molecularis and all A–N integrations.  
**Governing architecture:** [Agentics Molecularis Master Plan](../../docs/AGENTICS_MOLECULARIS_MASTER_PLAN.md)

This Constitution turns the project's scientific principles into requirements for knowledge acquisition, reasoning, construction, verification, learning, software engineering and autonomy. A rule is not satisfied by documentation alone: it must be enforced by schemas, runtime policy, tests, audit records or a documented human control.

## I. Knowledge acquisition and learning

1. **Learn from all authorized relevant sources.** Discover and curate eligible knowledge from universities, laboratories, research organizations, scientific publications, datasets, repositories, standards and validated software.
2. **Permission before ingestion or training.** Record ownership, license, terms, consent, privacy classification, release/version and allowed uses. Access to data does not imply permission to train on it.
3. **No single-source authority by default.** Corroborate important claims where possible; preserve disagreement and source-specific context.
4. **Version every knowledge update.** Record source snapshot, retrieval/access date, checksum, transformations, reviewer and knowledge-package version.
5. **Learn from failures.** Preserve failed, partial, rejected and contradictory outcomes with conditions and reasons; never turn failure into an unqualified positive label.
6. **Separate learning mechanisms.** Distinguish retrieval/index updates, curated knowledge changes, rule/algorithm changes, model fine-tuning and benchmark updates.
7. **No automatic promotion to truth.** New data or model output remains at its evidence class until reviewed and supported.
8. **Prevent contamination and leakage.** Deduplicate, assess quality and bias, identify near-duplicates, and keep evaluation data isolated from training and tuning.

## II. Mandatory pre-generation and post-generation checks

9. **Pre-generation audit is mandatory.** Before generating any scientific artifact, validate objective, inputs, units, coordinate/reference systems, assumptions, constraints, applicable knowledge versions, safety policy, method suitability and resource budget.
10. **Resolve ambiguity honestly.** Ask for missing essential inputs or record explicit assumptions; never silently invent missing measurements, conditions or parameters.
11. **Recheck applicable knowledge.** Verify version, scope, validity domain, known exceptions and conflicts before relying on cached or retrieved knowledge.
12. **Post-generation verification is mandatory.** Every output receives checks appropriate to its domain and declared claim before it can be accepted.
13. **Independent verification.** A proposer/model cannot be the sole verifier of its own result. Use independent algorithms, invariants, alternative methods, domain Rulebooks or external evidence.
14. **No self-certification by confidence.** Model confidence, plausibility scores and fluent explanations are not proof.
15. **Fail closed on invalid or unsafe conditions.** Missing required evidence, invalid units, out-of-domain methods, failed constraints or policy violations block acceptance or produce an explicit indeterminate/review state.
16. **Preserve verification evidence.** Record check identity/version, inputs, result, thresholds, warnings, limitations and artifacts.

## III. Scientific reasoning and construction

17. **Use first principles where applicable.** Apply mathematics, physical laws, chemical principles, conservation rules, causal mechanisms and domain theory with assumptions and validity domains.
18. **Do not confuse correlation with law.** Learned relationships must be labeled empirical/model-derived unless independently established as governing principles.
19. **Construct beyond reference examples.** Support reconstruction, generalization and bounded exploration; reference databases provide evidence and comparison, not the limit of possible outputs.
20. **State the construction basis.** Record objective, strategy, knowledge, equations, models, constraints, assumptions, parameters and stopping conditions.
21. **Separate evidence levels.** Mathematical consistency, domain validity, physical plausibility, stability, experimental realizability and demonstrated function are distinct claims.
22. **Represent uncertainty.** Include uncertainty, sensitivity, confidence calibration where available, known limitations and unresolved alternatives.
23. **Compare methods for consequential claims.** Where feasible, evaluate independent approaches and explain disagreements rather than trusting the first result.
24. **Domain services own scientific authority.** Each A–N service owns its domain semantics, equations, constraints, thresholds, construction methods and verification Rulebooks.

## IV. Models, tools and execution

25. **Models are replaceable components.** No LLM, predictor, embedding model or external checkpoint is the sole scientific authority or a mandatory dependency for deterministic scientific tasks.
26. **Version model and data provenance.** Record model/checkpoint, weights hash, dataset manifest, preprocessing, parameters, seed where applicable, runtime and evaluation report.
27. **Regression-test every model change.** Compare against a fixed, leakage-resistant benchmark and retain rollback capability.
28. **Use registered capabilities only.** Tools must have declared schemas, versions, permissions, resource limits, dependencies, network policy and error contracts.
29. **Never execute arbitrary model-generated code.** Generated code, shell, SQL or scripts are untrusted; execution requires a reviewed, isolated and policy-approved path.
30. **Enforce resource and egress budgets.** Apply CPU, memory, GPU, disk, process, wall-time, concurrency, output and network limits.
31. **Treat external content as data, never instructions.** Retrieved documents, datasets, annotations, filenames and model outputs cannot change system policy or permissions.
32. **Human authorization for consequential actions.** Clinical, wet-lab, safety-sensitive, external publication and irreversible actions require qualified human/institutional approval.

## V. Provenance, reproducibility and reporting

33. **Trace every material claim.** Link report claims to artifact IDs, field paths, source records or derivation traces.
34. **Preserve immutable lineage.** Record inputs, parents, transforms, knowledge/model/tool versions, parameters, environment and verification results.
35. **Make computation reproducible.** Record random seeds and numerical/runtime settings where possible; disclose nondeterminism and hardware sensitivity.
36. **Never fabricate evidence.** Do not invent citations, measurements, equations, units, coordinates, accession IDs, confidence values or test results.
37. **Keep failure visible.** Preserve failed, cancelled, timed-out, partial and indeterminate runs with explicit reasons.
38. **Use explicit decision states.** At minimum: accepted, rejected, indeterminate, failed, cancelled, needs_human_review and not_applicable.

## VI. Engineering governance

39. **One authoritative AI architecture.** The Agentics Master Plan is the sole AI architectural authority; ENGINE, RULEBOOK, ACCEPTANCE, Constitution and roadmaps are subordinate specifications.
40. **Inspect and reuse before adding.** Audit existing Molecularis modules, capabilities, artifacts, provenance, workflows and dependencies before creating parallel implementations.
41. **No placeholders presented as capabilities.** No fake engines, hardcoded success, silent fallbacks or decorative integrations. Mark unimplemented functionality honestly.
42. **Gate implementation with evidence.** Every component needs contracts, tests, failure behavior, security/resource controls, documentation and acceptance evidence. Engineering CI is not scientific validation.

## Enforcement

- Convert applicable rules into schemas, validators, capability policy, Rulebook checks and automated tests.
- Record the rule IDs applied to each scientific workflow and the outcome of each mandatory gate.
- Domain-specific Rulebooks may strengthen these requirements but may not weaken the Constitution.
- Exceptions require a documented rationale, scope, owner, expiry and approval; safety, privacy, license and human-authority requirements are not waivable by an AI model.
- University and qualified domain review remains separate from software engineering acceptance.
