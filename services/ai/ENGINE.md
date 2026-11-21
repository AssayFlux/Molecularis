# Molecularis AI — Intelligence and orchestration layer

Status: initial model-agnostic planning and guarded execution implementation. Provider integration and full scientific cross-service acceptance remain pending.

## Mission
Turn a natural-language research request into a versioned Molecularis Workflow v1, validate it against the active A–N capability registry, persist the plan with source-artifact lineage, require explicit approval, and execute through the existing RulebookExecutor.

## Architecture
1. A model adapter receives the request, the live capability catalog and caller-supplied artifact references.
2. The model returns a structured Workflow v1 object. It does not return Python, shell commands, SQL, imports or executable code.
3. Molecularis parses strict JSON, checks identifiers, input declarations, operation limits, capability registration and DAG structure.
4. The workflow is stored as a content-addressed artifact with input parents.
5. Execution requires explicit approval and uses existing registered service handlers and Core budgets.
6. Run evidence and output artifacts are recorded by the existing runtime.

## Trust boundary
Model output is untrusted data. No model-generated code is evaluated. Unknown capabilities, malformed workflows, unregistered handlers, missing inputs and oversized plans fail closed. Planning does not execute tools. Execution is opt-in through an explicit approval argument.

## Provider adapters
Core defines a Python callable contract and deliberately does not hard-code a vendor, API key, network client or model dependency. A provider-specific adapter must be configured by the deployment. Without one, Molecularis AI does not claim to provide autonomous natural-language reasoning.

## Current limitations
- This is the first agent foundation, not a finished autonomous research scientist.
- Real service-to-service artifact schema compatibility and artifact handoff need a dedicated integration phase.
- A–N bootstrap registers existing capabilities and handlers but does not prove every optional external engine is installed.
- No web research, citation retrieval, model training, long-term memory, human identity, multi-agent delegation or distributed execution.
- No autonomous retries or irreversible actions.
- Scientific validation, clinical interpretation and experimental approval remain outside the AI's authority.
