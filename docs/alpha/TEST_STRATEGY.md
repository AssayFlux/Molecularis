# Alpha Test Strategy

## Test layers
1. Static analysis, formatting and dependency/license checks.
2. Unit tests for domain logic, parsers, serializers and numerical routines.
3. Contract tests across Python, Rust, C++ and TypeScript.
4. API and database integration tests.
5. Worker isolation, quotas, cancellation, retry and artifact-integrity tests.
6. Browser end-to-end tests for responsive layouts and critical workflows.
7. Device/browser tests across phone, tablet, laptop and desktop classes.
8. Scientific reference tests and benchmark suites.
9. Security tests: authorization, path traversal, archive bombs, SSRF, injection, deserialization, secret leakage and sandbox escape attempts.
10. Backup/restore, upgrade, migration and rollback exercises.

## Cross-device matrix
Test touch and pointer input, keyboard navigation, screen readers, reduced motion, zoom/reflow, offline transitions, reconnect/sync, large files, upload interruption, session expiry and long-running job visibility.

## Scientific test requirements
For each engine record reference dataset and rights, reference tool/version, expected result, tolerance, numerical precision, random seed, hardware/runtime profile and known limitations. Avoid tests that only assert a non-empty output.

## Performance
Establish measured baselines before SLOs. Track client load and interaction, API latency, queue wait, execution throughput, memory, CPU/GPU utilization, artifact transfer and large-result rendering.

## Release evidence
Exact commit SHA, CI workflow URL, environment/toolchain, test command, result summary, skipped tests, known failures and reviewer are recorded for every milestone. A build passing is not scientific validation or platform support evidence.