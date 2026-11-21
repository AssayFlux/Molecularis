# Molecularis AI Rulebook

| Rule | Requirement |
|---|---|
| AI-001 | Planner output is untrusted structured data; never evaluate generated code |
| AI-002 | Only registered A–N capabilities may be selected |
| AI-003 | Workflow v1 schema, safe identifiers and bounded operation counts are mandatory |
| AI-004 | External inputs must exactly match caller-supplied artifact keys |
| AI-005 | Plans are persisted with request digest, planner identity and input lineage |
| AI-006 | Planning never executes scientific operations |
| AI-007 | Execution requires explicit approval |
| AI-008 | Execution uses the Core RulebookExecutor and its resource budgets |
| AI-009 | Failures are recorded by Core; no implicit retries |
| AI-010 | Model-generated explanations are not scientific evidence or validated conclusions |
| AI-011 | Missing provider configuration must be reported; no pretend AI fallback |
| AI-012 | Clinical and experimental decisions require independent human authority |
