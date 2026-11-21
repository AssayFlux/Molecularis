# Workflows Rulebook N

Status: operational v1 graph and orchestration rules; independent service-level validation remains separate.

| Rule | Requirement | Acceptance |
|---|---|---|
| WF-001 | Bounded safe workflow, operation, capability and value identifiers | Invalid identifiers rejected |
| WF-002 | Operation IDs, output keys and declared input keys are unique | Duplicate keys rejected |
| WF-003 | Every input resolves to a declared external input or operation output | Missing references rejected |
| WF-004 | Graph is acyclic with deterministic topological order | Cycles rejected; stable order |
| WF-005 | Every capability is registered in the active ServiceRegistry | Unknown capability rejected |
| WF-006 | Parameters are finite canonical JSON objects within byte limits | Malformed/non-finite/oversized rejected |
| WF-007 | Execution uses Core RulebookExecutor and shared budgets | End-to-end execution and failure evidence |
| WF-008 | Artifacts retain content integrity and lineage | SHA-256 and run input/output provenance verified |
| WF-009 | Workflow documents contain no secrets; Galaxy outputs are untrusted | Connector security tests and explicit validation boundary |

No scientific result validation, implicit retries, parallel scheduling, branching, loops, clinical decisions or guarantee of external output correctness.


## Agentics scientific workflow rules

- Apply the universal lifecycle across services while preserving domain-owned Rulebooks and scientific thresholds.
- Preflight every node: schemas, units, artifact integrity, capability version, permissions, source/evidence status and resource limits.
- Never allow a planner to invent unregistered capabilities, change a service's scientific rules or self-approve consequential execution.
- Verify node outputs independently according to the owning service's Rulebook; propagate failed/indeterminate states and invalidate dependent evidence after material changes.
- Preserve cross-service provenance, assumptions, uncertainty, evidence class, tool versions and environment.
- Use bounded retries, deterministic replay where possible, explicit cancellation and secure isolation.

Priority disciplines: Computer science, graph algorithms, formal methods, constraint solving, scheduling/operations research, provenance, reproducibility, resource optimization and secure execution.
See ../ai/AI_CONSTITUTION.md and ../ai/SCIENTIFIC_TOOL_REGISTRY.md.
