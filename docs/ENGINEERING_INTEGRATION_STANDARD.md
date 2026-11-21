> **Alpha transition notice (2026-11-21):** Apply this standard together with [docs/alpha/LANGUAGE_STRATEGY.md](alpha/LANGUAGE_STRATEGY.md) and [docs/alpha/MASTERPLAN.md](alpha/MASTERPLAN.md). Android-specific assumptions are migration context, not the target product architecture. Preserve its useful contract, testing, provenance and review requirements; reconcile any conflicts with the all-device North Star before implementation.

---



# Molecularis — Engineering & Integration Standard

**Status:** Owner-directed engineering standard  
**Adopted:** 2026-11-09  
**Applies to:** All tracks (R, S, I, P, G), every language boundary, app, engine, service and build pipeline  
**Normative rule:** This document supplements `NORTH_STAR.md`, `ROADMAP.md`, `DECISIONS.md` and D-016. It does not waive scientific, security, privacy, licensing, clinical or device-validation gates.

## 1. Project profile

### Goal
Build Molecularis as an offline-first scientific workbench for reproducible bioinformatics, structural biology, chemistry, enzyme kinetics and omics research, with auditable provenance and an optional authenticated, encrypted remote compute node. Precision-medicine work remains research-only and separately gated; clinical decision support is disabled.

### Team and experience
- Team size: **TBD — owner has not supplied a team roster**.
- Experience distribution: **TBD — do not assume staffing or expertise**.
- Until clarified, reviews and handoffs must be explicit and evidence-based; do not invent named owners.

### Platforms and versions
- Android: existing application target is Android 10 / API 29 minimum, arm64-v8a. This is a target, not a verified device-support matrix.
- iPhone/iOS: Swift application is an owner-directed target; minimum iOS version, supported devices and release scope are **TBD**. No Swift application currently exists in the repository.
- 3D visualisation: offline web visualisation using HTML/CSS/TypeScript and Three.js is the target; browser/WebView versions and supported graphics devices are **TBD**. No TypeScript/Three.js application currently exists.
- Remote compute: optional, authenticated and encrypted, user-configured only. Transport and deployment topology must be approved in a phase plan before implementation.
- Build tools: pin exact versions in the repository; record versions and hashes with every accepted build.

### Current state (repository inspection, 2026-11-09)
This is an **existing multi-language project**, not a greenfield scaffold:
- Kotlin/Jetpack Compose Android application and Gradle build exist.
- Python scientific package exists under `python/molecularis`; Android embeds Python 3.11 with pinned Biopython and NumPy. SciPy/pandas availability is target-specific and must be verified before use; do not assume they are packaged in Android.
- C++17 JNI source and CMake build exist, but the current native implementation is a smoke-test wrapper, not yet a substantive scientific core engine.
- Rust static library and JNI linkage exist, but current Rust source is a tiny numeric smoke-test function, not yet the security subsystem.
- SQLite persistence and JSON Schema contracts exist.
- No Swift, TypeScript, Three.js, pybind11 or Protobuf implementation was found in the inspected tree.
- Existing interfaces are a mixture of Chaquopy in-process calls, JNI/C ABI and JSON records. They are not yet governed by one end-to-end cross-language contract.

## 2. Language ownership

| Component | Sole responsibility | Must not own |
|---|---|---|
| Python | Scientific analysis and orchestration; NumPy, SciPy and pandas where supported and justified | UI, secret storage, cryptographic protocol implementation |
| C++17 | Performance-critical computational core and stable native engine API | UI, account/auth policy, custom cryptography |
| Rust | Security boundary: cryptography integration, authentication primitives, sandboxing and parsers for untrusted input | Scientific product logic or UI |
| Kotlin | Android app, platform lifecycle, presentation, permissions, persistence orchestration and WorkManager | Scientific algorithms or native engine internals |
| Swift | iPhone app and Apple platform integration | Scientific algorithms or native engine internals |
| HTML/CSS/TypeScript + Three.js | Offline 3D visualisation and interaction | Scientific source-of-truth calculations, secrets or engine internals |
| Bash | Build, test, packaging and deployment automation only | Application logic or scientific analysis |

Use audited cryptographic libraries and OS-backed secure storage. Do not invent cryptography. Rust security code must document threat model, attacker capability, trust boundary, mitigations, residual risks and tests. The C++ engine must remain independent of UI code. Apps must call stable public interfaces, never reach into engine internals.

**Migration note:** Existing code does not yet fully match this ownership table. In particular, current Rust/C++ code is a feasibility probe and not a production security/core-engine split. Do not silently re-label it as complete. Move or replace it only through a reviewed vertical slice with dependency analysis and tests.

