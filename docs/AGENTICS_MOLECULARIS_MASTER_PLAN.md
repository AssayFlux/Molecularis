# Agentics Molecularis — Master Architecture, Build Plan and Acceptance Standard

**Product name:** Agentics Molecularis  
**Parent platform:** Molecularis by AssayFlux  
**Plan version:** 1.0  
**Status:** Governing implementation plan; phases are sequential and gated  
**Branch:** CORE  
**Prepared:** 2026-11-21

## 1. Identity, purpose and product boundary

**Agentics** describes the engineering of goal-directed software agents: systems that interpret objectives, plan bounded actions, use tools, coordinate specialised capabilities, inspect outcomes and revise or stop according to policy. Agentics Molecularis is the agentic intelligence and orchestration system of the Molecularis scientific platform.

Molecularis remains the scientific computing platform and owner of scientific services, algorithms, data contracts, Rulebooks, execution and artifacts. Agentics Molecularis is not a replacement for those services and is not itself a source of scientific truth.

### Mission

Translate a researcher's natural-language objective into an inspectable, policy-compliant, reproducible scientific workflow; coordinate registered Molecularis capabilities; preserve all inputs, intermediate results, failures and validation evidence; and compose a useful answer whose claims are traceable to artifacts.

### North Star

**Agents propose and coordinate. Scientific engines compute. Rulebooks constrain and verify. Artifacts preserve evidence. Humans authorize consequential actions.**

### Product boundary

- Molecularis owns domain science and execution semantics.
- Agentics Molecularis owns intent interpretation, planning, capability selection, workflow composition, bounded coordination, evidence aggregation and answer composition.
- External LLMs are replaceable reasoning providers, never scientific authorities.
- External databases and models are accessed through explicit, versioned, licensed source/model adapters.
- The system must work without a hosted LLM for deterministic, pre-authored workflows and local operations where supported.
- No clinical diagnosis, treatment recommendation, experimental authorization or autonomous wet-lab action is implied.

## 2. Existing foundation — reuse before extending

The repository already contains a meaningful first implementation. Do not duplicate it:

1. `python/molecularis/ai.py` provides a model-agnostic callable planner contract, live capability catalog, strict Workflow v1 parsing, bounded operations, persisted plan artifacts, input lineage and explicit approval before execution.
2. `python/molecularis/workflows_service.py` defines WorkflowDocument, DAG validation, capability resolution, workflow ingestion and execution through the Core Rulebook runtime.
3. `python/molecularis/bootstrap.py` registers A–N service handlers and capabilities on a fresh platform.
4. Core/MSDE provides content-addressed artifacts, metadata catalog, lineage, budgets, capability registry and Rulebook execution evidence.
5. Services A–N are present as engineering implementations; real cross-service scientific artifact compatibility and scientific acceptance still require evidence.
6. `services/ai/ENGINE.md`, `RULEBOOK.md` and `ACCEPTANCE.md` are the initial AI specification and must evolve with this plan.

Current implementation limits: no configured production LLM provider is bundled; no complete source-ingestion service; no Predictor service; no evidence-grounded answer composer; no 50-query adversarial evaluation suite; no demonstrated full real-science cross-service chain; and no certified OS-level sandbox or recovery envelope. Do not describe the existing callable planner as a finished autonomous agent.

## 3. System architecture

### 3.1 Logical components

