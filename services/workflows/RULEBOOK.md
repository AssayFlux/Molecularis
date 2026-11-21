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
