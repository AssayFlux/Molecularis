# Molecularis Documentation Index

This index has one implementation authority: [MASTER_PLAN.md](MASTER_PLAN.md). Older plans are historical evidence and are not parallel execution instructions.

## Current project authority

| Purpose | Canonical document |
|---|---|
| Product direction | [North Star](../NORTH_STAR.md) |
| Complete implementation plan and phase gates | [Master Plan](MASTER_PLAN.md) |
| Exact repository inventory and gaps | [Repository Baseline](REPOSITORY_BASELINE.md) |
| Existing capabilities and migration mapping | [Capability Status](CAPABILITY_STATUS.md) |
| Superseded plan/document map | [Plan Retirement](PLAN_RETIREMENT.md) |
| Approved decisions and supersessions | [Decision Log](../DECISIONS.md) |
| Current concise roadmap pointer | [Roadmap](../ROADMAP.md) |

## Engineering standards and contracts

- [Architecture](architecture.md)
- [Engineering integration standard](ENGINEERING_INTEGRATION_STANDARD.md)
- [API/job contracts](alpha/API_AND_JOB_CONTRACTS.md)
- [Data model](alpha/DATA_MODEL.md)
- [Language strategy](alpha/LANGUAGE_STRATEGY.md) — supporting reference; framework selection remains open
- [Security threat model](security-threat-model.md)
- [Accessibility test plan](accessibility-test-plan.md)
- [Scientific rulebook plan](SCIENTIFIC_RULEBOOK_PLAN.md)
- [Scientific validation plan](SCIENTIFIC_VALIDATION_PLAN.md)

## Scientific integrations and validation

- [Third-party integration register](THIRD_PARTY_INTEGRATION_REGISTER.md)
- [Scientific engine integration matrix](SCIENTIFIC_ENGINE_INTEGRATION_MATRIX.md)
- [Engine runtime matrix](ENGINE_RUNTIME_MATRIX.md)
- [Scientific engine decisions](scientific-engine-decisions.md)
- [Validation index](../validation/README.md)
- [CI build evidence ledger](ci-build-evidence.md)

## Design and product experience

- [UI specification](ui/ui-spec.md)
- [Visual design system](ui/molecularis-visual-design-system.md)
- [Screen map](ui/screen-map.md)
- [Device matrix](ui/device-matrix.md)
- [Component catalogue](ui/component-catalogue.md)

## Historical and specialist evidence

The following records remain available for traceability, compatibility and specialist requirements. They do not supersede the Master Plan:

- Original source master: [docs/origin](origin/)
- Historical R/S/I/P/G/U track plans and audits: [track records](.)
- Dated repository audits, closure reports and CI evidence.
- [Decision log](../DECISIONS.md), [session log](../SESSION_LOG.md), and [change log](../CHANGELOG.md).

## Status discipline

Source presence, automated tests, reference validation, platform verification, independent review and release approval are separate states. Never upgrade a capability's status without evidence for that exact state. A green CI run does not by itself establish scientific validity, device support, security clearance or release readiness.