| Component | Responsibility | Authority boundary |
|---|---|---|
| Request Gateway | Accept text, files, structured inputs, user constraints and authorization context | Validates size/type; does not infer scientific truth |
| Intent Interpreter | Extract objective, entities, task type, constraints, requested outputs and uncertainty | Produces hypotheses and candidate interpretations |
| Entity Resolver | Resolve names/identifiers to ranked source records and accession candidates | Must preserve ambiguity; never silently select an uncertain identity |
| Source Manager | Retrieve, cache, checksum, license-check and version external data | Every retrieval becomes a provenance-bearing artifact |
| Capability Discovery | Read active registry and schemas; expose permitted operations | Only registered, enabled capabilities are callable |
| Planner | Compose typed Workflow v1 DAG and explain dependencies | Proposes; cannot execute or bypass policy |
| Plan Validator | Validate schemas, types, authorization, provenance, DAG, budgets and policy | Fail closed on unsupported or unsafe plans |
| Approval Manager | Present plan, data egress, cost/resource estimate and consequences | Explicit human approval for execution and consequential actions |
| Orchestrator | Schedule and invoke approved operations; track cancellation and failures | Calls only declared handlers through bounded runtime |
| Scientific Proposers | Invoke deterministic engines or configured model adapters | Outputs remain candidates/predictions until verified |
| Verifier | Run service Rulebooks, independent checks and acceptance criteria | Cannot be bypassed by model confidence or LLM narrative |
| Artifact & Evidence Ledger | Store immutable inputs, outputs, runs, source records and validation evidence | Canonical artifact data is authoritative |
| Answer Composer | Produce claims, values, tables and explanations from verified artifacts | Unsupported claims must be omitted or explicitly marked unknown |
| Audit & Evaluation | Record decisions, traces, provider metadata, policy outcomes and eval results | Sensitive data and secrets must be redacted |

### 3.2 Request-to-answer lifecycle

1. **Receive:** validate request, files, size, format, identity/authorization and declared privacy constraints.
2. **Interpret:** extract task, entities, desired outputs, scope, assumptions and missing information.
3. **Resolve:** query local indexes and approved Sources connectors; return ranked candidates with evidence and ambiguity.
4. **Clarify:** ask the user when unresolved ambiguity changes scientific meaning, authorization, data identity or execution risk.
5. **Discover:** inspect active capabilities, versions, input/output schemas, dependencies, resource needs and license/privacy constraints.
6. **Plan:** generate a Workflow v1 DAG with explicit inputs, outputs, parameters, provenance, method choices, verification operations and resource budgets.
7. **Validate:** validate every edge and schema, verify artifact existence/integrity, check policy and source/model licenses, check budgets and capability availability.
8. **Explain & approve:** show the proposed workflow, alternatives, assumptions, external data transfers, expected resources and irreversible effects; obtain explicit approval.
9. **Execute:** run approved operations using the bounded Rulebook runtime; preserve run states, intermediate artifacts, stdout/stderr summaries and failures according to policy.
10. **Verify:** apply service-specific acceptance rules and, where required, independent methods/reference comparisons.
11. **Compose:** answer only from artifact-backed facts; cite artifact IDs, source records, methods, versions, units, confidence and validation status.
12. **Audit:** persist workflow, plan, approval, execution, failure, verification and report records for replay and review.

### 3.3 Agent roles and autonomy

Start with a single orchestrator and explicit typed stages. Do not introduce multi-agent complexity before the single-agent workflow is safe and measurable.

Later, specialist agents may be isolated behind the same capability and artifact contracts:
- **Research agent:** decomposes objective and identifies evidence needs.
- **Source agent:** searches approved databases and returns source artifacts.
- **Planning agent:** proposes typed workflow DAGs.
- **Execution coordinator:** dispatches approved capabilities.
- **Verification agent:** selects and interprets declared verification procedures; the actual validators remain deterministic/domain-owned.
- **Reporting agent:** composes artifact-grounded results.

Agents communicate through typed messages and artifact references, not shared mutable memory. Every delegation has a bounded task, allowed tools, resource budget, timeout, provenance and termination condition. An agent cannot grant itself permissions or approve its own high-impact action.

Autonomy levels:
- **L0 — Explain:** answer questions about available capabilities and plans without execution.
- **L1 — Draft:** propose a plan; no scientific operation runs.
- **L2 — Approved execution:** execute a user-approved bounded workflow.
- **L3 — Bounded iteration:** execute pre-authorized, finite retry/optimization loops with declared stop criteria and budgets.
- **L4 — Autonomous consequential action:** out of scope until separate governance, safety, scientific and institutional approval. Never enable by default.

## 4. Core contracts and artifact model

### 4.1 Workflow contract

Reuse Workflow v1 and evolve through explicit versioning rather than creating a parallel planner format. Each operation must declare:
- Stable operation and capability IDs plus versions.
- Typed input artifact keys and output key.
- Parameters validated against the capability JSON Schema.
- Dependencies and deterministic ordering.
- Method/model identity and configuration where applicable.
- Resource budget and timeout.
- Required permissions and network/data-egress policy.
- Expected output schema/media type.
- Verification Rulebook IDs and acceptance criteria.
- Failure, cancellation, partial-output and retry semantics.