## 3. Integration-first workflow (mandatory)

Before changing code, the implementation plan and session record must state:

1. **Components involved:** languages, modules, apps, services, data stores and build targets.
2. **Direction of calls:** caller, callee, dependency direction and ownership of each operation.
3. **Transport:** in-process API, Chaquopy, JNI/C ABI, pybind11, files, REST, gRPC or WebSocket. Select only what is justified; do not add a transport by habit.
4. **Contract:** schema/version, field names, types, units, nullability, limits, error codes and compatibility policy.
5. **Boundary risks:** integer widths, floating-point representation, endianness, UTF-8, pointer lifetime, memory ownership, thread safety, async/cancellation, time zones, units and resource limits.
6. **Matching implementation:** when one side changes, update the other side, fixtures, validators and tests in the same increment. If the other side cannot be changed in that increment, name its exact required change and mark the interface incomplete.
7. **Check:** tests and cross-component failure modes, including what could break.

For substantial work, publish a short ordered plan first. Build in dependency order: schema/contract → engine/domain implementation → language binding → app/service integration → tests and evidence. Do not start dependent work before its contract is agreed.

### Interface-change control
- Never change a public interface silently.
- A contract change requires a versioning decision, compatibility/migration plan and a list of every affected caller, callee, schema, fixture, persisted record, app and remote client.
- Prefer additive compatible changes within a version. Breaking changes require a new major schema/interface version and a migration window or explicit rejection policy.
- Record the decision in `DECISIONS.md` where architecture, compatibility, security or platform scope changes.

## 4. Shared interface contract — JSON Schema is authoritative

For cross-component scientific requests/results/errors, use the shared **JSON Schema** at `api/engine-envelope-v1.schema.json`. It is the semantic source of truth; do not separately hand-maintain Kotlin, Python, Rust, C++ or Swift field definitions without contract tests.

### Envelope rules
- Encoding: UTF-8 JSON; reject malformed UTF-8 and malformed JSON at the receiving boundary.
- Version: `schema = "kinetics.engine-envelope.v1"`, `schema_version = 1`.
- Correlation: `request_id` is a UUID string; preserve it across the full call chain.
- Time: `created_at_utc` is RFC 3339 date-time with UTC offset `Z`; never use an implicit local timezone.
- Provenance: `source_sha256` is lowercase hexadecimal SHA-256 or explicit `null`; do not treat it as authentication.
- Engine identity: stable `engine.id` and explicit `engine.version`.
- Units: `units` is explicit. Every physical quantity must declare a unit; no implicit Å/nm, seconds/minutes, molar scales or coordinate conventions.
- Payload: `input` for requests, `output` for results. Payload-specific schemas must be referenced by the operation contract and validated separately.
- Errors: use the schema's stable `error.code`, boolean `retryable` and safe user-facing `message`. Never return secrets, stack traces, filesystem paths or sensitive input in a public error.
- Limits: each operation schema must declare maximum bytes, records, dimensions, execution time and memory where relevant. Reject over-limit inputs before expensive parsing/decryption/allocation.

### Boundary ABI rules
- Native interfaces use fixed-width integer types (`int32_t`, `uint32_t`, `uint64_t`) and explicit buffer lengths; never expose platform-sized `long` as a wire type.
- Strings crossing native boundaries are UTF-8 byte buffers plus lengths, not assumed NUL-terminated strings.
- Binary numeric formats must explicitly declare IEEE-754 width, byte order and unit. JSON numbers are semantic values, not a binary wire layout.
- Caller owns input buffers for the duration of the call. Callee must not retain caller pointers after return unless the contract explicitly transfers ownership.
- Returned memory must have one documented allocator and matching free function on the same side of the ABI. No cross-runtime freeing.
- No exception, Rust panic or C++ exception may cross a C ABI/JNI boundary. Convert failures to stable error codes/envelopes.
- JNI calls must respect Android thread rules. Long-running work belongs on a worker/executor and must expose cancellation/progress semantics in its operation contract.
- Swift/native interfaces must use an explicitly versioned C-compatible ABI or a documented generated binding. Do not expose C++ classes/templates directly to Swift.
- Remote requests use authenticated TLS and the same versioned envelope. REST/gRPC/WebSocket choice is a separate decision; local calls must not be forced through a network transport.

