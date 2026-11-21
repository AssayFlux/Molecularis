# ADR-0001: All-Device Platform Architecture

- Status: Accepted for Alpha planning
- Date: 2026-11-21
- Decision owner: Project owner
- Context: The prior project North Star described an Android-native scientific workbench. The owner explicitly changed the product direction to an all-device platform and clarified Alpha as the Git branch name.

## Decision
Use a responsive web application/PWA as the primary client across phone, tablet and desktop. Provide optional desktop packaging, an opt-in local compute connector, isolated hosted workers and institutional/HPC connectors. Keep scientific execution outside the browser for native/heavy workloads.

## Language ownership
C++, Rust and Python are preferred core languages. TypeScript/JavaScript supports the browser/PWA client. Cross-component contracts are versioned and language-neutral.

## Consequences
- Android-native product development is retired.
- Existing Android work is audited and migrated; scientific logic and user data are not discarded.
- Platform boundaries, data model, job lifecycle and provenance become shared contracts.
- Local and remote compute require explicit authorization, resource controls and audit.
- All advertised scientific features require evidence and research-use limitations.

## Alternatives considered
- Android-first with optional desktop: rejected by explicit owner direction.
- Desktop-only: rejected because the product must support phones and tablets.
- Browser-only execution: rejected for native and heavy scientific workloads due to security and resource constraints.

## Revisit when
A material platform constraint, security issue, accessibility finding or owner direction requires architecture revision.