Schema evolution must be backward-compatible where possible. Breaking changes require a new version and migration notes. The planner cannot invent capability IDs, alter schemas or bypass registry state.

### 4.2 Required artifact classes

| Artifact class | Minimum recorded information |
|---|---|
| User input | content hash, media type, size, user-supplied status, consent/authorization metadata where applicable |
| External source record | canonical URL, accession, provider, release/version, retrieval timestamp, checksum, license/terms, attribution and transformations |
| Model prediction | predicted namespace ID, model/checkpoint/version, weights hash, input hash, seed, parameters, software/runtime, confidence outputs and verification status |
| Experimental observation | separate experimental namespace, source accession, method, publication/deposition metadata, experimental conditions and source validation |
| Workflow plan | request digest, planner/provider identity, capability versions, DAG, input parents, validation report and approval reference |
| Execution run | run ID, plan hash, start/end, environment, resource use, operation states, logs/evidence and failures |
| Verification result | rule ID/version, validator identity/version, inputs, thresholds, metrics, pass/fail/indeterminate state and evidence artifacts |
| Scientific report | claim IDs, exact supporting artifact IDs/fields, units, methods, caveats and unsupported questions |

Artifact IDs are immutable and content-addressed. Human-readable identifiers are aliases mapped to immutable hashes; aliases never replace hashes. Predicted and experimental namespaces must remain distinct and machine-enforced.

### 4.3 Evidence-grounded answer contract

Every factual claim in a final scientific answer must map to one or more artifact fields. A report claim should carry:
- Claim ID and text.
- Artifact ID(s) and field/path(s).
- Source/method/model and version.
- Units and transformation history.
- Verification state and applicable rule IDs.
- Confidence or uncertainty with its definition.
- Limitations and applicability domain.

If a value is absent, invalid, ambiguous or not supported, state **“I cannot determine that from the available artifacts.”** The LLM may explain supported results but must not supply missing measurements, coordinates, accessions, confidence scores or citations from memory. Never treat generated prose as an artifact.

## 5. Security, privacy, safety and licensing

### 5.1 Execution security
- Use an OS-level sandbox/container for untrusted tools and model inference where feasible.
- Enforce CPU, memory, GPU, disk, process count, file size, wall-time, concurrency and output-size limits.
- Network is disabled by default; each capability declares exact allowed destinations/protocols and data egress.
- Use read-only inputs and isolated writable output directories; prevent path traversal and symlink escape.
- Never pass secrets in prompts, logs, command-line arguments or artifacts.
- Use deployment secret managers/environment injection; never commit credentials.
- Record sandbox profile, image digest, runtime and policy decision.
- Terminate process trees on timeout/cancellation and preserve failure evidence.

### 5.2 Untrusted data and prompt injection
- Retrieved web pages, database annotations, PDFs, sequence headers, structure metadata, filenames and model outputs are data, never instructions.
- Separate instructions from source payloads; quote/label source text and restrict its influence to the relevant data fields.
- Tool selection and permissions are decided by deterministic policy, not source text or LLM requests.
- Validate all structured outputs against strict schemas; reject unknown fields where contracts require.
- Add indirect prompt-injection fixtures across every connector and file type.
- Never let an external record change system rules, request secrets or authorize new tools.

### 5.3 Privacy
- Do not commit patient-identifiable, personal, controlled or private research data.
- Define local-only versus remote-processing modes.
- Warn and obtain consent before sending sequences, structures, compounds, cohort data or other user material to remote providers.
- Minimize payloads and redact logs.
- Define retention, deletion, access control and audit policies before multi-user deployment.
- No patient-level clinical interpretation in this release plan.

### 5.4 Licensing and data governance
- Maintain a source/model/dependency license ledger.
- Record license text/reference, version, retrieval date, permitted use, attribution, share-alike and non-commercial restrictions.
- Block use where deployment purpose conflicts with license terms.
- Do not infer blanket licensing from a database name; verify specific data releases, model weights, code and derived datasets separately.
- Distinguish experimental observations from predictions and synthetic labels.
- Preserve required attribution and share-alike obligations in downstream artifacts and reports.