### Preferred integration topology
- Android Kotlin ↔ Python: current Chaquopy in-process adapter; JSON envelope at the scientific operation boundary.
- Android Kotlin ↔ C++: JNI adapter over a narrow C ABI; never call C++ internals from UI.
- C++ ↔ Rust: narrow C ABI only for security services that Rust owns; no scientific dependency on Rust.
- Python ↔ C++: pybind11 may be used for host-side/native acceleration only after measured need and build/licence review. Android/iOS bindings require platform-specific adapter plans; pybind11 is not assumed portable to mobile.
- Swift ↔ native core/security: stable C ABI or reviewed generated binding, after iOS target and ABI are approved.
- TypeScript/Three.js ↔ app: versioned, validated visualisation payload through offline WebView/WKWebView message bridge. Viewer is presentation-only.
- App ↔ remote node: authenticated encrypted network API only when user-configured and enabled; no telemetry by default.

These are target contracts/topology, not claims that every edge is implemented today. Current implementation status must be reported honestly in the roadmap and registry.

## 5. Validation, security and code quality

- Validate untrusted input at every boundary: file import, schema decode, FFI, JNI, WebView bridge, persistence, remote API and export.
- Validate both syntax and semantics: ranges, dimensions, units, checksums, allowed operations, resource caps and authorization.
- Never hardcode secrets. Use Android Keystore, Apple Keychain/Secure Enclave as appropriate, or managed secret storage; never commit credentials.
- Prefer audited libraries for cryptography, TLS, parsing and serialization. Review licences, maintenance, ABI, platform support and supply-chain provenance before adding dependencies.
- Do not allow UI code to bypass service interfaces or directly mutate engine internals.
- Every non-trivial behavior needs tests: unit, contract/schema, negative/malformed input, boundary/limit, integration and migration tests as appropriate.
- Test cross-language round trips and failure paths, not just each language in isolation.
- Record deterministic fixtures, reference versions, tolerances, random seeds and numeric precision for scientific algorithms.
- Bash scripts must be safe under failure (`set -euo pipefail` where appropriate), quote paths, avoid leaking secrets and return meaningful exit codes.
- Do not mix languages in one source file. Each code change must identify its language, path, build configuration and tests in the change record.
- Do not invent APIs, dependencies, flags or capabilities. Verify upstream documentation or mark uncertainty.

## 6. Required change record

Every substantial increment must include a short record in the session log or phase plan:

- Goal and roadmap item.
- Components and call direction.
- Interface/schema version and contract changes.
- Files changed by language.
- Validation, threat and resource limits.
- Tests run, exact commands, outcomes and CI commit.
- Cross-component checks and known failure modes.
- Build artifact identity/hashes where applicable.
- Implemented vs automated-test-passed vs reference-validated vs emulator/device-verified.
- Open questions, blockers and next step.

## 7. Check section (mandatory in every engineering response)

Every engineering response must end with a **Check** section listing:
- What to test now, including affected languages and integration edges.
- What could break across components (schema drift, ABI mismatch, encoding, memory, threading, async, units/time zones, lifecycle, persistence, security).
- Tests not run and why; never call BLOCKED/NOT RUN a pass.

## 8. Questions and ambiguity

Ask short, specific questions before coding when an essential requirement is ambiguous. Do not guess project facts, device support, team capability, scientific assumptions, units, error semantics, licensing or security posture. For known project context, use repository evidence instead of asking the owner to repeat it. Record unanswered profile fields as TBD and continue only with work that does not depend on them.

## 9. Response format

- Start with the direct answer.
- For large tasks, give a short ordered plan and components involved.
- Be concise; use bullets and code blocks.
- Identify language and file for each code block.
- Provide complete runnable code and build/test configuration when code is requested.
- State flaws directly and offer a safer/better option with reasons.
- End with **Check** and **Next step**, including open questions only when they block the next action.

## 10. Project-specific guardrails remain in force

- `NORTH_STAR.md` remains the mission authority; this standard does not broaden clinical scope.
- Research Mode only in public builds. Clinical Decision Support remains disabled.
- No patient/PHI data or clinical recommendations before the existing P0 gate.
- No diagnosis, treatment, dosing, pathogenicity or efficacy claims without the applicable validation and governance.
- No runtime executable downloads, hidden telemetry or unreviewed dependencies.
- Follow D-016 build/test/fix/evidence cycle and the owner's current **R → S → I → P → G → U** sequencing instruction (D-023). Do not work tracks in parallel unless the owner changes that instruction. Existing partial U0–U3 work is retained as pre-existing baseline. G's bounded engineering gate was assessed on 2026-11-17; Track U has started and follows its own two-step gate. G's independent/operational obligations remain carry-forward.
- The owner’s two-step rule applies to each track, including G and U: Step 1 documented base implementation; Step 2 integration audit, tests and corrections. Report percentages only after that track's two-step gate, with the denominator clearly stated.
