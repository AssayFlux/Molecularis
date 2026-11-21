# Alpha Test Strategy

## Test layers
1. Static analysis, formatting and dependency/license checks.
2. Unit tests for domain logic, parsers, serializers and numerical routines.
3. Contract tests across Python, Rust, C++ and TypeScript.
4. API and database integration tests.
5. Worker isolation, quotas, cancellation, retry and artifact-integrity tests.
6. Desktop application end-to-end tests on Linux, Windows and macOS, including install/upgrade/uninstall and offline workflows.
7. Mobile application tests on Android and iOS/iPadOS, including lifecycle, permissions, storage and offline behaviour.
8. Optional web companion tests only after that product is approved.
9. Scientific reference tests and benchmark suites.
10. Security tests: authorization, path traversal, archive bombs, SSRF, injection, deserialization, secret leakage and sandbox escape attempts.
11. Backup/restore, upgrade, migration and rollback exercises.

## Cross-device matrix
Test desktop keyboard/pointer/window management and native filesystem behaviour on Linux, Windows and macOS; test touch, rotation, screen readers, lifecycle and permission flows on Android and iOS/iPadOS. Across all targets test reduced motion, zoom/reflow, offline transitions, reconnect/sync where enabled, large files, interruption recovery and long-running job visibility.

## Scientific test requirements
For each engine record reference dataset and rights, reference tool/version, expected result, tolerance, numerical precision, random seed, hardware/runtime profile and known limitations. Avoid tests that only assert a non-empty output.

## Performance
Establish measured baselines before SLOs. Track client load and interaction, API latency, queue wait, execution throughput, memory, CPU/GPU utilization, artifact transfer and large-result rendering.

## Release evidence
Exact commit SHA, CI workflow URL, environment/toolchain, test command, result summary, skipped tests, known failures and reviewer are recorded for every milestone. A build passing is not scientific validation or platform support evidence.