### 5.5 Biosecurity
- Any sequence, structure, molecule or protocol design capability must undergo a separate risk assessment before enablement.
- Screen against appropriately governed toxin/pathogen-virulence references and applicable institutional policies.
- Record screen version, input/output hashes, result, rationale and human-review record.
- Refuse harmful design intent; do not provide operational assistance for harmful biological activity.
- Screening does not replace human institutional oversight. Design remains disabled until P5 gate approval.

## 6. Model and provider strategy

### 6.1 LLM provider adapter
Define a provider-neutral adapter outside Core. It must support structured outputs/tool calls, bounded context, timeout, cancellation, retries only where safe, usage/cost accounting, model identity/version, request/response hashes and redacted telemetry. Credentials are deployment-managed. Provider responses are untrusted.

Required adapter behaviours:
- Capability schema supplied as constrained tool definitions.
- Strict JSON/Workflow v1 output; no executable code.
- Explicit refusal/unsupported state.
- Deterministic mock provider for CI.
- Optional hosted provider first; local model adapter later.
- No provider is considered configured until a real integration test in a controlled environment passes.

### 6.2 Model governance
Record model provider, model name/version, endpoint class, weights/checkpoint hash if local, prompt/template version, decoding parameters, seed if supported, tool schema version and evaluation results. Pin or explicitly record provider model revisions. Model changes trigger regression evaluation.

### 6.3 Scientific model adapters
Scientific predictors are separate from LLMs. Predictor adapters return canonical artifacts and full model provenance. License review applies to code, weights and training data independently. Never use a model's confidence as proof of correctness.

## 7. Sources service requirements (P1)

Create a Sources service following existing service ownership/layout conventions after auditing current source-related code and adapters. Initial connectors:
- RCSB PDB: Data API and structure file retrieval.
- UniProt REST: accession, sequence and annotation retrieval.
- AlphaFold DB: predicted structure retrieval, explicitly labelled predicted.
- InterPro: domain/family annotation.
- PubChem: compound identifiers and records.
- NCBI Entrez: approved databases, with API key/rate policy where applicable.

Connector contract:
- Provider identity, endpoint allowlist, request/response schema and version.
- Rate limiting, exponential backoff with jitter, bounded retries and respectful provider policy.
- ETag/Last-Modified caching where supported; cache key includes accession and release.
- Response-size/time limits and content-type validation.
- SHA-256 checksum and canonical artifact publication.
- Retrieval time, source release, accession, URL, license/terms and attribution.
- Offline fixture mode; CI must not depend on live network.
- Explicit stale-cache and partial-response semantics.

Entity resolution:
- Normalize names and identifiers without discarding original query.
- Return ranked candidates, evidence, source and accession.
- Expose ambiguity and conflicting records.
- Never silently resolve ambiguous biological entities.
- Ask the user when candidate choice changes the scientific result.

P1 acceptance: recorded fixtures resolve “human hemoglobin” into distinct alpha- and beta-chain candidates with explicit accessions and evidence; retrieve one selected PDB entry as a content-addressed artifact; repeated fixture retrieval yields stable bytes/checksum; license/provenance metadata is complete; offline tests pass.

## 8. Predictor service requirements (P3)

Create a distinct Predictor service; do not bury structure prediction inside the LLM layer or silently label predictions as experimental.

Initial interface:
- Inputs: validated protein sequence artifact, optional ligand/chain context, model selection, parameters, resource budget and optional MSA artifact.
- Outputs: mmCIF structure artifact plus confidence/metadata JSON, logs, model provenance and verification report.
- Model adapters are optional and independently licensed; candidate options include Boltz-family, OpenFold-family, Protenix, Chai and existing ESM/ESMFold paths only after exact checkpoint/license review.
- MSA: local MMseqs2 preferred; remote service is opt-in and requires explicit sequence-egress warning/consent.
- Resource estimation and GPU/CPU capability discovery before approval.
- Human-readable prediction alias such as MOL-P-000001 mapped to immutable SHA-256 identity; experimental IDs use a separate namespace.

Required prediction provenance: model name, version, code revision, checkpoint/weights hash, input sequence hash, MSA hash/source, parameters, random seed where supported, runtime/container digest, hardware, start/end, confidence outputs (for example pLDDT/PAE when produced), warnings and verification outcomes.

Verification Rulebook must include schema/geometry validation, chain/residue consistency, clashes, Ramachandran and stereochemistry checks where applicable, confidence thresholds justified by benchmark evidence, and optional independent predictor consensus (TM-score) or physics refinement. OpenMM relaxation is optional and must not be represented as independent experimental confirmation.

P3 acceptance: benchmark on structures released after each predictor's documented training cutoff, with leakage-aware dataset split and reported lDDT, TM-score, RMSD where appropriate, confidence calibration and failure cases. Record dataset provenance/license and do not claim universal accuracy.

## 9. Data and training pipeline (P4)

No fine-tuning or training from scratch before the pretrained baseline, evaluation harness and leakage-resistant dataset pipeline exist.

Pipeline:
1. Select and document permitted datasets and releases.
2. Download versioned snapshots with checksum and license manifest.
3. Store raw source snapshots as immutable artifacts.
4. Apply deterministic quality filters with rationale and threshold version.
5. Normalize structures/sequences while preserving raw parent artifacts.
6. Cluster sequence identity with pinned MMseqs2 settings.
7. Create time-based splits and cluster-based splits; document intersection/holdout rules.
8. Generate features with versioned featurizers and content hashes.
9. Train with pinned code/dependencies, configuration, seed and hardware metadata.
10. Evaluate on held-out data with calibration and subgroup/failure analysis.
11. Register model artifact with training manifest, data hashes, code commit, metrics, license and limitations.
12. Reproduce a run from its manifest within documented tolerances.

Experimental and synthetic labels must be separate. AlphaFold DB predictions are synthetic/predicted labels, not experimental ground truth. Never train on model-generated outputs as though measured; guard against recursive self-training and leakage.

Potential tools include PyTorch, Hugging Face datasets/hub, MLflow or W&B, DVC and MMseqs2, subject to license, privacy and reproducibility review. Tracking systems must not receive private data without explicit authorization.

P4 acceptance: an end-to-end training/evaluation run is reproducible from a committed manifest with metrics inside predeclared tolerances; test split is demonstrably separated by release date and sequence clusters; license ledger is complete.

## 10. Proposer → Verifier pattern across services (P5/P6)

A reusable domain pattern:
1. **Proposer:** model, heuristic or deterministic candidate generator proposes an output.
2. **Canonicalizer:** convert output into a typed Molecularis artifact; preserve raw candidate and transformation.
3. **Verifier:** deterministic/domain-owned Rulebook checks schema, scientific constraints, provenance, resource bounds and acceptance criteria.
4. **Independent check:** where required, use a genuinely independent method/reference; do not treat repeated calls to the proposer as independent.
5. **Decision:** accept, reject, indeterminate or request human review; never collapse these states into a generic success.
6. **Evidence:** persist every candidate, verifier result, threshold, failure and approval.
7. **Report:** expose candidate status and evidence; no unverified proposal is called a validated result.

Generalization examples:
- Chemistry: RDKit validity, valence, stereochemistry, property bounds and domain-specific safety rules.
- Kinetics: residual analysis, parameter identifiability, sensitivity, fit diagnostics and uncertainty.
- Genomics: reference build, coordinate normalization, annotation release, evidence level and variant QC.
- Omics: design validity, normalization assumptions, statistical model, multiple-testing correction and reproducibility.
- DNA/RNA: sequence constraints, thermodynamic assumptions and independent structure/oligo checks.
- Simulation: topology/parameter validity, energy/temperature/pressure diagnostics, convergence and stability.
- Pharmacogenomics/cohorts: source release, privacy, phenotype evidence and non-clinical boundaries.

P5 design is optional and disabled by default. It requires biosecurity screening, explicit human review and institutional approval. P6 expands proposer/verifier only service by service with domain-specific acceptance criteria.

## 11. Evaluation programme

### 11.1 Agentics evaluation set
Create at least 50 version-controlled, privacy-safe queries with expected intent, candidate entities, allowed capabilities, expected workflow shape, expected artifact classes, unsupported claims and pass/fail criteria. Cover:
- Direct factual retrieval and accession resolution.
- Ambiguous names and competing accessions.
- Sequence/structure workflows.
- Multi-service composition.
- Missing input and malformed artifact.
- Unsupported request and insufficient evidence.
- Requests to fabricate a number, coordinate, accession or citation.
- Prompt injection in fetched text, file metadata, FASTA headers and source annotations.
- Unauthorized tool/network access and secret exfiltration attempts.
- License conflict, remote sequence-egress consent and privacy restrictions.
- Resource exhaustion, timeout, cancellation, partial output and failed dependencies.
- Predicted-versus-experimental confusion.
- Model/provider outage and malformed structured output.

Measure task success, entity-resolution accuracy, schema-valid plan rate, unauthorized-call rate, artifact-grounding precision/recall, unsupported-claim rate, refusal correctness, reproducibility, latency and cost. Report per-category metrics and failures. A zero-fabrication target is mandatory on the curated eval set; it is not proof of zero risk in all deployments.

### 11.2 Scientific evaluation
Use domain-specific metrics and independent references, with predeclared thresholds. For structure prediction, report lDDT/TM-score/RMSD and confidence calibration with leakage-resistant splits. Report negative results and applicability limits.

### 11.3 Engineering evaluation
CI uses deterministic local fixtures and mock providers; no live API calls or credentials. Add property/fuzz tests for parsers, schemas and source content. Add security tests for sandbox escape, path traversal, prompt injection and network policy. Add crash/fault injection and backup/restore tests.

## 12. Phased delivery plan and gates

Phases are sequential. Complete the phase report and stop at its gate. Do not begin the next phase in the same implementation step unless the owner explicitly authorizes it. A phase gate requires implementation, tests, green CI, documentation and evidence; a written specification alone is not completion.

### P0 — Hygiene, trust baseline and platform safety
**Scope**
- Re-audit actual current branch state and reconcile README, SERVICE_STATUS, master plan, backlog and CI evidence.
- Correct stale status claims; every status transition links to commit/run/benchmark/validation artifact.
- Inventory current source adapters, model integrations, data and licenses before adding duplicate connectors.
- Add OS-level sandbox execution option with declared CPU/memory/time/disk/process/network limits; retain trusted in-process path only for explicitly trusted handlers.
- Record failed/intermediate execution evidence and cancellation/timeout outcomes.
- Implement artifact-store catalog backup/restore and corruption/crash-boundary tests.
- Define threat model, secret-handling and data-egress policy.
- Expand Ruff and typing checks incrementally without unrelated churn.

**Tests/evidence**
- Sandbox boundary, timeout, cancellation, process-tree termination and network-deny tests.
- Artifact-store backup/restore round trip, interrupted backup, corrupted blob/catalog and integrity audit.
- Failure-run evidence assertions.
- Docs/status consistency check and full CI.

**Gate P0:** CI green; sandbox boundary tests pass; backup/restore and failure-evidence tests pass; status documents agree with observed evidence. No scientific acceptance implied.

### P1 — Sources service
**Scope:** build connector framework, initial six connectors, offline cache, resolver, license ledger and source artifacts as specified in section 7.

**Gate P1:** human hemoglobin fixture returns distinct alpha/beta candidates with explicit ambiguity; a selected PDB fixture becomes an immutable artifact; checksum stable; metadata/license complete; offline CI green. No live network required in CI.

### P2 — Agentics orchestrator
**Scope**
- Add provider-neutral LLM adapter outside Core, deployment-managed secrets and deterministic mock.
- Convert active capability JSON Schemas to constrained provider tool definitions.
- Add structured intent/entity/plan objects while preserving Workflow v1 as execution contract.
- Implement clarification/ambiguity path, plan explanation and approval UX/API.
- Add artifact-only Answer Composer with claim-to-artifact citations.
- Add run/session state, cancellation, bounded iteration policy and redacted audit trace.
- Implement >=50-query adversarial evaluation suite and metrics.

**Gate P2:** all 50+ evals run in CI using mock/recorded fixtures; zero unsupported/fabricated claims in suite; prompt-injection cases cannot alter tools/policy; provider adapter integration passes controlled test; approval gate remains enforced; every reported scientific claim maps to artifact evidence.

### P3 — Predictor service
**Scope:** implement PredictorAdapter, exact model/license review, local MSA path, model provenance, predicted namespace, mmCIF/confidence artifacts and verification Rulebooks as specified in section 8.

**Gate P3:** benchmark on structures released after each predictor's documented training cutoff, with leakage-aware dataset split and reported lDDT, TM-score, RMSD where appropriate, confidence calibration and failure cases. Record dataset provenance/license and do not claim universal accuracy.

### P4 — Data and training pipeline
**Scope:** versioned data snapshots, license ledger, quality filters, clustering, temporal/cluster splits, reproducible training harness, model registry and experiment manifests.

**Gate P4:** a run reproduces from its manifest with metrics inside predeclared tolerances; test split is demonstrably separated by release date and sequence clusters; license ledger is complete.

### P5 — Optional design service (separately authorized)
**Scope:** design adapters, canonical candidate artifacts, proposer-verifier loop, biosecurity screening and human-review workflow. Disabled by default until approval.

**Gate P5:** screening test suite passes, human review and institutional approval are recorded, model/data license checks pass, and no unsafe design is released.

### P6 — Generalize across A–N
**Scope:** add domain-specific proposer/verifier packages and integration tests one service/domain at a time. Do not change all services in a single broad rewrite.

**Gate P6:** each domain has a versioned Rulebook, acceptance metrics, evidence schema, independent check where needed, regression suite and documented limitations. System-level cross-service workflows preserve provenance end to end.

## 13. Phase execution protocol and reporting

For each phase:
1. Inspect actual repository implementation and history.
2. Write a short gap analysis and exact file-level plan.
3. Define schemas and acceptance criteria before code.
4. Implement only the active phase.
5. Add unit, property, integration, adversarial and regression tests appropriate to scope.
6. Run local checks and CI; record exact commit and run URL.
7. Update engine, runtime, Rulebook, acceptance, status, backlog and README only where evidence warrants.
8. Report and stop at the gate.

Required phase report:
1. Files changed.
2. Tests added and executed.
3. CI evidence with run URL and commit.
4. What passed, failed, skipped and was not tested.
5. Open risks and explicit non-claims.
6. Exact gate decision: passed, failed or blocked.
7. Exact next phase, not started until gate passes.

## 14. Non-goals and prohibited shortcuts

- Do not train a protein structure model from scratch before pretrained baseline and evaluation.
- Do not add a second workflow format alongside Workflow v1 without a decision.
- Do not let an LLM call arbitrary shell, Python, SQL or network tools.
- Do not infer a scientific result from plausible language or model confidence.
- Do not silently choose among ambiguous biological entities.
- Do not merge predicted and experimental namespaces or labels.
- Do not use live external APIs in deterministic CI.
- Do not ingest data/models without license and provenance review.
- Do not enable remote MSA/provider egress without user-visible consent.
- Do not enable design capabilities before P5 approval.
- Do not claim a green CI run is scientific validation.
- Do not rewrite existing services or remove assets as a side effect of AI work.

## 15. Definition of complete

Agentics Molecularis is ready for a research-grade controlled pilot only when P0–P4 gates pass, representative A–N workflows execute with real typed artifact handoffs, evidence-grounded reports pass adversarial evaluation, sandbox/recovery/security controls are demonstrated, and university scientific/privacy review accepts the relevant domains. P5 remains separately optional. Production or clinical readiness requires additional deployment, institutional, regulatory and domain-specific acceptance; it is not implied by this plan.

## 16. References inside this repository

- [Molecularis North Star](NORTH_STAR.md)
- [Master Development Plan](MASTER_DEVELOPMENT_PLAN.md)
- [Service Status](SERVICE_STATUS.md)
- [Work Backlog](WORK_BACKLOG.md)
- [Scientific Validation Standard](SCIENTIFIC_VALIDATION_STANDARD.md)
- [Decision Log](DECISION_LOG.md)
- [Agentics Engine](../services/ai/ENGINE.md)
- [Agentics Rulebook](../services/ai/RULEBOOK.md)
- [Agentics Acceptance](../services/ai/ACCEPTANCE.md)
